# Logistic Baseline + Interpersonal Features (Median Split)

## Data
- W2: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Basic roster: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`

## Interpersonal Feature Engineering
- Relations used: online_friend / online_enemy / offline_friend / offline_enemy (5 nomination slots each year).
- Nominee mapping key: `(school_id, class, seat)` via `W2W3_Student_Basic_Info.csv`.
- Features include in/out counts, ratios, net scores, online-offline deltas, reciprocity/conflict, and class-normalized rates.

### Edge Build Diagnostics
| year   |   n_students_input |   n_rows_input |   ambiguous_lookup_keys |   raw_nomination_cells |   valid_positive_seat_cells |   accepted_edges_before_dedup |   dropped_invalid_or_empty |   dropped_lookup_not_found |   dropped_self_nomination |   accepted_edges_after_dedup |   dedup_removed |
|:-------|-------------------:|---------------:|------------------------:|-----------------------:|----------------------------:|------------------------------:|---------------------------:|---------------------------:|--------------------------:|-----------------------------:|----------------:|
| W2     |               6603 |           6603 |                       0 |                  83639 |                       83639 |                         61772 |                      48421 |                      21867 |                         0 |                        61772 |               0 |
| W3     |               6603 |           6603 |                       0 |                  80408 |                       80408 |                         60288 |                      51652 |                      19897 |                       223 |                        60288 |               0 |

## Model Comparison Summary
| scenario      | setting                             |   test_accuracy |   test_f1 |   test_auc |   cv5_accuracy_mean |   cv5_f1_mean |   cv5_auc_mean |   n_features_used |   n_rows_modeling |
|:--------------|:------------------------------------|----------------:|----------:|-----------:|--------------------:|--------------:|---------------:|------------------:|------------------:|
| w2_predict_w3 | baseline_drop                       |        0.659349 |  0.683099 |   0.715094 |            0.641531 |      0.665986 |       0.698306 |               117 |              6603 |
| w2_predict_w3 | baseline_drop_plus_interpersonal    |        0.660106 |  0.685794 |   0.711734 |            0.64153  |      0.665909 |       0.695988 |               165 |              6603 |
| w2_predict_w3 | baseline_no_drop                    |        0.666162 |  0.686567 |   0.729133 |            0.665004 |      0.686479 |       0.71866  |               127 |              6603 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal |        0.663134 |  0.68728  |   0.726108 |            0.660764 |      0.682447 |       0.716523 |               175 |              6603 |
| w2_predict_w3 | interpersonal_only                  |        0.529145 |  0.683622 |   0.553626 |            0.526276 |      0.683316 |       0.539329 |                48 |              6603 |
| w2_self       | baseline_drop                       |        0.722937 |  0.747586 |   0.802892 |            0.718611 |      0.74039  |       0.796962 |               117 |              6603 |
| w2_self       | baseline_drop_plus_interpersonal    |        0.732778 |  0.755371 |   0.804879 |            0.724214 |      0.744815 |       0.796767 |               165 |              6603 |
| w2_self       | baseline_no_drop                    |        0.774413 |  0.793056 |   0.845699 |            0.762378 |      0.781368 |       0.840641 |               127 |              6603 |
| w2_self       | baseline_no_drop_plus_interpersonal |        0.772142 |  0.790244 |   0.846761 |            0.762378 |      0.781593 |       0.839671 |               175 |              6603 |
| w2_self       | interpersonal_only                  |        0.563967 |  0.638191 |   0.571804 |            0.562773 |      0.638028 |       0.574274 |                48 |              6603 |
| w3_self       | baseline_drop                       |        0.694171 |  0.703377 |   0.765734 |            0.69181  |      0.708176 |       0.766245 |               119 |              6603 |
| w3_self       | baseline_drop_plus_interpersonal    |        0.687358 |  0.697879 |   0.765534 |            0.690296 |      0.706463 |       0.765506 |               167 |              6603 |
| w3_self       | baseline_no_drop                    |        0.710825 |  0.724784 |   0.786823 |            0.704078 |      0.723462 |       0.783372 |               129 |              6603 |
| w3_self       | baseline_no_drop_plus_interpersonal |        0.709311 |  0.722944 |   0.78637  |            0.702411 |      0.721384 |       0.782808 |               177 |              6603 |
| w3_self       | interpersonal_only                  |        0.554126 |  0.640195 |   0.569199 |            0.545054 |      0.638209 |       0.550978 |                48 |              6603 |

## Top Interpersonal Features by Permutation Importance (AUC)
| scenario      | setting                             | feature                                          |   importance_mean |   importance_std |
|:--------------|:------------------------------------|:-------------------------------------------------|------------------:|-----------------:|
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_received_like_ratio                           |          0.000501 |         0.000222 |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_reciprocal_enemy_count                        |          0.000363 |         0.00019  |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_reciprocal_enemy_count_rate_class             |          0.000292 |         0.00018  |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_in_offline_friend                             |          0.000273 |         0.000208 |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_in_friend_total                               |          0.000185 |         0.000188 |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_out_enemy_online_minus_offline                |          0.000171 |         6.2e-05  |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_out_offline_friend_rate_class                 |          0.000132 |         0.00029  |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_out_friend_total_rate_class                   |          0.000121 |         0.000139 |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_in_friend_online_minus_offline                |          0.000119 |         5.9e-05  |
| w2_predict_w3 | baseline_drop_plus_interpersonal    | ip_out_offline_enemy_rate_class                  |          0.000101 |         9.4e-05  |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_received_like_ratio                           |          0.000347 |         0.000157 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_reciprocal_enemy_count                        |          0.000226 |         0.000141 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_reciprocal_enemy_count_rate_class             |          9.8e-05  |         9.3e-05  |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_in_offline_friend                             |          7.4e-05  |         0.000108 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_reciprocal_friend_count                       |          7.3e-05  |         0.000333 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_sent_like_ratio                               |          6.1e-05  |         0.00014  |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_out_friend_total_rate_class                   |          5.8e-05  |         0.000161 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_out_offline_enemy_rate_class                  |          5.1e-05  |         7.6e-05  |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_out_offline_friend_rate_class                 |          5e-05    |         0.000274 |
| w2_predict_w3 | baseline_no_drop_plus_interpersonal | ip_in_friend_online_minus_offline                |          4.2e-05  |         6.1e-05  |
| w2_predict_w3 | interpersonal_only                  | ip_out_offline_enemy_rate_class                  |          0.002615 |         0.001936 |
| w2_predict_w3 | interpersonal_only                  | ip_out_enemy_total_rate_class                    |          0.002223 |         0.001783 |
| w2_predict_w3 | interpersonal_only                  | ip_class_size                                    |          0.002102 |         0.001246 |
| w2_predict_w3 | interpersonal_only                  | ip_class_size_minus1                             |          0.002095 |         0.001246 |
| w2_predict_w3 | interpersonal_only                  | ip_out_online_enemy_rate_class                   |          0.001399 |         0.001599 |
| w2_predict_w3 | interpersonal_only                  | ip_out_offline_enemy                             |          0.001378 |         0.001535 |
| w2_predict_w3 | interpersonal_only                  | ip_reciprocal_friend_count_rate_class            |          0.001109 |         0.001667 |
| w2_predict_w3 | interpersonal_only                  | ip_out_offline_friend_rate_class                 |          0.001047 |         0.000872 |
| w2_predict_w3 | interpersonal_only                  | ip_enemy_by_me_but_likes_me_count_rate_class     |          0.001007 |         0.000766 |
| w2_predict_w3 | interpersonal_only                  | ip_out_enemy_total                               |          0.000925 |         0.001283 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_sent_like_ratio                               |          0.00254  |         0.000659 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_in_online_friend_rate_class                   |          0.000683 |         0.000223 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_liked_by_me_but_enemy_to_me_count_rate_class  |          0.000668 |         0.000282 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_in_friend_total_rate_class                    |          0.000477 |         0.000229 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_out_online_enemy_rate_class                   |          0.000438 |         0.000134 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_out_enemy_total_rate_class                    |          0.000382 |         0.000132 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_reciprocal_friend_count_rate_class            |          0.00036  |         0.000387 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_enemy_by_me_but_likes_me_count_rate_class     |          0.00029  |         0.000334 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_out_offline_enemy_rate_class                  |          0.00026  |         0.000118 |
| w2_self       | baseline_drop_plus_interpersonal    | ip_enemy_by_me_but_likes_me_count                |          0.000253 |         0.00035  |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_sent_like_ratio                               |          0.001748 |         0.000353 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_liked_by_me_but_enemy_to_me_count_rate_class  |          0.000285 |         0.000171 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_in_friend_online_minus_offline                |          0.000231 |         0.000105 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_enemy_by_me_but_likes_me_count                |          0.00022  |         0.000259 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_in_online_friend_rate_class                   |          0.000207 |         7.5e-05  |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_in_enemy_online_minus_offline_rate_class      |          0.000194 |         0.000212 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_enemy_by_me_but_likes_me_count_rate_class     |          0.000187 |         0.000199 |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_in_friend_total_rate_class                    |          0.000114 |         8.8e-05  |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_out_online_enemy_rate_class                   |          0.000113 |         4.9e-05  |
| w2_self       | baseline_no_drop_plus_interpersonal | ip_out_enemy_total_rate_class                    |          0.0001   |         6.3e-05  |
| w2_self       | interpersonal_only                  | ip_sent_like_ratio                               |          0.00913  |         0.008069 |
| w2_self       | interpersonal_only                  | ip_in_offline_friend                             |          0.002586 |         0.00171  |
| w2_self       | interpersonal_only                  | ip_out_enemy_online_minus_offline                |          0.002533 |         0.004112 |
| w2_self       | interpersonal_only                  | ip_same_target_friend_and_enemy_count_rate_class |          0.002291 |         0.002693 |
| w2_self       | interpersonal_only                  | ip_in_friend_total                               |          0.002124 |         0.001564 |
| w2_self       | interpersonal_only                  | ip_reciprocal_friend_count                       |          0.001637 |         0.00208  |
| w2_self       | interpersonal_only                  | ip_in_online_friend                              |          0.001383 |         0.0012   |
| w2_self       | interpersonal_only                  | ip_liked_by_me_but_enemy_to_me_count_rate_class  |          0.001377 |         0.001239 |
| w2_self       | interpersonal_only                  | ip_in_enemy_online_minus_offline_rate_class      |          0.001112 |         0.00292  |
| w2_self       | interpersonal_only                  | ip_enemy_by_me_but_likes_me_count                |          0.000975 |         0.00108  |
| w3_self       | baseline_drop_plus_interpersonal    | ip_in_enemy_online_minus_offline                 |          0.00082  |         0.000652 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_in_online_enemy                               |          0.000703 |         0.000309 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_same_target_friend_and_enemy_count_rate_class |          0.000525 |         0.000238 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_same_target_friend_and_enemy_count            |          0.000505 |         0.000266 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_received_like_ratio                           |          0.000396 |         0.000252 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_in_enemy_total                                |          0.000357 |         0.000204 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_received_net                                  |          0.000351 |         0.000276 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_reciprocal_enemy_count_rate_class             |          0.000281 |         0.000134 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_sent_like_ratio                               |          0.000238 |         0.000221 |
| w3_self       | baseline_drop_plus_interpersonal    | ip_out_friend_online_minus_offline_rate_class    |          0.000142 |         0.000326 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_in_enemy_online_minus_offline                 |          0.000649 |         0.000491 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_in_online_enemy                               |          0.000608 |         0.000225 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_same_target_friend_and_enemy_count            |          0.000483 |         0.000245 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_same_target_friend_and_enemy_count_rate_class |          0.000451 |         0.0002   |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_reciprocal_enemy_count_rate_class             |          0.00037  |         0.000142 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_received_net                                  |          0.000357 |         0.000184 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_in_enemy_online_minus_offline_rate_class      |          0.000324 |         0.000415 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_out_online_friend_rate_class                  |          0.000323 |         0.00031  |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_in_enemy_total                                |          0.000318 |         0.000133 |
| w3_self       | baseline_no_drop_plus_interpersonal | ip_reciprocal_friend_count_rate_class            |          0.00029  |         0.000235 |
| w3_self       | interpersonal_only                  | ip_reciprocal_friend_count_rate_class            |          0.006278 |         0.002718 |
| w3_self       | interpersonal_only                  | ip_out_friend_online_minus_offline               |          0.004027 |         0.002397 |
| w3_self       | interpersonal_only                  | ip_in_enemy_online_minus_offline                 |          0.00401  |         0.001643 |
| w3_self       | interpersonal_only                  | ip_liked_by_me_but_enemy_to_me_count             |          0.002617 |         0.003612 |
| w3_self       | interpersonal_only                  | ip_same_target_friend_and_enemy_count_rate_class |          0.002199 |         0.003821 |
| w3_self       | interpersonal_only                  | ip_same_target_friend_and_enemy_count            |          0.001957 |         0.003111 |
| w3_self       | interpersonal_only                  | ip_out_offline_friend_rate_class                 |          0.00192  |         0.001074 |
| w3_self       | interpersonal_only                  | ip_out_friend_total_rate_class                   |          0.001745 |         0.001098 |
| w3_self       | interpersonal_only                  | ip_out_online_friend                             |          0.001725 |         0.00441  |
| w3_self       | interpersonal_only                  | ip_reciprocal_friend_count                       |          0.00169  |         0.001502 |

