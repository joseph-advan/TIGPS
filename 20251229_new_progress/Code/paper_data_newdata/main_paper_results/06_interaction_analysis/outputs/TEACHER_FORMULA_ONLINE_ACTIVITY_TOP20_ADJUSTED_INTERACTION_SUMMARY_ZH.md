# Teacher Formula Interaction Summary: Online Activity - Top20-adjusted interaction

## 模型

`logit(P(High Psychological Distress=1)) = task-specific LASSO Top20 main effects + b2*ModeratorHigh + b3*Feature*ModeratorHigh`

## 老師公式對應

- 每一列都是一個 adjusted interaction model：先放入該任務的 LASSO Top20 主效應，再一次加入一個 `Feature x ModeratorHigh` 交互作用項。
- 因此 W2 -> W2 跑 20 個模型，W2 -> W3 跑 20 個模型，共 40 個模型。
- Moderator = 0: `intercept = b0`, `slope = b1`。
- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。
- 因為 outcome 是 binary high psychological distress，所以 B 是 log-odds coefficient。
- 連續特徵已標準化為 z-score，因此 slope 表示在控制其他 Top20 主效應後，該特徵每增加 1 SD 的 log-odds 變化。
- 這裡的 p-value 是未做多重比較校正的 exploratory interaction screening；因為總共檢查 40 個 interaction，寫論文時建議保守解讀。

## b3 interaction 顯著結果 p < .05

| Analysis Mode              | Task     | Feature                                          | Category              |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Intercept when Moderator=0 |   Slope when Moderator=0 |   Intercept when Moderator=1 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                             |
|:---------------------------|:---------|:-------------------------------------------------|:----------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-----------------------------:|-------------------------:|-----------------------------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------|
| Top20-adjusted interaction | W2 -> W3 | Reciprocal Friendship Ties, Observed Count       | Interpersonal Network |                     0.009  |                       0.0273 |                     0.1176 |                           0.0283 |                       0.2845 |                   0.009  |                       0.3118 |                   0.1266 | High Online Activity=1 has a significantly stronger risk slope compared with High Online Activity=0.       |
| Top20-adjusted interaction | W2 -> W3 | Family Cohesion and Support (Family Functioning) | Family / Parenting    |                    -0.0821 |                       0.0326 |                    -0.1103 |                           0.0497 |                       0.2773 |                  -0.0821 |                       0.3099 |                  -0.1924 | High Online Activity=1 has a significantly stronger protective slope compared with High Online Activity=0. |

## 顯著結果公式代入與解釋

### W2 -> W3: Reciprocal Friendship Ties, Observed Count

老師公式：

```text
logit(P(High Psychological Distress = 1))
= all Top20 main effects + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh
```

代入本結果：

```text
b0 = 0.2845
b1 = 0.0090
b2 = 0.0273
b3 = 0.1176, p = 0.0283

logit(P(High Psychological Distress = 1))
= Top20 main effects, including (0.0090) * Feature + (0.0273) * ModeratorHigh + (0.1176) * Feature * ModeratorHigh
```

當 `Online Activity = 0`，也就是 `Low Online Activity`：

```text
intercept = b0 = 0.2845
slope = b1 = 0.0090
```

當 `Online Activity = 1`，也就是 `High Online Activity`：

```text
intercept = b0 + b2 = 0.2845 + 0.0273 = 0.3118
slope = b1 + b3 = 0.0090 + 0.1176 = 0.1266
```

解釋：

- `b3 = 0.1176` 且 `p = 0.0283`，表示 `High Online Activity` 會顯著改變 `Reciprocal Friendship Ties, Observed Count` 與高心理困擾之間的斜率。
- `Low Online Activity` 中，在控制同一任務 Top20 其他主效應後，`Reciprocal Friendship Ties, Observed Count` 每增加 1 SD，高心理困擾的 log-odds 改變 `0.0090`，對應 OR = `1.009`。
- `High Online Activity` 中，在控制同一任務 Top20 其他主效應後，`Reciprocal Friendship Ties, Observed Count` 每增加 1 SD，高心理困擾的 log-odds 改變 `0.1266`，對應 OR = `1.135`。
- interaction OR = `exp(b3) = 1.125`。
- 整體來看，兩組都是風險斜率；在 `High Online Activity` 中，這個 feature 的斜率比 `Low Online Activity` 較強。

### W2 -> W3: Family Cohesion and Support (Family Functioning)

老師公式：

```text
logit(P(High Psychological Distress = 1))
= all Top20 main effects + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh
```

代入本結果：

```text
b0 = 0.2773
b1 = -0.0821
b2 = 0.0326
b3 = -0.1103, p = 0.0497

logit(P(High Psychological Distress = 1))
= Top20 main effects, including (-0.0821) * Feature + (0.0326) * ModeratorHigh + (-0.1103) * Feature * ModeratorHigh
```

當 `Online Activity = 0`，也就是 `Low Online Activity`：

```text
intercept = b0 = 0.2773
slope = b1 = -0.0821
```

當 `Online Activity = 1`，也就是 `High Online Activity`：

```text
intercept = b0 + b2 = 0.2773 + 0.0326 = 0.3099
slope = b1 + b3 = -0.0821 + -0.1103 = -0.1924
```

解釋：

- `b3 = -0.1103` 且 `p = 0.0497`，表示 `High Online Activity` 會顯著改變 `Family Cohesion and Support (Family Functioning)` 與高心理困擾之間的斜率。
- `Low Online Activity` 中，在控制同一任務 Top20 其他主效應後，`Family Cohesion and Support (Family Functioning)` 每增加 1 SD，高心理困擾的 log-odds 改變 `-0.0821`，對應 OR = `0.921`。
- `High Online Activity` 中，在控制同一任務 Top20 其他主效應後，`Family Cohesion and Support (Family Functioning)` 每增加 1 SD，高心理困擾的 log-odds 改變 `-0.1924`，對應 OR = `0.825`。
- interaction OR = `exp(b3) = 0.896`。
- 整體來看，兩組都是保護斜率；在 `High Online Activity` 中，這個 feature 的斜率比 `Low Online Activity` 較強。


## Outputs

- Workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_online_activity_top20_adjusted_interaction_models.xlsx`
- Diagnostics: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\diagnostics\teacher_formula_online_activity_top20_adjusted_interaction_diagnostics.json`