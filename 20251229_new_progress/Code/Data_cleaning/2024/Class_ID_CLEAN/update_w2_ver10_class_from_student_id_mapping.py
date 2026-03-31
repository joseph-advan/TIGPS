from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd


VER9_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver9.csv"
)
CLASS_MAP_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_named8map_20260326.csv"
)
VER10_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver10.csv"
)
CHANGE_LOG_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\00_W2_Change_log.txt"
)
CODE_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN"
)


def read_text_encoding(path: Path) -> str:
    for enc in ["utf-8-sig", "utf-8", "cp950", "big5", "latin1"]:
        try:
            _ = path.read_text(encoding=enc)
            return enc
        except Exception:  # noqa: BLE001
            continue
    return "utf-8"


def normalize_to_int_if_possible(x: object) -> Optional[int]:
    if pd.isna(x):
        return None
    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None
    if s.isdigit():
        return int(s)
    try:
        f = float(s)
    except Exception:  # noqa: BLE001
        return None
    if f.is_integer():
        return int(f)
    return None


def main() -> None:
    CODE_DIR.mkdir(parents=True, exist_ok=True)

    w2 = pd.read_csv(VER9_PATH, low_memory=False, dtype={"student_id": str})
    m = pd.read_csv(CLASS_MAP_PATH, low_memory=False, dtype={"student_id": str})

    required_w2 = {"student_id", "class"}
    required_m = {"student_id", "class", "conversion_stage", "class_original"}
    if not required_w2.issubset(w2.columns):
        raise KeyError(f"W2 ver9 missing columns: {sorted(required_w2 - set(w2.columns))}")
    if not required_m.issubset(m.columns):
        raise KeyError(f"Class mapping file missing columns: {sorted(required_m - set(m.columns))}")

    w2["student_id"] = w2["student_id"].astype(str).str.strip()
    m["student_id"] = m["student_id"].astype(str).str.strip()
    m["mapped_class"] = pd.to_numeric(m["class"], errors="coerce").astype("Int64")

    map_keep = (
        m[["student_id", "mapped_class", "conversion_stage", "class_original"]]
        .drop_duplicates(subset=["student_id"], keep="first")
        .copy()
    )

    merged = w2.merge(map_keep, on="student_id", how="left")
    missing_map_n = int(merged["mapped_class"].isna().sum())
    if missing_map_n > 0:
        raise ValueError(f"There are {missing_map_n} rows in ver9 without class mapping by student_id.")

    merged["class_before"] = merged["class"]
    merged["class_after"] = merged["mapped_class"]

    old_norm = merged["class_before"].map(normalize_to_int_if_possible).astype("Int64")
    new_norm = merged["class_after"].astype("Int64")
    # Treat non-numeric/unknown old class as changed when new numeric class exists.
    merged["class_changed"] = old_norm.isna() | (old_norm != new_norm)

    changed_n = int(merged["class_changed"].sum())
    unchanged_n = int((~merged["class_changed"]).sum())

    # Replace class in final ver10
    merged["class"] = merged["class_after"].astype("Int64")

    # Keep original column order
    final_cols = list(w2.columns)
    ver10 = merged[final_cols].copy()
    ver10.to_csv(VER10_PATH, index=False, encoding="utf-8-sig")

    # Audit file
    audit = merged[
        [
            "student_id",
            "class_before",
            "class_after",
            "class_changed",
            "conversion_stage",
            "class_original",
        ]
    ].copy()
    audit_path = CODE_DIR / "W2_ver9_to_ver10_class_update_audit_20260326.csv"
    audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

    stage_counts = (
        merged["conversion_stage"]
        .value_counts(dropna=False)
        .rename_axis("conversion_stage")
        .reset_index(name="count")
    )
    stage_path = CODE_DIR / "W2_ver10_class_conversion_stage_counts_20260326.csv"
    stage_counts.to_csv(stage_path, index=False, encoding="utf-8-sig")

    # Append change log
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stage_lines = "\n".join([f"- {r['conversion_stage']}: {int(r['count'])}" for _, r in stage_counts.iterrows()])

    manual_map_lines = "\n".join(
        [
            "- 國二仁 -> 801",
            "- 八年忠班 -> 802",
            "- 國二和 -> 803",
            "- 國二忠 -> 804",
            "- 八年孝班 -> 805",
            "- 八年仁班 -> 806",
            "- 八勤 -> 807",
            "- 二年忠班 -> 808",
            "- 國中二A -> 809",
            "- 八義 -> 810",
            "- 國二義 -> 811",
        ]
    )

    log_block = (
        "\n\n--------------------------------------------------------------------------------\n"
        f"[Ver 9 -> Ver 10 | class update by student_id mapping] ({now})\n"
        "--------------------------------------------------------------------------------\n"
        f"Input file : {VER9_PATH.name}\n"
        f"Reference  : {CLASS_MAP_PATH.name}\n"
        f"Output file: {VER10_PATH.name}\n"
        "\n"
        "Reason:\n"
        "- Normalize class values into numeric IDs using student_id-level mapping.\n"
        "- Resolve named grade-8 classes into fixed numeric class codes.\n"
        "\n"
        "Changes:\n"
        f"- Source rows: {len(w2)}\n"
        f"- Mapped rows by student_id: {len(w2) - missing_map_n}\n"
        f"- class changed rows: {changed_n}\n"
        f"- class unchanged rows: {unchanged_n}\n"
        f"- Unmapped rows: {missing_map_n}\n"
        "\n"
        "Class conversion stage counts:\n"
        f"{stage_lines}\n"
        "\n"
        "Manual named grade-8 mapping used:\n"
        f"{manual_map_lines}\n"
        "\n"
        "Audit files:\n"
        f"- {audit_path.name}\n"
        f"- {stage_path.name}\n"
    )

    enc = read_text_encoding(CHANGE_LOG_PATH)
    with CHANGE_LOG_PATH.open("a", encoding=enc, newline="") as f:
        f.write(log_block)

    print("Done.")
    print(f"Output ver10: {VER10_PATH}")
    print(f"Changed rows: {changed_n}, unchanged rows: {unchanged_n}")
    print(f"Changelog appended: {CHANGE_LOG_PATH}")


if __name__ == "__main__":
    main()
