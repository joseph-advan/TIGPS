# Feature Decomposition Methods

Last updated: 2026-05-20

## Purpose

這份文件整理目前論文分析中使用的 feature decomposition 方法。目標是讓後續撰寫論文 Methods 時，只需要參考 `main_paper_results/00_methodology_and_data_audit` 裡的文件，不必回頭翻 `Code/paper_data_newdata/Feature_Decomposition` 的所有中間檔。

Feature decomposition 在本研究中的角色是「feature construction」，不是原始資料清理。資料清理流程已在 `01_data_cleaning_methods_detailed_ZH.md` 中記錄；本文件接續說明清理後資料如何被整理成模型使用的特徵。

## Analysis Scope

目前主論文分析只使用 W2 特徵作為 predictors，並進行兩個任務：

| Task | Predictor wave | Outcome wave | Outcome definition |
|---|---|---|---|
| W2 -> W2 | W2 predictors | W2 psychological distress | W2 psychological distress sum score median split |
| W2 -> W3 | W2 predictors | W3 psychological distress | W3 psychological distress sum score median split |

重要設定：

- W2 final data: `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv`
- W3 final data: `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv`
- Modeling sample: aligned W2/W3 students, `N = 6603`
- W2 psychological distress target group: `v55`
- W3 psychological distress target group: `54`
- W3 questionnaire subscales are retained only as reference mapping, not used as predictors in the current main-paper models.

## Why Decompose Questionnaire Groups

原本的資料包含一些大題組，例如 SEL、社群媒體自我呈現、FOMO 等。若直接把整個大題組平均成一個分數，會有兩個問題：

1. 同一個大題組可能混合不同心理構念。
2. 模型結果較難解釋，因為無法知道是哪一個子面向在影響心理困擾。

因此本研究將部分理論上可拆分的大題組拆成較小的小題組，讓每個 feature 更接近單一心理或行為構念。

例如，SEL 原本是一整組 `v54_1` 到 `v54_20`，現在拆成：

- Self-Awareness
- Self-Management
- Motivation & Goal Setting
- Social Awareness & Relationship Skills
- Help-Seeking
- Responsible Decision-Making

這樣後續 LASSO Top20、category-level interpretation、interaction analysis 都能更清楚描述「哪一種能力或經驗」與心理困擾風險較有關。

## Feature Construction Rules

### 1. Drop Version As Baseline

Feature decomposition 是從目前的 drop-version feature set 延伸而來。

W2 drop groups:

| Dropped feature group | Reason |
|---|---|
| `v57` | Outcome-adjacent / not retained in predictor set |
| `v50` | Dropped in current baseline feature plan |
| `v51` | Dropped in current baseline feature plan |
| `v52_health` | W2 scalar self-rated health item `v52`; dropped in the current drop-version feature set |

Note: `v52_health` 指的是 W2 的單題自評健康 `v52`。它不同於 `v52_1` 到 `v52_3` 的 self-worth items；`v52_1` 到 `v52_3` 沒有被當成 `v52_health` 一起 drop。

### 2. Groups Selected For Decomposition

目前 W2 被拆分的大題組如下：

| W2 group | Formal group name | Decomposition role |
|---|---|---|
| `v25` | Social Media Self-Presentation and Online Image Management | Split into 3 online self-presentation subscales |
| `v23` | Social Media Use: Selective Sharing and Impression Management | Split into 3 impression-management subscales |
| `v26` | Online Social Comparison and Perspective Seeking | Split into 2 online comparison / perspective-seeking subscales |
| `v27` | Online Peer Interaction Anxiety (FOMO) | Split into 2 FOMO / response-pressure subscales |
| `v54` | Social and Emotional Learning (SEL) Competencies | Split into 6 SEL subscales |

### 3. Subscale Scoring

目前 decomposition script 的小題組分數計算方式：

- 每個小題組使用 included items 的 row-wise mean。
- 若該小題組所有題項都缺失，該小題組分數設為 missing。
- Reliability workbook 另外回報 `N meeting >=50% valid items`，作為資料完整度診斷。
- Multiple-response risk behavior group `v42` 不用平均，而是用 count score；`v42_14` 是「以上皆非」，不納入風險行為計分。

## W2 Subscale Definitions Used In Current Analysis

