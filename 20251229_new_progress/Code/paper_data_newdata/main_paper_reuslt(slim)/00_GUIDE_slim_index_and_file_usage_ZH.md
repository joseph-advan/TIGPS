# Slim Main Paper Results 檔案索引與使用指南

這個資料夾是論文寫作用的 slim 版本。根目錄只保留最常用的主線檔案；圖檔集中放在 `figures/`；補充查證檔案放在 `supporting_files/`。

## 1. 命名規則

- `00_GUIDE_`：閱讀順序、論文流程、檔案使用說明。
- `01_METHOD_`：資料清理、feature decomposition、feature inventory、Cronbach alpha 摘要。
- `02_MODEL_`：模型表現比較。
- `03_TABLE1_`：Table 1 descriptive group differences。
- `04_INTERPERSONAL_`：interpersonal incremental modeling。
- `05_LASSO_`：LASSO Top 20 與 relative importance。
- `06_CATEGORY_`：category-level interpretation。
- `07_INTERACTION_`：Online Activity interaction analysis。
- `figures/`：所有圖檔與圖檔說明。
- `supporting_files/`：附錄、CSV、source index、詳細 workbook、拆開版本表格。

## 2. 建議閱讀順序

1. `00_GUIDE_paper_analysis_flow_for_advisor_ZH.md`
2. `00_GUIDE_slim_index_and_file_usage_ZH.md`
3. `01_METHOD_feature_inventory_ZH.md`
4. `02_MODEL_comparison_all_w2w2_w2w3.xlsx`
5. `03_TABLE1_group_differences_all.xlsx`
6. `04_INTERPERSONAL_feature_selection_summary.xlsx`
7. `05_LASSO_top20_feature_importance_with_categories.xlsx`
8. `figures/FIGURES_GUIDE_ZH.md`
9. `07_INTERACTION_online_activity_summary_ZH.md`
10. `07_INTERACTION_online_activity_models.xlsx`

## 3. Root 核心檔案清單

### 00 GUIDE

- `00_GUIDE_gender_dummy_coding_update_ZH.md`
- `00_GUIDE_paper_analysis_flow_for_advisor_ZH.md`
- `00_GUIDE_slim_index_and_file_usage_ZH.md`

### 01 METHODS

- `01_METHOD_data_cleaning_detailed_ZH.md`
- `01_METHOD_feature_decomposition_and_reliability_ZH.md`
- `01_METHOD_feature_inventory_ZH.md`
- `01_METHOD_subscale_definitions_record_ZH.md`

### 02 MODEL PERFORMANCE

- `02_MODEL_comparison_all_summary.md`
- `02_MODEL_comparison_all_w2w2_w2w3.xlsx`

### 03 TABLE 1

- `03_TABLE1_group_differences_all.xlsx`
- `03_TABLE1_group_differences_summary.md`

### 04 INTERPERSONAL MODELING

- `04_INTERPERSONAL_feature_selection_summary.xlsx`
- `04_INTERPERSONAL_incremental_modeling_summary.md`

### 05 LASSO TOP 20

- `05_LASSO_top20_feature_importance_summary.md`
- `05_LASSO_top20_feature_importance_with_categories.xlsx`

### 06 CATEGORY INTERPRETATION

- `06_CATEGORY_level_interpretation_summary_ZH.md`

### 07 INTERACTION ANALYSIS

- `07_INTERACTION_online_activity_models.xlsx`
- `07_INTERACTION_online_activity_summary_ZH.md`

## 4. 論文章節對應

| 論文章節 | 主要檔案 | 使用原因 |
|:--|:--|:--|
| Data Cleaning | `01_METHOD_data_cleaning_detailed_ZH.md` | 撰寫 W2/W3 清理、ID 對齊、peer nomination cleaning。 |
| Feature Decomposition | `01_METHOD_feature_decomposition_and_reliability_ZH.md` | 說明題組拆分、50% valid item rule、Cronbach alpha。 |
| Feature Inventory | `01_METHOD_feature_inventory_ZH.md` | 查所有 active predictors、outcome、moderator、interpersonal features。 |
| Subscale Definitions | `01_METHOD_subscale_definitions_record_ZH.md` | 說明各題組拆成哪些 subscales。 |
| Model Performance | `02_MODEL_comparison_all_w2w2_w2w3.xlsx` | 主模型比較表，包含 Logistic、LASSO、Ridge、GraphSAGE。 |
| Table 1 | `03_TABLE1_group_differences_all.xlsx` | W2->W2 與 W2->W3 的 high/low psychological distress group differences 總表。 |
| Interpersonal Modeling | `04_INTERPERSONAL_feature_selection_summary.xlsx` | 看 12 個 interpersonal features 是否被 LASSO 選擇、是否進 Top 20。 |
| LASSO Top 20 | `05_LASSO_top20_feature_importance_with_categories.xlsx` | 主 feature importance 表。 |
| Category Interpretation | `06_CATEGORY_level_interpretation_summary_ZH.md` | Category-level 中文解釋。 |
| Interaction Analysis | `07_INTERACTION_online_activity_models.xlsx` | Online Activity moderation 的完整 b0/b1/b2/b3 結果。 |

## 5. 建議主文圖檔

圖檔都在 `figures/`。請先讀：

- `figures/FIGURES_GUIDE_ZH.md`

主文最優先使用：

- `figures/05_LASSO_fig_category_relative_importance_summary.png`

其他圖可視篇幅放補充資料。

## 6. Supporting files 裡有什麼

`supporting_files/` 內放的是：

- CSV 版本
- source index
- detailed Cronbach alpha workbook
- V54 SEL deep dive
- split Table 1 workbook
- incremental model performance workbook
- category-level interpretation workbook

請先讀：

- `supporting_files/SUPPORTING_FILES_GUIDE_ZH.md`

這些不一定要先給教授，但當教授問細節時可以拿出來。

## 7. 已排除內容

- diagnostics folders
- `.json` diagnostic/detail files
- archive / old snapshot folders
- `__pycache__`
- Python scripts
- `99_archive_or_supplementary` exploratory outputs
