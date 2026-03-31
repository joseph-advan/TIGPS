Derived feature engineering and evaluation
========================================

Goal:
- Check whether the original 8 relationship variables can be transformed into ONE useful feature.
- Provide multiple derived feature options and evaluate their association with depression score.

Wave outputs (W2 and W3):
01_raw_plus_derived_features.csv
- student_id, depression_total, original 8 features, and all derived features.

02_derived_feature_evaluation.csv
- One row per derived feature.
- Includes: Pearson/Spearman correlation, p-values, skew, and univariate OLS R2.
- Sort by abs_spearman_rank (larger association first).

03_candidate_filter_flags.csv
- Quick rule flags to help pick candidate features.
- recommended=True means it passes all simple rules.

04_pca1_loadings_from_8features.csv
- PCA first component loading from original 8 features.
- pca1_8feat can be used as a single compressed feature.

Suggested usage:
1) Start from 02_derived_feature_evaluation.csv and focus on top 3-5 by abs_spearman_rank.
2) Prefer interpretable features first (friend_minus_enemy, enemy_ratio_of_total).
3) Use pca1_8feat only when you prefer a compact but less interpretable index.
