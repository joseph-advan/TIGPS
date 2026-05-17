# Ridge / Lasso / SHAP: Drop + Decomposition Features

## Setup
- Subscale config: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`
- Dropped groups (W3): `['49', '50', '51', '55']`
- Dropped groups (W2): `['v50', 'v51', 'v52_health', 'v57']`
- Feature set: current drop + decomposition features.
- W2 self-rated health is `v52_health` and is dropped; W2 `v52_1` to `v52_3` self-worth items are retained through the `v52` group when applicable.
- Scenarios: W2->W2, W3->W3, W2->W3
- Models: Ridge (L2 logistic), Lasso (L1 logistic)
- CV5 metrics are mean test-fold metrics across 5 stratified folds.

## Model Performance
| scenario_label   | model_label   |   test_accuracy |   test_f1 |   test_precision |   test_recall |   test_auc |   cv5_accuracy_mean |   cv5_f1_mean |   cv5_precision_mean |   cv5_recall_mean |   cv5_auc_mean |   n_features_used |
|:-----------------|:--------------|----------------:|----------:|-----------------:|--------------:|-----------:|--------------------:|--------------:|---------------------:|------------------:|---------------:|------------------:|
| W2 predict W2    | LASSO         |        0.741862 |  0.76434  |         0.755464 |      0.773427 |   0.817007 |            0.734057 |      0.755349 |             0.75244  |          0.758379 |       0.810642 |                30 |
| W2 predict W2    | RIDGE         |        0.73732  |  0.761184 |         0.749322 |      0.773427 |   0.816822 |            0.734967 |      0.756732 |             0.75218  |          0.761456 |       0.810738 |                30 |
| W2 predict W3    | LASSO         |        0.652536 |  0.671909 |         0.667614 |      0.676259 |   0.717409 |            0.650162 |      0.669613 |             0.665426 |          0.673868 |       0.707129 |                30 |
| W2 predict W3    | RIDGE         |        0.656321 |  0.675714 |         0.670922 |      0.680576 |   0.717664 |            0.648951 |      0.668461 |             0.664276 |          0.672717 |       0.707352 |                30 |
| W3 predict W3    | LASSO         |        0.657835 |  0.672938 |         0.676856 |      0.669065 |   0.735718 |            0.663943 |      0.683546 |             0.677312 |          0.689991 |       0.72909  |                31 |
| W3 predict W3    | RIDGE         |        0.658592 |  0.674368 |         0.676812 |      0.671942 |   0.735718 |            0.66364  |      0.684173 |             0.675855 |          0.692869 |       0.729389 |                31 |

## Top SHAP Features (Top 10 per scenario/model)
### W2 predict W2
#### RIDGE
| feature         |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52     |        0.54725  | -0.680822 |                  15.8551  | negative         |
| feature_v54_A   |        0.439576 |  0.530908 |                  12.3638  | positive         |
| feature_v1_male |        0.276999 | -0.277144 |                   6.45417 | negative         |
| feature_v28     |        0.234911 |  0.297227 |                   6.92185 | positive         |
| feature_v54_B   |        0.23157  | -0.324727 |                   7.56228 | negative         |
| feature_v5      |        0.21823  | -0.266772 |                   6.21261 | negative         |
| feature_v26_B   |        0.169469 |  0.22597  |                   5.26242 | positive         |
| feature_v54_E   |        0.159176 | -0.218643 |                   5.09179 | negative         |
| feature_v22     |        0.114864 |  0.144129 |                   3.35649 | positive         |
| feature_v27_B   |        0.104783 | -0.126743 |                   2.95161 | negative         |

#### LASSO
| feature         |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52     |        0.600429 | -0.746981 |                  18.6638  | negative         |
| feature_v54_A   |        0.493895 |  0.596512 |                  14.9042  | positive         |
| feature_v1_male |        0.27387  | -0.274013 |                   6.8464  | negative         |
| feature_v54_B   |        0.244572 | -0.342961 |                   8.5691  | negative         |
| feature_v28     |        0.239721 |  0.303312 |                   7.57846 | positive         |
| feature_v5      |        0.221563 | -0.270846 |                   6.76727 | negative         |
| feature_v26_B   |        0.161314 |  0.215096 |                   5.37432 | positive         |
| feature_v54_E   |        0.14809  | -0.203415 |                   5.08247 | negative         |
| feature_v22     |        0.108392 |  0.136008 |                   3.39826 | positive         |
| feature_v6      |        0.094503 |  0.123727 |                   3.09139 | positive         |

### W3 predict W3
#### RIDGE
| feature        |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:---------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_53_B   |        0.238585 |  0.289787 |                   8.89859 | positive         |
| feature_1_male |        0.203276 | -0.203282 |                   6.24226 | negative         |
| feature_29     |        0.186759 |  0.221721 |                   6.80846 | positive         |
| feature_53_E   |        0.162342 |  0.182192 |                   5.59462 | positive         |
| feature_4      |        0.132347 | -0.156718 |                   4.81239 | negative         |
| feature_53_A   |        0.126412 | -0.175765 |                   5.39727 | negative         |
| feature_26_C   |        0.109443 |  0.136548 |                   4.19302 | positive         |
| feature_52     |        0.107723 | -0.118154 |                   3.62819 | negative         |
| feature_30     |        0.103972 |  0.136694 |                   4.19752 | positive         |
| feature_24     |        0.10251  |  0.13323  |                   4.09115 | positive         |

#### LASSO
| feature        |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:---------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_53_B   |        0.301765 |  0.366526 |                   9.74267 | positive         |
| feature_1_male |        0.221294 | -0.221301 |                   5.88244 | negative         |
| feature_53_E   |        0.210362 |  0.236083 |                   6.27535 | positive         |
| feature_29     |        0.20904  |  0.248173 |                   6.59672 | positive         |
| feature_53_A   |        0.179629 | -0.249758 |                   6.63884 | negative         |
| feature_4      |        0.143678 | -0.170134 |                   4.52236 | negative         |
| feature_26_C   |        0.123316 |  0.153857 |                   4.08968 | positive         |
| feature_52     |        0.123019 | -0.134931 |                   3.58661 | negative         |
| feature_24     |        0.117959 |  0.15331  |                   4.07514 | positive         |
| feature_30     |        0.115442 |  0.151775 |                   4.03434 | positive         |

### W2 predict W3
#### RIDGE
| feature         |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52     |        0.267617 | -0.354238 |                  14.7632  | negative         |
| feature_v54_A   |        0.214214 |  0.247696 |                  10.323   | positive         |
| feature_v1_male |        0.156386 | -0.156432 |                   6.51945 | negative         |
| feature_v28     |        0.101239 |  0.125732 |                   5.24002 | positive         |
| feature_v5      |        0.100228 | -0.12342  |                   5.14364 | negative         |
| feature_v25_B   |        0.095078 | -0.11985  |                   4.99487 | negative         |
| feature_v26_B   |        0.09369  |  0.134038 |                   5.58615 | positive         |
| feature_v54_B   |        0.086924 | -0.110264 |                   4.59537 | negative         |
| feature_v54_E   |        0.083854 | -0.107673 |                   4.48736 | negative         |
| feature_v23_A   |        0.068863 |  0.079128 |                   3.29772 | positive         |

#### LASSO
| feature         |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52     |        0.286142 | -0.378759 |                  15.3154  | negative         |
| feature_v54_A   |        0.232594 |  0.268949 |                  10.8752  | positive         |
| feature_v1_male |        0.15708  | -0.157126 |                   6.35353 | negative         |
| feature_v28     |        0.104733 |  0.130072 |                   5.25958 | positive         |
| feature_v5      |        0.101622 | -0.125137 |                   5.06002 | negative         |
| feature_v26_B   |        0.098599 |  0.141061 |                   5.70392 | positive         |
| feature_v25_B   |        0.095082 | -0.119856 |                   4.84649 | negative         |
| feature_v54_B   |        0.093169 | -0.118186 |                   4.77895 | negative         |
| feature_v54_E   |        0.085825 | -0.110203 |                   4.45618 | negative         |
| feature_v23_A   |        0.070086 |  0.080534 |                   3.25645 | positive         |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_shap_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_relative_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_details.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_report_zh.md`

