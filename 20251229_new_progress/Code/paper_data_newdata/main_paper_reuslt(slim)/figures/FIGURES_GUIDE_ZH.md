# Figures Guide

This folder contains manuscript-ready or presentation-ready figure files copied from the slim main-paper result set.

## Figure Inventory

| File | Suggested Use | What It Shows |
|:--|:--|:--|
| `05_LASSO_fig_category_relative_importance_summary.png` | Main manuscript figure | Category-level LASSO relative importance across W2 -> W2 and W2 -> W3. Best for showing that SEL / Resilience is strongest and Interpersonal Network is comparatively small. |
| `05_LASSO_fig_top20_w2_to_w2.png` | Main or supplementary figure | W2 -> W2 LASSO Top 20 feature relative importance. Best for cross-sectional feature interpretation. |
| `05_LASSO_fig_top20_w2_to_w3.png` | Main or supplementary figure | W2 -> W3 LASSO Top 20 feature relative importance. Best for longitudinal feature interpretation. |
| `05_LASSO_fig_shared_top20_relative_importance.png` | Supplementary figure | Features that appear in both W2 -> W2 and W2 -> W3 LASSO Top 20 lists. Best for showing stable predictors across tasks. |
| `06_CATEGORY_fig_relative_importance_bar.png` | Optional main or supplementary figure | Category-level interpretation bar chart. Use if a simpler domain-level figure is needed. |
| `06_CATEGORY_fig_domain_story_mean_importance.png` | Supplementary figure | Domain-story view of category importance. Useful for narrative or advisor discussion. |
| `06_CATEGORY_fig_top_interaction_candidate_variables.png` | Supplementary figure | Candidate variables for later interaction analysis based on top predictors. Useful for explaining why interaction features were selected. |

## Recommended Figure Priority

1. Use `05_LASSO_fig_category_relative_importance_summary.png` as the primary figure.
2. Use `05_LASSO_fig_top20_w2_to_w2.png` and `05_LASSO_fig_top20_w2_to_w3.png` if the paper needs task-specific feature importance figures.
3. Use `05_LASSO_fig_shared_top20_relative_importance.png` as supplementary evidence for stable predictors.
4. Use the `06_CATEGORY_*.png` figures only if the advisor wants more domain-level visual explanation.

## Notes For LLM Use

- The figures are not diagnostics; they are interpretation outputs.
- The most important figure for the main paper story is the category-level LASSO relative-importance figure.
- If the paper needs fewer figures, keep only `05_LASSO_fig_category_relative_importance_summary.png` and move the rest to supplementary material.
