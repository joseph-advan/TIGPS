# 05_category_level_interpretation

## Purpose

Grouped interpretation and figures showing which feature categories dominate the LASSO Top 20 variables.

This folder does not retrain models. It reads the feature-importance outputs from `../04_feature_importance_top20` and converts them into domain-level interpretation for the manuscript.

## Main Outputs

Run:

```bash
python run_category_level_interpretation.py
```

Outputs:

- `outputs/category_level_interpretation.xlsx`
- `outputs/CATEGORY_LEVEL_INTERPRETATION_SUMMARY_ZH.md`
- `outputs/figures/category_level_relative_importance_bar.png`
- `outputs/figures/domain_story_mean_importance.png`
- `outputs/figures/top_interaction_candidate_variables.png`

## How this folder fits the paper

See `../PAPER_ANALYSIS_ROADMAP.md` for the full analysis sequence and interpretation logic.
