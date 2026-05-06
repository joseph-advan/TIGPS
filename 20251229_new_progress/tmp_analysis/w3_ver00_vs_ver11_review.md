# W3 ver00 vs ver11 Review (Inferred)

Generated: 2026-04-30

## Core result

- `TIGPS_W3_student_studentdata_ver00.csv`: 7714 rows (1 empty ID row), 382 cols.
- `W3_studentdata_ver11.csv`: 6713 rows, 382 cols.
- Final `ver11` IDs are exactly the same set as:
  - `Data/2024data/TIGPS_W2_studentdata_ver13.csv`
  - `Data/otherData/W2W3_Student_Basic_Info.csv`

## Row-level reduction decomposition (ver00 -> ver11)

Using available intermediate files in `Data/testing_clean/W3`:

1. ver00(non-empty IDs 7713) -> ver1(7236): remove 477 IDs
2. ver1(7236) -> ver2(6840): remove 396 IDs
3. ver2(6840) -> ver11(6713): remove 127 IDs

Total removed IDs: `477 + 396 + 127 = 1000` (plus 1 empty-ID row = 1001 row difference)

## Column-level transformation

- Same column count (382), but schema changed from long Chinese question text to short coded names.
- On shared IDs, 381/381 columns are deterministic raw->clean transforms.
- 47 columns are exact unchanged values (mostly seat/network nomination IDs, open text fields, height/weight/body-shape).
- 334 columns have value recoding.

## Inferred cleaning logic

1. ID normalize: trim spaces, remove empty/null IDs.
2. Keep only cross-year whitelist IDs (latest aligned set = 6713 IDs).
3. Rename headers to analysis schema (question-code style).
4. Apply per-column deterministic raw->clean mapping (text labels -> numeric codes).
5. Keep selected free-text columns (`其他*`, `Unnamed: 4`) as text.
6. Some fields are intentionally blanked in ver11:
   - `3`
   - `58-1`, `58-2`, `58-3`, `58-4`

## Notes vs changelog

- `00_W3_Change_log.txt` explains parts of ver6->ver10, but not all later harmonization details.
- Data evidence shows ver11 is fully synchronized to the latest W2/basic-info ID universe (6713).

## Reproducibility artifacts created

- `tmp_analysis/w3_ver00_to_ver11_header_mapping_by_position.csv`
- `tmp_analysis/w3_ver00_to_ver11_value_mapping_pairs.csv`
- `tmp_analysis/w3_ver00_to_ver11_column_stats.csv`
- `tmp_analysis/rebuild_w3_ver11_from_ver00.py`
- `tmp_analysis/W3_studentdata_ver11_rebuilt.csv`

Validation from script:

- rebuilt vs reference ver11: `cell_diff=0`, `row_diff=0`, `col_diff=0`
