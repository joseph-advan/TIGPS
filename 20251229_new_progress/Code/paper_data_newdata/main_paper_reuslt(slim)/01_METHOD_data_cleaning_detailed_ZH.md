# Data Cleaning Methods Detailed Record

## 0. Purpose of This Document

This document summarizes the data-cleaning process used to produce the final W2 and W3 analysis datasets for the main paper. It focuses only on data cleaning, ID alignment, questionnaire response cleaning, gender harmonization, and peer nomination cleaning. Feature decomposition is intentionally not included here and should be documented separately.

Final analysis datasets:

| Wave | Final cleaned dataset | Final rows | Role |
|---|---|---:|---|
| W2 / 2024 | `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv` | 6603 | W2 cleaned questionnaire and peer nomination data |
| W3 / 2025 | `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv` | 6603 | W3 cleaned questionnaire and peer nomination data |

The final W2 and W3 datasets contain the same 6603 student IDs and are ordered consistently for paired cross-wave analyses.

## 1. Raw Data Starting Point

The cleaning process started from the original W2 and W3 student questionnaire datasets. The two waves used different ID column names and had different row counts.

| Wave | Raw rows | Raw ID field | Initial issue |
|---|---:|---|---|
| W2 | 8892 | `student_id` | Student IDs were already available in a stable field. |
| W3 | 7714 | `TIGPS ID` | One row had a blank ID before cleaning. |

Because the project compares W2 and W3 students over time, the cleaning process was designed to create a paired analytic sample where each retained student appears in both waves.

## 2. Cross-Year Student ID Alignment

### What Was Done

Student IDs were normalized across W2 and W3. W2 used `student_id`; W3 used `TIGPS ID`, which was standardized to `student_id`. Only students appearing in both waves were retained in the first alignment step.

### Why This Was Done

The main analyses include both cross-sectional W2 analyses and longitudinal W2-to-W3 analyses. A common paired student sample avoids changing sample composition across models and ensures that W2 predictors can be matched to W3 outcomes.

### Result

| Wave | Rows before alignment | Rows after alignment | Rows removed |
|---|---:|---:|---:|
| W2 | 8892 | 7236 | 1656 |
| W3 | 7714 | 7236 | 478 |

After this initial alignment, both W2 and W3 had 7236 matched student rows.

## 3. Shared Removal of W2 Selected-Question Anomalies

### What Was Done

A set of selected W2 core questionnaire groups was expanded into 143 columns. W2 rows were removed if any selected column had a numeric prefix smaller than 0. The same student IDs removed from W2 were also removed from W3.

### Why This Was Done

Rows with negative values in selected core W2 questionnaire fields were treated as unreliable or invalid for downstream analysis. Because W2 and W3 needed to remain synchronized at this stage, the same students were removed from both waves.

### Result

| Wave | Rows before | Rows removed | Rows after |
|---|---:|---:|---:|
| W2 | 7236 | 396 | 6840 |
| W3 | 7236 | 396 | 6840 |

All 396 removed cases were negative-value cases in the selected W2 question fields.

## 4. W2-Specific Cleaning

## 4.1 W2 Seat Number Conflict Cleaning

### What Was Done

W2 peer nominations are based on class seat numbers. Therefore, W2 was checked for duplicate or conflicting seat keys using:

- `school_id`
- `class`
- `v13`

Here, `v13` was treated as the student's own W2 seat number.

Rows were removed when the same `(school_id, class, v13)` combination was linked to different `student_id` and `name` values.

### Why This Was Done

If the same school, class, and seat number identifies multiple different students, a peer nomination to that seat cannot be uniquely mapped to a student. These rows would create ambiguity in peer nomination cleaning and network construction.

### Result

| Item | Count |
|---|---:|
| Conflict groups removed | 21 |
| Rows removed | 45 |
| Rows remaining | 6795 |

Important interpretation: these conflict groups were removed rather than keeping one arbitrary student, because the seat mapping itself was ambiguous.

## 4.2 W2 Invalid Seat Number Removal

### What Was Done

Rows were removed when W2 seat number `v13` was invalid. Invalid values included:

