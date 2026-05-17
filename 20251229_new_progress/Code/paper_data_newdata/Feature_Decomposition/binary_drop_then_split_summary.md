# Binary Baseline: Drop Groups Then Split Groups

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- W2 dropped groups: `v50, v51, v52_health, v57`
- W3 dropped groups: `49, 50, 51, 55`
- Subscale config: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`
- W2 split groups: `v23, v25, v26, v27, v54`
- W3 split groups: `25, 26, 27, 28, 53`
- W2 direct features: `v52_health`
- Rule: target uses sum-score median split (binary), model is logistic regression.

- Main metrics are CV5 means: mean test-set metrics across 5 stratified cross-validation folds.

## Baseline Drop Version Before Splitting

This section uses the drop version feature set, without decomposing configured groups into subscales.

| scenario | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | test_accuracy | test_precision | test_recall | test_f1 | test_auc | n_features_used | n_rows_modeling |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.715733 | 0.732756 | 0.747473 | 0.739975 | 0.790897 | 0.725208 | 0.744444 | 0.749650 | 0.747038 | 0.798772 | 19 | 6603 |
| w3_self | 0.650011 | 0.660609 | 0.688267 | 0.674045 | 0.711898 | 0.661620 | 0.676136 | 0.684892 | 0.680486 | 0.717921 | 20 | 6603 |
| w2_predict_w3 | 0.641833 | 0.654398 | 0.676461 | 0.665211 | 0.698156 | 0.656321 | 0.668061 | 0.689209 | 0.678470 | 0.712138 | 19 | 6603 |


## Drop Version After Splitting Groups

This section starts from the same drop version, then splits configured groups into subscales.

| scenario | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | test_accuracy | test_precision | test_recall | test_f1 | test_auc | n_features_used | n_rows_modeling |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.733755 | 0.752286 | 0.757819 | 0.754988 | 0.810818 | 0.738834 | 0.753425 | 0.769231 | 0.761246 | 0.815948 | 30 | 6603 |
| w3_self | 0.663489 | 0.675966 | 0.692006 | 0.683819 | 0.729364 | 0.657078 | 0.675362 | 0.670504 | 0.672924 | 0.735974 | 31 | 6603 |
| w2_predict_w3 | 0.649708 | 0.663599 | 0.677898 | 0.670652 | 0.707362 | 0.658592 | 0.672805 | 0.683453 | 0.678087 | 0.718068 | 30 | 6603 |


## Difference: Split Minus Baseline

Positive value means the split version performs better than the baseline drop version.

| scenario | delta_cv5_accuracy_mean_split_minus_baseline | delta_cv5_precision_mean_split_minus_baseline | delta_cv5_recall_mean_split_minus_baseline | delta_cv5_f1_mean_split_minus_baseline | delta_cv5_auc_mean_split_minus_baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.018022 | 0.019530 | 0.010347 | 0.015013 | 0.019921 |
| w3_self | 0.013477 | 0.015357 | 0.003739 | 0.009774 | 0.017466 |
| w2_predict_w3 | 0.007875 | 0.009201 | 0.001437 | 0.005441 | 0.009206 |

