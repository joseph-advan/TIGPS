# Table 2 and Table 3 Generation Notes

## Inputs

- W2 data: `Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Table 1 variable plan: `Code\paper_data_newdata\tables\table1\config\table1_variable_plan_draft.csv`
- Table 1 scoring config: `Code\paper_data_newdata\tables\table1\config\table1_scoring_config.json`
- Subscale config: `Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`

## Outcome

- W2 outcome items: `v55_1` to `v55_14`.
- W3 outcome items: `54-1` to `54-14`.
- Outcome score aggregation: sum.
- Binary outcome: score >= wave-specific median cutoff.

## Predictors

- Predictors start from the Table 1 variable plan, excluding the psychological distress outcome.
- Decomposed groups replace their parent scale scores: FOMO, social media self-presentation, social media use, online social comparison, and SEL.
- Online Activity Sum is added as a predictor using complete four-item sums.
- Multi-item scale predictors require at least 50% valid items.
- Parenting items use the same reverse coding as Table 1.
- W2 `v52` is used as Self-Rated Health; W2 `v52_1` to `v52_3` are retained as Self-Worth.
- Gender reference category is Female. Family Structure reference category is Married, living together.

## Table 2

- Univariate logistic regression: one predictor at a time.
- Multivariable logistic regression: complete-case model across all predictors.
- Reported columns: B, SE, p-value, OR, and OR 95% CI.

## Table 3

- Table 3A compares standardized coefficients from multivariable logistic, LASSO logistic, and Ridge logistic.
- Table 3B compares model performance using an 80/20 stratified test split and 5-fold cross-validation.
- LASSO/Ridge coefficients do not have traditional SE/p-values; they are reported as standardized coefficients for model comparison.
