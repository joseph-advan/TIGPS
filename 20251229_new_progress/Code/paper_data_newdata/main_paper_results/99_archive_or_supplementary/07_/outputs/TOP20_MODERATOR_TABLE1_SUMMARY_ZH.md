# Top20 Moderator Table 1 Summary

## 目的

這個 07 分析針對 04 的 LASSO Top20 特徵，建立以 moderator 高低組為分組依據的 Table 1。

## 四張 Table 1

- `W2 -> W2`：依 W2 Problematic Internet Use 高低組比較 Top20 特徵。
- `W2 -> W3`：依 W2 Problematic Internet Use 高低組比較 Top20 特徵。
- `W2 -> W2`：依 W2 Online Activity 高低組比較 Top20 特徵。
- `W2 -> W3`：依 W2 Online Activity 高低組比較 Top20 特徵。

## 統計呈現

- 每個特徵以 `mean (SD)` 呈現。
- p-value 使用 Welch t-test。
- Between-group difference 使用 Cohen's d，方向是 High group mean - Low group mean。
- Binary 0/1 特徵也以 mean(SD) 呈現，mean 可視為比例。

## 注意事項

`v28` 是 Problematic Internet Use 高低組的分組依據，因此在 PIU Table 1 中不作為 focal feature 比較，已記錄在 `SkippedFeatures`。

## Outputs

- Combined workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\07_\outputs\top20_moderator_table1_combined.xlsx`
- W2toW2_PIU: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\07_\outputs\table1_w2_to_w2_by_problematic_internet_use_top20.xlsx`
- W2toW3_PIU: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\07_\outputs\table1_w2_to_w3_by_problematic_internet_use_top20.xlsx`
- W2toW2_OnlineActivity: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\07_\outputs\table1_w2_to_w2_by_online_activity_top20.xlsx`
- W2toW3_OnlineActivity: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\07_\outputs\table1_w2_to_w3_by_online_activity_top20.xlsx`
