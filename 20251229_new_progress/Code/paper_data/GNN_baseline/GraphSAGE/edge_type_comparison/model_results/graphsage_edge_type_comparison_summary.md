# GraphSAGE Edge-Set Comparison (single relation vs combined relations)

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
| W2 -> W3 | Baseline (untyped)  |             0.658675 |            0.014226 |       0.656948 |      0.017632 |              0.671855 |             0.014744 |           0.643338 |          0.028535 |        0.717297 |       0.014556 |               6713 |               118 |           38907 |
| W2 -> W3 | online_friend only  |             0.656441 |            0.011975 |       0.65776  |      0.011    |              0.666859 |             0.014851 |           0.649195 |          0.014717 |        0.713092 |       0.009539 |               6713 |               118 |           20899 |
| W2 -> W3 | online_enemy only   |             0.64825  |            0.006258 |       0.649865 |      0.009568 |              0.657998 |             0.005562 |           0.642167 |          0.01714  |        0.702642 |       0.015662 |               6713 |               118 |            9708 |
| W2 -> W3 | offline_friend only |             0.654505 |            0.016039 |       0.653619 |      0.015908 |              0.666893 |             0.017312 |           0.640996 |          0.017185 |        0.711714 |       0.015958 |               6713 |               118 |           22072 |
| W2 -> W3 | offline_enemy only  |             0.653165 |            0.011908 |       0.654904 |      0.013646 |              0.662855 |             0.011853 |           0.647438 |          0.020569 |        0.706886 |       0.012566 |               6713 |               118 |           10917 |
| W2 -> W3 | friend only         |             0.65242  |            0.015153 |       0.652339 |      0.016454 |              0.664065 |             0.017161 |           0.641581 |          0.024559 |        0.714026 |       0.014503 |               6713 |               118 |           26214 |
| W2 -> W3 | enemy only          |             0.652122 |            0.008176 |       0.653775 |      0.011838 |              0.661784 |             0.006615 |           0.646266 |          0.020801 |        0.703531 |       0.014859 |               6713 |               118 |           12997 |
| W2 -> W3 | online only         |             0.655547 |            0.010378 |       0.656743 |      0.01161  |              0.666102 |             0.013831 |           0.648316 |          0.022746 |        0.711268 |       0.013609 |               6713 |               118 |           30479 |
| W2 -> W3 | offline only        |             0.654058 |            0.016195 |       0.651376 |      0.020197 |              0.667898 |             0.015944 |           0.63631  |          0.031164 |        0.714411 |       0.016933 |               6713 |               118 |           32881 |
| W2 -> W2 | Baseline (untyped)  |             0.724795 |            0.008192 |       0.744277 |      0.009068 |              0.747601 |             0.00554  |           0.741047 |          0.013354 |        0.801658 |       0.008144 |               6713 |               118 |           38907 |
| W2 -> W2 | online_friend only  |             0.724646 |            0.008727 |       0.742234 |      0.009674 |              0.751212 |             0.006984 |           0.733609 |          0.015452 |        0.79972  |       0.006394 |               6713 |               118 |           20899 |
| W2 -> W2 | online_enemy only   |             0.715115 |            0.006753 |       0.735635 |      0.005195 |              0.738535 |             0.014193 |           0.733333 |          0.016634 |        0.78949  |       0.004438 |               6713 |               118 |            9708 |
| W2 -> W2 | offline_friend only |             0.727029 |            0.008918 |       0.744212 |      0.009219 |              0.754006 |             0.007311 |           0.734711 |          0.012027 |        0.803646 |       0.009899 |               6713 |               118 |           22072 |
| W2 -> W2 | offline_enemy only  |             0.715562 |            0.008632 |       0.735688 |      0.008874 |              0.739281 |             0.011623 |           0.732507 |          0.017562 |        0.78923  |       0.005017 |               6713 |               118 |           10917 |
| W2 -> W2 | friend only         |             0.730752 |            0.00606  |       0.747252 |      0.006421 |              0.75853  |             0.005588 |           0.736364 |          0.009606 |        0.805938 |       0.009275 |               6713 |               118 |           26214 |
| W2 -> W2 | enemy only          |             0.718838 |            0.003037 |       0.738725 |      0.00429  |              0.742493 |             0.01091  |           0.735537 |          0.018044 |        0.792627 |       0.002368 |               6713 |               118 |           12997 |
| W2 -> W2 | online only         |             0.728667 |            0.009907 |       0.747103 |      0.008595 |              0.753027 |             0.011067 |           0.741322 |          0.008003 |        0.797549 |       0.007594 |               6713 |               118 |           30479 |
| W2 -> W2 | offline only        |             0.721072 |            0.009749 |       0.740412 |      0.01052  |              0.744911 |             0.008083 |           0.736088 |          0.015549 |        0.798699 |       0.009716 |               6713 |               118 |           32881 |
| W3 -> W3 | Baseline (untyped)  |             0.708563 |            0.009041 |       0.703309 |      0.01012  |              0.729133 |             0.009389 |           0.679356 |          0.013578 |        0.777494 |       0.006692 |               6713 |               117 |           36754 |
| W3 -> W3 | online_friend only  |             0.707967 |            0.005252 |       0.702674 |      0.009867 |              0.728424 |             0.003629 |           0.679063 |          0.020859 |        0.780049 |       0.005086 |               6713 |               117 |           20086 |
| W3 -> W3 | online_enemy only   |             0.704542 |            0.006847 |       0.703576 |      0.011401 |              0.718286 |             0.010009 |           0.69019  |          0.025689 |        0.774767 |       0.005488 |               6713 |               117 |           10397 |
| W3 -> W3 | offline_friend only |             0.703351 |            0.007335 |       0.698349 |      0.007943 |              0.723109 |             0.007403 |           0.675256 |          0.00937  |        0.777257 |       0.005159 |               6713 |               117 |           20501 |
| W3 -> W3 | offline_enemy only  |             0.699628 |            0.00984  |       0.697402 |      0.014091 |              0.71491  |             0.010433 |           0.681406 |          0.027354 |        0.770022 |       0.005022 |               6713 |               117 |           10879 |
| W3 -> W3 | friend only         |             0.707372 |            0.00333  |       0.701722 |      0.005727 |              0.728503 |             0.00479  |           0.677013 |          0.012479 |        0.778511 |       0.004679 |               6713 |               117 |           24385 |
| W3 -> W3 | enemy only          |             0.698138 |            0.008219 |       0.696059 |      0.014346 |              0.713335 |             0.012274 |           0.68082  |          0.033065 |        0.770071 |       0.00504  |               6713 |               117 |           12854 |
| W3 -> W3 | online only         |             0.708116 |            0.006542 |       0.703798 |      0.007585 |              0.727238 |             0.008323 |           0.681991 |          0.012642 |        0.776734 |       0.00744  |               6713 |               117 |           30225 |
| W3 -> W3 | offline only        |             0.707669 |            0.005643 |       0.70121  |      0.007751 |              0.730019 |             0.003781 |           0.674671 |          0.012264 |        0.775872 |       0.004617 |               6713 |               117 |           31180 |

