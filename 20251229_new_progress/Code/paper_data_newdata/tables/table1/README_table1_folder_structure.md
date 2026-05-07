# Table 1 Folder Structure

This folder contains the files needed to generate and review Table 1 for W2 2024 and W3 2025.

## `scripts/`

- `build_table1_online_activity.py`: Rebuilds Table 1 outputs from the cleaned W2/W3 datasets.

## `config/`

- `table1_variable_plan_draft.csv`: Machine-readable variable plan.
- `table1_variable_plan_draft.md`: Human-readable variable plan.
- `table1_scoring_config.json`: Machine-readable scoring rules, labels, and reverse coding.
- `table1_scoring_decisions.md`: Human-readable scoring decisions.

## `outputs/`

- `table1_w2_2024.csv`
- `table1_w2_2024.md`
- `table1_w3_2025.csv`
- `table1_w3_2025.md`

## `diagnostics/`

- `table1_generation_notes.md`: Generation rules and output notes.
- `table1_online_activity_group_diagnostics.csv`: High/Low Online Activity grouping diagnostics.
- `table1_precheck_online_activity_and_reverse_items.md`: Earlier precheck for online activity items and reverse-coded parenting items.

## Removed Files

The old `table1_feature_missingness_precheck*` files were removed from this folder because missingness checks are now maintained separately in:

`Code/paper_data_newdata/feature_missingness_check/`

Python `__pycache__` files were also removed.
