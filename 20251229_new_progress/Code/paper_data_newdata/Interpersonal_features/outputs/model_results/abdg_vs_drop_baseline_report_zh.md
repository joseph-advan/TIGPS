# ABDG 人際特徵實驗報告（以 Drop Baseline 為基準）

## 1. 實驗設定
- 基準模型：Drop Baseline。
- 比較模型：Drop + A、Drop + B、Drop + D、Drop + G、Drop + ABDG。
- 三個任務：W2 -> W2、W3 -> W3、W2 -> W3。

### A/B/D/G 組別定義
| 組別   | 說明                 |   欄位數 | 欄位                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:-------|:---------------------|---------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A      | 基本提名 in/out 次數 |        8 | ip_out_online_friend; ip_in_online_friend; ip_out_online_enemy; ip_in_online_enemy; ip_out_offline_friend; ip_in_offline_friend; ip_out_offline_enemy; ip_in_offline_enemy                                                                                                                                                                                                                                                                                                                                                                                                    |
| B      | friend/enemy 合計    |        4 | ip_out_friend_total; ip_out_enemy_total; ip_in_friend_total; ip_in_enemy_total                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| D      | online-offline 差值  |        4 | ip_out_friend_online_minus_offline; ip_out_enemy_online_minus_offline; ip_in_friend_online_minus_offline; ip_in_enemy_online_minus_offline                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| G      | 互惠/衝突次數        |        5 | ip_reciprocal_friend_count; ip_reciprocal_enemy_count; ip_liked_by_me_but_enemy_to_me_count; ip_enemy_by_me_but_likes_me_count; ip_same_target_friend_and_enemy_count                                                                                                                                                                                                                                                                                                                                                                                                         |
| ABDG   | A+B+D+G 合併         |       21 | ip_out_online_friend; ip_in_online_friend; ip_out_online_enemy; ip_in_online_enemy; ip_out_offline_friend; ip_in_offline_friend; ip_out_offline_enemy; ip_in_offline_enemy; ip_out_friend_total; ip_out_enemy_total; ip_in_friend_total; ip_in_enemy_total; ip_out_friend_online_minus_offline; ip_out_enemy_online_minus_offline; ip_in_friend_online_minus_offline; ip_in_enemy_online_minus_offline; ip_reciprocal_friend_count; ip_reciprocal_enemy_count; ip_liked_by_me_but_enemy_to_me_count; ip_enemy_by_me_but_likes_me_count; ip_same_target_friend_and_enemy_count |

## 2. 整體平均（跨三任務）
| 設定          |   mean_test_accuracy |   mean_test_f1 |   mean_test_auc |
|:--------------|---------------------:|---------------:|----------------:|
| Drop + B      |             0.694423 |       0.713406 |        0.761635 |
| Drop + G      |             0.693666 |       0.713066 |        0.761522 |
| Drop + A      |             0.693162 |       0.712427 |        0.761386 |
| Drop + ABDG   |             0.692909 |       0.712805 |        0.761004 |
| Drop + D      |             0.692405 |       0.711506 |        0.761364 |
| Drop Baseline |             0.692152 |       0.711354 |        0.76124  |

## 3. 各任務比較（依 test_accuracy 由高到低）
### W2 -> W2
- Drop Baseline accuracy: **0.722937**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop + B      |        0.728993 |                      0.006056 |  0.754121 |                0.006535 |   0.805601 |                 0.00271  |                        4 |
| Drop + ABDG   |        0.728993 |                      0.006056 |  0.753103 |                0.005517 |   0.804886 |                 0.001994 |                       21 |
| Drop + G      |        0.728236 |                      0.005299 |  0.7519   |                0.004314 |   0.804708 |                 0.001816 |                        5 |
| Drop + A      |        0.727479 |                      0.004542 |  0.752747 |                0.005161 |   0.805641 |                 0.002749 |                        8 |
| Drop + D      |        0.723694 |                      0.000757 |  0.748102 |                0.000516 |   0.804874 |                 0.001983 |                        4 |
| Drop Baseline |        0.722937 |                      0        |  0.747586 |                0        |   0.802892 |                 0        |                        0 |

### W3 -> W3
- Drop Baseline accuracy: **0.694171**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop + B      |        0.694928 |                      0.000757 |  0.703894 |                0.000517 |   0.765288 |                -0.000446 |                        4 |
| Drop Baseline |        0.694171 |                      0        |  0.703377 |                0        |   0.765734 |                 0        |                        0 |
| Drop + G      |        0.693414 |                     -0.000757 |  0.702425 |               -0.000953 |   0.765851 |                 0.000117 |                        5 |
| Drop + D      |        0.692657 |                     -0.001514 |  0.701909 |               -0.001468 |   0.765592 |                -0.000143 |                        4 |
| Drop + A      |        0.6919   |                     -0.002271 |  0.700955 |               -0.002422 |   0.765217 |                -0.000517 |                        8 |
| Drop + ABDG   |        0.6919   |                     -0.002271 |  0.701394 |               -0.001983 |   0.766104 |                 0.00037  |                       21 |

### W2 -> W3
- Drop Baseline accuracy: **0.659349**
| 設定          |   test_accuracy |   delta_test_accuracy_vs_drop |   test_f1 |   delta_test_f1_vs_drop |   test_auc |   delta_test_auc_vs_drop |   n_group_features_added |
|:--------------|----------------:|------------------------------:|----------:|------------------------:|-----------:|-------------------------:|-------------------------:|
| Drop + D      |        0.660863 |                      0.001514 |  0.684507 |                0.001408 |   0.713625 |                -0.001469 |                        4 |
| Drop + A      |        0.660106 |                      0.000757 |  0.68358  |                0.000481 |   0.713301 |                -0.001793 |                        8 |
| Drop Baseline |        0.659349 |                      0        |  0.683099 |                0        |   0.715094 |                 0        |                        0 |
| Drop + B      |        0.659349 |                      0        |  0.682203 |               -0.000895 |   0.714016 |                -0.001078 |                        4 |
| Drop + G      |        0.659349 |                      0        |  0.684874 |                0.001775 |   0.714007 |                -0.001087 |                        5 |
| Drop + ABDG   |        0.657835 |                     -0.001514 |  0.683916 |                0.000817 |   0.712021 |                -0.003073 |                       21 |

## 4. 重點結論
- 可以直接看每個任務中，`delta_test_accuracy_vs_drop` 為正的組別代表比 drop baseline 好。
- `Drop + ABDG` 是四組合併版本；請和單組 A/B/D/G 對照，看是否有疊加效果。
- 如果多數任務中 `Drop + ABDG` 仍低於 baseline，表示四組一起加的噪音可能大於增益。

## 5. 產出檔案
- 摘要：`C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abdg_vs_drop_baseline_summary.csv`
- 差異：`C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abdg_vs_drop_baseline_deltas.csv`
- 明細：`C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abdg_vs_drop_baseline_details.json`
- 本報告：`C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Interpersonal_features\outputs\model_results\abdg_vs_drop_baseline_report_zh.md`

