# Baseline: Logistic 3-Class (33/67 Quantile Split)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is total sum, split into 3 classes by q33/q67, then modeled by multinomial logistic regression.

## Summary

| scenario | q33 | q67 | test_accuracy | test_macro_f1 | test_macro_auc_ovr | cv5_accuracy_mean | cv5_macro_f1_mean | cv5_macro_auc_ovr_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 15.0000 | 21.0000 | 0.570819 | 0.563834 | 0.763502 | 0.587355 | 0.577925 | 0.768920 | 7023 | 23 |
| w3_self | 15.0000 | 23.0000 | 0.575089 | 0.575429 | 0.759972 | 0.574257 | 0.574402 | 0.761583 | 7023 | 23 |
| w2_predict_w3 | 15.0000 | 23.0000 | 0.496085 | 0.495756 | 0.672756 | 0.507616 | 0.508181 | 0.690038 | 7023 | 23 |
