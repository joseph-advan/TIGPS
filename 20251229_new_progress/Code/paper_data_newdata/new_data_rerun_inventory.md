# paper_data_newdata New Data Rerun Inventory

Generated: 2026-05-06

## Requested New Data

Use these current cleaned aligned datasets:

- W2: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv`
- W3: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv`

These contain the same `6603` `student_id`s in the same order.

## Old Comparison Baseline

Use existing outputs under:

- `Code/paper_data`

as the old-result comparison baseline.

## Directory Inventory

### 1. `Feature_Decomposition`

Main script:

- `Feature_Decomposition/build_binary_drop_then_split_baseline.py`

Current hard-coded data:

- W2: `Data/2024data/TIGPS_W2_studentdata_ver11.csv`
- W3: `Data/2025data/W3_studentdata_ver10.csv`

Current outputs:

- `binary_drop_then_split_summary.csv`
- `binary_drop_then_split_summary.md`
- `binary_drop_then_split_details.json`

Rerun action needed:

- Change W2/W3 paths to the new cleaned aligned data.
- Rerun script.
- Compare new `summary.csv` against `Code/paper_data/Feature_Decomposition/binary_drop_then_split_summary.csv`.

### 2. `logistic_baseline`

Main scripts:

- `build_logistic_median_split_combined_with_precision_recall.py`
- `build_logistic_median_split_baseline_drop_groups.py`
- `build_regression_median_split_baseline.py`

Current hard-coded data:

- Some scripts use W2 `Data/2024data/TIGPS_W2_studentdata_ver12.csv`.
- The combined precision/recall script uses W2 `Data/2024data/TIGPS_W2_studentdata_ver13.csv`.
- W3 is generally `Data/2025data/W3_studentdata_ver11.csv`.

Current main outputs:

- `baseline_logistic_median_split_combined_summary_with_precision_recall.csv`
- `baseline_logistic_median_split_combined_summary_with_precision_recall.md`
- `baseline_logistic_median_split_combined_details_with_precision_recall.json`
- `baseline_logistic_median_split_drop_groups_classification_summary_with_precision_recall.csv`

Rerun action needed:

- Change all W2/W3 paths to the new cleaned aligned data.
- Rerun the combined precision/recall script first because it appears to be the current main baseline.
- Decide whether to also rerun the older/drop/regression scripts.
- Compare new summary CSVs against `Code/paper_data/logistic_baseline`.

### 3. `Interpersonal_features`

Core script:

- `run_interpersonal_feature_logistic_comparison.py`

Dependent scripts:

- `run_interpersonal_abcd_dsplit_comparison.py`
- `run_interpersonal_a1a2_b1b2_c1c2_d1d5_comparison.py`
- `run_interpersonal_abdg_group_comparison.py`

Current hard-coded data:

- W2: `Data/2024data/TIGPS_W2_studentdata_ver12.csv`
- W3: `Data/2025data/W3_studentdata_ver11.csv`
- Roster: `Data/otherData/W2W3_Student_Basic_Info.csv`

Current outputs:

- Feature tables:
  - `outputs/features/interpersonal_features_w2.csv`
  - `outputs/features/interpersonal_features_w3.csv`
  - `outputs/features/w2_relation_edges.csv`
  - `outputs/features/w3_relation_edges.csv`
- Model summaries:
  - `outputs/model_results/abcd_vs_drop_baseline_summary.csv`
  - `outputs/model_results/a1a2_b1b2_c1c2_d1d5_vs_drop_baseline_summary.csv`
  - additional delta/detail/report files

Important issue to clarify:

- The current core script builds peer nomination edges using `W2W3_Student_Basic_Info.csv`.
- The newly cleaned W2/W3 files already have cleaned nomination columns and final aligned `6603` IDs.
- If the analysis should preserve nominations to students outside the final aligned questionnaire roster, using `W2W3_Student_Basic_Info.csv` can still map some outside-sample nominees.
- If the analysis should only model relationships among the final 6603 students, the roster should be restricted to the final aligned sample.

Rerun action needed:

- Change W2/W3 paths to the new cleaned aligned data.
- Decide roster policy:
  - final aligned roster only, or
  - broader basic-info roster.
