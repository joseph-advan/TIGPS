# Interpersonal Incremental Modeling Summary

## Purpose

This analysis tests whether adding the 12 respondent-class-normalized interpersonal network indicators improves prediction beyond the current drop + decomposition individual-level feature set.

## Tasks and Models

- Tasks: W2 -> W2 and W2 -> W3.
- Feature sets: decomposed features only vs decomposed + 12 interpersonal features.
- Models: plain multivariable Logistic, LASSO Logistic, and Ridge Logistic.
- Main comparison metrics: CV5 AUC, CV5 F1, CV5 accuracy, and holdout test AUC/F1.

## Interpersonal Features Added

1. Online Total Nominations, Respondent-Class-Normalized (`ip_online_total_rate_class`): Observed online friendship and online negative nominations, sent and received / same-class respondents minus 1.
2. Offline Total Nominations, Respondent-Class-Normalized (`ip_offline_total_rate_class`): Observed offline friendship and offline negative nominations, sent and received / same-class respondents minus 1.
3. Outgoing Friendship Nominations, Respondent-Class-Normalized (`ip_out_friend_total_rate_class`): Observed online + offline friend nominations sent / same-class respondents minus 1.
4. Incoming Friendship Nominations, Respondent-Class-Normalized (`ip_in_friend_total_rate_class`): Observed online + offline friend nominations received / same-class respondents minus 1.
5. Outgoing Negative Nominations, Respondent-Class-Normalized (`ip_out_enemy_total_rate_class`): Observed online + offline negative nominations sent / same-class respondents minus 1.
6. Incoming Negative Nominations, Respondent-Class-Normalized (`ip_in_enemy_total_rate_class`): Observed online + offline negative nominations received / same-class respondents minus 1.
7. Reciprocal Friendship Ties, Respondent-Class-Normalized (`ip_reciprocal_friend_count_rate_class`): Observed mutual friendship nominations / same-class respondents minus 1.
8. Reciprocal Negative Ties, Respondent-Class-Normalized (`ip_reciprocal_enemy_count_rate_class`): Observed mutual negative nominations / same-class respondents minus 1.
9. Sent Positive Tie Ratio (`ip_sent_like_ratio`): Observed friend nominations sent / all observed nominations sent.
10. Received Positive Tie Ratio (`ip_received_like_ratio`): Observed friend nominations received / all observed nominations received.
11. Sent Network Valence, Respondent-Class-Normalized (`ip_sent_net_rate_class`): Observed friend nominations sent minus observed negative nominations sent / same-class respondents minus 1.
12. Received Network Valence, Respondent-Class-Normalized (`ip_received_net_rate_class`): Observed friend nominations received minus observed negative nominations received / same-class respondents minus 1.

## Performance Delta: Plus Interpersonal Minus Baseline

| Task     | Model                  |   Delta CV auc mean |   Delta CV f1 mean |   Delta CV accuracy mean |   Delta Test AUC |   Delta Test F1 |   N features baseline |   N features plus interpersonal |
|:---------|:-----------------------|--------------------:|-------------------:|-------------------------:|-----------------:|----------------:|----------------------:|--------------------------------:|
| W2 -> W2 | LASSO Logistic         |               0.001 |              0.002 |                    0.004 |            0.002 |           0     |                    30 |                              42 |
| W2 -> W2 | Multivariable Logistic |               0     |              0.001 |                    0.002 |            0.001 |           0.002 |                    30 |                              42 |
| W2 -> W2 | Ridge Logistic         |               0.001 |              0.002 |                    0.002 |            0.002 |           0.004 |                    30 |                              42 |
| W2 -> W3 | LASSO Logistic         |              -0.002 |              0     |                    0     |            0     |           0.004 |                    30 |                              42 |
| W2 -> W3 | Multivariable Logistic |              -0.003 |             -0.003 |                   -0.003 |           -0.001 |          -0.003 |                    30 |                              42 |
| W2 -> W3 | Ridge Logistic         |              -0.002 |             -0.002 |                   -0.002 |           -0.001 |           0.001 |                    30 |                              42 |

## Interpersonal Feature Selection Summary

| Task     | Model                  |   N interpersonal features |   Interpersonal features in Top 20 |   Interpersonal relative importance sum % |   Max interpersonal relative importance % | Best-ranked interpersonal feature                       |   Best interpersonal rank | LASSO-selected interpersonal features   |
|:---------|:-----------------------|---------------------------:|-----------------------------------:|------------------------------------------:|------------------------------------------:|:--------------------------------------------------------|--------------------------:|:----------------------------------------|
| W2 -> W2 | LASSO Logistic         |                         12 |                                  3 |                                      9.8  |                                      2.19 | Sent Positive Tie Ratio                                 |                        13 | 8                                       |
| W2 -> W2 | Multivariable Logistic |                         12 |                                  1 |                                     11.46 |                                      2.25 | Sent Positive Tie Ratio                                 |                        13 |                                         |
| W2 -> W2 | Ridge Logistic         |                         12 |                                  1 |                                     11.03 |                                      2.16 | Sent Positive Tie Ratio                                 |                        13 |                                         |
| W2 -> W3 | LASSO Logistic         |                         12 |                                  1 |                                      3.17 |                                      2.19 | Reciprocal Friendship Ties, Respondent-Class-Normalized |                        19 | 4                                       |
| W2 -> W3 | Multivariable Logistic |                         12 |                                  2 |                                     13.99 |                                      3.81 | Reciprocal Friendship Ties, Respondent-Class-Normalized |                         9 |                                         |
| W2 -> W3 | Ridge Logistic         |                         12 |                                  1 |                                     10.47 |                                      2.73 | Reciprocal Friendship Ties, Respondent-Class-Normalized |                        13 |                                         |

## Interpretation Guide

Use this analysis as the bridge between Table 1 and the later LASSO Top 20 feature-importance section. Table 1 only shows group differences. This incremental model tests whether interpersonal indicators add predictive value after individual-level features are included.

A strong argument for limited interpersonal incremental value would require: small performance deltas after adding the 12 features, few interpersonal features in the LASSO Top 20, and low Ridge relative importance for interpersonal indicators.

## Diagnostics

| Task     | Feature Set                      |   n_final_features | table1_interpersonal_status   | table1_interpersonal_features_added                                                                                                                                                                                                                                                                                                                   |   aligned_target_non_missing |
|:---------|:---------------------------------|-------------------:|:------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------:|
| W2 -> W2 | decomposed_features_only         |                 30 | nan                           | nan                                                                                                                                                                                                                                                                                                                                                   |                         6603 |
| W2 -> W2 | decomposed_plus_12_interpersonal |                 42 | ok                            | ip_online_total_rate_class;ip_offline_total_rate_class;ip_out_friend_total_rate_class;ip_in_friend_total_rate_class;ip_out_enemy_total_rate_class;ip_in_enemy_total_rate_class;ip_reciprocal_friend_count_rate_class;ip_reciprocal_enemy_count_rate_class;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net_rate_class;ip_received_net_rate_class |                         6603 |
| W2 -> W3 | decomposed_features_only         |                 30 | nan                           | nan                                                                                                                                                                                                                                                                                                                                                   |                         6603 |
| W2 -> W3 | decomposed_plus_12_interpersonal |                 42 | ok                            | ip_online_total_rate_class;ip_offline_total_rate_class;ip_out_friend_total_rate_class;ip_in_friend_total_rate_class;ip_out_enemy_total_rate_class;ip_in_enemy_total_rate_class;ip_reciprocal_friend_count_rate_class;ip_reciprocal_enemy_count_rate_class;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net_rate_class;ip_received_net_rate_class |                         6603 |

