# W2 ver5 to ver6 Nomination Cleaning Summary

Generated: 2026-05-06

## Source and Output

- Source: `TIGPS_W2_studentdata_ver5.csv`
- Output: `TIGPS_W2_studentdata_ver6.csv`
- Basis: final alignment uses the intersection of W2 ver5 and W3 ver4 student IDs.
- Rows after alignment: `6603`

## Cleaning Rules

- Blank, `0`, and negative nomination values are treated as no nomination and written as blank.
- Self nominations are written as blank.
- Repeated nominations within the same nomination group keep the first occurrence and blank later duplicates.
- Numeric nomination values are normalized to integer strings, for example `12.0` becomes `12`.
- Nominees not in the final aligned questionnaire roster are retained and marked in the edge list.
- No row is removed because of nomination cleaning.

W2 class roster uses `school_id`, `class`, and self seat `v13` from W2 ver5 after final ID alignment.

## Summary

| Item | Count |
|---|---:|
| Rows in output | 6603 |
| Changed nomination cells | 48421 |
| Event log rows | 70288 |
| Edge rows after cleaning | 83639 |
| Class rosters used | 342 |
| Duplicate roster seat groups | 0 |

## Event Status Counts

| Status/action | Count |
|---|---:|
| `non_positive_no_nomination_code` | 47819 |
| `nominee_not_in_final_aligned_roster_retained` | 21867 |
| `self_nomination_blanked` | 587 |
| `duplicate_nomination_blanked` | 15 |

## Artifacts

- `w2_ver6_nomination_cleaning_event_log.csv`
- `w2_ver6_peer_nomination_edges.csv`
- `w2_ver6_nomination_cleaning_group_summary.csv`
- `w2_ver6_nomination_cleaning_column_summary.csv`
- `w2_ver6_aligned_roster_duplicate_seats.csv`
