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
| W2 -> W3 | Baseline (untyped)  |             0.632702 |            0.011016 |       0.654059 |      0.013252 |              0.648206 |             0.010077 |           0.660432 |          0.023201 |        0.688274 |       0.012795 |               6603 |               117 |           37759 |
| W2 -> W3 | online_friend only  |             0.635731 |            0.009051 |       0.655756 |      0.009624 |              0.652056 |             0.008085 |           0.659568 |          0.012921 |        0.684352 |       0.011308 |               6603 |               117 |           20312 |
| W2 -> W3 | online_enemy only   |             0.631188 |            0.007711 |       0.646864 |      0.008748 |              0.651951 |             0.010082 |           0.642302 |          0.018168 |        0.679484 |       0.011096 |               6603 |               117 |            9412 |
| W2 -> W3 | offline_friend only |             0.630734 |            0.007108 |       0.65148  |      0.008362 |              0.646948 |             0.005304 |           0.656115 |          0.01183  |        0.683829 |       0.009043 |               6603 |               117 |           21463 |
| W2 -> W3 | offline_enemy only  |             0.629523 |            0.01279  |       0.647659 |      0.015439 |              0.648099 |             0.012406 |           0.64777  |          0.026097 |        0.679612 |       0.016446 |               6603 |               117 |           10585 |
| W2 -> W3 | friend only         |             0.635276 |            0.006157 |       0.651724 |      0.008856 |              0.654879 |             0.006739 |           0.648921 |          0.017646 |        0.68677  |       0.012279 |               6603 |               117 |           25458 |
| W2 -> W3 | enemy only          |             0.627252 |            0.012061 |       0.642637 |      0.017873 |              0.647955 |             0.008042 |           0.637986 |          0.030693 |        0.67798  |       0.015074 |               6603 |               117 |           12595 |
| W2 -> W3 | online only         |             0.634974 |            0.009189 |       0.655816 |      0.011296 |              0.650583 |             0.007052 |           0.661295 |          0.017893 |        0.686391 |       0.010186 |               6603 |               117 |           29601 |
| W2 -> W3 | offline only        |             0.629069 |            0.012604 |       0.651536 |      0.014855 |              0.643959 |             0.010275 |           0.659568 |          0.023014 |        0.685464 |       0.012986 |               6603 |               117 |           31943 |
| W2 -> W2 | Baseline (untyped)  |             0.720969 |            0.010364 |       0.740174 |      0.010791 |              0.746702 |             0.017476 |           0.734825 |          0.026648 |        0.788415 |       0.008594 |               6603 |               117 |           37759 |
| W2 -> W2 | online_friend only  |             0.717033 |            0.008017 |       0.734756 |      0.008951 |              0.74598  |             0.01298  |           0.724476 |          0.021044 |        0.788186 |       0.009353 |               6603 |               117 |           20312 |
| W2 -> W2 | online_enemy only   |             0.713248 |            0.011916 |       0.736426 |      0.015481 |              0.732425 |             0.009389 |           0.741259 |          0.031374 |        0.779675 |       0.010774 |               6603 |               117 |            9412 |
| W2 -> W2 | offline_friend only |             0.723997 |            0.011214 |       0.743052 |      0.00999  |              0.749184 |             0.015033 |           0.737343 |          0.014996 |        0.786215 |       0.009899 |               6603 |               117 |           21463 |
| W2 -> W2 | offline_enemy only  |             0.712036 |            0.019046 |       0.733125 |      0.020031 |              0.735113 |             0.015502 |           0.731469 |          0.028084 |        0.779405 |       0.013401 |               6603 |               117 |           10585 |
| W2 -> W2 | friend only         |             0.719001 |            0.010295 |       0.735862 |      0.01167  |              0.749104 |             0.012922 |           0.723636 |          0.02251  |        0.789718 |       0.009492 |               6603 |               117 |           25458 |
| W2 -> W2 | enemy only          |             0.71567  |            0.017673 |       0.737902 |      0.019255 |              0.73601  |             0.015372 |           0.74042  |          0.03108  |        0.780895 |       0.012131 |               6603 |               117 |           12595 |
| W2 -> W2 | online only         |             0.720515 |            0.009592 |       0.737891 |      0.012561 |              0.749055 |             0.008085 |           0.727552 |          0.024615 |        0.788233 |       0.007652 |               6603 |               117 |           29601 |
| W2 -> W2 | offline only        |             0.720666 |            0.009394 |       0.740523 |      0.007766 |              0.745186 |             0.01594  |           0.736503 |          0.017527 |        0.786033 |       0.008736 |               6603 |               117 |           31943 |
| W3 -> W3 | Baseline (untyped)  |             0.683724 |            0.010239 |       0.695483 |      0.012079 |              0.704749 |             0.011431 |           0.686906 |          0.021719 |        0.749986 |       0.008375 |               6603 |               119 |           35759 |
| W3 -> W3 | online_friend only  |             0.669644 |            0.006308 |       0.679768 |      0.007678 |              0.693946 |             0.011948 |           0.666763 |          0.019317 |        0.741729 |       0.007343 |               6603 |               119 |           19543 |
| W3 -> W3 | online_enemy only   |             0.676911 |            0.006466 |       0.686164 |      0.008544 |              0.701823 |             0.009981 |           0.671655 |          0.018658 |        0.743058 |       0.009158 |               6603 |               119 |           10140 |
| W3 -> W3 | offline_friend only |             0.672824 |            0.007059 |       0.685661 |      0.008495 |              0.693481 |             0.01129  |           0.678561 |          0.019445 |        0.742283 |       0.005222 |               6603 |               119 |           19972 |
| W3 -> W3 | offline_enemy only  |             0.677517 |            0.005201 |       0.688638 |      0.010727 |              0.699844 |             0.008687 |           0.678561 |          0.025941 |        0.742723 |       0.009661 |               6603 |               119 |           10633 |
| W3 -> W3 | friend only         |             0.672824 |            0.007916 |       0.685332 |      0.002955 |              0.694261 |             0.015509 |           0.677122 |          0.011424 |        0.742341 |       0.007511 |               6603 |               119 |           23700 |
| W3 -> W3 | enemy only          |             0.679334 |            0.010163 |       0.690741 |      0.010056 |              0.701382 |             0.013353 |           0.680863 |          0.018141 |        0.742287 |       0.012329 |               6603 |               119 |           12518 |
| W3 -> W3 | online only         |             0.676154 |            0.009152 |       0.686014 |      0.012922 |              0.700093 |             0.009883 |           0.673094 |          0.025324 |        0.747435 |       0.006656 |               6603 |               119 |           29438 |
| W3 -> W3 | offline only        |             0.67464  |            0.011819 |       0.688427 |      0.014553 |              0.69347  |             0.008801 |           0.683741 |          0.023154 |        0.743125 |       0.006626 |               6603 |               119 |           30424 |

