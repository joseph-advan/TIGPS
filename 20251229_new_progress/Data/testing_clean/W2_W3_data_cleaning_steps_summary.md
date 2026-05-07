# W2 / W3 Data Cleaning Steps Summary

Generated: 2026-05-06

## Scope

This note summarizes the data cleaning already done in:

- `Data/testing_clean/W2`
- `Data/testing_clean/W3`

It is based on the versioned CSV files, cleaning summaries, removed-row files, codebooks, and a fresh audit of the latest files:

- W2 latest: `W2/TIGPS_W2_studentdata_ver5.csv`
- W3 latest: `W3/TIGPS_W3_student_studentdata_ver4.csv`

## Current Latest Files

| Dataset | Latest file | Rows | Columns | Unique non-empty student IDs | Blank IDs | Duplicate ID rows |
|---|---|---:|---:|---:|---:|---:|
| W2 | `TIGPS_W2_studentdata_ver5.csv` | 6753 | 358 | 6753 | 0 | 0 |
| W3 | `TIGPS_W3_student_studentdata_ver4.csv` | 6686 | 382 | 6686 | 0 | 0 |

Latest W2/W3 ID overlap:

| Comparison | Count |
|---|---:|
| IDs in both W2 ver5 and W3 ver4 | 6603 |
| IDs only in W2 ver5 | 150 |
| IDs only in W3 ver4 | 83 |
| Net row difference, W2 minus W3 | 67 |

## Shared Cross-Year Cleaning

### Step 1. Cross-year ID intersection, raw to ver1

Source files:

- W2 source: `W2/TIGPS_W2_studentdata_ver0.csv`
- W3 source: `W3/TIGPS_W3_student_studentdata_ver00.csv`

Rule:

- Normalize IDs.
- Keep only IDs that appear in both W2 and W3.

Result:

| Dataset | Rows before | Rows after ver1 | Rows removed |
|---|---:|---:|---:|
| W2 | 8892 | 7236 | 1656 |
| W3 | 7714 | 7236 | 478 |

Notes:

- W2 had 8892 non-empty unique IDs.
- W3 had 7713 non-empty unique IDs and 1 blank-ID row.
- Cross-year overlap was 7236 unique IDs.

Artifacts:

- `cross_year_cleaning_ver1_summary.txt`
- `W2/w2_only_ids_from_ver0.txt`
- `W3/w3_only_ids_from_ver00.txt`
- `W2/w2_w3_overlap_ids_ver1.txt`

### Step 2. W2 anomaly rule with synced W3 removal, ver1 to ver2

Rule:

- In W2, selected key question prefixes were expanded to 143 columns.
- Drop W2 row if any selected column is empty or has numeric prefix `< 0`.
- Apply the same removed W2 student IDs to W3, so W2/W3 remain synchronized at ver2.

Result:

| Dataset | Rows before | Rows removed | Rows after ver2 |
|---|---:|---:|---:|
| W2 | 7236 | 396 | 6840 |
| W3 | 7236 | 396 | 6840 |

Removal reason:

- All 396 W2 removed rows were negative-value cases.
- No empty-only rows were removed in this step.

Artifacts:

- `ver2_cleaning_summary.txt`
- `W2/ver2_removed_student_ids_from_w2_rule.txt`

## W2 Cleaning Pipeline

### W2 ver2 to ver3: conflict and v13 anomaly removal

Input:

- `W2/TIGPS_W2_studentdata_ver2.csv`

Output:

- `W2/TIGPS_W2_studentdata_ver3.csv`

Cleaning steps:

| Step | Rule | Rows removed | Rows remaining |
|---|---|---:|---:|
| 1 | Remove groups with same `(school_id, class, v13)` but different `student_id` and `name` | 45 | 6795 |
| 2 | Remove `v13` anomalies: negative, `>60`, non-numeric, or empty | 42 | 6753 |
| 3 | Remove convenience columns: `cell`, `email`, `q_name`, `qb_code`, `school_name`, `status`, `student_oid` | 0 | 6753 |

Notes:

- Step 1 removed 21 conflict groups.
- Step 2 reason counts were `negative: 42`.
- Final W2 ver3 had 6753 unique student IDs.

Artifacts:

- `W2/w2_ver3_cleaning_summary.txt`
- `W2/w2_ver3_removed_step1_conflict.csv`
- `W2/w2_ver3_removed_step2_v13_anomaly.csv`

### W2 ver3 to ver4: class mapping cleanup

Input:

- `W2/TIGPS_W2_studentdata_ver3.csv`

Output:

- `W2/TIGPS_W2_studentdata_ver4.csv`

Cleaning steps:

- Convert non-numeric `class` values into numeric codes.
- Apply user rules:
  - `忠 -> 801`
  - `孝 -> 802`
  - `仁 -> 803`
  - `義 -> 804`
  - `勤 -> 805`
  - `和 -> 806`
  - `Y27 -> 999`
- Validate unresolved class values and post-mapping collision groups.

Result:

