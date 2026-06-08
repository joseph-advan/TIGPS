# 06 Teacher Formula Interaction Models

## Purpose

This folder estimates two interaction-model variants requested by the advisor.

Variant 1: single-feature plus gender interaction model:

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature
+ b2 * ModeratorHigh
+ b3 * Feature * ModeratorHigh
+ gender_male
```

Variant 2: Top20-adjusted interaction model:

```text
logit(P(High Psychological Distress = 1))
= task-specific LASSO Top20 main effects
+ b2 * ModeratorHigh
+ b3 * Feature * ModeratorHigh
```

Because the outcome is binary high psychological distress, the coefficients are logistic-regression log-odds coefficients.
Both variants use the task-specific LASSO Top20 features as focal interaction candidates. One interaction term is added at a time.

## Moderator Definitions

- Online Activity: W2 `v21_3` to `v21_6` summed frequency, split at the W2 median.

## Teacher Formula Interpretation

When `ModeratorHigh = 0`:

```text
intercept = b0
slope     = b1
```

When `ModeratorHigh = 1`:

```text
intercept = b0 + b2
slope     = b1 + b3
```

The key interaction test is `b3 Feature x Moderator p-value`.
It tests whether the focal feature slope differs between the low-moderator and high-moderator groups after controlling for the task-specific Top20 main effects.

## Main Outputs

- `outputs/teacher_formula_interaction_models_combined.xlsx`
- `outputs/teacher_formula_online_activity_single_feature_interaction_models.xlsx`
- `outputs/teacher_formula_online_activity_top20_adjusted_interaction_models.xlsx`
- `outputs/TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md`

## Main Sheets

- `TeacherFormulaCoefficients`: one row per Top20 feature and task, with `b0`, `b1`, `b2`, `b3`, derived intercepts, derived slopes, adjusted feature counts, and apparent model metrics.
- `CoefficientTermsLong`: long-format coefficient table.
- `PredictedProbabilities`: predicted probability values for plotting interaction lines.
- `SkippedFeatures`: features excluded from a specific moderator analysis.
- `FeatureScaling`: scaling details for each Top20 feature within each adjusted interaction model.
- `Single_vs_Adjusted` in the combined workbook: side-by-side comparison of the single-feature and Top20-adjusted interaction results.

## Note

- Single-feature variant: `W2 -> W2` runs 20 models and `W2 -> W3` runs 20 models.
- Top20-adjusted variant: `W2 -> W2` runs 20 models and `W2 -> W3` runs 20 models.
- Total models across both variants: 80.
