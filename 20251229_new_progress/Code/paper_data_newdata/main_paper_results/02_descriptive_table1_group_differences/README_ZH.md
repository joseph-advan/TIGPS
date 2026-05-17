# 02_descriptive_table1_group_differences

## 目的

這個資料夾現在改成跟預測任務對齊的 Table 1 描述性比較。

主設計：

- `W2 -> W2`：用 W2 baseline features，比較 W2 高心理困擾 vs 低心理困擾。
- `W2 -> W3`：用 W2 baseline features，比較 W3 高心理困擾 vs 低心理困擾。

這裡不再放 `W3 features -> W3 distress`，因為它不是 baseline prediction 的邏輯。

## 人際網絡特徵版本

每一個 prediction task 都會產生兩版：

- Observed network：未除以班級人數的原始人際提名指標。
- Class-adjusted network：把 count 類型的人際提名指標除以同班有填問卷人數 minus one。

這樣可以檢查「有沒有做班級調整」是否會改變 Table 1 的描述性結果。

## 如何重跑

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\02_descriptive_table1_group_differences\run_descriptive_table1_group_differences.py"
```

## 主要輸出

- `outputs/01_w2_features_to_w2_distress`：W2 features by W2 distress，包含 observed 與 class-adjusted network 兩版。
- `outputs/02_w2_features_to_w3_distress`：W2 features by W3 distress，包含 observed 與 class-adjusted network 兩版。
- `outputs/table1_prediction_aligned_group_differences.xlsx`：整合後 workbook。
- `outputs/TABLE1_PREDICTION_ALIGNED_GROUP_DIFFERENCES_SUMMARY.md`：簡要結果摘要。
- `outputs/diagnostics`：重跑紀錄與診斷。

## 解讀原則

Table 1 是描述性比較，不是因果模型。

- `p-value`：檢查高低心理困擾兩組在該變項上是否有差異。
- `Between-group difference`：差異大小。類別變項使用 Cramer's V，連續/量表變項使用 Cohen's d。
- `W2 -> W3` 的 Table 1 是後續 longitudinal feature importance 與 interaction analysis 的主要描述性銜接。
