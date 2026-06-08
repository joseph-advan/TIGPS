# 論文完整架構說明
## 使用圖神經網絡與機器學習預測青少年心理困擾風險：社交網絡、個人能力與數位生活的角色

> **使用說明**：本文件是依據你的所有分析結果整理出的論文寫作藍圖。每個章節都說明了：要寫什麼內容、語氣與方向、以及要放哪些表格或圖片。

---

## 論文主軸（建議對教授說明用）

> 本研究以 Wave 2 (W2) 基線資料預測學生當下（W2）與未來（W3）的高心理困擾風險。比較傳統線性模型（Logistic、LASSO、Ridge）與圖神經網絡模型（GraphSAGE）的預測表現後，發現 GraphSAGE 並未明顯優於線性模型，代表在目前同儕提名網絡建構下，圖結構資訊的額外預測貢獻有限。特徵重要性分析顯示，SEL / Resilience、Online / Digital Life、School Context / Belonging 與 Family / Parenting 是最主要的預測領域。最後，Interaction Analysis 顯示，家庭凝聚與支持對未來高心理困擾的保護效果在高線上活動學生中更強。

---

## 第一章：緒論（Introduction）

### 1.1 研究背景與動機

**要寫什麼：**

從公共衛生與社會現實角度出發，說明青少年心理健康問題的普遍性，以及現有研究的缺口。建議按照以下邏輯鋪陳：

1. **問題的嚴重性**：青少年心理困擾（心理健康問題、憂鬱、焦慮）是全球性公共健康議題，而台灣青少年也面臨相同挑戰。
2. **現有研究的侷限**：多數研究聚焦於單一因素（如家庭、學業壓力），較少整合個人能力（SEL）、社交網絡、數位生活等多維度因素。
3. **數位時代的新挑戰**：線上活動已成為青少年日常的一部分，但其與心理健康的交互關係尚不明確。
4. **機器學習方法的潛力**：傳統統計方法難以同時處理多個相互關聯的預測因子，機器學習方法（如 LASSO、圖神經網絡）提供了新的可能。

**語氣**：由寬到窄，從全球問題收斂到你的研究問題。

---

### 1.2 研究目的與問題

**要寫什麼：**

明確列出三個主要研究問題（RQ）：

> **RQ1**：比較傳統線性模型（Logistic、LASSO、Ridge）與圖神經網絡模型（GraphSAGE）在預測高心理困擾風險（當下與未來）上的表現差異。
>
> **RQ2**：在整合個人、家庭、學校、線上生活等多類因素後，同儕提名網絡特徵是否仍具有額外的增量預測貢獻？哪些特徵領域對心理困擾風險的預測貢獻最大？
>
> **RQ3**：線上活動程度（Online Activity）是否會調節重要保護因子（尤其是家庭支持）與未來心理困擾風險之間的關係？

---

### 1.3 研究貢獻

**要寫什麼（2-3 段）：**

1. 本研究是少數同時比較 GNN 與傳統線性模型在青少年心理健康預測上的實證研究。
2. 整合了同儕提名社交網絡資料與個人問卷資料，提供多維度的特徵重要性評估。
3. 首次在台灣青少年縱貫資料中，檢驗線上活動作為調節變項的潛在作用。

---

## 第二章：文獻回顧（Literature Review）

### 2.1 青少年心理困擾的風險與保護因子

**要寫什麼：**

回顧四個主要領域的文獻，對應到你的四大重要類別：

- **SEL / Resilience**：自我效能感、自我調節能力、社會情緒學習能力如何影響心理健康。
- **家庭支持（Family / Parenting）**：家庭凝聚力、親子關係對青少年心理困擾的保護作用。
- **學校脈絡（School Context / Belonging）**：學校歸屬感、師生關係、校園環境。
- **同儕關係（Interpersonal / Peer Network）**：正向/負向同儕提名、社交地位與心理健康的文獻。

---

### 2.2 數位生活與青少年心理健康

**要寫什麼：**

- 線上活動（社群媒體使用、網路成癮）與心理困擾的關聯。
- 問題性網路使用（Problematic Internet Use）的相關研究。
- 線上活動的調節效果：在什麼情境下，線上活動會放大或縮小某些保護因子的作用？
- 特別可以提到：數位時代中家庭支持的重要性（預鋪你最後的 interaction 發現）。

---

### 2.3 機器學習與圖神經網絡在心理健康預測的應用

