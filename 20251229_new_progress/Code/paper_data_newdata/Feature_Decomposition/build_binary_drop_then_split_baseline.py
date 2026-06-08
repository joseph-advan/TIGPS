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

# Same feature groups used in prior baseline scripts.
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
    "v9",
    "v12",
    "v8_03-v8_06",
    "v23",
    "v36",
    "v52_health",
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

# Drop groups matched to the current logistic baseline drop version.
# W2 v52_health is the scalar self-rated health item v52, not the v52_1-v52_3 self-worth group.
W2_DROP_GROUP_IDS = {"v57", "v50", "v51", "v52_health"}
W3_DROP_GROUP_IDS = {"55", "49", "50", "51"}

# Multiple-response "none of the above" options are not risk behaviors and
# should not be averaged into the delinquent/health-risk behavior score.
NONE_OF_ABOVE_ITEMS_BY_YEAR_GROUP = {
    ("W2", "v42"): {"v42_14"},
    ("W3", "39"): {"39-14"},
}

# These multiple-response risk-behavior groups are more interpretable as counts:
# one unit means one additional endorsed risk behavior.
COUNT_SCORE_GROUPS_BY_YEAR = {
    "W2": {"v42"},
    "W3": {"39"},
}


THIS_FILE = Path(__file__).resolve()
OUT_DIR = THIS_FILE.parent
MODEL_PERFORMANCE_OUT_DIR = OUT_DIR / "outputs" / "model_performance"
BASE_DIR = THIS_FILE.parents[3]

W2_DATA_PATH = BASE_DIR / r"Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv"
W3_DATA_PATH = BASE_DIR / r"Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv"
MERGED_PATH_CANDIDATES = [
    BASE_DIR / r"Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
    BASE_DIR / r"Code\EDA\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
]

SUMMARY_CSV_PATH = MODEL_PERFORMANCE_OUT_DIR / "binary_drop_then_split_summary.csv"
SUMMARY_MD_PATH = MODEL_PERFORMANCE_OUT_DIR / "binary_drop_then_split_summary.md"
DETAIL_JSON_PATH = MODEL_PERFORMANCE_OUT_DIR / "binary_drop_then_split_details.json"
SUBSCALE_CONFIG_PATH = OUT_DIR / "subscale_definitions_w2_w3.json"


def load_subscale_config(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_specs_from_config(config: dict[str, Any], wave: str) -> dict[str, dict[str, list[str]]]:
    specs: dict[str, dict[str, list[str]]] = {}
    for parent_group, group_info in config["waves"].get(wave, {}).items():
        subscales = group_info.get("subscales", {})
        specs[parent_group] = {
            subscale_name: list(subscale_info["items"])
            for subscale_name, subscale_info in subscales.items()
        }
    return specs


def direct_feature_specs_from_config(config: dict[str, Any], wave: str) -> dict[str, list[str]]:
    direct_features = config.get("direct_features", {}).get(wave, {})
    return {
        feature_name: list(feature_info["items"])
        for feature_name, feature_info in direct_features.items()
    }


def feature_metadata_from_config(config: dict[str, Any], wave: str) -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}

    for feature_name, feature_info in config.get("direct_features", {}).get(wave, {}).items():
        metadata[feature_name] = {
            "feature_name": feature_name,
            "source_group_id": feature_name,
            "formal_group_name_zh": feature_info.get("formal_group_name_zh", ""),
            "formal_group_name_en": feature_info.get("formal_group_name_en", ""),
            "subscale_name_zh": feature_info.get("formal_group_name_zh", ""),
            "subscale_name_en": feature_info.get("formal_group_name_en", ""),
            "description_zh": feature_info.get("note", ""),
            "is_direct_feature": True,
        }

    for parent_group, group_info in config["waves"].get(wave, {}).items():
        for subscale_name, subscale_info in group_info.get("subscales", {}).items():
            metadata[subscale_name] = {
                "feature_name": subscale_name,
                "source_group_id": parent_group,
                "formal_group_name_zh": group_info.get("formal_group_name_zh", ""),
                "formal_group_name_en": group_info.get("formal_group_name_en", ""),
                "subscale_name_zh": subscale_info.get("subscale_name_zh", ""),
                "subscale_name_en": subscale_info.get("subscale_name_en", ""),
                "description_zh": subscale_info.get("description_zh", ""),
                "is_direct_feature": False,
            }

    return metadata


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
    elif agg == "count":
        score = data.eq(1).sum(axis=1)
    else:
        raise ValueError(f"Unsupported agg='{agg}'. Use 'mean', 'sum', or 'count'.")
    score[data.notna().sum(axis=1) == 0] = np.nan
    return score, found, missing


