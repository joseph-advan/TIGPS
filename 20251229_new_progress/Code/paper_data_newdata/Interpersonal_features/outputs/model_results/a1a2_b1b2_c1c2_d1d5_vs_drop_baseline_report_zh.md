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
| Drop Baseline   |             0.692152 |       0.711354 |        0.76124  |
| Drop + A1 (OUT) |             0.692657 |       0.711966 |        0.76188  |
| Drop + A2 (IN)  |             0.693414 |       0.712246 |        0.760941 |
| Drop + B1 (OUT) |             0.693414 |       0.71263  |        0.761772 |
| Drop + B2 (IN)  |             0.693919 |       0.71284  |        0.761108 |
| Drop + C1 (OUT) |             0.690134 |       0.709661 |        0.761062 |
| Drop + C2 (IN)  |             0.694171 |       0.713076 |        0.76164  |
| Drop + D1       |             0.693919 |       0.712609 |        0.761173 |
| Drop + D2       |             0.694423 |       0.71341  |        0.761139 |
| Drop + D3       |             0.691143 |       0.710218 |        0.760511 |
| Drop + D4       |             0.693414 |       0.712789 |        0.761166 |
| Drop + D5       |             0.692152 |       0.711668 |        0.761487 |

## 3. Scenario Details
### W2 -> W2
Drop Baseline test_accuracy: **0.722937**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.722937 |                      0        |  0.747586 |                0        |   0.802892 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.730507 |                      0.00757  |  0.753804 |                0.006217 |   0.804854 |                 0.001962 |                        4 |
| Drop + A2 (IN)  |        0.726722 |                      0.003785 |  0.751206 |                0.00362  |   0.803808 |                 0.000916 |                        4 |
| Drop + B1 (OUT) |        0.728993 |                      0.006056 |  0.75242  |                0.004834 |   0.804473 |                 0.001581 |                        2 |
| Drop + B2 (IN)  |        0.728993 |                      0.006056 |  0.753444 |                0.005857 |   0.803963 |                 0.001071 |                        2 |
| Drop + C1 (OUT) |        0.720666 |                     -0.002271 |  0.74499  |               -0.002597 |   0.802883 |                -9e-06    |                        2 |
| Drop + C2 (IN)  |        0.725965 |                      0.003028 |  0.750345 |                0.002759 |   0.804932 |                 0.00204  |                        2 |
| Drop + D1       |        0.725208 |                      0.002271 |  0.748092 |                0.000505 |   0.802315 |                -0.000577 |                        1 |
| Drop + D2       |        0.728236 |                      0.005299 |  0.7519   |                0.004314 |   0.802763 |                -0.000129 |                        1 |
| Drop + D3       |        0.722937 |                      0        |  0.747586 |                0        |   0.802656 |                -0.000235 |                        1 |
| Drop + D4       |        0.725208 |                      0.002271 |  0.749136 |                0.00155  |   0.802938 |                 4.6e-05  |                        1 |
| Drop + D5       |        0.722937 |                      0        |  0.747586 |                0        |   0.802834 |                -5.8e-05  |                        1 |

### W3 -> W3
Drop Baseline test_accuracy: **0.694171**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.694171 |                      0        |  0.703377 |                0        |   0.765734 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.6919   |                     -0.002271 |  0.701394 |               -0.001983 |   0.766091 |                 0.000356 |                        4 |
| Drop + A2 (IN)  |        0.692657 |                     -0.001514 |  0.701471 |               -0.001907 |   0.765038 |                -0.000696 |                        4 |
| Drop + B1 (OUT) |        0.694171 |                      0        |  0.703812 |                0.000435 |   0.765932 |                 0.000198 |                        2 |
| Drop + B2 (IN)  |        0.693414 |                     -0.000757 |  0.702425 |               -0.000953 |   0.765109 |                -0.000625 |                        2 |
| Drop + C1 (OUT) |        0.692657 |                     -0.001514 |  0.702782 |               -0.000596 |   0.765642 |                -9.2e-05  |                        2 |
| Drop + C2 (IN)  |        0.694928 |                      0.000757 |  0.703894 |                0.000517 |   0.765693 |                -4.1e-05  |                        2 |
| Drop + D1       |        0.694171 |                      0        |  0.703377 |                0        |   0.766173 |                 0.000439 |                        1 |
| Drop + D2       |        0.694171 |                      0        |  0.703377 |                0        |   0.7655   |                -0.000234 |                        1 |
| Drop + D3       |        0.690386 |                     -0.003785 |  0.698155 |               -0.005222 |   0.765058 |                -0.000676 |                        1 |
| Drop + D4       |        0.694928 |                      0.000757 |  0.704762 |                0.001385 |   0.765389 |                -0.000345 |                        1 |
| Drop + D5       |        0.695685 |                      0.001514 |  0.705279 |                0.001901 |   0.766532 |                 0.000798 |                        1 |

### W2 -> W3
Drop Baseline test_accuracy: **0.659349**

| setting_label   |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:----------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop Baseline   |        0.659349 |                      0        |  0.683099 |                0        |   0.715094 |                 0        |                        0 |
| Drop + A1 (OUT) |        0.655564 |                     -0.003785 |  0.680702 |               -0.002397 |   0.714696 |                -0.000398 |                        4 |
| Drop + A2 (IN)  |        0.660863 |                      0.001514 |  0.684062 |                0.000963 |   0.713977 |                -0.001117 |                        4 |
| Drop + B1 (OUT) |        0.657078 |                     -0.002271 |  0.681658 |               -0.00144  |   0.714913 |                -0.000182 |                        2 |
| Drop + B2 (IN)  |        0.659349 |                      0        |  0.682652 |               -0.000447 |   0.714253 |                -0.000841 |                        2 |
| Drop + C1 (OUT) |        0.657078 |                     -0.002271 |  0.68121  |               -0.001888 |   0.71466  |                -0.000434 |                        2 |
| Drop + C2 (IN)  |        0.66162  |                      0.002271 |  0.684989 |                0.001891 |   0.714297 |                -0.000798 |                        2 |
| Drop + D1       |        0.662377 |                      0.003028 |  0.686357 |                0.003259 |   0.71503  |                -6.4e-05  |                        1 |
| Drop + D2       |        0.660863 |                      0.001514 |  0.684951 |                0.001852 |   0.715154 |                 6e-05    |                        1 |
| Drop + D3       |        0.660106 |                      0.000757 |  0.684912 |                0.001814 |   0.713818 |                -0.001276 |                        1 |
| Drop + D4       |        0.660106 |                      0.000757 |  0.684469 |                0.001371 |   0.71517  |                 7.6e-05  |                        1 |
| Drop + D5       |        0.657835 |                     -0.001514 |  0.682138 |               -0.000961 |   0.715096 |                 2e-06    |                        1 |

## 4. Output Files
- summary: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_summary.csv`
- deltas: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_deltas.csv`
- details: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_details.json`
- report: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_report_zh.md`

