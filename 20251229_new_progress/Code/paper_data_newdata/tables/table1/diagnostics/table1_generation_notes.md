# Table 1 Generation Notes

## Input Data

- W2: `Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3: `Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Variable plan: `Code\paper_data_newdata\tables\table1\config\table1_variable_plan_draft.csv`
- Scoring config: `Code\paper_data_newdata\tables\table1\config\table1_scoring_config.json`

## Grouping Rule

- Students must have all four online activity items valid.
- High Online Activity: `online_activity_sum > wave-specific median`.
- Low Online Activity: `online_activity_sum <= wave-specific median`.

## Presentation Rule

- Categorical variables: `n (%)` by response category.
- Binary variables: coded `1` as `Yes n (%)`.
- Single-item ordinal variables: `mean (SD)`.
- Multi-item scales: mean of available items, requiring at least 50% valid items.
- p-values compare High vs Low Online Activity.
- Categorical and binary variables use chi-square tests; binary variables use Fisher's exact test if expected cell counts are below 5.
- Single-item ordinal and multi-item scale variables use Welch two-sample t-tests.

## Reverse Coding

- Parenting Practices and Parent-Child Interaction Quality uses reverse coding.
- W2 reverse-coded items: `v6_1`, `v6_5`, `v6_6`, `v6_8`, `v6_9`.
- W3 reverse-coded items: `5-1`, `5-5`, `5-6`, `5-8`, `5-9`.
- Formula: `reversed_value = min + max - original_value`, with `min = 1`, `max = 4`.

## Gender Label

- `1 = Male`.
- `2 = Female`.

## Outputs

- `table1_w2_2024.csv`
- `table1_w2_2024.md`
- `table1_w3_2025.csv`
- `table1_w3_2025.md`
- `diagnostics/table1_online_activity_group_diagnostics.csv`