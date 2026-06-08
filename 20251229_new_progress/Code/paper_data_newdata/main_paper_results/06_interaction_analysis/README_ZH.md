# 06 Teacher Formula Interaction Models

## 目的

這個資料夾用老師指定的交互作用公式，保留兩種 interaction models。

第一種是 single-feature + gender interaction model：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature
+ b2 * ModeratorHigh
+ b3 * Feature * ModeratorHigh
+ gender_male
```

第二種是 Top20-adjusted interaction model：

```text
logit(P(High Psychological Distress = 1))
= task-specific LASSO Top20 main effects
+ b2 * ModeratorHigh
+ b3 * Feature * ModeratorHigh
```

因為 outcome 是 binary high psychological distress，所以 B 是 logistic regression 的 log-odds coefficient。

兩種模型都使用該任務自己的 LASSO Top20 predictors 作為 focal interaction candidates，然後一次加入一個 `Feature x ModeratorHigh` 交互作用項。

## Moderator 定義

- Online Activity：W2 `v21_3` 到 `v21_6` 的頻率加總，並用 W2 median 分成 High / Low。

## 老師公式對應

當 `ModeratorHigh = 0`：

```text
intercept = b0
slope     = b1
```

當 `ModeratorHigh = 1`：

```text
intercept = b0 + b2
slope     = b1 + b3
```

真正要看的 interaction test 是：

```text
b3 Feature x Moderator p-value
```

它代表在控制同一任務的 Top20 主效應後，該 feature 對 high psychological distress 的斜率，是否會因為 High / Low Online Activity 而顯著不同。

## 主要輸出

- `outputs/teacher_formula_interaction_models_combined.xlsx`
- `outputs/teacher_formula_online_activity_single_feature_interaction_models.xlsx`
- `outputs/teacher_formula_online_activity_top20_adjusted_interaction_models.xlsx`
- `outputs/TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md`
- `outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_SINGLE_FEATURE_INTERACTION_SUMMARY_ZH.md`
- `outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_TOP20_ADJUSTED_INTERACTION_SUMMARY_ZH.md`

## 主要 Sheet

- `TeacherFormulaCoefficients`：每個任務的每個 Top20 feature 一列，包含 `b0`, `b1`, `b2`, `b3`, derived intercept, derived slope, adjusted feature counts, and apparent model metrics。
- `CoefficientTermsLong`：長格式係數表，包含 focal terms 與 Top20 adjustment terms。
- `PredictedProbabilities`：用於畫 interaction lines 的 predicted probability。
- `SkippedFeatures`：被排除的 feature。
- `FeatureScaling`：每個 adjusted interaction model 中，各 Top20 feature 的 scaling 資訊。
- `Single_vs_Adjusted`：在 combined workbook 中，並排比較 single-feature 與 Top20-adjusted 的 interaction 結果。

## 模型數量

- Single-feature variant：`W2 -> W2` 20 個模型，`W2 -> W3` 20 個模型。
- Top20-adjusted variant：`W2 -> W2` 20 個模型，`W2 -> W3` 20 個模型。
- 兩種模型合計：80 個模型。
