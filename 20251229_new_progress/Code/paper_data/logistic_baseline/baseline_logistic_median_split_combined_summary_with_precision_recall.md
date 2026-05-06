# Baseline Logistic Median Split: Combined Summary (With Precision/Recall)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver13.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver11.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is median-split into binary 0/1, modeled with logistic regression.
- Versions included: no-drop and drop-groups.
- Added metrics: precision and recall (train/test/CV).

## No-drop Version

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.745810 | 0.756766 | 0.780496 | 0.733433 | 0.745333 | 0.769972 | 0.757453 | 0.806607 | 0.742738 | 0.756196 | 0.773971 | 0.764761 | 0.819856 | 6713 | 23 |
| w3_self | 0.727188 | 0.731556 | 0.732894 | 0.732688 | 0.739645 | 0.732064 | 0.735835 | 0.807127 | 0.727245 | 0.732597 | 0.730974 | 0.731689 | 0.805261 | 6713 | 23 |
| w2_predict_w3 | 0.673557 | 0.680945 | 0.674716 | 0.661206 | 0.670149 | 0.657394 | 0.663710 | 0.720686 | 0.668704 | 0.675344 | 0.672139 | 0.673573 | 0.729489 | 6713 | 23 |

## Drop-groups Version

- Dropped W2 feature groups: `v50, v51, v52, v57`
- Dropped W3 feature groups: `49, 50, 52, 55`

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.712849 | 0.724274 | 0.756720 | 0.718541 | 0.732620 | 0.754821 | 0.743555 | 0.781449 | 0.709069 | 0.721947 | 0.750820 | 0.735997 | 0.777482 | 6713 | 19 |
| w3_self | 0.703352 | 0.705184 | 0.716795 | 0.681310 | 0.685590 | 0.689605 | 0.687591 | 0.755231 | 0.695666 | 0.697676 | 0.709315 | 0.703394 | 0.767840 | 6713 | 19 |
| w2_predict_w3 | 0.654004 | 0.660198 | 0.659715 | 0.638124 | 0.649469 | 0.626647 | 0.637854 | 0.700135 | 0.652318 | 0.658696 | 0.657788 | 0.658096 | 0.708412 | 6713 | 19 |

## Delta (Drop - No-drop)

- Positive value means drop-groups performs better; negative means worse.

| scenario | delta_test_accuracy_drop_minus_no_drop | delta_test_precision_drop_minus_no_drop | delta_test_recall_drop_minus_no_drop | delta_test_f1_drop_minus_no_drop | delta_test_auc_drop_minus_no_drop | delta_cv5_accuracy_mean_drop_minus_no_drop | delta_cv5_precision_mean_drop_minus_no_drop | delta_cv5_recall_mean_drop_minus_no_drop | delta_cv5_f1_mean_drop_minus_no_drop | delta_cv5_auc_mean_drop_minus_no_drop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | -0.014892 | -0.012713 | -0.015152 | -0.013898 | -0.025157 | -0.033669 | -0.034249 | -0.023152 | -0.028765 | -0.042374 |
| w3_self | -0.051378 | -0.054055 | -0.042460 | -0.048244 | -0.051896 | -0.031579 | -0.034920 | -0.021658 | -0.028295 | -0.037421 |
| w2_predict_w3 | -0.023083 | -0.020680 | -0.030747 | -0.025856 | -0.020551 | -0.016386 | -0.016648 | -0.014351 | -0.015477 | -0.021077 |
