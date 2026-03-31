from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


INPUT_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_20260326.csv"
)
OUTPUT_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_named8map_20260326.csv"
)
CODE_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN"
)


# User-specified named classes (all treated as grade 8), mapped to 8xx class IDs.
NAMED_CLASS_MAP: Dict[str, int] = {
    "國二仁": 801,
    "八年忠班": 802,
    "國二和": 803,
    "國二忠": 804,
    "八年孝班": 805,
    "八年仁班": 806,
    "八勤": 807,
    "二年忠班": 808,
    "國中二A": 809,
    "八義": 810,
    "國二義": 811,
}


def main() -> None:
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_PATH, low_memory=False, dtype={"student_id": str})

    required_cols = {"class", "class_original", "conversion_stage"}
    missing = required_cols - set(df.columns)
    if missing:
        raise KeyError(f"Input missing required columns: {sorted(missing)}")

    # Only replace rows that are currently fallback and class_original appears in mapping.
    target_mask = (
        df["conversion_stage"].eq("school_label_encoded_fallback")
        & df["class_original"].astype(str).isin(NAMED_CLASS_MAP.keys())
    )

    before_class = df.loc[target_mask, "class"].copy()
    df.loc[target_mask, "class"] = (
        df.loc[target_mask, "class_original"]
        .astype(str)
        .map(NAMED_CLASS_MAP)
        .astype("Int64")
    )
    df.loc[target_mask, "conversion_stage"] = "manual_named_grade8_mapping"

    # Ensure integer-like class output where possible.
    df["class"] = pd.to_numeric(df["class"], errors="coerce").astype("Int64")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    # Mapping table and summary
    mapping_df = pd.DataFrame(
        [{"class_original": k, "mapped_class": v} for k, v in NAMED_CLASS_MAP.items()]
    )
    mapping_df.to_csv(
        CODE_DIR / "named_grade8_class_mapping_table_20260326.csv",
        index=False,
        encoding="utf-8-sig",
    )

    changed_rows = int(target_mask.sum())
    changed_preview = (
        pd.DataFrame(
            {
                "student_id": df.loc[target_mask, "student_id"],
                "class_original": df.loc[target_mask, "class_original"],
                "class_before": before_class,
                "class_after": df.loc[target_mask, "class"],
            }
        )
        .sort_values(["class_original", "student_id"])
        .reset_index(drop=True)
    )
    changed_preview.to_csv(
        CODE_DIR / "named_grade8_class_mapping_changed_rows_20260326.csv",
        index=False,
        encoding="utf-8-sig",
    )

    summary_lines = [
        "Manual named grade-8 class mapping summary",
        "=========================================",
        f"Input file: {INPUT_PATH}",
        f"Output file: {OUTPUT_PATH}",
        "",
        f"Rows in input: {len(df)}",
        f"Rows updated by named mapping: {changed_rows}",
        "",
        "Mapping:",
    ]
    for k, v in NAMED_CLASS_MAP.items():
        n = int((df["class_original"].astype(str).eq(k) & target_mask).sum())
        summary_lines.append(f"- {k} -> {v} (updated rows: {n})")

    summary_path = CODE_DIR / "named_grade8_class_mapping_summary_20260326.txt"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    print("Done.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Updated rows: {changed_rows}")


if __name__ == "__main__":
    main()

