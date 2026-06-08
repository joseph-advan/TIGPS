# V54 Revision and Main Results Rerun Summary

Date: 2026-05-20

## What Changed

The W2 SEL (`v54`) decomposition was revised after the V54 deep dive.

Old definition:

- `v54_A Self-Awareness`: `v54_1, v54_2, v54_3, v54_18`
- `v54_F Responsible Decision-Making`: `v54_17, v54_19, v54_20`

New definition:

- `v54_A Self-Awareness`: `v54_1, v54_2, v54_3`
- `v54_F Responsible Decision-Making`: `v54_17, v54_18, v54_19, v54_20`

Reason:

- `v54_18` asks whether the student knows what is right or wrong.
- Conceptually, this is closer to moral judgment / responsible decision-making than emotion or body awareness.
- Reliability supports the change: Self-Awareness alpha remains good, and Responsible Decision-Making alpha improves.

## V54 Reliability After Revision

| Subscale | Items | Cronbach alpha | Interpretation |
|---|---|---:|---|
| Self-Awareness | `v54_1, v54_2, v54_3` | 0.857 | Good |
| Self-Management | `v54_4, v54_5, v54_6` | 0.896 | Good |
| Motivation & Goal Setting | `v54_7, v54_8, v54_9` | 0.904 | Good |
| Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` | 0.834 | Good |
| Help-Seeking | `v54_12, v54_16` | 0.661 | Questionable but usable |
| Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` | 0.827 | Good |

## Feature Decomposition Performance

Only the two current main-paper tasks were rerun:

- W2 predictors -> W2 high psychological distress
- W2 predictors -> W3 high psychological distress

| Task | Drop-only CV5 AUC | Drop + revised decomposition CV5 AUC | AUC gain |
|---|---:|---:|---:|
| W2 -> W2 | 0.790897 | 0.810315 | +0.019418 |
| W2 -> W3 | 0.698156 | 0.707296 | +0.009140 |

Interpretation:

- The decomposition still improves performance over the drop-only feature set.
- The W2 -> W2 gain is small-to-moderate and meaningful for feature engineering.
- The W2 -> W3 gain is smaller but still positive.
- Compared with the pre-revision decomposition, the performance change is minimal, so the V54 revision mainly improves construct validity rather than changing model performance.

## Rerun Scope

The following folders were rerun after the V54 revision:

1. `01_model_performance`
2. `02_descriptive_table1_group_differences`
3. `03_interpersonal_incremental_modeling`
4. `04_feature_importance_top20`
5. `05_category_level_interpretation`
6. `06_interaction_analysis`

## Main Rerun Findings

### 01 Model Performance

The overall model-performance story did not change.

- Best non-GNN model remains Original-group Logistic with no-drop features.
- GraphSAGE still does not outperform the best non-GNN model.
- Decomposed Logistic / Ridge / LASSO remain close to each other.

Key comparison:

| Task | GraphSAGE AUC | Best non-GNN AUC | Best non-GNN model | GraphSAGE minus best non-GNN AUC |
|---|---:|---:|---|---:|
| W2 -> W2 | 0.812142 | 0.822924 | Original-group Logistic | -0.010782 |
| W2 -> W3 | 0.699486 | 0.714129 | Original-group Logistic | -0.014643 |

Conclusion: the paper's model-performance narrative remains stable: GNN is not clearly superior to simpler models.

### 02 Descriptive Table 1

Table 1 now reflects the revised V54 item grouping.

The SEL rows now use:

- Self-Awareness: `v54_1, v54_2, v54_3`
- Responsible Decision-Making: `v54_17, v54_18, v54_19, v54_20`

The W2 -> W3 descriptive pattern remains interpretable:

- Self-Management, Motivation/Goal Setting, Social Awareness/Relationship Skills, Help-Seeking, and Responsible Decision-Making are lower in the high-distress group.
- Self-Awareness remains higher in the high-distress group, so it should be interpreted carefully as awareness/sensitivity rather than straightforward protection.

### 03 Interpersonal Incremental Modeling

The interpersonal-feature story changed slightly.

Before the V54 revision, W2 -> W3 had no interpersonal features in the LASSO Top 20. After rerun:

| Task | LASSO-selected interpersonal features | Interpersonal features in Top 20 | Interpersonal RI sum % |
|---|---:|---:|---:|
| W2 -> W2 | 8 / 12 | 2 | 8.15% |
| W2 -> W3 | 5 / 12 | 2 | 6.09% |

