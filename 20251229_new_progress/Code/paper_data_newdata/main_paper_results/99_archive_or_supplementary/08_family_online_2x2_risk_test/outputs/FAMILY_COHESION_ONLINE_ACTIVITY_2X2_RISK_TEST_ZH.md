# Family Cohesion x Online Activity 2x2 Risk Test

## 這個測試在回答什麼

這個 08 測試不是取代 06 的交互作用模型，而是把 06 中最重要的 Family Cohesion x Online Activity 結果改成更直覺的 2x2 組別比較。

分組方式：

- Family Cohesion：使用 W2 `v5` 題組分數，以 W2 中位數切成 High / Low。
- Online Activity：使用 W2 `v21_3` 到 `v21_6` 加總分數，以 W2 中位數切成 High / Low。
- Outcome：High Psychological Distress，使用各任務的心理困擾題組加總後以中位數切分。

四組為：

1. High Family Cohesion + Low Online Activity
2. High Family Cohesion + High Online Activity
3. Low Family Cohesion + Low Online Activity
4. Low Family Cohesion + High Online Activity

## 主要結果：W2 -> W3

W2 -> W3 中，高心理困擾比例最高的組別是 `Low Family Cohesion + High Online Activity`，比例為 62.0%（n=1824）。
你關心的 `Low Family Cohesion + High Online Activity` 組別，高心理困擾比例為 62.0%（n=1824），風險排名第 1。

## 2x2 interaction 係數怎麼看

這裡也用老師給的公式概念重新估計一次，但把 Family Cohesion 也切成 High / Low：

```text
logit(P(High Psychological Distress = 1))
= b0 + b1 * LowFamily + b2 * HighOnline + b3 * LowFamily * HighOnline
```

在這個設定中：

- `b0`：High Family Cohesion + Low Online Activity 的 baseline logit。
- `b1`：在 Low Online Activity 裡，Low Family 比 High Family 多出的差異。
- `b2`：在 High Family Cohesion 裡，High Online 比 Low Online 多出的差異。
- `b3`：Low Family + High Online 這個組合是否有額外加乘風險。

W2 -> W3 的 `b3` = 0.1197，p = 0.243。

這代表目前沒有足夠證據說 `Low Family Cohesion + High Online Activity` 有超過兩個主效果相加之外的額外加乘風險。

## 可以怎麼寫

較保守、符合目前統計結果的寫法：

> We further examined whether students with lower family cohesion and high online activity constituted a higher-risk subgroup. A 2x2 group comparison was conducted using median splits of W2 family cohesion and W2 online activity. This analysis provides an intuitive subgroup-level description of future psychological distress risk, complementing the continuous interaction model in Section 06.

中文解釋：這個測試可以用來說明不同家庭支持與網路活躍組合下，未來高心理困擾比例是否不同。但如果 `b3` 不顯著，就不要說明確存在加乘反效果；可以說是描述性風險分層。

## 輸出檔案

- `family_cohesion_online_activity_2x2_risk_test.xlsx`：包含 group summary、group logistic、2x2 teacher-equivalent interaction、diagnostics。

## Diagnostics

- wave: W2
- feature_set: drop_plus_decomposition
- n_rows: 6603
- n_predictor_columns: 30
- drop_group_ids: v50;v51;v52_health;v57
- split_group_ids: v23;v25;v26;v27;v54
- direct_feature_ids: v52_health
- skipped_no_mapping: 
- skipped_no_columns: 
- table1_interpersonal_status: ok
- table1_interpersonal_version: observed_count
- table1_interpersonal_features_added: ip_online_total;ip_offline_total;ip_out_friend_total;ip_in_friend_total;ip_out_enemy_total;ip_in_enemy_total;ip_reciprocal_friend_count;ip_reciprocal_enemy_count;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net;ip_received_net
- table1_interpersonal_features_missing: 
- online_activity_items: ['v21_3', 'v21_4', 'v21_5', 'v21_6']
- online_activity_definition: sum(v21_3 to v21_6) > W2 median
- online_activity_complete_rows: 6546
- online_activity_median: 15.0
- high_online_n: 3035
- low_online_n: 3511
- missing_online_n: 57
- Task: W2 -> W2
- target_items: ['v55_1', 'v55_2', 'v55_3', 'v55_4', 'v55_5', 'v55_6', 'v55_7', 'v55_8', 'v55_9', 'v55_10', 'v55_11', 'v55_12', 'v55_13', 'v55_14']
- target_score_aggregation: sum
- target_min_valid_items: 7
- target_median_cutoff: 17.0
- target_non_missing: 6603
- target_positive: 3576
- target_negative: 3027
- family_feature_code: v5
- family_feature_column: feature_v5
- family_feature_name: Family Cohesion and Support (Family Functioning)
- family_split_definition: High Family Cohesion = feature_v5 > W2 median; Low Family Cohesion = feature_v5 <= W2 median.
- family_median: 3.1666666666666665
- high_family_n: 2918
- low_family_n: 3685
- missing_family_n: 0
- analysis_n: 6546
- wave: W2
- feature_set: drop_plus_decomposition
- n_rows: 6603
- n_predictor_columns: 30
- drop_group_ids: v50;v51;v52_health;v57
- split_group_ids: v23;v25;v26;v27;v54
- direct_feature_ids: v52_health
- skipped_no_mapping: 
- skipped_no_columns: 
- table1_interpersonal_status: ok
- table1_interpersonal_version: observed_count
- table1_interpersonal_features_added: ip_online_total;ip_offline_total;ip_out_friend_total;ip_in_friend_total;ip_out_enemy_total;ip_in_enemy_total;ip_reciprocal_friend_count;ip_reciprocal_enemy_count;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net;ip_received_net
- table1_interpersonal_features_missing: 
- online_activity_items: ['v21_3', 'v21_4', 'v21_5', 'v21_6']
- online_activity_definition: sum(v21_3 to v21_6) > W2 median
- online_activity_complete_rows: 6546
- online_activity_median: 15.0
- high_online_n: 3035
- low_online_n: 3511
- missing_online_n: 57
- Task: W2 -> W3
- target_items: ['54-1', '54-2', '54-3', '54-4', '54-5', '54-6', '54-7', '54-8', '54-9', '54-10', '54-11', '54-12', '54-13', '54-14']
- target_score_aggregation: sum
- target_min_valid_items: 7
- target_median_cutoff: 21.0
- target_non_missing: 6603
- target_positive: 3474
- target_negative: 3129
- family_feature_code: v5
- family_feature_column: feature_v5
- family_feature_name: Family Cohesion and Support (Family Functioning)
- family_split_definition: High Family Cohesion = feature_v5 > W2 median; Low Family Cohesion = feature_v5 <= W2 median.
- family_median: 3.1666666666666665
- high_family_n: 2918
- low_family_n: 3685
- missing_family_n: 0
- analysis_n: 6546
