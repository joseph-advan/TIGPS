# ABCD（D 拆成 D1~D5）與 Drop Baseline 比較報告

## 1. 設定
- 本次比較設定：Drop Baseline、A、B、C、D1、D2、D3、D4、D5。
- 三個情境：W2 -> W2、W3 -> W3、W2 -> W3。

| 設定          |   加入特徵數 | 加入特徵                                                                                                                                                                   |
|:--------------|-------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Drop Baseline |            0 |                                                                                                                                                                            |
| Drop + A      |            8 | ip_out_online_friend; ip_in_online_friend; ip_out_online_enemy; ip_in_online_enemy; ip_out_offline_friend; ip_in_offline_friend; ip_out_offline_enemy; ip_in_offline_enemy |
| Drop + B      |            4 | ip_out_friend_total; ip_out_enemy_total; ip_in_friend_total; ip_in_enemy_total                                                                                             |
| Drop + C      |            4 | ip_out_friend_online_minus_offline; ip_out_enemy_online_minus_offline; ip_in_friend_online_minus_offline; ip_in_enemy_online_minus_offline                                 |
| Drop + D1     |            1 | ip_reciprocal_friend_count                                                                                                                                                 |
| Drop + D2     |            1 | ip_reciprocal_enemy_count                                                                                                                                                  |
| Drop + D3     |            1 | ip_liked_by_me_but_enemy_to_me_count                                                                                                                                       |
| Drop + D4     |            1 | ip_enemy_by_me_but_likes_me_count                                                                                                                                          |
| Drop + D5     |            1 | ip_same_target_friend_and_enemy_count                                                                                                                                      |

### D1~D5 定義
| D子組   | 特徵                                  | 說明                                      |
|:--------|:--------------------------------------|:------------------------------------------|
| D1      | ip_reciprocal_friend_count            | 互相提名 friend 的人數                    |
| D2      | ip_reciprocal_enemy_count             | 互相提名 enemy 的人數                     |
| D3      | ip_liked_by_me_but_enemy_to_me_count  | 我提名 friend、對方提名我 enemy 的人數    |
| D4      | ip_enemy_by_me_but_likes_me_count     | 我提名 enemy、對方提名我 friend 的人數    |
| D5      | ip_same_target_friend_and_enemy_count | 同一目標同時被提名 friend 與 enemy 的人數 |

## 2. 各設定平均表現
| 設定          |   mean_test_accuracy |   mean_test_f1 |   mean_test_auc |
|:--------------|---------------------:|---------------:|----------------:|
| Drop Baseline |             0.692152 |       0.711354 |        0.76124  |
| Drop + A      |             0.693162 |       0.712427 |        0.761386 |
| Drop + B      |             0.694423 |       0.713406 |        0.761635 |
| Drop + C      |             0.692405 |       0.711506 |        0.761364 |
| Drop + D1     |             0.693919 |       0.712609 |        0.761173 |
| Drop + D2     |             0.694423 |       0.71341  |        0.761139 |
| Drop + D3     |             0.691143 |       0.710218 |        0.760511 |
| Drop + D4     |             0.693414 |       0.712789 |        0.761166 |
| Drop + D5     |             0.692152 |       0.711668 |        0.761487 |

## 3. 各情境比較（相對 Drop Baseline）
### W2 -> W2
- Drop Baseline accuracy: **0.722937**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added | group_features_added                                                                                                                                                |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Drop Baseline |        0.722937 |                      0        |  0.747586 |                0        |   0.802892 |                 0        |                        0 |                                                                                                                                                                     |
| Drop + A      |        0.727479 |                      0.004542 |  0.752747 |                0.005161 |   0.805641 |                 0.002749 |                        8 | ip_out_online_friend;ip_in_online_friend;ip_out_online_enemy;ip_in_online_enemy;ip_out_offline_friend;ip_in_offline_friend;ip_out_offline_enemy;ip_in_offline_enemy |
| Drop + B      |        0.728993 |                      0.006056 |  0.754121 |                0.006535 |   0.805601 |                 0.00271  |                        4 | ip_out_friend_total;ip_out_enemy_total;ip_in_friend_total;ip_in_enemy_total                                                                                         |
| Drop + C      |        0.723694 |                      0.000757 |  0.748102 |                0.000516 |   0.804874 |                 0.001983 |                        4 | ip_out_friend_online_minus_offline;ip_out_enemy_online_minus_offline;ip_in_friend_online_minus_offline;ip_in_enemy_online_minus_offline                             |
| Drop + D1     |        0.725208 |                      0.002271 |  0.748092 |                0.000505 |   0.802315 |                -0.000577 |                        1 | ip_reciprocal_friend_count                                                                                                                                          |
| Drop + D2     |        0.728236 |                      0.005299 |  0.7519   |                0.004314 |   0.802763 |                -0.000129 |                        1 | ip_reciprocal_enemy_count                                                                                                                                           |
| Drop + D3     |        0.722937 |                      0        |  0.747586 |                0        |   0.802656 |                -0.000235 |                        1 | ip_liked_by_me_but_enemy_to_me_count                                                                                                                                |
| Drop + D4     |        0.725208 |                      0.002271 |  0.749136 |                0.00155  |   0.802938 |                 4.6e-05  |                        1 | ip_enemy_by_me_but_likes_me_count                                                                                                                                   |
| Drop + D5     |        0.722937 |                      0        |  0.747586 |                0        |   0.802834 |                -5.8e-05  |                        1 | ip_same_target_friend_and_enemy_count                                                                                                                               |

