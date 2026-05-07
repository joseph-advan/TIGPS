# Ridge / Lasso / SHAP (Three Scenarios)

## Setup
- Feature map: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\features_used\W2W3_Features.csv`
- Excluded groups (W3): `['49', '50', '52', '55']`
- Excluded groups (W2): `['v50', 'v51', 'v52', 'v57']`
- Scenarios: W2->W2, W3->W3, W2->W3
- Models: Ridge (L2 logistic), Lasso (L1 logistic)

## Model Performance
| scenario_label   | model_label   |   test_accuracy |   test_f1 |   test_precision |   test_recall |   test_auc |   cv5_accuracy_mean |   cv5_f1_mean |   cv5_precision_mean |   cv5_recall_mean |   cv5_auc_mean |   n_features_used |
|:-----------------|:--------------|----------------:|----------:|-----------------:|--------------:|-----------:|--------------------:|--------------:|---------------------:|------------------:|---------------:|------------------:|
| W2 predict W2    | LASSO         |        0.717638 |  0.743643 |         0.731081 |      0.756643 |   0.799495 |            0.722396 |      0.743853 |             0.74318  |          0.744677 |       0.795621 |               118 |
| W2 predict W2    | RIDGE         |        0.721423 |  0.746207 |         0.736054 |      0.756643 |   0.803203 |            0.719671 |      0.741558 |             0.740232 |          0.742999 |       0.796993 |               118 |
| W2 predict W3    | LASSO         |        0.694171 |  0.689708 |         0.739703 |      0.646043 |   0.760986 |            0.684388 |      0.682552 |             0.724972 |          0.645076 |       0.74658  |               132 |
| W2 predict W3    | RIDGE         |        0.700227 |  0.700454 |         0.738437 |      0.666187 |   0.759942 |            0.683026 |      0.683255 |             0.720657 |          0.649684 |       0.744452 |               132 |
| W3 predict W3    | LASSO         |        0.693414 |  0.707158 |         0.710756 |      0.703597 |   0.763601 |            0.693476 |      0.71022  |             0.706746 |          0.71388  |       0.766269 |               119 |
| W3 predict W3    | RIDGE         |        0.694171 |  0.703377 |         0.718141 |      0.689209 |   0.765734 |            0.69181  |      0.708176 |             0.705845 |          0.710713 |       0.766245 |               119 |

## Top SHAP Features (Top 10 per scenario/model)
### W2 predict W2
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v1        |        0.25475  | -0.254884 |                   3.98969 | negative         |
| v54_2     |        0.147578 |  0.172788 |                   2.70465 | positive         |
| v54_1     |        0.139976 |  0.16179  |                   2.53249 | positive         |
| v6_1      |        0.124582 |  0.144663 |                   2.2644  | positive         |
| v28_6     |        0.111239 |  0.126946 |                   1.98707 | positive         |
| v19_3     |        0.110166 | -0.129419 |                   2.0258  | negative         |
| v54_4     |        0.105415 | -0.152462 |                   2.38649 | negative         |
| v54_6     |        0.103542 | -0.151699 |                   2.37455 | negative         |
| v26_3     |        0.095101 | -0.120972 |                   1.89358 | negative         |
| v5_5      |        0.093608 | -0.11732  |                   1.8364  | negative         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v1        |        0.323023 | -0.323192 |                   5.5145  | negative         |
| v54_2     |        0.189233 |  0.221559 |                   3.78036 | positive         |
| v54_1     |        0.161276 |  0.186409 |                   3.18062 | positive         |
| v6_1      |        0.154745 |  0.179688 |                   3.06594 | positive         |
| v19_3     |        0.147797 | -0.173627 |                   2.96252 | negative         |
| v54_6     |        0.133238 | -0.195207 |                   3.33074 | negative         |
| v5_5      |        0.13276  | -0.16639  |                   2.83904 | negative         |
| v28_6     |        0.128762 |  0.146942 |                   2.5072  | positive         |
| v54_4     |        0.12195  | -0.176376 |                   3.00944 | negative         |
| v42_14    |        0.119341 | -0.152942 |                   2.60958 | negative         |

### W3 predict W3
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| 51        |        0.361715 |  0.449401 |                   8.2843  | positive         |
| 1         |        0.164685 |  0.164691 |                   3.03592 | positive         |
| 53-2      |        0.113405 | -0.134192 |                   2.4737  | negative         |
| 5-1       |        0.093692 |  0.11506  |                   2.12102 | positive         |
| 39-14     |        0.091739 | -0.107374 |                   1.97934 | negative         |
| 29-10     |        0.084094 |  0.089104 |                   1.64256 | positive         |
| 53-8      |        0.08258  | -0.091904 |                   1.69417 | negative         |
| 24-7      |        0.080278 |  0.093753 |                   1.72825 | positive         |
| 53-4      |        0.080212 |  0.097536 |                   1.79799 | positive         |
| 53-12     |        0.079153 |  0.091526 |                   1.6872  | positive         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| 51        |        0.476058 |  0.591464 |                  12.0655  | positive         |
| 1         |        0.19225  |  0.192256 |                   3.92191 | positive         |
| 53-2      |        0.153283 | -0.18138  |                   3.70003 | negative         |
| 39-14     |        0.120911 | -0.141517 |                   2.88685 | negative         |
| 5-1       |        0.108519 |  0.133269 |                   2.7186  | positive         |
| 53-15     |        0.100062 | -0.119268 |                   2.43299 | negative         |
| 29-10     |        0.094222 |  0.099836 |                   2.03659 | positive         |
| 53-5      |        0.092865 |  0.115439 |                   2.35488 | positive         |
| 53-4      |        0.092291 |  0.112224 |                   2.28931 | positive         |
| 53-12     |        0.089604 |  0.10361  |                   2.11358 | positive         |

### W2 predict W3
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v55_8     |        0.092736 |  0.117583 |                   4.12022 | positive         |
| v55_2     |        0.085988 |  0.110446 |                   3.87013 | positive         |
| v1        |        0.076601 | -0.076624 |                   2.68497 | negative         |
| v55_7     |        0.069938 |  0.103026 |                   3.61014 | positive         |
| v55_1     |        0.064775 |  0.086025 |                   3.01439 | positive         |
| v55_10    |        0.054905 |  0.079408 |                   2.78254 | positive         |
| v55_14    |        0.053422 |  0.074984 |                   2.62753 | positive         |
| v55_3     |        0.050374 |  0.064846 |                   2.27228 | positive         |
| v23_1     |        0.046473 |  0.04998  |                   1.75135 | positive         |
| v25_6     |        0.044486 | -0.051276 |                   1.79676 | negative         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v55_8     |        0.160075 |  0.202963 |                  11.2092  | positive         |
| v55_2     |        0.126543 |  0.162536 |                   8.97651 | positive         |
| v55_7     |        0.111666 |  0.164495 |                   9.08469 | positive         |
| v1        |        0.101076 | -0.101106 |                   5.58384 | negative         |
| v55_14    |        0.092357 |  0.129634 |                   7.1594  | positive         |
| v55_1     |        0.076361 |  0.101412 |                   5.60074 | positive         |
| v55_10    |        0.067673 |  0.097874 |                   5.40537 | positive         |
| v25_6     |        0.065371 | -0.075348 |                   4.16129 | negative         |
| v27_1     |        0.063365 |  0.08742  |                   4.82803 | positive         |
| v6_2      |        0.057724 | -0.070641 |                   3.90136 | negative         |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_shap_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_relative_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_details.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_report_zh.md`

