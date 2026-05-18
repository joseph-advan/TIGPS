# Interpersonal Incremental Modeling Summary

## Purpose

This analysis tests whether adding the 12 respondent-class-normalized interpersonal network indicators improves prediction beyond the current drop + decomposition individual-level feature set.

## Tasks and Models

- Tasks: W2 -> W2 and W2 -> W3.
- Feature sets: decomposed features only vs decomposed + 12 interpersonal features.
- Models: plain multivariable Logistic, LASSO Logistic, and Ridge Logistic.
- Main comparison metrics: CV5 AUC, CV5 F1, CV5 accuracy, and holdout test AUC/F1.

## Interpersonal Features Added

1. Online Total Nominations, Observed Count (`ip_online_total`): Observed online friendship and online negative nominations, sent and received.
2. Offline Total Nominations, Observed Count (`ip_offline_total`): Observed offline friendship and offline negative nominations, sent and received.
3. Outgoing Friendship Nominations, Observed Count (`ip_out_friend_total`): Observed online + offline friend nominations sent.
4. Incoming Friendship Nominations, Observed Count (`ip_in_friend_total`): Observed online + offline friend nominations received.
5. Outgoing Negative Nominations, Observed Count (`ip_out_enemy_total`): Observed online + offline negative nominations sent.
6. Incoming Negative Nominations, Observed Count (`ip_in_enemy_total`): Observed online + offline negative nominations received.
7. Reciprocal Friendship Ties, Observed Count (`ip_reciprocal_friend_count`): Observed mutual friendship nominations.
8. Reciprocal Negative Ties, Observed Count (`ip_reciprocal_enemy_count`): Observed mutual negative nominations.
9. Sent Positive Tie Ratio (`ip_sent_like_ratio`): Observed friend nominations sent / all observed nominations sent.
10. Received Positive Tie Ratio (`ip_received_like_ratio`): Observed friend nominations received / all observed nominations received.
11. Sent Network Valence, Observed (`ip_sent_net`): Observed friend nominations sent minus observed negative nominations sent.
12. Received Network Valence, Observed (`ip_received_net`): Observed friend nominations received minus observed negative nominations received.

## Performance Delta: Plus Interpersonal Minus Baseline

| Task     | Model                  |   Delta CV auc mean |   Delta CV f1 mean |   Delta CV accuracy mean |   Delta Test AUC |   Delta Test F1 |   N features baseline |   N features plus interpersonal |
|:---------|:-----------------------|--------------------:|-------------------:|-------------------------:|-----------------:|----------------:|----------------------:|--------------------------------:|
| W2 -> W2 | LASSO Logistic         |               0     |              0.001 |                    0.002 |            0.002 |          -0.002 |                    30 |                              42 |
| W2 -> W2 | Multivariable Logistic |               0     |              0.002 |                    0.002 |            0.001 |           0     |                    30 |                              42 |
| W2 -> W2 | Ridge Logistic         |               0     |             -0.001 |                    0     |            0.002 |           0     |                    30 |                              42 |
| W2 -> W3 | LASSO Logistic         |              -0.003 |              0     |                    0.001 |           -0.001 |          -0.001 |                    30 |                              42 |
| W2 -> W3 | Multivariable Logistic |              -0.003 |             -0.001 |                   -0.001 |           -0.002 |          -0.002 |                    30 |                              42 |
| W2 -> W3 | Ridge Logistic         |              -0.002 |             -0.002 |                   -0.002 |           -0.002 |          -0.005 |                    30 |                              42 |

## Interpersonal Feature Selection Summary

| Task     | Model                  |   N interpersonal features |   Interpersonal features in Top 20 |   Interpersonal relative importance sum % |   Max interpersonal relative importance % | Best-ranked interpersonal feature          |   Best interpersonal rank | LASSO-selected interpersonal features   |
|:---------|:-----------------------|---------------------------:|-----------------------------------:|------------------------------------------:|------------------------------------------:|:-------------------------------------------|--------------------------:|:----------------------------------------|
| W2 -> W2 | LASSO Logistic         |                         12 |                                  2 |                                      5.19 |                                      1.63 | Sent Positive Tie Ratio                    |                        17 | 7                                       |
| W2 -> W2 | Multivariable Logistic |                         12 |                                  2 |                                     10.55 |                                      1.97 | Sent Positive Tie Ratio                    |                        13 |                                         |
| W2 -> W2 | Ridge Logistic         |                         12 |                                  2 |                                      9.91 |                                      1.83 | Sent Positive Tie Ratio                    |                        16 |                                         |
| W2 -> W3 | LASSO Logistic         |                         12 |                                  0 |                                      3.95 |                                      1.63 | Reciprocal Friendship Ties, Observed Count |                        22 | 4                                       |
| W2 -> W3 | Multivariable Logistic |                         12 |                                  2 |                                     13.72 |                                      3.41 | Reciprocal Friendship Ties, Observed Count |                        10 |                                         |
| W2 -> W3 | Ridge Logistic         |                         12 |                                  1 |                                     10.57 |                                      2.52 | Reciprocal Friendship Ties, Observed Count |                        15 |                                         |

## Interpretation Guide

Use this analysis as the bridge between Table 1 and the later LASSO Top 20 feature-importance section. Table 1 only shows group differences. This incremental model tests whether interpersonal indicators add predictive value after individual-level features are included.

A strong argument for limited interpersonal incremental value would require: small performance deltas after adding the 12 features, few interpersonal features in the LASSO Top 20, and low Ridge relative importance for interpersonal indicators.

## Diagnostics

| Task     | Feature Set                      |   n_final_features | table1_interpersonal_status   | table1_interpersonal_features_added                                                                                                                                                                                                     |   aligned_target_non_missing |
|:---------|:---------------------------------|-------------------:|:------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------:|
| W2 -> W2 | decomposed_features_only         |                 30 | nan                           | nan                                                                                                                                                                                                                                     |                         6603 |
| W2 -> W2 | decomposed_plus_12_interpersonal |                 42 | ok                            | ip_online_total;ip_offline_total;ip_out_friend_total;ip_in_friend_total;ip_out_enemy_total;ip_in_enemy_total;ip_reciprocal_friend_count;ip_reciprocal_enemy_count;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net;ip_received_net |                         6603 |
| W2 -> W3 | decomposed_features_only         |                 30 | nan                           | nan                                                                                                                                                                                                                                     |                         6603 |
| W2 -> W3 | decomposed_plus_12_interpersonal |                 42 | ok                            | ip_online_total;ip_offline_total;ip_out_friend_total;ip_in_friend_total;ip_out_enemy_total;ip_in_enemy_total;ip_reciprocal_friend_count;ip_reciprocal_enemy_count;ip_sent_like_ratio;ip_received_like_ratio;ip_sent_net;ip_received_net |                         6603 |