**要寫什麼：**

- 傳統統計（Logistic Regression）與正則化模型（LASSO、Ridge）在心理健康預測的應用與限制。
- 圖神經網絡（GNN）在社交網絡分析的原理與應用，包括 GraphSAGE 的技術特點。
- 目前 GNN 在教育或心理健康預測中的應用文獻（如果有），以及其結果的混合性（不一定優於傳統模型）。
- 這段文獻可以預先為你的結果「GNN 未明顯優於線性模型」埋伏筆：並非 GNN 本身不好，而是在特定資料結構與特徵定義下，其額外貢獻有限。

---

## 第三章：研究方法（Methods）

### 3.1 研究設計與樣本

**要寫什麼：**

- 縱貫設計（Longitudinal Design）：Wave 2 → Wave 3 追蹤研究。
- 樣本：台灣某縣市國中生，說明 Wave 2 與 Wave 3 的樣本數（僅保留兩波均有資料且可對齊的學生）。
- 注意：你需要確認最終 analytic sample 的人數後填入。

---

### 3.2 資料清理（Data Cleaning）

**要寫什麼：**

> Student-level W2 and W3 datasets were cleaned and aligned using a common student identifier. Peer nomination data were screened for duplicate nominations, self-nominations, and invalid nominations. Duplicate nominations within the same nomination group were retained once, while self-nominations were treated as missing nominations. The final analytic sample included students with aligned IDs across waves. Gender coding was harmonized across W2 and W3 and represented as a male dummy variable (Gender: Male vs. Female) in predictive models.

主要說明六個步驟：
1. 整理 W2 與 W3 學生問卷資料。
2. 統一 student_id 格式，建立跨年度可對齊的 paired sample。
3. 針對重複提名、自我提名、無效座號等 peer nomination 資料進行清理。
4. 自我提名視為沒有提名；同一題組內重複提名同一座號只保留一次。
5. 建立 W2 與 W3 final aligned datasets，只保留兩年共同且可追蹤的學生。
6. W3 gender coding 已調整為與 W2 一致，模型中轉為 dummy variable：`Gender: Male (vs. Female)`。

**參考檔案**：`01_METHOD_data_cleaning_detailed_ZH.md`

---

### 3.3 測量工具與特徵建構（Measures / Feature Inventory）

**要寫什麼：**

這一段要說明你的預測變項（Predictors）、結果變項（Outcome）與調節變項（Moderator）各是什麼。

建議用表格形式呈現（**放在論文中作為 Appendix Table 或 Methods Table**）：

#### 結果變項（Outcome）
- **W2 High Psychological Distress**：以 W2 測量的心理困擾量表分數，dichotomize 為高/低（使用哪個切點需說明）。
- **W3 High Psychological Distress**：以 W3 測量的心理困擾量表分數，dichotomize 為高/低。

#### 調節變項（Moderator）
- **High Online Activity**：以 W2 的線上活動頻率/總量 dichotomize 為高/低（說明分切點）。

#### 預測變項（Predictors）——依類別
分成以下幾類說明，可以在 Methods 文字中描述主要大類，並在附錄放完整 feature list：

| 類別 | 代表量表 | 量表說明 |
|:--|:--|:--|
| SEL / Resilience | v52（Self-Worth）, v54_A（Self-Awareness）, v54_B（Self-Management）, v54_E（Help-Seeking）等 | 社會情緒能力、自我效能、韌性 |
| Online / Digital Life | v28（Problematic Internet Use）, v26_B（Online Perspective Seeking）, v22（Online Coping）等 | 線上活動模式、網路使用習慣 |
| School Context / Belonging | 學校歸屬感、師生關係相關量表 | 學校情境因素 |
| Family / Parenting | v5（Family Cohesion and Support）等 | 家庭支持與親職功能 |
| Interpersonal Network | 12 個 observed peer nomination features（Friendship, Negative, Reciprocal 等） | 同儕提名網絡特徵 |
| Demographic / Social Status | 性別（Gender: Male dummy）等 | 背景控制變項 |
| Bullying / Victimization | 霸凌受害相關量表 | 校園霸凌經歷 |
| Delinquency / Risk Behavior | 偏差行為相關量表 | 高風險行為 |

**參考檔案**：`01_METHOD_feature_inventory_ZH.md`

---

### 3.4 特徵拆分與信度分析（Feature Decomposition & Reliability）

