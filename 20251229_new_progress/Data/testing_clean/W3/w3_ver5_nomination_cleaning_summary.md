# W3 ver4 to ver5 Nomination Cleaning Summary

Generated: 2026-05-06

## Source and Output

- Source: `TIGPS_W3_student_studentdata_ver4.csv`
- Output: `TIGPS_W3_student_studentdata_ver5.csv`
- Basis: final alignment uses the intersection of W2 ver5 and W3 ver4 student IDs.
- Rows after alignment: `6603`

## Cleaning Rules

- Blank, `0`, and negative nomination values are treated as no nomination and written as blank.
- Self nominations are written as blank.
- Repeated nominations within the same nomination group keep the first occurrence and blank later duplicates.
- Numeric nomination values are normalized to integer strings, for example `12.0` becomes `12`.
- Nominees not in the final aligned questionnaire roster are retained and marked in the edge list.
- No row is removed because of nomination cleaning.

W3 ver4 does not include `school_id` and `class`, so W3 class roster uses the aligned W2 ver5 `school_id` and `class`; W3 self seat uses column `7`.

## Summary

| Item | Count |
|---|---:|
| Rows in output | 6603 |
| Changed nomination cells | 90992 |
| Event log rows | 92248 |
| Edge rows after cleaning | 80408 |
| Class rosters used | 342 |
| Duplicate roster seat groups | 58 |

## Event Status Counts

| Status/action | Count |
|---|---:|
| `valid_nomination` | 55287 |
| `nominee_not_in_final_aligned_roster_retained` | 20126 |
| `non_positive_no_nomination_code` | 10938 |
| `duplicate_nomination_blanked` | 4604 |
| `self_nomination_blanked` | 1293 |

## Artifacts

- `w3_ver5_nomination_cleaning_event_log.csv`
- `w3_ver5_peer_nomination_edges.csv`
- `w3_ver5_nomination_cleaning_group_summary.csv`
- `w3_ver5_nomination_cleaning_column_summary.csv`
- `w3_ver5_aligned_roster_duplicate_seats.csv`
