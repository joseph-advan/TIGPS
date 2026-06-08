# 論文寫作檔案使用清單

## 使用原則

本文件整理撰寫論文時，應該從 `main_paper_results` 使用哪些檔案、放在論文哪一段、以及使用原因。

建議原則：

- 主文主要使用 `00` 到 `06` 的最新結果。
- 不建議主文引用 `99_archive_or_supplementary`，除非教授要求補充舊探索分析。
- 不建議使用 `01_model_performance/00_final_comparison_summary` 裡的舊 snapshot，因為最新模型比較已整理在 `01_model_performance/05_model_comparison_all/outputs`。
- `diagnostics`、`json`、程式碼檔案主要作為方法透明性與備查，不一定放入主文。
- `xlsx` 檔案適合整理正式表格；`md` 檔案適合撰寫文字敘述與檢查邏輯；`png` 檔案適合放入圖表或簡報。

## 一、主文必用檔案

### 1. Methodology：資料清理與特徵建構

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Methods: Data Cleaning | `00_methodology_and_data_audit/01_data_cleaning_methods_detailed_ZH.md` | 撰寫資料清理流程 | 說明 W2/W3 清理、ID 對齊、peer nomination 清理、final aligned sample 的形成 |
| Methods: Data Source / Audit Trail | `00_methodology_and_data_audit/02_data_cleaning_source_index_ZH.md` | 查資料清理來源 | 用來確認每個資料清理步驟對應的檔案與輸出，不一定全文放主文 |
| Methods: Feature Decomposition | `00_methodology_and_data_audit/03_feature_decomposition_methods_ZH.md` | 撰寫題組拆分方法 | 說明為什麼拆題組、如何拆 subscales、如何使用 50% valid item rule |
| Methods: Feature Inventory | `00_methodology_and_data_audit/04_feature_inventory_ZH.md` | 列出模型使用特徵 | 用來確認所有 active W2 predictors、outcome、moderator、interpersonal features 的正式名稱與題號 |
| Methods / Supplement: Feature Inventory Table | `00_methodology_and_data_audit/feature_inventory_supporting_files/main_paper_feature_inventory.xlsx` | 製作附錄特徵表 | 可作為正式 feature inventory 附錄，包含題號、中文名、英文名、用途 |
| Methods: Cronbach's alpha | `00_methodology_and_data_audit/feature_decomposition_supporting_files/subscale_cronbach_alpha_reliability.xlsx` | 題組拆分信度佐證 | 用 Cronbach's alpha 支持 feature decomposition 的合理性 |
| Methods: Cronbach's alpha summary | `00_methodology_and_data_audit/feature_decomposition_supporting_files/subscale_cronbach_alpha_reliability_summary.md` | 撰寫信度摘要 | 可快速引用各 subscale 的 reliability 判斷，不需要每次打開 xlsx |
| Methods: Subscale Definitions | `00_methodology_and_data_audit/feature_decomposition_supporting_files/W2_W3_subscale_definitions_record.md` | 列出拆分題組 | 用於說明每個大題組拆成哪些小題組，以及各自中英文名稱 |

建議寫法重點：

- 資料清理先講 W2/W3 student data alignment。
- 接著講 peer nomination cleaning。
- 再講 feature decomposition 與 Cronbach's alpha。
- 最後講 active W2 predictors、outcome、moderator 與 interpersonal features。

### 2. Results: Model Performance Comparison

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Results Table: Model Performance | `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx` | 正式模型比較表 | 整合 Logistic、Decomposed Logistic、LASSO、Ridge、GraphSAGE，在 W2->W2 與 W2->W3 的 AUC、Accuracy、F1 等指標 |
| Results Table: Model Performance CSV | `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.csv` | 快速讀取模型比較數字 | 適合複製數字到論文或做二次整理 |
| Results Text: Model Performance Summary | `01_model_performance/05_model_comparison_all/outputs/MODEL_COMPARISON_ALL_SUMMARY.md` | 撰寫模型結果敘述 | 已整理 GraphSAGE 與 non-GNN 的比較重點 |

