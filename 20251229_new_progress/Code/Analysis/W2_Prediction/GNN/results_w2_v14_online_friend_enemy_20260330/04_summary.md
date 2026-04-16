# W2 v14 Four-Relation GNN Pipeline Summary

## Experiment Setup

- **W2 data**: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- **Merged mapping**: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- **Seeds**: [42, 52, 62, 72, 82]
- **Split method**: group-disjoint by school_id+class
- **Nodes**: 7023
- **online_friend edges (unique no-self)**: 22557
- **online_enemy edges (unique no-self)**: 10631
- **offline_friend edges (unique no-self)**: 23796
- **offline_enemy edges (unique no-self)**: 11948
- **Merged edges (unique no-self)**: 42193
- **Unmatched nominations**: 19811
- **Mapping conflict keys**: 0

## Key Findings

- For classification (accuracy, f1, auc), baseline_non_graph is the best on all three metrics.
- For regression_sum (rmse, mae, r2), sage_merge is the best model.
- For regression_sum median_class_acc_from_score, baseline_non_graph is still the best.
- gat_merge is the weakest model in regression_sum and has the largest variance.

## Classification Metrics (mean +/- std)

| metric | baseline_non_graph | gcn_merge | gcn_separate | sage_merge | sage_separate | gat_merge | gat_separate | best |
|---|---|---|---|---|---|---|---|---|
| accuracy | 0.7542 +/- 0.0146 | 0.6411 +/- 0.0058 | 0.7024 +/- 0.0154 | 0.7497 +/- 0.0069 | 0.7395 +/- 0.0100 | 0.6284 +/- 0.0128 | 0.6971 +/- 0.0016 | baseline_non_graph |
| f1 | 0.7750 +/- 0.0136 | 0.6735 +/- 0.0079 | 0.7278 +/- 0.0075 | 0.7694 +/- 0.0076 | 0.7573 +/- 0.0102 | 0.6668 +/- 0.0193 | 0.7203 +/- 0.0110 | baseline_non_graph |
| auc | 0.8316 +/- 0.0071 | 0.6933 +/- 0.0057 | 0.7762 +/- 0.0104 | 0.8312 +/- 0.0063 | 0.8221 +/- 0.0066 | 0.6760 +/- 0.0089 | 0.7702 +/- 0.0081 | baseline_non_graph |

## Regression Sum Metrics (mean +/- std)

| metric | baseline_non_graph | gcn_merge | gcn_separate | sage_merge | sage_separate | gat_merge | gat_separate | best | delta_sage_merge_vs_baseline |
|---|---|---|---|---|---|---|---|---|---|
| rmse | 8.1250 +/- 0.2381 | 10.6973 +/- 0.2879 | 9.5910 +/- 0.3266 | 8.0470 +/- 0.3280 | 8.1343 +/- 0.2859 | 12.3903 +/- 1.5938 | 10.0879 +/- 0.3061 | sage_merge | +0.0780 |
| mae | 5.5362 +/- 0.1215 | 7.3380 +/- 0.2602 | 6.5231 +/- 0.2300 | 5.3827 +/- 0.2274 | 5.4339 +/- 0.2055 | 8.0416 +/- 1.1288 | 6.7970 +/- 0.2916 | sage_merge | +0.1535 |
| r2 | 0.4100 +/- 0.0169 | -0.0231 +/- 0.0370 | 0.1779 +/- 0.0276 | 0.4209 +/- 0.0357 | 0.4085 +/- 0.0259 | -0.3927 +/- 0.3674 | 0.0905 +/- 0.0255 | sage_merge | +0.0110 |
| median_class_acc_from_score | 0.7072 +/- 0.0064 | 0.5976 +/- 0.0087 | 0.6534 +/- 0.0109 | 0.6910 +/- 0.0136 | 0.6907 +/- 0.0091 | 0.5402 +/- 0.0494 | 0.6260 +/- 0.0156 | baseline_non_graph | -0.0162 |

## Notes

- Lower is better for rmse and mae.
- Higher is better for accuracy, f1, auc, and r2.
- Results are mean and std across 5 seeds: 42, 52, 62, 72, 82.
- Split is group-disjoint by school_id+class to reduce group leakage between train and test.

## Appendix: Model Rankings

Ranking rule:
- For `rmse` and `mae`, lower is better.
- For `accuracy`, `f1`, `auc`, `r2`, and `median_class_acc_from_score`, higher is better.

### Task: `classification`

#### Metric: `accuracy`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | baseline_non_graph | 0.754176 | 0.014578 | 0.7542 +/- 0.0146 | +0.000000 |
| 2 | sage_merge | 0.749721 | 0.006877 | 0.7497 +/- 0.0069 | -0.004455 |
| 3 | sage_separate | 0.739500 | 0.010001 | 0.7395 +/- 0.0100 | -0.014675 |
| 4 | gcn_separate | 0.702376 | 0.015374 | 0.7024 +/- 0.0154 | -0.051799 |
| 5 | gat_separate | 0.697054 | 0.001562 | 0.6971 +/- 0.0016 | -0.057122 |
| 6 | gcn_merge | 0.641116 | 0.005835 | 0.6411 +/- 0.0058 | -0.113060 |
| 7 | gat_merge | 0.628447 | 0.012771 | 0.6284 +/- 0.0128 | -0.125728 |

