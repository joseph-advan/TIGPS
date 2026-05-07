from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
TEST_SIZE = 0.2
LOGIT_CS = np.logspace(-4, 4, 41)

# Keep the same feature-group setups used in existing baseline scripts.
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

W2_DATA_PATH = BASE_DIR / r"Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv"
W3_DATA_PATH = BASE_DIR / r"Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv"
MERGED_PATH_CANDIDATES = [
    BASE_DIR / r"Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
    BASE_DIR / r"Code\EDA\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
]

NO_DROP_SUMMARY_CSV_PATH = (
    OUT_DIR / "baseline_logistic_median_split_classification_summary_with_precision_recall.csv"
)
DROP_SUMMARY_CSV_PATH = (
    OUT_DIR / "baseline_logistic_median_split_drop_groups_classification_summary_with_precision_recall.csv"
)
COMBINED_SUMMARY_CSV_PATH = OUT_DIR / "baseline_logistic_median_split_combined_summary_with_precision_recall.csv"
DETAIL_JSON_PATH = OUT_DIR / "baseline_logistic_median_split_combined_details_with_precision_recall.json"
SUMMARY_MD_PATH = OUT_DIR / "baseline_logistic_median_split_combined_summary_with_precision_recall.md"


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


def build_target_table(
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
    valid_score = score.dropna()
    if valid_score.empty:
        raise ValueError(f"Target group {target_group_id} in year {year} is all missing.")

    cutoff = float(valid_score.median())
    target_binary = (score >= cutoff).astype(float)
    target_binary[score.isna()] = np.nan

    table["target_score"] = score
    table["target_binary"] = target_binary

    meta = {
        "target_year": year,
        "target_group_id": target_group_id,
        "target_score_aggregation": "sum",
        "target_items_requested": target_items,
        "target_items_used": found,
        "target_items_missing_columns": missing,
        "target_median_cutoff": cutoff,
    }
    return table, meta


def dedup_by_student_id(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.loc[out["student_id"].notna()].copy()
    out = out.drop_duplicates(subset=["student_id"], keep="first").copy()
    return out


def metric_classification(y_true: pd.Series, prob: np.ndarray) -> dict[str, float]:
    pred = (prob >= 0.5).astype(int)
    out: dict[str, float] = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
    }
    try:
        out["auc"] = float(roc_auc_score(y_true, prob))
    except Exception:
        out["auc"] = float("nan")
    return out


def run_logistic_binary_classification(model_df: pd.DataFrame, feature_cols: list[str]) -> dict[str, Any]:
    y = model_df["target_binary"].astype(int)
    X = model_df[feature_cols].copy()

    non_empty_features = [c for c in feature_cols if X[c].notna().sum() > 0]
    dropped_all_missing = [c for c in feature_cols if c not in non_empty_features]
    if not non_empty_features:
        raise ValueError("No usable feature columns remain after all-missing check.")

    X = X[non_empty_features]
    feature_cols = non_empty_features

    if y.nunique(dropna=True) < 2:
        raise ValueError("Target has fewer than 2 classes after filtering.")

    stratify = y if y.nunique(dropna=True) == 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=stratify,
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
                    max_iter=5000,
                    solver="lbfgs",
                    penalty="l2",
                    scoring="roc_auc",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)

    prob_train = model.predict_proba(X_train)[:, 1]
    prob_test = model.predict_proba(X_test)[:, 1]
    chosen_c = float(model.named_steps["logit"].C_[0])
    train_cls = metric_classification(y_train, prob_train)
    test_cls = metric_classification(y_test, prob_test)

    fixed = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "logit",
                LogisticRegression(
                    C=chosen_c,
                    max_iter=5000,
                    solver="lbfgs",
                    penalty="l2",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    scoring = {
        "accuracy": "accuracy",
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": make_scorer(recall_score, zero_division=0),
        "f1": make_scorer(f1_score, zero_division=0),
        "roc_auc": "roc_auc",
    }
    cv_scores = cross_validate(
        fixed,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=None,
    )

    out = {
        "n_rows_modeling": int(len(model_df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_features_used": int(len(feature_cols)),
        "dropped_all_missing_feature_cols": dropped_all_missing,
        "c_selected": chosen_c,
        "train_accuracy": train_cls["accuracy"],
        "train_precision": train_cls["precision"],
        "train_recall": train_cls["recall"],
        "train_f1": train_cls["f1"],
        "train_auc": train_cls["auc"],
        "test_accuracy": test_cls["accuracy"],
        "test_precision": test_cls["precision"],
        "test_recall": test_cls["recall"],
        "test_f1": test_cls["f1"],
        "test_auc": test_cls["auc"],
        "cv5_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
        "cv5_accuracy_std": float(np.std(cv_scores["test_accuracy"], ddof=1)),
        "cv5_precision_mean": float(np.mean(cv_scores["test_precision"])),
        "cv5_precision_std": float(np.std(cv_scores["test_precision"], ddof=1)),
        "cv5_recall_mean": float(np.mean(cv_scores["test_recall"])),
        "cv5_recall_std": float(np.std(cv_scores["test_recall"], ddof=1)),
        "cv5_f1_mean": float(np.mean(cv_scores["test_f1"])),
        "cv5_f1_std": float(np.std(cv_scores["test_f1"], ddof=1)),
        "cv5_auc_mean": float(np.mean(cv_scores["test_roc_auc"])),
        "cv5_auc_std": float(np.std(cv_scores["test_roc_auc"], ddof=1)),
        "target_positive_rate": float(y.mean()),
        "target_positive_count": int(y.sum()),
        "target_negative_count": int((1 - y).sum()),
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
    target_table, target_meta = build_target_table(
        target_df_raw, merged, year=target_year, target_group_id=target_group_id
    )

    used_group_ids = feature_meta["feature_group_ids_used"]
    feature_cols = [f"group_{gid}" for gid in used_group_ids]
    if not feature_cols:
        raise ValueError(f"{scenario_name}: no usable feature groups.")

    if pair_by_student_id:
        x_df = dedup_by_student_id(feature_table[["student_id"] + feature_cols])
        y_df = dedup_by_student_id(target_table[["student_id", "target_score", "target_binary"]])
        model_df = x_df.merge(y_df, on="student_id", how="inner")
    else:
        model_df = pd.DataFrame(index=feature_table.index)
        model_df["student_id"] = feature_table["student_id"]
        for col in feature_cols:
            model_df[col] = feature_table[col]
        model_df["target_score"] = target_table["target_score"]
        model_df["target_binary"] = target_table["target_binary"]

    model_df = model_df.loc[model_df["target_binary"].notna()].copy()
    metrics = run_logistic_binary_classification(model_df=model_df, feature_cols=feature_cols)

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
        "target_median_cutoff": target_meta["target_median_cutoff"],
        "n_rows_modeling": metrics["n_rows_modeling"],
        "n_train": metrics["n_train"],
        "n_test": metrics["n_test"],
        "n_features_requested": len(feature_group_ids),
        "n_features_used": metrics["n_features_used"],
        "target_positive_rate": metrics["target_positive_rate"],
        "c_selected": metrics["c_selected"],
        "train_accuracy": metrics["train_accuracy"],
        "train_precision": metrics["train_precision"],
        "train_recall": metrics["train_recall"],
        "train_f1": metrics["train_f1"],
        "train_auc": metrics["train_auc"],
        "test_accuracy": metrics["test_accuracy"],
        "test_precision": metrics["test_precision"],
        "test_recall": metrics["test_recall"],
        "test_f1": metrics["test_f1"],
        "test_auc": metrics["test_auc"],
        "cv5_accuracy_mean": metrics["cv5_accuracy_mean"],
        "cv5_accuracy_std": metrics["cv5_accuracy_std"],
        "cv5_precision_mean": metrics["cv5_precision_mean"],
        "cv5_precision_std": metrics["cv5_precision_std"],
        "cv5_recall_mean": metrics["cv5_recall_mean"],
        "cv5_recall_std": metrics["cv5_recall_std"],
        "cv5_f1_mean": metrics["cv5_f1_mean"],
        "cv5_f1_std": metrics["cv5_f1_std"],
        "cv5_auc_mean": metrics["cv5_auc_mean"],
        "cv5_auc_std": metrics["cv5_auc_std"],
        "skipped_feature_groups_no_mapping_items": ";".join(
            feature_meta["skipped_feature_groups_no_mapping_items"]
        ),
        "skipped_feature_groups_no_columns": ";".join(feature_meta["skipped_feature_groups_no_columns"]),
        "dropped_all_missing_feature_cols": ";".join(metrics["dropped_all_missing_feature_cols"]),
    }

    return summary_row, scenario_detail


def evaluate_version(
    *,
    version_name: str,
    merged: pd.DataFrame,
    w2_raw: pd.DataFrame,
    w3_raw: pd.DataFrame,
    w2_feature_groups: list[str],
    w3_feature_groups: list[str],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    scenarios = [
        {
            "scenario_name": "w2_self",
            "feature_df_raw": w2_raw,
            "target_df_raw": w2_raw,
            "feature_year": "W2",
            "target_year": "W2",
            "target_group_id": W2_TARGET_GROUP_ID,
            "pair_by_student_id": False,
        },
        {
            "scenario_name": "w3_self",
            "feature_df_raw": w3_raw,
            "target_df_raw": w3_raw,
            "feature_year": "W3",
            "target_year": "W3",
            "target_group_id": W3_TARGET_GROUP_ID,
            "pair_by_student_id": False,
        },
        {
            "scenario_name": "w2_predict_w3",
            "feature_df_raw": w2_raw,
            "target_df_raw": w3_raw,
            "feature_year": "W2",
            "target_year": "W3",
            "target_group_id": W3_TARGET_GROUP_ID,
            "pair_by_student_id": True,
        },
    ]

    summary_rows: list[dict[str, Any]] = []
    version_details: dict[str, Any] = {"version_name": version_name, "scenarios": {}}

    for config in scenarios:
        if config["feature_year"] == "W2":
            feature_group_ids = w2_feature_groups
        elif config["feature_year"] == "W3":
            feature_group_ids = w3_feature_groups
        else:
            raise ValueError(f"Unsupported feature_year={config['feature_year']}")

        summary_row, detail = run_scenario(
            scenario_name=config["scenario_name"],
            feature_df_raw=config["feature_df_raw"],
            target_df_raw=config["target_df_raw"],
            merged=merged,
            feature_year=config["feature_year"],
            target_year=config["target_year"],
            feature_group_ids=feature_group_ids,
            target_group_id=config["target_group_id"],
            pair_by_student_id=config["pair_by_student_id"],
        )
        summary_rows.append(summary_row)
        version_details["scenarios"][config["scenario_name"]] = detail

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df[
        [
            "scenario",
            "feature_year",
            "target_year",
            "target_group_id",
            "target_median_cutoff",
            "n_rows_modeling",
            "n_train",
            "n_test",
            "n_features_requested",
            "n_features_used",
            "target_positive_rate",
            "c_selected",
            "train_accuracy",
            "train_precision",
            "train_recall",
            "train_f1",
            "train_auc",
            "test_accuracy",
            "test_precision",
            "test_recall",
            "test_f1",
            "test_auc",
            "cv5_accuracy_mean",
            "cv5_accuracy_std",
            "cv5_precision_mean",
            "cv5_precision_std",
            "cv5_recall_mean",
            "cv5_recall_std",
            "cv5_f1_mean",
            "cv5_f1_std",
            "cv5_auc_mean",
            "cv5_auc_std",
            "skipped_feature_groups_no_mapping_items",
            "skipped_feature_groups_no_columns",
            "dropped_all_missing_feature_cols",
        ]
    ]
    return summary_df, version_details


def format_md_cell(value: Any, float_digits: int = 6) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.{float_digits}f}"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return str(value)


def dataframe_to_markdown(df: pd.DataFrame, columns: list[str]) -> str:
    lines: list[str] = []
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    lines.append(header)
    lines.append(separator)
    for _, row in df.iterrows():
        values = [format_md_cell(row[col]) for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_delta_table(no_drop_df: pd.DataFrame, drop_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "scenario",
        "test_accuracy",
        "test_precision",
        "test_recall",
        "test_f1",
        "test_auc",
        "cv5_accuracy_mean",
        "cv5_precision_mean",
        "cv5_recall_mean",
        "cv5_f1_mean",
        "cv5_auc_mean",
    ]
    merged = no_drop_df[cols].merge(drop_df[cols], on="scenario", suffixes=("_no_drop", "_drop"))
    out = pd.DataFrame({"scenario": merged["scenario"]})
    for metric in cols[1:]:
        out[f"delta_{metric}_drop_minus_no_drop"] = merged[f"{metric}_drop"] - merged[f"{metric}_no_drop"]
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    merged_path = pick_first_existing_path(MERGED_PATH_CANDIDATES)
    w2_raw = normalize_student_id(pd.read_csv(W2_DATA_PATH, low_memory=False))
    w3_raw = normalize_student_id(pd.read_csv(W3_DATA_PATH, low_memory=False))

    merged = pd.read_csv(merged_path, dtype=str)
    for c in ["Year", "Group_ID", "Question_ID"]:
        if c in merged.columns:
            merged[c] = merged[c].astype(str).str.strip()

    no_drop_df, no_drop_details = evaluate_version(
        version_name="no_drop",
        merged=merged,
        w2_raw=w2_raw,
        w3_raw=w3_raw,
        w2_feature_groups=W2_FEATURE_GROUP_IDS,
        w3_feature_groups=W3_FEATURE_GROUP_IDS,
    )
    drop_df, drop_details = evaluate_version(
        version_name="drop_groups",
        merged=merged,
        w2_raw=w2_raw,
        w3_raw=w3_raw,
        w2_feature_groups=W2_FEATURE_GROUP_IDS_DROP,
        w3_feature_groups=W3_FEATURE_GROUP_IDS_DROP,
    )
    delta_df = build_delta_table(no_drop_df, drop_df)

    no_drop_df.to_csv(NO_DROP_SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")
    drop_df.to_csv(DROP_SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")
    combined_df = pd.concat(
        [no_drop_df.assign(version="no_drop"), drop_df.assign(version="drop_groups")], ignore_index=True
    )
    combined_df.to_csv(COMBINED_SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")

    details = {
        "settings": {
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
            "logit_cs_count": int(len(LOGIT_CS)),
            "w2_data_path": str(W2_DATA_PATH),
            "w3_data_path": str(W3_DATA_PATH),
            "merged_path": str(merged_path),
            "drop_groups": {
                "w2_feature_group_ids_dropped": sorted(W2_DROP_GROUP_IDS),
                "w3_feature_group_ids_dropped": sorted(W3_DROP_GROUP_IDS),
            },
            "note": (
                "Target score is median-split into binary 0/1, modeled with logistic regression. "
                "This rerun includes precision/recall for train, test, and 5-fold CV."
            ),
        },
        "versions": {"no_drop": no_drop_details, "drop_groups": drop_details},
    }
    with open(DETAIL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    table_cols = [
        "scenario",
        "train_accuracy",
        "train_precision",
        "train_recall",
        "test_accuracy",
        "test_precision",
        "test_recall",
        "test_f1",
        "test_auc",
        "cv5_accuracy_mean",
        "cv5_precision_mean",
        "cv5_recall_mean",
        "cv5_f1_mean",
        "cv5_auc_mean",
        "n_rows_modeling",
        "n_features_used",
    ]
    delta_cols = [
        "scenario",
        "delta_test_accuracy_drop_minus_no_drop",
        "delta_test_precision_drop_minus_no_drop",
        "delta_test_recall_drop_minus_no_drop",
        "delta_test_f1_drop_minus_no_drop",
        "delta_test_auc_drop_minus_no_drop",
        "delta_cv5_accuracy_mean_drop_minus_no_drop",
        "delta_cv5_precision_mean_drop_minus_no_drop",
        "delta_cv5_recall_mean_drop_minus_no_drop",
        "delta_cv5_f1_mean_drop_minus_no_drop",
        "delta_cv5_auc_mean_drop_minus_no_drop",
    ]

    with open(SUMMARY_MD_PATH, "w", encoding="utf-8") as f:
        f.write("# Baseline Logistic Median Split: Combined Summary (With Precision/Recall)\n\n")
        f.write(f"- W2 data: `{W2_DATA_PATH}`\n")
        f.write(f"- W3 data: `{W3_DATA_PATH}`\n")
        f.write(f"- Mapping: `{merged_path}`\n")
        f.write("- Rule: target score is median-split into binary 0/1, modeled with logistic regression.\n")
        f.write("- Versions included: no-drop and drop-groups.\n")
        f.write("- Added metrics: precision and recall (train/test/CV).\n\n")

        f.write("## No-drop Version\n\n")
        f.write(dataframe_to_markdown(no_drop_df, table_cols))
        f.write("\n\n")

        f.write("## Drop-groups Version\n\n")
        f.write(f"- Dropped W2 feature groups: `{', '.join(sorted(W2_DROP_GROUP_IDS))}`\n")
        f.write(f"- Dropped W3 feature groups: `{', '.join(sorted(W3_DROP_GROUP_IDS))}`\n\n")
        f.write(dataframe_to_markdown(drop_df, table_cols))
        f.write("\n\n")

        f.write("## Delta (Drop - No-drop)\n\n")
        f.write("- Positive value means drop-groups performs better; negative means worse.\n\n")
        f.write(dataframe_to_markdown(delta_df, delta_cols))
        f.write("\n")

    print("Combined baseline rerun completed.")
    print(f"Wrote: {SUMMARY_MD_PATH}")
    print(f"Wrote: {NO_DROP_SUMMARY_CSV_PATH}")
    print(f"Wrote: {DROP_SUMMARY_CSV_PATH}")
    print(f"Wrote: {COMBINED_SUMMARY_CSV_PATH}")
    print(f"Wrote: {DETAIL_JSON_PATH}")


if __name__ == "__main__":
    main()
