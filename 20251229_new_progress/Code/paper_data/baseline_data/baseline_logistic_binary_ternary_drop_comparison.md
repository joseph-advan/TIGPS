# Baseline Comparison: Binary vs Ternary, Full vs Drop-Groups

## Executive Summary

- Four settings are compared:
  - Binary full: `baseline_logistic_median_split_classification_summary.csv`
  - Binary drop-groups: `baseline_logistic_median_split_drop_groups_classification_summary.csv`
  - Ternary full (33/67): `baseline_logistic_tertile_33_67_classification_summary.csv`
  - Ternary drop-groups (33/67): `baseline_logistic_tertile_33_67_drop_groups_classification_summary.csv`
- Best binary test accuracy (full): `w2_self` = `0.7573`
- Best ternary test accuracy (full): `w3_self` = `0.5751`
- Average drop impact on test accuracy:
  - Binary: `-0.0266` (drop - full)
  - Ternary: `-0.0301` (drop - full)
- In current data, dropping the specified groups lowers performance in all three scenarios for both binary and ternary settings.

## Binary (Median Split) - Full vs Drop

| scenario | full_test_acc | drop_test_acc | delta_acc | full_test_f1 | drop_test_f1 | delta_f1 | full_test_auc | drop_test_auc | delta_auc |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.757295 | 0.720996 | -0.036299 | 0.777850 | 0.742782 | -0.035068 | 0.820486 | 0.784406 | -0.036081 |
| w3_self | 0.707473 | 0.684698 | -0.022776 | 0.719836 | 0.698844 | -0.020992 | 0.787829 | 0.752752 | -0.035077 |
| w2_predict_w3 | 0.656228 | 0.635587 | -0.020641 | 0.653763 | 0.637907 | -0.015857 | 0.723444 | 0.703792 | -0.019652 |

### Binary CV5 Comparison

| scenario | full_cv5_acc | drop_cv5_acc | delta_cv5_acc | full_cv5_f1 | drop_cv5_f1 | delta_cv5_f1 | full_cv5_auc | drop_cv5_auc | delta_cv5_auc |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.744270 | 0.710949 | -0.033321 | 0.765811 | 0.737089 | -0.028722 | 0.820455 | 0.777671 | -0.042784 |
| w3_self | 0.727321 | 0.697704 | -0.029617 | 0.732842 | 0.706002 | -0.026840 | 0.806155 | 0.768045 | -0.038110 |
| w2_predict_w3 | 0.667240 | 0.648729 | -0.018510 | 0.672513 | 0.654675 | -0.017837 | 0.730958 | 0.709049 | -0.021909 |

## Ternary (33/67 Split) - Full vs Drop

| scenario | full_test_acc | drop_test_acc | delta_acc | full_test_macro_f1 | drop_test_macro_f1 | delta_macro_f1 | full_test_macro_auc_ovr | drop_test_macro_auc_ovr | delta_macro_auc_ovr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.570819 | 0.537367 | -0.033452 | 0.563834 | 0.526458 | -0.037376 | 0.763502 | 0.724337 | -0.039165 |
| w3_self | 0.575089 | 0.540214 | -0.034875 | 0.575429 | 0.541676 | -0.033754 | 0.759972 | 0.732452 | -0.027520 |
| w2_predict_w3 | 0.496085 | 0.474021 | -0.022064 | 0.495756 | 0.470561 | -0.025195 | 0.672756 | 0.654433 | -0.018323 |

### Ternary CV5 Comparison

| scenario | full_cv5_acc | drop_cv5_acc | delta_cv5_acc | full_cv5_macro_f1 | drop_cv5_macro_f1 | delta_cv5_macro_f1 | full_cv5_macro_auc_ovr | drop_cv5_macro_auc_ovr | delta_cv5_macro_auc_ovr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.587355 | 0.534101 | -0.053254 | 0.577925 | 0.521839 | -0.056086 | 0.768920 | 0.725252 | -0.043667 |
| w3_self | 0.574257 | 0.538659 | -0.035598 | 0.574402 | 0.539368 | -0.035035 | 0.761583 | 0.730007 | -0.031576 |
| w2_predict_w3 | 0.507616 | 0.486687 | -0.020930 | 0.508181 | 0.484221 | -0.023960 | 0.690038 | 0.666580 | -0.023459 |

## Notes

- `delta` is always computed as `drop - full`; negative means the drop-groups version is worse.
- Binary uses median split (0/1), ternary uses 33/67 quantiles (0/1/2).
