# A1/A2 B1/B2 C1/C2 D1~D5 vs Drop Baseline

## 1. Group Definition
- A1 (OUT): ip_out_online_friend, ip_out_online_enemy, ip_out_offline_friend, ip_out_offline_enemy
- A2 (IN): ip_in_online_friend, ip_in_online_enemy, ip_in_offline_friend, ip_in_offline_enemy
- B1 (OUT): ip_out_friend_total, ip_out_enemy_total
- B2 (IN): ip_in_friend_total, ip_in_enemy_total
- C1 (OUT): ip_out_friend_online_minus_offline, ip_out_enemy_online_minus_offline
- C2 (IN): ip_in_friend_online_minus_offline, ip_in_enemy_online_minus_offline
- D1~D5: single-feature groups

| group           |   n_features | features                                                                               |
|:----------------|-------------:|:---------------------------------------------------------------------------------------|
| Drop Baseline   |            0 |                                                                                        |
| Drop + A1 (OUT) |            4 | ip_out_online_friend; ip_out_online_enemy; ip_out_offline_friend; ip_out_offline_enemy |
| Drop + A2 (IN)  |            4 | ip_in_online_friend; ip_in_online_enemy; ip_in_offline_friend; ip_in_offline_enemy     |
| Drop + B1 (OUT) |            2 | ip_out_friend_total; ip_out_enemy_total                                                |
| Drop + B2 (IN)  |            2 | ip_in_friend_total; ip_in_enemy_total                                                  |
| Drop + C1 (OUT) |            2 | ip_out_friend_online_minus_offline; ip_out_enemy_online_minus_offline                  |
| Drop + C2 (IN)  |            2 | ip_in_friend_online_minus_offline; ip_in_enemy_online_minus_offline                    |
| Drop + D1       |            1 | ip_reciprocal_friend_count                                                             |
| Drop + D2       |            1 | ip_reciprocal_enemy_count                                                              |
| Drop + D3       |            1 | ip_liked_by_me_but_enemy_to_me_count                                                   |
| Drop + D4       |            1 | ip_enemy_by_me_but_likes_me_count                                                      |
| Drop + D5       |            1 | ip_same_target_friend_and_enemy_count                                                  |

## 2. Overall Mean Performance
| setting_label   |   mean_test_accuracy |   mean_test_f1 |   mean_test_auc |
|:----------------|---------------------:|---------------:|----------------:|
| Drop Baseline   |             0.710102 |       0.715628 |        0.775751 |
| Drop + A1 (OUT) |             0.708116 |       0.714191 |        0.776381 |
| Drop + A2 (IN)  |             0.706875 |       0.712788 |        0.775535 |
| Drop + B1 (OUT) |             0.708364 |       0.714218 |        0.776099 |
| Drop + B2 (IN)  |             0.707372 |       0.713359 |        0.775711 |
| Drop + C1 (OUT) |             0.711095 |       0.717319 |        0.77599  |
| Drop + C2 (IN)  |             0.705882 |       0.711381 |        0.775361 |
| Drop + D1       |             0.707372 |       0.713695 |        0.775771 |
| Drop + D2       |             0.706627 |       0.712607 |        0.775779 |
| Drop + D3       |             0.709109 |       0.714408 |        0.775562 |
| Drop + D4       |             0.710102 |       0.715833 |        0.77575  |
| Drop + D5       |             0.711591 |       0.717421 |        0.776188 |

## 3. Scenario Details
### W2 -> W2
Drop Baseline test_accuracy: **0.747580**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.74758  |                      0        |  0.764747 |                0        |   0.812782 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.740879 |                     -0.006701 |  0.759003 |               -0.005744 |   0.814233 |                 0.001451 |                        4 |
| Drop + A2 (IN)  |        0.740879 |                     -0.006701 |  0.759669 |               -0.005078 |   0.812931 |                 0.00015  |                        4 |
| Drop + B1 (OUT) |        0.741623 |                     -0.005957 |  0.759529 |               -0.005218 |   0.813869 |                 0.001087 |                        2 |
| Drop + B2 (IN)  |        0.739389 |                     -0.008191 |  0.757953 |               -0.006794 |   0.812962 |                 0.000181 |                        2 |
| Drop + C1 (OUT) |        0.745346 |                     -0.002234 |  0.763485 |               -0.001261 |   0.812931 |                 0.00015  |                        2 |
| Drop + C2 (IN)  |        0.743112 |                     -0.004468 |  0.760915 |               -0.003832 |   0.812572 |                -0.00021  |                        2 |
| Drop + D1       |        0.740879 |                     -0.006701 |  0.76     |               -0.004747 |   0.812936 |                 0.000154 |                        1 |
| Drop + D2       |        0.743857 |                     -0.003723 |  0.763085 |               -0.001661 |   0.813199 |                 0.000417 |                        1 |
| Drop + D3       |        0.746091 |                     -0.001489 |  0.76303  |               -0.001717 |   0.812677 |                -0.000105 |                        1 |
| Drop + D4       |        0.745346 |                     -0.002234 |  0.7625   |               -0.002247 |   0.812735 |                -4.7e-05  |                        1 |
| Drop + D5       |        0.74758  |                      0        |  0.764747 |                0        |   0.812904 |                 0.000123 |                        1 |

