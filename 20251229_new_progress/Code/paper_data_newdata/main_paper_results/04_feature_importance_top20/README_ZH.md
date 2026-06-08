# 04_feature_importance_top20

## 目的

這個資料夾接在 `03_interpersonal_incremental_modeling` 之後，用來整理 LASSO 模型中最重要的 Top 20 特徵。

目前同時保留兩種排序方式：

- Coefficient-based Top 20：使用 selected lambda 下的 standardized coefficient 絕對值排序。
- Lambda-entry Top 20：使用 LASSO path 中，特徵第一次變成 non-zero 的 lambda 強度排序。

## 主要設定

- Model：LASSO Logistic。
- Tasks：`W2 -> W2` 與 `W2 -> W3`。
- Feature set：drop + decomposition + 12 observed interpersonal indicators。

## 主要輸出

- `outputs/lasso_top20_feature_importance_with_categories.xlsx`：主要 workbook。
- `outputs/LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md`：結果摘要。
- `outputs/diagnostics/lasso_top20_feature_importance_diagnostics.json`：產生紀錄。

## 重要 Sheet

- `LASSO_Top20_Combined`：coefficient-based Top 20。
- `LASSO_Top20_W2toW2`：W2 -> W2 coefficient-based Top 20。
- `LASSO_Top20_W2toW3`：W2 -> W3 coefficient-based Top 20。
- `Lambda_Top20_Combined`：lambda-entry Top 20。
- `Lambda_Top20_W2toW2`：W2 -> W2 lambda-entry Top 20。
- `Lambda_Top20_W2toW3`：W2 -> W3 lambda-entry Top 20。
- `Coeff_vs_Lambda_Top20`：兩種 Top 20 排序的並排比較。
- `LambdaPath_AllFeatures`：每個特徵的 entry lambda、entry C、selected-lambda coefficient。
- `LambdaPath_C_Summary`：每個 C/lambda grid point 下有幾個 non-zero features。
- `CategorySummary` / `CategorySummaryWide`：coefficient-based category summary。
- `LambdaCategorySummary` / `LambdaCategorySummaryWide`：lambda-entry category summary。
- `InterpersonalSummary`：人際網絡特徵被 LASSO 保留、移除、進 Top20 的狀況。

## RI 定義

Coefficient-based RI：

```text
abs(standardized coefficient) / sum(abs(standardized coefficients)) * 100
```

Lambda-entry RI：

```text
entry lambda / sum(entry lambda across features in the task) * 100
```

因為 scikit-learn 使用 `C` 作為 inverse regularization strength，所以這裡用：

```text
lambda = 1 / C
```

解讀上，越早在強 regularization 下變成 non-zero 的特徵，`entry lambda` 越大，lambda-entry 排名越前面。

## 重跑方式

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\04_feature_importance_top20\run_feature_importance_top20.py"
```
