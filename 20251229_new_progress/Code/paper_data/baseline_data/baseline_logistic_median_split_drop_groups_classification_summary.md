# Baseline: Logistic Regression on Median-Split Target (Drop Groups Version)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Dropped W2 feature groups: `v50, v51, v52, v57`
- Dropped W3 feature groups: `49, 50, 52, 55`
- Rule: target score is split by median into 0/1; logistic regression predicts this binary target.

## Classification Summary

| scenario | train_accuracy | test_accuracy | test_f1 | test_auc | cv5_accuracy_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.711997 | 0.720996 | 0.742782 | 0.784406 | 0.710949 | 0.737089 | 0.777671 | 7023 | 19 |
| w3_self | 0.700961 | 0.684698 | 0.698844 | 0.752752 | 0.697704 | 0.706002 | 0.768045 | 7023 | 19 |
| w2_predict_w3 | 0.651477 | 0.635587 | 0.637907 | 0.703792 | 0.648729 | 0.654675 | 0.709049 | 7023 | 19 |
