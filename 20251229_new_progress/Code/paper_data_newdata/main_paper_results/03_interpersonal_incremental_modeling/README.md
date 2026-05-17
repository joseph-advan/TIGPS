# 03 Interpersonal Incremental Modeling

## Purpose

This folder tests whether adding the 12 interpersonal network indicators improves prediction beyond the current drop + decomposition individual-level feature set.

This is the bridge between Table 1 and the later feature-importance analysis:

1. Table 1 describes whether high- and low-distress students differ on interpersonal indicators.
2. This folder tests whether those indicators add incremental predictive value in models.
3. The next folder, `04_feature_importance_top20`, should then examine whether interpersonal indicators appear among the strongest LASSO predictors.

## Analysis Design

### Tasks

- `W2 -> W2`: W2 predictors classify W2 high psychological distress.
- `W2 -> W3`: W2 predictors classify W3 high psychological distress.

### Feature Sets

- `decomposed_features_only`: current drop + decomposition individual-level features.
- `decomposed_plus_12_interpersonal`: decomposed features plus 12 respondent-class-normalized interpersonal indicators.

### Models

- Plain multivariable Logistic regression.
- LASSO Logistic regression.
- Ridge Logistic regression.

## Interpersonal Features

The added interpersonal block uses the class-adjusted version aligned with the revised Table 1 design:

- Online total nominations.
- Offline total nominations.
- Outgoing friendship nominations.
- Incoming friendship nominations.
- Outgoing negative nominations.
- Incoming negative nominations.
- Reciprocal friendship ties.
- Reciprocal negative ties.
- Sent positive tie ratio.
- Received positive tie ratio.
- Sent network valence.
- Received network valence.

Count and valence indicators are respondent-class-normalized. Positive tie ratios are already ratios and are not divided again.

## Output Files

- `outputs/interpersonal_incremental_model_performance.xlsx`
  - Model performance for all tasks, feature sets, and models.
  - Performance deltas comparing plus-interpersonal against baseline.
  - Selection-count summary.
  - Diagnostics.

- `outputs/interpersonal_feature_selection_summary.xlsx`
  - Interpersonal feature coefficients and ranks.
  - Long-format coefficients for all features.
  - Interpersonal selection counts.

- `outputs/INTERPERSONAL_INCREMENTAL_MODELING_SUMMARY.md`
  - Human-readable summary of methods, deltas, and interpretation.

- `outputs/interpersonal_incremental_modeling_diagnostics.json`
  - Machine-readable diagnostics and feature definitions.

## Current Result Summary

Adding the 12 interpersonal features produced only very small performance changes.

For `W2 -> W2`, CV AUC changed by approximately 0.000 to 0.001 across Logistic, LASSO, and Ridge. CV F1 changed by approximately 0.001 to 0.002.

For `W2 -> W3`, CV AUC decreased slightly by approximately -0.002 to -0.003 for Logistic/Ridge/LASSO, while CV F1 was unchanged or slightly lower/unchanged depending on the model.

The interpersonal block therefore appears to have limited incremental predictive value beyond the decomposed individual-level features. This supports moving next to `04_feature_importance_top20` to test whether interpersonal indicators appear among the LASSO Top 20 and to identify the dominant predictor categories.

## Re-run Command

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\03_interpersonal_incremental_modeling\run_interpersonal_incremental_modeling.py"
```
