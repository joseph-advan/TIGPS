# Revised Final Aligned Datasets and Peer Nomination QC

Generated: 2026-05-06

## Basis

- W2 source: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver5.csv`
- W3 source: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver4.csv`
- Aligned rule: keep only the 6603 `student_id`s present in both W2 ver5 and W3 ver4.
- W2 rows and W3 rows are ordered by W2 ver5 `student_id` order.

## Revised Rules

- `duplicate_nomination_within_group` is not an issue and is retained.
- `self_nomination` is not an issue and is converted to blank in the revised aligned output files.
- If the nominee did not fill the questionnaire or is not in the final aligned questionnaire roster, this is not an issue. It is recorded only as `nominee_not_in_final_questionnaire_roster_no_issue`.
- Blank, `0`, and negative values are treated as no nomination.
- In this revised QC, only non-numeric nomination values and nomination values `>60` are counted as issues.

## Nomination Columns Used

W2:

- `v14_1_01` to `v14_1_05`: online like
- `v14_2_01` to `v14_2_05`: online dislike
- `v14_3_01` to `v14_3_05`: offline like
- `v14_4_01` to `v14_4_05`: offline dislike
- self seat: `v13`
- class key: `school_id` + `class`

W3:

- `8-1_0` to `8-1_4`: online like
- `8-2_0` to `8-2_4`: online dislike
- `8-3_0` to `8-3_4`: offline like
- `8-4_0` to `8-4_4`: offline dislike
- self seat: W3 column `7`
- class key for aligned QC: `school_id` + `class` from W2 ver5 aligned roster

## Revised Aligned Outputs

| Output | Rows | Notes |
|---|---:|---|
| `TIGPS_W2_studentdata_ver5_final_aligned_common_ids_with_W3_ver4_self_nomination_blank.csv` | 6603 | W2 ver5 aligned, self nominations blanked |
| `TIGPS_W3_student_studentdata_ver4_final_aligned_common_ids_with_W2_ver5_self_nomination_blank.csv` | 6603 | W3 ver4 aligned, self nominations blanked |
| `common_student_ids_w2ver5_w3ver4.csv` | 6603 | Common ID list |

## Revised QC Result

| Wave | Rows checked | Rows with issue | Issue events |
|---|---:|---:|---:|
| W2 ver5 aligned revised | 6603 | 0 | 0 |
| W3 ver4 aligned revised | 6603 | 0 | 0 |

W2 recorded event counts:

```json
{
  "valid_nomination": 61780,
  "non_positive_no_nomination_code": 47819,
  "nominee_not_in_final_questionnaire_roster_no_issue": 21874,
  "self_nomination_blanked_no_issue": 587,
  "duplicate_nomination_within_group_no_issue": 10
}
```

W3 recorded event counts:

```json
{
  "valid_nomination": 63385,
  "nominee_not_in_final_questionnaire_roster_no_issue": 21627,
  "blank_no_nomination": 34817,
  "non_positive_no_nomination_code": 10938,
  "duplicate_nomination_within_group_no_issue": 1705,
  "self_nomination_blanked_no_issue": 1293
}
```

## Files

- `revised_peer_nomination_qc_summary.json`
- `W2_ver5_aligned_revised_peer_nomination_events.csv`
- `W2_ver5_aligned_revised_peer_nomination_issue_rows.csv`
- `W2_ver5_aligned_revised_peer_nomination_event_rows_summary.csv`
- `W2_ver5_aligned_revised_peer_nomination_group_summary.csv`
- `W2_ver5_aligned_revised_peer_nomination_column_summary.csv`
- `W3_ver4_aligned_revised_peer_nomination_events.csv`
- `W3_ver4_aligned_revised_peer_nomination_issue_rows.csv`
- `W3_ver4_aligned_revised_peer_nomination_event_rows_summary.csv`
- `W3_ver4_aligned_revised_peer_nomination_group_summary.csv`
- `W3_ver4_aligned_revised_peer_nomination_column_summary.csv`
