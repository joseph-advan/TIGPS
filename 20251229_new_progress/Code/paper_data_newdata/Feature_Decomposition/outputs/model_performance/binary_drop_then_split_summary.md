# Binary Baseline: Drop Groups Then Split Groups

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- W2 dropped groups: `v50, v51, v52_health, v57`
- Subscale config: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`
- W2 split groups: `v23, v25, v26, v27, v54`
- W2 direct features: `v52_health`
- Current scope: W2 predictors only; scenarios are `w2_self` and `w2_predict_w3`.
- Rule: target uses sum-score median split (binary), model is logistic regression.

- Main metrics are CV5 means: mean test-set metrics across 5 stratified cross-validation folds.

## Baseline Drop Version Before Splitting

This section uses the drop version feature set, without decomposing configured groups into subscales.

| scenario | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | test_accuracy | test_precision | test_recall | test_f1 | test_auc | n_features_used | n_rows_modeling |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.715733 | 0.732756 | 0.747473 | 0.739975 | 0.790897 | 0.725208 | 0.744444 | 0.749650 | 0.747038 | 0.798772 | 19 | 6603 |
| w2_predict_w3 | 0.641833 | 0.654398 | 0.676461 | 0.665211 | 0.698156 | 0.656321 | 0.668061 | 0.689209 | 0.678470 | 0.712138 | 19 | 6603 |


## Drop Version After Splitting Groups

This section starts from the same drop version, then splits configured groups into subscales.

| scenario | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | test_accuracy | test_precision | test_recall | test_f1 | test_auc | n_features_used | n_rows_modeling |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.736481 | 0.756044 | 0.757818 | 0.756863 | 0.810315 | 0.743376 | 0.759669 | 0.769231 | 0.764420 | 0.818706 | 30 | 6603 |
| w2_predict_w3 | 0.649556 | 0.662747 | 0.679914 | 0.671205 | 0.707296 | 0.657835 | 0.671368 | 0.684892 | 0.678063 | 0.718475 | 30 | 6603 |


## Difference: Split Minus Baseline

Positive value means the split version performs better than the baseline drop version.

| scenario | delta_cv5_accuracy_mean_split_minus_baseline | delta_cv5_precision_mean_split_minus_baseline | delta_cv5_recall_mean_split_minus_baseline | delta_cv5_f1_mean_split_minus_baseline | delta_cv5_auc_mean_split_minus_baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| w2_self | 0.020748 | 0.023289 | 0.010346 | 0.016888 | 0.019418 |
| w2_predict_w3 | 0.007724 | 0.008349 | 0.003453 | 0.005994 | 0.009140 |

