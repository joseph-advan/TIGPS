# 論文分析流程與目前主要發現整理

## 1. 目前論文主軸

本研究原本以「運用圖神經網絡建構青少年心理健康風險預測模型：文化歸屬感的影響」作為初步方向。依據目前實際分析結果，建議論文主軸可以調整為：

> 本研究以 W2 baseline 資料預測學生當下與未來的高心理困擾風險，並比較傳統線性模型、正則化模型與 GraphSAGE 圖神經網絡模型的預測表現。結果顯示，GraphSAGE 並未明顯優於 Logistic、LASSO 或 Ridge 等線性模型，表示在目前的同儕提名網絡建構方式下，社交網絡結構對心理困擾風險預測的額外貢獻有限。進一步的特徵重要性分析顯示，SEL / Resilience、Online / Digital Life、School Context / Belonging 與 Family / Parenting 等個人與環境層面的變項，比人際網絡特徵具有更穩定且更大的預測權重。最後，本研究進一步檢驗 Online Activity 是否會調節重要保護因子與未來心理困擾風險之間的關係。

這個寫法保留原本 GNN 與 social network 的特色，但不把論文卡死在「GNN 一定要比較好」的假設上，而是把結果轉成一個更穩健的研究發現：

- GraphSAGE 沒有明顯勝過線性模型。
- 同儕提名網絡特徵在模型中的增量預測價值有限。
- SEL / Resilience、家庭支持、學校脈絡、線上生活相關因素更能解釋心理困擾風險。
- Online Activity 可以作為數位時代下的調節變項，檢驗哪些保護因子在高線上活動學生中更重要。

## 2. 建議論文整體架構

### 2.1 摘要

摘要可以按照以下邏輯寫：

1. 研究背景：青少年心理困擾與數位生活、人際網絡、家庭與學校因素都有關。
2. 研究目的：比較傳統模型與圖神經網絡模型對高心理困擾風險的預測表現，並進一步辨識重要特徵與可能的保護因子。
3. 方法：使用 W2 baseline features，建立兩個任務：W2 -> W2 與 W2 -> W3。模型包含 Logistic、Logistic + planned drop、Logistic + drop + feature decomposition、LASSO、Ridge 與 GraphSAGE。
4. 結果：GraphSAGE 未明顯優於線性模型；LASSO Top 20 顯示 SEL / Resilience 的相對重要性最高；Interpersonal Network 的相對重要性較低；Online Activity interaction 顯示 Family Cohesion 對 W3 高心理困擾的保護效果在 High Online Activity 組中更強。
5. 結論：在目前資料與網絡定義下，個人心理社會能力與家庭支持比同儕提名網絡更能預測心理困擾風險，且家庭支持可能是高線上活動學生的重要保護因子。

## 3. Methodology 應該怎麼寫

### 3.1 Data Cleaning

Data cleaning 的段落可以放在 methodology 前半段，重點不是列出所有技術細節，而是說明資料如何被整理到可分析狀態：

1. 整理 W2 與 W3 學生問卷資料。
2. 統一 student_id 格式，建立可跨年度對齊的 paired sample。
3. 針對重複提名、自我提名、無效座號等 peer nomination 資料進行清理。
4. 自我提名視為沒有提名；同一題組內重複提名同一座號只保留一次。
5. 建立 W2 與 W3 final aligned datasets，只保留兩年共同且可追蹤的學生。
6. W3 gender coding 已調整為與 W2 一致，並在模型中轉為 dummy variable：`Gender: Male (vs Female)`。

建議寫法：

> Student-level W2 and W3 datasets were cleaned and aligned using a common student identifier. Peer nomination data were screened for duplicate nominations, self-nominations, and invalid nominations. Duplicate nominations within the same nomination group were retained once, while self-nominations were treated as missing nominations. The final analytic sample included students with aligned IDs across waves. Gender coding was harmonized across W2 and W3 and represented as a male dummy variable in predictive models.

### 3.2 Feature Decomposition

這一段是 methodology 的重要部分，因為你後面的主要模型不是直接使用所有原始大題組，而是使用 drop + decomposition 版本。

可以這樣寫：

1. 有些題組本身太大，理論上可能包含不同心理構念。
2. 因此將部分題組拆成 subscales，例如 social media self-presentation、FOMO、SEL competencies。
3. 每個 subscale 使用題項平均分數。
4. 多題量表採用至少 50% valid item rule。
5. 使用 Cronbach's alpha 檢查拆分後題組的內部一致性。
6. Feature decomposition 的目的不是只追求模型 AUC，而是提升解釋性與理論對應性。

