# Table 1 Variable Plan Draft

This file defines how variables should be presented in W2 2024 and W3 2025 Table 1, stratified by high vs low online activity.

## Stratification Variable

- W2 online activity items: `v21_3`, `v21_4`, `v21_5`, `v21_6`
- W3 online activity items: `21-3`, `21-4`, `21-5`, `21-6`
- High Online Activity: `online_activity_sum > wave-specific median`
- Low Online Activity: `online_activity_sum <= wave-specific median`

## Presentation Rules

| Variable type | Presentation |
|---|---|
| Group size | `n` |
| Categorical | `n (%)` by response category |
| Binary | `n (%)` for the value coded `1` |
| Single-item ordinal | `mean (SD)` |
| Multi-item scale | scale score `mean (SD)` |

`p-value` compares High Online Activity vs Low Online Activity:

- Categorical variables: chi-square test.
- Binary variables: chi-square test, with Fisher's exact test if expected cell counts are below 5.
- Single-item ordinal and multi-item scale variables: Welch two-sample t-test.

## Scoring Updates

- Gender labels: `1 = Male`, `2 = Female`.
- Online activity grouping uses the strict complete-item rule.
- Parenting Practices and Parent-Child Interaction Quality reverse-coded items:
  - W2: `v6_1`, `v6_5`, `v6_6`, `v6_8`, `v6_9`
  - W3: `5-1`, `5-5`, `5-6`, `5-8`, `5-9`
- Reverse-coding method: `reversed_value = min_value + max_value - original_value`, with `min = 1` and `max = 4`.
- After reverse coding, higher parenting scale scores indicate more favorable parenting / parent-child interaction quality.

## Variables That Can Be Presented Directly as Percentages

- Gender
- Parental Marital Status / Family Structure
- Cyberbullying Victimization
- Cyberbullying Perpetration
- Physical/Offline Bullying Victimization
- Physical/Offline Bullying Perpetration

## Variables That Should Be Presented as Mean (SD)

- Perceived Social Status
- Overall Life Satisfaction
- Recent Subjective Happiness
- Perceived Effectiveness of School-based Digital/Technology Learning
- Psychological Distress Symptoms
- Positive Mental Well-being
- Self-Worth and Positive Self-Concept
- Online Peer Interaction Anxiety (FOMO)
- Delinquent and Health-Risk Behaviors
- Parenting Practices and Parent-Child Interaction Quality
- Family Cohesion and Support
- Problematic Internet Use and Internet Dependence
- Social Media Self-Presentation and Online Image Management
- Parental Involvement in Schooling and Academic Monitoring
- Social Media Use: Selective Sharing and Impression Management
- Online Social Comparison and Perspective Seeking
- Social and Emotional Learning (SEL) Competencies
- Online Coping and Support Seeking under Distress
- Self-Rated Health Status

## Confirmed Mapping Update

- Self-Rated Health Status is confirmed as W2 `v52` and W3 `51`; present as `mean (SD)`.

## Detailed Mapping

See `table1_variable_plan_draft.csv`.
