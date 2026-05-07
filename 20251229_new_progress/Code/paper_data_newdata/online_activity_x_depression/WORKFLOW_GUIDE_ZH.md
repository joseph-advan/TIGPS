# Online Activity x Depression Workflow Guide

This document describes the workflow used to examine whether online activity and peer nomination patterns are associated with depressive symptoms in W2 and W3.

## 1. Purpose

The analysis answers three questions:

1. Are students with higher online activity or peer nomination counts different in depressive symptoms?
2. Do online activity and depressive symptoms change from W2 to W3?
3. Do family support or self-worth show protective associations among higher-risk students?

## 2. Data Sources

Current cleaned data:

- W2: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv`
- W3: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv`

The current analysis uses the final aligned W2/W3 student roster. Both waves are restricted to the same 6603 `student_id` values.

## 3. Main Variables

### 3.1 Online Activity

Online activity is calculated from the summed frequency of selected online activity items.

- W2 items: `v21_3` to `v21_6`
- W3 items: `21-3` to `21-6`

`high_activity` is defined as:

```text
online_activity_sum > wave-specific median
```

### 3.2 Depressive Symptoms

Depressive symptoms are constructed from depression-related survey items.

- W2 items: `v14_1_01` to `v14_1_05`, `v14_2_01` to `v14_2_05`
- W3 items: `8-1_0` to `8-1_4`, `8-4_0` to `8-4_4`

Higher values indicate higher depressive symptoms after item scoring and reverse-item handling.

### 3.3 Peer Nomination

Peer nomination features are derived from cleaned peer nomination fields.

- W2 nomination items: `v55_1` to `v55_14`
- W3 nomination items: `54-1` to `54-14`

The workflow computes:

- `nom_out_count`: number of valid nominations made by the student
- `nom_in_count`: number of valid nominations received by the student
- `nom_total_count`: `nom_out_count + nom_in_count`

Within each class, nomination counts are standardized:

- `nom_out_z`
- `nom_in_z`
- `nom_total_z`

High nomination groups are defined as:

```text
high_nomination_out_main = nom_out_z > 0
high_nomination_in_main = nom_in_z > 0
high_nomination_total_main = nom_total_z > 0
```

### 3.4 Protective Factors

Two protective factors are used in the high-risk analysis:

- Family support
- Self-worth

These are constructed from configured survey items in the analysis script and reverse-item configuration.

## 4. Analysis Stages

### Stage 1: Main Effects

Output:

- `stage1_main_effects.csv`

Method:

- Welch two-sample t-test
- Compares depressive symptoms between high and low groups

Grouping variables:

- `high_activity`
- `high_nomination_out_main`
- `high_nomination_in_main`
- `high_nomination_total_main`

### Stage 2: Cross-Year Change

Output:

- `stage2_cross_year.csv`

Method:

- Welch two-sample t-test
- Compares W2 and W3 values

Outcomes:

- Online activity
- Depressive symptoms

### Stage 3A: Protective Effects Within High-Risk Groups

Output:

- `stage3_within_highrisk_protective_effects.csv`

Method:

- Within each high-risk group, compare depressive symptoms between students with higher and lower protective factors.
- Protective factors are split by wave-specific median.

Interpretation:

- A negative `mean_diff_high_minus_low` means students with higher protective factor scores have lower depressive symptoms.

### Stage 3B: Interaction Models

Output:

- `stage3_interaction_models.csv`

Method:

- Regression models with high-risk group, protective factor, and interaction term.

Key term:

```text
interaction_beta
```

Interpretation:

- `interaction_beta < 0`: the protective factor is associated with weaker risk-related depression differences.
- `interaction_beta > 0`: the protective factor is associated with stronger risk-related depression differences.

## 5. Output Files

The script writes the following files:

- `wave_features_w2.csv`
- `wave_features_w3.csv`
- `stage1_main_effects.csv`
- `stage2_cross_year.csv`
- `stage3_within_highrisk_protective_effects.csv`
- `stage3_interaction_models.csv`
- `analysis_report.md`

## 6. Current Key Results

### 6.1 Stage 1 Main Effects

| Analysis | Low N | High N | Mean diff high-low | p-value | Cohen's d |
|---|---:|---:|---:|---:|---:|
| W2 online activity | 3511 | 3035 | 0.1657 | 1.13e-18 | -0.2220 |
| W2 nomination out | 3579 | 3024 | 0.0917 | 8.63e-07 | -0.1226 |
| W2 nomination in | 2864 | 3739 | -0.0341 | 0.0667 | 0.0455 |
| W2 nomination total | 2884 | 3719 | -0.0055 | 0.7659 | 0.0074 |
| W3 online activity | 3617 | 2986 | 0.0602 | 0.0016 | -0.0789 |
| W3 nomination out | 3474 | 3129 | 0.0187 | 0.3192 | -0.0245 |
| W3 nomination in | 3069 | 3522 | 0.0250 | 0.1833 | -0.0328 |
| W3 nomination total | 2997 | 3594 | 0.0097 | 0.6068 | -0.0127 |

Summary:

- Higher online activity is associated with higher depressive symptoms in both W2 and W3.
- The effect is stronger in W2 than in W3.
- Higher outgoing nomination is associated with higher depressive symptoms in W2, but not in W3.
- Incoming and total nomination groups do not show consistent main-effect differences.

### 6.2 Stage 2 Cross-Year Change

The cross-year analysis compares W2 and W3 values for online activity and depressive symptoms.

Use `stage2_cross_year.csv` for the exact means, mean differences, p-values, and effect sizes.

### 6.3 Stage 3 Protective Effects

The within-risk-group results evaluate whether family support and self-worth are associated with lower depressive symptoms among students in higher-risk groups.

Expected interpretation:

- If the protective factor has a negative mean difference, higher support or self-worth is associated with lower depressive symptoms.
- Family support and self-worth should be interpreted as correlational protective indicators, not causal effects.

The interaction models test whether the association between high-risk status and depressive symptoms differs by protective factor level.

## 7. How To Run

From the project root:

```powershell
python 20251229_new_progress/Code/paper_data_newdata/online_activity_x_depression/run_online_activity_x_depression.py
```

## 8. Notes

- The workflow now uses the cleaned and aligned W2/W3 datasets.
- All cross-wave analyses should remain restricted to the same 6603 students.
- The results are descriptive and correlational.
- Multiple testing should be considered when interpreting Stage 3 results.
- Reverse-item handling is controlled by `reverse_items_config.json`.