建議寫法：

> Several broad questionnaire blocks were decomposed into theoretically meaningful subscales to improve interpretability. Subscale scores were calculated as row-wise means when at least 50% of items were valid. Cronbach's alpha was used to evaluate internal consistency of multi-item subscales. This decomposition strategy was used to align model features with interpretable psychological and behavioral constructs.

### 3.3 Prediction Tasks

目前主要任務有兩個：

| Task | Feature side | Outcome side | Interpretation |
|:--|:--|:--|:--|
| W2 -> W2 | W2 features | W2 high psychological distress | Cross-sectional prediction |
| W2 -> W3 | W2 features | W3 high psychological distress | Longitudinal prediction |

建議在論文中明確說明：

- W2 -> W2 是 cross-sectional association / prediction。
- W2 -> W3 是 longitudinal risk prediction。
- 兩者都使用 W2 baseline predictors，避免把 W3 的資訊提前放進模型中。

## 4. Model Performance：為什麼先比較模型

資料來源：

`main_paper_results/01_model_performance/05_model_comparison_all/outputs/model_comparison_all_w2w2_w2w3.csv`

### 4.1 模型設計

目前比較的模型包括：

| Model | Feature set | 目的 |
|:--|:--|:--|
| Original-group Logistic (no drop) | 原始大題組，不刪題組 | 最基礎 benchmark |
| Original-group Logistic (drop selected groups) | 原始大題組，但移除 planned drop groups | 測試刪除部分題組後的 baseline |
| Decomposed Logistic | drop + decomposition | 測試拆題組後的可解釋 Logistic |
| LASSO Logistic | drop + decomposition | 特徵選擇與相對重要性 |
| Ridge Logistic | drop + decomposition | 穩定正則化係數 |
| GraphSAGE | drop + decomposition + graph edges | 測試同儕網絡圖結構是否提升預測 |

### 4.2 主要結果

目前最新結果：

| Task | Best non-GNN model | Best non-GNN AUC | GraphSAGE AUC | Interpretation |
|:--|:--|--:|--:|:--|
| W2 -> W2 | Original-group Logistic (no drop) | 0.8229 | 0.8187 | GraphSAGE 沒有明顯更好 |
| W2 -> W3 | Original-group Logistic (no drop) | 0.7141 | 0.6974 | GraphSAGE 低於最佳非 GNN |

可以寫成：

> Across both cross-sectional and longitudinal tasks, GraphSAGE did not outperform the best non-GNN models. This suggests that, under the current peer-nomination network construction, graph-based social-structure information did not provide clear incremental predictive advantage over individual-level questionnaire features.

需要注意：

- 這不能寫成「社交圈完全沒有影響」。
- 比較嚴謹的寫法是：「在目前同儕提名特徵與 GraphSAGE 設定下，社交網絡資訊沒有帶來明顯額外預測效益」。

## 5. Table 1：描述性差異與同儕提名訊號

資料來源：

- `main_paper_results/02_descriptive_table1_group_differences/outputs/01_w2_features_to_w2_distress/table1_w2_to_w2_observed_network.xlsx`
- `main_paper_results/02_descriptive_table1_group_differences/outputs/02_w2_features_to_w3_distress/table1_w2_to_w3_observed_network.xlsx`

### 5.1 Table 1 的目的

Table 1 不是要直接證明因果，也不是模型特徵重要性排序。Table 1 的功能是：

1. 描述 High Psychological Distress 與 Low Psychological Distress 兩組學生在各特徵上的平均或比例差異。
2. 初步觀察哪些變項在高低心理困擾組之間有顯著差異。
3. 為後續模型分析提供描述性背景。

### 5.2 Interpersonal features 在 Table 1 的結果

目前 12 個 observed interpersonal features 中：

| Task | p < .05 顯著數量 | p < .01 顯著數量 | Interpretation |
|:--|--:|--:|:--|
| W2 -> W2 | 8 / 12 | 5 / 12 | 橫斷面中，部分提名特徵與當下心理困擾有差異 |
| W2 -> W3 | 4 / 12 | 4 / 12 | 到縱貫預測時，顯著提名特徵減少 |

W2 -> W3 中仍顯著的 observed interpersonal features：

