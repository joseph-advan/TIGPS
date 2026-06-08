# 07 Top20 Moderator Table 1

## Purpose

This folder creates Table 1 style comparisons for section 04 LASSO Top20 features across high-vs-low moderator groups.

## Tables

- `W2 -> W2`: Top20 feature scores by W2 Problematic Internet Use group.
- `W2 -> W3`: Top20 feature scores by W2 Problematic Internet Use group.
- `W2 -> W2`: Top20 feature scores by W2 Online Activity group.
- `W2 -> W3`: Top20 feature scores by W2 Online Activity group.

## Moderator Definitions

- Online Activity: median split of summed W2 `v21_3` to `v21_6`.
- Problematic Internet Use: median split of the constructed W2 `v28` feature.

## Statistics

- Features are summarized as `mean (SD)`.
- p-values use Welch t-test.
- Between-group difference uses Cohen's d.
- Cohen's d direction is high group mean minus low group mean.

## Note

For Problematic Internet Use tables, `v28` is skipped as a focal feature because `v28` defines the grouping variable.
