# 07 Top20 Moderator Table 1

## 目的

這個資料夾針對 04 的 LASSO Top20 特徵，建立以 moderator 高低組分組的 Table 1。

## 目前產出四張表

- `W2 -> W2`：依 W2 Problematic Internet Use 高低組比較 Top20 特徵。
- `W2 -> W3`：依 W2 Problematic Internet Use 高低組比較 Top20 特徵。
- `W2 -> W2`：依 W2 Online Activity 高低組比較 Top20 特徵。
- `W2 -> W3`：依 W2 Online Activity 高低組比較 Top20 特徵。

## Moderator 定義

- Online Activity：`v21_3` 到 `v21_6` 總和，依 W2 中位數切分。
- Problematic Internet Use：建構後的 `v28` 特徵分數，依 W2 中位數切分。

## 統計呈現

- 每個 Top20 特徵以 `mean (SD)` 呈現。
- p-value 使用 Welch t-test。
- Between-group difference 使用 Cohen's d。
- Cohen's d 方向是 High group mean - Low group mean。

## 注意事項

在 Problematic Internet Use Table 1 中，`v28` 本身會被跳過，因為 `v28` 是分組依據，不適合再拿來比較高低 `v28` 組。
