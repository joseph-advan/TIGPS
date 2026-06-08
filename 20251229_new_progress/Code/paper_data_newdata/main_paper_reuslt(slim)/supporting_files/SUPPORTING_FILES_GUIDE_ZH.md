# Supporting Files Guide

這個資料夾收納「論文寫作時不一定要第一時間打開，但仍建議保留」的補充檔案。

## 為什麼移到這裡

這些檔案多半是下列類型：

- CSV 版本：和 xlsx 或 md 內容重複，適合程式讀取，不一定適合教授直接看。
- Source index：用來追蹤來源與版本，主文寫作時較少直接引用。
- 詳細 reliability workbook：主文通常使用 summary，詳細表可在教授追問時打開。
- V54 deep dive：是 SEL 拆分的補充佐證，不一定要放在主線。
- 拆開的 Table 1：主文通常用總表，拆開版本留作查證。
- incremental model performance：主線重點是 feature selection，performance 表保留作補充。
- category-level workbook：主線多使用 summary 與 LASSO workbook，完整 workbook 留作補充。

## 檔案說明

| File | Why kept here |
|:--|:--|
| `01_METHOD_data_cleaning_source_index_ZH.md` | Data cleaning source trace, mainly for audit. |
| `01_METHOD_source_index_ZH.md` | Methodology source trace, mainly for audit. |
| `01_METHOD_feature_inventory.csv` | CSV version of feature inventory, useful for scripts. |
| `01_METHOD_feature_inventory.xlsx` | Detailed feature inventory workbook, useful as appendix. |
| `01_METHOD_subscale_definitions_table.csv` | CSV table of subscale definitions. |
| `01_METHOD_cronbach_alpha_reliability.xlsx` | Detailed Cronbach alpha workbook. |
| `01_METHOD_v54_sel_deep_dive_reliability.xlsx` | Detailed V54/SEL reliability deep dive. |
| `01_METHOD_v54_sel_deep_dive_summary.md` | V54/SEL deep dive summary. |
| `02_MODEL_comparison_all_w2w2_w2w3.csv` | CSV version of model comparison. |
| `03_TABLE1_w2_features_to_w2_distress_observed_network.xlsx` | Split Table 1 for W2 -> W2 only. |
| `03_TABLE1_w2_features_to_w3_distress_observed_network.xlsx` | Split Table 1 for W2 -> W3 only. |
| `04_INTERPERSONAL_incremental_model_performance.xlsx` | Performance comparison for interpersonal incremental modeling. |
| `06_CATEGORY_level_interpretation.xlsx` | Full category-level interpretation workbook. |

## 使用建議

- 如果要快速跟教授討論，先看根目錄檔案，不一定要打開這裡。
- 如果教授問「這個結論的來源在哪裡」或「能不能看更細的表」，再打開這個資料夾。
- 如果要交最精簡版本，可以暫時不附這個資料夾；但建議本機保留。
