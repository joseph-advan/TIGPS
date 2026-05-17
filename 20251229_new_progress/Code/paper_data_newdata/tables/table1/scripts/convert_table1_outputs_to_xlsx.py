from __future__ import annotations

from pathlib import Path

import pandas as pd


TABLE1_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FOLDERS = [
    TABLE1_DIR / "outputs" / "01_online_activity_observed",
    TABLE1_DIR / "outputs" / "03_psychological_distress_observed",
]


def autosize_columns(worksheet) -> None:
    for column_cells in worksheet.columns:
        max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_len + 2, 12), 60)


def convert_csv_to_xlsx(csv_path: Path) -> Path:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    xlsx_path = csv_path.with_suffix(".xlsx")
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Table1")
        worksheet = writer.book["Table1"]
        worksheet.freeze_panes = "A2"
        autosize_columns(worksheet)
    return xlsx_path


def main() -> None:
    written: list[Path] = []
    for folder in OUTPUT_FOLDERS:
        if not folder.exists():
            continue
        for csv_path in sorted(folder.glob("*.csv")):
            written.append(convert_csv_to_xlsx(csv_path))

    print("Wrote/updated xlsx files:")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
