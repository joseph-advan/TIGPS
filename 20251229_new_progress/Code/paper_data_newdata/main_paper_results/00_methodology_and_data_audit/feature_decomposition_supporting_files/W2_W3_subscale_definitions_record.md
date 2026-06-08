# W2 and W3 Subscale Definitions Record

Last updated: 2026-05-20

This document is the current human-readable record for the Feature_Decomposition subscale definitions. It records how broad questionnaire groups were split into smaller theoretically interpretable subscales, their Chinese and English names, and the item columns included in each subscale.

## Current Analysis Scope

- Current main-paper predictors: W2 features only.
- Current prediction tasks: W2 predictors -> W2 high psychological distress; W2 predictors -> W3 high psychological distress.
- W2 definitions are used in modeling, Table 1 group differences, LASSO Top20, category-level interpretation, and interaction analysis.
- W3 definitions are retained only as questionnaire mapping/reference. W3 subscales are not used as predictors in the current two-task main analysis.
- Subscale score rule in the current Feature_Decomposition model script: row-wise mean of available included items; rows with all included items missing are set to missing.

## Important Current Decisions

- W2 self-rated health is `v52` and is handled as `v52_health`.
- W2 self-worth items `v52_1` to `v52_3` are a separate retained feature group and are not dropped with `v52_health`.
- W2 `v54_18` is assigned to Responsible Decision-Making, not Self-Awareness.
- W3 `53-18` is mapped in the same conceptual way for reference only.
- Cronbach's alpha reliability is currently calculated for W2 subscales only, because W3 predictors are not used in the current main analysis.

## W2 Subscale Definitions Used In Current Analysis

| Original group | Formal group name | Counterpart | Subscale code | Chinese subscale name | English subscale name | Included items | Scope |
|---|---|---|---|---|---|---|---|
| `v25` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `26` | `v25_A` | 網路理想自我呈現 | Online Ideal Self-Presentation | `v25_1, v25_2, v25_3` | Used as W2 predictor |
| `v25` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `26` | `v25_B` | 現實自我認同滿意度 | Real-life Self-Satisfaction | `v25_4, v25_5, v25_6` | Used as W2 predictor |
| `v25` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `26` | `v25_C` | 虛實形象差異與網路沈浸 | Online-Offline Discrepancy & Immersion | `v25_7, v25_8, v25_9, v25_10, v25_11, v25_12, v25_13, v25_14, v25_15` | Used as W2 predictor |
| `v23` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `25` | `v23_A` | 選擇性正向分享 | Selective Positive Sharing | `v23_1, v23_2, v23_3` | Used as W2 predictor |
| `v23` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `25` | `v23_B` | 真實／非理想化自我呈現 | Authentic and Less-Ideal Self-Presentation | `v23_4, v23_5, v23_6` | Used as W2 predictor |
| `v23` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `25` | `v23_C` | 隱性社群瀏覽與被動參與 | Covert Social Media Monitoring and Passive Participation | `v23_7, v23_8, v23_9` | Used as W2 predictor |
| `v26` | 線上社會比較與觀點搜尋 / Online Social Comparison and Perspective Seeking | `27` | `v26_A` | 線上向上社會比較 | Online Upward Social Comparison | `v26_1, v26_2, v26_3` | Used as W2 predictor |
| `v26` | 線上社會比較與觀點搜尋 / Online Social Comparison and Perspective Seeking | `27` | `v26_B` | 線上觀點搜尋與獲取 | Online Perspective Seeking | `v26_4, v26_5, v26_6` | Used as W2 predictor |
| `v27` | 網路同儕互動焦慮（錯失恐懼，FOMO） / Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) | `28` | `v27_A` | 錯失恐懼與社交焦慮 | Fear of Missing Out & Social Anxiety | `v27_1, v27_2, v27_3` | Used as W2 predictor |
| `v27` | 網路同儕互動焦慮（錯失恐懼，FOMO） / Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) | `28` | `v27_B` | 線上活動錯失困擾 | Distress from Missing Online Events | `v27_4` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_A` | 自我覺察 | Self-Awareness | `v54_1, v54_2, v54_3` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_B` | 自我管理 | Self-Management | `v54_4, v54_5, v54_6` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_C` | 動機與目標導向 | Motivation & Goal Setting | `v54_7, v54_8, v54_9` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_D` | 人際技巧與社交意識 | Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_E` | 求助行為與社會支持 | Help-Seeking | `v54_12, v54_16` | Used as W2 predictor |
| `v54` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `53` | `v54_F` | 負責任的決策與社會影響 | Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` | Used as W2 predictor |

## W3 Reference Mapping