- Outgoing Negative Nominations, Observed Count
- Reciprocal Negative Ties, Observed Count
- Sent Positive Tie Ratio
- Sent Network Valence, Observed

可以寫成：

> Descriptive group comparisons showed that several interpersonal nomination indicators differed between high- and low-distress students in the W2 cross-sectional task. However, fewer interpersonal indicators remained significant in the W2 -> W3 longitudinal task. This pattern suggests that peer nomination features may capture concurrent social difficulties more strongly than future psychological distress risk.

需要注意：

- W2 -> W2 有比較多 interpersonal features 顯著，不能直接說「完全沒有關係」。
- 更好的說法是：「同儕提名特徵在當下心理狀態上有部分差異，但其縱貫預測訊號減弱」。

## 6. Interpersonal Incremental Modeling：同儕網絡特徵是否真的進入模型

資料來源：

`main_paper_results/03_interpersonal_incremental_modeling/outputs/interpersonal_feature_selection_summary.xlsx`

### 6.1 這一段的目的

Table 1 只能看單變項或描述性差異。接下來要問：

> 當所有個人、家庭、學校、線上生活、SEL 特徵一起進入模型後，同儕提名特徵還有沒有保留重要性？

因此 03 的重點是：

- 加入 12 個 observed interpersonal features。
- 使用 LASSO 看哪些 interpersonal features 被保留。
- 看哪些 interpersonal features 進入 Top 20。
- 看 interpersonal features 的總 relative importance 是否大。

### 6.2 最新 LASSO 結果

W2 -> W2：

- 12 個 interpersonal features 中，LASSO 選到 6 個。
- 進入 LASSO Top 20 的 interpersonal features 有 2 個：
  - Online Total Nominations, Observed Count
  - Outgoing Friendship Nominations, Observed Count
- 沒有被 LASSO 選擇的有 6 個：
  - Incoming Negative Nominations, Observed Count
  - Outgoing Negative Nominations, Observed Count
  - Received Network Valence, Observed
  - Reciprocal Negative Ties, Observed Count
  - Reciprocal Friendship Ties, Observed Count
  - Sent Network Valence, Observed

W2 -> W3：

- 12 個 interpersonal features 中，LASSO 選到 4 個。
- 進入 LASSO Top 20 的 interpersonal features 有 2 個：
  - Online Total Nominations, Observed Count
  - Reciprocal Friendship Ties, Observed Count
- 被 LASSO 選到但沒有進入 Top 20 的有 2 個：
  - Incoming Negative Nominations, Observed Count
  - Sent Network Valence, Observed
- 沒有被 LASSO 選擇的有 8 個：
  - Incoming Friendship Nominations, Observed Count
  - Offline Total Nominations, Observed Count
  - Outgoing Negative Nominations, Observed Count
  - Outgoing Friendship Nominations, Observed Count
  - Received Positive Tie Ratio
  - Received Network Valence, Observed
  - Reciprocal Negative Ties, Observed Count
  - Sent Positive Tie Ratio

### 6.3 可以怎麼解釋

> Although some interpersonal indicators showed significant group differences in Table 1, LASSO retained only a limited subset of interpersonal features after accounting for individual-, family-, school-, and digital-life predictors. This suggests that interpersonal network indicators may provide some signal, but their incremental contribution is relatively modest compared with psychological, family, and digital-life factors.

## 7. LASSO Top 20 與 Category-Level Interpretation

資料來源：

- `main_paper_results/04_feature_importance_top20/outputs/LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md`
- `main_paper_results/04_feature_importance_top20/outputs/figures/lasso_top20_category_relative_importance_summary.png`
- `main_paper_results/04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w2.png`
- `main_paper_results/04_feature_importance_top20/outputs/figures/lasso_top20_relative_importance_w2_to_w3.png`

### 7.1 Relative Importance 的定義

這裡的 Relative Importance 不是 LASSO 原生自動輸出的指標，而是用 LASSO standardized coefficients 後處理計算：

```text
Relative Importance %
= abs(standardized LASSO coefficient for feature)
  / sum(abs(standardized LASSO coefficients across all features))
  * 100
```

所以它代表的是：

> 這個特徵的標準化係數絕對值，在整體 LASSO 係數總量中佔多少比例。

不能解釋成「這個變項解釋了多少百分比的心理困擾」，而應該解釋成：

> This variable contributed a larger share of the total absolute standardized LASSO coefficient magnitude.

### 7.2 Category-level 主要結果

