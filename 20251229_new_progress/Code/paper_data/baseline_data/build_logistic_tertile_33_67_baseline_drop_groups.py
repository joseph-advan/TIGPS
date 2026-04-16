from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
TEST_SIZE = 0.2
LOGIT_CS = np.logspace(-4, 4, 41)
LOW_Q = 0.33
HIGH_Q = 0.67

# Keep the same group setups used by previous baseline scripts.
W2_FEATURE_GROUP_IDS = [
    "v57",
    "v27",
    "v42",
    "v6",
    "v5",
    "v49",
    "v38",
    "v40",
    "v52",
    "v50",
    "v28",
    "v25",
    "v34",
    "v19",
    "v1",
    "v3",
    "v23",
    "v36",
    "v521",
    "v26",
    "v54",
    "v51",
    "v22",
]

W3_FEATURE_GROUP_IDS = [
    "55",
    "28",
    "39",
    "5",
    "4",
    "48",
    "34",
    "36",
    "52",
    "49",
    "29",
    "26",
    "30",
    "11",
    "1",
    "3",
    "59",
    "25",
    "32",
    "51",
    "27",
    "53",
    "50",
    "24",
]

W2_TARGET_GROUP_ID = "v55"
W3_TARGET_GROUP_ID = "54"

W2_DROP_GROUP_IDS = {"v57", "v52", "v50", "v51"}
W3_DROP_GROUP_IDS = {"55", "52", "49", "50"}

W2_FEATURE_GROUP_IDS_DROP = [g for g in W2_FEATURE_GROUP_IDS if g not in W2_DROP_GROUP_IDS]
W3_FEATURE_GROUP_IDS_DROP = [g for g in W3_FEATURE_GROUP_IDS if g not in W3_DROP_GROUP_IDS]


THIS_FILE = Path(__file__).resolve()
OUT_DIR = THIS_FILE.parent
BASE_DIR = THIS_FILE.parents[3]

W2_DATA_PATH = BASE_DIR / r"Data\2024data\TIGPS_W2_studentdata_ver11.csv"
W3_DATA_PATH = BASE_DIR / r"Data\2025data\W3_studentdata_ver10.csv"
MERGED_PATH_CANDIDATES = [
    BASE_DIR / r"Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
    BASE_DIR / r"Code\EDA\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
]

SUMMARY_CSV_PATH = OUT_DIR / "baseline_logistic_tertile_33_67_drop_groups_classification_summary.csv"
SUMMARY_MD_PATH = OUT_DIR / "baseline_logistic_tertile_33_67_drop_groups_classification_summary.md"
DETAIL_JSON_PATH = OUT_DIR / "baseline_logistic_tertile_33_67_drop_groups_classification_details.json"


def pick_first_existing_path(candidates: list[Path]) -> Path:
    for p in candidates:
        if p.exists():
            return p
    candidate_str = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(f"No mapping file found. Tried:\n{candidate_str}")


def normalize_student_id(df: pd.DataFrame) -> pd.DataFrame:
    if "student_id" not in df.columns:
        raise KeyError("Column 'student_id' is required.")
    out = df.copy()
    sid = out["student_id"].astype(str).str.strip()
    sid = sid.replace({"": np.nan, "nan": np.nan, "None": np.nan, "<NA>": np.nan})
    out["student_id"] = sid
    return out


def resolve_group_items(merged: pd.DataFrame, year: str, group_id: str) -> list[str]:
    sub = merged[
        (merged["Year"].astype(str).str.strip() == str(year).strip())
        & (merged["Group_ID"].astype(str).str.strip() == str(group_id).strip())
    ]
    return sub["Question_ID"].dropna().astype(str).str.strip().tolist()


def candidate_item_names(item: str) -> list[str]:
    out = [item]
    if "-" in item:
        out.append(item.replace("-", "_"))
    if "_" in item:
        out.append(item.replace("_", "-"))
    return list(dict.fromkeys(out))


def resolve_existing_items(df: pd.DataFrame, items: list[str]) -> tuple[list[str], list[str]]:
    colset = set(df.columns)
    found: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()

    for item in items:
        actual = None
        for cand in candidate_item_names(item):
            if cand in colset:
                actual = cand
                break
        if actual is None:
            missing.append(item)
            continue
        if actual not in seen:
            found.append(actual)
            seen.add(actual)
    return found, missing


