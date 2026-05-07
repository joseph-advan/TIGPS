# Table 1 Precheck: Online Activity Groups and Reverse Items

## Online Activity Grouping

Two possible rules were checked:

- Loose rule: calculate `online_activity_sum` if at least one of the four online activity items is valid.
- Strict rule: calculate `online_activity_sum` only if all four online activity items are valid.

| Wave | Median loose | High loose | Low loose | Unclassified loose | Median strict | High strict | Low strict | Unclassified strict | Partial missing among 4 items |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W2 2024 | 15.0 | 3057 | 3546 | 0 | 15.0 | 3035 | 3511 | 57 | 57 |
| W3 2025 | 19.0 | 2986 | 3617 | 0 | 19.0 | 2986 | 3617 | 0 | 0 |

### Missingness by Wave

#### W2 2024

- All four valid: 6546
- Partially missing: 57
- All four missing: 0
- Valid item count distribution: {1: np.int64(1), 2: np.int64(5), 3: np.int64(51), 4: np.int64(6546)}
- Item missing counts: {'v21_3': np.int64(19), 'v21_4': np.int64(17), 'v21_5': np.int64(14), 'v21_6': np.int64(14)}

#### W3 2025

- All four valid: 6603
- Partially missing: 0
- All four missing: 0
- Valid item count distribution: {4: np.int64(6603)}
- Item missing counts: {'21-3': np.int64(0), '21-4': np.int64(0), '21-5': np.int64(0), '21-6': np.int64(0)}

## Reverse Item Check

The current executable reverse-item configuration file is:

- `Code/paper_data_newdata/online_activity_x_depression/reverse_items_config.json`

Current configuration status: all reverse-item lists are empty. This means the current scripts do not reverse-code any Table 1 variables unless we explicitly add a rule.

### Recommended Handling Before Final Table 1

- For descriptive Table 1, do not reverse-code any item automatically unless the codebook confirms it.
- Use raw score direction for now and document it as raw/observed item scoring.
- If the formal questionnaire codebook identifies reverse-worded items, add them before calculating scale `mean (SD)`.

### Variables Requiring Special Attention

| Variable | Current reverse config | Reason to check |
|---|---|---|
| Self-Worth and Positive Self-Concept | none | The W2/W3 matched Table 1 items are positive (`v52_1`-`v52_3`, `52-1`-`52-3`). Extra unmatched items in the broader questionnaire include negative wording, but they are not in the current matched Table 1 plan. |
| Positive Mental Well-being (WHO-5) | none | Current W3 `55-1`-`55-5` appear positively worded; W2 formal mapping should be kept to matched available items only. |
| Parenting Practices and Parent-Child Interaction Quality | none | Mixed support/conflict/monitoring content; reverse coding depends on whether the intended score is support quality or general parent interaction difficulty. Needs codebook decision. |
| Social and Emotional Learning (SEL) Competencies | none | Most matched items appear competency-positive, but some emotion-awareness items need direction confirmation from codebook. |
| Psychological Distress Symptoms | none | Usually higher score means more symptoms; no reverse coding needed if all items are symptom/problem indicators. |

## Practical Recommendation

Use the strict online activity rule for Table 1 if you want the grouping variable to be based on complete online activity information. This excludes 57 W2 students from the High/Low grouping and excludes 0 W3 students. Use the loose rule only if you want to preserve all 6603 students in both years.