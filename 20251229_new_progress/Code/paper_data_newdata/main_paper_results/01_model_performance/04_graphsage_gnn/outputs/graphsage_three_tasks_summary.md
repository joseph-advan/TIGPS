# GraphSAGE Baseline (Three Tasks)

## Data
- W2: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Basic info: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`

## Graph
- Node features use the current drop + decomposition feature set from `Feature_Decomposition`.
- Edges are built from nomination columns (online/offline friend/enemy).
- GraphSAGE uses incoming neighbor aggregation with row-normalized sparse adjacency.
- Metrics are test-set mean/std over 5 random seeds, not CV5 folds.

## Results (mean/std over 5 seeds)
| task     |   test_accuracy_mean |   test_accuracy_std |   test_precision_mean |   test_precision_std |   test_recall_mean |   test_recall_std |   test_f1_mean |   test_f1_std |   test_auc_mean |   test_auc_std |   n_nodes_modeling |   n_edges_graph |   n_features_used |   target_median_cutoff |
|:---------|---------------------:|--------------------:|----------------------:|---------------------:|-------------------:|------------------:|---------------:|--------------:|----------------:|---------------:|-------------------:|----------------:|------------------:|-----------------------:|
| W2 -> W3 |             0.645117 |            0.012616 |              0.662544 |             0.009619 |           0.663022 |          0.023261 |       0.662663 |      0.015306 |        0.699477 |       0.014236 |               6603 |           37759 |                30 |                     21 |
| W2 -> W2 |             0.738077 |            0.011892 |              0.766942 |             0.012001 |           0.741538 |          0.016248 |       0.753937 |      0.011868 |        0.812578 |       0.007723 |               6603 |           37759 |                30 |                     17 |
| W3 -> W3 |             0.66374  |            0.013246 |              0.686261 |             0.012444 |           0.664748 |          0.015971 |       0.675299 |      0.01359  |        0.730201 |       0.010581 |               6603 |           35759 |                31 |                     21 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\diagnostics\graphsage_three_tasks_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w2_relation_edges_graphsage.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w3_relation_edges_graphsage.csv`