主文應該使用這個資料夾的最新總比較，不建議再使用：

- `01_model_performance/00_final_comparison_summary`
- `source_snapshots_previous`
- `old_05_source_index_archive`

這些比較像舊版或歷史備份。

建議主文重點：

- W2 -> W2：GraphSAGE 沒有明顯優於最佳 non-GNN。
- W2 -> W3：GraphSAGE 也沒有優於最佳 non-GNN。
- 因此後續不是強調 GNN 勝出，而是轉向解釋「哪些特徵比較重要」。

### 3. Results: Descriptive Table 1 Group Differences

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Table 1 Main Workbook | `02_descriptive_table1_group_differences/outputs/table1_prediction_aligned_group_differences.xlsx` | Table 1 總表 | 同時包含 W2->W2 與 W2->W3 的 high/low psychological distress group comparisons |
| Table 1 W2->W2 | `02_descriptive_table1_group_differences/outputs/01_w2_features_to_w2_distress/table1_w2_to_w2_observed_network.xlsx` | W2 特徵對 W2 心理困擾 | 橫斷面 group difference table，可觀察當下心理困擾差異 |
| Table 1 W2->W3 | `02_descriptive_table1_group_differences/outputs/02_w2_features_to_w3_distress/table1_w2_to_w3_observed_network.xlsx` | W2 特徵對 W3 心理困擾 | 縱貫 group difference table，可觀察未來心理困擾差異 |
| Table 1 Summary | `02_descriptive_table1_group_differences/outputs/TABLE1_PREDICTION_ALIGNED_GROUP_DIFFERENCES_SUMMARY.md` | 撰寫 Table 1 結果摘要 | 可用來快速描述 p-value、effect size、network features 的差異 |

建議主文重點：

- Table 1 的功能是描述 high vs low psychological distress groups 的差異。
- Interpersonal features 在 W2->W2 中較多達顯著，但到 W2->W3 時減少。
- 這可以支持「同儕提名特徵比較像當下狀態的訊號，縱貫預測力較弱」。

目前已確認：

| Task | Interpersonal p < .05 | Interpersonal p < .01 | 建議解釋 |
|:--|--:|--:|:--|
| W2 -> W2 | 8 / 12 | 5 / 12 | 橫斷面有部分同儕提名差異 |
| W2 -> W3 | 4 / 12 | 4 / 12 | 縱貫預測時，同儕提名差異減弱 |

### 4. Results: Interpersonal Incremental Modeling

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Results: Interpersonal Model Test | `03_interpersonal_incremental_modeling/outputs/interpersonal_incremental_model_performance.xlsx` | 看加入 interpersonal features 後模型表現是否改善 | 用來回答「社交/提名特徵是否增加預測效果」 |
| Results: Interpersonal Feature Selection | `03_interpersonal_incremental_modeling/outputs/interpersonal_feature_selection_summary.xlsx` | 看 12 個 interpersonal features 是否被 LASSO 選到、是否進 Top 20 | 這是支持「interpersonal contribution limited」的核心表 |
| Results Text Summary | `03_interpersonal_incremental_modeling/outputs/INTERPERSONAL_INCREMENTAL_MODELING_SUMMARY.md` | 撰寫結果說明 | 可快速引用 LASSO 選擇數量、Top 20 數量、被剔除的特徵 |

建議主文重點：

- 不只看 Table 1，而是檢查在完整模型裡 interpersonal features 是否仍重要。
- W2->W2：12 個 interpersonal features 中，LASSO 選到 6 個，Top 20 有 2 個。
- W2->W3：12 個 interpersonal features 中，LASSO 選到 4 個，Top 20 有 2 個。
- 這支持 interpersonal network features 有一些訊號，但整體增量有限。

