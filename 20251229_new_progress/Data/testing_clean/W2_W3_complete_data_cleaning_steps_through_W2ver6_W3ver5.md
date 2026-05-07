# W2 / W3 Data Cleaning Documentation

Generated: 2026-05-06

## Purpose

This document describes the complete data cleaning flow applied to the W2 and W3 student questionnaire datasets, starting from the original raw data and ending with the current cleaned, aligned analysis datasets.

The final goal of the cleaning process was to produce two wave-specific datasets that:

- contain the same students in W2 and W3,
- have one row per student,
- use consistent `student_id` values,
- have major categorical questionnaire responses encoded for analysis,
- have clean peer nomination fields for network analysis,
- preserve nominations to classmates who may not be in the final questionnaire sample.

The current final outputs are:

| Wave | Final dataset | Rows | Description |
|---|---|---:|---|
| W2 | `W2/TIGPS_W2_studentdata_ver6.csv` | 6603 | Cleaned W2 questionnaire data aligned to W3 |
| W3 | `W3/TIGPS_W3_student_studentdata_ver5.csv` | 6603 | Cleaned W3 questionnaire data aligned to W2 |

Both final datasets contain the same `6603` student IDs in the same row order.

## Raw Data Starting Point

The original W2 and W3 questionnaire files had different row counts and slightly different identifier structures.

| Wave | Raw rows | Raw ID field | Notes |
|---|---:|---|---|
| W2 | 8892 | `student_id` | No blank IDs in the raw file used for this cleaning pipeline |
| W3 | 7714 | `TIGPS ID` | One row had a blank ID before cleaning |

Because the downstream analysis requires comparing students across two years, the first major cleaning task was to create a shared W2/W3 analysis population.

## Overall Cleaning Flow

The full cleaning workflow can be summarized as:

1. Normalize student IDs and keep only students appearing in both W2 and W3.
2. Remove W2 rows with clear selected-question anomalies and remove the same students from W3 to keep the waves synchronized.
3. Clean W2 seat number and class fields so peer nomination mapping can use `(school_id, class, seat number)`.
4. Rename and encode W3 columns into a stable question-code schema.
5. Encode categorical questionnaire responses in both waves.
6. Remove W3 rows with impossible peer nomination values greater than the expected class seat range.
7. Final-align W2 and W3 again after wave-specific cleaning.
8. Clean peer nomination fields in both waves.
9. Produce final wide datasets, peer nomination edge lists, cleaning logs, and summary files.

## Step 1. Cross-Year Student ID Alignment

### Reason

The raw W2 and W3 datasets did not contain exactly the same students. Since the intended analysis compares W2 and W3, students needed to be matched by ID.

### Cleaning Rule

- Normalize student IDs.
- Use W2 `student_id` and W3 `TIGPS ID`.
- Keep only students whose ID appears in both waves.
- Remove rows that appear in only one wave.

### Result

| Wave | Rows before | Rows after ID alignment | Rows removed |
|---|---:|---:|---:|
| W2 | 8892 | 7236 | 1656 |
| W3 | 7714 | 7236 | 478 |

After this step, W2 and W3 both had `7236` rows.

## Step 2. Remove W2 Selected-Question Anomalies and Synchronize W3

### Reason

Some W2 rows contained clear invalid values in selected core questionnaire fields. These rows were not reliable for downstream analysis. Because W2 and W3 needed to stay synchronized at this stage, the same student IDs removed from W2 were also removed from W3.

### Cleaning Rule

- A set of selected W2 question groups was expanded into `143` columns.
- A W2 row was removed if any selected column had a numeric prefix less than `0`.
- Empty-only cases were checked, but no rows were removed for empty-only values in this step.
- The same removed W2 student IDs were removed from W3.

### Result

| Wave | Rows before | Rows removed | Rows after |
|---|---:|---:|---:|
| W2 | 7236 | 396 | 6840 |
| W3 | 7236 | 396 | 6840 |

All `396` removed cases were negative-value cases.

## W2-Specific Cleaning

## Step 3. Clean W2 Seat Number Conflicts

### Reason

W2 peer nomination fields use class seat numbers. Therefore, each student must have a reliable school, class, and seat number combination. If multiple students shared the same `(school_id, class, seat number)` but had different IDs or names, the nomination target could not be uniquely identified.

### Cleaning Rule

- Use `school_id`, `class`, and `v13`.
- Treat `v13` as the W2 seat number.
- Remove groups where the same `(school_id, class, v13)` was linked to different `student_id` and `name` values.

### Result

| Item | Count |
|---|---:|
| Conflict groups removed | 21 |
| Rows removed | 45 |
| Rows remaining | 6795 |

## Step 4. Remove W2 Invalid Seat Numbers

### Reason

W2 seat number `v13` is required for peer nomination analysis. Rows with impossible or invalid seat numbers cannot be used to identify self-nomination or same-class nomination targets.

### Cleaning Rule

Remove rows where `v13` was:

- negative,
- greater than `60`,
- non-numeric,
- empty.

### Result