## Delta vs Baseline (same task)
| task     | mode_label          |   delta_accuracy_vs_baseline |   delta_f1_vs_baseline |   delta_precision_vs_baseline |   delta_recall_vs_baseline |   delta_auc_vs_baseline |
|:---------|:--------------------|-----------------------------:|-----------------------:|------------------------------:|---------------------------:|------------------------:|
| W2 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W3 | online_friend only  |                    -0.002234 |               0.000812 |                     -0.004995 |                   0.005857 |               -0.004204 |
| W2 -> W3 | online_enemy only   |                    -0.010424 |              -0.007083 |                     -0.013857 |                  -0.001171 |               -0.014655 |
| W2 -> W3 | offline_friend only |                    -0.00417  |              -0.003329 |                     -0.004962 |                  -0.002343 |               -0.005583 |
| W2 -> W3 | offline_enemy only  |                    -0.00551  |              -0.002045 |                     -0.009    |                   0.0041   |               -0.010411 |
| W2 -> W3 | friend only         |                    -0.006255 |              -0.004609 |                     -0.007789 |                  -0.001757 |               -0.003271 |
| W2 -> W3 | enemy only          |                    -0.006552 |              -0.003173 |                     -0.010071 |                   0.002928 |               -0.013765 |
| W2 -> W3 | online only         |                    -0.003127 |              -0.000205 |                     -0.005752 |                   0.004978 |               -0.006028 |
| W2 -> W3 | offline only        |                    -0.004617 |              -0.005572 |                     -0.003957 |                  -0.007028 |               -0.002886 |
| W2 -> W2 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W2 | online_friend only  |                    -0.000149 |              -0.002043 |                      0.003612 |                  -0.007438 |               -0.001938 |
| W2 -> W2 | online_enemy only   |                    -0.00968  |              -0.008642 |                     -0.009066 |                  -0.007713 |               -0.012168 |
| W2 -> W2 | offline_friend only |                     0.002234 |              -6.5e-05  |                      0.006405 |                  -0.006336 |                0.001987 |
| W2 -> W2 | offline_enemy only  |                    -0.009233 |              -0.008588 |                     -0.008319 |                  -0.00854  |               -0.012429 |
| W2 -> W2 | friend only         |                     **0.005957** |               0.002976 |                      0.010929 |                  -0.004683 |                0.00428  |
| W2 -> W2 | enemy only          |                    -0.005957 |              -0.005552 |                     -0.005108 |                  -0.00551  |               -0.009031 |
| W2 -> W2 | online only         |                     0.003872 |               0.002826 |                      0.005426 |                   0.000275 |               -0.004109 |
| W2 -> W2 | offline only        |                    -0.003723 |              -0.003865 |                     -0.00269  |                  -0.004959 |               -0.002959 |
| W3 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W3 -> W3 | online_friend only  |                    -0.000596 |              -0.000634 |                     -0.000709 |                  -0.000293 |                0.002555 |
| W3 -> W3 | online_enemy only   |                    -0.004021 |               0.000267 |                     -0.010847 |                   0.010835 |               -0.002726 |
| W3 -> W3 | offline_friend only |                    -0.005212 |              -0.004959 |                     -0.006024 |                  -0.0041   |               -0.000236 |
| W3 -> W3 | offline_enemy only  |                    -0.008935 |              -0.005907 |                     -0.014222 |                   0.00205  |               -0.007471 |
| W3 -> W3 | friend only         |                    -0.001191 |              -0.001586 |                     -0.00063  |                  -0.002343 |                0.001017 |
| W3 -> W3 | enemy only          |                    -0.010424 |              -0.007249 |                     -0.015798 |                   0.001464 |               -0.007423 |
| W3 -> W3 | online only         |                    -0.000447 |               0.00049  |                     -0.001895 |                   0.002635 |               -0.00076  |
| W3 -> W3 | offline only        |                    -0.000894 |              -0.002098 |                      0.000886 |                  -0.004685 |               -0.001622 |

## Best Mode by Accuracy
| task     | best_mode_by_accuracy   |   test_accuracy_mean |   test_f1_mean |   test_precision_mean |   test_recall_mean |   test_auc_mean |
|:---------|:------------------------|---------------------:|---------------:|----------------------:|-------------------:|----------------:|
| W2 -> W2 | friend only             |             0.730752 |       0.747252 |              0.75853  |           0.736364 |        0.805938 |
| W3 -> W3 | Baseline (untyped)      |             0.708563 |       0.703309 |              0.729133 |           0.679356 |        0.777494 |
| W2 -> W3 | Baseline (untyped)      |             0.658675 |       0.656948 |              0.671855 |           0.643338 |        0.717297 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\model_results\graphsage_edge_type_comparison_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\model_results\graphsage_edge_type_comparison_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\model_results\graphsage_edge_type_comparison_delta.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\diagnostics\graphsage_edge_type_comparison_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\features\w2_relation_edges.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\edge_type_comparison\features\w3_relation_edges.csv`