- Rerun core script and dependent comparison scripts.
- Compare new feature counts and model summaries against `Code/paper_data/Interpersonal_features`.

### 4. `GNN_baseline`

Main scripts:

- `run_graphsage_three_tasks.py`
- `run_graphsage_edge_type_comparison.py`

Dependency:

- Imports/reuses the `Interpersonal_features` core module.

Current outputs:

- `GraphSAGE/outputs/model_results/graphsage_three_tasks_summary.csv`
- `GraphSAGE/edge_type_comparison/model_results/graphsage_edge_type_comparison_summary.csv`
- duplicated outputs under `GNN_baseline/outputs/...`

Current hard-coded data:

- Indirectly through the Interpersonal core script:
  - W2 old path
  - W3 old path
  - basic-info roster

Rerun action needed:

- Update Interpersonal core first.
- Then rerun GNN scripts.
- Compare new GraphSAGE summaries against `Code/paper_data/GNN_baseline`.

### 5. `Ridge_lasso`

Main script:

- `run_ridge_lasso_shap_three_scenarios.py`

Current hard-coded references:

- Feature map: `Code/paper_data/features_used/W2W3_Features.csv`
- Interpersonal core: `Code/paper_data/Interpersonal_features`

Important issue:

- This script is inside `paper_data_newdata`, but it imports the core script from old `Code/paper_data/Interpersonal_features`, not from `Code/paper_data_newdata/Interpersonal_features`.
- If left unchanged, it will rerun using old paths/core behavior.

Rerun action needed:

- Point feature map to `Code/paper_data_newdata/features_used/W2W3_Features.csv`.
- Point core import to `Code/paper_data_newdata/Interpersonal_features`.
- Ensure Interpersonal core uses new W2/W3 paths.
- Rerun.
- Compare new `ridge_lasso_three_scenarios_summary.csv` and importance tables against `Code/paper_data/Ridge_lasso`.

### 6. `online_activity_x_depression`

Main script:

- `run_online_activity_x_depression.py`

Current hard-coded data:

- W2: `Data/2024data/TIGPS_W2_studentdata_ver13.csv`
- W3: `Data/2025data/W3_studentdata_ver11.csv`

Current outputs:

- `wave_features_w2.csv`
- `wave_features_w3.csv`
- `stage1_main_effects.csv`
- `stage2_cross_year.csv`
- `stage3_within_highrisk_protective_effects.csv`
- `stage3_interaction_models.csv`
- `analysis_report.md`

Rerun action needed:

- Change W2/W3 paths to the new cleaned aligned data.
- Rerun script.
- Compare all stage CSV outputs against `Code/paper_data/online_activity_x_depression`.

### 7. `data_cleaning_audit`

Files:

- `apply_w2_ver4_mapping_cleaning.py`
- mapping/audit reports

Current role:

- This appears to be an audit or transformation utility for older W2 mapping steps, not a model/analysis module that should be rerun on the final W2 ver6 / W3 ver5 pair.

Recommended handling:

- Skip for the new-data analysis rerun unless the goal is to re-audit the historical cleaning process itself.

## Key Questions Before Rerun

1. For Interpersonal and GNN analyses, should peer nomination edges be built using only the final 6603-student aligned roster, or should they use the broader `W2W3_Student_Basic_Info.csv` roster to preserve edges to classmates outside the final questionnaire sample?

2. Should I overwrite the existing outputs inside `Code/paper_data_newdata`, or should I write rerun outputs into a new subfolder such as `Code/paper_data_newdata/rerun_w2ver6_w3ver5`?

3. Should all older/secondary scripts be rerun, or only the current main result scripts?

Suggested main scripts:

- Feature decomposition: `build_binary_drop_then_split_baseline.py`
- Logistic baseline: `build_logistic_median_split_combined_with_precision_recall.py`
- Interpersonal: core plus `abcd`, `a1a2/b1b2/c1c2/d1d5`
- GNN: both GraphSAGE scripts
- Ridge/Lasso: `run_ridge_lasso_shap_three_scenarios.py`
- Online activity/depression: `run_online_activity_x_depression.py`

