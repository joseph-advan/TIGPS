# online_activity_x_depression

This folder contains a reproducible analysis pipeline for:
- Main effects of online activity and nomination exposure on depression.
- Cross-year comparison between W2 and W3 high-risk groups.
- Protective-factor tests (family cohesion, self-worth) within high-risk groups.

Detailed Chinese workflow guide:

`20251229_new_progress/Code/paper_data/online_activity_x_depression/WORKFLOW_GUIDE_ZH.md`

## Run

```powershell
python 20251229_new_progress/Code/paper_data/online_activity_x_depression/run_online_activity_x_depression.py
```

## Reverse items

If any items must be reverse-coded, edit:

`20251229_new_progress/Code/paper_data/online_activity_x_depression/reverse_items_config.json`

The script auto-creates this file on first run with empty reverse-item lists.

## Outputs

- `wave_features_w2.csv`
- `wave_features_w3.csv`
- `stage1_main_effects.csv`
- `stage2_cross_year.csv`
- `stage3_within_highrisk_protective_effects.csv`
- `stage3_interaction_models.csv`
- `analysis_report.md`
