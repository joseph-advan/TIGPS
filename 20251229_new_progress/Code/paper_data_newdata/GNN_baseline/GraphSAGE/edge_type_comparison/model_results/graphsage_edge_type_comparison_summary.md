# GraphSAGE Edge-Set Comparison (single relation vs combined relations)

## Feature Set
- Node features use the current drop + decomposition feature set from `Feature_Decomposition`.
- Edges are built from nomination columns and then subset by relation type.
- Metrics are test-set mean/std over 5 random seeds, not CV5 folds.

## Experiment Groups
- Baseline (untyped): all four relations merged into one edge type.
- online_friend only
- online_enemy only
- offline_friend only
- offline_enemy only
- friend only = online_friend + offline_friend
- enemy only = online_enemy + offline_enemy
- online only = online_friend + online_enemy
- offline only = offline_friend + offline_enemy

## Summary (5 seeds mean/std)
| task     | mode_label          |   test_accuracy_mean |   test_accuracy_std |   test_f1_mean |   test_f1_std |   test_precision_mean |   test_precision_std |   test_recall_mean |   test_recall_std |   test_auc_mean |   test_auc_std |   n_nodes_modeling |   n_features_used |   n_edges_graph |
|:---------|:--------------------|---------------------:|--------------------:|---------------:|--------------:|----------------------:|---------------------:|-------------------:|------------------:|----------------:|---------------:|-------------------:|------------------:|----------------:|
| W2 -> W3 | Baseline (untyped)  |             0.642392 |            0.012976 |       0.659885 |      0.015366 |              0.660178 |             0.010567 |           0.659856 |          0.023265 |        0.698532 |       0.013681 |               6603 |                30 |           37759 |
| W2 -> W3 | online_friend only  |             0.644512 |            0.013099 |       0.659571 |      0.016929 |              0.664325 |             0.009724 |           0.655252 |          0.026696 |        0.694965 |       0.012309 |               6603 |                30 |           20312 |
| W2 -> W3 | online_enemy only   |             0.634065 |            0.004481 |       0.651148 |      0.008798 |              0.653122 |             0.003542 |           0.649496 |          0.018796 |        0.686484 |       0.012146 |               6603 |                30 |            9412 |
| W2 -> W3 | offline_friend only |             0.640727 |            0.010987 |       0.656634 |      0.012706 |              0.660267 |             0.009918 |           0.653237 |          0.018826 |        0.695249 |       0.011746 |               6603 |                30 |           21463 |
| W2 -> W3 | offline_enemy only  |             0.638304 |            0.015279 |       0.655208 |      0.017761 |              0.656966 |             0.012755 |           0.653813 |          0.026835 |        0.689954 |       0.015053 |               6603 |                30 |           10585 |
| W2 -> W3 | friend only         |             0.644815 |            0.011364 |       0.66218  |      0.015932 |              0.662346 |             0.006918 |           0.662446 |          0.027701 |        0.695339 |       0.012263 |               6603 |                30 |           25458 |
| W2 -> W3 | enemy only          |             0.637547 |            0.009177 |       0.651607 |      0.013831 |              0.658922 |             0.006698 |           0.644892 |          0.025077 |        0.688751 |       0.013631 |               6603 |                30 |           12595 |
| W2 -> W3 | online only         |             0.642695 |            0.014283 |       0.659343 |      0.015535 |              0.661363 |             0.013244 |           0.657554 |          0.02138  |        0.696089 |       0.013273 |               6603 |                30 |           29601 |
| W2 -> W3 | offline only        |             0.641181 |            0.013499 |       0.661372 |      0.012831 |              0.657049 |             0.015282 |           0.666187 |          0.019875 |        0.695966 |       0.013921 |               6603 |                30 |           31943 |
| W2 -> W2 | Baseline (untyped)  |             0.736109 |            0.013143 |       0.752431 |      0.013699 |              0.764192 |             0.012057 |           0.741259 |          0.019898 |        0.812182 |       0.007853 |               6603 |                30 |           37759 |
| W2 -> W2 | online_friend only  |             0.735958 |            0.011584 |       0.75302  |      0.012498 |              0.76238  |             0.008981 |           0.744056 |          0.01891  |        0.809425 |       0.006461 |               6603 |                30 |           20312 |
| W2 -> W2 | online_enemy only   |             0.731416 |            0.008421 |       0.749686 |      0.00826  |              0.756524 |             0.010826 |           0.743217 |          0.014225 |        0.802771 |       0.006604 |               6603 |                30 |            9412 |
| W2 -> W2 | offline_friend only |             0.734141 |            0.006395 |       0.750811 |      0.007261 |              0.761879 |             0.004773 |           0.74014  |          0.011848 |        0.811461 |       0.009066 |               6603 |                30 |           21463 |
| W2 -> W2 | offline_enemy only  |             0.730204 |            0.013003 |       0.748226 |      0.010209 |              0.756551 |             0.018776 |           0.74042  |          0.011383 |        0.803896 |       0.010331 |               6603 |                30 |           10585 |
| W2 -> W2 | friend only         |             0.731113 |            0.010461 |       0.74739  |      0.0123   |              0.760012 |             0.006778 |           0.735385 |          0.019886 |        0.810684 |       0.009299 |               6603 |                30 |           25458 |
| W2 -> W2 | enemy only          |             0.736109 |            0.011665 |       0.752815 |      0.009978 |              0.76394  |             0.016948 |           0.742378 |          0.014492 |        0.805954 |       0.00871  |               6603 |                30 |           12595 |
| W2 -> W2 | online only         |             0.733384 |            0.011445 |       0.749711 |      0.01395  |              0.761661 |             0.006755 |           0.738462 |          0.023965 |        0.808816 |       0.005578 |               6603 |                30 |           29601 |
| W2 -> W2 | offline only        |             0.736715 |            0.012886 |       0.754036 |      0.012368 |              0.762751 |             0.014086 |           0.745734 |          0.016487 |        0.811577 |       0.008971 |               6603 |                30 |           31943 |
| W3 -> W3 | Baseline (untyped)  |             0.659349 |            0.012365 |       0.671157 |      0.013676 |              0.681791 |             0.011104 |           0.661007 |          0.018596 |        0.730065 |       0.011088 |               6603 |                31 |           35759 |
| W3 -> W3 | online_friend only  |             0.661166 |            0.006644 |       0.673967 |      0.008362 |              0.682531 |             0.007972 |           0.665899 |          0.016212 |        0.725678 |       0.007654 |               6603 |                31 |           19543 |
| W3 -> W3 | online_enemy only   |             0.667525 |            0.011741 |       0.679707 |      0.010516 |              0.689296 |             0.013113 |           0.670504 |          0.011654 |        0.72856  |       0.007903 |               6603 |                31 |           10140 |
| W3 -> W3 | offline_friend only |             0.661014 |            0.008117 |       0.67477  |      0.008377 |              0.681312 |             0.008789 |           0.668489 |          0.012364 |        0.72445  |       0.007652 |               6603 |                31 |           19972 |
| W3 -> W3 | offline_enemy only  |             0.663891 |            0.007524 |       0.67873  |      0.009751 |              0.682579 |             0.005991 |           0.675108 |          0.016616 |        0.724885 |       0.007165 |               6603 |                31 |           10633 |
| W3 -> W3 | friend only         |             0.663891 |            0.008658 |       0.677689 |      0.008021 |              0.68401  |             0.010565 |           0.671655 |          0.011632 |        0.726805 |       0.008396 |               6603 |                31 |           23700 |
| W3 -> W3 | enemy only          |             0.664345 |            0.015577 |       0.677978 |      0.01524  |              0.684462 |             0.015053 |           0.671655 |          0.016263 |        0.727395 |       0.010896 |               6603 |                31 |           12518 |
| W3 -> W3 | online only         |             0.661771 |            0.013587 |       0.674324 |      0.018256 |              0.682942 |             0.010084 |           0.666475 |          0.029675 |        0.72714  |       0.012342 |               6603 |                31 |           29438 |
| W3 -> W3 | offline only        |             0.660409 |            0.010765 |       0.673616 |      0.013145 |              0.681174 |             0.009026 |           0.666475 |          0.020377 |        0.725881 |       0.010348 |               6603 |                31 |           30424 |

