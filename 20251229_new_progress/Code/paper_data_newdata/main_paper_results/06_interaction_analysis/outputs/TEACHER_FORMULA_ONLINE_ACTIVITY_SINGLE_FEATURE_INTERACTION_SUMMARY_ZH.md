# Teacher Formula Interaction Summary: Online Activity - Single-feature + gender interaction

## 模型

`logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + gender_male`

## 老師公式對應

- 每一列都是一個 single-feature interaction model：只放入一個 focal Top20 feature、High Online Activity、交互作用項與性別。
- 因此 W2 -> W2 跑 20 個模型，W2 -> W3 跑 20 個模型，共 40 個模型。
- Moderator = 0: `intercept = b0`, `slope = b1`。
- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。
- 因為 outcome 是 binary high psychological distress，所以 B 是 log-odds coefficient。
- 連續特徵已標準化為 z-score，因此 slope 表示在控制性別後，該特徵每增加 1 SD 的 log-odds 變化。
- 這裡的 p-value 是未做多重比較校正的 exploratory interaction screening；因為總共檢查 40 個 interaction，寫論文時建議保守解讀。

## b3 interaction 顯著結果 p < .05

| Analysis Mode                       | Task     | Feature                                          | Category           |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Intercept when Moderator=0 |   Slope when Moderator=0 |   Intercept when Moderator=1 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                             |
|:------------------------------------|:---------|:-------------------------------------------------|:-------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-----------------------------:|-------------------------:|-----------------------------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------|
| Single-feature + gender interaction | W2 -> W3 | Family Cohesion and Support (Family Functioning) | Family / Parenting |                    -0.2947 |                        0.225 |                    -0.1117 |                           0.0361 |                       0.3002 |                  -0.2947 |                       0.5252 |                  -0.4063 | High Online Activity=1 has a significantly stronger protective slope compared with High Online Activity=0. |

## 顯著結果公式代入與解釋

### W2 -> W3: Family Cohesion and Support (Family Functioning)

老師公式：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + gender_male
```

代入本結果：

```text
b0 = 0.3002
b1 = -0.2947
b2 = 0.2250
b3 = -0.1117, p = 0.0361

logit(P(High Psychological Distress = 1))
= 0.3002 + (-0.2947) * Feature + (0.2250) * ModeratorHigh + (-0.1117) * Feature * ModeratorHigh + gender_male
```

當 `Online Activity = 0`，也就是 `Low Online Activity`：

```text
intercept = b0 = 0.3002
slope = b1 = -0.2947
```

當 `Online Activity = 1`，也就是 `High Online Activity`：

```text
intercept = b0 + b2 = 0.3002 + 0.2250 = 0.5252
slope = b1 + b3 = -0.2947 + -0.1117 = -0.4063
```

解釋：

- `b3 = -0.1117` 且 `p = 0.0361`，表示 `High Online Activity` 會顯著改變 `Family Cohesion and Support (Family Functioning)` 與高心理困擾之間的斜率。
- `Low Online Activity` 中，在控制性別後，`Family Cohesion and Support (Family Functioning)` 每增加 1 SD，高心理困擾的 log-odds 改變 `-0.2947`，對應 OR = `0.745`。
- `High Online Activity` 中，在控制性別後，`Family Cohesion and Support (Family Functioning)` 每增加 1 SD，高心理困擾的 log-odds 改變 `-0.4063`，對應 OR = `0.666`。
- interaction OR = `exp(b3) = 0.894`。
- 整體來看，兩組都是保護斜率；在 `High Online Activity` 中，這個 feature 的斜率比 `Low Online Activity` 較強。


## Outputs

- Workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_online_activity_single_feature_interaction_models.xlsx`
- Diagnostics: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\diagnostics\teacher_formula_online_activity_single_feature_interaction_diagnostics.json`