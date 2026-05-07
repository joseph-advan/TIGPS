# Final Aligned Datasets and Peer Nomination QC

Generated: 2026-05-06

## Basis

- W2 source: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver5.csv`
- W3 source: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver4.csv`
- Final aligned rule: keep only `student_id` values present in both W2 ver5 and W3 ver4.
- Row order follows W2 ver5.

## Aligned Dataset Outputs

| Output | Rows | Notes |
|---|---:|---|
| `TIGPS_W2_studentdata_ver5_final_aligned_common_ids_with_W3_ver4.csv` | 6603 | W2 ver5 columns plus `_aligned_source`, `_aligned_basis` |
| `TIGPS_W3_student_studentdata_ver4_final_aligned_common_ids_with_W2_ver5.csv` | 6603 | W3 ver4 columns plus `_aligned_source`, `_aligned_basis` |
| `common_student_ids_w2ver5_w3ver4.csv` | 6603 | Common ID list |

ID counts:

| Item | Count |
|---|---:|
| W2 ver5 rows | 6753 |
| W3 ver4 rows | 6686 |
| Common IDs | 6603 |
| W2-only IDs | 150 |
| W3-only IDs | 83 |

## Peer Nomination QC Rules

- Valid same-class seat: positive numeric nomination must exist in the respondent's `school_id + class` roster.
- Self nomination: positive numeric nomination equals the respondent's own seat number.
- Duplicate nomination: the same positive seat is nominated more than once within the same question group.
- Blank, `0`, and negative values are treated as no-nomination codes, not QC issues.
- For aligned QC, `not_valid_same_class_seat` means the nominated seat is not present in the final 6603-student common-ID roster. It may still have existed in the original raw class before row filtering.

W2 roster source:

- `school_id`, `class`, `v13` from W2 ver5.

W3 roster source:

- `school_id`, `class`, `name` from `Data/otherData/W2W3_Student_Basic_Info.csv`.
- current seat from W3 ver4 column `7`.
- W3 basic-info missing rows: 103.

## QC Summary

### Aligned Common-ID QC

This is the primary QC for paired W2/W3 analysis because it uses only the final 6603 common IDs.

For W3 aligned QC:

- `school_id` and `class` come from the aligned W2 ver5 roster.
- current seat comes from W3 ver4 column `7`.

| Wave | Rows checked | Class rosters | Rows with issue | Issue cells/events | Duplicate roster seat groups |
|---|---:|---:|---:|---:|---:|
| W2 ver5 aligned common IDs | 6603 | 342 | 5150 | 22471 | 0 |
| W3 ver4 aligned common IDs | 6603 | 342 | 5193 | 24625 | 58 |

W2 aligned issue type counts:

```json
{
  "not_valid_same_class_seat": 21874,
  "self_nomination": 587,
  "duplicate_nomination_within_group": 10
}
```

W3 aligned issue type counts:

```json
{
  "not_valid_same_class_seat": 21627,
  "duplicate_nomination_within_group": 1705,
  "self_nomination": 1293
}
```

Aligned QC output files:

- `aligned_peer_nomination_qc_summary.json`
- `W2_ver5_aligned_peer_nomination_issues.csv`
- `W2_ver5_aligned_peer_nomination_issue_rows_summary.csv`
- `W2_ver5_aligned_peer_nomination_issue_group_summary.csv`
- `W2_ver5_aligned_peer_nomination_column_status_summary.csv`
- `W2_ver5_aligned_roster_duplicate_seats.csv`
- `W3_ver4_aligned_peer_nomination_issues.csv`
- `W3_ver4_aligned_peer_nomination_issue_rows_summary.csv`
- `W3_ver4_aligned_peer_nomination_issue_group_summary.csv`
- `W3_ver4_aligned_peer_nomination_column_status_summary.csv`
- `W3_ver4_aligned_roster_duplicate_seats.csv`

### Full Latest-File QC

This is a secondary diagnostic over all rows in W2 ver5 and W3 ver4 before final common-ID alignment.

| Wave | Rows checked | Class rosters | Rows with issue | Issue cells/events | Duplicate roster seat groups |
|---|---:|---:|---:|---:|---:|
| W2 ver5 | 6753 | 342 | 5161 | 21888 | 0 |
| W3 ver4 | 6686 | 342 | 5274 | 25871 | 57 |

W2 issue type counts:

```json
{
  "not_valid_same_class_seat": 21255,
  "self_nomination": 623,
  "duplicate_nomination_within_group": 10
}
```

W3 issue type counts:

```json
{
  "not_valid_same_class_seat": 22732,
  "duplicate_nomination_within_group": 1763,
  "self_nomination": 1376
}
```

## QC Output Files

- `W2_ver5_peer_nomination_issues.csv`
- `W2_ver5_peer_nomination_issue_rows_summary.csv`
- `W2_ver5_peer_nomination_issue_group_summary.csv`
- `W2_ver5_peer_nomination_column_status_summary.csv`
- `W2_ver5_roster_duplicate_seats.csv`
- `W3_ver4_peer_nomination_issues.csv`
- `W3_ver4_peer_nomination_issue_rows_summary.csv`
- `W3_ver4_peer_nomination_issue_group_summary.csv`
- `W3_ver4_peer_nomination_column_status_summary.csv`
- `W3_ver4_roster_duplicate_seats.csv`
- `W3_ver4_roster_for_peer_nomination_qc_from_basic_info.csv`
- `final_aligned_and_peer_nomination_qc_summary.json`