**要寫什麼：**

> Several broad questionnaire blocks were decomposed into theoretically meaningful subscales to improve interpretability. Subscale scores were calculated as row-wise means when at least 50% of items were valid. Cronbach's alpha was used to evaluate internal consistency of multi-item subscales. This decomposition strategy was adopted to align model features with interpretable psychological and behavioral constructs rather than to solely maximize model AUC.

重點說明：
1. 部分大型題組包含多個理論上不同的心理構念，因此進行拆分。
2. 例如：Social Media Self-Presentation → 拆成 v23_A、v23_B；SEL Competencies → 拆成 v54_A（自我覺察）、v54_B（自我管理）、v54_C（動機設定）、v54_D（社會覺察）、v54_E（求助行為）。
3. 量表分數以各題平均計算，至少 50% 題項有效才計算。
4. 使用 Cronbach's alpha 評估拆分後量表的內部一致性。

**📋 建議放一個 Methods Table**：列出拆分後各 subscale 的題項數、Cronbach's alpha。

**參考檔案**：`01_METHOD_feature_decomposition_and_reliability_ZH.md`、`01_METHOD_subscale_definitions_record_ZH.md`

---

### 3.5 預測任務設計（Prediction Tasks）

**要寫什麼：**

清楚說明兩個預測任務：

| 任務 | 預測變項 | 結果變項 | 詮釋 |
|:--|:--|:--|:--|
| W2 → W2 | W2 features | W2 高心理困擾 | 橫斷面預測（Cross-sectional prediction） |
| W2 → W3 | W2 features | W3 高心理困擾 | 縱貫預測（Longitudinal prediction） |

強調：兩個任務都僅使用 W2 baseline predictors，W3 資料完全不進入模型（避免資料洩漏）。

---

### 3.6 模型設計（Models）

**要寫什麼：**

說明六個比較模型的設計邏輯：

| 模型 | 特徵組合 | 設計目的 |
|:--|:--|:--|
| Logistic（原始大題組，無刪除） | 原始題組，不刪 | 最基礎 benchmark |
| Logistic（原始大題組，有計畫刪題） | 原始題組，移除 planned drop groups | 測試刪題後的 baseline 變化 |
| Logistic（拆分後） | drop + decomposition | 拆題後可解釋的 Logistic |
| LASSO Logistic | drop + decomposition | 特徵選擇，獲取相對重要性 |
| Ridge Logistic | drop + decomposition | 穩定的正則化係數 |
| GraphSAGE | drop + decomposition + graph edges（同儕提名） | 測試同儕網絡圖結構是否提升預測 |

說明 GraphSAGE 的圖建構方式：以同儕提名資料建立鄰接矩陣（adjacency matrix），以 W2 問卷特徵作為節點特徵（node features）。

說明評估指標：使用 AUC-ROC 作為主要比較指標，並搭配交叉驗證（cross-validation）或 hold-out test set。

---

### 3.7 Interaction Analysis 方法

**要寫什麼：**

說明 Logistic Regression moderation model：

```
logit(P(High Psychological Distress = 1))
= b0 + b1 × Feature
  + b2 × ModeratorHigh
  + b3 × Feature × ModeratorHigh
  + covariates
```

- `Feature`：LASSO Top 20 中的重要特徵（連續，已標準化為 z-score）。
- `ModeratorHigh`：High Online Activity（0 = 低線上活動，1 = 高線上活動）。
- `b3`：交互作用項係數，若顯著則表示該特徵的保護效果在兩組間有差異。
- 協變量（covariates）：性別等人口學背景變項。

---

## 第四章：研究結果（Results）

> **建議結果章節的順序：**
> 1. 模型表現比較
> 2. Table 1 描述性差異
> 3. 同儕提名增量建模
> 4. LASSO Top 20 與類別重要性
> 5. Interaction Analysis

---

### 4.1 模型表現比較（Model Performance Comparison）

**要寫什麼：**

以文字報告六個模型在兩個任務的 AUC，並製作表格呈現。

主要結論：
> Across both cross-sectional and longitudinal tasks, GraphSAGE did not outperform the best non-GNN models. In the W2 → W2 task, the best non-GNN model achieved an AUC of 0.8229, while GraphSAGE achieved 0.8187. In the W2 → W3 task, the best non-GNN model achieved 0.7141, while GraphSAGE achieved 0.6974. This suggests that, under the current peer-nomination network construction, graph-based social-structure information did not provide clear incremental predictive advantage over individual-level questionnaire features.

