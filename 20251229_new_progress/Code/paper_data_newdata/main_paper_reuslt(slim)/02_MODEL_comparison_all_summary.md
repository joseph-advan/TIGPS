# All Model Performance Comparison

This folder compares all model-performance outputs generated under `01_model_performance`.

## Included Models

- Original-group Logistic baseline: non-decomposed/original questionnaire groups. This is the only place where no-drop is intentionally reported.
- Decomposed Logistic baseline: drop + decomposition features.
- LASSO Logistic and Ridge Logistic: regularized models with drop + decomposition features.
- GraphSAGE: GNN using drop + decomposition node features and peer nomination graph edges. No no-drop GNN version is run or reported.

## Important Metric Note

Logistic, LASSO, and Ridge rows use CV5 mean metrics in the main `AUC`, `Accuracy`, `F1`, `Precision`, and `Recall` columns. GraphSAGE uses 5-seed held-out test mean metrics, not CV5 folds.

## Key Deltas

| Task     |   GraphSAGE AUC |   Best non-GNN AUC | Best non-GNN AUC model            |   GraphSAGE minus best non-GNN AUC |   GraphSAGE F1 |   Best non-GNN F1 | Best non-GNN F1 model             |   GraphSAGE minus best non-GNN F1 |   Decomposed Logistic AUC |   GraphSAGE minus Decomposed Logistic AUC |
|:---------|----------------:|-------------------:|:----------------------------------|-----------------------------------:|---------------:|------------------:|:----------------------------------|----------------------------------:|--------------------------:|------------------------------------------:|
| W2 -> W2 |          0.8187 |             0.8229 | Original-group Logistic (no drop) |                            -0.0042 |         0.7562 |            0.7691 | Original-group Logistic (no drop) |                           -0.0129 |                     0.819 |                                   -0.0003 |
| W2 -> W3 |          0.6974 |             0.7141 | Original-group Logistic (no drop) |                            -0.0167 |         0.6549 |            0.6805 | Original-group Logistic (no drop) |                           -0.0256 |                     0.71  |                                   -0.0126 |

Output workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\01_model_performance\05_model_comparison_all\outputs\model_comparison_all_w2w2_w2w3.xlsx`
