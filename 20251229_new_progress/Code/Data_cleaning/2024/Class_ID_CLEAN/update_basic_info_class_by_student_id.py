from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd


W2_SOURCE_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\other\TIGPS_W2_studentdata_ver0.csv"
)
BASIC_INFO_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info.csv"
)

CODE_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN"
)
OUTPUT_BASIC_INFO_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_20260326.csv"
)


CH_NUM_MAP = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "兩": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}

LETTER_CLASS_MAP = {
    "甲": 1,
    "乙": 2,
    "丙": 3,
    "丁": 4,
    "戊": 5,
    "己": 6,
    "庚": 7,
    "辛": 8,
    "壬": 9,
    "癸": 10,
}

A_TO_J_MAP = {chr(ord("A") + i): i + 1 for i in range(10)}


def read_csv_with_fallback(path: Path) -> pd.DataFrame:
    encodings = ["utf-8-sig", "utf-8", "cp950", "big5", "latin1"]
    err = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except Exception as e:  # noqa: BLE001
            err = e
    raise RuntimeError(f"Cannot read {path} with fallback encodings") from err


def chinese_num_to_int(text: str) -> Optional[int]:
    s = str(text).strip()
    if s == "":
        return None
    if re.fullmatch(r"\d+", s):
        return int(s)

    # Handle 1-99 basic Chinese numeric expressions.
    if s in CH_NUM_MAP:
        return CH_NUM_MAP[s]
    if "十" in s:
        parts = s.split("十")
        if len(parts) != 2:
            return None
        left, right = parts[0], parts[1]
        tens = 1 if left == "" else CH_NUM_MAP.get(left)
        if tens is None:
            return None
        ones = 0 if right == "" else CH_NUM_MAP.get(right)
        if ones is None:
            return None
        return tens * 10 + ones
    return None


def parse_class_to_numeric(raw: object) -> Tuple[Optional[int], str]:
    if pd.isna(raw):
        return None, "missing"

    s = str(raw).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None, "missing"

    # 1) numeric integer
    if re.fullmatch(r"[+-]?\d+", s):
        return int(s), "numeric_integer"

    # 2) float integer-like, e.g. 801.0
    if re.fullmatch(r"[+-]?\d+\.0+", s):
        return int(float(s)), "numeric_integer_decimal0"

    # 3) Chinese grade/class pattern: 八年十班, 8年1班
    m = re.fullmatch(r"([零〇一二三四五六七八九十兩\d]+)年([零〇一二三四五六七八九十兩\d]+)班", s)
    if m:
        g = chinese_num_to_int(m.group(1))
        c = chinese_num_to_int(m.group(2))
        if g is not None and c is not None:
            return g * 100 + c, "grade_year_class_pattern"

    # 4) 國二03 / 國2甲 / 國二甲
    m = re.fullmatch(r"國([零〇一二三四五六七八九十兩\d])([零〇一二三四五六七八九十兩\d]{1,2}|[甲乙丙丁戊己庚辛壬癸A-Ja-j])", s)
    if m:
        grade = chinese_num_to_int(m.group(1))
        cls_raw = m.group(2).upper()
        cls_num = None
        if cls_raw in LETTER_CLASS_MAP:
            cls_num = LETTER_CLASS_MAP[cls_raw]
        elif cls_raw in A_TO_J_MAP:
            cls_num = A_TO_J_MAP[cls_raw]
        else:
            cls_num = chinese_num_to_int(cls_raw)
        if grade is not None and cls_num is not None:
            return grade * 100 + cls_num, "nation_grade_class_pattern"

    # 5) Alnum ending with 2-3 digits: J204, Y27 -> 204, 27
    m = re.fullmatch(r"[A-Za-z]+(\d{2,3})", s)
    if m:
        return int(m.group(1)), "alnum_trailing_digits"

    # 6) Generic trailing digits in mixed text
    m = re.search(r"(\d{2,3})$", s)
    if m:
        return int(m.group(1)), "generic_trailing_digits"

    return None, "unparsed"


@dataclass
class UpdateSummary:
    total_rows: int
    matched_student_id_rows: int
    updated_rows: int
    fallback_encoded_rows: int
    still_null_rows: int