- negative values,
- values greater than 60,
- non-numeric values,
- empty values.

### Why This Was Done

W2 `v13` is required to identify self-nominations and same-class nomination targets. Invalid seat numbers prevent reliable network edge construction.

### Result

| Item | Count |
|---|---:|
| Rows removed | 42 |
| Observed removal reason | Negative `v13` values |
| Rows remaining | 6753 |

## 4.3 W2 Administrative Column Removal

### What Was Done

The following administrative or personally identifying columns were removed:

- `cell`
- `email`
- `q_name`
- `qb_code`
- `school_name`
- `status`
- `student_oid`

### Why This Was Done

These fields were not used in modeling and were removed to reduce unnecessary personal or administrative information in the cleaned analysis dataset.

### Result

| Item | Count |
|---|---:|
| Rows before | 6753 |
| Rows after | 6753 |
| Columns removed | 7 |
| Columns remaining | 358 |

## 4.4 W2 Class Code Standardization

### What Was Done

The W2 `class` field contained both numeric and non-numeric class labels. Non-numeric labels were converted into numeric class codes using fixed mappings:

| Original label | Standardized class code |
|---|---:|
| `忠` | 801 |
| `孝` | 802 |
| `仁` | 803 |
| `義` | 804 |
| `勤` | 805 |
| `和` | 806 |
| `Y27` | 999 |

After mapping, the dataset was checked to ensure that no unresolved class labels remained and that the mapping did not create duplicate seat-key conflicts.

### Why This Was Done

Class codes are required for peer nomination cleaning because nomination targets are interpreted within a school-class roster. Standardizing class codes ensures consistent roster construction.

### Result

| Check | Before | After |
|---|---:|---:|
| Rows | 6753 | 6753 |
| Non-numeric class rows | 2138 | 0 |
| Unresolved class rows | n/a | 0 |
| Duplicate seat-key conflict groups after mapping | n/a | 0 |

## 4.5 W2 Questionnaire Response Encoding

### What Was Done

W2 questionnaire responses were converted from Chinese categorical labels into numeric codes where appropriate. Peer nomination columns were intentionally excluded from response recoding because they represent nominated seat numbers rather than ordinal questionnaire responses.

Peer nomination columns preserved as seat-number fields:

- `v14_1_01` to `v14_1_05`
- `v14_2_01` to `v14_2_05`
- `v14_3_01` to `v14_3_05`
- `v14_4_01` to `v14_4_05`

### Why This Was Done

Statistical modeling and machine learning require numeric feature values. However, nomination fields must remain as seat numbers so they can later be converted into network edges.

### Result

| Item | Count |
|---|---:|
| Rows | 6753 |
| Columns | 358 |
| Questionnaire columns beginning with `v` | 351 |
| Mapped questionnaire columns | 331 |
| Unmapped peer nomination columns | 20 |
| Cells changed by response encoding | 2136585 |

## 5. W3-Specific Cleaning

## 5.1 W3 Questionnaire Column Renaming

### What Was Done

W3 raw column names were renamed from long Chinese question text into stable question-code style names. The W3 ID column was standardized to `student_id`.

### Why This Was Done

Stable coded column names are required for matching W2 and W3 questions, building features, and writing reproducible scripts.

### Result

| Check | Result |
|---|---:|
| Rows before | 6840 |
| Rows after | 6840 |
| Columns before | 382 |
| Columns after | 382 |

## 5.2 W3 Gender Field Encoding and Later Harmonization

### What Was Done Initially

In the W3 questionnaire response encoding stage, W3 gender-related columns `1` and `2` were encoded numerically as:

- male = `1`
- female = `2`
- other = `0`
- missing = blank

### Later Harmonization

A later audit found that W2 used a different biological sex convention. To make W3 consistent with W2, W3 biological sex column `1` was recoded:

- `1 -> 2`
- `2 -> 1`

Final harmonized convention used in the cleaned W2 and W3 analysis files:

- `1 = Female`
- `2 = Male`

### Why This Was Done

