from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import shap
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
FEATURE_MAP_PATH = PROJECT_ROOT / r"Code\paper_data\features_used\W2W3_Features.csv"
OUT_DIR = SCRIPT_DIR / "outputs"
MODEL_OUT = OUT_DIR / "model_results"

# Reuse robust column-resolution helpers from existing pipeline.
CORE_DIR = PROJECT_ROOT / r"Code\paper_data\Interpersonal_features"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
import run_interpersonal_feature_logistic_comparison as core  # noqa: E402


RANDOM_STATE = 42
TEST_SIZE = 0.2
CS_GRID = np.logspace(-4, 4, 41)

EXCLUDE_W3_GROUPS = {"55", "52", "49", "50"}
EXCLUDE_W2_GROUPS = {"v57", "v52", "v50", "v51"}


@dataclass(frozen=True)
class Scenario:
    name: str
    feature_year: str
    target_year: str
    target_group_id: str


SCENARIOS = [
    Scenario(name="w2_predict_w2", feature_year="W2", target_year="W2", target_group_id="v55"),
    Scenario(name="w3_predict_w3", feature_year="W3", target_year="W3", target_group_id="54"),
    Scenario(name="w2_predict_w3", feature_year="W2", target_year="W3", target_group_id="54"),
]

MODEL_CONFIGS = [
    {"model_type": "ridge", "penalty": "l2", "solver": "lbfgs", "max_iter": 5000},
    {"model_type": "lasso", "penalty": "l1", "solver": "saga", "max_iter": 8000},
]


def _ensure_dirs() -> None:
    MODEL_OUT.mkdir(parents=True, exist_ok=True)


def _safe_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(roc_auc_score(y_true, y_prob))


def _format_md_table(df: pd.DataFrame, cols: list[str]) -> str:
    out = df[cols].copy()
    for c in out.columns:
        if pd.api.types.is_float_dtype(out[c]):
            out[c] = out[c].map(lambda v: f"{v:.6f}")
    return out.to_markdown(index=False)


