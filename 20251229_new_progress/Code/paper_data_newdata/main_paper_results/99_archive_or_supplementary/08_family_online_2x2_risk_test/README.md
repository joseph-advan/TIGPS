# Family Cohesion x Online Activity 2x2 Risk Test

## Purpose

This section converts the continuous interaction result from Section 06 into an intuitive subgroup-level risk test.

The main question is whether students with lower W2 family cohesion and high W2 online activity form a higher-risk subgroup for psychological distress.

## Design

Four groups are created from W2 predictors:

1. High Family Cohesion + Low Online Activity
2. High Family Cohesion + High Online Activity
3. Low Family Cohesion + Low Online Activity
4. Low Family Cohesion + High Online Activity

Definitions:

- Family Cohesion: W2 `v5` decomposed feature score. High = above W2 median; Low = at or below W2 median.
- Online Activity: W2 `v21_3` to `v21_6` summed score. High = above W2 median; Low = at or below W2 median.
- Outcome: High Psychological Distress by median split of the distress score for each task.

## Outputs

- `outputs/family_cohesion_online_activity_2x2_risk_test.xlsx`
- `outputs/FAMILY_COHESION_ONLINE_ACTIVITY_2X2_RISK_TEST_ZH.md`

## Interpretation Rule

Use the group percentages to describe risk ranking. Use the 2x2 interaction coefficient `b3` only to decide whether the Low Family + High Online combination has an additional multiplicative/logit-scale effect beyond the two main effects.
