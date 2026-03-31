from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Set

import pandas as pd


DUP_GROUP_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN\W2_ver10_duplicate_details_school_class_v13_20260326.csv"
)

W2_VER10_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver10.csv"
)
W2_VER11_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv"
)

BASIC_INFO_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_named8map_20260326.csv"
)
BASIC_INFO_NEW_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info_class_numeric_updated_named8map_after_w2ver11_20260330.csv"
)

W3_VER9_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver9.csv"
)
W3_VER10_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv"
)

W2_LOG_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\00_W2_Change_log.txt"
)
W3_LOG_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\00_W3_Change_log.txt"
)

CODE_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN"
)


def detect_text_encoding(path: Path) -> str:
    for enc in ["utf-8-sig", "utf-8", "cp950", "big5", "latin1"]:
        try:
            _ = path.read_text(encoding=enc)
            return enc
        except Exception:  # noqa: BLE001
            continue
    return "utf-8"


def parse_remove_ids(dup_path: Path) -> List[str]:
    dup = pd.read_csv(dup_path, low_memory=False)
    ids: Set[str] = set()
    for s in dup["student_ids"].astype(str):
        ids.update([x.strip() for x in s.split(";") if x.strip()])
    return sorted(ids)


def drop_by_student_id(df: pd.DataFrame, remove_ids: Set[str]) -> pd.DataFrame:
    out = df.copy()
    out["student_id"] = out["student_id"].astype(str).str.strip()
    return out.loc[~out["student_id"].isin(remove_ids)].copy()


def append_log(path: Path, block: str) -> None:
    enc = detect_text_encoding(path)
    with path.open("a", encoding=enc, newline="") as f:
        f.write(block)


