# 02_descriptive_table1_group_differences

## Purpose

This folder builds the prediction-aligned Table 1 descriptive group-difference results.

The main design is:

- `W2 -> W2`: W2 baseline features grouped by W2 high vs low psychological distress.
- `W2 -> W3`: W2 baseline features grouped by W3 high vs low psychological distress.

W3 features grouped by W3 distress are intentionally excluded from this main paper-results folder because they do not match the baseline-prediction logic.

## Network Specifications

Each prediction task is produced in two versions:

- Observed network: raw interpersonal nomination counts, ratios, and valence features.
- Class-adjusted network: count-like interpersonal features divided by same-class respondents minus one.

This lets the paper compare whether the interpersonal conclusions depend on class-size adjustment.

## How To Rerun

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\run_descriptive_table1_group_differences.py"
```

The runner rebuilds this folder's `outputs` directory from the current cleaned W2/W3 student datasets, current drop + decomposition feature definitions, and current interpersonal feature files.

## Output Structure

- `outputs/01_w2_features_to_w2_distress`: W2 baseline features by W2 distress, observed and class-adjusted network versions.
- `outputs/02_w2_features_to_w3_distress`: W2 baseline features by W3 distress, observed and class-adjusted network versions.
- `outputs/table1_prediction_aligned_group_differences.xlsx`: combined workbook for manuscript review.
- `outputs/TABLE1_PREDICTION_ALIGNED_GROUP_DIFFERENCES_SUMMARY.md`: concise interpretation summary.
- `outputs/diagnostics`: generation diagnostics.

## Interpretation Rule

Table 1 is descriptive, not causal.

- `p-value` tests whether each feature differs between high- and low-distress groups.
- `Between-group difference` is Cramer's V for categorical rows and Cohen's d for continuous/scale rows.
- The W2 -> W3 table is the key descriptive bridge into longitudinal feature importance and interaction analyses.
