# Family Cohesion x Online Activity 2x2 Risk Test

## 目的

這個資料夾把 06 的連續交互作用結果，改成比較直覺的 2x2 組別風險檢查。

主要問題是：W2 家庭凝聚/支持較低、且 W2 網路活躍較高的學生，是否形成未來心理困擾較高的風險組別。

## 分組方式

使用 W2 predictors 建立四組：

1. High Family Cohesion + Low Online Activity
2. High Family Cohesion + High Online Activity
3. Low Family Cohesion + Low Online Activity
4. Low Family Cohesion + High Online Activity

定義：

- Family Cohesion：W2 `v5` 拆解後的 feature score。高分 = 高於 W2 中位數；低分 = 小於等於 W2 中位數。
- Online Activity：W2 `v21_3` 到 `v21_6` 加總。高分 = 高於 W2 中位數；低分 = 小於等於 W2 中位數。
- Outcome：High Psychological Distress，以各任務心理困擾分數中位數切分。

## 輸出

- `outputs/family_cohesion_online_activity_2x2_risk_test.xlsx`
- `outputs/FAMILY_COHESION_ONLINE_ACTIVITY_2X2_RISK_TEST_ZH.md`

## 解讀規則

用四組的高心理困擾比例描述哪一組風險最高；用 2x2 interaction 的 `b3` 判斷 Low Family + High Online 是否有超過兩個主效果相加之外的額外加乘效果。