**⚠️ 注意語氣**：不要寫「社交圈完全沒有影響」，要寫「在目前的同儕提名網絡建構下，圖結構資訊未提供明顯額外預測效益」。

---

#### 📊 建議放：Table 2 — 各模型 AUC 比較表

| 模型 | W2→W2 AUC | W2→W3 AUC |
|:--|--:|--:|
| Logistic（原始，無刪題） | 0.8229 | 0.7141 |
| Logistic（原始，有刪題） | … | … |
| Logistic（拆分後） | … | … |
| LASSO | … | … |
| Ridge | … | … |
| GraphSAGE | 0.8187 | 0.6974 |

**資料來源**：`02_MODEL_comparison_all_w2w2_w2w3.xlsx`

---

### 4.2 描述性群體差異（Descriptive Group Differences / Table 1）

**要寫什麼：**

描述高/低心理困擾兩組學生在各主要預測變項上的差異，並說明統計顯著性。

特別說明同儕提名特徵的模式：
> Descriptive group comparisons showed that several interpersonal nomination indicators differed between high- and low-distress students in the W2 cross-sectional task (8 out of 12 features, p < .05). However, fewer interpersonal indicators remained significant in the W2 → W3 longitudinal task (4 out of 12 features, p < .05). This pattern suggests that peer nomination features may more strongly capture concurrent social difficulties than future psychological distress risk.

---

#### 📊 建議放：Table 1 — 高/低心理困擾組描述性差異

呈現格式：
- 欄位：變項名稱 | Low Distress M (SD) 或 % | High Distress M (SD) 或 % | 統計量（t 或 χ²）| p 值 | Effect Size（Cohen's d 或 Cramér's V）
- 分成 W2→W2 與 W2→W3 兩個部分，或分兩個 table。
- 連續變項用均值、標準差；類別變項用次數、百分比。
- 可以按照類別（SEL、Online、Family、School、Interpersonal Network 等）分組呈現。

**資料來源**：`03_TABLE1_group_differences_all.xlsx`

---

### 4.3 同儕提名特徵的增量預測貢獻（Interpersonal Incremental Modeling）

**要寫什麼：**

這一段承接 Table 1（描述性差異），進一步問：當所有其他因素都進入模型後，同儕提名特徵還有沒有被 LASSO 保留？

> Although some interpersonal nomination indicators showed significant group differences in Table 1, LASSO retained only a limited subset of interpersonal features after accounting for individual-, family-, school-, and digital-life predictors. In the W2 → W2 task, 6 out of 12 interpersonal features were selected by LASSO, with 2 entering the Top 20. In the W2 → W3 task, only 4 were selected, with 2 in the Top 20. The summed relative importance of the Interpersonal Network category was 3.04% (W2 → W2) and 5.11% (W2 → W3), substantially lower than SEL / Resilience (40.29% and 33.02%, respectively).

---

#### 📊 建議放：Table 3（或補充表）— Interpersonal Features LASSO 選取結果

| 特徵名稱 | W2→W2 LASSO 選取 | W2→W2 Top 20 | W2→W3 LASSO 選取 | W2→W3 Top 20 |
|:--|:--:|:--:|:--:|:--:|
| Online Total Nominations, Observed Count | ✓ | ✓（排名 17） | ✓ | ✓（排名 14） |
| Outgoing Friendship Nominations | ✓ | ✓ | ✗ | ✗ |
| Reciprocal Friendship Ties | ✗ | ✗ | ✓ | ✓ |
| … | … | … | … | … |

**資料來源**：`04_INTERPERSONAL_feature_selection_summary.xlsx`

---

### 4.4 LASSO Top 20 特徵重要性與類別詮釋（Feature Importance & Category-Level Interpretation）

**要寫什麼：**

這是結果章節的核心，分兩個層次呈現：

**（a）特徵層次**：報告兩個任務中 LASSO Top 20 的相對重要性排名，特別點出跨任務穩定出現的特徵（如 Self-Worth、Self-Awareness、Family Cohesion 等）。

**（b）類別層次**：報告各大類別的相對重要性加總。

