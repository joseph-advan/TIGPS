# W3 ver5 Gender Recoding to W2 Convention

Date: 2026-05-11 15:13:34

## File Updated

- `TIGPS_W3_student_studentdata_ver5.csv`

## Reason

W2 biological sex coding uses `1 = Female`, `2 = Male` based on the 2024 category mapping table (`v1`: `1. ? -> 1`, `2. ? -> 2`).
W3 ver4 encoding originally used `1 = Male`, `2 = Female` based on `ver4_encoding_codebook.csv`.
To make W2 and W3 gender coding consistent for Table 1 and downstream model interpretation, W3 column `1` was recoded to the W2 convention.

## Recoding Rule

- W3 column `1`: `1 -> 2`
- W3 column `1`: `2 -> 1`
- Other values, if present, were left unchanged.

## Final Convention After This Change

- `1 = Female`
- `2 = Male`

## Counts

| gender_code | meaning_after_recode | before_count_original_w3_convention | after_count_w2_convention |
|---:|---|---:|---:|
| 1 | Female | 3287 | 3316 |
| 2 | Male | 3316 | 3287 |


## Output Count File

- `w3_ver5_gender_recode_to_w2_convention_counts.xlsx`
