from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress")
W2_DATA_PATH = (
    BASE_DIR / r"Data\2024data\TIGPS_W2_studentdata_ver6.csv"
)
W3_DATA_PATH = (
    BASE_DIR
    / r"Data\2025data\TIGPS_W3_studentdata_ver6.csv"
)
MERGED_PATH = BASE_DIR / r"Code\EDA\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv"
OUT_DIR = (
    BASE_DIR
    / r"Code\Analysis\W2_Predict_W3\ML_baseline\Mental分組測試\Regression\題組\細拆分"
)

W3_TARGET_GROUP_ID = "54"

# User-specified W2 groups (cross-year prediction to W3 group 54), but several are split into subscales.
W2_GROUPS_REQUESTED = [
    "v55", "v57", "v52", "v50", "v51", "v27", "v42", "v6", "v5", "v49",
    "v38", "v40", "v28", "v25", "v34", "v19", "v1", "v3", "v23", "v36",
    "v521", "v26", "v54", "v22",
]

DROP_SOURCE_GROUP_IDS = ["v57", "v52", "v51", "v50"]

RANDOM_STATE = 42
TEST_SIZE = 0.2
ALPHAS = np.logspace(-4, 4, 81)


def make_cols(prefix: str, start: int, end: int) -> list[str]:
    return [f"{prefix}_{i}" for i in range(start, end + 1)]


# Groups to split and their subscales (replace original group score with these features).
SUBSCALE_SPECS: dict[str, dict[str, Any]] = {
    "v25_A": {"source_group_id": "v25", "item_cols": make_cols("v25", 1, 3)},
    "v25_B": {"source_group_id": "v25", "item_cols": make_cols("v25", 4, 6)},
    "v25_C": {"source_group_id": "v25", "item_cols": make_cols("v25", 7, 15)},
    "v26_A": {"source_group_id": "v26", "item_cols": make_cols("v26", 1, 3)},
    "v26_B": {"source_group_id": "v26", "item_cols": make_cols("v26", 4, 6)},
    "v27_A": {"source_group_id": "v27", "item_cols": make_cols("v27", 1, 3)},
    "v27_B": {"source_group_id": "v27", "item_cols": ["v27_4"]},  # single-item subscale
    "v54_A": {"source_group_id": "v54", "item_cols": make_cols("v54", 1, 3)},
    "v54_B": {"source_group_id": "v54", "item_cols": make_cols("v54", 4, 6)},
    "v54_C": {"source_group_id": "v54", "item_cols": make_cols("v54", 7, 9)},
    "v23_A": {"source_group_id": "v23", "item_cols": make_cols("v23", 1, 3)},
    "v23_B": {"source_group_id": "v23", "item_cols": make_cols("v23", 4, 6)},
    "v23_C": {"source_group_id": "v23", "item_cols": make_cols("v23", 7, 9)},
}

SPLIT_SOURCE_GROUP_IDS = {meta["source_group_id"] for meta in SUBSCALE_SPECS.values()}


def resolve_group_items(merged: pd.DataFrame, year: str, group_id: str) -> list[str]:
    sub = merged[
        (merged["Year"].astype(str).str.strip() == year)
        & (merged["Group_ID"].astype(str).str.strip() == group_id)
    ]
    return sub["Question_ID"].dropna().astype(str).str.strip().tolist()


def candidate_item_names(item: str) -> list[str]:
    cands = [item]
    if "-" in item:
        cands.append(item.replace("-", "_"))
    if "_" in item:
        cands.append(item.replace("_", "-"))
    return list(dict.fromkeys(cands))


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


def compute_feature_score(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, list[str], list[str]]:
    found, missing = resolve_existing_items(df, items)
    if not found:
        return pd.Series(np.nan, index=df.index, dtype=float), found, missing
    data = df[found].apply(pd.to_numeric, errors="coerce")
    score = data.mean(axis=1, skipna=True)
    score[data.notna().sum(axis=1) == 0] = np.nan
    return score, found, missing