> Category-level analysis showed that SEL / Resilience accounted for the largest share of relative importance in both tasks (W2 → W2: 40.29%; W2 → W3: 33.02%). Online / Digital Life was the second largest category (19.05%; 22.32%), followed by School Context / Belonging (9.19%; 9.42%) and Family / Parenting (7.38%; 6.24%). In contrast, Interpersonal Network features accounted for a much smaller share (3.04%; 5.11%), supporting the interpretation that individual psychosocial capacities and contextual factors are more central predictors of psychological distress than peer nomination network indicators in the current models.

**說明 Relative Importance 的定義**（重要！）：
> Relative importance was calculated as the absolute value of the standardized LASSO coefficient for each feature, divided by the sum of all absolute standardized coefficients, multiplied by 100. This metric represents each feature's proportional contribution to the total absolute LASSO coefficient magnitude and should not be interpreted as percentage of variance explained.

---

#### 📊 建議放：Table 4 — Category-Level Relative Importance Summary

| 類別 | W2→W2 Top 20 特徵數 | W2→W2 Relative Importance % | W2→W3 Top 20 特徵數 | W2→W3 Relative Importance % |
|:--|--:|--:|--:|--:|
| SEL / Resilience | 5 | 40.29 | 5 | 33.02 |
| Online / Digital Life | 5 | 19.05 | 6 | 22.32 |
| School Context / Belonging | 2 | 9.19 | 2 | 9.42 |
| Family / Parenting | 2 | 7.38 | 2 | 6.24 |
| Demographic / Social Status | 1 | 6.02 | 1 | 6.11 |
| Interpersonal Network | 2 | 3.04 | 2 | 5.11 |
| Bullying / Victimization | 2 | 3.69 | 1 | 2.02 |
| Delinquency / Risk Behavior | 1 | 1.47 | 1 | 3.36 |

---

#### 🖼️ 建議放：Figure 1 — Category-Level Relative Importance 圖

**使用圖檔**：`figures/05_LASSO_fig_category_relative_importance_summary.png`

這是論文最重要的主圖，應放在主文中。圖說明（Figure Caption）可以寫：

> Figure 1. Category-level LASSO relative importance across W2 → W2 and W2 → W3 prediction tasks. Relative importance for each category was calculated as the sum of absolute standardized LASSO coefficients for features within that category, divided by the total sum across all features, expressed as a percentage. SEL / Resilience consistently showed the highest relative importance, while Interpersonal Network showed comparatively limited contribution.

---

#### 🖼️ 可選擇放：Figure 2a & 2b — W2→W2 與 W2→W3 各自的 Top 20 特徵圖

**使用圖檔**：
- `figures/05_LASSO_fig_top20_w2_to_w2.png`
- `figures/05_LASSO_fig_top20_w2_to_w3.png`

可以放在主文或補充附錄（Supplementary Materials）。

---

### 4.5 Interaction Analysis：線上活動作為調節變項

**要寫什麼：**

說明 Interaction 分析的目的（承接 RQ3），然後報告唯一顯著的 interaction 結果。

**主要結論**：

> A significant interaction between Family Cohesion and Support and High Online Activity was found in the W2 → W3 prediction task (b3 = −0.1117, p = .036). Family Cohesion and Support was negatively associated with future high psychological distress in both groups. In the low-online-activity group, each 1-SD increase in family cohesion was associated with a decrease in log-odds of future high distress (b1 = −0.2947, OR = 0.745). In the high-online-activity group, this protective association was stronger (b1 + b3 = −0.4063, OR = 0.666). The significant interaction indicates that the protective role of family cohesion may be amplified among students with higher online activity.

**⚠️ 注意語氣**：
- 不要寫「高線上活動本身是保護因子」。
- 要寫「家庭支持的保護效果在高線上活動學生中更強」。
- 用 "associated with" 而非 "causes"。

---

#### 📊 建議放：Table 5 — Interaction Analysis 結果

| 任務 | 特徵 | b1（主效果） | b2（調節主效果） | b3（交互作用） | p 值 | Low Online Activity OR | High Online Activity OR |
|:--|:--|--:|--:|--:|--:|--:|--:|
| W2 → W3 | Family Cohesion and Support | −0.2947 | 0.2250 | −0.1117 | .036 | 0.745 | 0.666 |

**資料來源**：`07_INTERACTION_online_activity_models.xlsx`

---

#### 🖼️ 可選擇放：Figure 3 — 交互作用圖（Interaction Plot）