def main() -> None:
    CODE_DIR.mkdir(parents=True, exist_ok=True)

    src = read_csv_with_fallback(W2_SOURCE_PATH)
    if "student_id" not in src.columns or "class" not in src.columns:
        raise KeyError("W2 source requires columns: student_id, class")

    basic = pd.read_csv(BASIC_INFO_PATH, low_memory=False, dtype={"student_id": str})
    if "student_id" not in basic.columns or "class" not in basic.columns:
        raise KeyError("Basic info requires columns: student_id, class")

    src = src[["student_id", "school_id", "class"]].copy()
    src["student_id"] = src["student_id"].astype(str).str.strip()
    src["school_id"] = pd.to_numeric(src["school_id"], errors="coerce").astype("Int64")

    parsed = src["class"].apply(parse_class_to_numeric)
    src["class_numeric_parsed"] = parsed.apply(lambda x: x[0]).astype("Int64")
    src["parse_method"] = parsed.apply(lambda x: x[1])

    # Fallback: unresolved classes -> school-specific label encoding
    unresolved_mask = src["class_numeric_parsed"].isna()
    unresolved = src.loc[unresolved_mask, ["school_id", "class"]].copy()
    unresolved["class"] = unresolved["class"].astype(str).str.strip()

    fallback_map: Dict[Tuple[int, str], int] = {}
    for school_id, grp in unresolved.groupby("school_id", dropna=False):
        if pd.isna(school_id):
            continue
        labels = sorted([x for x in grp["class"].dropna().unique() if x and x.lower() not in {"nan", "none", "null"}])
        for idx, lbl in enumerate(labels, start=1):
            # Make deterministic numeric id per school to keep all class values numeric.
            # Example: school 11301 label-1 -> 1130101
            fallback_map[(int(school_id), lbl)] = int(school_id) * 100 + idx

    def apply_fallback(row: pd.Series) -> Optional[int]:
        if pd.notna(row["class_numeric_parsed"]):
            return int(row["class_numeric_parsed"])
        sid = row["school_id"]
        cls = str(row["class"]).strip()
        if pd.isna(sid):
            return None
        return fallback_map.get((int(sid), cls))

    src["class_numeric_final"] = src.apply(apply_fallback, axis=1).astype("Int64")
    src["conversion_stage"] = src["parse_method"]
    src.loc[
        src["parse_method"].eq("unparsed") & src["class_numeric_final"].notna(),
        "conversion_stage",
    ] = "school_label_encoded_fallback"

    # Keep best mapping per student_id (first non-null final)
    src = src.sort_values(
        by=["class_numeric_final", "parse_method"],
        key=lambda c: c.notna().astype(int),
        ascending=False,
    )
    map_df = src.drop_duplicates(subset=["student_id"], keep="first")[
        ["student_id", "class", "class_numeric_final", "parse_method", "conversion_stage"]
    ].copy()
    map_df = map_df.rename(columns={"class": "class_source_raw"})

    # Update target file by student_id
    basic["student_id"] = basic["student_id"].astype(str).str.strip()
    merged = basic.merge(map_df, on="student_id", how="left")

    merged["class_original"] = merged["class"]
    merged["class_numeric_updated"] = merged["class_numeric_final"].astype("Int64")
    merged["class"] = merged["class_numeric_updated"]

    out_cols = ["student_id", "school_id", "school_name", "class", "name", "v13", "class_original", "conversion_stage"]
    out_cols = [c for c in out_cols if c in merged.columns]
    out_df = merged[out_cols].copy()

    # Save outputs
    OUTPUT_BASIC_INFO_PATH.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_BASIC_INFO_PATH, index=False, encoding="utf-8-sig")

    map_path = CODE_DIR / "W2_ver0_student_id_class_numeric_mapping_20260326.csv"
    map_df.to_csv(map_path, index=False, encoding="utf-8-sig")

    audit_path = CODE_DIR / "W2W3_basic_info_class_update_audit_20260326.csv"
    merged[
        [
            "student_id",
            "class_original",
            "class_numeric_updated",
            "parse_method",
            "conversion_stage",
        ]
    ].to_csv(audit_path, index=False, encoding="utf-8-sig")

    summary = UpdateSummary(
        total_rows=len(merged),
        matched_student_id_rows=int(merged["class_numeric_final"].notna().sum()),
        updated_rows=int(merged["class"].notna().sum()),
        fallback_encoded_rows=int((merged["conversion_stage"] == "school_label_encoded_fallback").sum()),
        still_null_rows=int(merged["class"].isna().sum()),
    )

    summary_txt = CODE_DIR / "W2W3_basic_info_class_update_summary_20260326.txt"
    lines = [
        "W2W3_Student_Basic_Info class numeric update summary",
        "===================================================",
        f"Source W2 class file: {W2_SOURCE_PATH}",
        f"Target basic info: {BASIC_INFO_PATH}",
        "",
        f"total_rows: {summary.total_rows}",
        f"matched_student_id_rows (has mapped numeric class): {summary.matched_student_id_rows}",
        f"updated_rows (class non-null in output): {summary.updated_rows}",
        f"fallback_encoded_rows: {summary.fallback_encoded_rows}",
        f"still_null_rows: {summary.still_null_rows}",
        "",
        f"Output basic info file: {OUTPUT_BASIC_INFO_PATH}",
        f"Student mapping file: {map_path}",
        f"Audit file: {audit_path}",
    ]
    summary_txt.write_text("\n".join(lines), encoding="utf-8")

    print("Done.")
    print(f"Output file: {OUTPUT_BASIC_INFO_PATH}")
    print(f"Summary: {summary_txt}")


if __name__ == "__main__":
    main()
