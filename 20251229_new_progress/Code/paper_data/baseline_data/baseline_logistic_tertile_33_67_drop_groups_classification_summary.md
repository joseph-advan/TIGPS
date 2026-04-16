# Baseline: Logistic 3-Class (33/67 Quantile Split, Drop Groups Version)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Dropped W2 feature groups: `v50, v51, v52, v57`
- Dropped W3 feature groups: `49, 50, 52, 55`
- Rule: target score is total sum, split into 3 classes by q33/q67, then modeled by multinomial logistic regression.

## Summary

| scenario | q33 | q67 | test_accuracy | test_macro_f1 | test_macro_auc_ovr | cv5_accuracy_mean | cv5_macro_f1_mean | cv5_macro_auc_ovr_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 15.0000 | 21.0000 | 0.537367 | 0.526458 | 0.724337 | 0.534101 | 0.521839 | 0.725252 | 7023 | 19 |
| w3_self | 15.0000 | 23.0000 | 0.540214 | 0.541676 | 0.732452 | 0.538659 | 0.539368 | 0.730007 | 7023 | 19 |
| w2_predict_w3 | 15.0000 | 23.0000 | 0.474021 | 0.470561 | 0.654433 | 0.486687 | 0.484221 | 0.666580 | 7023 | 19 |