## Delta vs Baseline (same task)
| task     | mode_label          |   delta_accuracy_vs_baseline |   delta_f1_vs_baseline |   delta_precision_vs_baseline |   delta_recall_vs_baseline |   delta_auc_vs_baseline |
|:---------|:--------------------|-----------------------------:|-----------------------:|------------------------------:|---------------------------:|------------------------:|
| W2 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W3 | online_friend only  |                     0.003028 |               0.001697 |                      0.00385  |                  -0.000863 |               -0.003921 |
| W2 -> W3 | online_enemy only   |                    -0.001514 |              -0.007196 |                      0.003745 |                  -0.018129 |               -0.00879  |
| W2 -> W3 | offline_friend only |                    -0.001968 |              -0.00258  |                     -0.001258 |                  -0.004317 |               -0.004445 |
| W2 -> W3 | offline_enemy only  |                    -0.003179 |              -0.0064   |                     -0.000107 |                  -0.012662 |               -0.008661 |
| W2 -> W3 | friend only         |                     0.002574 |              -0.002336 |                      0.006673 |                  -0.011511 |               -0.001504 |
| W2 -> W3 | enemy only          |                    -0.00545  |              -0.011423 |                     -0.000251 |                  -0.022446 |               -0.010294 |
| W2 -> W3 | online only         |                     0.002271 |               0.001756 |                      0.002376 |                   0.000863 |               -0.001883 |
| W2 -> W3 | offline only        |                    -0.003634 |              -0.002523 |                     -0.004247 |                  -0.000863 |               -0.00281  |
| W2 -> W2 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W2 -> W2 | online_friend only  |                    -0.003936 |              -0.005418 |                     -0.000722 |                  -0.01035  |               -0.000228 |
| W2 -> W2 | online_enemy only   |                    -0.007721 |              -0.003748 |                     -0.014277 |                   0.006434 |               -0.00874  |
| W2 -> W2 | offline_friend only |                     0.003028 |               0.002879 |                      0.002483 |                   0.002517 |               -0.0022   |
| W2 -> W2 | offline_enemy only  |                    -0.008933 |              -0.007049 |                     -0.011589 |                  -0.003357 |               -0.009009 |
| W2 -> W2 | friend only         |                    -0.001968 |              -0.004311 |                      0.002402 |                  -0.011189 |                0.001304 |
| W2 -> W2 | enemy only          |                    -0.005299 |              -0.002271 |                     -0.010692 |                   0.005594 |               -0.007519 |
| W2 -> W2 | online only         |                    -0.000454 |              -0.002283 |                      0.002354 |                  -0.007273 |               -0.000182 |
| W2 -> W2 | offline only        |                    -0.000303 |               0.000349 |                     -0.001516 |                   0.001678 |               -0.002382 |
| W3 -> W3 | Baseline (untyped)  |                     0        |               0        |                      0        |                   0        |                0        |
| W3 -> W3 | online_friend only  |                    -0.01408  |              -0.015715 |                     -0.010803 |                  -0.020144 |               -0.008257 |
| W3 -> W3 | online_enemy only   |                    -0.006813 |              -0.009319 |                     -0.002926 |                  -0.015252 |               -0.006928 |
| W3 -> W3 | offline_friend only |                    -0.010901 |              -0.009822 |                     -0.011267 |                  -0.008345 |               -0.007703 |
| W3 -> W3 | offline_enemy only  |                    -0.006207 |              -0.006845 |                     -0.004904 |                  -0.008345 |               -0.007262 |
| W3 -> W3 | friend only         |                    -0.010901 |              -0.010151 |                     -0.010488 |                  -0.009784 |               -0.007644 |
| W3 -> W3 | enemy only          |                    -0.004391 |              -0.004742 |                     -0.003366 |                  -0.006043 |               -0.007698 |
| W3 -> W3 | online only         |                    -0.00757  |              -0.009469 |                     -0.004656 |                  -0.013813 |               -0.002551 |
| W3 -> W3 | offline only        |                    -0.009084 |              -0.007056 |                     -0.011278 |                  -0.003165 |               -0.006861 |

## Best Mode by Accuracy
| task     | best_mode_by_accuracy   |   test_accuracy_mean |   test_f1_mean |   test_precision_mean |   test_recall_mean |   test_auc_mean |
|:---------|:------------------------|---------------------:|---------------:|----------------------:|-------------------:|----------------:|
| W2 -> W2 | offline_friend only     |             0.723997 |       0.743052 |              0.749184 |           0.737343 |        0.786215 |
| W3 -> W3 | Baseline (untyped)      |             0.683724 |       0.695483 |              0.704749 |           0.686906 |        0.749986 |
| W2 -> W3 | online_friend only      |             0.635731 |       0.655756 |              0.652056 |           0.659568 |        0.684352 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\model_results\graphsage_edge_type_comparison_delta.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\diagnostics\graphsage_edge_type_comparison_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\features\w2_relation_edges.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\GraphSAGE\edge_type_comparison\features\w3_relation_edges.csv`

