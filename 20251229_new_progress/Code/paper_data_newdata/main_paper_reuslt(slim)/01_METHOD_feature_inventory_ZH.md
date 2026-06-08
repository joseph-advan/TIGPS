# Main Paper Feature Inventory

## Purpose

本文件整理目前 main-paper analyses 使用的特徵、題號、正式中英文名稱、用途，以及後續 LASSO Top 20 圖表使用的概念分類規則。

## Current Scope

- 主要預測任務：`W2 -> W2` 與 `W2 -> W3`。
- Predictor side：使用 W2 baseline features。
- 人際網絡特徵：目前只使用 observed, non-class-adjusted 版本。
- Moderator：目前 interaction analysis 只使用 Online Activity Frequency；`v28` 不再列為 moderator。

## Summary Counts

- Total rows in inventory: 48
- Outcome / moderator variables: 3
- Active W2 model predictors: 33
- Observed interpersonal features: 12

## Category Rules Used In Feature Importance Figures

04 的 LASSO Top 20 category-level figures 使用下列規則分類。若一個 feature 符合多個規則，會依程式中的規則順序先配到第一個符合的 category。

| Category                    | Rule                                                                                | Chinese Explanation                                                              |
|:----------------------------|:------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| SEL / Resilience            | Feature Code starts with v54, or Feature Code is v52.                               | 社會情緒學習、復原力、自我概念相關特徵。                                         |
| Family / Parenting          | Feature Code is v5, v6, or v19.                                                     | 家庭凝聚、親職互動、父母參與與學業監督。                                         |
| Online / Digital Life       | Feature Code starts with v22, v23, v25, v26, or v27, or Feature Code is v28 or v49. | 線上活動、網路使用、網路自我呈現、FOMO、社群比較、問題性網路使用與數位學習經驗。 |
| Bullying / Victimization    | Feature Code is v34, v36, v38, or v40.                                              | 線上或線下霸凌受害與加害經驗。                                                   |
| Interpersonal Network       | Feature Code starts with ip_.                                                       | 由同儕提名資料建構的人際網絡指標。                                               |
| Demographic / Social Status | Feature Code is v1_male, v1, 1, 1_male, or v3.                                      | 性別 dummy 與主觀社會地位。                                                      |
| School Context / Belonging  | Feature Code is v9, v12, or v8_03-v8_06.                                            | 學校歸屬、同儕支持，以及學校社會逆境與同儕壓力事件。                             |
| Delinquency / Risk Behavior | Feature Code is v42.                                                                | 偏差行為與健康風險行為。                                                         |
| Other                       | Features that do not match the above rules.                                         | 未落入上述規則的其他特徵。                                                       |

## Outcome And Moderator Variables

| Feature Code   | Chinese Name                         | English Name                                                            | Items / Construction                                                                     | Scoring / Coding                                                            | Used as Moderator              |
|:---------------|:-------------------------------------|:------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------|:----------------------------------------------------------------------------|:-------------------------------|
| 54             | 心理困擾症狀（憂鬱／焦慮／自傷意念） | Psychological Distress Symptoms (Depression/Anxiety/Self-harm Ideation) | 54-1;54-2;54-3;54-4;54-5;54-6;54-7;54-8;54-9;54-10;54-11;54-12;54-13;54-14               | Median split / binary high psychological distress outcome for W3.           | No                             |
| v55            | 心理困擾症狀（憂鬱／焦慮／自傷意念） | Psychological Distress Symptoms (Depression/Anxiety/Self-harm Ideation) | v55_1;v55_2;v55_3;v55_4;v55_5;v55_6;v55_7;v55_8;v55_9;v55_10;v55_11;v55_12;v55_13;v55_14 | Median split / binary high psychological distress outcome for W2.           | No                             |
| v21_3-v21_6    | 線上活動頻率                         | Online Activity Frequency                                               | v21_3;v21_4;v21_5;v21_6                                                                  | Summed W2 frequency score, split at the W2 median for interaction analysis. | Yes, Online Activity Frequency |

## Newly Included School-Context Predictors

以下三個題組已納入 active W2 predictors，後續重新執行 01-06 時會進入 drop + decomposition feature set。

| Feature Code   | Chinese Name               | English Name                                   | Items / Construction    | Scoring / Coding   |
|:---------------|:---------------------------|:-----------------------------------------------|:------------------------|:-------------------|
| v9             | 學校歸屬感與學校認同       | School Belonging and School Identification     | v9_1;v9_2;v9_3          | mean               |
| v12            | 班級同儕支持與信任         | Classmate Support and Trust                    | v12_1;v12_2;v12_3       | mean               |
| v8_03-v8_06    | 學校社會逆境與同儕壓力事件 | School Social Adversity and Peer Stress Events | v8_03;v8_04;v8_05;v8_06 | mean               |

