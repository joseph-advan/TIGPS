# TIGPS W3 ver4 Cleaning and Encoding Log

## Files
- Source data: `c:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver3_gender12_coded.csv`
- Encoding plan: `c:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\tmp_analysis\w3_ver3_options_encoding_plan_excluding_user_columns.csv`
- Output ver4: `c:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver4.csv`
- Removed rows (>60 in 8-1~8-4): `c:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver4_removed_gt60_rows.csv`
- Encoding codebook: `c:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver4_encoding_codebook.csv`

## Step 1: Apply Encoding by Plan
- Encoded by plan types: `gender`, `ordinal_3`, `ordinal_4`, `ordinal_5`, `binary_text`, `nominal_text`, `high_cardinality_text`.
- Kept by plan types (not encoded): `peer_nomination`, `numeric_or_preencoded`, `identifier`, `free_text`.

### User-Requested Skip Columns Found
- `17-1`
- `18-1`
- `58-1`
- `58-1-1`
- `58-1-2`
- `58-2`
- `58-2-1`
- `58-2-2`
- `58-3`
- `58-3-1`
- `58-3-2`
- `58-4`
- `58-4-1`
- `64`
- `65`
- `No ID.1`
- `No ID.2`
- `No ID.3`
- `Unnamed: 4`
- `_______分`
- `_______分.1`
- `____分鐘.1`
- `____分鐘.2`
- `____小時.1`
- `____小時.2`
- `上午_______點`
- `下午_______點`

### Requested Skip Names Not Found In This File
- `58-4-2`

### Encoding Summary
- Total columns in source: 382
- Encoded columns: 329
- Skipped by user request: 27
- Kept by plan (non-encodable types): 25
- Kept because no plan row: 0
- Total changed cells by encoding: 1927513
- Total unmapped non-empty cells left unchanged: 0

### Gender Coding
- Rule retained: male=1, female=2, other=0, missing=''.
- Column `1` before row-drop: {'1': 3447, '2': 3393}
- Column `2` before row-drop: {'1': 3409, '2': 3304, '0': 127}
- Column `1` after row-drop : {'2': 3350, '1': 3336}
- Column `2` after row-drop : {'1': 3307, '2': 3259, '0': 120}

## Step 2: Remove Rows with nomination value > 60
Checked columns:
- `8-1_0`
- `8-1_1`
- `8-1_2`
- `8-1_3`
- `8-1_4`
- `8-2_0`
- `8-2_1`
- `8-2_2`
- `8-2_3`
- `8-2_4`
- `8-3_0`
- `8-3_1`
- `8-3_2`
- `8-3_3`
- `8-3_4`
- `8-4_0`
- `8-4_1`
- `8-4_2`
- `8-4_3`
- `8-4_4`

- Rows before removal: 6840
- Rows removed (`any nomination column > 60`): 154
- Rows after removal (ver4): 6686

## Notes
- Alias handling applied: `58-4-2` matched as `No ID.3` in this schema and was skipped.
- Full per-column mapping dictionary is stored in codebook CSV.