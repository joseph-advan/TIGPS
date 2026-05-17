# 04_feature_importance_top20

## 目的

這個資料夾用來整理 LASSO Top 20 feature importance。

主要分析：

- 模型：LASSO Logistic。
- 任務：`W2 -> W2`、`W2 -> W3`。
- 特徵版本：drop + decomposition + 12 interpersonal indicators。
- 排名依據：standardized coefficient 的絕對值。

## 跟 03 的關係

`03_interpersonal_incremental_modeling` 問的是：加入 12 個 interpersonal features 以後，模型表現有沒有變好。

`04_feature_importance_top20` 問的是：在加入這些特徵後，真正進入 LASSO Top 20 的重要變項是誰，以及它們屬於哪些概念類別。

## 主要輸出

- `outputs/lasso_top20_feature_importance_with_categories.xlsx`：主要 workbook。
- `outputs/LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md`：摘要與解讀。
- `outputs/diagnostics/lasso_top20_feature_importance_diagnostics.json`：產生紀錄。

## 解讀原則

LASSO 是主模型，因為 LASSO 可以把較弱的變項係數壓成 0，因此可以解釋為 feature selection。

Ridge 只是參考，因為 Ridge 不會剔除變項，只會縮小係數。

Relative Importance % 的意思是：

```text
abs(standardized coefficient) / 所有 features 的 abs(standardized coefficient) 總和 * 100
```

Category summary 是為了把 Top 20 從單一變項層次整理成論文可以解釋的概念類別，例如 SEL/resilience、family/parenting、online/digital life、bullying、interpersonal network。
