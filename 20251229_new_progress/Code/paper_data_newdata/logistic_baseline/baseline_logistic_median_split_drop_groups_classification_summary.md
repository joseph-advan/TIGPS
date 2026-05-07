# Baseline: Logistic Regression on Median-Split Target (Drop Groups Version)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Dropped W2 feature groups: `v50, v51, v52, v57`
- Dropped W3 feature groups: `49, 50, 52, 55`
- Rule: target score is split by median into 0/1; logistic regression predicts this binary target.

## Classification Summary

| scenario | train_accuracy | test_accuracy | test_f1 | test_auc | cv5_accuracy_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.682128 | 0.689629 | 0.725201 | 0.757234 | 0.682112 | 0.713902 | 0.747869 | 6603 | 18 |
| w3_self | 0.687997 | 0.678274 | 0.697939 | 0.737665 | 0.683935 | 0.705392 | 0.747986 | 6603 | 20 |
| w2_predict_w3 | 0.629496 | 0.650265 | 0.676471 | 0.699246 | 0.631992 | 0.661510 | 0.676051 | 6603 | 18 |
