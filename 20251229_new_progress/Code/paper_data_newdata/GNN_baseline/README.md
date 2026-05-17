# GNN Baseline

This folder contains GraphSAGE experiments for the TIGPS W2/W3 peer nomination networks.

## Current Feature Set

The current scripts use the drop + decomposition feature set from `Feature_Decomposition`:

- Drop version removes the configured health/family/SES-style groups used in the current baseline.
- Decomposition splits configured multi-item groups into subscales before building node features.
- W2 self-rated health is represented as `v52_health` and is dropped in the drop version.
- W2 `v52_1` to `v52_3` are self-worth items and are retained when applicable.

## Graph Edges

Edges are built from peer nomination columns and mapped to `student_id_src -> student_id_dst` using the roster logic from the interpersonal feature pipeline.

Relation types:

- `online_friend`
- `online_enemy`
- `offline_friend`
- `offline_enemy`

## Scripts

- `run_graphsage_three_tasks.py`: runs GraphSAGE for three tasks using all relation types merged as one untyped graph.
- `run_graphsage_edge_type_comparison.py`: compares GraphSAGE performance across different edge subsets, such as friend-only, enemy-only, online-only, and offline-only.

## Evaluation

The GNN scripts report test-set mean and standard deviation over 5 random seeds. These are not CV5 folds.

Each seed uses:

- train/validation/test split
- validation early stopping
- final metrics on the held-out test set

## Main Outputs

Three-task GraphSAGE:

- `outputs/model_results/graphsage_three_tasks_summary.md`
- `outputs/model_results/graphsage_three_tasks_summary.csv`
- `outputs/model_results/graphsage_three_tasks_seed_metrics.csv`
- `outputs/diagnostics/graphsage_three_tasks_diagnostics.json`

Edge-type comparison:

- `GraphSAGE/edge_type_comparison/model_results/graphsage_edge_type_comparison_summary.md`
- `GraphSAGE/edge_type_comparison/model_results/graphsage_edge_type_comparison_summary.csv`
- `GraphSAGE/edge_type_comparison/model_results/graphsage_edge_type_comparison_delta.csv`
- `GraphSAGE/edge_type_comparison/diagnostics/graphsage_edge_type_comparison_diagnostics.json`

## Model Choice Notes

For the current research question, start with GraphSAGE as the primary GNN baseline because it is stable, scalable, and works well with sparse student nomination graphs.

Use edge-type comparison results to decide whether all relations should be merged or restricted by relation type. If the goal is to preserve online/offline and friend/enemy meaning directly inside the model, the next model to test should be a relational GNN, such as R-GCN or relation-aware GraphSAGE.