def compute_group_score(
    df: pd.DataFrame, items: list[str], agg: str = "mean"
) -> tuple[pd.Series, list[str], list[str]]:
    found, missing = resolve_existing_items(df, items)
    if not found:
        return pd.Series(np.nan, index=df.index, dtype=float), found, missing
    data = df[found].apply(pd.to_numeric, errors="coerce")
    if agg == "mean":
        score = data.mean(axis=1, skipna=True)
    elif agg == "sum":
        score = data.sum(axis=1, skipna=True)
    else:
        raise ValueError(f"Unsupported agg='{agg}'. Use 'mean' or 'sum'.")
    score[data.notna().sum(axis=1) == 0] = np.nan
    return score, found, missing


def build_feature_table(
    df: pd.DataFrame,
    merged: pd.DataFrame,
    year: str,
    feature_group_ids: list[str],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    table = pd.DataFrame(index=df.index)
    table["student_id"] = df["student_id"]

    requested = list(feature_group_ids)
    used: list[str] = []
    skipped_no_mapping_items: list[str] = []
    skipped_no_columns: list[str] = []
    partial_missing_columns: dict[str, list[str]] = {}
    group_items_used: dict[str, list[str]] = {}

    for gid in requested:
        items = resolve_group_items(merged, year=year, group_id=gid)
        if not items:
            skipped_no_mapping_items.append(gid)
            continue

        score, found, missing = compute_group_score(df, items, agg="mean")
        if not found:
            skipped_no_columns.append(gid)
            continue

        if missing:
            partial_missing_columns[gid] = missing
        used.append(gid)
        group_items_used[gid] = found
        table[f"group_{gid}"] = score

    meta = {
        "feature_year": year,
        "feature_group_ids_requested": requested,
        "feature_group_ids_used": used,
        "skipped_feature_groups_no_mapping_items": skipped_no_mapping_items,
        "skipped_feature_groups_no_columns": skipped_no_columns,
        "partial_feature_groups_missing_columns": partial_missing_columns,
        "group_items_used": group_items_used,
    }
    return table, meta


def build_target_table_tertile(
    df: pd.DataFrame,
    merged: pd.DataFrame,
    year: str,
    target_group_id: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    table = pd.DataFrame(index=df.index)
    table["student_id"] = df["student_id"]

    target_items = resolve_group_items(merged, year=year, group_id=target_group_id)
    if not target_items:
        raise ValueError(f"No mapping items found for target group {target_group_id} in year {year}.")

    score, found, missing = compute_group_score(df, target_items, agg="sum")
    if not found:
        raise ValueError(
            f"Target group {target_group_id} in year {year} has no usable columns in dataset."
        )

    valid_score = score.dropna()
    if valid_score.empty:
        raise ValueError(f"Target group {target_group_id} in year {year} is all missing.")

    q33 = float(valid_score.quantile(LOW_Q))
    q67 = float(valid_score.quantile(HIGH_Q))

    target_class = pd.Series(np.nan, index=score.index, dtype=float)
    target_class.loc[score < q33] = 0.0
    target_class.loc[(score >= q33) & (score < q67)] = 1.0
    target_class.loc[score >= q67] = 2.0

    table["target_score"] = score
    table["target_class"] = target_class

    class_counts = (
        target_class.dropna().astype(int).value_counts().sort_index().to_dict()
    )

    meta = {
        "target_year": year,
        "target_group_id": target_group_id,
        "target_score_aggregation": "sum",
        "target_items_requested": target_items,
        "target_items_used": found,
        "target_items_missing_columns": missing,
        "target_cutoff_q33": q33,
        "target_cutoff_q67": q67,
        "target_class_counts": class_counts,
    }
    return table, meta


def dedup_by_student_id(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.loc[out["student_id"].notna()].copy()
    out = out.drop_duplicates(subset=["student_id"], keep="first").copy()
    return out


def metric_multiclass(y_true: np.ndarray, y_pred: np.ndarray, prob: np.ndarray) -> dict[str, float]:
    out: dict[str, float] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }
    try:
        out["macro_auc_ovr"] = float(roc_auc_score(y_true, prob, multi_class="ovr", average="macro"))
    except Exception:
        out["macro_auc_ovr"] = float("nan")
    return out


def run_logistic_tertile_classification(model_df: pd.DataFrame, feature_cols: list[str]) -> dict[str, Any]:
    y = model_df["target_class"].astype(int)
    X = model_df[feature_cols].copy()

    non_empty_features = [c for c in feature_cols if X[c].notna().sum() > 0]
    dropped_all_missing = [c for c in feature_cols if c not in non_empty_features]
    if not non_empty_features:
        raise ValueError("No usable feature columns remain after all-missing check.")
    X = X[non_empty_features]
    feature_cols = non_empty_features

    if y.nunique(dropna=True) < 3:
        raise ValueError("Target has fewer than 3 classes after filtering.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "logit",
                LogisticRegressionCV(
                    Cs=LOGIT_CS,
                    cv=cv,
                    max_iter=6000,
                    solver="lbfgs",
                    penalty="l2",
                    scoring="accuracy",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)

    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)
    prob_train = model.predict_proba(X_train)
    prob_test = model.predict_proba(X_test)
    train_cls = metric_multiclass(y_train.to_numpy(), pred_train, prob_train)
    test_cls = metric_multiclass(y_test.to_numpy(), pred_test, prob_test)

    c_raw = np.asarray(model.named_steps["logit"].C_).reshape(-1)
    c_selected_mean = float(np.mean(c_raw))
    c_selected_raw = [float(v) for v in c_raw.tolist()]

    fixed = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "logit",
                LogisticRegression(
                    C=c_selected_mean,
                    max_iter=6000,
                    solver="lbfgs",
                    penalty="l2",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    cv_scores = cross_validate(
        fixed,
        X,
        y,
        cv=cv,
        scoring=("accuracy", "f1_macro", "roc_auc_ovr"),
        n_jobs=None,
    )

    class_counts = y.value_counts().sort_index().to_dict()

    out = {
        "n_rows_modeling": int(len(model_df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_features_used": int(len(feature_cols)),
        "dropped_all_missing_feature_cols": dropped_all_missing,
        "c_selected_mean": c_selected_mean,
        "c_selected_raw": c_selected_raw,
        "train_accuracy": train_cls["accuracy"],
        "train_macro_f1": train_cls["macro_f1"],
        "train_macro_auc_ovr": train_cls["macro_auc_ovr"],
        "test_accuracy": test_cls["accuracy"],
        "test_macro_f1": test_cls["macro_f1"],
        "test_macro_auc_ovr": test_cls["macro_auc_ovr"],
        "cv5_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
        "cv5_accuracy_std": float(np.std(cv_scores["test_accuracy"], ddof=1)),
        "cv5_macro_f1_mean": float(np.mean(cv_scores["test_f1_macro"])),
        "cv5_macro_f1_std": float(np.std(cv_scores["test_f1_macro"], ddof=1)),
        "cv5_macro_auc_ovr_mean": float(np.mean(cv_scores["test_roc_auc_ovr"])),
        "cv5_macro_auc_ovr_std": float(np.std(cv_scores["test_roc_auc_ovr"], ddof=1)),
        "class0_count": int(class_counts.get(0, 0)),
        "class1_count": int(class_counts.get(1, 0)),
        "class2_count": int(class_counts.get(2, 0)),
    }
    return out


def run_scenario(
    *,
    scenario_name: str,
    feature_df_raw: pd.DataFrame,
    target_df_raw: pd.DataFrame,
    merged: pd.DataFrame,
    feature_year: str,
    target_year: str,
    feature_group_ids: list[str],
    target_group_id: str,
    pair_by_student_id: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_table, feature_meta = build_feature_table(
        feature_df_raw, merged, year=feature_year, feature_group_ids=feature_group_ids
    )
    target_table, target_meta = build_target_table_tertile(
        target_df_raw, merged, year=target_year, target_group_id=target_group_id
    )

    used_group_ids = feature_meta["feature_group_ids_used"]
    feature_cols = [f"group_{gid}" for gid in used_group_ids]
    if not feature_cols:
        raise ValueError(f"{scenario_name}: no usable feature groups.")

    if pair_by_student_id:
        x_df = dedup_by_student_id(feature_table[["student_id"] + feature_cols])
        y_df = dedup_by_student_id(target_table[["student_id", "target_score", "target_class"]])
        model_df = x_df.merge(y_df, on="student_id", how="inner")
    else:
        model_df = pd.DataFrame(index=feature_table.index)
        model_df["student_id"] = feature_table["student_id"]
        for col in feature_cols:
            model_df[col] = feature_table[col]
        model_df["target_score"] = target_table["target_score"]
        model_df["target_class"] = target_table["target_class"]

    model_df = model_df.loc[model_df["target_class"].notna()].copy()
    metrics = run_logistic_tertile_classification(model_df=model_df, feature_cols=feature_cols)

    scenario_detail: dict[str, Any] = {
        "scenario": scenario_name,
        "feature_year": feature_year,
        "target_year": target_year,
        "pair_by_student_id": pair_by_student_id,
        "feature_meta": feature_meta,
        "target_meta": target_meta,
        "metrics": metrics,
    }

    summary_row: dict[str, Any] = {
        "scenario": scenario_name,
        "feature_year": feature_year,
        "target_year": target_year,
        "target_group_id": target_group_id,
        "target_cutoff_q33": target_meta["target_cutoff_q33"],
        "target_cutoff_q67": target_meta["target_cutoff_q67"],
        "n_rows_modeling": metrics["n_rows_modeling"],
        "n_train": metrics["n_train"],
        "n_test": metrics["n_test"],
        "n_features_requested": len(feature_group_ids),
        "n_features_used": metrics["n_features_used"],
        "class0_count": metrics["class0_count"],
        "class1_count": metrics["class1_count"],
        "class2_count": metrics["class2_count"],
        "c_selected_mean": metrics["c_selected_mean"],
        "test_accuracy": metrics["test_accuracy"],
        "test_macro_f1": metrics["test_macro_f1"],
        "test_macro_auc_ovr": metrics["test_macro_auc_ovr"],
        "cv5_accuracy_mean": metrics["cv5_accuracy_mean"],
        "cv5_macro_f1_mean": metrics["cv5_macro_f1_mean"],
        "cv5_macro_auc_ovr_mean": metrics["cv5_macro_auc_ovr_mean"],
        "skipped_feature_groups_no_mapping_items": ";".join(
            feature_meta["skipped_feature_groups_no_mapping_items"]
        ),
        "skipped_feature_groups_no_columns": ";".join(feature_meta["skipped_feature_groups_no_columns"]),
        "dropped_all_missing_feature_cols": ";".join(metrics["dropped_all_missing_feature_cols"]),
    }

    return summary_row, scenario_detail


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    merged_path = pick_first_existing_path(MERGED_PATH_CANDIDATES)
    w2_raw = normalize_student_id(pd.read_csv(W2_DATA_PATH, low_memory=False))
    w3_raw = normalize_student_id(pd.read_csv(W3_DATA_PATH, low_memory=False))

    merged = pd.read_csv(merged_path, dtype=str)
    for c in ["Year", "Group_ID", "Question_ID"]:
        if c in merged.columns:
            merged[c] = merged[c].astype(str).str.strip()

    scenarios = [
        {
            "scenario_name": "w2_self",
            "feature_df_raw": w2_raw,
            "target_df_raw": w2_raw,
            "feature_year": "W2",
            "target_year": "W2",
            "feature_group_ids": W2_FEATURE_GROUP_IDS_DROP,
            "target_group_id": W2_TARGET_GROUP_ID,
            "pair_by_student_id": False,
        },
        {
            "scenario_name": "w3_self",
            "feature_df_raw": w3_raw,
            "target_df_raw": w3_raw,
            "feature_year": "W3",
            "target_year": "W3",
            "feature_group_ids": W3_FEATURE_GROUP_IDS_DROP,
            "target_group_id": W3_TARGET_GROUP_ID,
            "pair_by_student_id": False,
        },
        {
            "scenario_name": "w2_predict_w3",
            "feature_df_raw": w2_raw,
            "target_df_raw": w3_raw,
            "feature_year": "W2",
            "target_year": "W3",
            "feature_group_ids": W2_FEATURE_GROUP_IDS_DROP,
            "target_group_id": W3_TARGET_GROUP_ID,
            "pair_by_student_id": True,
        },
    ]

    summary_rows: list[dict[str, Any]] = []
    details: dict[str, Any] = {
        "settings": {
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
            "logit_cs_count": int(len(LOGIT_CS)),
            "target_split": "sum score tertile by quantiles 0.33 / 0.67",
            "drop_groups": {
                "w2_feature_group_ids_dropped": sorted(W2_DROP_GROUP_IDS),
                "w3_feature_group_ids_dropped": sorted(W3_DROP_GROUP_IDS),
            },
            "w2_data_path": str(W2_DATA_PATH),
            "w3_data_path": str(W3_DATA_PATH),
            "merged_path": str(merged_path),
            "note": (
                "Baseline uses whole-group scores only (no subscale splitting). "
                "Specified feature groups are dropped first. "
                "Target is 3-class from sum-score quantiles (33/67) and modeled via multinomial logistic regression."
            ),
        },
        "scenarios": {},
    }

    for config in scenarios:
        summary_row, detail = run_scenario(merged=merged, **config)
        summary_rows.append(summary_row)
        details["scenarios"][config["scenario_name"]] = detail

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df[
        [
            "scenario",
            "feature_year",
            "target_year",
            "target_group_id",
            "target_cutoff_q33",
            "target_cutoff_q67",
            "n_rows_modeling",
            "n_train",
            "n_test",
            "n_features_requested",
            "n_features_used",
            "class0_count",
            "class1_count",
            "class2_count",
            "c_selected_mean",
            "test_accuracy",
            "test_macro_f1",
            "test_macro_auc_ovr",
            "cv5_accuracy_mean",
            "cv5_macro_f1_mean",
            "cv5_macro_auc_ovr_mean",
            "skipped_feature_groups_no_mapping_items",
            "skipped_feature_groups_no_columns",
            "dropped_all_missing_feature_cols",
        ]
    ]
    summary_df.to_csv(SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")

    with open(DETAIL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    with open(SUMMARY_MD_PATH, "w", encoding="utf-8") as f:
        f.write("# Baseline: Logistic 3-Class (33/67 Quantile Split, Drop Groups Version)\n\n")
        f.write(f"- W2 data: `{W2_DATA_PATH}`\n")
        f.write(f"- W3 data: `{W3_DATA_PATH}`\n")
        f.write(f"- Mapping: `{merged_path}`\n")
        f.write(f"- Dropped W2 feature groups: `{', '.join(sorted(W2_DROP_GROUP_IDS))}`\n")
        f.write(f"- Dropped W3 feature groups: `{', '.join(sorted(W3_DROP_GROUP_IDS))}`\n")
        f.write("- Rule: target score is total sum, split into 3 classes by q33/q67, then modeled by multinomial logistic regression.\n\n")
        f.write("## Summary\n\n")
        f.write(
            "| scenario | q33 | q67 | test_accuracy | test_macro_f1 | test_macro_auc_ovr | cv5_accuracy_mean | cv5_macro_f1_mean | cv5_macro_auc_ovr_mean | n_rows_modeling | n_features_used |\n"
        )
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for _, row in summary_df.iterrows():
            f.write(
                f"| {row['scenario']} | "
                f"{row['target_cutoff_q33']:.4f} | "
                f"{row['target_cutoff_q67']:.4f} | "
                f"{row['test_accuracy']:.6f} | "
                f"{row['test_macro_f1']:.6f} | "
                f"{row['test_macro_auc_ovr']:.6f} | "
                f"{row['cv5_accuracy_mean']:.6f} | "
                f"{row['cv5_macro_f1_mean']:.6f} | "
                f"{row['cv5_macro_auc_ovr_mean']:.6f} | "
                f"{int(row['n_rows_modeling'])} | "
                f"{int(row['n_features_used'])} |\n"
            )

    print("3-class baseline completed.")
    print(f"Wrote: {SUMMARY_CSV_PATH}")
    print(f"Wrote: {SUMMARY_MD_PATH}")
    print(f"Wrote: {DETAIL_JSON_PATH}")
    print("\n3-class summary table:")
    print(
        summary_df[
            [
                "scenario",
                "test_accuracy",
                "test_macro_f1",
                "test_macro_auc_ovr",
                "cv5_accuracy_mean",
                "cv5_macro_f1_mean",
                "cv5_macro_auc_ovr_mean",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
