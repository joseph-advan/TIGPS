# 06 Teacher Formula Interaction Models

## Purpose

This folder estimates the interaction models in the format requested by the advisor:

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + covariates
```

Because the outcome is binary high psychological distress, the coefficients are logistic-regression log-odds coefficients.

## Moderator Definitions

- Online Activity: W2 `v21_3` to `v21_6` summed frequency, split at the W2 median.
- Problematic Internet Use: constructed W2 `v28` feature, split at the W2 median.

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

## Main Outputs

- `outputs/teacher_formula_interaction_models_combined.xlsx`
- `outputs/teacher_formula_online_activity_interaction_models.xlsx`
- `outputs/teacher_formula_problematic_internet_use_interaction_models.xlsx`
- `outputs/TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md`

## Main Sheets

- `TeacherFormulaCoefficients`: one row per Top20 feature and task, with `b0`, `b1`, `b2`, `b3`, derived intercepts, and derived slopes.
- `CoefficientTermsLong`: long-format coefficient table.
- `PredictedProbabilities`: predicted probability values for plotting interaction lines.
- `SkippedFeatures`: features excluded from a specific moderator analysis.

## Note

For the problematic internet use moderator analysis, `v28` is excluded as a focal feature because `v28` defines the high/low moderator group.
