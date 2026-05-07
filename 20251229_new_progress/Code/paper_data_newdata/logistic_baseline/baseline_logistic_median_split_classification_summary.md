# Baseline: Logistic Regression on Median-Split Target (No Subscale Splitting)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is split by median into 0/1; logistic regression predicts this binary target.

## Classification Summary

| scenario | train_accuracy | test_accuracy | test_f1 | test_auc | cv5_accuracy_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w2_self | 0.740061 | 0.752460 | 0.772125 | 0.823843 | 0.740266 | 0.763302 | 0.818072 | 6603 | 22 |
| w3_self | 0.689890 | 0.669947 | 0.696801 | 0.744243 | 0.682116 | 0.707395 | 0.753279 | 6603 | 24 |
| w2_predict_w3 | 0.655055 | 0.667676 | 0.689314 | 0.723723 | 0.651221 | 0.675041 | 0.710088 | 6603 | 22 |