可以畫一張 moderation plot：X 軸為 Family Cohesion and Support（低/高），Y 軸為 Predicted Probability of High Psychological Distress，兩條線分別代表 Low Online Activity 與 High Online Activity。這種圖很直觀，教授通常喜歡看。

**注意**：目前 `figures/` 資料夾中沒有這張圖，需要另外用 Python 或 R 繪製。可以基於 `07_INTERACTION_online_activity_models.xlsx` 中的係數計算 predicted probabilities 後繪圖。

---

## 第五章：討論（Discussion）

### 5.1 GNN 未明顯優於線性模型的可能解釋

**要寫什麼（2-3 段）：**

1. **技術層面**：在目前同儕提名方式建構的網絡中，圖結構可能過於稀疏或噪音較多，GraphSAGE 難以從中學習到額外的有效訊號。
2. **心理學層面**：個人層面的心理社會特徵（SEL、家庭、學校）已能解釋大部分心理困擾的變異，同儕網絡的增量貢獻因此較為有限。
3. **方法論提醒**：GNN 的優勢通常在於當圖結構資訊能提供節點特徵之外的額外訊號時。本研究結果提示，未來需要思考更精細的網絡建構方式（如加入師生關係、班級情境等）。

---

### 5.2 SEL / Resilience 是最主要預測領域的詮釋

**要寫什麼：**

- 連結到文獻回顧中的 SEL 理論（如 CASEL 框架）。
- Self-Worth（自我價值感）在兩個任務中都是排名第一的特徵，呼應自尊理論在心理健康的重要性。
- Self-Awareness 呈正向關聯（注意：高自我覺察但方向為正，可能反映 self-awareness 量表中包含負面情緒覺察的題項，需要查看題項後解釋）。
- Help-Seeking 和 Self-Management 是保護因子，代表有助於主動因應壓力的能力。

---

### 5.3 Online / Digital Life 的角色

**要寫什麼：**

- Online / Digital Life 是第二大重要類別，且在縱貫預測（W2 → W3）中比橫斷面（W2 → W2）更重要，代表線上生活對未來心理困擾的預測效果更顯著。
- 問題性網路使用（Problematic Internet Use）呈正向關聯（風險因子）。
- 線上尋求觀點（Online Perspective Seeking）也呈正向關聯——這個發現值得討論：可能反映困擾中的個體更傾向於線上尋求資訊，也可能是社會比較的一種形式。

---

### 5.4 家庭支持在高線上活動學生中的調節效果

**要寫什麼：**

- Family Cohesion × High Online Activity 的顯著交互作用，代表在數位時代中，家庭連結可能是高線上活動青少年的重要緩衝機制。
- 可以從依附理論（Attachment Theory）或家庭保護因子角度詮釋。
- 實務意涵：對於高線上活動的學生，加強家庭支持介入可能比單純限制線上活動更有效。

---

### 5.5 研究限制

**要寫什麼（4-5 點）：**

1. **同儕提名網絡建構方式**：目前使用的是問卷式同儕提名，可能無法完整捕捉真實社交網絡結構（如線上互動、班級外人際關係）。
2. **樣本限制**：樣本來自特定地區，可能限制結果的外部效度（generalizability）。
3. **橫斷面因果推論限制**：W2 → W2 任務為橫斷面設計，無法推論因果方向。
4. **心理困擾二元化**：將連續的心理困擾分數 dichotomize 為高/低可能有訊息損失。
5. **線上活動定義**：線上活動以量表測量，可能無法完整捕捉實際的線上行為模式。

---

## 第六章：結論（Conclusion）

**要寫什麼（1-2 段）：**

> 本研究以縱貫資料比較了傳統線性模型與圖神經網絡模型在預測青少年高心理困擾風險上的表現。結果顯示，GraphSAGE 並未明顯優於線性模型，表明在目前同儕提名網絡定義下，圖結構資訊的額外預測效益有限。特徵重要性分析指出，SEL / Resilience、Online / Digital Life、School Context / Belonging 與 Family / Parenting 是最主要的預測類別，而同儕提名網絡特徵的增量貢獻相對有限。此外，Interaction Analysis 顯示，家庭凝聚與支持對未來高心理困擾的保護效果在高線上活動學生中更強，為數位時代青少年心理健康的保護因子研究提供了新的實證依據。

> 這些發現提示，在支持青少年心理健康的實務工作中，除了關注線上活動本身的使用量，更應重視個人心理社會能力的培養（SEL / Resilience）、家庭支持的加強，以及學校歸屬感的建立。對高線上活動的學生而言，良好的家庭支持可能是特別重要的保護機制。

