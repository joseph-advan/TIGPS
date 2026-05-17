# 05 Model Comparison All

## Purpose

This folder integrates all model-performance outputs generated under `01_model_performance`.

## Included Model Families

- Original-group Logistic baseline.
- Decomposed Logistic baseline.
- LASSO Logistic.
- Ridge Logistic.
- GraphSAGE GNN.

## Main Output

- `outputs/model_comparison_all_w2w2_w2w3.xlsx`
- `outputs/MODEL_COMPARISON_ALL_SUMMARY.md`

## Interpretation

The main comparison is designed to answer whether GraphSAGE clearly outperforms simpler Logistic/Ridge/LASSO models. Current results do not show a clear GraphSAGE advantage, which motivates the next analysis step: testing whether interpersonal network indicators add incremental predictive value and whether they appear in the LASSO Top 20 feature-importance results.
