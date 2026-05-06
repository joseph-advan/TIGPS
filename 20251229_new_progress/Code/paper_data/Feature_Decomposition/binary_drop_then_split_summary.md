# Binary Baseline: Drop Groups Then Split Groups

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver10.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- W2 dropped groups: `v50, v51, v52, v57`
- W3 dropped groups: `49, 50, 52, 55`
- W2 split groups: `v23, v25, v26, v27, v54`
- Rule: target uses sum-score median split (binary), model is logistic regression.

## Accuracy Across Three Scenarios

| scenario | test_accuracy | cv5_accuracy_mean | test_f1 | test_auc | n_features_used | n_rows_modeling |
|---|---:|---:|---:|---:|---:|---:|
| w2_self | 0.740214 | 0.732590 | 0.760656 | 0.805433 | 27 | 7023 |
| w3_self | 0.684698 | 0.697704 | 0.698844 | 0.752752 | 19 | 7023 |
| w2_predict_w3 | 0.663345 | 0.665816 | 0.661417 | 0.722023 | 27 | 7023 |
