# Teacher Formula Interaction Summary: Problematic Internet Use

## 模型

`logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates`

## 老師公式對應

- Moderator = 0: `intercept = b0`, `slope = b1`。
- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。
- 因為 outcome 是 binary high psychological distress，所以 B 是 log-odds coefficient。
- 連續特徵已標準化為 z-score，因此 slope 表示該特徵每增加 1 SD 的 log-odds 變化。

## b3 interaction 顯著結果 p < .05

| Task     | Feature                              | Category              |   b1 Feature Main Effect B |   b2 Moderator Main Effect B |   b3 Feature x Moderator B |   b3 Feature x Moderator p-value |   Intercept when Moderator=0 |   Slope when Moderator=0 |   Intercept when Moderator=1 |   Slope when Moderator=1 | Teacher Formula Interpretation                                                                                       |
|:---------|:-------------------------------------|:----------------------|---------------------------:|-----------------------------:|---------------------------:|---------------------------------:|-----------------------------:|-------------------------:|-----------------------------:|-------------------------:|:---------------------------------------------------------------------------------------------------------------------|
| W2 -> W3 | Fear of Missing Out & Social Anxiety | Online / Digital Life |                     0.2583 |                       0.5998 |                    -0.1535 |                            0.005 |                       0.1351 |                   0.2583 |                       0.7349 |                   0.1047 | High Problematic Internet Use=1 has a significantly weaker risk slope compared with High Problematic Internet Use=0. |

## 顯著結果公式代入與解釋

### W2 -> W3: Fear of Missing Out & Social Anxiety

老師公式：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + covariates
```

代入本結果：

```text
b0 = 0.1351
b1 = 0.2583
b2 = 0.5998
b3 = -0.1535, p = 0.005

logit(P(High Psychological Distress = 1))
= 0.1351 + (0.2583) * Feature + (0.5998) * ModeratorHigh + (-0.1535) * Feature * ModeratorHigh + covariates
```

當 `Problematic Internet Use = 0`，也就是 `Low Problematic Internet Use`：

```text
intercept = b0 = 0.1351
slope = b1 = 0.2583
```

當 `Problematic Internet Use = 1`，也就是 `High Problematic Internet Use`：

```text
intercept = b0 + b2 = 0.1351 + 0.5998 = 0.7349
slope = b1 + b3 = 0.2583 + -0.1535 = 0.1047
```

解釋：

- `b3 = -0.1535` 且 `p = 0.005`，表示 `High Problematic Internet Use` 會顯著改變 `Fear of Missing Out & Social Anxiety` 與高心理困擾之間的斜率。
- `Low Problematic Internet Use` 中，`Fear of Missing Out & Social Anxiety` 每增加 1 SD，高心理困擾的 log-odds 改變 `0.2583`，對應 OR = `1.295`。
- `High Problematic Internet Use` 中，`Fear of Missing Out & Social Anxiety` 每增加 1 SD，高心理困擾的 log-odds 改變 `0.1047`，對應 OR = `1.110`。
- interaction OR = `exp(b3) = 0.858`。
- 整體來看，兩組都是風險斜率；在 `High Problematic Internet Use` 中，這個 feature 的斜率比 `Low Problematic Internet Use` 較弱。


## Outputs

- Workbook: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\teacher_formula_problematic_internet_use_interaction_models.xlsx`
- Diagnostics: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\06_interaction_analysis\outputs\diagnostics\teacher_formula_problematic_internet_use_interaction_diagnostics.json`