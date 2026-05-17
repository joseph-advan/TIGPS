# Prediction-Aligned Table 1 Group Differences Summary

## Main decision

This section now aligns Table 1 with the prediction tasks used in model performance. The predictor side is always W2 baseline features.

Included tasks:

- W2 -> W2: W2 baseline features grouped by W2 high vs low psychological distress.
- W2 -> W3: W2 baseline features grouped by W3 high vs low psychological distress.

Excluded from the main output:

- W3 features -> W3 distress. This is intentionally excluded because it does not match the baseline-prediction logic.

## Network specifications

Each prediction task is produced twice:

- Observed network: raw interpersonal nomination counts, ratios, and valence features.
- Class-adjusted network: count-like interpersonal features divided by same-class respondents minus one.

## Main workbook

- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\outputs\table1_prediction_aligned_group_differences.xlsx`

## Output files

- W2 -> W2 / Observed network: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\outputs\01_w2_features_to_w2_distress\table1_w2_to_w2_observed_network.xlsx`
- W2 -> W2 / Class-adjusted network: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\outputs\01_w2_features_to_w2_distress\table1_w2_to_w2_class_adjusted_network.xlsx`
- W2 -> W3 / Observed network: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\outputs\02_w2_features_to_w3_distress\table1_w2_to_w3_observed_network.xlsx`
- W2 -> W3 / Class-adjusted network: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\outputs\02_w2_features_to_w3_distress\table1_w2_to_w3_class_adjusted_network.xlsx`

## Largest descriptive differences by table


### W2 -> W2 - Observed network

| Question ID                                                           | Variable                                                    | High Psychological Distress   | Low Psychological Distress   | p-value   |   Between-group difference | Between-group difference type   |
|:----------------------------------------------------------------------|:------------------------------------------------------------|:------------------------------|:-----------------------------|:----------|---------------------------:|:--------------------------------|
| v52_1; v52_2; v52_3                                                   | Self-Worth and Positive Self-Concept, mean (SD)             | 2.74 (0.79)                   | 3.37 (0.63)                  | <0.001    |                     -0.875 | Cohen's d                       |
| v28_1; v28_2; v28_3; v28_4; v28_5; v28_6; v28_7; v28_8; v28_9; v28_10 | Problematic Internet Use and Internet Dependence, mean (SD) | 2.17 (0.63)                   | 1.83 (0.66)                  | <0.001    |                      0.523 | Cohen's d                       |
| v5_1; v5_2; v5_3; v5_4; v5_5; v5_6                                    | Family Cohesion and Support (Family Functioning), mean (SD) | 3.02 (0.65)                   | 3.33 (0.58)                  | <0.001    |                     -0.492 | Cohen's d                       |
| v54_4; v54_5; v54_6                                                   | Self-Management, mean (SD)                                  | 2.97 (0.73)                   | 3.26 (0.63)                  | <0.001    |                     -0.426 | Cohen's d                       |
| v54_12; v54_16                                                        | Help-Seeking, mean (SD)                                     | 2.77 (0.73)                   | 3.06 (0.68)                  | <0.001    |                     -0.418 | Cohen's d                       |
| v27_1; v27_2; v27_3                                                   | Fear of Missing Out & Social Anxiety, mean (SD)             | 2.18 (0.76)                   | 1.92 (0.72)                  | <0.001    |                      0.354 | Cohen's d                       |
| v25_7; v25_8; v25_9; v25_10; v25_11; v25_12; v25_13; v25_14; v25_15   | Online-Offline Discrepancy & Immersion, mean (SD)           | 2.28 (0.73)                   | 2.03 (0.75)                  | <0.001    |                      0.339 | Cohen's d                       |
| v54_7; v54_8; v54_9                                                   | Motivation & Goal Setting, mean (SD)                        | 2.89 (0.73)                   | 3.12 (0.68)                  | <0.001    |                     -0.324 | Cohen's d                       |

### W2 -> W2 - Class-adjusted network

| Question ID                                                           | Variable                                                    | High Psychological Distress   | Low Psychological Distress   | p-value   |   Between-group difference | Between-group difference type   |
|:----------------------------------------------------------------------|:------------------------------------------------------------|:------------------------------|:-----------------------------|:----------|---------------------------:|:--------------------------------|
| v52_1; v52_2; v52_3                                                   | Self-Worth and Positive Self-Concept, mean (SD)             | 2.74 (0.79)                   | 3.37 (0.63)                  | <0.001    |                     -0.875 | Cohen's d                       |
| v28_1; v28_2; v28_3; v28_4; v28_5; v28_6; v28_7; v28_8; v28_9; v28_10 | Problematic Internet Use and Internet Dependence, mean (SD) | 2.17 (0.63)                   | 1.83 (0.66)                  | <0.001    |                      0.523 | Cohen's d                       |
| v5_1; v5_2; v5_3; v5_4; v5_5; v5_6                                    | Family Cohesion and Support (Family Functioning), mean (SD) | 3.02 (0.65)                   | 3.33 (0.58)                  | <0.001    |                     -0.492 | Cohen's d                       |
| v54_4; v54_5; v54_6                                                   | Self-Management, mean (SD)                                  | 2.97 (0.73)                   | 3.26 (0.63)                  | <0.001    |                     -0.426 | Cohen's d                       |
| v54_12; v54_16                                                        | Help-Seeking, mean (SD)                                     | 2.77 (0.73)                   | 3.06 (0.68)                  | <0.001    |                     -0.418 | Cohen's d                       |
| v27_1; v27_2; v27_3                                                   | Fear of Missing Out & Social Anxiety, mean (SD)             | 2.18 (0.76)                   | 1.92 (0.72)                  | <0.001    |                      0.354 | Cohen's d                       |
| v25_7; v25_8; v25_9; v25_10; v25_11; v25_12; v25_13; v25_14; v25_15   | Online-Offline Discrepancy & Immersion, mean (SD)           | 2.28 (0.73)                   | 2.03 (0.75)                  | <0.001    |                      0.339 | Cohen's d                       |
| v54_7; v54_8; v54_9                                                   | Motivation & Goal Setting, mean (SD)                        | 2.89 (0.73)                   | 3.12 (0.68)                  | <0.001    |                     -0.324 | Cohen's d                       |

### W2 -> W3 - Observed network

| Question ID                                                           | Variable                                                    | High Psychological Distress   | Low Psychological Distress   | p-value   |   Between-group difference | Between-group difference type   |
|:----------------------------------------------------------------------|:------------------------------------------------------------|:------------------------------|:-----------------------------|:----------|---------------------------:|:--------------------------------|
| v52_1; v52_2; v52_3                                                   | Self-Worth and Positive Self-Concept, mean (SD)             | 2.83 (0.81)                   | 3.25 (0.70)                  | <0.001    |                     -0.557 | Cohen's d                       |
| v28_1; v28_2; v28_3; v28_4; v28_5; v28_6; v28_7; v28_8; v28_9; v28_10 | Problematic Internet Use and Internet Dependence, mean (SD) | 2.13 (0.65)                   | 1.88 (0.66)                  | <0.001    |                      0.37  | Cohen's d                       |
| v5_1; v5_2; v5_3; v5_4; v5_5; v5_6                                    | Family Cohesion and Support (Family Functioning), mean (SD) | 3.06 (0.65)                   | 3.28 (0.61)                  | <0.001    |                     -0.349 | Cohen's d                       |
| v25_7; v25_8; v25_9; v25_10; v25_11; v25_12; v25_13; v25_14; v25_15   | Online-Offline Discrepancy & Immersion, mean (SD)           | 2.27 (0.75)                   | 2.04 (0.74)                  | <0.001    |                      0.306 | Cohen's d                       |
| v27_1; v27_2; v27_3                                                   | Fear of Missing Out & Social Anxiety, mean (SD)             | 2.17 (0.75)                   | 1.94 (0.74)                  | <0.001    |                      0.303 | Cohen's d                       |
| v54_4; v54_5; v54_6                                                   | Self-Management, mean (SD)                                  | 3.01 (0.72)                   | 3.20 (0.67)                  | <0.001    |                     -0.277 | Cohen's d                       |
| v54_12; v54_16                                                        | Help-Seeking, mean (SD)                                     | 2.81 (0.73)                   | 3.00 (0.70)                  | <0.001    |                     -0.268 | Cohen's d                       |
| v25_4; v25_5; v25_6                                                   | Real-life Self-Satisfaction, mean (SD)                      | 2.69 (0.78)                   | 2.89 (0.76)                  | <0.001    |                     -0.258 | Cohen's d                       |

### W2 -> W3 - Class-adjusted network

| Question ID                                                           | Variable                                                    | High Psychological Distress   | Low Psychological Distress   | p-value   |   Between-group difference | Between-group difference type   |
|:----------------------------------------------------------------------|:------------------------------------------------------------|:------------------------------|:-----------------------------|:----------|---------------------------:|:--------------------------------|
| v52_1; v52_2; v52_3                                                   | Self-Worth and Positive Self-Concept, mean (SD)             | 2.83 (0.81)                   | 3.25 (0.70)                  | <0.001    |                     -0.557 | Cohen's d                       |
| v28_1; v28_2; v28_3; v28_4; v28_5; v28_6; v28_7; v28_8; v28_9; v28_10 | Problematic Internet Use and Internet Dependence, mean (SD) | 2.13 (0.65)                   | 1.88 (0.66)                  | <0.001    |                      0.37  | Cohen's d                       |
| v5_1; v5_2; v5_3; v5_4; v5_5; v5_6                                    | Family Cohesion and Support (Family Functioning), mean (SD) | 3.06 (0.65)                   | 3.28 (0.61)                  | <0.001    |                     -0.349 | Cohen's d                       |
| v25_7; v25_8; v25_9; v25_10; v25_11; v25_12; v25_13; v25_14; v25_15   | Online-Offline Discrepancy & Immersion, mean (SD)           | 2.27 (0.75)                   | 2.04 (0.74)                  | <0.001    |                      0.306 | Cohen's d                       |
| v27_1; v27_2; v27_3                                                   | Fear of Missing Out & Social Anxiety, mean (SD)             | 2.17 (0.75)                   | 1.94 (0.74)                  | <0.001    |                      0.303 | Cohen's d                       |
| v54_4; v54_5; v54_6                                                   | Self-Management, mean (SD)                                  | 3.01 (0.72)                   | 3.20 (0.67)                  | <0.001    |                     -0.277 | Cohen's d                       |
| v54_12; v54_16                                                        | Help-Seeking, mean (SD)                                     | 2.81 (0.73)                   | 3.00 (0.70)                  | <0.001    |                     -0.268 | Cohen's d                       |
| v25_4; v25_5; v25_6                                                   | Real-life Self-Satisfaction, mean (SD)                      | 2.69 (0.78)                   | 2.89 (0.76)                  | <0.001    |                     -0.258 | Cohen's d                       |

## Interpersonal feature signal

This table focuses on the stricter `p < .01` threshold. Because the sample size is large, statistical significance alone is not enough; the effect-size columns should be read at the same time.

| Table key | Interpersonal rows | Rows with p < .01 | Median absolute effect size | Max absolute effect size |
|---|---:|---:|---:|---:|
| w2_to_w2_observed_network | 12 | 5 | 0.053 | 0.215 |
| w2_to_w2_class_adjusted_network | 12 | 6 | 0.080 | 0.226 |
| w2_to_w3_observed_network | 12 | 4 | 0.030 | 0.113 |
| w2_to_w3_class_adjusted_network | 12 | 6 | 0.063 | 0.130 |

## Interpretation

Use these tables as descriptive screening evidence before the model-based feature-importance and interaction sections. The W2 -> W3 table is especially important for the longitudinal story because it asks whether baseline W2 characteristics already distinguish students who later fall into the W3 high-distress group.

For the interpersonal features, the main question is not only whether p-values pass the threshold. The more important pattern is whether the observed differences are large enough to matter and whether they remain consistent after class adjustment. If a feature is significant but has a small absolute effect size, it should be described as a detectable descriptive difference rather than a strong substantive difference.

The `NetworkComparison` sheet is arranged by interpersonal feature concept. For each concept, the observed row is followed immediately by the class-adjusted row, so the reader can directly compare whether class-size adjustment changes the p-value, group means, or effect size.
