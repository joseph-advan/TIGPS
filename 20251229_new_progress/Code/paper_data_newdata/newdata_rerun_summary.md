# paper_data_newdata 重跑摘要

更新日期：2026-05-06

## 這次使用的資料

- W2 student data: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv`
- W3 student data: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv`
- W2/W3 共同 ID 表: `Code/paper_data_newdata/features_used/w2_ver6_w3_ver5_common_student_ids.csv`
- Interpersonal / GNN roster: 使用 final aligned roster，共 6603 人。

這次的分析採用「只分析兩年都有資料的共同 student_id」策略。因此 W2 與 W3 的模型、提名 edge、GNN node roster 都固定在同一批 6603 名學生上。

## 是否需要共同 ID 表

需要。

原因是 W2/W3 現在所有跨年度比較、W2 預測 W3、Interpersonal network、GNN node set 都應該使用同一個 paired sample。共同 ID 表可以作為後續所有腳本的固定 cohort 定義，避免不同分析各自用不同的 row filtering 規則，導致結果無法直接比較。

## 已重跑並覆蓋的分析

### Feature Decomposition

腳本：

- `Feature_Decomposition/build_binary_drop_then_split_baseline.py`

主要結果：

| Scenario | N | Accuracy | F1 | AUC |
|---|---:|---:|---:|---:|
| W2 self | 6603 | 0.7199 | 0.7448 | 0.7897 |
| W3 self | 6603 | 0.6783 | 0.6979 | 0.7377 |
| W2 predict W3 | 6603 | 0.6495 | 0.6733 | 0.7112 |

相較舊資料，樣本數由 7023 變成 6603。三個 scenario 的 accuracy / AUC 大致下降，主要是 final aligned cohort 較嚴格。

### Logistic Baseline

腳本：

- `logistic_baseline/build_logistic_median_split_combined_with_precision_recall.py`
- `logistic_baseline/build_logistic_median_split_baseline_drop_groups.py`
- `logistic_baseline/build_regression_median_split_baseline.py`

主要結果：

| Scenario | N | Accuracy | F1 | AUC |
|---|---:|---:|---:|---:|
| W2 self | 6603 | 0.7525 | 0.7721 | 0.8238 |
| W3 self | 6603 | 0.6699 | 0.6968 | 0.7442 |
| W2 predict W3 | 6603 | 0.6677 | 0.6893 | 0.7237 |

另一組 drop-groups legacy 設定結果：

| Scenario | N | Accuracy | F1 | AUC |
|---|---:|---:|---:|---:|
| W2 self | 6603 | 0.6896 | 0.7252 | 0.7572 |
| W3 self | 6603 | 0.6783 | 0.6979 | 0.7377 |
| W2 predict W3 | 6603 | 0.6503 | 0.6765 | 0.6992 |

相較舊資料，樣本數由 6713 變成 6603。部分 W2 與 W2 predict W3 logistic 指標上升，W3 self 指標下降。

### Interpersonal Features

腳本：

- `Interpersonal_features/run_interpersonal_feature_logistic_comparison.py`
- `Interpersonal_features/run_interpersonal_abcd_dsplit_comparison.py`
- `Interpersonal_features/run_interpersonal_a1a2_b1b2_c1c2_d1d5_comparison.py`
- `Interpersonal_features/run_interpersonal_abdg_group_comparison.py`

核心設定：

- roster 使用 W2 final aligned roster 的 `school_id`, `class`, `v13`。
- W2 edge 用 W2 cleaned nomination 欄位。
- W3 edge 用 W3 cleaned nomination 欄位。
- 自我提名已在資料清理階段轉空白。
- 同一題組重複提名只保留第一次，其餘轉空白。

核心 comparison 部分主要結果：

| Scenario | Setting | N | Accuracy | F1 | AUC |
|---|---|---:|---:|---:|---:|
| W2 predict W3 | baseline_drop | 6603 | 0.6593 | 0.6831 | 0.7151 |
| W2 predict W3 | baseline_drop_plus_interpersonal | 6603 | 0.6601 | 0.6858 | 0.7117 |
| W2 predict W3 | baseline_no_drop | 6603 | 0.6662 | 0.6866 | 0.7291 |
| W2 predict W3 | baseline_no_drop_plus_interpersonal | 6603 | 0.6631 | 0.6873 | 0.7261 |
| W2 predict W3 | interpersonal_only | 6603 | 0.5291 | 0.6836 | 0.5536 |
| W2 self | baseline_drop | 6603 | 0.7229 | 0.7476 | 0.8029 |
| W2 self | baseline_drop_plus_interpersonal | 6603 | 0.7328 | 0.7554 | 0.8049 |

