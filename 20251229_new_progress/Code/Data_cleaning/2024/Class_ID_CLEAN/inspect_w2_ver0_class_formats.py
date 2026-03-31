from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


DATA_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\other\TIGPS_W2_studentdata_ver0.csv"
)
OUT_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\Class_ID_CLEAN"
)


def read_csv_with_fallback(path: Path) -> pd.DataFrame:
    encodings = ["utf-8-sig", "utf-8", "cp950", "big5", "latin1"]
    last_error = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except Exception as e:  # noqa: BLE001
            last_error = e
    raise RuntimeError(f"Failed to read CSV with tried encodings: {encodings}") from last_error


def has_chinese(s: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", s))


def has_letter(s: str) -> bool:
    return bool(re.search(r"[A-Za-z]", s))


def has_digit(s: str) -> bool:
    return bool(re.search(r"\d", s))


def is_int_string(s: str) -> bool:
    return bool(re.fullmatch(r"[+-]?\d+", s))


def is_intlike_float_string(s: str) -> bool:
    return bool(re.fullmatch(r"[+-]?\d+\.0+", s))


def is_nonint_float_string(s: str) -> bool:
    if not re.fullmatch(r"[+-]?\d+\.\d+", s):
        return False
    return not is_intlike_float_string(s)


def is_chinese_grade_class(s: str) -> bool:
    # Examples: 八年十班, 8年10班, 八年3班
    return bool(re.fullmatch(r"[零〇一二三四五六七八九十百兩\d]+年[零〇一二三四五六七八九十百兩\d]+班", s))


def classify_value(s: str) -> str:
    if s == "":
        return "empty_string"
    if is_int_string(s):
        return "numeric_integer"
    if is_intlike_float_string(s):
        return "numeric_integer_with_decimal_zero"
    if is_nonint_float_string(s):
        return "numeric_decimal_noninteger"
    if is_chinese_grade_class(s):
        return "chinese_grade_class_pattern"
    if has_chinese(s) and has_digit(s):
        return "contains_chinese_and_digit_other"
    if has_chinese(s):
        return "contains_chinese_other"
    if has_letter(s) and has_digit(s):
        return "alphanumeric_mixed"
    if has_letter(s):
        return "alphabetic_only"
    if has_digit(s):
        return "digits_with_symbols"
    return "symbols_or_other"


def format_examples(series: pd.Series, k: int = 10) -> str:
    vals = series.dropna().astype(str).str.strip()
    vals = vals[vals != ""]
    if vals.empty:
        return "(none)"
    top = vals.value_counts().head(k)
    return "; ".join([f"{idx} ({cnt})" for idx, cnt in top.items()])


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = read_csv_with_fallback(DATA_PATH)
    if "class" not in df.columns:
        raise KeyError("Column 'class' not found in CSV.")

    raw = df["class"]
    raw_str = raw.astype(str).str.strip()
    missing_mask = raw.isna() | raw_str.str.lower().isin(["nan", "none", "null"]) | (raw_str == "")
    non_missing = raw_str[~missing_mask].copy()

    classified = non_missing.apply(classify_value)
    class_df = pd.DataFrame({"class_value": non_missing, "format_type": classified})

    # Summary by type
    type_counts = class_df["format_type"].value_counts(dropna=False).rename_axis("format_type").reset_index(name="count")
    type_counts["pct_of_non_missing"] = type_counts["count"] / len(non_missing) * 100

    # Frequency of each exact value
    value_counts = class_df["class_value"].value_counts(dropna=False).rename_axis("class_value").reset_index(name="count")

    # Numeric-only deep check
    numeric_like_mask = class_df["format_type"].isin(
        ["numeric_integer", "numeric_integer_with_decimal_zero", "numeric_decimal_noninteger"]
    )
    numeric_vals = class_df.loc[numeric_like_mask, "class_value"].copy()
    numeric_clean = pd.to_numeric(numeric_vals, errors="coerce")
    numeric_summary = {
        "numeric_rows": int(numeric_clean.notna().sum()),
        "numeric_unique_values": int(numeric_clean.dropna().nunique()),
        "numeric_min": float(numeric_clean.min()) if numeric_clean.notna().any() else None,
        "numeric_max": float(numeric_clean.max()) if numeric_clean.notna().any() else None,
        "numeric_noninteger_rows": int((numeric_clean.dropna() % 1 != 0).sum()) if numeric_clean.notna().any() else 0,
    }

    # Examples by format
    examples_rows: List[Dict[str, str]] = []
    for fmt in type_counts["format_type"].tolist():
        ex = format_examples(class_df.loc[class_df["format_type"] == fmt, "class_value"], k=10)
        examples_rows.append({"format_type": fmt, "examples_top10": ex})
    examples_df = pd.DataFrame(examples_rows)

    # Save CSV outputs
    type_counts_path = OUT_DIR / "W2_ver0_class_format_type_counts.csv"
    value_counts_path = OUT_DIR / "W2_ver0_class_value_counts.csv"
    examples_path = OUT_DIR / "W2_ver0_class_format_examples.csv"

    type_counts.to_csv(type_counts_path, index=False, encoding="utf-8-sig")
    value_counts.to_csv(value_counts_path, index=False, encoding="utf-8-sig")
    examples_df.to_csv(examples_path, index=False, encoding="utf-8-sig")

    # Build text report
    total_rows = len(df)
    missing_rows = int(missing_mask.sum())
    non_missing_rows = int((~missing_mask).sum())

    non_numeric_types = type_counts[
        ~type_counts["format_type"].isin(
            ["numeric_integer", "numeric_integer_with_decimal_zero", "numeric_decimal_noninteger"]
        )
    ]

    lines: List[str] = []
    lines.append("W2_ver0 class 欄位格式檢查報告")
    lines.append("================================")
    lines.append("")
    lines.append(f"資料來源: {DATA_PATH}")
    lines.append(f"總列數: {total_rows}")
    lines.append(f"class 缺值列數: {missing_rows}")
    lines.append(f"class 非缺值列數: {non_missing_rows}")
    lines.append("")
    lines.append("一、格式分佈")
    for _, r in type_counts.iterrows():
        lines.append(
            f"- {r['format_type']}: {int(r['count'])} ({float(r['pct_of_non_missing']):.2f}% of non-missing)"
        )
    lines.append("")
    lines.append("二、是否有中文班級型態（例如: 八年十班）")
    has_cn_pattern = (type_counts["format_type"] == "chinese_grade_class_pattern").any()
    cn_count = int(
        type_counts.loc[type_counts["format_type"] == "chinese_grade_class_pattern", "count"].sum()
    )
    lines.append(f"- chinese_grade_class_pattern 出現筆數: {cn_count}")
    lines.append(f"- 是否出現這種型態: {'有' if has_cn_pattern else '沒有'}")
    lines.append("")
    lines.append("三、數字格式細節")
    lines.append(f"- numeric_rows: {numeric_summary['numeric_rows']}")
    lines.append(f"- numeric_unique_values: {numeric_summary['numeric_unique_values']}")
    lines.append(f"- numeric_min: {numeric_summary['numeric_min']}")
    lines.append(f"- numeric_max: {numeric_summary['numeric_max']}")
    lines.append(f"- numeric_noninteger_rows: {numeric_summary['numeric_noninteger_rows']}")
    lines.append("")
    lines.append("四、各格式常見值（前10）")
    for _, r in examples_df.iterrows():
        lines.append(f"- {r['format_type']}: {r['examples_top10']}")
    lines.append("")
    lines.append("五、非純數字格式提醒")
    if non_numeric_types.empty:
        lines.append("- 沒有非數字格式。")
    else:
        for _, r in non_numeric_types.iterrows():
            lines.append(f"- {r['format_type']}: {int(r['count'])} 筆")
    lines.append("")
    lines.append("輸出檔案:")
    lines.append(f"- {type_counts_path}")
    lines.append(f"- {value_counts_path}")
    lines.append(f"- {examples_path}")

    report_path = OUT_DIR / "W2_ver0_class_format_report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Done. Report: {report_path}")


if __name__ == "__main__":
    main()

