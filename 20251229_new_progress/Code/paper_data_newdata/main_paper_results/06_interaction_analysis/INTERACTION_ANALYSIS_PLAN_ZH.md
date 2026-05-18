# 06 Teacher Formula Interaction Analysis Plan

## 研究問題

老師要看的不是單純的高低組描述，而是標準 interaction model：

```text
y = b0 + b1 * X + b2 * M + b3 * X * M
```

在本研究中，因為 outcome 是 binary high psychological distress，所以正式模型是：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + covariates
```

## 兩種 Moderator

1. **Online Activity**
   - W2 `v21_3` 到 `v21_6` 總和。
   - 依 W2 中位數切成 high / low。

2. **Problematic Internet Use**
   - W2 建構後的 `v28` 特徵。
   - 依 W2 中位數切成 high / low。
   - `v28` 本身不作為 focal feature，避免自我交互作用。

## 老師公式的對應

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

## 主要輸出欄位

```text
b0 Intercept B
b1 Feature Main Effect B
b2 Moderator Main Effect B
b3 Feature x Moderator B
b3 Feature x Moderator p-value
Intercept when Moderator=0
Slope when Moderator=0
Intercept when Moderator=1
Slope when Moderator=1
```

## 解讀重點

- `b1`：當 moderator = 0 時，Feature 對 high psychological distress 的斜率。
- `b2`：當 Feature = 0 時，高 moderator 組相對低 moderator 組的 intercept 差異。
- `b3`：interaction effect，也就是 moderator 是否改變 Feature 的斜率。
- `b1 + b3`：當 moderator = 1 時，Feature 對 high psychological distress 的斜率。

## 視覺化

`PredictedProbabilities` sheet 提供後續畫 interaction plot 的資料。可以畫兩條線：

- Moderator = 0
- Moderator = 1

Y 軸是 predicted probability of high psychological distress。
