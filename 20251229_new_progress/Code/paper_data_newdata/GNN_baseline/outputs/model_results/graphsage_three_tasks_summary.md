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
| W2 -> W3 |             0.638607 |            0.00629  |              0.658086 |             0.006842 |           0.651799 |          0.00464  |       0.654918 |      0.005283 |        0.697382 |       0.009855 |               6603 |           37759 |                33 |                     21 |
| W2 -> W2 |             0.739288 |            0.011336 |              0.766141 |             0.016739 |           0.746853 |          0.01602  |       0.756157 |      0.009968 |        0.818737 |       0.010379 |               6603 |           37759 |                33 |                     17 |
| W3 -> W3 |             0.661771 |            0.010848 |              0.684519 |             0.010269 |           0.662446 |          0.014606 |       0.673253 |      0.011426 |        0.730118 |       0.010357 |               6603 |           35759 |                31 |                     21 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\diagnostics\graphsage_three_tasks_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w2_relation_edges_graphsage.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w3_relation_edges_graphsage.csv`