However, incremental model performance still changes only minimally after adding interpersonal features. So the better conclusion is:

> Interpersonal indicators appear in some LASSO Top 20 lists after the revised decomposition, but their incremental predictive contribution remains small.

This is more cautious than saying interpersonal features have no signal.

### 04 Feature Importance Top 20

The main Top20 structure changed in a few places.

V54-related changes:

- `v54_A Self-Awareness` remains rank 2 in both W2 -> W2 and W2 -> W3, but its relative importance decreases because `v54_18` was removed.
- `v54_B Self-Management` remains important in both tasks.
- `v54_E Help-Seeking` remains important in both tasks.
- `v54_F Responsible Decision-Making` drops out of W2 -> W2 Top20 after moving `v54_18` into it.
- `v54_D Social Awareness & Relationship Skills` enters W2 -> W2 Top20.
- `v54_C Motivation & Goal Setting` enters W2 -> W3 Top20.

Added Top20 features:

| Task | Added Feature |
|---|---|
| W2 -> W2 | Online Total Nominations, Observed Count |
| W2 -> W2 | Social Feedback Dependency |
| W2 -> W2 | Social Awareness & Relationship Skills |
| W2 -> W3 | Online Total Nominations, Observed Count |
| W2 -> W3 | Reciprocal Friendship Ties, Observed Count |
| W2 -> W3 | Motivation & Goal Setting |

Removed Top20 features:

| Task | Removed Feature |
|---|---|
| W2 -> W2 | Incoming Friendship Nominations, Observed Count |
| W2 -> W2 | Cyberbullying Perpetration |
| W2 -> W2 | Responsible Decision-Making |
| W2 -> W3 | Fear of Missing Out & Social Anxiety |
| W2 -> W3 | Cyberbullying Victimization |
| W2 -> W3 | Cyberbullying Perpetration |

### 05 Category-Level Interpretation

The broad story remains stable:

- SEL / Resilience remains the dominant domain across both tasks.
- Online / Digital Life remains the second-largest domain.
- Family / Parenting remains a moderate contextual domain.

Notable changes:

- W2 -> W2 SEL relative importance decreases from 44.73% to 40.97%, but remains clearly dominant.
- W2 -> W3 SEL relative importance remains stable around 36%.
- W2 -> W3 Interpersonal Network now appears in the Top20 category summary with 2 features and 4.52% total relative importance.
- Bullying / Victimization decreases in W2 -> W3 because cyberbullying features drop out of Top20.

### 06 Interaction Analysis

This is the clearest downstream change.

#### Online Activity Moderator

Before revision, the significant result was:

- W2 -> W3: Family Cohesion x High Online Activity

After revision, the W2 -> W3 result remains the same, and one W2 -> W2 result appears:

| Task | Feature | b3 | p-value | Interpretation |
|---|---|---:|---:|---|
| W2 -> W2 | Social Feedback Dependency | -0.1032 | 0.048 | High Online Activity weakens the positive risk slope. |
| W2 -> W3 | Family Cohesion and Support | -0.1117 | 0.036 | High Online Activity strengthens the protective slope. |

The key longitudinal interaction remains stable: Family Cohesion is more protective among high-online-activity students.

#### Problematic Internet Use Moderator

Before revision, this was significant:

- W2 -> W3: Fear of Missing Out & Social Anxiety x High Problematic Internet Use, p = 0.005

After revision:

- No b3 interaction is significant at p < .05.

Reason:

- `Fear of Missing Out & Social Anxiety` is no longer in the W2 -> W3 LASSO Top20 after the V54 revision.
- Since 06 interaction analysis only tests LASSO Top20 features, that previous FOMO interaction is no longer part of the current tested feature set.

Interpretation:

> The Online Activity moderation story is stable; the Problematic Internet Use moderation story is no longer supported under the revised V54 Top20 feature set.

## Overall Conclusion

The V54 revision improves theoretical validity and reliability without materially changing model performance. The major paper-level findings remain mostly stable:

1. GNN does not outperform simpler non-GNN models.
2. SEL / Resilience remains the dominant feature domain.
3. Online / Digital Life remains important but secondary.
4. Family Cohesion x Online Activity remains the strongest longitudinal interaction story.

The main change is that the previous Problematic Internet Use x FOMO interaction should no longer be presented as a current primary result unless FOMO is included as a theory-driven interaction candidate outside the LASSO Top20 screening rule.
