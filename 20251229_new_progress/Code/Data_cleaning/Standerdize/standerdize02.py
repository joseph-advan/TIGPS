import argparse
import os
import re
from typing import Dict, List

import pandas as pd

# Input paths
DEFAULT_W2_PATH = (
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data"
    r"\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
)
DEFAULT_W3_PATH = (
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data"
    r"\TIGPS_W3_studentdata_ver5_cleaned_cols_removed_missing_common_only(cleaned_q_21).csv"
)

# Output naming
W2_OUT_NAME = "TIGPS_W2_studentdata_ver6_cleaned_mental_common_only(standerdized).csv"
W3_OUT_NAME = "TIGPS_W3_studentdata_ver6_cleaned_cols_removed_missing_common_only(cleaned_q_21)(standerdized).csv"

MISSING_TOKENS = {"", " ", "NA", "N/A", "nan", "NaN", "NULL", "null", "None"}

# Skip columns (manual)
SKIP_W2 = {
    "v59",
    "v60",
    "v13",
    "v61",
    "v62",
    "v63",
    "v1",
    # W2 expanded options
    "v14_1_01",
    "v14_1_02",
    "v14_1_03",
    "v14_1_04",
    "v14_1_05",
    "v14_2_01",
    "v14_2_02",
    "v14_2_03",
    "v14_2_04",
    "v14_2_05",
    "v14_3_01",
    "v14_3_02",
    "v14_3_03",
    "v14_3_04",
    "v14_3_05",
    "v14_4_01",
    "v14_4_02",
    "v14_4_03",
    "v14_4_04",
    "v14_4_05",
}

SKIP_W3 = {
    "58",
    "63",
    "7",
    "64",
    "65",
    "66",
    "1",
    # time/other fields
    "上午_______點",
    "_______分",
    "下午_______點",
    "_______分.1",
    "58-1",
    "_______點_______分",
    "_______分.2",
    "58-2",
    "_______點_______分.1",
    "_______分.3",
    "58-3",
    "_______點_______分.2",
    "_______分.4",
    "58-4",
    "_______點_______分.3",
    "_______分.5",
    "____小時.1",
    "____分鐘.1",
    "____小時.2",
    "____分鐘.2",
    "____小時",
    "____分鐘",
    "其他",
    "其他.1",
    "其他.2",
    "其他.3",
    "其他.4",
    "3",
    "Unnamed: 4",
    # multi-dummy columns
    "8-1_0",
    "8-1_1",
    "8-1_2",
    "8-1_3",
    "8-1_4",
    "8-2_0",
    "8-2_1",
    "8-2_2",
    "8-2_3",
    "8-2_4",
    "8-3_0",
    "8-3_1",
    "8-3_2",
    "8-3_3",
    "8-3_4",
    "8-4_0",
    "8-4_1",
    "8-4_2",
    "8-4_3",
    "8-4_4",
}

# Meta columns (auto-skip)
META_W2 = {
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

META_W3 = {"student_id"}


def normalize_missing(series: pd.Series) -> pd.Series:
    s = series
    if s.dtype == object:
        s = s.apply(lambda x: x.strip() if isinstance(x, str) else x)
    return s.replace(list(MISSING_TOKENS), pd.NA)


def is_question_col(col: str, dataset: str) -> bool:
    if dataset == "W2":
        return bool(re.match(r"^v\d+", str(col), re.IGNORECASE))
    return bool(re.match(r"^\d", str(col)))


def minmax_scale(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    nonnull = s.dropna()
    if nonnull.empty:
        return s
    min_v = nonnull.min()
    max_v = nonnull.max()
    if min_v == max_v:
        return s
    return (s - min_v) / (max_v - min_v)


def standardize_df(
    df: pd.DataFrame,
    dataset: str,
    skip_cols: set,
    meta_cols: set,
) -> Dict[str, pd.DataFrame]:
    df_out = df.copy()
    excluded_rows = []

    for col in df.columns:
        reason = ""
        if col in meta_cols:
            reason = "meta_column"
        elif col in skip_cols:
            reason = "manual_skip"
        elif str(col).lower().startswith("unnamed"):
            reason = "unnamed_column"
        elif not is_question_col(col, dataset):
            reason = "non_question"

        if reason:
            excluded_rows.append({"column": col, "reason": reason})
            continue

        s = normalize_missing(df_out[col])
        numeric = pd.to_numeric(s, errors="coerce")
        numeric_ratio = numeric.notna().mean()
        if numeric_ratio < 0.9:
            excluded_rows.append({"column": col, "reason": "non_numeric"})
            continue

        df_out[col] = minmax_scale(s)

    excluded_df = pd.DataFrame(excluded_rows).drop_duplicates().reset_index(drop=True)
    return {"data": df_out, "excluded": excluded_df}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Standardize W2/W3 (per-item min-max), excluding specified columns."
    )
    parser.add_argument("--w2", default=DEFAULT_W2_PATH, help="Path to W2 CSV")
    parser.add_argument("--w3", default=DEFAULT_W3_PATH, help="Path to W3 CSV")
    parser.add_argument(
        "--out-dir-w2",
        default=os.path.dirname(os.path.abspath(DEFAULT_W2_PATH)),
        help="Output directory for W2 (default: same as input)",
    )
    parser.add_argument(
        "--out-dir-w3",
        default=os.path.dirname(os.path.abspath(DEFAULT_W3_PATH)),
        help="Output directory for W3 (default: same as input)",
    )
    args = parser.parse_args()

    w2 = pd.read_csv(args.w2, low_memory=False)
    w3 = pd.read_csv(args.w3, low_memory=False)

    w2_res = standardize_df(w2, "W2", SKIP_W2, META_W2)
    w3_res = standardize_df(w3, "W3", SKIP_W3, META_W3)

    w2_out_path = os.path.join(args.out_dir_w2, W2_OUT_NAME)
    w3_out_path = os.path.join(args.out_dir_w3, W3_OUT_NAME)

    w2_res["data"].to_csv(w2_out_path, index=False, encoding="utf-8-sig")
    w3_res["data"].to_csv(w3_out_path, index=False, encoding="utf-8-sig")

    w2_ex_path = os.path.join(args.out_dir_w2, "excluded_columns_W2.csv")
    w3_ex_path = os.path.join(args.out_dir_w3, "excluded_columns_W3.csv")

    w2_res["excluded"].to_csv(w2_ex_path, index=False, encoding="utf-8-sig")
    w3_res["excluded"].to_csv(w3_ex_path, index=False, encoding="utf-8-sig")

    print("W2 standardized:", w2_out_path)
    print("W3 standardized:", w3_out_path)
    print("Excluded lists:", w2_ex_path, w3_ex_path)


if __name__ == "__main__":
    main()
