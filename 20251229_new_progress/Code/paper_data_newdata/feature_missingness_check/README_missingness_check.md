# Missingness Check for All Formal Question Groups

This folder checks missingness for every formal paper-use question group, separately for W2 2024 and W3 2025.

## Input Data

- W2: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv`
- W3: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv`
- Formal variable list: the paper-use formal question-group CSV in `Data/otherData`.

## Definitions

- `n_all_items_valid`: number of students with all items valid for that question group.
- `n_at_least_50pct_valid`: number of students with at least half of the items valid.
- `n_below_50pct_but_some_valid`: number of students with at least one valid item but fewer than 50% valid items.
- `n_zero_valid_items`: number of students with no valid item in that question group.
- `n_any_missing_item`: number of students missing at least one item in that question group.

## Output Files

- `all_formal_question_groups_missingness_summary.csv`: question-group-level missingness summary.
- `all_formal_question_groups_item_missingness.csv`: item-level missingness counts.
- `all_formal_question_groups_missingness_issues.csv`: only question groups with any missingness issue.
- `all_formal_question_groups_missingness_flag_counts.csv`: count of question groups by missingness flag.

## Missingness Flag Counts

| dataset | missingness_flag | n_question_groups |
|---|---|---:|
| W2 2024 | COMPLETE | 25 |
| W3 2025 | COMPLETE | 24 |
| W3 2025 | HAS_ROWS_BELOW_50PCT | 1 |

## Question Groups With Missingness Issues

| dataset | variable_name | group_id | n_items_defined_existing | n_all_items_valid | n_at_least_50pct_valid | n_below_50pct_but_some_valid | n_zero_valid_items | n_any_missing_item | max_item_missing_n | missingness_flag |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| W3 2025 | Social Media Use: Selective Sharing and Impression Management | 25 | 10 | 6336 | 6336 | 267 | 0 | 267 | 267 | HAS_ROWS_BELOW_50PCT |

## Interpretation

- If a group is `COMPLETE`, applying a 50% valid-item rule will not change its score.
- If a group is `HAS_ROWS_BELOW_50PCT`, those rows would become missing under a 50% valid-item rule, but would be scored under a one-valid-item rule.
- If a group is `HAS_PARTIAL_MISSING_BUT_AT_LEAST_50PCT`, a 50% rule still keeps all rows, but some scores are based on partial items.

## Main Finding

Across the 25 formal question groups, W2 has no missingness issue. W3 has one issue: Social Media Use: Selective Sharing and Impression Management. In W3, 267 students answered only item `25-0` and were missing `25-1` to `25-9`, so they are below the 50% valid-item threshold for that question group.