def main() -> None:
    CODE_DIR.mkdir(parents=True, exist_ok=True)

    remove_ids = parse_remove_ids(DUP_GROUP_PATH)
    remove_set = set(remove_ids)
    if len(remove_ids) != 22:
        raise ValueError(f"Expected 22 ids from duplicate file, got {len(remove_ids)}")

    # W2 ver10 -> ver11
    w2 = pd.read_csv(W2_VER10_PATH, low_memory=False, dtype={"student_id": str})
    w2_before = len(w2)
    w2_after_df = drop_by_student_id(w2, remove_set)
    w2_after = len(w2_after_df)
    w2_removed = w2_before - w2_after
    w2_after_df.to_csv(W2_VER11_PATH, index=False, encoding="utf-8-sig")

    # Basic info update using new W2 list
    b = pd.read_csv(BASIC_INFO_PATH, low_memory=False, dtype={"student_id": str})
    b_before = len(b)
    b_after_df = drop_by_student_id(b, remove_set)
    b_after = len(b_after_df)
    b_removed = b_before - b_after
    b_after_df.to_csv(BASIC_INFO_NEW_PATH, index=False, encoding="utf-8-sig")

    # W3 ver9 -> ver10
    w3 = pd.read_csv(W3_VER9_PATH, low_memory=False, dtype={"student_id": str})
    w3_before = len(w3)
    w3_after_df = drop_by_student_id(w3, remove_set)
    w3_after = len(w3_after_df)
    w3_removed = w3_before - w3_after
    w3_after_df.to_csv(W3_VER10_PATH, index=False, encoding="utf-8-sig")

    # Presence audit
    id_audit_rows = []
    w2_ids = set(w2["student_id"].astype(str).str.strip())
    w3_ids = set(w3["student_id"].astype(str).str.strip())
    b_ids = set(b["student_id"].astype(str).str.strip())
    for sid in remove_ids:
        id_audit_rows.append(
            {
                "student_id": sid,
                "in_w2_ver10": sid in w2_ids,
                "in_w3_ver9": sid in w3_ids,
                "in_basic_info_before": sid in b_ids,
            }
        )
    id_audit_df = pd.DataFrame(id_audit_rows)
    id_audit_path = CODE_DIR / "removed_22_ids_presence_audit_20260330.csv"
    id_audit_df.to_csv(id_audit_path, index=False, encoding="utf-8-sig")

    remove_list_path = CODE_DIR / "removed_22_student_ids_20260330.txt"
    remove_list_path.write_text("\n".join(remove_ids), encoding="utf-8")

    summary_path = CODE_DIR / "remove_22_ids_build_ver11_w3ver10_summary_20260330.txt"
    summary_lines = [
        "Remove 22 duplicate student_id and build new versions",
        "====================================================",
        f"duplicate source file: {DUP_GROUP_PATH}",
        f"remove_ids_count: {len(remove_ids)}",
        "",
        f"W2 before: {w2_before}",
        f"W2 removed: {w2_removed}",
        f"W2 after (ver11): {w2_after}",
        f"W2 output: {W2_VER11_PATH}",
        "",
        f"BasicInfo before: {b_before}",
        f"BasicInfo removed: {b_removed}",
        f"BasicInfo after: {b_after}",
        f"BasicInfo output: {BASIC_INFO_NEW_PATH}",
        "",
        f"W3 before: {w3_before}",
        f"W3 removed: {w3_removed}",
        f"W3 after (ver10): {w3_after}",
        f"W3 output: {W3_VER10_PATH}",
        "",
        f"remove list: {remove_list_path}",
        f"id presence audit: {id_audit_path}",
    ]
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    first30 = ", ".join(remove_ids[:30])

    w2_block = (
        "\n\n--------------------------------------------------------------------------------\n"
        f"[Ver 10 -> Ver 11 | remove duplicate 22 student_id] ({now})\n"
        "--------------------------------------------------------------------------------\n"
        f"Input file : {W2_VER10_PATH.name}\n"
        f"Reference  : {DUP_GROUP_PATH.name}\n"
        f"Output file: {W2_VER11_PATH.name}\n"
        "\n"
        "Reason:\n"
        "- Remove 22 student_id that belonged to duplicated (school_id, class, v13) groups.\n"
        "\n"
        "Changes:\n"
        f"- Source rows: {w2_before}\n"
        f"- Removed rows: {w2_removed}\n"
        f"- Output rows: {w2_after}\n"
        f"- Removed student_id (22): {first30}\n"
        "\n"
        "Related updates:\n"
        f"- Basic info updated file: {BASIC_INFO_NEW_PATH.name} (rows: {b_before} -> {b_after})\n"
        f"- W3 updated file: {W3_VER10_PATH.name} (rows: {w3_before} -> {w3_after})\n"
        "\n"
        "Audit files:\n"
        f"- {remove_list_path.name}\n"
        f"- {id_audit_path.name}\n"
        f"- {summary_path.name}\n"
    )
    append_log(W2_LOG_PATH, w2_block)

    w3_block = (
        "\n\n--------------------------------------------------------------------------------\n"
        f"[Ver 9 -> Ver 10 | remove duplicate 22 student_id from W2 duplicate list] ({now})\n"
        "--------------------------------------------------------------------------------\n"
        f"Input file : {W3_VER9_PATH.name}\n"
        f"Reference  : {DUP_GROUP_PATH.name}\n"
        f"Output file: {W3_VER10_PATH.name}\n"
        "\n"
        "Reason:\n"
        "- Keep W3 aligned with W2 ver11 after removing duplicated seat-key student_id.\n"
        "\n"
        "Changes:\n"
        f"- Source rows: {w3_before}\n"
        f"- Removed rows: {w3_removed}\n"
        f"- Output rows: {w3_after}\n"
        f"- Removed student_id list source: {remove_list_path.name}\n"
    )
    append_log(W3_LOG_PATH, w3_block)

    print("Done.")
    print(f"W2 ver11: {W2_VER11_PATH}")
    print(f"Basic info updated: {BASIC_INFO_NEW_PATH}")
    print(f"W3 ver10: {W3_VER10_PATH}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()

