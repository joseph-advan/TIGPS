# Baseline Logistic Median Split: Combined Summary (With Precision/Recall)

- W2 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Rule: target score is median-split into binary 0/1, modeled with logistic regression.
- Versions included in this single integrated report: no-drop and drop-groups.
- Added metrics: precision and recall (train/test/CV).

## Important W2 `v52` Note

- In W2, self-rated health is the scalar column `v52`; in this rerun it is modeled as direct feature `v52_health`.
- The drop-groups version drops `v52_health`, so it drops W2 self-rated health (`v52`).
- W2 Self-Worth / Positive Self-Concept is a separate group using `v52_1`, `v52_2`, and `v52_3`; these items are **not** dropped by the current drop-groups version.

## No-drop Version

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.748201 | 0.760286 | 0.781545 | 0.753217 | 0.766074 | 0.783217 | 0.774550 | 0.830460 | 0.746475 | 0.758518 | 0.780188 | 0.769099 | 0.822924 | 6603 | 23 |
| w3_self | 0.689890 | 0.693063 | 0.736956 | 0.669947 | 0.674293 | 0.720863 | 0.696801 | 0.744243 | 0.682116 | 0.685985 | 0.730286 | 0.707395 | 0.753279 | 6603 | 24 |
| w2_predict_w3 | 0.656759 | 0.666322 | 0.696294 | 0.674489 | 0.685315 | 0.705036 | 0.695035 | 0.728878 | 0.657581 | 0.668402 | 0.693147 | 0.680526 | 0.714129 | 6603 | 23 |

## Drop-groups Version

- Dropped W2 feature groups: `v50, v51, v52_health, v57`
- Dropped W3 feature groups: `49, 50, 51, 55`

| scenario | train_accuracy | train_precision | train_recall | test_accuracy | test_precision | test_recall | test_f1 | test_auc | cv5_accuracy_mean | cv5_precision_mean | cv5_recall_mean | cv5_f1_mean | cv5_auc_mean | n_rows_modeling | n_features_used |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | 0.718478 | 0.735920 | 0.749039 | 0.722180 | 0.742340 | 0.745455 | 0.743894 | 0.797660 | 0.716794 | 0.734422 | 0.746914 | 0.740565 | 0.790312 | 6603 | 19 |
| w3_self | 0.652026 | 0.662409 | 0.690536 | 0.657835 | 0.672831 | 0.680576 | 0.676681 | 0.717549 | 0.647285 | 0.658126 | 0.685677 | 0.671524 | 0.710735 | 6603 | 20 |
| w2_predict_w3 | 0.644453 | 0.656478 | 0.680101 | 0.657078 | 0.669944 | 0.686331 | 0.678038 | 0.711099 | 0.642590 | 0.654751 | 0.678474 | 0.666359 | 0.697504 | 6603 | 19 |

## Delta (Drop - No-drop)

- Positive value means drop-groups performs better; negative means worse.

| scenario | delta_test_accuracy_drop_minus_no_drop | delta_test_precision_drop_minus_no_drop | delta_test_recall_drop_minus_no_drop | delta_test_f1_drop_minus_no_drop | delta_test_auc_drop_minus_no_drop | delta_cv5_accuracy_mean_drop_minus_no_drop | delta_cv5_precision_mean_drop_minus_no_drop | delta_cv5_recall_mean_drop_minus_no_drop | delta_cv5_f1_mean_drop_minus_no_drop | delta_cv5_auc_mean_drop_minus_no_drop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| w2_self | -0.031037 | -0.023734 | -0.037762 | -0.030657 | -0.032800 | -0.029681 | -0.024095 | -0.033274 | -0.028533 | -0.032612 |
| w3_self | -0.012112 | -0.001463 | -0.040288 | -0.020120 | -0.026695 | -0.034830 | -0.027860 | -0.044609 | -0.035872 | -0.042544 |
| w2_predict_w3 | -0.017411 | -0.015371 | -0.018705 | -0.016997 | -0.017779 | -0.014991 | -0.013651 | -0.014673 | -0.014167 | -0.016625 |

## Dropped Groups and Dropped Items

These are the feature groups removed in the drop-groups version.

- Dropped W2 feature groups: `v50, v51, v52_health, v57`
- Dropped W3 feature groups: `49, 50, 51, 55`

| Year | Dropped Group | Item | Item Exists In Dataset | Question Text |
| --- | --- | --- | --- | --- |
| W2 | v50 | v50 | True | 整體來說，你對自己的生活感到滿意嗎？ |
| W2 | v51 | v51 | True | 整體來說，你覺得最近的日子過得快樂嗎？ |
| W2 | v52_health | v52 | True | 整體而言，你覺得自己目前的健康狀況如何？ |
| W2 | v57 | v57_1 | True | 請問過去兩週中，你對以下敘述的感受程度？ (1)我感到情緒開朗且精神不錯 |
| W2 | v57 | v57_2 | True | 請問過去兩週中，你對以下敘述的感受程度？ (2)我感到心情平靜和放鬆 |
| W2 | v57 | v57_3 | True | 請問過去兩週中，你對以下敘述的感受程度？ (3)我感到有活力且精力充沛 |
| W2 | v57 | v57_4 | True | 請問過去兩週中，你對以下敘述的感受程度？ (4)我醒來感到神清氣爽並有充分休息 |
| W2 | v57 | v57_5 | True | 請問過去兩週中，你對以下敘述的感受程度？ (5)我的日常生活中充滿讓我感興趣的事物 |
| W3 | 49 | 49 | True | 49.整體來說，你對自己的生活感到滿意嗎？ |
| W3 | 50 | 50 | True | 50.整體來說，你覺得最近的日子過得快樂嗎？ |
| W3 | 51 | 51 | True | 51.整體而言，你覺得自己目前的健康狀況如何？ |
| W3 | 55 | 55-1 | True | 55.請問過去兩週中，你對以下敘述的感受程度？ - 55-1.我感到情緒開朗且精神不錯。 |
| W3 | 55 | 55-2 | True | 55.請問過去兩週中，你對以下敘述的感受程度？ - 55-2.我感到心情平靜和放鬆。 |
| W3 | 55 | 55-3 | True | 55.請問過去兩週中，你對以下敘述的感受程度？ - 55-3.我感到有活力且精力充沛。 |
| W3 | 55 | 55-4 | True | 55.請問過去兩週中，你對以下敘述的感受程度？ - 55-4.我醒來感到神清氣爽並有充分休息。 |
| W3 | 55 | 55-5 | True | 55.請問過去兩週中，你對以下敘述的感受程度？ - 55-5.我的日常生活中充滿讓我感興趣的事物。 |
