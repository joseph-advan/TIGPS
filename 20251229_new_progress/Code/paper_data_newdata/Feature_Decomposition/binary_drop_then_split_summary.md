# Binary Baseline: Drop Groups Then Split Groups

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- W2 dropped groups: `v50, v51, v57`
- W3 dropped groups: `49, 50, 55`
- Subscale config: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`
- W2 split groups: `v23, v25, v26, v27, v54`
- W3 split groups: `25, 26, 27, 28, 53`
- W2 direct features: `v52_health`
- Rule: target uses sum-score median split (binary), model is logistic regression.

## Accuracy Across Three Scenarios

| scenario | test_accuracy | cv5_accuracy_mean | test_f1 | test_auc | n_features_used | n_rows_modeling |
|---|---:|---:|---:|---:|---:|---:|
| w2_self | 0.740348 | 0.742085 | 0.761640 | 0.826440 | 31 | 6603 |
| w3_self | 0.679031 | 0.691355 | 0.698006 | 0.752086 | 32 | 6603 |
| w2_predict_w3 | 0.666162 | 0.650768 | 0.685674 | 0.724585 | 31 | 6603 |
