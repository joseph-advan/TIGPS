# Baseline: Logistic Regression on Median-Split Target (No Subscale Splitting)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is split by median into 0/1; logistic regression predicts this binary target.

## Classification Summary

| scenario | train_accuracy | test_accuracy | test_f1 | test_auc | cv5_accuracy_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.744927 | 0.757295 | 0.777850 | 0.820486 | 0.744270 | 0.765811 | 0.820455 | 7023 | 23 |
| w3_self | 0.734247 | 0.707473 | 0.719836 | 0.787829 | 0.727321 | 0.732842 | 0.806155 | 7023 | 23 |
| w2_predict_w3 | 0.673015 | 0.656228 | 0.653763 | 0.723444 | 0.667240 | 0.672513 | 0.730958 | 7023 | 23 |
