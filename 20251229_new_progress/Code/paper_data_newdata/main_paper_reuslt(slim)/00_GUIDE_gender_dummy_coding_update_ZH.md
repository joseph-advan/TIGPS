# Gender Dummy Coding Update

## Reason
Gender should not be treated as a continuous 1/2 numeric predictor in prediction models. The model-ready feature set now uses an explicit binary dummy variable so the coefficient is interpretable as a male-versus-female contrast.

## Coding Rule
- W2 source item: `v1`
- W3 source item: `1`
- Original cleaned-data coding: `1 = Female`, `2 = Male`
- Model-ready dummy coding: `Female = 0`, `Male = 1`
- W2 model column: `feature_v1_male`
- W3 model column: `feature_1_male`
- Original-group baseline model column: `group_v1_male` for W2 feature models

## Files Updated
- `Feature_Decomposition/build_binary_drop_then_split_baseline.py`
- `logistic_baseline/build_logistic_median_split_combined_with_precision_recall.py`
- `tables/scripts/build_table2_table3_drop_decomposition.py`
- `tables/table1/scripts/build_table1_drop_decomposition.py`
- `main_paper_results/04_feature_importance_top20/run_feature_importance_top20.py`

## Outputs Rerun
- `main_paper_results/01_model_performance`
- `main_paper_results/02_descriptive_table1_group_differences`
- `main_paper_results/03_interpersonal_incremental_modeling`
- `main_paper_results/04_feature_importance_top20`
- `Feature_Decomposition` baseline summary outputs

## Interpretation
In logistic-style models, a negative coefficient for `Gender: Male (vs Female)` means male students have lower predicted odds or risk score for high psychological distress than female students, holding the other included predictors constant.

In Table 1, gender remains presented descriptively as two categories, Female and Male, while internally using the corrected dummy-coded feature source.