| Check | Before | After |
|---|---:|---:|
| Rows | 6753 | 6753 |
| Non-numeric class rows | 2138 | 0 |
| Unresolved rows | n/a | 0 |
| Collision groups after mapping | n/a | 0 |

Artifacts:

- `W2/w2_ver4_class_mapping_summary.txt`
- `W2/w2_ver4_class_mapping_table.csv`
- `W2/w2_ver4_class_unresolved_rows.csv`

### W2 ver4 to ver5: value encoding / mapping

Input:

- `W2/TIGPS_W2_studentdata_ver4.csv`

Output:

- `W2/TIGPS_W2_studentdata_ver5.csv`

Cleaning steps:

- Apply raw-to-cleaned mapping from `Code/paper_data/data_cleaning_audit/raw_to_cleaned_latest_group_summary.csv`.
- Convert most Chinese categorical response labels into numeric values.
- Keep selected unmapped nomination/free-text fields.

Result:

| Item | Count |
|---|---:|
| Rows | 6753 |
| Columns | 358 |
| `v*` columns | 351 |
| Mapped `v*` columns present in file | 331 |
| Unmapped `v*` columns | 20 |
| Changed cells | 2136585 |
| `v*` columns with Chinese text before mapping | 317 |
| `v*` columns with Chinese text after mapping | 2 |

Unmapped `v*` columns:

- `v14_1_01` to `v14_1_05`
- `v14_2_01` to `v14_2_05`
- `v14_3_01` to `v14_3_05`
- `v14_4_01` to `v14_4_05`

These are peer nomination fields and were intentionally left as IDs/numeric-like values.

Residual non-numeric `v*` columns:

| Column | Non-numeric rows | Main examples |
|---|---:|---|
| `v59_3h` | 6703 | `晚上11點`, `半夜12點`, `凌晨1點`, `晚上10點` |
| `v59_4h` | 6703 | `早上9點`, `早上8點`, `早上10點`, `早上7點` |

Fresh audit:

- W2 latest has no duplicated raw headers.
- W2 latest has no blank or duplicated `student_id`.
- W2 latest has no `>60` values in `v14_*` nomination columns.

Artifacts:

- `W2/w2_ver5_mapping_cleaning_summary.txt`
- `W2/w2_ver5_remaining_non_numeric_values.csv`

## W3 Cleaning Pipeline

### W3 ver00 to ver1: cross-year ID intersection

This was done together with W2 in shared Step 1.

Result:

| Dataset | Rows before | Rows after ver1 | Rows removed |
|---|---:|---:|---:|
| W3 | 7714 | 7236 | 478 |

Artifacts:

- `cross_year_cleaning_ver1_summary.txt`
- `W3/w3_only_ids_from_ver00.txt`

### W3 ver1 to ver2: synced W2 anomaly removal

This was done together with W2 in shared Step 2.

Rule:

- Remove W3 rows whose IDs were removed from W2 by the W2 selected-column anomaly rule.

Result:

| Dataset | Rows before | Rows removed | Rows after ver2 |
|---|---:|---:|---:|
| W3 | 7236 | 396 | 6840 |

Artifact:

- `ver2_cleaning_summary.txt`

### W3 ver2 to ver3: header rename

Input:

- `W3/TIGPS_W3_student_studentdata_ver2.csv`

Output:

- `W3/TIGPS_W3_student_studentdata_ver3.csv`

Cleaning step:

- Rename headers by question-code order using `Data/2025data/00_W3_學生問卷題目列表.csv`.
- Data values were unchanged.

Result:

| Check | Result |
|---|---:|
| Rows | 6840 to 6840, unchanged |
| Columns | 382 to 382, matched |
| Duplicate header labels after rename | 2 label groups |

Duplicate labels reported:

- `No ID`: 4 occurrences in the summary; fresh raw-header audit found 3 duplicate `No ID` headers in ver3.
- `____小時.2`: 2 occurrences in the summary.

Artifacts:

- `W3/ver3_header_rename_summary.txt`
- `W3/w3_ver2_vs_question_list_diff.txt`

### W3 ver3 to ver3.5: gender coding for columns 1 and 2

Input:

- `W3/TIGPS_W3_student_studentdata_ver3.csv`

Output:

- `W3/TIGPS_W3_student_studentdata_ver3.5_gender12_coded.csv`

Cleaning step:

- Encode gender-related columns `1` and `2`.
- Rule: male `=1`, female `=2`, other `=0`, missing `=''`.

Result:

| Column | Before | After |
|---|---|---|
| `1` | male/female labels | `1`, `2` |
| `2` | male/female/other labels | `1`, `2`, `0` |

Rows remained 6840.

Artifacts:

- `tmp_analysis/w3_ver3_gender12_coding_summary_v3.txt`
- `tmp_analysis/w3_ver3_options_encoding_plan_excluding_user_columns.csv`
- `tmp_analysis/w3_ver3_options_encoding_plan_excluding_user_columns.md`

### W3 ver3.5 to ver4: planned encoding and nomination outlier removal

Input:

- `W3/TIGPS_W3_student_studentdata_ver3.5_gender12_coded.csv`

Output:

- `W3/TIGPS_W3_student_studentdata_ver4.csv`

