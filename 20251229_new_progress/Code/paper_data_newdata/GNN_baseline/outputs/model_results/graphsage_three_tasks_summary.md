# GraphSAGE Baseline (Three Tasks)

## Data
- W2: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Basic info: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`

## Graph
- Edges are built from nomination columns (online/offline friend/enemy).
- GraphSAGE uses incoming neighbor aggregation with row-normalized sparse adjacency.

## Results (mean/std over 5 seeds)
| task     |   test_accuracy_mean |   test_accuracy_std |   test_f1_mean |   test_f1_std |   test_auc_mean |   test_auc_std |   n_nodes_modeling |   n_edges_graph |   n_features_used |   target_median_cutoff |
|:---------|---------------------:|--------------------:|---------------:|--------------:|----------------:|---------------:|-------------------:|----------------:|------------------:|-----------------------:|
| W2 -> W3 |             0.632702 |            0.011016 |       0.654059 |      0.013252 |        0.688274 |       0.012795 |               6603 |           37759 |               117 |                     21 |
| W2 -> W2 |             0.720969 |            0.010364 |       0.740174 |      0.010791 |        0.788415 |       0.008594 |               6603 |           37759 |               117 |                     17 |
| W3 -> W3 |             0.683724 |            0.010239 |       0.695483 |      0.012079 |        0.749986 |       0.008375 |               6603 |           35759 |               119 |                     21 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\model_results\graphsage_three_tasks_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\diagnostics\graphsage_three_tasks_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w2_relation_edges_graphsage.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\GNN_baseline\outputs\features\w3_relation_edges_graphsage.csv`