def exclude_none_of_above_items(year: str, group_id: str, items: list[str]) -> list[str]:
    excluded = NONE_OF_ABOVE_ITEMS_BY_YEAR_GROUP.get((str(year), str(group_id)), set())
    if not excluded:
        return items
    return [item for item in items if item not in excluded]


def score_aggregation_for_group(year: str, group_id: str) -> str:
    if str(group_id) in COUNT_SCORE_GROUPS_BY_YEAR.get(str(year), set()):
        return "count"
    return "mean"


GENDER_DUMMY_SPECS = {
    "W2": {
        "source_feature": "v1",
        "dummy_feature": "v1_male",
        "source_item": "v1",
    },
    "W3": {
        "source_feature": "1",
        "dummy_feature": "1_male",
        "source_item": "1",
    },
}


def apply_gender_dummy_feature(
    table: pd.DataFrame,
    feature_rows: list[dict[str, Any]],
    year: str,
) -> list[dict[str, Any]]:
    """Encode gender as Male=1 vs Female=0 instead of using raw 1/2 codes."""
    spec = GENDER_DUMMY_SPECS.get(str(year))
    if not spec:
        return []

    source_feature = spec["source_feature"]
    source_col = f"feature_{source_feature}"
    if source_col not in table.columns:
        return []

    dummy_feature = spec["dummy_feature"]
    dummy_col = f"feature_{dummy_feature}"
    raw = pd.to_numeric(table[source_col], errors="coerce")
    dummy = pd.Series(np.nan, index=table.index, dtype=float)
    dummy.loc[raw.eq(1)] = 0.0
    dummy.loc[raw.eq(2)] = 1.0
    table[dummy_col] = dummy
    table.drop(columns=[source_col], inplace=True)

    for row in feature_rows:
        if str(row.get("feature_name")) == source_feature and str(row.get("source_group_id")) == source_feature:
            row.update(
                {
                    "feature_name": dummy_feature,
                    "source_group_id": source_feature,
                    "is_gender_dummy": True,
                    "dummy_reference_value": 1,
                    "dummy_reference_label": "Female",
                    "dummy_target_value": 2,
                    "dummy_target_label": "Male",
                    "score_aggregation": "dummy_2_vs_1",
                    "used_items": row.get("used_items") or [spec["source_item"]],
                }
            )
            break

    return [
        {
            "year": str(year),
            "source_feature": source_feature,
            "dummy_feature": dummy_feature,
            "source_column": source_col,
            "dummy_column": dummy_col,
            "reference": "Female=0",
            "target": "Male=1",
            "n_reference": int(dummy.eq(0).sum()),
            "n_target": int(dummy.eq(1).sum()),
            "n_missing_or_other": int(dummy.isna().sum()),
        }
    ]