---

## 附錄建議（Supplementary Materials）

以下內容建議放在附錄或 Supplementary Materials，不需要放在主文中，但教授或審查者問到時可以提供：

| 附錄 | 內容 | 來源檔案 |
|:--|:--|:--|
| Appendix A：Feature Inventory | 所有 active predictor 完整列表、量表名稱、題項數 | `01_METHOD_feature_inventory_ZH.md` |
| Appendix B：Subscale Definitions & Cronbach's alpha | 各 subscale 的題項、Cronbach's alpha 值 | `01_METHOD_subscale_definitions_record_ZH.md`、`01_METHOD_feature_decomposition_and_reliability_ZH.md` |
| Appendix C：Gender Dummy Coding 說明 | Gender coding 的處理方式 | `00_GUIDE_gender_dummy_coding_update_ZH.md` |
| Appendix D：Full Interaction Analysis Table | 所有 feature × Online Activity 的 b0/b1/b2/b3 結果（包含不顯著的） | `07_INTERACTION_online_activity_models.xlsx` |
| Appendix Figure S1 | W2→W2 LASSO Top 20 特徵重要性圖 | `figures/05_LASSO_fig_top20_w2_to_w2.png` |
| Appendix Figure S2 | W2→W3 LASSO Top 20 特徵重要性圖 | `figures/05_LASSO_fig_top20_w2_to_w3.png` |
| Appendix Figure S3 | 跨任務穩定特徵（Shared Top 20）圖 | `figures/05_LASSO_fig_shared_top20_relative_importance.png` |

---

## 論文主文表格與圖片一覽（Quick Reference）

| 編號 | 類型 | 標題 | 放在哪裡 | 來源 |
|:--|:--|:--|:--|:--|
| Table 1 | 表格 | 高/低心理困擾組描述性差異 | 主文 Results 4.2 | `03_TABLE1_group_differences_all.xlsx` |
| Table 2 | 表格 | 各模型 AUC 比較 | 主文 Results 4.1 | `02_MODEL_comparison_all_w2w2_w2w3.xlsx` |
| Table 3 | 表格 | Interpersonal Features LASSO 選取結果 | 主文 Results 4.3 | `04_INTERPERSONAL_feature_selection_summary.xlsx` |
| Table 4 | 表格 | Category-Level Relative Importance Summary | 主文 Results 4.4 | `06_CATEGORY_level_interpretation_summary_ZH.md` |
| Table 5 | 表格 | Interaction Analysis 結果 | 主文 Results 4.5 | `07_INTERACTION_online_activity_models.xlsx` |
| Figure 1 | 圖 | Category-Level LASSO Relative Importance（雙任務比較） | 主文 Results 4.4 | `figures/05_LASSO_fig_category_relative_importance_summary.png` |
| Figure 2 | 圖 | Interaction Plot（Family Cohesion × Online Activity） | 主文 Results 4.5 | 需另外繪製 |
| Figure S1 | 補充圖 | W2→W2 LASSO Top 20 | 附錄 | `figures/05_LASSO_fig_top20_w2_to_w2.png` |
| Figure S2 | 補充圖 | W2→W3 LASSO Top 20 | 附錄 | `figures/05_LASSO_fig_top20_w2_to_w3.png` |
| Figure S3 | 補充圖 | Shared Top 20 穩定特徵 | 附錄 | `figures/05_LASSO_fig_shared_top20_relative_importance.png` |

---

## 注意事項與語氣提醒

1. **不要說「GNN 沒有用」** → 要說「在目前同儕提名網絡建構方式下，GraphSAGE 未提供明顯額外預測效益」
2. **不要說「同儕網絡沒有影響」** → 要說「同儕提名特徵在本研究模型中的增量預測貢獻有限」
3. **不要說「家庭支持一定能保護高線上活動學生」** → 要說「家庭支持與較低未來心理困擾風險相關，且此關聯在高線上活動學生中更強」
4. **Relative Importance 不是 variance explained** → 要說「proportional share of total absolute standardized LASSO coefficient magnitude」
5. **W2→W2 是 cross-sectional，不能推論因果** → 只能說 association/prediction，不能說 cause

---

*本文件由 Claude (Cowork) 依據 TIGPS 研究資料整理，2026-05-21。*