### 5. Results: LASSO Top 20 Feature Importance

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Results: Top 20 Main Workbook | `04_feature_importance_top20/outputs/lasso_top20_feature_importance_with_categories.xlsx` | 正式 Top 20 與 category summary 表 | 主要用來呈現 LASSO Top 20、shared features、category-level summary |
| Results Text: Top 20 Summary | `04_feature_importance_top20/outputs/LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md` | 撰寫 Top 20 結果 | 已包含 relative importance 定義與主要結果 |
| Figure: Category Summary | `04_feature_importance_top20/outputs/figures/lasso_top20_category_relative_importance_summary.png` | 主文圖 | 顯示不同 category 在兩個任務中的 relative importance |
| Figure: W2->W2 Top 20 | `04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w2.png` | 補充圖或主文圖 | 顯示 W2->W2 的 LASSO Top 20 |
| Figure: W2->W3 Top 20 | `04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w3.png` | 補充圖或主文圖 | 顯示 W2->W3 的 LASSO Top 20 |
| Figure: Shared Top 20 | `04_feature_importance_top20/outputs/figures/shared_lasso_top20_relative_importance.png` | 補充圖 | 顯示兩任務共同進入 Top 20 的特徵 |

建議主文重點：

- LASSO Top 20 是論文中解釋「哪些特徵最重要」的核心。
- Relative Importance 是用 `abs(standardized LASSO coefficient) / sum(abs(coefficients)) * 100` 計算。
- SEL / Resilience 是兩個任務中最重要的 category。
- Interpersonal Network 的 relative importance 明顯低於 SEL / Resilience、Online / Digital Life、School Context / Belonging、Family / Parenting。

### 6. Results: Category-Level Interpretation

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Results: Category Interpretation Workbook | `05_category_level_interpretation/outputs/category_level_interpretation.xlsx` | category-level 結果整理 | 可以作為 category interpretation 的正式表 |
| Results Text: Category Interpretation | `05_category_level_interpretation/outputs/CATEGORY_LEVEL_INTERPRETATION_SUMMARY_ZH.md` | 撰寫 domain-level 發現 | 幫你把 LASSO Top 20 轉成論文敘事 |
| Figure: Category Relative Importance | `05_category_level_interpretation/outputs/figures/category_level_relative_importance_bar.png` | 主文圖或補充圖 | 顯示 category-level importance |
| Figure: Domain Story | `05_category_level_interpretation/outputs/figures/domain_story_mean_importance.png` | 補充圖 | 用來視覺化 domain-level story |
| Figure: Interaction Candidates | `05_category_level_interpretation/outputs/figures/top_interaction_candidate_variables.png` | 連接 interaction analysis | 說明為什麼後續選 Top 20 特徵做 interaction |

建議主文重點：

- 04 是「LASSO Top 20 表與圖」。
- 05 是「把 Top 20 轉成概念分類與論文敘事」。
- 如果篇幅有限，主文可以用 04 的圖，05 的內容作為文字解釋來源。

### 7. Results: Online Activity Interaction Analysis

| 使用位置 | 建議使用檔案 | 用途 | 為什麼要用 |
|:--|:--|:--|:--|
| Results: Interaction Main Workbook | `06_interaction_analysis/outputs/teacher_formula_online_activity_interaction_models.xlsx` | 正式 interaction model 結果 | 包含 b0、b1、b2、b3、斜率、OR、p-value、預測機率 |
| Results Text: Interaction Summary | `06_interaction_analysis/outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md` | 撰寫 interaction 結果 | 目前只列 p < .05 的主要 interaction，適合直接轉寫 |
| Results: Combined Interaction Workbook | `06_interaction_analysis/outputs/teacher_formula_interaction_models_combined.xlsx` | 備查 | 若未來增加 moderator，可以看 combined version；目前主文主要用 online activity |
| Results Text: Combined Summary | `06_interaction_analysis/outputs/TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md` | 備查 | 總摘要，不一定放主文 |

建議主文重點：

- Interaction analysis 是接在 LASSO Top 20 後面。
- 目的不是再做模型比較，而是找數位情境下的保護因子。
- 目前顯著結果是 W2->W3 的 `Family Cohesion and Support x High Online Activity`。
- 解釋方式要保守：家庭支持與較低未來心理困擾風險相關，且此關聯在 high online activity group 中更強。

