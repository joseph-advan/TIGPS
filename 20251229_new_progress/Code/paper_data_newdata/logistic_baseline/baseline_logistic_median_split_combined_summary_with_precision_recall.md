# Baseline Logistic Median Split: Combined Summary (With Precision/Recall)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is median-split into binary 0/1, modeled with logistic regression.
- Versions included: no-drop and drop-groups.
- Added metrics: precision and recall (train/test/CV).

## No-drop Version

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.740061 | 0.754272 | 0.771409 | 0.752460 | 0.769444 | 0.774825 | 0.772125 | 0.823843 | 0.740266 | 0.753273 | 0.773758 | 0.763302 | 0.818072 | 6603 | 22 |
| w3_self | 0.689890 | 0.693063 | 0.736956 | 0.669947 | 0.674293 | 0.720863 | 0.696801 | 0.744243 | 0.682116 | 0.685985 | 0.730286 | 0.707395 | 0.753279 | 6603 | 24 |
| w2_predict_w3 | 0.655055 | 0.664716 | 0.694854 | 0.667676 | 0.678273 | 0.700719 | 0.689314 | 0.723723 | 0.651221 | 0.662252 | 0.688538 | 0.675041 | 0.710088 | 6603 | 22 |

## Drop-groups Version

- Dropped W2 feature groups: `v50, v51, v52, v57`
- Dropped W3 feature groups: `49, 50, 52, 55`

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.682128 | 0.695307 | 0.735407 | 0.689629 | 0.696268 | 0.756643 | 0.725201 | 0.757234 | 0.682112 | 0.695965 | 0.732929 | 0.713902 | 0.747869 | 6603 | 18 |
| w3_self | 0.687997 | 0.696422 | 0.721483 | 0.678274 | 0.689607 | 0.706475 | 0.697939 | 0.737665 | 0.683935 | 0.692386 | 0.719060 | 0.705392 | 0.747986 | 6603 | 20 |
| w2_predict_w3 | 0.629496 | 0.638570 | 0.681540 | 0.650265 | 0.658936 | 0.694964 | 0.676471 | 0.699246 | 0.631992 | 0.640820 | 0.683655 | 0.661510 | 0.676051 | 6603 | 18 |

## Delta (Drop - No-drop)

- Positive value means drop-groups performs better; negative means worse.

| scenario | delta_test_accuracy_drop_minus_no_drop | delta_test_precision_drop_minus_no_drop | delta_test_recall_drop_minus_no_drop | delta_test_f1_drop_minus_no_drop | delta_test_auc_drop_minus_no_drop | delta_cv5_accuracy_mean_drop_minus_no_drop | delta_cv5_precision_mean_drop_minus_no_drop | delta_cv5_recall_mean_drop_minus_no_drop | delta_cv5_f1_mean_drop_minus_no_drop | delta_cv5_auc_mean_drop_minus_no_drop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | -0.062831 | -0.073177 | -0.018182 | -0.046924 | -0.066609 | -0.058154 | -0.057307 | -0.040829 | -0.049401 | -0.070203 |
| w3_self | 0.008327 | 0.015313 | -0.014388 | 0.001138 | -0.006578 | 0.001819 | 0.006401 | -0.011226 | -0.002003 | -0.005293 |
| w2_predict_w3 | -0.017411 | -0.019337 | -0.005755 | -0.012843 | -0.024477 | -0.019230 | -0.021432 | -0.004883 | -0.013531 | -0.034037 |
