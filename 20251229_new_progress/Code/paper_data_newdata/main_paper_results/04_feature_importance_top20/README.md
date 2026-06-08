# 04_feature_importance_top20

## Purpose

This folder identifies the strongest predictors after the interpersonal incremental modeling step.

The primary analysis now reports two ranking views:

- Model: LASSO Logistic.
- Tasks: `W2 -> W2` and `W2 -> W3`.
- Feature set: drop + decomposition + 12 interpersonal indicators.
- Coefficient-based Top 20: ranked by absolute standardized coefficient at the selected lambda.
- Lambda-entry Top 20: ranked by the regularization strength at which each feature first becomes non-zero on the LASSO path.

## Why This Comes After 03

`03_interpersonal_incremental_modeling` tests whether adding interpersonal features improves model performance.

This folder asks a different question: after adding those features, which predictors actually appear among the strongest LASSO predictors, and what conceptual categories do they represent?

## Outputs

- `outputs/lasso_top20_feature_importance_with_categories.xlsx`: main workbook.
- `outputs/LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md`: interpretation summary.
- `outputs/diagnostics/lasso_top20_feature_importance_diagnostics.json`: generation diagnostics.

## Workbook Sheets

- `LASSO_Top20_Combined`: Top 20 features for both tasks.
- `LASSO_Top20_W2toW2`: W2 -> W2 Top 20.
- `LASSO_Top20_W2toW3`: W2 -> W3 Top 20.
- `Lambda_Top20_Combined`: Lambda-entry Top 20 for both tasks.
- `Lambda_Top20_W2toW2`: W2 -> W2 lambda-entry Top 20.
- `Lambda_Top20_W2toW3`: W2 -> W3 lambda-entry Top 20.
- `Coeff_vs_Lambda_Top20`: side-by-side comparison of coefficient-based and lambda-entry Top 20 lists.
- `LambdaPath_AllFeatures`: entry lambda, entry C, and selected-lambda coefficient for all features.
- `LambdaPath_C_Summary`: number of non-zero features at each C/lambda grid point.
- `CategorySummary`: category-level counts and relative-importance sums.
- `CategorySummaryWide`: side-by-side category summary for both tasks.
- `LambdaCategorySummary`: category-level summary for lambda-entry Top 20.
- `LambdaCategorySummaryWide`: side-by-side lambda-entry category summary for both tasks.
- `SharedTop20`: features appearing in both tasks' Top 20.
- `InterpersonalSummary`: how many interpersonal features were retained, removed, and ranked in Top 20.
- `Ridge_Top20_Reference`: Ridge reference only.
- `Logistic_Top20_Reference`: multivariable logistic reference only.

## Rerun

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\04_feature_importance_top20\run_feature_importance_top20.py"
```

## Interpretation

LASSO is the primary model because it can shrink weak variables to zero. Ridge is useful as a sensitivity reference, but Ridge does not remove variables.

Coefficient-based RI is calculated within each task/model as:

```text
abs(standardized coefficient) / sum(abs(standardized coefficients)) * 100
```

Lambda-entry RI is calculated as:

```text
entry lambda / sum(entry lambda across features in the task) * 100
```

Because scikit-learn uses `C` as inverse regularization strength, lambda is approximated as:

```text
lambda = 1 / C
```

Features with larger entry lambda became non-zero under stronger LASSO regularization and therefore receive stronger lambda-entry ranking.

Category summaries help translate the Top 20 variable list into manuscript-level domains such as SEL/resilience, family/parenting, online/digital life, bullying, and interpersonal network indicators.