#### Metric: `f1`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | baseline_non_graph | 0.775044 | 0.013578 | 0.7750 +/- 0.0136 | +0.000000 |
| 2 | sage_merge | 0.769403 | 0.007638 | 0.7694 +/- 0.0076 | -0.005641 |
| 3 | sage_separate | 0.757274 | 0.010161 | 0.7573 +/- 0.0102 | -0.017771 |
| 4 | gcn_separate | 0.727757 | 0.007457 | 0.7278 +/- 0.0075 | -0.047287 |
| 5 | gat_separate | 0.720327 | 0.010984 | 0.7203 +/- 0.0110 | -0.054717 |
| 6 | gcn_merge | 0.673456 | 0.007886 | 0.6735 +/- 0.0079 | -0.101588 |
| 7 | gat_merge | 0.666814 | 0.019303 | 0.6668 +/- 0.0193 | -0.108231 |

#### Metric: `auc`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | baseline_non_graph | 0.831604 | 0.007132 | 0.8316 +/- 0.0071 | +0.000000 |
| 2 | sage_merge | 0.831155 | 0.006329 | 0.8312 +/- 0.0063 | -0.000449 |
| 3 | sage_separate | 0.822095 | 0.006622 | 0.8221 +/- 0.0066 | -0.009510 |
| 4 | gcn_separate | 0.776222 | 0.010422 | 0.7762 +/- 0.0104 | -0.055382 |
| 5 | gat_separate | 0.770167 | 0.008106 | 0.7702 +/- 0.0081 | -0.061438 |
| 6 | gcn_merge | 0.693308 | 0.005661 | 0.6933 +/- 0.0057 | -0.138297 |
| 7 | gat_merge | 0.676008 | 0.008931 | 0.6760 +/- 0.0089 | -0.155597 |

### Task: `regression_sum`

#### Metric: `rmse`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | sage_merge | 8.047017 | 0.328017 | 8.0470 +/- 0.3280 | +0.077991 |
| 2 | baseline_non_graph | 8.125008 | 0.238089 | 8.1250 +/- 0.2381 | +0.000000 |
| 3 | sage_separate | 8.134311 | 0.285942 | 8.1343 +/- 0.2859 | -0.009303 |
| 4 | gcn_separate | 9.590990 | 0.326603 | 9.5910 +/- 0.3266 | -1.465982 |
| 5 | gat_separate | 10.087874 | 0.306064 | 10.0879 +/- 0.3061 | -1.962865 |
| 6 | gcn_merge | 10.697286 | 0.287863 | 10.6973 +/- 0.2879 | -2.572278 |
| 7 | gat_merge | 12.390251 | 1.593757 | 12.3903 +/- 1.5938 | -4.265243 |

#### Metric: `mae`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | sage_merge | 5.382692 | 0.227418 | 5.3827 +/- 0.2274 | +0.153536 |
| 2 | sage_separate | 5.433935 | 0.205533 | 5.4339 +/- 0.2055 | +0.102292 |
| 3 | baseline_non_graph | 5.536227 | 0.121453 | 5.5362 +/- 0.1215 | +0.000000 |
| 4 | gcn_separate | 6.523084 | 0.229973 | 6.5231 +/- 0.2300 | -0.986857 |
| 5 | gat_separate | 6.796988 | 0.291570 | 6.7970 +/- 0.2916 | -1.260761 |
| 6 | gcn_merge | 7.338024 | 0.260221 | 7.3380 +/- 0.2602 | -1.801797 |
| 7 | gat_merge | 8.041611 | 1.128815 | 8.0416 +/- 1.1288 | -2.505384 |

#### Metric: `r2`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | sage_merge | 0.420913 | 0.035701 | 0.4209 +/- 0.0357 | +0.010963 |
| 2 | baseline_non_graph | 0.409951 | 0.016870 | 0.4100 +/- 0.0169 | +0.000000 |
| 3 | sage_separate | 0.408521 | 0.025859 | 0.4085 +/- 0.0259 | -0.001430 |
| 4 | gcn_separate | 0.177924 | 0.027585 | 0.1779 +/- 0.0276 | -0.232027 |
| 5 | gat_separate | 0.090486 | 0.025510 | 0.0905 +/- 0.0255 | -0.319465 |
| 6 | gcn_merge | -0.023109 | 0.036980 | -0.0231 +/- 0.0370 | -0.433060 |
| 7 | gat_merge | -0.392736 | 0.367413 | -0.3927 +/- 0.3674 | -0.802687 |

#### Metric: `median_class_acc_from_score`

| rank | model | mean | std | mean +/- std | delta_vs_baseline (good direction) |
|---:|---|---:|---:|---|---:|
| 1 | baseline_non_graph | 0.707199 | 0.006448 | 0.7072 +/- 0.0064 | +0.000000 |
| 2 | sage_merge | 0.690981 | 0.013570 | 0.6910 +/- 0.0136 | -0.016219 |
| 3 | sage_separate | 0.690718 | 0.009134 | 0.6907 +/- 0.0091 | -0.016482 |
| 4 | gcn_separate | 0.653419 | 0.010850 | 0.6534 +/- 0.0109 | -0.053780 |
| 5 | gat_separate | 0.626019 | 0.015561 | 0.6260 +/- 0.0156 | -0.081180 |
| 6 | gcn_merge | 0.597640 | 0.008692 | 0.5976 +/- 0.0087 | -0.109560 |
| 7 | gat_merge | 0.540184 | 0.049407 | 0.5402 +/- 0.0494 | -0.167016 |