def metric_dict(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def fit_and_eval(
    X: pd.DataFrame,
    y: pd.Series,
    train_idx: pd.Index,
    test_idx: pd.Index,
    feature_defs_used: pd.DataFrame,
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    X_train, X_test = X.loc[train_idx], X.loc[test_idx]
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]

    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("ridge", RidgeCV(alphas=ALPHAS, cv=cv)),
        ]
    )
    model.fit(X_train, y_train)

    yhat_train = model.predict(X_train)
    yhat_test = model.predict(X_test)
    train_metrics = metric_dict(y_train, yhat_train)
    test_metrics = metric_dict(y_test, yhat_test)
    alpha_selected = float(model.named_steps["ridge"].alpha_)

    fixed_model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("ridge", RidgeCV(alphas=[alpha_selected], cv=None)),
        ]
    )
    cv_scores = cross_validate(
        fixed_model,
        X,
        y,
        cv=cv,
        scoring=("r2", "neg_root_mean_squared_error", "neg_mean_absolute_error"),
        n_jobs=None,
    )
    cv_summary = {
        "r2_mean": float(np.mean(cv_scores["test_r2"])),
        "r2_std": float(np.std(cv_scores["test_r2"], ddof=1)),
        "rmse_mean": float(np.mean(-cv_scores["test_neg_root_mean_squared_error"])),
        "rmse_std": float(np.std(-cv_scores["test_neg_root_mean_squared_error"], ddof=1)),
        "mae_mean": float(np.mean(-cv_scores["test_neg_mean_absolute_error"])),
        "mae_std": float(np.std(-cv_scores["test_neg_mean_absolute_error"], ddof=1)),
    }

    coef_df = feature_defs_used.copy()
    coef_df["coef"] = model.named_steps["ridge"].coef_
    coef_df["abs_coef"] = np.abs(coef_df["coef"])
    coef_df = coef_df.sort_values("abs_coef", ascending=False).reset_index(drop=True)

    pred_df = pd.DataFrame(
        {
            "index": X_test.index,
            "y_true": y_test.values,
            "y_pred": yhat_test,
            "residual": y_test.values - yhat_test,
        }
    ).sort_values("index")

    result = {
        "n_features": int(X.shape[1]),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "alpha_selected": alpha_selected,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "cv5_metrics": cv_summary,
    }
    return result, coef_df, pred_df


