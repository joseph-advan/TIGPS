# logistic_baseline_added_Interpersonal_features

## Structure
- `run_interpersonal_feature_logistic_comparison.py`: main pipeline script.
- `outputs/features/`: generated interpersonal features and relation edge lists.
- `outputs/model_results/`: model comparison outputs.
- `outputs/diagnostics/`: feature-generation diagnostics.

## Main Outputs
- `outputs/features/interpersonal_features_w2.csv`
- `outputs/features/interpersonal_features_w3.csv`
- `outputs/model_results/logistic_median_split_interpersonal_comparison_summary.csv`
- `outputs/model_results/logistic_median_split_interpersonal_comparison_summary.md`
- `outputs/model_results/interpersonal_permutation_importance.csv`
- `outputs/model_results/logistic_median_split_interpersonal_deltas.csv`
- `outputs/model_results/logistic_median_split_interpersonal_deltas.md`

## Data Sources Used
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Roster source: W2 ver6 final aligned roster (`school_id`, `class`, `v13`) for the shared 6603-student sample.

## Run
```powershell
python run_interpersonal_feature_logistic_comparison.py
```