Cleaning step 1: encoding by plan

- Encoded plan types:
  - `gender`
  - `ordinal_3`
  - `ordinal_4`
  - `ordinal_5`
  - `binary_text`
  - `nominal_text`
  - `high_cardinality_text`
- Kept non-encoded plan types:
  - `peer_nomination`
  - `numeric_or_preencoded`
  - `identifier`
  - `free_text`
- User-requested skip columns were kept as-is.

Encoding result:

| Item | Count |
|---|---:|
| Source rows | 6840 |
| Source columns | 382 |
| Encoded columns | 329 |
| Skipped by user request | 27 |
| Kept by plan | 25 |
| Kept because no plan row | 0 |
| Changed cells | 1927513 |
| Unmapped non-empty cells left unchanged | 0 |

Cleaning step 2: remove peer nomination rows with value `>60`

Checked columns:

- `8-1_0` to `8-1_4`
- `8-2_0` to `8-2_4`
- `8-3_0` to `8-3_4`
- `8-4_0` to `8-4_4`

Result:

| Rows before removal | Rows removed | Rows after ver4 |
|---:|---:|---:|
| 6840 | 154 | 6686 |

Fresh audit:

- W3 latest has no duplicated raw headers.
- W3 latest has no blank or duplicated `student_id`.
- W3 latest still has 9 non-numeric columns, mostly intentionally skipped/free-text/time AM-PM fields:
  - `Unnamed: 4`
  - `No ID.1`
  - `17-1`
  - `18-1`
  - `No ID.2`
  - `58-1`
  - `58-2`
  - `58-3`
  - `58-4`

Artifacts:

- `W3/ver4_change_log.md`
- `W3/ver4_encoding_codebook.csv`
- `W3/ver4_removed_gt60_rows.csv`
- `tmp_analysis/w3_ver4_build_summary.json`

## What Has Not Been Fully Done Yet

### 1. Final W2/W3 IDs have not been re-synchronized

W2 and W3 were synchronized at ver2 with 6840 rows each. After that:

- W2 removed 87 rows through W2-specific rules.
- W3 removed 154 rows through W3-specific nomination rules.
- 4 IDs were removed by both W2 and W3 rules.

Therefore latest W2/W3 are no longer the same ID set:

- W2-only: 150 IDs
- W3-only: 83 IDs
- Shared final IDs: 6603

Recommendation:

- If the analysis requires paired W2/W3 samples, create a final aligned dataset using the intersection of W2 ver5 and W3 ver4 IDs, or explicitly decide whether to sync each wave's later removals to the other wave.

Related artifact:

- `tmp_analysis/w2_ver5_vs_w3_ver4_student_id_diff.csv`

### 2. W2 time text fields are still not numerically encoded

W2 still has non-numeric values in:

- `v59_3h`
- `v59_4h`

Recommendation:

- Convert labels such as `晚上11點`, `半夜12點`, `凌晨1點`, `早上9點` into a consistent 24-hour numeric hour scale if these fields are used in modeling.
- Otherwise mark them as excluded/free-text-like fields in the analysis codebook.

### 3. W3 skipped time/free-text fields remain non-numeric

W3 still has non-numeric values in skipped/free-text/time fields, especially:

- `58-1`, `58-2`, `58-3`, `58-4`: AM/PM labels.
- `17-1`, `18-1`, `No ID.1`, `No ID.2`, `Unnamed: 4`: free text or other text fields.

Recommendation:

- If W3 sleep/time columns are used, combine AM/PM with hour/minute columns and convert them to numeric time features.
- If free-text columns are not used, keep them explicitly excluded in downstream modeling.

### 4. Some W3 column names are still unclear

W3 has columns such as `No ID.1`, `No ID.2`, `No ID.3`, and mojibake-like skip-column names in logs.

Recommendation:

- Rename these columns to stable semantic names before final publication or modeling, especially if they are kept in the analysis dataset.
- Keep a codebook mapping original column names to final names.

### 5. Peer nomination validity has only been checked by simple numeric threshold

Current completed checks:

- W2 `v14_*` nomination columns: no values `>60`.
- W3 `8-1_*` to `8-4_*`: rows with any value `>60` were removed.

Still worth checking:

- Values should be valid classmates / roster numbers within each class, not only `<=60`.
- Values should not nominate self, if self-nomination is invalid for the research design.
- Duplicate nominations within the same item set may need a rule.

### 6. Final modeling codebook should state included vs excluded columns

Both waves now have encoded numeric columns plus intentionally preserved text/nomination fields.

Recommendation:

- Create a final W2/W3 analysis codebook with:
  - column name
  - wave
  - construct/question group
  - data type
  - encoding rule
  - whether included in modeling
  - reason if excluded

## Recommended Next Cleaning Step

For cross-year / paired modeling, the most important next step is to produce final aligned datasets:

- `W2_final_aligned_to_W3_ver4.csv`
- `W3_final_aligned_to_W2_ver5.csv`

using the 6603 shared final `student_id`s, unless the analysis intentionally allows wave-specific sample sizes.