| Category | W2 -> W2 Relative Importance Sum % | W2 -> W3 Relative Importance Sum % | Combined Relative Importance Sum % |
|:--|--:|--:|--:|
| SEL / Resilience | 40.2882 | 33.0172 | 73.3054 |
| Online / Digital Life | 19.0510 | 22.3208 | 41.3718 |
| School Context / Belonging | 9.1944 | 9.4172 | 18.6116 |
| Family / Parenting | 7.3789 | 6.2372 | 13.6161 |
| Demographic / Social Status | 6.0151 | 6.1146 | 12.1297 |
| Interpersonal Network | 3.0419 | 5.1132 | 8.1551 |
| Bullying / Victimization | 3.6894 | 2.0191 | 5.7086 |
| Delinquency / Risk Behavior | 1.4658 | 3.3639 | 4.8296 |

### 7.3 可以怎麼寫

> Category-level LASSO Top 20 results showed that SEL / Resilience accounted for the largest share of relative importance in both W2 -> W2 and W2 -> W3 tasks. Online / Digital Life was the second largest category, followed by School Context / Belonging and Family / Parenting. In contrast, Interpersonal Network features accounted for a much smaller share of relative importance. This supports the interpretation that individual resilience and psychosocial capacities are more central predictors of psychological distress than peer nomination network indicators in the current models.

這會接到你的核心論點：

- GraphSAGE 沒有比線性模型好。
- Interpersonal features 的增量貢獻有限。
- 真正穩定重要的是 SEL / Resilience、Online / Digital Life、School Context / Belonging、Family / Parenting。

## 8. Interaction Analysis：Online Activity 是否改變保護因子的效果

資料來源：

`main_paper_results/06_interaction_analysis/outputs/TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md`

### 8.1 為什麼做 interaction

前面 LASSO Top 20 告訴我們哪些特徵重要。接下來 interaction analysis 要回答：

> 在高線上活動的學生中，某些保護因子是否更重要？

也就是從預測模型轉向應用問題：

> 在數位時代中，我們如何保護青少年的心理健康？

### 8.2 Teacher formula

使用老師建議的模型：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * Feature
  + b2 * ModeratorHigh
  + b3 * Feature * ModeratorHigh
  + covariates
```

其中：

- `Feature` 是 LASSO Top 20 中的重要特徵。
- `ModeratorHigh` 是 High Online Activity，低線上活動為 0，高線上活動為 1。
- `b1` 是 Low Online Activity 組中 Feature 的斜率。
- `b3` 是 High Online Activity 組相對於 Low Online Activity 組的斜率差異。
- `b1 + b3` 是 High Online Activity 組中 Feature 的斜率。

### 8.3 目前顯著 interaction

目前 `p < .05` 的 interaction 是：

| Task | Feature | b1 | b2 | b3 | b3 p-value |
|:--|:--|--:|--:|--:|--:|
| W2 -> W3 | Family Cohesion and Support (Family Functioning) | -0.2947 | 0.2250 | -0.1117 | 0.036 |

代入模型：

```text
logit(P(High Psychological Distress = 1))
= 0.3002
  + (-0.2947) * Family Cohesion
  + 0.2250 * High Online Activity
  + (-0.1117) * Family Cohesion * High Online Activity
  + covariates
