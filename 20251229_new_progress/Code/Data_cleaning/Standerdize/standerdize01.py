import argparse
import os
import re
from typing import Dict, List, Tuple

import pandas as pd

# -----------------------------
# Default paths (override via CLI)
# -----------------------------
DEFAULT_W2_PATH = (
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data"
    r"\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
)
DEFAULT_W3_PATH = (
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data"
    r"\TIGPS_W3_studentdata_ver5_cleaned_cols_removed_missing_common_only(cleaned_q_21).csv"
)

META_COLS_W2 = {
    "student_oid",
    "student_id",
    "qb_code",
    "q_name",
    "school_id",
    "school_name",
    "class",
    "status",
    "name",
    "cell",
    "cell_who",
    "email",
}

META_COLS_W3 = {
    "student_id",
}

MISSING_TOKENS = {
    "",
    " ",
    "NA",
    "N/A",
    "nan",
    "NaN",
    "NULL",
    "null",
    "None",
}

QUESTION_PATTERNS = {
    "W2": re.compile(r"^v\d+[a-zA-Z]?", re.IGNORECASE),
    "W3": re.compile(r"^\d"),
}

OTHER_COL_PATTERNS = [
    "其他",
    "Other",
    "____",
    "____小時",
    "____分鐘",
    "點",
    "分",
    "小時",
    "分鐘",
]


def normalize_missing(series: pd.Series) -> pd.Series:
    s = series.copy()
    if s.dtype == object:
        s = s.apply(lambda x: x.strip() if isinstance(x, str) else x)
    s = s.replace(list(MISSING_TOKENS), pd.NA)
    return s


def is_other_like(col_name: str) -> bool:
    name = str(col_name)
    return any(pat in name for pat in OTHER_COL_PATTERNS)


def detect_role(col_name: str, dataset: str) -> str:
    if dataset == "W2" and col_name in META_COLS_W2:
        return "meta"
    if dataset == "W3" and col_name in META_COLS_W3:
        return "meta"
    if QUESTION_PATTERNS[dataset].match(str(col_name)):
        return "question"
    return "aux"


def infer_type(series: pd.Series, col_name: str, role: str) -> str:
    col_name_str = str(col_name)
    if col_name_str.lower().startswith("unnamed"):
        return "drop_col"

    s = normalize_missing(series)
    nonnull = s.dropna()
    n = len(nonnull)
    if n == 0:
        return "empty"

    if role == "meta":
        if nonnull.apply(lambda x: isinstance(x, str)).mean() > 0.5:
            return "meta_text"
        return "meta_numeric"

    # Check if numeric-like
    numeric = pd.to_numeric(nonnull, errors="coerce")
    numeric_ratio = numeric.notna().mean()

    if numeric_ratio >= 0.9:
        values = numeric.dropna()
        uniq = sorted(values.unique())
        uniq_set = set(uniq)

        if is_other_like(col_name_str):
            return "time_part_numeric"

        if uniq_set.issubset({0, 1}):
            return "binary_01"
        if uniq_set.issubset({1, 2}):
            return "binary_12"
        if uniq_set.issubset({1, 2, 3, 4}):
            return "likert_4"
        if uniq_set.issubset({1, 2, 3, 4, 5}):
            return "likert_5"
        if uniq_set.issubset({1, 2, 3, 4, 5, 6, 7}):
            return "likert_7"
        if len(uniq_set) <= 10:
            return "ordinal_numeric"
        return "numeric"

    # Text-like
    n_unique = nonnull.astype(str).nunique()
    unique_ratio = n_unique / n if n else 0
    if is_other_like(col_name_str):
        return "text_other"
    if n_unique > 50 or unique_ratio > 0.5:
        return "text"
    return "categorical"