## Active W2 Predictor Set

此表已依 `Feature Code` 排序，且拆題組列使用小題組名稱。

| Feature Code   | Original / Source Group   | Chinese Name                                   | English Name                                                                           | Feature Family              | Items / Construction                                                                       |
|:---------------|:--------------------------|:-----------------------------------------------|:---------------------------------------------------------------------------------------|:----------------------------|:-------------------------------------------------------------------------------------------|
| v1_male        | v1                        | 性別（人口統計變項）                           | Gender: Male (vs Female)                                                               | Demographic / Social Status | v1                                                                                         |
| v3             | v3                        | 主觀社會地位知覺（社會階層認知）               | Perceived Social Status (Subjective Social Status)                                     | Demographic / Social Status | v3                                                                                         |
| v5             | v5                        | 家庭凝聚力與家庭支持（家庭功能）               | Family Cohesion and Support (Family Functioning)                                       | Family / Parenting          | v5_1;v5_2;v5_3;v5_4;v5_5;v5_6                                                              |
| v6             | v6                        | 親職教養方式與親子互動品質（支持／衝突／監督） | Parenting Practices and Parent–Child Interaction Quality (Support/Conflict/Monitoring) | Family / Parenting          | v6_1;v6_2;v6_3;v6_4;v6_5;v6_6;v6_7;v6_8;v6_9;v6_10                                         |
| v9             | v9                        | 學校歸屬感與學校認同                           | School Belonging and School Identification                                             | School Context / Belonging  | v9_1;v9_2;v9_3                                                                             |
| v12            | v12                       | 班級同儕支持與信任                             | Classmate Support and Trust                                                            | School Context / Belonging  | v12_1;v12_2;v12_3                                                                          |
| v19            | v19                       | 家長學校參與與學習關注程度                     | Parental Involvement in Schooling and Academic Monitoring                              | Family / Parenting          | v19_1;v19_2;v19_3;v19_4;v19_5;v19_6;v19_7;v19_8;v19_9;v19_10                               |
| v22            | v22                       | 負向情緒情境下的線上因應與情緒調節             | Online Coping and Emotion Regulation under Distress                                    | Online / Digital Life       | v22_1;v22_2;v22_3;v22_4;v22_5;v22_6                                                        |
| v23_A          | v23                       | 選擇性正向分享                                 | Selective Positive Sharing                                                             | Online / Digital Life       | v23_1;v23_2;v23_3                                                                          |
| v23_B          | v23                       | 真實／非理想化自我呈現                         | Authentic and Less-Ideal Self-Presentation                                             | Online / Digital Life       | v23_4;v23_5;v23_6                                                                          |
| v23_C          | v23                       | 隱性社群瀏覽與被動參與                         | Covert Social Media Monitoring and Passive Participation                               | Online / Digital Life       | v23_7;v23_8;v23_9                                                                          |
| v25_A          | v25                       | 網路理想自我呈現                               | Online Ideal Self-Presentation                                                         | Online / Digital Life       | v25_1;v25_2;v25_3                                                                          |
| v25_B          | v25                       | 現實自我認同滿意度                             | Real-life Self-Satisfaction                                                            | Online / Digital Life       | v25_4;v25_5;v25_6                                                                          |
| v25_C          | v25                       | 虛實形象差異與網路沉浸                         | Online-Offline Discrepancy & Immersion                                                 | Online / Digital Life       | v25_7;v25_8;v25_9;v25_10;v25_11;v25_12;v25_13;v25_14;v25_15                                |
| v26_A          | v26                       | 線上向上社會比較                               | Online Upward Social Comparison                                                        | Online / Digital Life       | v26_1;v26_2;v26_3                                                                          |
| v26_B          | v26                       | 線上觀點搜尋與獲取                             | Online Perspective Seeking                                                             | Online / Digital Life       | v26_4;v26_5;v26_6                                                                          |
| v27_A          | v27                       | 錯失恐懼與社交監測                             | Online Peer FOMO and Social Monitoring                                                 | Online / Digital Life       | v27_1;v27_2;v27_3                                                                          |
| v27_B          | v27                       | 線上活動錯失困擾                               | Distress from Missing Online Events                                                    | Online / Digital Life       | v27_4                                                                                      |
| v28            | v28                       | 問題性網路使用與網路依賴                       | Problematic Internet Use and Internet Dependence                                       | Online / Digital Life       | v28_1;v28_2;v28_3;v28_4;v28_5;v28_6;v28_7;v28_8;v28_9;v28_10                               |
| v34            | v34                       | 現實／線下霸凌受害經驗                         | Offline Bullying Victimization                                                         | Bullying / Victimization    | v34                                                                                        |
| v36            | v36                       | 現實／線下霸凌加害經驗                         | Offline Bullying Perpetration                                                          | Bullying / Victimization    | v36                                                                                        |
| v38            | v38                       | 網路／數位霸凌受害經驗                         | Cyberbullying Victimization                                                            | Bullying / Victimization    | v38                                                                                        |
| v40            | v40                       | 網路／數位霸凌加害經驗                         | Cyberbullying Perpetration                                                             | Bullying / Victimization    | v40                                                                                        |
| v42            | v42                       | 偏差與風險行為                                 | Delinquent and Risk Behaviors                                                          | Delinquency / Risk Behavior | v42_01;v42_02;v42_03;v42_04;v42_05;v42_06;v42_07;v42_08;v42_09;v42_10;v42_11;v42_12;v42_13 |
| v49            | v49                       | 數位學習支持：學校科技課程效益知覺             | Perceived Effectiveness of School-based Digital/Technology Learning                    | Online / Digital Life       | v49                                                                                        |
| v52            | v52                       | 自我價值與正向自我概念                         | Self-Worth and Positive Self-Concept                                                   | SEL / Resilience            | v52_1;v52_2;v52_3                                                                          |
| v54_A          | v54                       | 自我覺察                                       | Self-Awareness                                                                         | SEL / Resilience            | v54_1;v54_2;v54_3                                                                          |
| v54_B          | v54                       | 自我管理                                       | Self-Management                                                                        | SEL / Resilience            | v54_4;v54_5;v54_6                                                                          |
| v54_C          | v54                       | 動機與目標導向                                 | Motivation & Goal Setting                                                              | SEL / Resilience            | v54_7;v54_8;v54_9                                                                          |
| v54_D          | v54                       | 人際技巧與社交意識                             | Social Awareness & Relationship Skills                                                 | SEL / Resilience            | v54_10;v54_11;v54_13;v54_14;v54_15                                                         |
| v54_E          | v54                       | 求助行為與社會支持                             | Help-Seeking                                                                           | SEL / Resilience            | v54_12;v54_16                                                                              |
| v54_F          | v54                       | 負責任的決策與社會影響                         | Responsible Decision-Making                                                            | SEL / Resilience            | v54_17;v54_18;v54_19;v54_20                                                                |
| v8_03-v8_06    | v8_03-v8_06               | 學校社會逆境與同儕壓力事件                     | School Social Adversity and Peer Stress Events                                         | School Context / Belonging  | v8_03;v8_04;v8_05;v8_06                                                                    |