| Original group | Formal group name | Counterpart | Subscale code | Chinese subscale name | English subscale name | Included items | Scope |
|---|---|---|---|---|---|---|---|
| `26` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `v25` | `26_A` | 網路理想自我呈現 | Online Ideal Self-Presentation | `26-1, 26-2, 26-3` | Reference mapping only |
| `26` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `v25` | `26_B` | 現實自我認同滿意度 | Real-life Self-Satisfaction | `26-4, 26-5, 26-6` | Reference mapping only |
| `26` | 社群媒體自我呈現與網路形象管理 / Social Media Self-Presentation and Online Image Management | `v25` | `26_C` | 虛實形象差異與網路沈浸 | Online-Offline Discrepancy & Immersion | `26-7, 26-8, 26-9, 26-10, 26-11, 26-12, 26-13, 26-14, 26-15` | Reference mapping only |
| `25` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `v23` | `25_A` | 選擇性正向分享 | Selective Positive Sharing | `25-1, 25-2, 25-3` | Reference mapping only |
| `25` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `v23` | `25_B` | 真實／非理想化自我呈現 | Authentic and Less-Ideal Self-Presentation | `25-4, 25-5, 25-6` | Reference mapping only |
| `25` | 社群媒體使用行為：選擇性分享與印象管理 / Social Media Use: Selective Sharing and Impression Management | `v23` | `25_C` | 隱性社群瀏覽與被動參與 | Covert Social Media Monitoring and Passive Participation | `25-7, 25-8, 25-9` | Reference mapping only |
| `27` | 線上社會比較與觀點搜尋 / Online Social Comparison and Perspective Seeking | `v26` | `27_A` | 線上向上社會比較 | Online Upward Social Comparison | `27-1, 27-2, 27-3` | Reference mapping only |
| `27` | 線上社會比較與觀點搜尋 / Online Social Comparison and Perspective Seeking | `v26` | `27_B` | 線上觀點搜尋與獲取 | Online Perspective Seeking | `27-4, 27-5, 27-6` | Reference mapping only |
| `28` | 網路同儕互動焦慮（錯失恐懼，FOMO） / Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) | `v27` | `28_A` | 錯失恐懼與社交焦慮 | Fear of Missing Out & Social Anxiety | `28-1, 28-2, 28-3` | Reference mapping only |
| `28` | 網路同儕互動焦慮（錯失恐懼，FOMO） / Online Peer Interaction Anxiety (Fear of Missing Out, FOMO) | `v27` | `28_B` | 線上活動錯失困擾 | Distress from Missing Online Events | `28-4` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_A` | 自我覺察 | Self-Awareness | `53-1, 53-2, 53-3` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_B` | 自我管理 | Self-Management | `53-4, 53-5, 53-6` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_C` | 動機與目標導向 | Motivation & Goal Setting | `53-7, 53-8, 53-9` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_D` | 人際技巧與社交意識 | Social Awareness & Relationship Skills | `53-10, 53-11, 53-13, 53-14, 53-15` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_E` | 求助行為與社會支持 | Help-Seeking | `53-12, 53-16` | Reference mapping only |
| `53` | 社會情緒學習（SEL）能力 / Social and Emotional Learning (SEL) Competencies | `v54` | `53_F` | 負責任的決策與社會影響 | Responsible Decision-Making | `53-17, 53-18, 53-19, 53-20` | Reference mapping only |

## SEL v54 Rationale

The SEL group was split into six subscales:

| Subscale | Meaning | Current W2 items |
|---|---|---|
| Self-Awareness | Awareness of one's body signals, emotions, and internal states. | `v54_1, v54_2, v54_3` |
| Self-Management | Emotion regulation and coping strategies under stress or low mood. | `v54_4, v54_5, v54_6` |
| Motivation & Goal Setting | Goal-setting intention, efficacy, execution, and strategic planning. | `v54_7, v54_8, v54_9` |
| Social Awareness & Relationship Skills | Understanding others, empathy-related recognition, openness, and prosocial behavior. | `v54_10, v54_11, v54_13, v54_14, v54_15` |
| Help-Seeking | Seeking support from adults/teachers or peers. | `v54_12, v54_16` |
| Responsible Decision-Making | Outcome prediction, impulse control, diverse problem-solving, moral judgment, and norm maintenance. | `v54_17, v54_18, v54_19, v54_20` |

`v54_18` was moved from Self-Awareness to Responsible Decision-Making because the item is conceptually closer to moral judgment / knowing right from wrong than to emotion or body awareness. The updated reliability check supports this revision: Self-Awareness remains reliable and Responsible Decision-Making improves.

## Reliability Check

The current W2-only Cronbach's alpha check is stored in:

- `outputs/reliability/subscale_cronbach_alpha_reliability.xlsx`
- `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md`
- `outputs/reliability/subscale_cronbach_alpha_reliability_details.json`

Current SEL reliability after the v54 revision:

| W2 subscale | Items | Cronbach's alpha | Interpretation |
|---|---|---:|---|
| Self-Awareness | `v54_1, v54_2, v54_3` | 0.857 | Good |
| Self-Management | `v54_4, v54_5, v54_6` | 0.896 | Good |
| Motivation & Goal Setting | `v54_7, v54_8, v54_9` | 0.904 | Good |
| Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` | 0.834 | Good |
| Help-Seeking | `v54_12, v54_16` | 0.661 | Questionable but usable |
| Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` | 0.827 | Good |

## Related Files

| File | Role |
|---|---|
| `subscale_definitions_w2_w3.json` | Machine-readable source configuration for subscale definitions. |
| `subscale_definitions_w2_w3_table.csv` | Flat CSV version of the same definitions. |
| `build_binary_drop_then_split_baseline.py` | Compares drop-only features against drop + decomposition features. |
| `outputs/model_performance/binary_drop_then_split_summary.md` | Prediction-performance summary for the decomposition strategy. |
| `run_subscale_cronbach_alpha_reliability.py` | Computes Cronbach's alpha for W2 configured subscales. |
| `run_v54_sel_deep_dive.py` | V54-specific reliability deep dive. |
| `docs/v54_revision_rerun_change_summary.md` | Summary of the v54 revision and downstream rerun findings. |