Gender must use the same coding convention across waves before it can be used as a covariate, table variable, or model feature. Without harmonization, gender effects would be misinterpreted across years.

### Output Record

Detailed record:

- `Data/testing_clean/W3/w3_ver5_gender_recode_to_w2_convention.md`
- `Data/testing_clean/W3/w3_ver5_gender_recode_to_w2_convention_counts.xlsx`

## 5.3 W3 Questionnaire Response Encoding

### What Was Done

W3 categorical text responses were encoded into numeric values according to response type, including:

- gender fields,
- 3-point ordinal responses,
- 4-point ordinal responses,
- 5-point ordinal responses,
- binary text responses,
- nominal text responses,
- high-cardinality text responses.

Some fields were intentionally left unencoded:

- peer nomination fields,
- already numeric fields,
- identifiers,
- free-text fields,
- user-requested skipped fields.

### Why This Was Done

Like W2, W3 questionnaire responses needed to be numeric for modeling, but nomination and free-text fields required separate handling.

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

## 5.4 W3 Impossible Peer Nomination Value Removal

### What Was Done

W3 peer nomination fields were checked for values greater than 60. Rows with at least one peer nomination value greater than 60 were removed.

Checked W3 nomination columns:

- `8-1_0` to `8-1_4`
- `8-2_0` to `8-2_4`
- `8-3_0` to `8-3_4`
- `8-4_0` to `8-4_4`

### Why This Was Done

Peer nomination values should represent classroom seat numbers. Values greater than 60 were considered impossible under the expected class-seat range and would create invalid nomination targets.

### Result

| Item | Count |
|---|---:|
| Rows before removal | 6840 |
| Rows removed | 154 |
| Rows remaining | 6686 |

## 6. Final Cross-Wave Alignment

### What Was Done

After W2-specific and W3-specific cleaning, the two waves were aligned again by `student_id`. Only students appearing in both cleaned wave-specific files were retained. W2 row order was used as the final row order.

### Why This Was Done

Wave-specific cleaning changed the row counts separately. A final alignment was needed so that all main analyses use the same paired W2/W3 student sample.

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

Final aligned ID list:

- `Data/testing_clean/w2_ver6_w3_ver5_common_student_ids.csv`

## 7. Peer Nomination Cleaning

## 7.1 General Peer Nomination Cleaning Rules

The same conceptual rules were applied to W2 and W3 nomination fields:

1. Blank, `0`, and negative nomination values were treated as no nomination and written as blank.
2. Self nominations were written as blank.
3. Repeated nominations within the same nomination group kept the first occurrence and blanked later duplicates.
4. Positive numeric values were normalized to integer strings, such as `12.0 -> 12`.
5. Nominees not in the final aligned questionnaire roster were retained and marked in edge lists.
6. No student rows were removed because of nomination cleaning.

### Why This Was Done

These rules prevent self-loops, duplicate nominations, and invalid non-positive nominations from distorting network measures while preserving nominations to classmates who may not be in the final paired questionnaire sample.

## 7.2 W2 Peer Nomination Cleaning

### Nomination Fields

| Question group | Columns |
|---|---|
| Online like | `v14_1_01` to `v14_1_05` |
| Online dislike | `v14_2_01` to `v14_2_05` |
| Offline like | `v14_3_01` to `v14_3_05` |
| Offline dislike | `v14_4_01` to `v14_4_05` |

### Roster Used

W2 class roster used:

- `school_id`
- `class`
- self seat number `v13`

### Result

| Item | Count |
|---|---:|
| Rows in output | 6603 |
| Changed nomination cells | 48421 |
| Event log rows | 70288 |
| Edge rows after cleaning | 83639 |
| Class rosters used | 342 |
| Duplicate roster seat groups | 0 |

W2 event status counts:

| Status/action | Count |
|---|---:|
| Non-positive no-nomination code | 47819 |
| Nominee not in final aligned roster retained | 21867 |
| Self nomination blanked | 587 |
| Duplicate nomination blanked | 15 |

W2 output artifacts:

- `Data/testing_clean/W2/w2_ver6_nomination_cleaning_event_log.csv`
- `Data/testing_clean/W2/w2_ver6_peer_nomination_edges.csv`
- `Data/testing_clean/W2/w2_ver6_nomination_cleaning_group_summary.csv`
- `Data/testing_clean/W2/w2_ver6_nomination_cleaning_column_summary.csv`
- `Data/testing_clean/W2/w2_ver6_aligned_roster_duplicate_seats.csv`

## 7.3 W3 Peer Nomination Cleaning

### Nomination Fields

| Question group | Columns |
|---|---|
| Online like | `8-1_0` to `8-1_4` |
| Online dislike | `8-2_0` to `8-2_4` |
| Offline like | `8-3_0` to `8-3_4` |
| Offline dislike | `8-4_0` to `8-4_4` |

### Roster Used

The cleaned W3 questionnaire file did not contain `school_id` and `class`. Therefore, W3 nomination cleaning used:

- aligned W2 `school_id`,
- aligned W2 `class`,
- W3 self seat number column `7`.

### Why This Was Done

W3 nominations still refer to classmates by seat number. Since W3 lacked school/class roster fields, the aligned W2 school/class structure was used to define the classroom roster for final aligned W3 nomination cleaning.

### Result

| Item | Count |
|---|---:|
| Rows in output | 6603 |
| Changed nomination cells | 90992 |
| Event log rows | 92248 |
| Edge rows after cleaning | 80408 |
| Class rosters used | 342 |
| Duplicate roster seat groups | 58 |

W3 event status counts:

| Status/action | Count |
|---|---:|
| Valid nomination | 55287 |
| Nominee not in final aligned roster retained | 20126 |
| Non-positive no-nomination code | 10938 |
| Duplicate nomination blanked | 4604 |
| Self nomination blanked | 1293 |

W3 output artifacts:

- `Data/testing_clean/W3/w3_ver5_nomination_cleaning_event_log.csv`
- `Data/testing_clean/W3/w3_ver5_peer_nomination_edges.csv`
- `Data/testing_clean/W3/w3_ver5_nomination_cleaning_group_summary.csv`
- `Data/testing_clean/W3/w3_ver5_nomination_cleaning_column_summary.csv`
- `Data/testing_clean/W3/w3_ver5_aligned_roster_duplicate_seats.csv`

## 8. Final Validation Checks

After all data-cleaning steps, the final datasets passed the following checks:

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
| Remaining nomination values greater than 60 | None |

## 9. Interpretation Notes for the Paper

Several interpretation choices should be stated clearly in the Methods section:

1. The final analytic sample is a paired W2/W3 sample, not the full original W2 or W3 sample.
2. Peer nomination cleaning did not remove student rows.
3. Self nominations and repeated nominations were treated as invalid nomination cells and blanked.
4. Nominations to classmates outside the final questionnaire roster were retained in edge lists because those classmates may have been present in the classroom but absent from the final paired survey sample.
5. W3 gender was harmonized to the W2 coding convention before final analysis.
6. W3 class roster information was borrowed from aligned W2 school/class fields because W3 did not contain those fields in the cleaned file.

## 10. Short Paper-Ready Methods Paragraph

The student questionnaire datasets from W2 and W3 were cleaned separately and then aligned by student ID. Student IDs were normalized across waves, and the analytic sample was restricted to students present in both W2 and W3. W2-specific cleaning addressed ambiguous school-class-seat combinations, invalid seat numbers, administrative columns, class-code standardization, and categorical response encoding. W3-specific cleaning included question-code renaming, categorical response encoding, removal of impossible peer nomination values, and harmonization of gender coding to the W2 convention. After wave-specific cleaning, the two datasets were aligned again, yielding a final paired sample of 6,603 students in each wave.

Peer nomination fields were cleaned after final alignment. Non-positive nomination values were treated as no nomination, self-nominations were set to missing, and repeated nominations within the same nomination block retained only the first occurrence. Positive numeric nomination values were standardized to integer strings. Nominations to classmates outside the final aligned questionnaire roster were retained and flagged in edge lists rather than removed. No student rows were removed during peer nomination cleaning.