def _load_feature_group_map() -> tuple[list[str], list[str], pd.DataFrame]:
    fmap = pd.read_csv(FEATURE_MAP_PATH, dtype=str, encoding="utf-8-sig")
    fmap = fmap.rename(columns={c: c.strip() for c in fmap.columns})
    required = {"W3_Group_ID", "W2_Group_ID"}
    miss = required - set(fmap.columns)
    if miss:
        raise KeyError(f"Missing columns in {FEATURE_MAP_PATH}: {miss}")

    w2_groups = (
        fmap["W2_Group_ID"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", np.nan)
        .dropna()
        .unique()
        .tolist()
    )
    w3_groups = (
        fmap["W3_Group_ID"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", np.nan)
        .dropna()
        .unique()
        .tolist()
    )

    w2_groups = [g for g in w2_groups if g not in EXCLUDE_W2_GROUPS]
    w3_groups = [g for g in w3_groups if g not in EXCLUDE_W3_GROUPS]
    return w2_groups, w3_groups, fmap


def _run_one_model(
    model_type: str,
    penalty: str,
    solver: str,
    max_iter: int,
    model_df: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    x_full = model_df[feature_cols].apply(pd.to_numeric, errors="coerce")
    usable_cols = [c for c in x_full.columns if x_full[c].notna().any()]
    dropped_all_na = [c for c in feature_cols if c not in usable_cols]
    if not usable_cols:
        raise RuntimeError("All feature columns are all-NA after numeric conversion.")

    x = x_full[usable_cols]
    y = model_df["target_class"].astype(int).to_numpy()
    if len(np.unique(y)) < 2:
        raise RuntimeError("Target has only one class after filtering.")

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    tune_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegressionCV(
                    Cs=CS_GRID,
                    cv=5,
                    penalty=penalty,
                    solver=solver,
                    scoring="roc_auc",
                    max_iter=max_iter,
                    n_jobs=1,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    tune_pipe.fit(x_train, y_train)
    best_c = float(tune_pipe.named_steps["model"].C_[0])

    final_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    C=best_c,
                    penalty=penalty,
                    solver=solver,
                    max_iter=max_iter,
                    n_jobs=1,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    final_pipe.fit(x_train, y_train)

    y_train_pred = final_pipe.predict(x_train)
    y_test_pred = final_pipe.predict(x_test)
    y_train_prob = final_pipe.predict_proba(x_train)[:, 1]
    y_test_prob = final_pipe.predict_proba(x_test)[:, 1]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_validate(
        final_pipe,
        x,
        y,
        cv=cv,
        scoring=["accuracy", "f1", "precision", "recall", "roc_auc"],
        n_jobs=1,
        return_train_score=False,
    )

    metrics = {
        "model_type": model_type,
        "n_rows_modeling": int(len(model_df)),
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "n_features_requested": int(len(feature_cols)),
        "n_features_used": int(len(usable_cols)),
        "dropped_all_na_features": ";".join(dropped_all_na),
        "c_selected": best_c,
        "train_accuracy": float(accuracy_score(y_train, y_train_pred)),
        "train_f1": float(f1_score(y_train, y_train_pred, zero_division=0)),
        "train_precision": float(precision_score(y_train, y_train_pred, zero_division=0)),
        "train_recall": float(recall_score(y_train, y_train_pred, zero_division=0)),
        "train_auc": _safe_auc(y_train, y_train_prob),
        "test_accuracy": float(accuracy_score(y_test, y_test_pred)),
        "test_f1": float(f1_score(y_test, y_test_pred, zero_division=0)),
        "test_precision": float(precision_score(y_test, y_test_pred, zero_division=0)),
        "test_recall": float(recall_score(y_test, y_test_pred, zero_division=0)),
        "test_auc": _safe_auc(y_test, y_test_prob),
        "cv5_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
        "cv5_accuracy_std": float(np.std(cv_scores["test_accuracy"])),
        "cv5_f1_mean": float(np.mean(cv_scores["test_f1"])),
        "cv5_f1_std": float(np.std(cv_scores["test_f1"])),
        "cv5_precision_mean": float(np.mean(cv_scores["test_precision"])),
        "cv5_precision_std": float(np.std(cv_scores["test_precision"])),
        "cv5_recall_mean": float(np.mean(cv_scores["test_recall"])),
        "cv5_recall_std": float(np.std(cv_scores["test_recall"])),
        "cv5_auc_mean": float(np.mean(cv_scores["test_roc_auc"])),
        "cv5_auc_std": float(np.std(cv_scores["test_roc_auc"])),
    }

    # SHAP for linear logistic model on standardized feature space.
    imputer = final_pipe.named_steps["imputer"]
    scaler = final_pipe.named_steps["scaler"]
    lr = final_pipe.named_steps["model"]
    x_train_proc = scaler.transform(imputer.transform(x_train[usable_cols]))
    x_test_proc = scaler.transform(imputer.transform(x_test[usable_cols]))

    explainer = shap.LinearExplainer(lr, x_train_proc)
    shap_values = explainer(x_test_proc)
    shap_abs_mean = np.abs(shap_values.values).mean(axis=0)

    coef = lr.coef_.ravel()
    coef_abs = np.abs(coef)
    coef_abs_sum = float(coef_abs.sum()) if float(coef_abs.sum()) > 0 else 1.0

    shap_df = pd.DataFrame(
        {
            "feature": usable_cols,
            "shap_abs_mean": shap_abs_mean,
            "coef": coef,
            "coef_abs": coef_abs,
            "relative_importance_pct": coef_abs / coef_abs_sum * 100.0,
            "coef_direction": np.where(coef >= 0, "positive", "negative"),
        }
    ).sort_values("shap_abs_mean", ascending=False)

    return metrics, shap_df.reset_index(drop=True), pd.DataFrame({"feature": usable_cols})


def main() -> None:
    _ensure_dirs()

    merged_path = core.pick_first_existing_path(core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")
    w2_raw = core.normalize_student_id(pd.read_csv(core.W2_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    w3_raw = core.normalize_student_id(pd.read_csv(core.W3_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))

    w2_groups, w3_groups, fmap = _load_feature_group_map()
    year_groups = {"W2": w2_groups, "W3": w3_groups}
    year_raw = {"W2": w2_raw, "W3": w3_raw}

    summary_rows: list[dict[str, Any]] = []
    shap_rows: list[dict[str, Any]] = []
    relative_rows: list[dict[str, Any]] = []
    details_records: list[dict[str, Any]] = []

    for sc in SCENARIOS:
        data_df = year_raw[sc.feature_year]
        target_df = year_raw[sc.target_year]

        group_ids = [g for g in year_groups[sc.feature_year] if g != sc.target_group_id]
        feat_cols, missing_by_group = core.collect_feature_columns(
            merged=merged,
            data_year=sc.feature_year,
            data_df=data_df,
            group_ids=group_ids,
        )

        target_table, target_meta = core.build_target_table_median(
            merged=merged,
            target_year=sc.target_year,
            target_group_id=sc.target_group_id,
            target_df=target_df,
        )
        model_df = core.prepare_model_table(
            features_df=data_df[["student_id"] + feat_cols],
            target_table=target_table,
            feature_cols=feat_cols,
        )

        for mc in MODEL_CONFIGS:
            metrics, shap_df, used_df = _run_one_model(
                model_type=mc["model_type"],
                penalty=mc["penalty"],
                solver=mc["solver"],
                max_iter=mc["max_iter"],
                model_df=model_df,
                feature_cols=feat_cols,
            )

            summary_rows.append(
                {
                    "scenario": sc.name,
                    "feature_year": sc.feature_year,
                    "target_year": sc.target_year,
                    "target_group_id": sc.target_group_id,
                    "n_feature_groups_requested": len(group_ids),
                    "n_feature_columns_requested": len(feat_cols),
                    "target_median_cutoff": target_meta["target_median_cutoff"],
                    "target_positive_rate": target_meta["target_positive_rate"],
                    **metrics,
                }
            )

            shap_tmp = shap_df.copy()
            shap_tmp.insert(0, "model_type", mc["model_type"])
            shap_tmp.insert(0, "scenario", sc.name)
            shap_rows.append(shap_tmp)

            rel_tmp = shap_df[["feature", "coef_abs", "relative_importance_pct", "coef_direction"]].copy()
            rel_tmp.insert(0, "model_type", mc["model_type"])
            rel_tmp.insert(0, "scenario", sc.name)
            relative_rows.append(rel_tmp.sort_values("relative_importance_pct", ascending=False))

            details_records.append(
                {
                    "scenario": sc.name,
                    "model_type": mc["model_type"],
                    "feature_year": sc.feature_year,
                    "target_year": sc.target_year,
                    "target_group_id": sc.target_group_id,
                    "target_meta": target_meta,
                    "group_ids_used": group_ids,
                    "missing_by_group": missing_by_group,
                    "n_used_features_after_na_drop": int(len(used_df)),
                    "top10_shap": shap_df.head(10).to_dict(orient="records"),
                    "top10_relative_importance": rel_tmp.sort_values("relative_importance_pct", ascending=False).head(10).to_dict(orient="records"),
                }
            )

    summary_df = pd.DataFrame(summary_rows).sort_values(["scenario", "model_type"]).reset_index(drop=True)
    shap_all_df = pd.concat(shap_rows, ignore_index=True)
    rel_all_df = pd.concat(relative_rows, ignore_index=True)

    summary_csv = MODEL_OUT / "ridge_lasso_three_scenarios_summary.csv"
    shap_csv = MODEL_OUT / "ridge_lasso_three_scenarios_shap_importance.csv"
    rel_csv = MODEL_OUT / "ridge_lasso_three_scenarios_relative_importance.csv"
    details_json = MODEL_OUT / "ridge_lasso_three_scenarios_details.json"
    report_md = MODEL_OUT / "ridge_lasso_three_scenarios_report_zh.md"

    summary_df.to_csv(summary_csv, index=False, encoding="utf-8-sig")
    shap_all_df.to_csv(shap_csv, index=False, encoding="utf-8-sig")
    rel_all_df.to_csv(rel_csv, index=False, encoding="utf-8-sig")
    details_json.write_text(
        json.dumps(
            {
                "paths": {
                    "feature_map_path": str(FEATURE_MAP_PATH),
                    "w2_data_path": str(core.W2_DATA_PATH),
                    "w3_data_path": str(core.W3_DATA_PATH),
                    "mapping_path": str(merged_path),
                },
                "excluded_groups": {
                    "W3": sorted(EXCLUDE_W3_GROUPS),
                    "W2": sorted(EXCLUDE_W2_GROUPS),
                },
                "feature_group_map_n_rows": int(len(fmap)),
                "records": details_records,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8-sig",
    )

    # Build report markdown
    name_map = {
        "w2_predict_w2": "W2 predict W2",
        "w3_predict_w3": "W3 predict W3",
        "w2_predict_w3": "W2 predict W3",
    }
    show = summary_df.copy()
    show["scenario_label"] = show["scenario"].map(name_map)
    show["model_label"] = show["model_type"].str.upper()

    lines: list[str] = []
    lines.append("# Ridge / Lasso / SHAP (Three Scenarios)")
    lines.append("")
    lines.append("## Setup")
    lines.append(f"- Feature map: `{FEATURE_MAP_PATH}`")
    lines.append(f"- Excluded groups (W3): `{sorted(EXCLUDE_W3_GROUPS)}`")
    lines.append(f"- Excluded groups (W2): `{sorted(EXCLUDE_W2_GROUPS)}`")
    lines.append("- Scenarios: W2->W2, W3->W3, W2->W3")
    lines.append("- Models: Ridge (L2 logistic), Lasso (L1 logistic)")
    lines.append("")
    lines.append("## Model Performance")
    lines.append(
        _format_md_table(
            show,
            [
                "scenario_label",
                "model_label",
                "test_accuracy",
                "test_f1",
                "test_precision",
                "test_recall",
                "test_auc",
                "cv5_accuracy_mean",
                "cv5_f1_mean",
                "cv5_precision_mean",
                "cv5_recall_mean",
                "cv5_auc_mean",
                "n_features_used",
            ],
        )
    )
    lines.append("")

    lines.append("## Top SHAP Features (Top 10 per scenario/model)")
    for sc in SCENARIOS:
        lines.append(f"### {name_map[sc.name]}")
        for model_type in ["ridge", "lasso"]:
            sub = shap_all_df[(shap_all_df["scenario"] == sc.name) & (shap_all_df["model_type"] == model_type)].head(10)
            sub = sub.copy()
            sub["model"] = model_type.upper()
            lines.append(f"#### {model_type.upper()}")
            lines.append(_format_md_table(sub, ["feature", "shap_abs_mean", "coef", "relative_importance_pct", "coef_direction"]))
            lines.append("")

    lines.append("## Output Files")
    lines.append(f"- `{summary_csv}`")
    lines.append(f"- `{shap_csv}`")
    lines.append(f"- `{rel_csv}`")
    lines.append(f"- `{details_json}`")
    lines.append(f"- `{report_md}`")
    lines.append("")

    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")

    print("Done.")
    print("Wrote:", summary_csv)
    print("Wrote:", shap_csv)
    print("Wrote:", rel_csv)
    print("Wrote:", details_json)
    print("Wrote:", report_md)


if __name__ == "__main__":
    main()