| Parent group | Subscale code | Chinese name | English name | Included W2 items |
|---|---|---|---|---|
| `v25` | `v25_A` | 網路理想自我呈現 | Online Ideal Self-Presentation | `v25_1, v25_2, v25_3` |
| `v25` | `v25_B` | 現實自我認同滿意度 | Real-life Self-Satisfaction | `v25_4, v25_5, v25_6` |
| `v25` | `v25_C` | 虛實形象差異與網路沈浸 | Online-Offline Discrepancy & Immersion | `v25_7, v25_8, v25_9, v25_10, v25_11, v25_12, v25_13, v25_14, v25_15` |
| `v23` | `v23_A` | 選擇性正向分享 | Selective Positive Sharing | `v23_1, v23_2, v23_3` |
| `v23` | `v23_B` | 真實／非理想化自我呈現 | Authentic and Less-Ideal Self-Presentation | `v23_4, v23_5, v23_6` |
| `v23` | `v23_C` | 隱性社群瀏覽與被動參與 | Covert Social Media Monitoring and Passive Participation | `v23_7, v23_8, v23_9` |
| `v26` | `v26_A` | 線上向上社會比較 | Online Upward Social Comparison | `v26_1, v26_2, v26_3` |
| `v26` | `v26_B` | 線上觀點搜尋與獲取 | Online Perspective Seeking | `v26_4, v26_5, v26_6` |
| `v27` | `v27_A` | 錯失恐懼與社交焦慮 | Fear of Missing Out & Social Anxiety | `v27_1, v27_2, v27_3` |
| `v27` | `v27_B` | 線上活動錯失困擾 | Distress from Missing Online Events | `v27_4` |
| `v54` | `v54_A` | 自我覺察 | Self-Awareness | `v54_1, v54_2, v54_3` |
| `v54` | `v54_B` | 自我管理 | Self-Management | `v54_4, v54_5, v54_6` |
| `v54` | `v54_C` | 動機與目標導向 | Motivation & Goal Setting | `v54_7, v54_8, v54_9` |
| `v54` | `v54_D` | 人際技巧與社交意識 | Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` |
| `v54` | `v54_E` | 求助行為與社會支持 | Help-Seeking | `v54_12, v54_16` |
| `v54` | `v54_F` | 負責任的決策與社會影響 | Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` |

## SEL v54 Revision

原本 `v54_18` 曾被放在 Self-Awareness，但後續檢查後改放到 Responsible Decision-Making。

修正後：

