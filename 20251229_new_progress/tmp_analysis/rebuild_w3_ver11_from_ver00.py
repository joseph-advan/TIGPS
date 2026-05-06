from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(r"c:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress")

RAW_W3_PATH = ROOT / r"Data/2025data/TIGPS_W3_student_studentdata_ver00.csv"
W2_WHITELIST_PATH = ROOT / r"Data/2024data/TIGPS_W2_studentdata_ver13.csv"
HEADER_MAP_PATH = ROOT / r"tmp_analysis/w3_ver00_to_ver11_header_mapping_by_position.csv"
VALUE_MAP_PATH = ROOT / r"tmp_analysis/w3_ver00_to_ver11_value_mapping_pairs.csv"
REFERENCE_VER11_PATH = ROOT / r"Data/2025data/W3_studentdata_ver11.csv"
OUTPUT_PATH = ROOT / r"tmp_analysis/W3_studentdata_ver11_rebuilt.csv"


def norm_id(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip()


def norm_val(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
        .str.strip()
        .replace({"nan": "", "NaN": "", "None": "", "NULL": ""})
    )


def main() -> None:
    raw = pd.read_csv(RAW_W3_PATH, encoding="utf-8-sig", low_memory=False)
    w2 = pd.read_csv(W2_WHITELIST_PATH, encoding="utf-8-sig", low_memory=False)
    header_map = pd.read_csv(HEADER_MAP_PATH, encoding="utf-8-sig", keep_default_na=False)
    value_map = pd.read_csv(VALUE_MAP_PATH, encoding="utf-8-sig", keep_default_na=False)
    ref = pd.read_csv(REFERENCE_VER11_PATH, encoding="utf-8-sig", low_memory=False)

    raw["student_id"] = norm_id(raw["TIGPS ID"])
    keep_ids = set(norm_id(w2["student_id"]))

    cleaned = raw[~raw["student_id"].isin(["", "nan", "NaN", "None", "NULL"])].copy()
    cleaned = cleaned[cleaned["student_id"].isin(keep_ids)].copy()

    # Build schema: student_id + 381 survey columns by position mapping
    raw_survey_cols = [c for c in cleaned.columns if c not in ("TIGPS ID", "student_id")]
    if len(raw_survey_cols) != len(header_map):
        raise ValueError(
            f"Survey column count mismatch: raw={len(raw_survey_cols)} vs header_map={len(header_map)}"
        )

    ordered_cols = ["student_id"] + raw_survey_cols
    rebuilt = cleaned[ordered_cols].copy()
    rebuilt.columns = ["student_id"] + header_map["ver11_col"].astype(str).tolist()

    # Apply deterministic raw->clean value mapping by ver11 column
    for col in rebuilt.columns:
        if col == "student_id":
            continue
        sub = value_map[value_map["ver11_col"] == col][["raw_value", "clean_value"]]
        mapping = dict(zip(sub["raw_value"].astype(str), sub["clean_value"].astype(str)))
        rebuilt[col] = norm_val(rebuilt[col]).map(lambda v: mapping.get(v, v))

    rebuilt.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    # Validate against existing ver11
    a = rebuilt.copy()
    b = ref.copy()
    a["student_id"] = norm_id(a["student_id"])
    b["student_id"] = norm_id(b["student_id"])
    a = a.sort_values("student_id").reset_index(drop=True)
    b = b.sort_values("student_id").reset_index(drop=True)

    # Ensure same column order as reference
    a = a[b.columns]

    aa = a.fillna("").astype(str).apply(lambda s: s.str.strip())
    bb = b.fillna("").astype(str).apply(lambda s: s.str.strip())
    neq = aa != bb

    cell_diff = int(neq.to_numpy().sum())
    row_diff = int(neq.any(axis=1).sum())
    col_diff = int(neq.any(axis=0).sum())

    print("Rebuild done:", OUTPUT_PATH)
    print("shape_rebuilt:", aa.shape)
    print("shape_reference:", bb.shape)
    print("cell_diff:", cell_diff)
    print("row_diff:", row_diff)
    print("col_diff:", col_diff)


if __name__ == "__main__":
    main()