## Delta vs Baseline (same task)
| task     | mode_label          |   delta_accuracy_vs_baseline |   delta_f1_vs_baseline |   delta_precision_vs_baseline |   delta_recall_vs_baseline |   delta_auc_vs_baseline |
|:---------|:--------------------|-----------------------------:|-----------------------:|------------------------------:|---------------------------:|------------------------:|
| W2 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W3 | online_friend only  |                     0.00212  |              -0.000314 |                      0.004146 |                  -0.004604 |               -0.003567 |
| W2 -> W3 | online_enemy only   |                    -0.008327 |              -0.008737 |                     -0.007057 |                  -0.01036  |               -0.012048 |
| W2 -> W3 | offline_friend only |                    -0.001665 |              -0.003251 |                      8.9e-05  |                  -0.006619 |               -0.003282 |
| W2 -> W3 | offline_enemy only  |                    -0.004088 |              -0.004677 |                     -0.003213 |                  -0.006043 |               -0.008577 |
| W2 -> W3 | friend only         |                     0.002422 |               0.002295 |                      0.002168 |                   0.00259  |               -0.003193 |
| W2 -> W3 | enemy only          |                    -0.004845 |              -0.008278 |                     -0.001256 |                  -0.014964 |               -0.009781 |
| W2 -> W3 | online only         |                     0.000303 |              -0.000542 |                      0.001185 |                  -0.002302 |               -0.002443 |
| W2 -> W3 | offline only        |                    -0.001211 |               0.001487 |                     -0.003129 |                   0.006331 |               -0.002566 |
| W2 -> W2 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W2 | online_friend only  |                    -0.000151 |               0.000589 |                     -0.001812 |                   0.002797 |               -0.002757 |
| W2 -> W2 | online_enemy only   |                    -0.004693 |              -0.002745 |                     -0.007668 |                   0.001958 |               -0.009411 |
| W2 -> W2 | offline_friend only |                    -0.001968 |              -0.00162  |                     -0.002314 |                  -0.001119 |               -0.000721 |
| W2 -> W2 | offline_enemy only  |                    -0.005905 |              -0.004205 |                     -0.007642 |                  -0.000839 |               -0.008286 |
| W2 -> W2 | friend only         |                    -0.004996 |              -0.005041 |                     -0.00418  |                  -0.005874 |               -0.001497 |
| W2 -> W2 | enemy only          |                     0        |               0.000384 |                     -0.000253 |                   0.001119 |               -0.006227 |
| W2 -> W2 | online only         |                    -0.002725 |              -0.00272  |                     -0.002531 |                  -0.002797 |               -0.003365 |
| W2 -> W2 | offline only        |                     0.000606 |               0.001605 |                     -0.001441 |                   0.004476 |               -0.000605 |
| W3 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W3 -> W3 | online_friend only  |                     0.001817 |               0.00281  |                      0.00074  |                   0.004892 |               -0.004387 |
| W3 -> W3 | online_enemy only   |                     0.008176 |               0.00855  |                      0.007505 |                   0.009496 |               -0.001505 |
| W3 -> W3 | offline_friend only |                     0.001665 |               0.003613 |                     -0.000478 |                   0.007482 |               -0.005614 |
| W3 -> W3 | offline_enemy only  |                     0.004542 |               0.007573 |                      0.000789 |                   0.014101 |               -0.00518  |
| W3 -> W3 | friend only         |                     0.004542 |               0.006532 |                      0.00222  |                   0.010647 |               -0.00326  |
| W3 -> W3 | enemy only          |                     0.004996 |               0.006821 |                      0.002671 |                   0.010647 |               -0.002669 |
| W3 -> W3 | online only         |                     0.002422 |               0.003166 |                      0.001151 |                   0.005468 |               -0.002925 |
| W3 -> W3 | offline only        |                     0.00106  |               0.002459 |                     -0.000617 |                   0.005468 |               -0.004184 |

## Best Mode by Accuracy
| task     | best_mode_by_accuracy   |   test_accuracy_mean |   test_f1_mean |   test_precision_mean |   test_recall_mean |   test_auc_mean |
|:---------|:------------------------|---------------------:|---------------:|----------------------:|-------------------:|----------------:|
| W2 -> W2 | offline only            |             0.736715 |       0.754036 |              0.762751 |           0.745734 |        0.811577 |
| W3 -> W3 | online_enemy only       |             0.667525 |       0.679707 |              0.689296 |           0.670504 |        0.72856  |
| W2 -> W3 | friend only             |             0.644815 |       0.66218  |              0.662346 |           0.662446 |        0.695339 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_delta.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\diagnostics\graphsage_edge_type_comparison_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\features\w2_relation_edges.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\features\w3_relation_edges.csv`