| Subscale | Current items |
|---|---|
| Self-Awareness | `v54_1, v54_2, v54_3` |
| Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` |

理由：

- `v54_18` 的內容較接近「知道是非 / moral judgment」。
- 它比起身體狀態、情緒辨識或內在感受，更接近 Responsible Decision-Making。
- 調整後 Self-Awareness 仍維持良好 reliability。
- 調整後 Responsible Decision-Making 的 reliability 也達到良好水準。

## Reliability Check

Cronbach's alpha 用來檢查拆出來的小題組內部一致性。這不是唯一決定標準，但可以作為拆題組是否合理的支持證據。

目前只計算 W2 小題組的 Cronbach's alpha，因為目前主分析只使用 W2 predictors。

整體結果：

| Reliability category | Count |
|---|---:|
| Total configured W2 subscales checked | 16 |
| Single-item subscales where alpha is not applicable | 1 |
| Good alpha >= 0.80 | 13 |
| Acceptable alpha 0.70-0.79 | 1 |
| Questionable alpha 0.60-0.69 | 1 |
| Low alpha < 0.60 | 0 |

Review flags:

| Subscale | Issue | Interpretation |
|---|---|---|
| `v27_B` Distress from Missing Online Events | Single-item subscale | Cronbach's alpha not applicable |
| `v54_E` Help-Seeking | Alpha = 0.661 | Questionable but usable; should be noted as a two-item lower-reliability subscale |

SEL v54 reliability after revision:

| W2 SEL subscale | Items | Cronbach's alpha | Interpretation |
|---|---|---:|---|
| Self-Awareness | `v54_1, v54_2, v54_3` | 0.857 | Good |
| Self-Management | `v54_4, v54_5, v54_6` | 0.896 | Good |
| Motivation & Goal Setting | `v54_7, v54_8, v54_9` | 0.904 | Good |
| Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` | 0.834 | Good |
| Help-Seeking | `v54_12, v54_16` | 0.661 | Questionable but usable |
| Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` | 0.827 | Good |

## Prediction Check: Drop-Only vs Drop + Decomposition

為了確認拆題組不只是理論上合理，也檢查它是否改善預測表現。比較方式是：

- Baseline: current drop-version feature set, without decomposition.
- Split version: same drop-version feature set, but selected broad groups are replaced by smaller subscales.
- Model: logistic regression.
- Metrics: CV5 mean test-fold metrics from 5 stratified cross-validation folds.

Performance summary:

| Task | Drop-only CV5 Accuracy | Drop + Decomposition CV5 Accuracy | Drop-only CV5 AUC | Drop + Decomposition CV5 AUC | AUC difference |
|---|---:|---:|---:|---:|---:|
| W2 -> W2 | 0.715733 | 0.736481 | 0.790897 | 0.810315 | +0.019418 |
| W2 -> W3 | 0.641833 | 0.649556 | 0.698156 | 0.707296 | +0.009140 |

Interpretation:

- Decomposition improves both W2 -> W2 and W2 -> W3 AUC.
- The W2 -> W2 improvement is larger.
- The W2 -> W3 improvement is smaller but still positive.
- Therefore, feature decomposition is justified both theoretically and empirically, but the improvement should be described as modest rather than large.

## How This Connects To Later Main-Paper Results

Feature decomposition is used as the feature foundation for the later main-paper analysis:

| Later section | How decomposition is used |
|---|---|
| `01_model_performance` | Compares original-group models, decomposed models, Ridge/LASSO, and GraphSAGE. |
| `02_descriptive_table1_group_differences` | Uses decomposed feature names and subscale scores in group difference tables. |
| `03_interpersonal_incremental_modeling` | Tests whether interpersonal/network features add predictive value beyond decomposed individual features. |
| `04_feature_importance_top20` | Uses LASSO relative importance after decomposition to identify top predictors. |
| `05_category_level_interpretation` | Groups decomposed predictors into broader conceptual domains such as SEL, Online/Digital Life, Family/Parenting, Bullying, and Interpersonal Network. |
| `06_interaction_analysis` | Tests whether selected top features interact with high online activity or problematic internet use. |

## Supporting Files Copied Into This Folder

必要附件已複製到：

`main_paper_results/00_methodology_and_data_audit/feature_decomposition_supporting_files/`

| File | Purpose |
|---|---|
| `W2_W3_subscale_definitions_record.md` | Full paper-facing snapshot of W2/W3 subscale definitions and v54 rationale. |
| `subscale_definitions_w2_w3_table.csv` | Full W2/W3 subscale definition table, including W3 reference mapping. |
| `binary_drop_then_split_summary.md` | Human-readable drop-only vs drop + decomposition performance summary. |
| `binary_drop_then_split_summary.csv` | Performance comparison of drop-only vs drop + decomposition. |
| `subscale_cronbach_alpha_reliability_summary.md` | Human-readable W2 subscale reliability summary. |
| `subscale_cronbach_alpha_reliability.xlsx` | Full reliability workbook for W2 subscales. |
| `v54_sel_deep_dive_reliability_summary.md` | Human-readable v54 SEL reliability deep-dive summary. |
| `v54_sel_deep_dive_reliability.xlsx` | V54-specific reliability deep dive workbook. |

The full working scripts and intermediate machine-readable details remain in:

`Code/paper_data_newdata/Feature_Decomposition`

This 00-methodology folder keeps only the paper-facing summary and necessary supporting evidence.

## Suggested Methods Wording

可在論文 Methods 中使用或改寫下列文字：

> To improve interpretability of broad questionnaire domains, selected W2 questionnaire groups were decomposed into theoretically defined subscales. Subscale scores were computed as the row-wise mean of available items within each subscale, with all-missing subscales treated as missing. The current main analysis used W2 predictors only and evaluated two tasks: W2 predictors to W2 high psychological distress and W2 predictors to W3 high psychological distress. Internal consistency of W2 subscales was evaluated using Cronbach's alpha, and the decomposition strategy was further checked by comparing predictive performance between the drop-only feature set and the drop-plus-decomposition feature set.

中文版本：

> 為提升模型特徵的可解釋性，本研究將部分 W2 大題組依理論構念拆分為較小的小題組。每個小題組分數以該小題組題項的列平均計算，若該小題組所有題項皆缺失則設為缺失。主要分析僅使用 W2 特徵作為 predictors，並分別預測 W2 與 W3 的高心理困擾狀態。小題組內部一致性以 Cronbach's alpha 檢查，並進一步比較 drop-only feature set 與 drop + decomposition feature set 的預測表現，以確認拆題組策略在理論與模型表現上皆具有合理性。