## 二、建議主文表格與圖表配置

### Table 1

使用：

- `02_descriptive_table1_group_differences/outputs/table1_prediction_aligned_group_differences.xlsx`
- 或拆成：
  - `01_w2_features_to_w2_distress/table1_w2_to_w2_observed_network.xlsx`
  - `02_w2_features_to_w3_distress/table1_w2_to_w3_observed_network.xlsx`

建議呈現：

- High Psychological Distress
- Low Psychological Distress
- Total
- p-value
- between-group difference / effect size

用途：

- 描述樣本與高低心理困擾組差異。
- 為後續模型分析提供背景。

### Table 2

使用：

- `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx`

建議呈現：

- Task
- Model
- Feature Set
- AUC
- Accuracy
- F1
- Precision
- Recall

用途：

- 展示 GNN vs non-GNN 的模型表現。
- 支持「GraphSAGE 沒有明顯優於線性模型」。

### Table 3

使用：

- `03_interpersonal_incremental_modeling/outputs/interpersonal_feature_selection_summary.xlsx`

建議呈現：

- Task
- Interpersonal feature
- Selected by LASSO
- Top 20 by Abs Std. B
- Relative Importance %
- Rank

用途：

- 說明 interpersonal features 在模型中的實際保留情況。
- 支持「同儕提名特徵增量貢獻有限」。

### Table 4

使用：

- `04_feature_importance_top20/outputs/lasso_top20_feature_importance_with_categories.xlsx`

建議呈現：

- LASSO Top 20
- Feature Code
- Variable
- Category
- Std. B
- Relative Importance %
- Direction

用途：

- 展示最重要的預測特徵。
- 連接 category-level interpretation。

### Table 5

使用：

- `06_interaction_analysis/outputs/teacher_formula_online_activity_interaction_models.xlsx`
- `06_interaction_analysis/outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md`

建議呈現：

- Task
- Feature
- b1
- b2
- b3
- b3 p-value
- Slope when Moderator=0
- Slope when Moderator=1
- OR Slope Moderator=0
- OR Slope Moderator=1

用途：

- 呈現 Online Activity moderation。
- 支持「Family Cohesion 在 high online activity group 中保護性關聯更強」。

## 三、建議主文圖表

### Figure 1: Model Performance Comparison

可使用資料：

- `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx`

目前沒有獨立圖檔，但可以用 workbook 自行畫 bar chart。

建議圖意：

- x 軸：model
- y 軸：AUC 或 Accuracy
- 分組：W2->W2、W2->W3

用途：

- 清楚展示 GraphSAGE 沒有明顯優於 Logistic / LASSO / Ridge。

### Figure 2: Category-Level Relative Importance

直接使用：

- `04_feature_importance_top20/outputs/figures/lasso_top20_category_relative_importance_summary.png`

用途：

- 展示 SEL / Resilience 是最主要 category。
- 展示 Interpersonal Network 的 relative importance 較小。

### Figure 3: LASSO Top 20 by Task

直接使用：

- `04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w2.png`
- `04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w3.png`

用途：

- 展示兩個任務各自的 Top 20 特徵。

### Figure 4: Shared Top 20 Predictors

直接使用：

- `04_feature_importance_top20/outputs/figures/shared_lasso_top20_relative_importance.png`

用途：

- 強調哪些變項在 W2->W2 與 W2->W3 都穩定重要。

### Figure 5: Category-Level Interpretation

可選擇使用：

- `05_category_level_interpretation/outputs/figures/category_level_relative_importance_bar.png`
- `05_category_level_interpretation/outputs/figures/domain_story_mean_importance.png`

用途：

- 如果 04 的圖已經足夠，05 的圖可以放補充資料。
- 如果想把論文故事講得更清楚，可以用 05 的 domain story 圖。

## 四、附錄或備查使用檔案

### 方法透明性備查