def build_feature_table(
    df: pd.DataFrame,
    merged: pd.DataFrame,
    year: str,
    feature_group_ids: list[str],
    drop_group_ids: set[str],
    split_specs: dict[str, dict[str, list[str]]] | None = None,
    direct_feature_specs: dict[str, list[str]] | None = None,
    feature_metadata: dict[str, dict[str, Any]] | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    split_specs = split_specs or {}
    direct_feature_specs = direct_feature_specs or {}
    feature_metadata = feature_metadata or {}

    table = pd.DataFrame(index=df.index)
    table["student_id"] = df["student_id"]

    feature_rows: list[dict[str, Any]] = []
    skipped_no_mapping_items: list[str] = []
    skipped_no_columns: list[str] = []
    partial_missing_columns: dict[str, list[str]] = {}
    dropped_by_group_rule: list[str] = []

    for gid in feature_group_ids:
        if gid in drop_group_ids:
            dropped_by_group_rule.append(gid)
            continue

        if gid in direct_feature_specs:
            score, used, missing = compute_group_score(df, direct_feature_specs[gid], agg="mean")
            if not used:
                skipped_no_columns.append(gid)
                continue
            if missing:
                partial_missing_columns[gid] = missing
            col_name = f"feature_{gid}"
            table[col_name] = score
            row = {
                "feature_name": gid,
                "source_group_id": gid,
                "is_split_feature": False,
                "is_direct_feature": True,
                "used_items": used,
            }
            row.update(feature_metadata.get(gid, {}))
            feature_rows.append(row)
            continue

        if gid in split_specs:
            for sub_name, sub_items in split_specs[gid].items():
                score, used, missing = compute_group_score(df, sub_items, agg="mean")
                if not used:
                    skipped_no_columns.append(sub_name)
                    continue
                if missing:
                    partial_missing_columns[sub_name] = missing
                col_name = f"feature_{sub_name}"
                table[col_name] = score
                row = {
                    "feature_name": sub_name,
                    "source_group_id": gid,
                    "is_split_feature": True,
                    "is_direct_feature": False,
                    "used_items": used,
                }
                row.update(feature_metadata.get(sub_name, {}))
                feature_rows.append(row)
            continue

        items = resolve_group_items(merged, year=year, group_id=gid)
        items = exclude_none_of_above_items(year, gid, items)
        if not items:
            skipped_no_mapping_items.append(gid)
            continue
        score, used, missing = compute_group_score(df, items, agg=score_aggregation_for_group(year, gid))
        if not used:
            skipped_no_columns.append(gid)
            continue
        if missing:
            partial_missing_columns[gid] = missing
        col_name = f"feature_{gid}"
        table[col_name] = score
        feature_rows.append(
            {
                "feature_name": gid,
                "source_group_id": gid,
                "is_split_feature": False,
                "is_direct_feature": False,
                "used_items": used,
                "score_aggregation": score_aggregation_for_group(year, gid),
            }
        )

    gender_dummy_changes = apply_gender_dummy_feature(table, feature_rows, year)
    feature_cols = [f"feature_{r['feature_name']}" for r in feature_rows]

    meta = {
        "feature_year": year,
        "feature_group_ids_requested": feature_group_ids,
        "drop_group_ids": sorted(drop_group_ids),
        "dropped_by_group_rule": sorted(dropped_by_group_rule),
        "split_group_ids": sorted(split_specs.keys()),
        "direct_feature_ids": sorted(direct_feature_specs.keys()),
        "gender_dummy_features": gender_dummy_changes,
        "feature_defs": feature_rows,
        "feature_cols": feature_cols,
        "n_features_used": len(feature_cols),
        "skipped_feature_groups_no_mapping_items": sorted(set(skipped_no_mapping_items)),
        "skipped_feature_groups_no_columns": sorted(set(skipped_no_columns)),
        "partial_feature_groups_missing_columns": partial_missing_columns,
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
    if not found:
        raise ValueError(
            f"Target group {target_group_id} in year {year} has no usable columns in dataset."
        )

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


def metric_binary(y_true: np.ndarray, prob: np.ndarray) -> dict[str, float]:
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


def run_logistic_binary(model_df: pd.DataFrame, feature_cols: list[str]) -> dict[str, Any]:
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
    train_cls = metric_binary(y_train.to_numpy(), prob_train)
    test_cls = metric_binary(y_test.to_numpy(), prob_test)
    chosen_c = float(model.named_steps["logit"].C_[0])

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
    cv_scores = cross_validate(
        fixed,
        X,
        y,
        cv=cv,
        scoring={
            "accuracy": "accuracy",
            "precision": make_scorer(precision_score, zero_division=0),
            "recall": make_scorer(recall_score, zero_division=0),
            "f1": make_scorer(f1_score, zero_division=0),
            "roc_auc": "roc_auc",
        },
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
    drop_group_ids: set[str],
    split_specs: dict[str, dict[str, list[str]]] | None = None,
    direct_feature_specs: dict[str, list[str]] | None = None,
    feature_metadata: dict[str, dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_table, feature_meta = build_feature_table(
        feature_df_raw,
        merged,
        year=feature_year,
        feature_group_ids=feature_group_ids,
        drop_group_ids=drop_group_ids,
        split_specs=split_specs,
        direct_feature_specs=direct_feature_specs,
        feature_metadata=feature_metadata,
    )
    target_table, target_meta = build_target_table(
        target_df_raw, merged, year=target_year, target_group_id=target_group_id
    )

    feature_cols = feature_meta["feature_cols"]
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
    metrics = run_logistic_binary(model_df=model_df, feature_cols=feature_cols)

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
        "n_features_used": metrics["n_features_used"],
        "test_accuracy": metrics["test_accuracy"],
        "test_precision": metrics["test_precision"],
        "test_recall": metrics["test_recall"],
        "test_f1": metrics["test_f1"],
        "test_auc": metrics["test_auc"],
        "cv5_accuracy_mean": metrics["cv5_accuracy_mean"],
        "cv5_precision_mean": metrics["cv5_precision_mean"],
        "cv5_recall_mean": metrics["cv5_recall_mean"],
        "cv5_f1_mean": metrics["cv5_f1_mean"],
        "cv5_auc_mean": metrics["cv5_auc_mean"],
        "drop_group_ids": ";".join(sorted(drop_group_ids)),
        "split_group_ids": ";".join(sorted((split_specs or {}).keys())),
        "direct_feature_ids": ";".join(sorted((direct_feature_specs or {}).keys())),
    }
    return summary_row, scenario_detail


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    merged_path = pick_first_existing_path(MERGED_PATH_CANDIDATES)
    subscale_config = load_subscale_config(SUBSCALE_CONFIG_PATH)
    w2_split_specs = split_specs_from_config(subscale_config, "W2")
    w2_direct_specs = direct_feature_specs_from_config(subscale_config, "W2")
    w2_feature_metadata = feature_metadata_from_config(subscale_config, "W2")

    w2_raw = normalize_student_id(pd.read_csv(W2_DATA_PATH, low_memory=False))
    w3_raw = normalize_student_id(pd.read_csv(W3_DATA_PATH, low_memory=False))

    merged = pd.read_csv(merged_path, dtype=str)
    for c in ["Year", "Group_ID", "Question_ID"]:
        if c in merged.columns:
            merged[c] = merged[c].astype(str).str.strip()

    split_scenarios = [
        {
            "scenario_name": "w2_self",
            "feature_df_raw": w2_raw,
            "target_df_raw": w2_raw,
            "feature_year": "W2",
            "target_year": "W2",
            "feature_group_ids": W2_FEATURE_GROUP_IDS,
            "target_group_id": W2_TARGET_GROUP_ID,
            "pair_by_student_id": False,
            "drop_group_ids": W2_DROP_GROUP_IDS,
            "split_specs": w2_split_specs,
            "direct_feature_specs": w2_direct_specs,
            "feature_metadata": w2_feature_metadata,
        },
        {
            "scenario_name": "w2_predict_w3",
            "feature_df_raw": w2_raw,
            "target_df_raw": w3_raw,
            "feature_year": "W2",
            "target_year": "W3",
            "feature_group_ids": W2_FEATURE_GROUP_IDS,
            "target_group_id": W3_TARGET_GROUP_ID,
            "pair_by_student_id": True,
            "drop_group_ids": W2_DROP_GROUP_IDS,
            "split_specs": w2_split_specs,
            "direct_feature_specs": w2_direct_specs,
            "feature_metadata": w2_feature_metadata,
        },
    ]
    baseline_scenarios = [
        {
            **cfg,
            "split_specs": {},
            "feature_metadata": {},
        }
        for cfg in split_scenarios
    ]

    summary_rows: list[dict[str, Any]] = []
    details: dict[str, Any] = {
        "settings": {
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
            "logit_cs_count": int(len(LOGIT_CS)),
            "w2_data_path": str(W2_DATA_PATH),
            "w3_data_path": str(W3_DATA_PATH),
            "merged_path": str(merged_path),
            "subscale_config_path": str(SUBSCALE_CONFIG_PATH),
            "note": (
                "Binary model with drop-groups first, direct feature correction for W2 health, "
                "then split specified W2 predictor groups into configured subscales. "
                "Current main-paper planning uses W2 predictors only for W2->W2 and W2->W3 tasks."
            ),
            "drop_groups": {
                "W2": sorted(W2_DROP_GROUP_IDS),
            },
            "split_groups": {
                "W2": sorted(w2_split_specs.keys()),
            },
            "direct_features": {
                "W2": sorted(w2_direct_specs.keys()),
            },
            "subscale_config": subscale_config,
        },
        "baseline_drop_no_split": {},
        "drop_then_split": {},
    }

    for cfg in baseline_scenarios:
        summary_row, detail = run_scenario(merged=merged, **cfg)
        summary_row["model_version"] = "baseline_drop_no_split"
        summary_rows.append(summary_row)
        details["baseline_drop_no_split"][cfg["scenario_name"]] = detail

    for cfg in split_scenarios:
        summary_row, detail = run_scenario(merged=merged, **cfg)
        summary_row["model_version"] = "drop_then_split"
        summary_rows.append(summary_row)
        details["drop_then_split"][cfg["scenario_name"]] = detail

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df[
        [
            "model_version",
            "scenario",
            "feature_year",
            "target_year",
            "target_group_id",
            "target_median_cutoff",
            "cv5_accuracy_mean",
            "cv5_precision_mean",
            "cv5_recall_mean",
            "cv5_f1_mean",
            "cv5_auc_mean",
            "n_rows_modeling",
            "n_train",
            "n_test",
            "n_features_used",
            "test_accuracy",
            "test_precision",
            "test_recall",
            "test_f1",
            "test_auc",
            "drop_group_ids",
            "split_group_ids",
            "direct_feature_ids",
        ]
    ]
    MODEL_PERFORMANCE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")

    with open(DETAIL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    baseline_df = summary_df.loc[summary_df["model_version"] == "baseline_drop_no_split"].copy()
    split_df = summary_df.loc[summary_df["model_version"] == "drop_then_split"].copy()
    cv5_cols = [
        "cv5_accuracy_mean",
        "cv5_precision_mean",
        "cv5_recall_mean",
        "cv5_f1_mean",
        "cv5_auc_mean",
    ]
    display_cols = [
        "scenario",
        *cv5_cols,
        "test_accuracy",
        "test_precision",
        "test_recall",
        "test_f1",
        "test_auc",
        "n_features_used",
        "n_rows_modeling",
    ]
    delta_df = split_df[["scenario", *cv5_cols]].merge(
        baseline_df[["scenario", *cv5_cols]],
        on="scenario",
        suffixes=("_split", "_baseline"),
    )
    for col in cv5_cols:
        delta_df[f"delta_{col}_split_minus_baseline"] = (
            delta_df[f"{col}_split"] - delta_df[f"{col}_baseline"]
        )
    delta_display_cols = [
        "scenario",
        *[f"delta_{col}_split_minus_baseline" for col in cv5_cols],
    ]

    def write_md_table(f, df: pd.DataFrame, columns: list[str]) -> None:
        f.write("| " + " | ".join(columns) + " |\n")
        f.write("| " + " | ".join(["---"] + ["---:"] * (len(columns) - 1)) + " |\n")
        for _, row in df.iterrows():
            values = []
            for col in columns:
                value = row[col]
                if isinstance(value, (float, np.floating)):
                    values.append(f"{float(value):.6f}")
                elif isinstance(value, (int, np.integer)):
                    values.append(str(int(value)))
                else:
                    values.append(str(value))
            f.write("| " + " | ".join(values) + " |\n")

    with open(SUMMARY_MD_PATH, "w", encoding="utf-8") as f:
        f.write("# Binary Baseline: Drop Groups Then Split Groups\n\n")
        f.write(f"- W2 data: `{W2_DATA_PATH}`\n")
        f.write(f"- W3 data: `{W3_DATA_PATH}`\n")
        f.write(f"- Mapping: `{merged_path}`\n")
        f.write(f"- W2 dropped groups: `{', '.join(sorted(W2_DROP_GROUP_IDS))}`\n")
        f.write(f"- Subscale config: `{SUBSCALE_CONFIG_PATH}`\n")
        f.write(f"- W2 split groups: `{', '.join(sorted(w2_split_specs.keys()))}`\n")
        f.write(f"- W2 direct features: `{', '.join(sorted(w2_direct_specs.keys()))}`\n")
        f.write("- Current scope: W2 predictors only; scenarios are `w2_self` and `w2_predict_w3`.\n")
        f.write("- Rule: target uses sum-score median split (binary), model is logistic regression.\n\n")
        f.write(
            "- Main metrics are CV5 means: mean test-set metrics across 5 stratified "
            "cross-validation folds.\n\n"
        )
        f.write("## Baseline Drop Version Before Splitting\n\n")
        f.write("This section uses the drop version feature set, without decomposing configured groups into subscales.\n\n")
        write_md_table(f, baseline_df[display_cols], display_cols)
        f.write("\n\n")

        f.write("## Drop Version After Splitting Groups\n\n")
        f.write("This section starts from the same drop version, then splits configured groups into subscales.\n\n")
        write_md_table(f, split_df[display_cols], display_cols)
        f.write("\n\n")

        f.write("## Difference: Split Minus Baseline\n\n")
        f.write("Positive value means the split version performs better than the baseline drop version.\n\n")
        write_md_table(f, delta_df[delta_display_cols], delta_display_cols)
        f.write("\n")

    print("Binary drop-then-split baseline completed.")
    print(f"Wrote: {SUMMARY_CSV_PATH}")
    print(f"Wrote: {SUMMARY_MD_PATH}")
    print(f"Wrote: {DETAIL_JSON_PATH}")
    print("\nAccuracy summary:")
    print(
        summary_df[
            [
                "model_version",
                "scenario",
                "cv5_accuracy_mean",
                "cv5_precision_mean",
                "cv5_recall_mean",
                "cv5_f1_mean",
                "cv5_auc_mean",
                "test_accuracy",
                "test_precision",
                "test_recall",
                "test_f1",
                "test_auc",
                "n_features_used",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
