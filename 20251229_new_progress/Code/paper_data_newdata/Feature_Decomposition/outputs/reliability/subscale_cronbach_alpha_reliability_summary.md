# Subscale Cronbach's Alpha Reliability Check

## Purpose

This reliability check extends the Feature_Decomposition workflow. The current main-paper plan uses W2 predictors only for W2->W2 and W2->W3 tasks, so Cronbach's alpha is calculated only for W2 configured subscales.

## Data Used

- W2 cleaned data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- Subscale config: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\Feature_Decomposition\subscale_definitions_w2_w3.json`

## Scoring and Reliability Rules

- Cronbach's alpha is calculated on complete cases for the items within each subscale.
- `N meeting >=50% valid items` is also reported because the modeling pipeline uses multi-item scale scores; this count shows how many students have enough valid item responses for a 50% valid-item rule.
- Single-item subscales cannot have Cronbach's alpha and are marked as not applicable.
- Low alpha does not automatically invalidate a subscale, but it means the item grouping should be reviewed against theory and item wording.
- W3 subscale reliability is intentionally not calculated in this output because W3 questionnaire features are not used as predictors in the current two-task design.

## Overall Summary

- Total configured subscales checked: `16`
- Single-item subscales where alpha is not applicable: `1`
- Good alpha >= 0.80: `13`
- Acceptable alpha 0.70-0.79: `1`
- Questionable alpha 0.60-0.69: `1`
- Low alpha < 0.60: `0`

## Review Flags

| Wave   | Parent Group   | Scale Code   | Scale English Name                  |   Defined Item Count |   Cronbach alpha |   Minimum corrected item-total correlation | Review Flag                     |
|:-------|:---------------|:-------------|:------------------------------------|---------------------:|-----------------:|-------------------------------------------:|:--------------------------------|
| W2     | v27            | v27_B        | Distress from Missing Online Events |                    1 |          nan     |                                    nan     | single_item_no_alpha            |
| W2     | v54            | v54_E        | Help-Seeking                        |                    2 |            0.661 |                                      0.506 | alpha_0.60_to_0.69_questionable |

## How to Use This Result

Use this as supporting evidence for the decomposition strategy. The prediction comparison shows whether splitting improves model performance; Cronbach's alpha shows whether each proposed subscale is internally coherent. If a theoretically important subscale has low alpha, it can still be retained, but the limitation should be noted and the item wording should be reviewed.

## Output Files

- `subscale_cronbach_alpha_reliability.xlsx`
- `subscale_cronbach_alpha_reliability_details.json`