| Item | Count |
|---|---:|
| Rows removed | 42 |
| Removal reason observed | Negative `v13` values |
| Rows remaining | 6753 |

## Step 5. Remove W2 Administrative Columns

### Reason

Some W2 columns were administrative or personally identifying fields that were not needed for downstream modeling.

### Cleaning Rule

Remove the following columns:

- `cell`
- `email`
- `q_name`
- `qb_code`
- `school_name`
- `status`
- `student_oid`

### Result

| Item | Count |
|---|---:|
| Rows before | 6753 |
| Rows after | 6753 |
| Columns removed | 7 |
| Columns remaining | 358 |

## Step 6. Standardize W2 Class Codes

### Reason

The W2 `class` field contained a mixture of numeric and non-numeric class labels. For peer nomination mapping and modeling, class needed to be represented consistently.

### Cleaning Rule

- Convert class labels into numeric class codes.
- Apply fixed mappings for named classes:
  - `忠 -> 801`
  - `孝 -> 802`
  - `仁 -> 803`
  - `義 -> 804`
  - `勤 -> 805`
  - `和 -> 806`
  - `Y27 -> 999`
- Validate that no unresolved class labels remained.
- Validate that class conversion did not create duplicate `(school_id, class, seat number)` conflicts.

### Result

| Check | Before | After |
|---|---:|---:|
| Rows | 6753 | 6753 |
| Non-numeric class rows | 2138 | 0 |
| Unresolved class rows | n/a | 0 |
| Duplicate seat-key conflict groups after mapping | n/a | 0 |

## Step 7. Encode W2 Questionnaire Responses

### Reason

Many W2 questionnaire responses were Chinese categorical labels. These needed to be converted into numeric codes for statistical modeling and machine learning.

### Cleaning Rule

- Apply a response-code mapping to W2 questionnaire columns.
- Convert categorical response labels into numeric values.
- Keep peer nomination columns as nomination seat numbers rather than recoding them as questionnaire responses.

### Result

| Item | Count |
|---|---:|
| Rows | 6753 |
| Columns | 358 |
| Questionnaire columns beginning with `v` | 351 |
| Mapped questionnaire columns | 331 |
| Unmapped peer nomination columns | 20 |
| Cells changed by response encoding | 2136585 |

The intentionally preserved W2 peer nomination columns were:

- `v14_1_01` to `v14_1_05`
- `v14_2_01` to `v14_2_05`
- `v14_3_01` to `v14_3_05`
- `v14_4_01` to `v14_4_05`

## W3-Specific Cleaning

## Step 8. Rename W3 Questionnaire Columns

### Reason

The W3 raw data used long Chinese question text as headers. For analysis, modeling, and comparison with W2, these headers needed to be renamed into stable question-code style names.

### Cleaning Rule

- Rename W3 columns using the official W3 question-code order.
- Keep row values unchanged.

### Result

| Check | Result |
|---|---:|
| Rows before | 6840 |
| Rows after | 6840 |
| Columns before | 382 |
| Columns after | 382 |

The W3 ID field was standardized to `student_id`.

## Step 9. Encode W3 Gender Fields

### Reason

W3 gender-related columns needed to use numeric codes consistent with the rest of the cleaned analysis dataset.

### Cleaning Rule

For W3 columns `1` and `2`:

- male = `1`
- female = `2`
- other = `0`
- missing = blank

### Result

| Item | Count |
|---|---:|
| Rows before | 6840 |
| Rows after | 6840 |

## Step 10. Encode W3 Questionnaire Responses

### Reason

Like W2, W3 contained categorical text responses that needed numeric coding for modeling.

### Cleaning Rule

Encode W3 columns according to response type:

- gender
- 3-point ordinal responses
- 4-point ordinal responses
- 5-point ordinal responses
- binary text responses
- nominal text responses
- high-cardinality text responses

Some fields were intentionally kept without encoding:

- peer nomination fields,
- already numeric fields,
- identifiers,
- free-text fields,
- user-requested skipped fields.

### Result

| Item | Count |
|---|---:|
| Rows before encoding | 6840 |
| Columns | 382 |
| Encoded columns | 329 |
| User-requested skipped columns | 27 |
| Kept non-encoded columns by plan | 25 |
| Unmapped non-empty cells after encoding | 0 |
| Cells changed by encoding | 1927513 |

## Step 11. Remove W3 Impossible Peer Nomination Values

### Reason

W3 peer nomination values should represent class seat numbers. Values greater than `60` were treated as impossible for the expected class size and were removed at the row level.

### Cleaning Rule

Check these W3 peer nomination columns:

- `8-1_0` to `8-1_4`
- `8-2_0` to `8-2_4`
- `8-3_0` to `8-3_4`
- `8-4_0` to `8-4_4`

Remove any row with at least one nomination value greater than `60`.

### Result

| Item | Count |
|---|---:|
| Rows before removal | 6840 |
| Rows removed | 154 |
| Rows remaining | 6686 |

## Final Cross-Wave Alignment

## Step 12. Align W2 and W3 to the Same Final Student IDs

### Reason

