# 06 Teacher Formula Interaction Models

## 目的

這個資料夾依照老師指定的 interaction model 形式重新整理 06：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + covariates
```

因為 outcome 是 binary high psychological distress，所以這裡的 B 是 logistic regression 的 log-odds coefficient。

## Moderator 定義

- Online Activity：W2 `v21_3` 到 `v21_6` 的總和，依 W2 中位數切成高低組。
- Problematic Internet Use：建構後的 W2 `v28` 特徵，依 W2 中位數切成高低組。

## 老師公式解讀

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

真正的 interaction 檢定是：

```text
b3 Feature x Moderator p-value
```

## 主要輸出

- `outputs/teacher_formula_interaction_models_combined.xlsx`
- `outputs/teacher_formula_online_activity_interaction_models.xlsx`
- `outputs/teacher_formula_problematic_internet_use_interaction_models.xlsx`
- `outputs/TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md`

## 主要 Sheet

- `TeacherFormulaCoefficients`：每個 Top20 feature 和 task 一列，包含 `b0`, `b1`, `b2`, `b3`，以及 derived intercept 和 derived slope。
- `CoefficientTermsLong`：長格式係數表。
- `PredictedProbabilities`：後續畫 interaction lines 用的 predicted probability。
- `SkippedFeatures`：記錄被排除的 feature。

## 注意事項

在 Problematic Internet Use moderator 分析中，`v28` 本身會被排除為 focal feature，因為 `v28` 已經被拿來定義高低組。
