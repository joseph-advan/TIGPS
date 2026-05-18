# Paper Analysis Roadmap

## Core Research Logic

The project began with the idea of using graph neural networks to predict adolescent psychological distress from peer nomination networks and individual questionnaire features. The current analysis strategy is more precise: first evaluate whether GraphSAGE meaningfully improves prediction beyond simpler linear or regularized models, then examine which features actually explain risk.

The revised narrative is:

1. Compare model performance across Logistic, Ridge/LASSO, and GraphSAGE.
2. Use Table 1 to describe how high- and low-distress students differ, especially after adding interpersonal network indicators.
3. Test whether the 12 interpersonal indicators improve prediction when added directly to non-GNN models.
4. Use LASSO Top 20 relative importance to identify the strongest predictors.
5. Group the Top 20 predictors into interpretable domains.
6. Test teacher-formula interaction models to examine whether online activity or problematic internet use changes the slope of each LASSO Top 20 feature.
7. Use Table 1 style summaries to describe how LASSO Top 20 feature scores differ across online-activity and problematic-internet-use groups.
8. Use a 2x2 subgroup risk test to examine whether lower family cohesion plus high online activity identifies a higher-risk subgroup.
9. Extend the interpretation longitudinally using W2 predictors and W3 outcomes or distress-change groups.

## Folder Order

| Folder | Role in Paper |
|---|---|
| `00_methodology_and_data_audit` | Methods: data cleaning, ID alignment, feature construction, questionnaire decomposition, peer nomination cleaning. |
| `01_model_performance` | Step 1: compare original Logistic, decomposed Logistic, Ridge/LASSO, and GraphSAGE for W2->W2 and W2->W3. |
| `02_descriptive_table1_group_differences` | Step 2: Table 1 group differences for high vs low psychological distress, including interpersonal features. |
| `03_interpersonal_incremental_modeling` | Step 3: add the 12 interpersonal features to models and test whether they improve performance or enter LASSO Top features. |
| `04_feature_importance_top20` | Step 4: LASSO Top 20 relative importance for W2->W2 and W2->W3, with Ridge and univariate references. |
| `05_category_level_interpretation` | Step 5: group Top 20 variables into domains and visualize which domains dominate. |
| `06_interaction_analysis` | Step 6: estimate teacher-formula interaction models with b0, b1, b2, b3, derived intercepts, derived slopes, and predicted probabilities. |
| `07_` | Step 7: Table 1 style summaries of LASSO Top20 feature scores by online-activity and problematic-internet-use groups. |
| `08_family_online_2x2_risk_test` | Step 8: 2x2 subgroup risk test for W2 Family Cohesion high/low by W2 Online Activity high/low, focused on future psychological distress risk. |
| `09_longitudinal_change_analysis` | Step 9: examine W2 predictors of W3 distress and distress-change patterns. |
| `10_figures_and_manuscript_exports` | Final paper-ready tables, figures, and simplified exports. |
| `99_archive_or_supplementary` | Exploratory, older, or supplementary results. |

## Step 1. Model Performance

### Purpose

Show whether GraphSAGE provides clear predictive improvement compared with simpler models.

### Models

- Original-group Logistic baseline: uses original or minimally transformed questionnaire groups.
- Decomposed Logistic baseline: uses the current decomposed feature set.
- LASSO Logistic: regularized model used for variable selection and feature importance.
- Ridge Logistic: regularized model used as a stability and collinearity-robust comparison.
- GraphSAGE: GNN baseline using peer nomination graph structure.

### Main Tasks

- `W2 -> W2`: W2 predictors classify W2 high psychological distress.
- `W2 -> W3`: W2 predictors classify W3 high psychological distress.

### Interpretation

If GraphSAGE performs similarly to Logistic/Ridge/LASSO, the paper should not overstate GNN superiority. Instead, this result motivates a deeper feature-level analysis.

## Step 2. Descriptive Table 1 With Interpersonal Features

### Purpose

Describe whether high- and low-distress students differ on individual, online, bullying, family, SEL, and interpersonal network features.

### Interpersonal Features

The Table 1 interpersonal block should include the 12 features currently used in the revised design:

1. Online total nominations.
2. Offline total nominations.
3. Outgoing friendship nominations.
4. Incoming friendship nominations.
5. Outgoing negative nominations.
6. Incoming negative nominations.
7. Reciprocal friendship ties.
8. Reciprocal negative ties.
9. Sent positive tie ratio.
10. Received positive tie ratio.
11. Sent network valence.
12. Received network valence.