### W3 -> W3
- Drop Baseline accuracy: **0.694171**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added | group_features_added                                                                                                                                                |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Drop Baseline |        0.694171 |                      0        |  0.703377 |                0        |   0.765734 |                 0        |                        0 |                                                                                                                                                                     |
| Drop + A      |        0.6919   |                     -0.002271 |  0.700955 |               -0.002422 |   0.765217 |                -0.000517 |                        8 | ip_out_online_friend;ip_in_online_friend;ip_out_online_enemy;ip_in_online_enemy;ip_out_offline_friend;ip_in_offline_friend;ip_out_offline_enemy;ip_in_offline_enemy |
| Drop + B      |        0.694928 |                      0.000757 |  0.703894 |                0.000517 |   0.765288 |                -0.000446 |                        4 | ip_out_friend_total;ip_out_enemy_total;ip_in_friend_total;ip_in_enemy_total                                                                                         |
| Drop + C      |        0.692657 |                     -0.001514 |  0.701909 |               -0.001468 |   0.765592 |                -0.000143 |                        4 | ip_out_friend_online_minus_offline;ip_out_enemy_online_minus_offline;ip_in_friend_online_minus_offline;ip_in_enemy_online_minus_offline                             |
| Drop + D1     |        0.694171 |                      0        |  0.703377 |                0        |   0.766173 |                 0.000439 |                        1 | ip_reciprocal_friend_count                                                                                                                                          |
| Drop + D2     |        0.694171 |                      0        |  0.703377 |                0        |   0.7655   |                -0.000234 |                        1 | ip_reciprocal_enemy_count                                                                                                                                           |
| Drop + D3     |        0.690386 |                     -0.003785 |  0.698155 |               -0.005222 |   0.765058 |                -0.000676 |                        1 | ip_liked_by_me_but_enemy_to_me_count                                                                                                                                |
| Drop + D4     |        0.694928 |                      0.000757 |  0.704762 |                0.001385 |   0.765389 |                -0.000345 |                        1 | ip_enemy_by_me_but_likes_me_count                                                                                                                                   |
| Drop + D5     |        0.695685 |                      0.001514 |  0.705279 |                0.001901 |   0.766532 |                 0.000798 |                        1 | ip_same_target_friend_and_enemy_count                                                                                                                               |

### W2 -> W3
- Drop Baseline accuracy: **0.659349**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added | group_features_added                                                                                                                                                |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Drop Baseline |        0.659349 |                      0        |  0.683099 |                0        |   0.715094 |                 0        |                        0 |                                                                                                                                                                     |
| Drop + A      |        0.660106 |                      0.000757 |  0.68358  |                0.000481 |   0.713301 |                -0.001793 |                        8 | ip_out_online_friend;ip_in_online_friend;ip_out_online_enemy;ip_in_online_enemy;ip_out_offline_friend;ip_in_offline_friend;ip_out_offline_enemy;ip_in_offline_enemy |
| Drop + B      |        0.659349 |                      0        |  0.682203 |               -0.000895 |   0.714016 |                -0.001078 |                        4 | ip_out_friend_total;ip_out_enemy_total;ip_in_friend_total;ip_in_enemy_total                                                                                         |
| Drop + C      |        0.660863 |                      0.001514 |  0.684507 |                0.001408 |   0.713625 |                -0.001469 |                        4 | ip_out_friend_online_minus_offline;ip_out_enemy_online_minus_offline;ip_in_friend_online_minus_offline;ip_in_enemy_online_minus_offline                             |
| Drop + D1     |        0.662377 |                      0.003028 |  0.686357 |                0.003259 |   0.71503  |                -6.4e-05  |                        1 | ip_reciprocal_friend_count                                                                                                                                          |
| Drop + D2     |        0.660863 |                      0.001514 |  0.684951 |                0.001852 |   0.715154 |                 6e-05    |                        1 | ip_reciprocal_enemy_count                                                                                                                                           |
| Drop + D3     |        0.660106 |                      0.000757 |  0.684912 |                0.001814 |   0.713818 |                -0.001276 |                        1 | ip_liked_by_me_but_enemy_to_me_count                                                                                                                                |
| Drop + D4     |        0.660106 |                      0.000757 |  0.684469 |                0.001371 |   0.71517  |                 7.6e-05  |                        1 | ip_enemy_by_me_but_likes_me_count                                                                                                                                   |
| Drop + D5     |        0.657835 |                     -0.001514 |  0.682138 |               -0.000961 |   0.715096 |                 2e-06    |                        1 | ip_same_target_friend_and_enemy_count                                                                                                                               |

## 4. 輸出檔案
- Summary CSV: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abcd_dsplit_vs_drop_baseline_summary.csv`
- Delta CSV: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abcd_dsplit_vs_drop_baseline_deltas.csv`
- Details JSON: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abcd_dsplit_vs_drop_baseline_details.json`
- Markdown 報告: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abcd_dsplit_vs_drop_baseline_report_zh.md`

