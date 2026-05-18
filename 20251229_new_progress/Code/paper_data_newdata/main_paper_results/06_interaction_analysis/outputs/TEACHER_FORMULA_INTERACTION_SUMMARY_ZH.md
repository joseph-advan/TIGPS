# Teacher Formula Interaction Analysis Summary

## 這次 06 的重點

這版 06 依照老師指定的公式重新整理：

`logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates`

- Moderator = 0: `intercept = b0`, `slope = b1`。
- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。
- `b3` 是真正的 interaction effect，檢查 moderator 是否改變 feature 對 high psychological distress 的斜率。

## online_activity

### b3 interaction 顯著結果 p < .05

| Task     | Moderator       | Feature                                          |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                             |
|:---------|:----------------|:-------------------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------|
| W2 -> W3 | Online Activity | Family Cohesion and Support (Family Functioning) |                    -0.2947 |                        0.225 |                    -0.1117 |                            0.036 |                  -0.2947 |                  -0.4063 | High Online Activity=1 has a significantly stronger protective slope compared with High Online Activity=0. |

### b3 interaction 邊緣顯著結果 .05 <= p < .10

| Task     | Moderator       | Feature                                                       |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                          |
|:---------|:----------------|:--------------------------------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:--------------------------------------------------------------------------------------------------------|
| W2 -> W2 | Online Activity | Sent Positive Tie Ratio                                       |                    -0.1703 |                       0.2753 |                    -0.099  |                            0.058 |                  -0.1703 |                  -0.2693 | High Online Activity=1 has a marginally stronger protective slope compared with High Online Activity=0. |
| W2 -> W3 | Online Activity | Problematic Internet Use and Internet Dependence              |                     0.4098 |                       0.1437 |                    -0.1001 |                            0.06  |                   0.4098 |                   0.3097 | High Online Activity=1 has a marginally weaker risk slope compared with High Online Activity=0.         |
| W2 -> W3 | Online Activity | Fear of Missing Out & Social Anxiety                          |                     0.3233 |                       0.2087 |                    -0.0956 |                            0.065 |                   0.3233 |                   0.2278 | High Online Activity=1 has a marginally weaker risk slope compared with High Online Activity=0.         |
| W2 -> W3 | Online Activity | Cyberbullying Perpetration (including Misinformation-related) |                     1.0059 |                       0.2638 |                    -0.3847 |                            0.096 |                   1.0059 |                   0.6212 | High Online Activity=1 has a marginally weaker risk slope compared with High Online Activity=0.         |

## problematic_internet_use

### b3 interaction 顯著結果 p < .05

| Task     | Moderator                | Feature                              |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                                       |
|:---------|:-------------------------|:-------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:---------------------------------------------------------------------------------------------------------------------|
| W2 -> W3 | Problematic Internet Use | Fear of Missing Out & Social Anxiety |                     0.2583 |                       0.5998 |                    -0.1535 |                            0.005 |                   0.2583 |                   0.1047 | High Problematic Internet Use=1 has a significantly weaker risk slope compared with High Problematic Internet Use=0. |

### b3 interaction 邊緣顯著結果 .05 <= p < .10

| Task     | Moderator                | Feature                                         |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Slope when Moderator=0 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                                                                     |
|:---------|:-------------------------|:------------------------------------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-------------------------:|-------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| W2 -> W2 | Problematic Internet Use | Incoming Friendship Nominations, Observed Count |                    -0.1131 |                       1.0481 |                     0.1026 |                            0.05  |                  -0.1131 |                  -0.0104 | High Problematic Internet Use=1 has a marginally weaker protective slope compared with High Problematic Internet Use=0.                            |
| W2 -> W2 | Problematic Internet Use | Instant Response Pressure                       |                     0.0456 |                       1.0509 |                    -0.1048 |                            0.055 |                   0.0456 |                  -0.0592 | High Problematic Internet Use=1 has a marginally shift from risk/non-protective to protective slope compared with High Problematic Internet Use=0. |
| W2 -> W2 | Problematic Internet Use | Physical/Offline Bullying Victimization         |                     0.9408 |                       1.0214 |                    -0.2267 |                            0.081 |                   0.9408 |                   0.7141 | High Problematic Internet Use=1 has a marginally weaker risk slope compared with High Problematic Internet Use=0.                                  |
| W2 -> W2 | Problematic Internet Use | Online Perspective Seeking                      |                     0.0984 |                       1.0054 |                     0.0978 |                            0.081 |                   0.0984 |                   0.1962 | High Problematic Internet Use=1 has a marginally stronger risk slope compared with High Problematic Internet Use=0.                                |
| W2 -> W3 | Problematic Internet Use | Real-life Self-Satisfaction                     |                    -0.2052 |                       0.7086 |                    -0.1015 |                            0.06  |                  -0.2052 |                  -0.3067 | High Problematic Internet Use=1 has a marginally stronger protective slope compared with High Problematic Internet Use=0.                          |
| W2 -> W3 | Problematic Internet Use | Online-Offline Discrepancy & Immersion          |                     0.2651 |                       0.5982 |                    -0.1006 |                            0.065 |                   0.2651 |                   0.1645 | High Problematic Internet Use=1 has a marginally weaker risk slope compared with High Problematic Internet Use=0.                                  |
| W2 -> W3 | Problematic Internet Use | Self-Worth and Positive Self-Concept            |                    -0.542  |                       0.5722 |                     0.0999 |                            0.077 |                  -0.542  |                  -0.4421 | High Problematic Internet Use=1 has a marginally weaker protective slope compared with High Problematic Internet Use=0.                            |

## Outputs

- Combined workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_interaction_models_combined.xlsx`
- Online Activity workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_online_activity_interaction_models.xlsx`
- Problematic Internet Use workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_problematic_internet_use_interaction_models.xlsx`