### W3 -> W3
Drop Baseline test_accuracy: **0.705138**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.705138 |                      0        |  0.703593 |                0        |   0.791104 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.704393 |                     -0.000745 |  0.703067 |               -0.000526 |   0.790969 |                -0.000135 |                        4 |
| Drop + A2 (IN)  |        0.702159 |                     -0.002978 |  0.70015  |               -0.003443 |   0.790335 |                -0.00077  |                        4 |
| Drop + B1 (OUT) |        0.704393 |                     -0.000745 |  0.702622 |               -0.000971 |   0.790825 |                -0.00028  |                        2 |
| Drop + B2 (IN)  |        0.703649 |                     -0.001489 |  0.702096 |               -0.001497 |   0.790576 |                -0.000528 |                        2 |
| Drop + C1 (OUT) |        0.708116 |                      0.002978 |  0.707463 |                0.00387  |   0.791306 |                 0.000202 |                        2 |
| Drop + C2 (IN)  |        0.703649 |                     -0.001489 |  0.702096 |               -0.001497 |   0.790769 |                -0.000335 |                        2 |
| Drop + D1       |        0.703649 |                     -0.001489 |  0.702541 |               -0.001052 |   0.790976 |                -0.000129 |                        1 |
| Drop + D2       |        0.699926 |                     -0.005212 |  0.697674 |               -0.005918 |   0.790306 |                -0.000799 |                        1 |
| Drop + D3       |        0.703649 |                     -0.001489 |  0.701649 |               -0.001944 |   0.790625 |                -0.000479 |                        1 |
| Drop + D4       |        0.705882 |                      0.000745 |  0.705444 |                0.001851 |   0.791107 |                 2e-06    |                        1 |
| Drop + D5       |        0.706627 |                      0.001489 |  0.705531 |                0.001938 |   0.792164 |                 0.001059 |                        1 |

### W2 -> W3
Drop Baseline test_accuracy: **0.677587**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.677587 |                      0        |  0.678545 |                0        |   0.723366 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.679077 |                      0.001489 |  0.680504 |                0.001959 |   0.723941 |                 0.000575 |                        4 |
| Drop + A2 (IN)  |        0.677587 |                      0        |  0.678545 |                0        |   0.72334  |                -2.7e-05  |                        4 |
| Drop + B1 (OUT) |        0.679077 |                      0.001489 |  0.680504 |                0.001959 |   0.723604 |                 0.000237 |                        2 |
| Drop + B2 (IN)  |        0.679077 |                      0.001489 |  0.68003  |                0.001485 |   0.723595 |                 0.000228 |                        2 |
| Drop + C1 (OUT) |        0.679821 |                      0.002234 |  0.681009 |                0.002464 |   0.723732 |                 0.000366 |                        2 |
| Drop + C2 (IN)  |        0.670886 |                     -0.006701 |  0.671131 |               -0.007414 |   0.722741 |                -0.000626 |                        2 |
| Drop + D1       |        0.677587 |                      0        |  0.678545 |                0        |   0.723402 |                 3.5e-05  |                        1 |
| Drop + D2       |        0.676098 |                     -0.001489 |  0.67706  |               -0.001485 |   0.723832 |                 0.000466 |                        1 |
| Drop + D3       |        0.677587 |                      0        |  0.678545 |                0        |   0.723384 |                 1.8e-05  |                        1 |
| Drop + D4       |        0.679077 |                      0.001489 |  0.679554 |                0.001009 |   0.723408 |                 4.2e-05  |                        1 |
| Drop + D5       |        0.680566 |                      0.002978 |  0.681987 |                0.003442 |   0.723495 |                 0.000129 |                        1 |

## 4. Output Files
- summary: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_summary.csv`
- deltas: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_deltas.csv`
- details: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_details.json`
- report: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_report_zh.md`

