# Table 1 Scoring Decisions

This file records scoring decisions requested for Table 1 generation.

## Online Activity Grouping

- Rule: strict complete-item rule.
- W2 items: `v21_3`, `v21_4`, `v21_5`, `v21_6`.
- W3 items: `21-3`, `21-4`, `21-5`, `21-6`.
- High Online Activity: `online_activity_sum > wave-specific median`.
- Low Online Activity: `online_activity_sum <= wave-specific median`.
- Students missing any of the four online activity items are excluded from that wave-specific Table 1 grouping.

## Reverse Coding

Reverse-coding method:

```text
reversed_value = min_value + max_value - original_value
```

For the parenting practices / parent-child interaction quality scale, use `min = 1` and `max = 4`.

| Wave | Reverse-coded items |
|---|---|
| W2 2024 | `v6_1`, `v6_5`, `v6_6`, `v6_8`, `v6_9` |
| W3 2025 | `5-1`, `5-5`, `5-6`, `5-8`, `5-9` |

W3 items are inferred from the W2-W3 item mapping:

- `v6_1` -> `5-1`
- `v6_5` -> `5-5`
- `v6_6` -> `5-6`
- `v6_8` -> `5-8`
- `v6_9` -> `5-9`

After reverse coding, a higher parenting scale score indicates more favorable parenting / parent-child interaction quality.

## Gender Labels

| Raw value | Label |
|---:|---|
| 1 | Male |
| 2 | Female |

W2 gender column: `v1`. W3 gender column: `1`.

## Family Structure Labels

W2 family structure column: `v2`.

| W2 raw value | Label |
|---:|---|
| 1 | Married, living together |
| 2 | Married, separated due to work |
| 3 | Married, separated |
| 4 | Divorced, living separately |
| 5 | Divorced, living together |
| 6 | Unmarried, living together |
| 7 | Unmarried, living separately |
| 8 | Biological father deceased |
| 9 | Biological mother deceased |
| 10 | Both biological parents deceased |
| 11 | Other |

W3 family structure column: `3`.

| W3 raw value | Label |
|---:|---|
| 1 | Married, living together |
| 2 | Biological father deceased |
| 3 | Divorced, living separately |
| 4 | Unmarried, living separately |
| 5 | Married, separated |
| 6 | Divorced, living together |
| 7 | Married, separated due to work |
| 8 | Biological mother deceased |
| 9 | Other |
| 10 | Unmarried, living together |

Important: W2 and W3 use different numeric codes for some family-structure categories, so labels are wave-specific.

## Output Config

Machine-readable config: `table1_scoring_config.json`.

## p-value Rule

The `p-value` column compares High Online Activity vs Low Online Activity.

- Categorical variables: chi-square test.
- Binary variables: chi-square test; Fisher's exact test is used if expected cell counts are below 5.
- Single-item ordinal and multi-item scale variables: Welch two-sample t-test.
