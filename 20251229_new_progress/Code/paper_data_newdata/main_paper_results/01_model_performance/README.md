# 01 Model Performance

## Purpose

This folder contains runnable, manuscript-facing model-performance analyses for the main paper.

## Version Rule

Only the original Logistic baseline reports a no-drop version. All later models use the current drop + decomposition feature design.

- `01_logistic_original_groups`: original/non-decomposed Logistic baseline, including no-drop and drop-groups versions.
- `02_logistic_decomposed_groups`: plain Logistic using drop + decomposition features.
- `03_ridge_lasso_regularized`: LASSO and Ridge using drop + decomposition features.
- `04_graphsage_gnn`: GraphSAGE using drop + decomposition node features and peer nomination graph edges. No no-drop GNN is run or reported.
- `05_model_comparison_all`: integrated comparison across all model families.

## Main Tasks

- `W2 -> W2`: W2 predictors classify W2 high psychological distress.
- `W2 -> W3`: W2 predictors classify W3 high psychological distress.

## Recommended Reading Order

1. Open `05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.xlsx` for the integrated result.
2. Use folders `01` to `04` only when you need model-specific outputs or reruns.
3. Use `03_interpersonal_incremental_modeling` outside this folder for the next step: testing whether 12 interpersonal indicators add predictive value.
