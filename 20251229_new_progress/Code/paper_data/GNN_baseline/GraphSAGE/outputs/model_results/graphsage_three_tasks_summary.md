# GraphSAGE Baseline (Three Tasks)

## Data
- W2: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver12.csv`
- W3: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver11.csv`
- Mapping: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv`
- Basic info: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\otherData\W2W3_Student_Basic_Info.csv`

## Graph
- Edges are built from nomination columns (online/offline friend/enemy).
- GraphSAGE uses incoming neighbor aggregation with row-normalized sparse adjacency.

## Results (mean/std over 5 seeds)
| task     |   test_accuracy_mean |   test_accuracy_std |   test_f1_mean |   test_f1_std |   test_auc_mean |   test_auc_std |   n_nodes_modeling |   n_edges_graph |   n_features_used |   target_median_cutoff |
|:---------|---------------------:|--------------------:|---------------:|--------------:|----------------:|---------------:|-------------------:|----------------:|------------------:|-----------------------:|
| W2 -> W3 |             0.658675 |            0.014226 |       0.656948 |      0.017632 |        0.717297 |       0.014556 |               6713 |           38907 |               118 |                     18 |
| W2 -> W2 |             0.724795 |            0.008192 |       0.744277 |      0.009068 |        0.801658 |       0.008144 |               6713 |           38907 |               118 |                     17 |
| W3 -> W3 |             0.708563 |            0.009041 |       0.703309 |      0.01012  |        0.777494 |       0.006692 |               6713 |           36754 |               117 |                     18 |

## Output Files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\model_results\graphsage_three_tasks_seed_metrics.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\model_results\graphsage_three_tasks_summary.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\diagnostics\graphsage_three_tasks_diagnostics.json`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\features\w2_relation_edges_graphsage.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\outputs\features\w3_relation_edges_graphsage.csv`

