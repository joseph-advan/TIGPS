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
| W2 predict W2    | LASSO         |        0.742619 |  0.762901 |         0.760779 |      0.765035 |   0.831967 |            0.74042  |      0.760396 |             0.75978  |          0.761174 |       0.81962  |                33 |
| W2 predict W2    | RIDGE         |        0.741105 |  0.761838 |         0.758669 |      0.765035 |   0.832025 |            0.740268 |      0.760654 |             0.7589   |          0.762573 |       0.81963  |                33 |
| W2 predict W3    | LASSO         |        0.654807 |  0.674286 |         0.669504 |      0.679137 |   0.717935 |            0.651375 |      0.6709   |             0.666341 |          0.6756   |       0.709957 |                33 |
| W2 predict W3    | RIDGE         |        0.654807 |  0.675676 |         0.668073 |      0.683453 |   0.717852 |            0.650768 |      0.671078 |             0.665022 |          0.677326 |       0.710064 |                33 |
| W3 predict W3    | LASSO         |        0.660863 |  0.674891 |         0.68082  |      0.669065 |   0.736222 |            0.66576  |      0.685511 |             0.678669 |          0.692581 |       0.729324 |                31 |
| W3 predict W3    | RIDGE         |        0.659349 |  0.675325 |         0.677279 |      0.673381 |   0.73613  |            0.664397 |      0.685011 |             0.676416 |          0.69402  |       0.729648 |                31 |

## Top SHAP Features (Top 10 per scenario/model)
### W2 predict W2
#### RIDGE
| feature             |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:--------------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52         |        0.494653 | -0.615386 |                  14.5819  | negative         |
| feature_v54_A       |        0.339346 |  0.409088 |                   9.69353 | positive         |
| feature_v1_male     |        0.279688 | -0.279834 |                   6.63081 | negative         |
| feature_v8_03-v8_06 |        0.258419 |  0.32784  |                   7.76832 | positive         |
| feature_v28         |        0.226435 |  0.286502 |                   6.7888  | positive         |
| feature_v54_B       |        0.202503 | -0.283968 |                   6.72874 | negative         |
| feature_v5          |        0.186072 | -0.227461 |                   5.38978 | negative         |
| feature_v26_B       |        0.164749 |  0.219677 |                   5.20534 | positive         |
| feature_v54_E       |        0.158031 | -0.21707  |                   5.14357 | negative         |
| feature_v22         |        0.098941 |  0.12415  |                   2.94179 | positive         |

#### LASSO
| feature             |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:--------------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52         |        0.575995 | -0.716583 |                  17.5573  | negative         |
| feature_v54_A       |        0.405852 |  0.489262 |                  11.9876  | positive         |
| feature_v1_male     |        0.283619 | -0.283767 |                   6.95269 | negative         |
| feature_v8_03-v8_06 |        0.281809 |  0.357512 |                   8.75955 | positive         |
| feature_v28         |        0.241767 |  0.305901 |                   7.495   | positive         |
| feature_v54_B       |        0.221278 | -0.310295 |                   7.60266 | negative         |
| feature_v5          |        0.193128 | -0.236086 |                   5.78443 | negative         |
| feature_v26_B       |        0.167867 |  0.223835 |                   5.48426 | positive         |
| feature_v54_E       |        0.155318 | -0.213344 |                   5.22721 | negative         |
| feature_v22         |        0.091714 |  0.115082 |                   2.81966 | positive         |

### W3 predict W3
#### RIDGE
| feature        |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:---------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_53_B   |        0.240533 |  0.292153 |                   8.94417 | positive         |
| feature_1_male |        0.202961 | -0.202967 |                   6.21377 | negative         |
| feature_29     |        0.18732  |  0.222386 |                   6.80828 | positive         |
| feature_53_E   |        0.157096 |  0.176305 |                   5.39751 | positive         |
| feature_53_A   |        0.149688 | -0.174519 |                   5.34283 | negative         |
| feature_4      |        0.132802 | -0.157256 |                   4.81433 | negative         |
| feature_26_C   |        0.110074 |  0.137335 |                   4.20446 | positive         |
| feature_52     |        0.109857 | -0.120494 |                   3.68889 | negative         |
| feature_30     |        0.104096 |  0.136858 |                   4.18985 | positive         |
| feature_24     |        0.10196  |  0.132516 |                   4.05693 | positive         |

#### LASSO
| feature        |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:---------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_53_B   |        0.299171 |  0.363375 |                  10.0471  | positive         |
| feature_1_male |        0.218486 | -0.218493 |                   6.04122 | negative         |
| feature_29     |        0.207684 |  0.246562 |                   6.81733 | positive         |
| feature_53_A   |        0.2027   | -0.236325 |                   6.53425 | negative         |
| feature_53_E   |        0.194659 |  0.218461 |                   6.04033 | positive         |
| feature_4      |        0.142645 | -0.168911 |                   4.67031 | negative         |
| feature_52     |        0.120359 | -0.132013 |                   3.65009 | negative         |
| feature_26_C   |        0.117071 |  0.146066 |                   4.03864 | positive         |
| feature_53_F   |        0.114837 | -0.156628 |                   4.33068 | negative         |
| feature_30     |        0.114169 |  0.1501   |                   4.15019 | positive         |

### W2 predict W3
#### RIDGE
| feature             |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:--------------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52         |        0.231399 | -0.306297 |                  13.2577  | negative         |
| feature_v54_A       |        0.163847 |  0.189006 |                   8.18091 | positive         |
| feature_v1_male     |        0.153254 | -0.153299 |                   6.63539 | negative         |
| feature_v8_03-v8_06 |        0.124457 |  0.145489 |                   6.29733 | positive         |
| feature_v28         |        0.095445 |  0.118536 |                   5.13072 | positive         |
| feature_v26_B       |        0.086389 |  0.123593 |                   5.34961 | positive         |
| feature_v25_B       |        0.083283 | -0.104982 |                   4.54405 | negative         |
| feature_v5          |        0.082351 | -0.101407 |                   4.38931 | negative         |
| feature_v54_E       |        0.07772  | -0.099796 |                   4.31957 | negative         |
| feature_v54_B       |        0.074138 | -0.094044 |                   4.0706  | negative         |

#### LASSO
| feature             |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:--------------------|----------------:|----------:|--------------------------:|:-----------------|
| feature_v52         |        0.270324 | -0.357821 |                  14.5781  | negative         |
| feature_v54_A       |        0.190943 |  0.220262 |                   8.97375 | positive         |
| feature_v1_male     |        0.15979  | -0.159837 |                   6.51196 | negative         |
| feature_v8_03-v8_06 |        0.135782 |  0.158728 |                   6.46676 | positive         |
| feature_v28         |        0.105597 |  0.131144 |                   5.34299 | positive         |
| feature_v26_B       |        0.099249 |  0.141991 |                   5.78491 | positive         |
| feature_v54_E       |        0.086645 | -0.111256 |                   4.53269 | negative         |
| feature_v54_B       |        0.084905 | -0.107703 |                   4.38795 | negative         |
| feature_v5          |        0.084762 | -0.104376 |                   4.25241 | negative         |
| feature_v25_B       |        0.084574 | -0.10661  |                   4.34344 | negative         |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_shap_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_relative_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_details.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_report_zh.md`