## Observed Interpersonal Features

| Feature Code               | English Name                                    | Items / Construction                                                              | Scoring / Coding                                          |
|:---------------------------|:------------------------------------------------|:----------------------------------------------------------------------------------|:----------------------------------------------------------|
| ip_in_enemy_total          | Incoming Negative Nominations, Observed Count   | Observed online + offline negative nominations received                           | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_in_friend_total         | Incoming Friendship Nominations, Observed Count | Observed online + offline friend nominations received                             | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_offline_total           | Offline Total Nominations, Observed Count       | Observed offline friendship and offline negative nominations, sent and received   | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_online_total            | Online Total Nominations, Observed Count        | Observed online friendship and online negative nominations, sent and received     | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_out_enemy_total         | Outgoing Negative Nominations, Observed Count   | Observed online + offline negative nominations sent                               | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_out_friend_total        | Outgoing Friendship Nominations, Observed Count | Observed online + offline friend nominations sent                                 | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_received_like_ratio     | Received Positive Tie Ratio                     | Observed friend nominations received / all observed nominations received          | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_received_net            | Received Network Valence, Observed              | Observed friend nominations received minus observed negative nominations received | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_reciprocal_enemy_count  | Reciprocal Negative Ties, Observed Count        | Observed mutual negative nominations                                              | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_reciprocal_friend_count | Reciprocal Friendship Ties, Observed Count      | Observed mutual friendship nominations                                            | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_sent_like_ratio         | Sent Positive Tie Ratio                         | Observed friend nominations sent / all observed nominations sent                  | Observed, non-class-adjusted count/ratio/valence feature. |
| ip_sent_net                | Sent Network Valence, Observed                  | Observed friend nominations sent minus observed negative nominations sent         | Observed, non-class-adjusted count/ratio/valence feature. |

## Supporting Files

- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\00_methodology_and_data_audit\feature_inventory_supporting_files\main_paper_feature_inventory.xlsx`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\main_paper_results\00_methodology_and_data_audit\feature_inventory_supporting_files\main_paper_feature_inventory.csv`

## Notes

- `v9`、`v12`、`v8_03-v8_06` 目前作為 W2 predictors。
- `v8_03-v8_06` 是 W2 selected multiple-response school adversity / peer stress items，使用 row-wise mean 建立整體指標。
- 本文件刻意不列 class-adjusted interpersonal features，因為目前 main-paper Table 1 與後續模型先以 observed version 為主。