整體看，Interpersonal features 對 W2 self 有小幅幫助；對 W2 predict W3 的幫助較不穩定，baseline_no_drop 仍是較強設定。

### GNN Baseline

腳本：

- `GNN_baseline/run_graphsage_three_tasks.py`
- `GNN_baseline/run_graphsage_edge_type_comparison.py`

GraphSAGE three-task 主要結果：

| Scenario | Nodes | Edges | Features | Accuracy mean | F1 mean | AUC mean |
|---|---:|---:|---:|---:|---:|---:|
| W2 predict W3 | 6603 | 37759 | 117 | 0.6327 | 0.6541 | 0.6883 |
| W2 self | 6603 | 37759 | 117 | 0.7210 | 0.7402 | 0.7884 |
| W3 self | 6603 | 35759 | 119 | 0.6837 | 0.6955 | 0.7500 |

Edge type comparison 中，W2 predict W3 的 untyped baseline AUC 約 0.6883；friend-only 約 0.6868；enemy-only 約 0.6780。就目前結果看，單靠 edge type 拆分沒有明顯超越 untyped baseline。

### Ridge / Lasso

腳本：

- `Ridge_lasso/run_ridge_lasso_shap_three_scenarios.py`

主要結果：

| Scenario | N | Accuracy range | F1 range | AUC range |
|---|---:|---:|---:|---:|
| W2 predict W2 | 6603 | 0.7176-0.7214 | 0.7436-0.7462 | 0.7995-0.8032 |
| W2 predict W3 | 6603 | 0.6942-0.7002 | 0.6897-0.7005 | 0.7599-0.7610 |
| W3 predict W3 | 6603 | 0.6934-0.6942 | 0.7034-0.7072 | 0.7636-0.7657 |

相較舊資料，樣本數由 6713 變成 6603。W2 predict W3 的 AUC 略高，W2/W3 self 類 scenario 多數略低。

### Online Activity x Depression

腳本：

- `online_activity_x_depression/run_online_activity_x_depression.py`

Stage 1 main effects 主要結果：

| Analysis | Low N | High N | Mean diff high-low | p-value | Cohen's d |
|---|---:|---:|---:|---:|---:|
| W2 activity main | 3511 | 3035 | 0.1657 | 1.13e-18 | -0.2220 |
| W2 nomination out main | 3579 | 3024 | 0.0917 | 8.63e-07 | -0.1226 |
| W2 nomination in main | 2864 | 3739 | -0.0341 | 0.0667 | 0.0455 |
| W2 nomination total main | 2884 | 3719 | -0.0055 | 0.7659 | 0.0074 |
| W3 activity main | 3617 | 2986 | 0.0602 | 0.0016 | -0.0789 |
| W3 nomination out main | 3474 | 3129 | 0.0187 | 0.3192 | -0.0245 |
| W3 nomination in main | 3069 | 3522 | 0.0250 | 0.1833 | -0.0328 |
| W3 nomination total main | 2997 | 3594 | 0.0097 | 0.6068 | -0.0127 |

整體看，online activity 與 depressive symptom 的差異在 W2 較明顯，在 W3 仍顯著但效果較小。Nomination out 在 W2 顯著，W3 不顯著。

## 舊資料比較

已產生比較報告：

- `Code/paper_data_newdata/newdata_vs_old_paper_data_comparison.md`
- `Code/paper_data_newdata/newdata_vs_old_paper_data_comparison_summary.json`

整體差異：

- 新資料分析全部固定使用 6603 名 W2/W3 aligned student_id。
- 舊分析多數使用 6713 或 7023 人，依腳本而異。
- 新資料的結果因為 cohort 較嚴格，很多 accuracy / AUC 會略降；但部分 W2 predict W3 的 logistic 與 Ridge/Lasso 指標反而略升。
- Interpersonal / GNN 的 network node set 現在已一致化，不再混用較大的舊 roster。

## 舊路徑檢查

目前會實際重跑的 `.py` 腳本已改成使用新的 W2/W3 cleaned data。

仍然保留舊路徑的檔案只有：

- `new_data_rerun_inventory.md`
- `data_cleaning_audit/*`

這些是歷史紀錄與 audit 文件，不是目前分析腳本。