```

Low Online Activity：

```text
intercept = b0 = 0.3002
slope = b1 = -0.2947
OR = exp(-0.2947) = 0.745
```

High Online Activity：

```text
intercept = b0 + b2 = 0.3002 + 0.2250 = 0.5252
slope = b1 + b3 = -0.2947 + (-0.1117) = -0.4063
OR = exp(-0.4063) = 0.666
```

Interaction：

```text
b3 = -0.1117
p = 0.036
interaction OR = exp(-0.1117) = 0.894
```

### 8.4 解釋方式

可以這樣寫：

> Family Cohesion and Support was negatively associated with future high psychological distress in both low- and high-online-activity groups. The significant interaction term indicated that this protective association was stronger among students with high online activity. Specifically, each 1-SD increase in family cohesion was associated with lower odds of future high psychological distress, with a stronger reduction in the high-online-activity group.

中文可以寫：

> 家庭凝聚與支持在低線上活動與高線上活動學生中都呈現保護效果，但此保護效果在高線上活動學生中更強。這表示對線上活動較高的學生而言，較高的家庭支持可能更能降低其未來高心理困擾風險。

需要注意：

- 這不是說「高線上活動本身是保護因子」。
- 這是在說「當學生處於高線上活動情境時，家庭支持與未來心理困擾之間的負向關聯更強」。
- 也不能直接寫成因果，除非論文語氣保守，例如「may serve as a protective factor」或「is associated with lower risk」。

## 9. 建議給教授看的主論點版本

可以把整體故事整理成下面這段：

> 本研究首先比較 Logistic、LASSO、Ridge 與 GraphSAGE 在 W2 -> W2 與 W2 -> W3 兩個任務中的心理困擾預測表現。結果顯示，GraphSAGE 並未明顯優於非 GNN 模型，表示在目前以同儕提名資料建構的網絡中，圖結構資訊沒有提供明顯額外預測效益。接著，Table 1 顯示同儕提名特徵在 W2 橫斷面高低心理困擾組之間有部分差異，但到 W2 -> W3 的縱貫預測時，顯著特徵數量減少。進一步以 LASSO 檢視特徵選擇後，只有少數 interpersonal features 進入 Top 20，且 Interpersonal Network 類別的 relative importance 明顯低於 SEL / Resilience、Online / Digital Life、School Context / Belonging 與 Family / Parenting。最後，interaction analysis 顯示 Family Cohesion and Support 對未來高心理困擾具有保護效果，且此保護效果在 High Online Activity 組中更強。整體而言，本研究結果支持：青少年的心理困擾風險不僅與數位生活有關，更與個人 SEL / resilience capacity、家庭支持與學校脈絡密切相關；相比之下，同儕提名網絡特徵在目前模型中的增量預測貢獻較有限。

## 10. 建議問教授的問題

可以直接拿下面幾個問題問教授：

1. 論文主軸是否可以從「GNN 預測模型」調整為「比較 GNN 與線性模型後，發現個人與家庭/學校特徵比同儕網絡特徵更具預測力」？
2. Table 1 是否要保留 interpersonal features 的 p-value 與 effect size，用來支持「同儕網絡在橫斷面有部分差異，但縱貫預測訊號較弱」？
3. LASSO Top 20 是否可以作為後續 category-level interpretation 的主要依據？
4. Relative Importance 是否可以用 standardized LASSO coefficients 的絕對值比例來呈現？
5. Interaction analysis 是否聚焦在 Online Activity 作為 moderator，並只討論 p < .05 的顯著 interaction？
6. Family Cohesion x High Online Activity 的結果，是否可以作為論文最後的應用性發現：對高線上活動學生而言，家庭支持可能是更重要的保護因子？

## 11. 目前最適合的論文結果順序

建議 Results 章節按照以下順序：

1. Model Performance Comparison
   - 說明 Logistic / Ridge / LASSO / GraphSAGE 的表現。
   - 結論：GraphSAGE 沒有明顯優於線性模型。

2. Descriptive Group Differences
   - 使用 Table 1 說明 High vs Low Psychological Distress 的特徵差異。
   - 特別指出 interpersonal features 在 W2 -> W2 較明顯，但 W2 -> W3 減弱。

3. Interpersonal Incremental Modeling
   - 檢查 12 個 interpersonal features 加入模型後是否被 LASSO 保留。
   - 結論：只有少數 interpersonal features 進入 Top 20。

4. LASSO Top 20 and Category-Level Importance
   - 以 LASSO Top 20 找出最穩定重要的特徵。
   - 結論：SEL / Resilience 最重要，其次是 Online / Digital Life、School Context / Belonging、Family / Parenting。

5. Interaction Analysis
   - 檢查 Online Activity 是否調節 Top 20 特徵與心理困擾風險的關係。
   - 結論：Family Cohesion and Support 對 W3 高心理困擾的保護效果在 High Online Activity 組中更強。

## 12. 最後建議

目前這個論文邏輯是可以成立的，但建議語氣要保守：

- 不要寫「社交圈沒有影響」。
- 建議寫「同儕提名網絡特徵在本研究模型中的增量預測貢獻有限」。
- 不要寫「家庭支持一定能保護高線上活動學生」。
- 建議寫「家庭支持與較低未來心理困擾風險相關，且此關聯在高線上活動學生中更強」。

目前最穩定的核心結論是：

> GraphSAGE did not clearly outperform linear models; interpersonal network indicators had limited incremental predictive contribution; SEL / resilience and family support showed stronger and more interpretable associations with adolescent psychological distress risk, especially under high online activity.