| 檔案 | 建議用途 |
|:--|:--|
| `00_methodology_and_data_audit/METHODOLOGY_SOURCE_INDEX_ZH.md` | 方法來源索引，適合自己查，不一定放主文 |
| `00_methodology_and_data_audit/feature_decomposition_supporting_files/binary_drop_then_split_summary.md` | feature decomposition 對模型表現的補充說明 |
| `00_methodology_and_data_audit/feature_decomposition_supporting_files/v54_sel_deep_dive_reliability.xlsx` | 若教授問 V54 怎麼拆，可作為補充佐證 |
| `00_methodology_and_data_audit/feature_decomposition_supporting_files/v54_sel_deep_dive_reliability_summary.md` | V54 deep dive 摘要 |

### 模型細節備查

| 檔案 | 建議用途 |
|:--|:--|
| `01_model_performance/01_logistic_original_groups/outputs/logistic_original_groups_performance.xlsx` | 若要拆開說明 original group logistic |
| `01_model_performance/02_logistic_decomposed_groups/outputs/logistic_decomposed_groups_performance.xlsx` | 若要拆開說明 decomposed logistic |
| `01_model_performance/03_ridge_lasso_regularized/outputs/ridge_lasso_regularized_performance.xlsx` | 若要拆開說明 Ridge/LASSO model performance |
| `01_model_performance/04_graphsage_gnn/outputs/graphsage_gnn_performance.xlsx` | 若要拆開說明 GraphSAGE performance |
| `01_model_performance/03_ridge_lasso_regularized/outputs/ridge_lasso_three_scenarios_relative_importance.csv` | 舊的 Ridge/LASSO importance 參考，目前主文建議以 04 LASSO Top 20 為主 |

### Diagnostics 備查

以下檔案不建議放主文，但可以用於檢查結果是否正確：

- `02_descriptive_table1_group_differences/outputs/diagnostics/table1_prediction_aligned_group_differences_diagnostics.json`
- `03_interpersonal_incremental_modeling/outputs/interpersonal_incremental_modeling_diagnostics.json`
- `04_feature_importance_top20/outputs/diagnostics/lasso_top20_feature_importance_diagnostics.json`
- `05_category_level_interpretation/outputs/diagnostics/category_level_interpretation_diagnostics.json`
- `06_interaction_analysis/outputs/diagnostics/teacher_formula_online_activity_interaction_diagnostics.json`

## 五、不建議放入主文的內容

### 1. `99_archive_or_supplementary`

這裡主要是舊探索、備用分析或目前不是主線的內容。除非教授要求，不建議放進主文主結果。

其中可以備查的有：

- `99_archive_or_supplementary/08_family_online_2x2_risk_test`

這個可以作為 interaction finding 的補充，但目前主文建議先用 06 的 teacher-formula interaction model。

### 2. `01_model_performance/00_final_comparison_summary`

這裡有些舊版 summary 與 snapshot。最新模型比較應該使用：

- `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx`

### 3. `__pycache__`

完全不需要放入論文或交給教授。

### 4. 舊版 source snapshots

以下資料夾是歷史備份，不建議主文引用：

- `01_model_performance/00_final_comparison_summary/source_snapshots_previous`
- `01_model_performance/00_final_comparison_summary/old_05_source_index_archive`

## 六、main_paper_results 以外建議保留引用的檔案

雖然主文結果主要來自 `main_paper_results`，但下面這些檔案在寫方法或確認題目時仍重要。

| 檔案 | 用途 |
|:--|:--|
| `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv` | W2 final cleaned student data |
| `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv` | W3 final cleaned student data |
| `Data/otherData/論文使用之題組正式名稱.csv` | 題組正式中英文名稱來源 |
| `Data/2024data/00_W2_學生問卷題目列表.csv` | W2 原始問卷題目內容確認 |
| `Data/2025data/00_W3_學生問卷題目列表.csv` | W3 原始問卷題目內容確認 |
| `DOCS/大專生研究計畫書_蔡加恩 (7).docx` | 初始研究動機與計畫背景參考 |
| `DOCS/論文邏輯檢查_20260520_v1.txt` | 你原本整理的分析敘事草稿 |
| `DOCS/論文邏輯檢查_20260520_teacher_v1.txt` | 目前較接近正式論文流程的老師版整理 |

