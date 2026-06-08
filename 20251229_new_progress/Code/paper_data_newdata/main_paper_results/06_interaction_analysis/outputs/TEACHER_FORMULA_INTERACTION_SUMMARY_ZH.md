# Teacher Formula Interaction Analysis Summary

## 這次 06 的重點

這版 06 同時保留兩種老師公式 interaction models：

1. Single-feature + gender: `logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + gender_male`。
2. Top20-adjusted: `logit(P(High Psychological Distress=1)) = task-specific LASSO Top20 main effects + b2*ModeratorHigh + b3*Feature*ModeratorHigh`。

- 每個任務使用該任務自己的 LASSO Top20 作為候選 focal features。
- 每種模型都一次只加入一個 `Feature x ModeratorHigh` interaction term。
- 每種模型各跑 40 個 interaction tests：W2 -> W2 20 個，W2 -> W3 20 個。
- Moderator = 0: `intercept = b0`, `slope = b1`。
- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。
- `b3` 是真正的 interaction effect，檢查 moderator 是否改變 feature 對 high psychological distress 的斜率。
- p-value 未做多重比較校正；本段應作為 exploratory interaction screening，而不是確認性因果證據。

## Single-feature + gender interaction

### b3 interaction 顯著結果 p < .05

| Analysis Mode                       | Task     | Moderator       | Feature                                          |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                             |
|:------------------------------------|:---------|:----------------|:-------------------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------|
| Single-feature + gender interaction | W2 -> W3 | Online Activity | Family Cohesion and Support (Family Functioning) |                    -0.2947 |                        0.225 |                    -0.1117 |                           0.0361 |                  -0.2947 |                  -0.4063 | High Online Activity=1 has a significantly stronger protective slope compared with High Online Activity=0. |

## Top20-adjusted interaction

### b3 interaction 顯著結果 p < .05

| Analysis Mode              | Task     | Moderator       | Feature                                          |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                             |
|:---------------------------|:---------|:----------------|:-------------------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------|
| Top20-adjusted interaction | W2 -> W3 | Online Activity | Reciprocal Friendship Ties, Observed Count       |                     0.009  |                       0.0273 |                     0.1176 |                           0.0283 |                   0.009  |                   0.1266 | High Online Activity=1 has a significantly stronger risk slope compared with High Online Activity=0.       |
| Top20-adjusted interaction | W2 -> W3 | Online Activity | Family Cohesion and Support (Family Functioning) |                    -0.0821 |                       0.0326 |                    -0.1103 |                           0.0497 |                  -0.0821 |                  -0.1924 | High Online Activity=1 has a significantly stronger protective slope compared with High Online Activity=0. |

## Single-feature vs Top20-adjusted 對照

這張表用來判斷 interaction 是否在只控制性別時顯著，或是在控制 Top20 主效應後仍顯著。

| Task     | Feature                                          | Category              |   Single b3 Interaction B |   Single b3 Interaction p-value |   Adjusted b3 Interaction B |   Adjusted b3 Interaction p-value | Significance pattern                     |
|:---------|:-------------------------------------------------|:----------------------|--------------------------:|--------------------------------:|----------------------------:|----------------------------------:|:-----------------------------------------|
| W2 -> W3 | Reciprocal Friendship Ties, Observed Count       | Interpersonal Network |                    0.0658 |                          0.19   |                      0.1176 |                            0.0283 | Significant only in Top20-adjusted model |
| W2 -> W3 | Family Cohesion and Support (Family Functioning) | Family / Parenting    |                   -0.1117 |                          0.0361 |                     -0.1103 |                            0.0497 | Significant in both models               |

## Outputs

- Combined workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_interaction_models_combined.xlsx`
- Single-feature workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_online_activity_single_feature_interaction_models.xlsx`
- Top20-adjusted workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_online_activity_top20_adjusted_interaction_models.xlsx`