def build_feature_spec_table(
    w2_df: pd.DataFrame,
    merged: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str], dict[str, list[str]]]:
    rows: list[dict[str, Any]] = []
    skipped_no_items: list[str] = []
    partial_missing_items: dict[str, list[str]] = {}

    for gid in W2_GROUPS_REQUESTED:
        if gid in SPLIT_SOURCE_GROUP_IDS:
            continue
        requested_items = resolve_group_items(merged, "W2", gid)
        if not requested_items:
            raise ValueError(f"No W2 items found for requested group {gid}")
        score, items_used, missing_items = compute_feature_score(w2_df, requested_items)
        if not items_used:
            skipped_no_items.append(gid)
            continue
        w2_df[f"__tmp_feature_{gid}"] = score
        if missing_items:
            partial_missing_items[gid] = missing_items
        rows.append(
            {
                "feature_name": gid,
                "source_group_id": gid,
                "feature_type": "whole_group",
                "items_requested": "; ".join(requested_items),
                "items_used": "; ".join(items_used),
                "item_count_requested": len(requested_items),
                "item_count_used": len(items_used),
                "missing_items_from_mapping": "; ".join(missing_items),
                "tmp_col": f"__tmp_feature_{gid}",
            }
        )

    for feature_name, meta in SUBSCALE_SPECS.items():
        requested_items = list(meta["item_cols"])
        score, items_used, missing_items = compute_feature_score(w2_df, requested_items)
        if not items_used:
            skipped_no_items.append(feature_name)
            continue
        w2_df[f"__tmp_feature_{feature_name}"] = score
        if missing_items:
            partial_missing_items[feature_name] = missing_items
        rows.append(
            {
                "feature_name": feature_name,
                "source_group_id": meta["source_group_id"],
                "feature_type": "subscale",
                "items_requested": "; ".join(requested_items),
                "items_used": "; ".join(items_used),
                "item_count_requested": len(requested_items),
                "item_count_used": len(items_used),
                "missing_items_from_mapping": "; ".join(missing_items),
                "tmp_col": f"__tmp_feature_{feature_name}",
            }
        )

    feature_defs = pd.DataFrame(rows)
    # preserve user-requested order with split expansion in-place
    ordered_names: list[str] = []
    split_order = [
        ("v25", ["v25_A", "v25_B", "v25_C"]),
        ("v26", ["v26_A", "v26_B"]),
        ("v27", ["v27_A", "v27_B"]),
        ("v54", ["v54_A", "v54_B", "v54_C"]),
        ("v23", ["v23_A", "v23_B", "v23_C"]),
    ]
    split_map = {k: v for k, v in split_order}
    existing_names = set(feature_defs["feature_name"].tolist())
    for gid in W2_GROUPS_REQUESTED:
        if gid in split_map:
            for sub in split_map[gid]:
                if sub in existing_names:
                    ordered_names.append(sub)
        else:
            if gid in existing_names:
                ordered_names.append(gid)

    return feature_defs, ordered_names, partial_missing_items


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    w2 = pd.read_csv(W2_DATA_PATH, low_memory=False)
    w3 = pd.read_csv(W3_DATA_PATH, low_memory=False)
    merged = pd.read_csv(MERGED_PATH, dtype=str)
    merged["Year"] = merged["Year"].astype(str).str.strip()
    merged["Group_ID"] = merged["Group_ID"].astype(str).str.strip()
    merged["Question_ID"] = merged["Question_ID"].astype(str).str.strip()

    # W3 target (group 54)
    w3_target_items_requested = resolve_group_items(merged, "W3", W3_TARGET_GROUP_ID)
    if not w3_target_items_requested:
        raise ValueError(f"No W3 items found for target group {W3_TARGET_GROUP_ID}")
    y_w3, w3_target_items_used, w3_target_missing_items = compute_feature_score(
        w3, w3_target_items_requested
    )
    if y_w3.notna().sum() == 0:
        raise ValueError(f"W3 target {W3_TARGET_GROUP_ID} is all-missing.")

    # W2 feature scores (whole groups + subscales)
    feature_defs, full_feature_order, partial_missing_items = build_feature_spec_table(w2, merged)
    if not full_feature_order:
        raise ValueError("No usable W2 features after building split feature table.")

    feature_defs = feature_defs.set_index("feature_name").loc[full_feature_order].reset_index()
    feature_defs["is_drop_candidate_by_source"] = feature_defs["source_group_id"].isin(DROP_SOURCE_GROUP_IDS)

    # Build merge dataset
    if "student_id" not in w2.columns or "student_id" not in w3.columns:
        raise ValueError("Both W2 and W3 datasets must contain student_id.")

    X_df = pd.DataFrame(index=w2.index)
    X_df["merge_id"] = w2["student_id"].astype(str).str.strip()
    for _, row in feature_defs.iterrows():
        X_df[f"feature_{row['feature_name']}"] = w2[row["tmp_col"]]

    y_df = pd.DataFrame(
        {
            "merge_id": w3["student_id"].astype(str).str.strip(),
            "target_w3_54": y_w3,
        }
    )

    dup_w2 = int(X_df["merge_id"].duplicated().sum())
    dup_w3 = int(y_df["merge_id"].duplicated().sum())
    inner_rows = pd.merge(X_df[["merge_id"]], y_df[["merge_id"]], on="merge_id", how="inner")

    data = pd.merge(X_df, y_df, on="merge_id", how="inner")
    data = data.dropna(subset=["target_w3_54"]).copy()
    y = data["target_w3_54"].astype(float)

    # User explicitly requested checking standardisation here (since ver6 unstandardised distributions are loaded)
    # The X features are already standardised through Pipeline(steps=[('scaler', StandardScaler())])
    # However we will standardise y dynamically so target metrics are aligned structurally relative to standardized variance
    y = (y - y.mean()) / y.std()

    # Fixed split for fair full-vs-drop comparison
    train_idx, test_idx = train_test_split(data.index, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    train_idx = pd.Index(train_idx)
    test_idx = pd.Index(test_idx)

    full_feature_names = feature_defs["feature_name"].tolist()
    drop_feature_names = feature_defs.loc[
        ~feature_defs["source_group_id"].isin(DROP_SOURCE_GROUP_IDS), "feature_name"
    ].tolist()
    drop_effective_sources = sorted(
        set(feature_defs.loc[feature_defs["is_drop_candidate_by_source"], "source_group_id"].tolist())
    )

    X_full = data[[f"feature_{n}" for n in full_feature_names]].copy()
    X_drop = data[[f"feature_{n}" for n in drop_feature_names]].copy()

    feature_defs_full = feature_defs.copy()
    feature_defs_full["feature_col"] = feature_defs_full["feature_name"].map(lambda x: f"feature_{x}")
    feature_defs_drop = (
        feature_defs_full.set_index("feature_name").loc[drop_feature_names].reset_index()
    )

    full_res, full_coef, full_pred = fit_and_eval(X_full, y, train_idx, test_idx, feature_defs_full)
    drop_res, drop_coef, drop_pred = fit_and_eval(X_drop, y, train_idx, test_idx, feature_defs_drop)

    metrics_to_compare = [
        ("train_r2", full_res["train_metrics"]["r2"], drop_res["train_metrics"]["r2"]),
        ("train_rmse", full_res["train_metrics"]["rmse"], drop_res["train_metrics"]["rmse"]),
        ("train_mae", full_res["train_metrics"]["mae"], drop_res["train_metrics"]["mae"]),
        ("test_r2", full_res["test_metrics"]["r2"], drop_res["test_metrics"]["r2"]),
        ("test_rmse", full_res["test_metrics"]["rmse"], drop_res["test_metrics"]["rmse"]),
        ("test_mae", full_res["test_metrics"]["mae"], drop_res["test_metrics"]["mae"]),
        ("cv5_r2_mean", full_res["cv5_metrics"]["r2_mean"], drop_res["cv5_metrics"]["r2_mean"]),
        ("cv5_rmse_mean", full_res["cv5_metrics"]["rmse_mean"], drop_res["cv5_metrics"]["rmse_mean"]),
        ("cv5_mae_mean", full_res["cv5_metrics"]["mae_mean"], drop_res["cv5_metrics"]["mae_mean"]),
        ("alpha_selected", full_res["alpha_selected"], drop_res["alpha_selected"]),
        ("n_features", float(full_res["n_features"]), float(drop_res["n_features"])),
    ]
    compare_df = pd.DataFrame(
        [
            {
                "metric": name,
                "full_model": full_val,
                "drop_model": drop_val,
                "delta_drop_minus_full": drop_val - full_val,
            }
            for name, full_val, drop_val in metrics_to_compare
        ]
    )

    feature_defs_out = feature_defs[
        [
            "feature_name",
            "source_group_id",
            "feature_type",
            "item_count_requested",
            "item_count_used",
            "items_requested",
            "items_used",
            "missing_items_from_mapping",
            "is_drop_candidate_by_source",
        ]
    ].copy()

    bundle = {
        "task": "Cross-year Ridge: W2 selected groups (with subscale splits) predict W3 group 54",
        "w2_data_path": str(W2_DATA_PATH),
        "w3_data_path": str(W3_DATA_PATH),
        "mapping_path": str(MERGED_PATH),
        "score_definition": "Feature/target scores are row-wise means across their item sets (skipna=True; all-missing rows => NaN). Explicit target (y) standardisation applied for recoded ver6 dataset scale.",
        "w3_target_group_id": W3_TARGET_GROUP_ID,
        "w3_target_items_requested": w3_target_items_requested,
        "w3_target_items_used": w3_target_items_used,
        "w3_target_missing_items_from_mapping": w3_target_missing_items,
        "w2_groups_requested_original": W2_GROUPS_REQUESTED,
        "split_source_groups": sorted(SPLIT_SOURCE_GROUP_IDS),
        "drop_source_group_ids_requested": DROP_SOURCE_GROUP_IDS,
        "drop_source_group_ids_effective": drop_effective_sources,
        "full_feature_names": full_feature_names,
        "drop_feature_names": drop_feature_names,
        "partial_missing_items": partial_missing_items,
        "w2_duplicate_merge_ids": dup_w2,
        "w3_duplicate_merge_ids": dup_w3,
        "n_rows_w2": int(len(w2)),
        "n_rows_w3": int(len(w3)),
        "n_rows_after_inner_merge": int(len(inner_rows)),
        "n_rows_after_target_nonmissing_filter": int(len(data)),
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "full_model": full_res,
        "drop_model": drop_res,
    }

    # Simplified file names using "ridge_recoded_ver6"
    prefix = "ridge_recoded_ver6"
    compare_csv = OUT_DIR / f"{prefix}_metrics_comparison.csv"
    summary_txt = OUT_DIR / f"{prefix}_summary.txt"
    summary_json = OUT_DIR / f"{prefix}_comparison.json"
    feature_def_csv = OUT_DIR / f"{prefix}_feature_definitions.csv"
    full_coef_csv = OUT_DIR / f"{prefix}_full_coefficients.csv"
    drop_coef_csv = OUT_DIR / f"{prefix}_drop_coefficients.csv"
    full_pred_csv = OUT_DIR / f"{prefix}_full_predictions.csv"
    drop_pred_csv = OUT_DIR / f"{prefix}_drop_predictions.csv"

    compare_df.to_csv(compare_csv, index=False, encoding="utf-8-sig")
    feature_defs_out.to_csv(feature_def_csv, index=False, encoding="utf-8-sig")
    full_coef.to_csv(full_coef_csv, index=False, encoding="utf-8-sig")
    drop_coef.to_csv(drop_coef_csv, index=False, encoding="utf-8-sig")
    full_pred.to_csv(full_pred_csv, index=False, encoding="utf-8-sig")
    drop_pred.to_csv(drop_pred_csv, index=False, encoding="utf-8-sig")
    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    with open(summary_txt, "w", encoding="utf-8") as f:
        f.write("Ridge Comparison: W2 select -> W3 group 54 (Recoded Ver6)\n")
        f.write("=" * 74 + "\n")
        f.write(f"W2 data: {W2_DATA_PATH}\n")
        f.write(f"W3 data: {W3_DATA_PATH}\n")
        f.write(f"Target standardisation applied (y-mean)/y-std!\n")
        f.write(f"Target group (W3): {W3_TARGET_GROUP_ID}\n")
        f.write(f"Target items used ({len(w3_target_items_used)}): {', '.join(w3_target_items_used)}\n")
        if w3_target_missing_items:
            f.write(f"Target missing mapped items: {', '.join(w3_target_missing_items)}\n")
        f.write("\nFeature design:\n")
        f.write(f"- Original requested W2 groups: {', '.join(W2_GROUPS_REQUESTED)}\n")
        f.write(f"- Split source groups: {', '.join(sorted(SPLIT_SOURCE_GROUP_IDS))}\n")
        f.write(f"- Full features after splitting ({len(full_feature_names)}): {', '.join(full_feature_names)}\n")
        f.write(f"- Dropped source groups (requested): {', '.join(DROP_SOURCE_GROUP_IDS)}\n")
        f.write(f"- Dropped source groups (effective): {', '.join(drop_effective_sources)}\n")
        f.write(f"- Drop-model features ({len(drop_feature_names)}): {', '.join(drop_feature_names)}\n")
        f.write("\nSubscale definitions:\n")
        for _, r in feature_defs_out[feature_defs_out["feature_type"] == "subscale"].iterrows():
            f.write(
                f"- {r['feature_name']} (from {r['source_group_id']}): "
                f"{r['items_used'] or r['items_requested']}\n"
            )
        f.write(f"\nW2 duplicate merge_ids: {dup_w2}\n")
        f.write(f"W3 duplicate merge_ids: {dup_w3}\n")
        f.write(f"Rows after inner merge: {len(inner_rows)}\n")
        f.write(f"Rows after target non-missing filter: {len(data)}\n")
        f.write(f"Train/Test: {len(train_idx)}/{len(test_idx)} (fixed split)\n")
        f.write("\nMetrics comparison (drop - full):\n")
        for _, r in compare_df.iterrows():
            f.write(
                f"- {r['metric']}: full={r['full_model']:.6f}, "
                f"drop={r['drop_model']:.6f}, delta={r['delta_drop_minus_full']:.6f}\n"
            )

    print("Ridge cross-year comparison on Recoded Ver6 completed.")
    print(f"Rows after merge/target filter: {len(data)} | Train/Test: {len(train_idx)}/{len(test_idx)}")
    print(f"Full features: {len(full_feature_names)} | Drop features: {len(drop_feature_names)}")
    print("Full test metrics:", json.dumps(full_res["test_metrics"], ensure_ascii=False))
    print("Drop test metrics:", json.dumps(drop_res["test_metrics"], ensure_ascii=False))
    print(f"Wrote metrics comparison: {compare_csv}")


if __name__ == "__main__":
    main()