這些檔案可以用來寫背景與方法，但主結果建議仍以 `main_paper_results` 的最新 outputs 為準。

## 七、建議最終交給教授的檔案包

如果要整理一包給教授看，建議最少包含：

1. `PAPER_ANALYSIS_FLOW_FOR_ADVISOR_ZH.md`
2. `THESIS_FILE_USAGE_GUIDE_ZH.md`
3. `00_methodology_and_data_audit/04_feature_inventory_ZH.md`
4. `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx`
5. `02_descriptive_table1_group_differences/outputs/table1_prediction_aligned_group_differences.xlsx`
6. `03_interpersonal_incremental_modeling/outputs/interpersonal_feature_selection_summary.xlsx`
7. `04_feature_importance_top20/outputs/lasso_top20_feature_importance_with_categories.xlsx`
8. `04_feature_importance_top20/outputs/figures/lasso_top20_category_relative_importance_summary.png`
9. `06_interaction_analysis/outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md`
10. `06_interaction_analysis/outputs/teacher_formula_online_activity_interaction_models.xlsx`

如果教授想看完整方法，再補：

1. `00_methodology_and_data_audit/01_data_cleaning_methods_detailed_ZH.md`
2. `00_methodology_and_data_audit/03_feature_decomposition_methods_ZH.md`
3. `00_methodology_and_data_audit/feature_decomposition_supporting_files/subscale_cronbach_alpha_reliability.xlsx`
4. `00_methodology_and_data_audit/feature_decomposition_supporting_files/W2_W3_subscale_definitions_record.md`

## 八、建議論文主文引用順序

建議主文 Results 順序如下：

1. Model performance comparison
   - 使用 `01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx`

2. Descriptive group differences
   - 使用 `02_descriptive_table1_group_differences/outputs/table1_prediction_aligned_group_differences.xlsx`

3. Interpersonal incremental modeling
   - 使用 `03_interpersonal_incremental_modeling/outputs/interpersonal_feature_selection_summary.xlsx`

4. LASSO Top 20 feature importance
   - 使用 `04_feature_importance_top20/outputs/lasso_top20_feature_importance_with_categories.xlsx`
   - 使用 `04_feature_importance_top20/outputs/figures/lasso_top20_category_relative_importance_summary.png`

5. Category-level interpretation
   - 使用 `05_category_level_interpretation/outputs/CATEGORY_LEVEL_INTERPRETATION_SUMMARY_ZH.md`
   - 視篇幅決定是否放 `05_category_level_interpretation/outputs/figures/category_level_relative_importance_bar.png`

6. Interaction analysis
   - 使用 `06_interaction_analysis/outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md`
   - 使用 `06_interaction_analysis/outputs/teacher_formula_online_activity_interaction_models.xlsx`

## 九、目前應補充或注意的地方

### 1. Model performance 可以補一張正式圖

目前 `01_model_performance` 有正式表格，但沒有 model performance 圖。如果教授希望視覺化，可以再用 `model_comparison_all_w2w2_w2w3.xlsx` 畫 AUC / Accuracy bar chart。

### 2. Table 1 主文可能不需要列全部變項

Table 1 很大。主文可以放精簡版，完整版放 appendix。

建議主文強調：

- Demographics
- SEL / Resilience
- Family / Parenting
- Online / Digital Life
- School Context / Belonging
- Interpersonal Network summary

### 3. Interpersonal features 的結論要保守

不要寫：

> 同儕網絡不影響心理狀態。

建議寫：

> 在目前模型與 observed peer nomination feature 設定下，同儕網絡特徵提供的額外預測貢獻有限，且縱貫預測訊號弱於個人、家庭、學校與數位生活特徵。

### 4. Interaction analysis 不要過度因果化

不要寫：

> 家庭支持會保護高線上活動學生。

建議寫：

> 家庭支持與較低未來高心理困擾風險相關，且此負向關聯在 high online activity group 中更強。
