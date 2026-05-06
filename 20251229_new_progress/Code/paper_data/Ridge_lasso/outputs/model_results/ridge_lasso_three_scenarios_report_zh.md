# Ridge / Lasso / SHAP (Three Scenarios)

## Setup
- Feature map: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\features_used\W2W3_Features.csv`
- Excluded groups (W3): `['49', '50', '52', '55']`
- Excluded groups (W2): `['v50', 'v51', 'v52', 'v57']`
- Scenarios: W2->W2, W3->W3, W2->W3
- Models: Ridge (L2 logistic), Lasso (L1 logistic)

## Model Performance
| scenario_label   | model_label   |   test_accuracy |   test_f1 |   test_precision |   test_recall |   test_auc |   cv5_accuracy_mean |   cv5_f1_mean |   cv5_precision_mean |   cv5_recall_mean |   cv5_auc_mean |   n_features_used |
|:-----------------|:--------------|----------------:|----------:|-----------------:|--------------:|-----------:|--------------------:|--------------:|---------------------:|------------------:|---------------:|------------------:|
| W2 predict W2    | LASSO         |        0.737156 |  0.755709 |         0.759388 |      0.752066 |   0.810621 |            0.740354 |      0.760513 |             0.757884 |          0.763498 |       0.815095 |               119 |
| W2 predict W2    | RIDGE         |        0.743112 |  0.760915 |         0.76569  |      0.756198 |   0.811994 |            0.738566 |      0.759291 |             0.755406 |          0.763498 |       0.814813 |               119 |
| W2 predict W3    | LASSO         |        0.702159 |  0.686028 |         0.739425 |      0.639824 |   0.755657 |            0.704753 |      0.690427 |             0.740105 |          0.647253 |       0.765823 |               133 |
| W2 predict W3    | RIDGE         |        0.702159 |  0.685535 |         0.740238 |      0.63836  |   0.758086 |            0.70654  |      0.693747 |             0.739704 |          0.653403 |       0.766615 |               133 |
| W3 predict W3    | LASSO         |        0.706627 |  0.707281 |         0.717949 |      0.696925 |   0.790323 |            0.717564 |      0.718365 |             0.72932  |          0.707848 |       0.796763 |               117 |
| W3 predict W3    | RIDGE         |        0.705138 |  0.703593 |         0.719755 |      0.688141 |   0.791104 |            0.715927 |      0.715549 |             0.729421 |          0.70229  |       0.797085 |               117 |

## Top SHAP Features (Top 10 per scenario/model)
### W2 predict W2
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v521      |        0.337532 | -0.412776 |                   6.58554 | negative         |
| v1        |        0.228388 | -0.228192 |                   3.64064 | negative         |
| v54_2     |        0.162302 |  0.186456 |                   2.97477 | positive         |
| v54_1     |        0.156447 |  0.175371 |                   2.79792 | positive         |
| v54_4     |        0.114251 | -0.15692  |                   2.50355 | negative         |
| v25_6     |        0.107089 | -0.126521 |                   2.01855 | negative         |
| v6_1      |        0.102946 |  0.121406 |                   1.93695 | positive         |
| v28_6     |        0.102716 |  0.124781 |                   1.99078 | positive         |
| v54_6     |        0.097273 | -0.126514 |                   2.01844 | negative         |
| v54_3     |        0.096199 |  0.106931 |                   1.706   | positive         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v521      |        0.444151 | -0.543162 |                   9.43572 | negative         |
| v1        |        0.284725 | -0.284481 |                   4.94196 | negative         |
| v54_2     |        0.207082 |  0.2379   |                   4.13277 | positive         |
| v54_1     |        0.182417 |  0.204483 |                   3.55225 | positive         |
| v54_4     |        0.150702 | -0.206985 |                   3.59571 | negative         |
| v25_6     |        0.138359 | -0.163466 |                   2.8397  | negative         |
| v5_5      |        0.124379 | -0.164586 |                   2.85916 | negative         |
| v28_6     |        0.120484 |  0.146366 |                   2.54265 | positive         |
| v42_14    |        0.119817 | -0.148748 |                   2.58403 | negative         |
| v6_1      |        0.119046 |  0.140393 |                   2.43888 | positive         |

### W3 predict W3
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| 51        |        0.424569 | -0.511713 |                   7.65383 | negative         |
| 1         |        0.174458 |  0.174317 |                   2.60731 | positive         |
| 53-4      |        0.150305 | -0.198436 |                   2.96806 | negative         |
| 30        |        0.140459 |  0.163057 |                   2.43888 | positive         |
| 27-2      |        0.1319   |  0.150734 |                   2.25457 | positive         |
| 53-12     |        0.129007 | -0.158493 |                   2.37063 | negative         |
| 5-1       |        0.11581  |  0.146095 |                   2.18518 | positive         |
| 53-2      |        0.115539 |  0.138791 |                   2.07594 | positive         |
| 5-6       |        0.113041 |  0.144405 |                   2.15991 | positive         |
| 53-5      |        0.100219 | -0.14147  |                   2.116   | negative         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| 51        |        0.5117   | -0.616729 |                   9.56312 | negative         |
| 53-4      |        0.195051 | -0.257512 |                   3.99303 | negative         |
| 1         |        0.18615  |  0.186    |                   2.88416 | positive         |
| 27-2      |        0.166826 |  0.190647 |                   2.95621 | positive         |
| 53-12     |        0.159646 | -0.196136 |                   3.04133 | negative         |
| 30        |        0.157004 |  0.182264 |                   2.82622 | positive         |
| 53-2      |        0.15046  |  0.180741 |                   2.8026  | positive         |
| 5-6       |        0.130338 |  0.166501 |                   2.58181 | positive         |
| 5-1       |        0.125972 |  0.158913 |                   2.46414 | positive         |
| 53-14     |        0.118163 |  0.151311 |                   2.34625 | positive         |

### W2 predict W3
#### RIDGE
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v55_8     |        0.103976 |  0.133023 |                   4.10326 | positive         |
| v1        |        0.096956 | -0.096156 |                   2.96605 | negative         |
| v521      |        0.076973 | -0.091511 |                   2.82278 | negative         |
| v55_14    |        0.075034 |  0.103177 |                   3.18262 | positive         |
| v55_2     |        0.073391 |  0.098098 |                   3.02595 | positive         |
| v55_3     |        0.064317 |  0.085794 |                   2.64642 | positive         |
| v55_13    |        0.063032 |  0.08546  |                   2.63613 | positive         |
| v55_7     |        0.057652 |  0.085981 |                   2.6522  | positive         |
| v55_10    |        0.053712 |  0.074988 |                   2.31309 | positive         |
| v55_1     |        0.050473 |  0.072949 |                   2.25021 | positive         |

#### LASSO
| feature   |   shap_abs_mean |      coef |   relative_importance_pct | coef_direction   |
|:----------|----------------:|----------:|--------------------------:|:-----------------|
| v55_8     |        0.183546 |  0.234823 |                   9.6377  | positive         |
| v1        |        0.161879 | -0.160543 |                   6.58907 | negative         |
| v55_14    |        0.155836 |  0.214285 |                   8.79478 | positive         |
| v521      |        0.110987 | -0.13195  |                   5.41556 | negative         |
| v55_2     |        0.093258 |  0.124654 |                   5.11611 | positive         |
| v55_3     |        0.07613  |  0.101551 |                   4.16788 | positive         |
| v55_7     |        0.069722 |  0.103982 |                   4.26768 | positive         |
| v54_2     |        0.066292 |  0.07507  |                   3.08105 | positive         |
| v55_13    |        0.053903 |  0.073083 |                   2.99949 | positive         |
| v25_6     |        0.051887 | -0.066479 |                   2.72846 | negative         |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_shap_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_relative_importance.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_details.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\Ridge_lasso\outputs\model_results\ridge_lasso_three_scenarios_report_zh.md`