def build_profile(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for col in df.columns:
        role = detect_role(col, dataset)
        inferred = infer_type(df[col], col, role)

        s = normalize_missing(df[col])
        nonnull = s.dropna()
        n_total = len(df)
        n_nonnull = len(nonnull)
        n_unique = nonnull.nunique() if n_nonnull else 0

        numeric = pd.to_numeric(nonnull, errors="coerce")
        numeric_ratio = numeric.notna().mean() if n_nonnull else 0.0
        min_val = numeric.min() if numeric_ratio >= 0.9 and not numeric.empty else ""
        max_val = numeric.max() if numeric_ratio >= 0.9 and not numeric.empty else ""

        example_values = (
            "|".join([str(v) for v in nonnull.unique()[:5]]) if n_nonnull else ""
        )

        rows.append(
            {
                "dataset": dataset,
                "column": col,
                "role": role,
                "inferred_type": inferred,
                "n_nonnull": n_nonnull,
                "nonnull_pct": round(n_nonnull / n_total, 4) if n_total else 0.0,
                "n_unique": n_unique,
                "numeric_ratio": round(float(numeric_ratio), 4),
                "min": min_val,
                "max": max_val,
                "example_values": example_values,
            }
        )
    return pd.DataFrame(rows)


def build_type_map(profile_df: pd.DataFrame) -> pd.DataFrame:
    actions = []
    for _, row in profile_df.iterrows():
        col = str(row["column"])
        role = row["role"]
        inferred = row["inferred_type"]

        if col.lower().startswith("unnamed") or inferred == "drop_col":
            action = "drop"
        elif role == "meta":
            action = "keep_meta"
        else:
            action = "keep"

        actions.append(action)

    type_map = profile_df[["dataset", "column", "role", "inferred_type"]].copy()
    type_map["action"] = actions
    type_map["notes"] = ""
    return type_map


def standardize_df(df: pd.DataFrame, type_map: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy()
    for _, row in type_map.iterrows():
        col = row["column"]
        action = row["action"]
        inferred = row["inferred_type"]

        if action == "drop":
            if col in df_out.columns:
                df_out = df_out.drop(columns=[col])
            continue

        if col not in df_out.columns:
            continue

        s = normalize_missing(df_out[col])

        if inferred in {
            "binary_01",
            "binary_12",
            "likert_4",
            "likert_5",
            "likert_7",
            "ordinal_numeric",
            "numeric",
            "time_part_numeric",
            "meta_numeric",
        }:
            df_out[col] = pd.to_numeric(s, errors="coerce")
        else:
            df_out[col] = s

    return df_out


def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile and standardize W2/W3 student datasets."
    )
    parser.add_argument("--w2", default=DEFAULT_W2_PATH, help="Path to W2 CSV")
    parser.add_argument("--w3", default=DEFAULT_W3_PATH, help="Path to W3 CSV")
    parser.add_argument(
        "--out-dir",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Output directory",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply standardization using type_map files",
    )
    parser.add_argument(
        "--map-w2",
        default="type_map_W2.csv",
        help="Type map for W2 (relative to out-dir if not absolute)",
    )
    parser.add_argument(
        "--map-w3",
        default="type_map_W3.csv",
        help="Type map for W3 (relative to out-dir if not absolute)",
    )
    args = parser.parse_args()

    ensure_dir(args.out_dir)

    w2 = pd.read_csv(args.w2, low_memory=False)
    w3 = pd.read_csv(args.w3, low_memory=False)

    if not args.apply:
        profile_w2 = build_profile(w2, "W2")
        profile_w3 = build_profile(w3, "W3")

        profile_w2.to_csv(os.path.join(args.out_dir, "profile_W2.csv"), index=False)
        profile_w3.to_csv(os.path.join(args.out_dir, "profile_W3.csv"), index=False)

        type_map_w2 = build_type_map(profile_w2)
        type_map_w3 = build_type_map(profile_w3)

        type_map_w2.to_csv(os.path.join(args.out_dir, "type_map_W2.csv"), index=False)
        type_map_w3.to_csv(os.path.join(args.out_dir, "type_map_W3.csv"), index=False)

        print("Profiles and type maps created in:", args.out_dir)
        print("Review type_map_W2.csv and type_map_W3.csv before applying.")
        return

    map_w2_path = (
        args.map_w2
        if os.path.isabs(args.map_w2)
        else os.path.join(args.out_dir, args.map_w2)
    )
    map_w3_path = (
        args.map_w3
        if os.path.isabs(args.map_w3)
        else os.path.join(args.out_dir, args.map_w3)
    )

    type_map_w2 = pd.read_csv(map_w2_path)
    type_map_w3 = pd.read_csv(map_w3_path)

    w2_std = standardize_df(w2, type_map_w2)
    w3_std = standardize_df(w3, type_map_w3)

    w2_std.to_csv(os.path.join(args.out_dir, "W2_standardized.csv"), index=False)
    w3_std.to_csv(os.path.join(args.out_dir, "W3_standardized.csv"), index=False)

    print("Standardized files written to:", args.out_dir)


if __name__ == "__main__":
    main()