### Interpretation Limits

Table 1 is descriptive. It can show group differences, p-values, and effect sizes, but it cannot by itself prove predictive importance or causal influence.

## Step 3. Incremental Modeling With Interpersonal Features

### Purpose

Test whether interpersonal network indicators add predictive value beyond the decomposed individual-level features.

### Suggested Comparisons

- Decomposed features only.
- Decomposed features plus the 12 interpersonal features.

### Evidence Needed

Interpersonal features can be described as having limited predictive value only if several patterns align:

- Model AUC/F1 changes little after adding the 12 interpersonal features.
- LASSO rarely selects interpersonal features among the Top 20.
- Ridge relative importance for interpersonal features is low.
- Table 1 effect sizes for interpersonal features are small or inconsistent.

## Step 4. Feature Importance Top 20

### Primary Ranking

Use LASSO relative importance as the main Top 20 ranking criterion.

### Supporting Columns

Add Ridge relative importance and univariate Logistic B/p-value as reference columns.

### Required Top 20 Sets

- `W2 -> W2`: cross-sectional feature importance.
- `W2 -> W3`: longitudinal feature importance.
- Overlap list: variables that appear in both Top 20 lists.

## Step 5. Category-Level Interpretation

### Purpose

Move from individual variable names to interpretable domains.

### Suggested Categories

- SEL / social-emotional competencies.
- Resilience / self-worth / individual capacity.
- Online behavior / digital life.
- Bullying / victimization / school risk.
- Family / socioeconomic context.
- Interpersonal network indicators.
- Demographic / background.

### Figures

Recommended figures:

- LASSO Top 20 bar chart for W2->W2.
- LASSO Top 20 bar chart for W2->W3.
- Category-level summed relative importance chart.
- W2->W2 vs W2->W3 overlap or side-by-side comparison.

## Step 6. Interaction Analysis

### Research Question

In a digital world, which protective factors reduce psychological distress risk among children with high online activity?

### Main Interaction Terms

- High Online Activity x SEL.
- High Online Activity x resilience or self-worth.
- High Online Activity x bullying/victimization.
- High Online Activity x digital literacy, if a stable measure is available.

### Recommended Model

Use theory-driven Logistic regression for final interaction estimates, even if LASSO is used earlier for feature screening.

General form:

```text
High Psychological Distress
~ High Online Activity
+ Moderator
+ High Online Activity x Moderator
+ covariates
```

### Interpretation

A negative interaction coefficient suggests the moderator may buffer the association between high online activity and psychological distress. This should be visualized with predicted probability plots rather than interpreted only from coefficients.

## Step 7. Top20 Moderator Table 1

### Purpose

Describe how the LASSO Top 20 predictors differ across high/low online-activity and high/low problematic-internet-use groups. This provides descriptive context for the interaction models.

## Step 8. Family Cohesion x Online Activity 2x2 Risk Test

### Purpose

Translate the Family Cohesion x Online Activity interaction into a direct subgroup comparison. The four groups are High Family + Low Online, High Family + High Online, Low Family + Low Online, and Low Family + High Online.

### Interpretation

Use the observed high-distress percentages to describe risk ranking. Use the 2x2 interaction term only to determine whether Low Family + High Online has extra risk beyond the two main effects.

## Step 9. Longitudinal Change Analysis

### Purpose

Strengthen the argument that selected features are not only cross-sectional correlates but also relate to later psychological distress.

### Suggested Outcome Designs

- W2 features -> W3 high psychological distress.
- W2 features -> W3-W2 distress change score.
- Transition groups:
  - low distress -> low distress.
  - low distress -> high distress.
  - high distress -> low distress.
  - high distress -> high distress.

## Main Paper Takeaway

The expected paper logic is not simply that GNN works. The stronger and more coherent story is:

GraphSAGE does not substantially outperform Logistic, Ridge, or LASSO models. Interpersonal network indicators should therefore be examined directly rather than assumed to dominate prediction. Descriptive and incremental models can test whether these indicators add meaningful value. Feature importance analysis can then identify the strongest domains, likely including SEL, resilience, bullying/victimization, family context, and online behavior. Finally, interaction models can test whether SEL, resilience, or digital literacy protect children with high online activity from psychological distress.