After the earlier shared cleaning stage, W2 and W3 each had additional wave-specific cleaning. This caused the final W2 and W3 student sets to differ. For paired analysis, the two datasets needed to contain the exact same students.

### Cleaning Rule

- Use the cleaned W2 dataset with `6753` rows.
- Use the cleaned W3 dataset with `6686` rows.
- Keep only student IDs appearing in both.
- Preserve W2 row order in both final outputs.

### Result

| Item | Count |
|---|---:|
| W2 rows before final alignment | 6753 |
| W3 rows before final alignment | 6686 |
| Common student IDs retained | 6603 |
| W2-only IDs removed | 150 |
| W3-only IDs removed | 83 |
| Final W2 rows | 6603 |
| Final W3 rows | 6603 |

## Peer Nomination Cleaning

## Step 13. Clean W2 Peer Nomination Fields

### Reason

The peer nomination fields are used to construct social network edges. They needed to be cleaned so self-loops and repeated nominations within the same question group do not distort network construction.

### W2 Nomination Fields

| Question group | Columns |
|---|---|
| Online like | `v14_1_01` to `v14_1_05` |
| Online dislike | `v14_2_01` to `v14_2_05` |
| Offline like | `v14_3_01` to `v14_3_05` |
| Offline dislike | `v14_4_01` to `v14_4_05` |

W2 class roster:

- school: `school_id`
- class: `class`
- self seat number: `v13`

### Cleaning Rule

- Blank, `0`, and negative nomination values were converted to blank.
- Self nominations were converted to blank.
- If the same student nominated the same seat more than once within the same question group, the first occurrence was kept and later duplicates were converted to blank.
- Numeric values were normalized to integer strings, for example `12.0` became `12`.
- Nominations to seats not present in the final aligned questionnaire roster were retained and marked in the edge list.
- No row was removed because of nomination cleaning.

### Result

| Item | Count |
|---|---:|
| Rows checked | 6603 |
| Class rosters used | 342 |
| Changed nomination cells | 48421 |
| Peer nomination edges after cleaning | 83639 |
| Duplicate roster seat groups | 0 |

W2 event counts:

| Event | Count |
|---|---:|
| Non-positive no-nomination codes converted to blank | 47819 |
| Nominations outside final aligned roster retained | 21867 |
| Self nominations converted to blank | 587 |
| Duplicate nominations converted to blank | 15 |

## Step 14. Clean W3 Peer Nomination Fields

### Reason

The W3 peer nomination fields needed the same cleaning logic as W2 so the two years can be compared consistently.

### W3 Nomination Fields

| Question group | Columns |
|---|---|
| Online like | `8-1_0` to `8-1_4` |
| Online dislike | `8-2_0` to `8-2_4` |
| Offline like | `8-3_0` to `8-3_4` |
| Offline dislike | `8-4_0` to `8-4_4` |

W3 class roster:

- W3 self seat number: column `7`
- W3 cleaned questionnaire file does not contain `school_id` or `class`
- Therefore, for the final aligned dataset, W3 uses the aligned W2 `school_id` and `class` as the class roster reference

### Cleaning Rule

- Blank, `0`, and negative nomination values were converted to blank.
- Self nominations were converted to blank.
- If the same student nominated the same seat more than once within the same question group, the first occurrence was kept and later duplicates were converted to blank.
- Numeric values were normalized to integer strings, for example `12.0` became `12`.
- Nominations to seats not present in the final aligned questionnaire roster were retained and marked in the edge list.
- No row was removed because of nomination cleaning.

### Result

| Item | Count |
|---|---:|
| Rows checked | 6603 |
| Class rosters used | 342 |
| Changed nomination cells | 90992 |
| Peer nomination edges after cleaning | 80408 |
| Duplicate roster seat groups | 58 |

W3 event counts:

| Event | Count |
|---|---:|
| Numeric values normalized to integer strings | 74157 |
| Non-positive no-nomination codes converted to blank | 10938 |
| Nominations outside final aligned roster retained without numeric normalization | 1256 |
| Duplicate nominations converted to blank | 4604 |
| Self nominations converted to blank | 1293 |

## Final Validation

After all cleaning steps:

| Check | Result |
|---|---|
| W2 final rows | 6603 |
| W3 final rows | 6603 |
| W2 and W3 student IDs | Identical |
| W2 and W3 row order | Identical |
| Blank student IDs | None |
| Duplicate student IDs | None |
| Remaining self nominations | None |
| Remaining duplicate nominations within each question group | None |
| Remaining `0` or negative nomination values | None |
| Remaining nomination values greater than `60` | None |

## Important Interpretation Notes

- The final W2 and W3 files are designed for paired cross-year analysis.
- Nominations to students outside the final aligned questionnaire sample were retained, not removed.
- These retained outside-roster nominations are marked in the edge lists because the nominee may have existed in the original classroom but did not appear in the final paired questionnaire sample.
- W3 class membership in the final aligned nomination cleaning uses W2 aligned `school_id` and `class` because the cleaned W3 questionnaire file does not carry these fields.
- Row removal in the final step was caused only by W2/W3 student ID alignment, not by peer nomination cleaning.
