# ABCD 人際特徵比較報告（以 Drop Baseline 為基準）

## 1. 版本與命名
- 本報告只使用 `A / B / C / D` 四組代號。
- 基準模型固定為 `Drop Baseline`。
- 四組合併版本命名為 `ABCD(四組合併)`。

## 2. 四個組別在做什麼
| 組別 | 核心概念 | 欄位數 |
|---|---|---:|
| A | 基本提名 in/out 次數（四種關係的送出與收到） | 8 |
| B | friend/enemy 合計（線上+現實總量） | 4 |
| C | online-offline 差值（線上減線下） | 4 |
| D | 互惠/衝突（互相喜歡、互相討厭、交叉衝突） | 5 |
| ABCD(四組合併) | A+B+C+D 一起加入 | 21 |

### A 組欄位
`ip_out_online_friend`, `ip_in_online_friend`, `ip_out_online_enemy`, `ip_in_online_enemy`, `ip_out_offline_friend`, `ip_in_offline_friend`, `ip_out_offline_enemy`, `ip_in_offline_enemy`

### B 組欄位
`ip_out_friend_total`, `ip_out_enemy_total`, `ip_in_friend_total`, `ip_in_enemy_total`

### C 組欄位
`ip_out_friend_online_minus_offline`, `ip_out_enemy_online_minus_offline`, `ip_in_friend_online_minus_offline`, `ip_in_enemy_online_minus_offline`

### D 組欄位
`ip_reciprocal_friend_count`, `ip_reciprocal_enemy_count`, `ip_liked_by_me_but_enemy_to_me_count`, `ip_enemy_by_me_but_likes_me_count`, `ip_same_target_friend_and_enemy_count`

## 3. 每個欄位的中文意義（逐欄）
| 欄位 | 中文意義 |
|---|---|
| ip_out_online_friend | 我在線上提名「喜歡」同學的人數（送出） |
| ip_in_online_friend | 我在線上被提名為「喜歡」的人數（收到） |
| ip_out_online_enemy | 我在線上提名「不喜歡」同學的人數（送出） |
| ip_in_online_enemy | 我在線上被提名為「不喜歡」的人數（收到） |
| ip_out_offline_friend | 我在現實提名「喜歡」同學的人數（送出） |
| ip_in_offline_friend | 我在現實被提名為「喜歡」的人數（收到） |
| ip_out_offline_enemy | 我在現實提名「不喜歡」同學的人數（送出） |
| ip_in_offline_enemy | 我在現實被提名為「不喜歡」的人數（收到） |
| ip_out_friend_total | 我提名「喜歡」總數（線上+現實） |
| ip_out_enemy_total | 我提名「不喜歡」總數（線上+現實） |
| ip_in_friend_total | 我被提名「喜歡」總數（線上+現實） |
| ip_in_enemy_total | 我被提名「不喜歡」總數（線上+現實） |
| ip_out_friend_online_minus_offline | 我提名「喜歡」的線上-線下差值 |
| ip_out_enemy_online_minus_offline | 我提名「不喜歡」的線上-線下差值 |
| ip_in_friend_online_minus_offline | 我被提名「喜歡」的線上-線下差值 |
| ip_in_enemy_online_minus_offline | 我被提名「不喜歡」的線上-線下差值 |
| ip_reciprocal_friend_count | 互相喜歡的人數（雙向 friend） |
| ip_reciprocal_enemy_count | 互相不喜歡的人數（雙向 enemy） |
| ip_liked_by_me_but_enemy_to_me_count | 我喜歡對方，但對方不喜歡我的人數 |
| ip_enemy_by_me_but_likes_me_count | 我不喜歡對方，但對方喜歡我的人數 |
| ip_same_target_friend_and_enemy_count | 同一目標同時出現在我喜歡與不喜歡名單的人數 |

## 4. 整體平均（三任務平均）
| 設定 | mean_test_accuracy | mean_test_f1 | mean_test_auc |
|---|---:|---:|---:|
| Drop Baseline | 0.710102 | 0.715628 | 0.775751 |
| Drop + A | 0.708613 | 0.714575 | 0.775899 |
| Drop + B | 0.708116 | 0.714003 | 0.775796 |
| Drop + C | 0.707372 | 0.713242 | 0.775577 |
| Drop + D | 0.706627 | 0.713433 | 0.775990 |
| Drop + ABCD(四組合併) | 0.705386 | 0.712105 | 0.775856 |

## 5. 各任務結果（依 test_accuracy 由高到低）
### W2 -> W2
- Drop Baseline accuracy：**0.747580**

| 設定 | test_accuracy | delta_test_accuracy_vs_drop | test_f1 | delta_test_f1_vs_drop | test_auc | delta_test_auc_vs_drop | n_group_features_added |
|---|---:|---:|---:|---:|---:|---:|---:|
| Drop Baseline | 0.747580 | +0.000000 | 0.764747 | +0.000000 | 0.812782 | +0.000000 | 0 |
| Drop + C | 0.743857 | -0.003723 | 0.762102 | -0.002644 | 0.812857 | +0.000076 | 4 |
| Drop + D | 0.743112 | -0.004468 | 0.762233 | -0.002514 | 0.813476 | +0.000694 | 5 |
| Drop + A | 0.741623 | -0.005957 | 0.760524 | -0.004222 | 0.814199 | +0.001418 | 8 |
| Drop + B | 0.740879 | -0.006701 | 0.759336 | -0.005411 | 0.813947 | +0.001165 | 4 |
| Drop + ABCD(四組合併) | 0.739389 | -0.008191 | 0.759285 | -0.005462 | 0.813775 | +0.000993 | 21 |

### W3 -> W3
- Drop Baseline accuracy：**0.705138**

| 設定 | test_accuracy | delta_test_accuracy_vs_drop | test_f1 | delta_test_f1_vs_drop | test_auc | delta_test_auc_vs_drop | n_group_features_added |
|---|---:|---:|---:|---:|---:|---:|---:|
| Drop + A | 0.705882 | +0.000745 | 0.703676 | +0.000083 | 0.789731 | -0.001373 | 8 |
| Drop + C | 0.705882 | +0.000745 | 0.705004 | +0.001411 | 0.790765 | -0.000339 | 4 |
| Drop Baseline | 0.705138 | +0.000000 | 0.703593 | +0.000000 | 0.791104 | +0.000000 | 0 |
| Drop + B | 0.705138 | +0.000000 | 0.703148 | -0.000444 | 0.789835 | -0.001269 | 4 |
| Drop + ABCD(四組合併) | 0.702159 | -0.002978 | 0.701937 | -0.001655 | 0.790470 | -0.000634 | 21 |
| Drop + D | 0.701415 | -0.003723 | 0.700075 | -0.003518 | 0.790776 | -0.000328 | 5 |

### W2 -> W3
- Drop Baseline accuracy：**0.677587**

| 設定 | test_accuracy | delta_test_accuracy_vs_drop | test_f1 | delta_test_f1_vs_drop | test_auc | delta_test_auc_vs_drop | n_group_features_added |
|---|---:|---:|---:|---:|---:|---:|---:|
| Drop + A | 0.678332 | +0.000745 | 0.679525 | +0.000980 | 0.723765 | +0.000399 | 8 |
| Drop + B | 0.678332 | +0.000745 | 0.679525 | +0.000980 | 0.723606 | +0.000240 | 4 |
| Drop Baseline | 0.677587 | +0.000000 | 0.678545 | +0.000000 | 0.723366 | +0.000000 | 0 |
| Drop + D | 0.675354 | -0.002234 | 0.677991 | -0.000554 | 0.723719 | +0.000353 | 5 |
| Drop + ABCD(四組合併) | 0.674609 | -0.002978 | 0.675093 | -0.003452 | 0.723322 | -0.000044 | 21 |
| Drop + C | 0.672375 | -0.005212 | 0.672619 | -0.005926 | 0.723109 | -0.000257 | 4 |

## 6. 結論
- 單組別來看，A/B 在部分任務有小幅正向；C/D 多數任務偏負向或不穩定。
- `Drop + ABCD(四組合併)` 在三個任務都沒有超越 Drop Baseline。
- 建議下一步：在 A/B/C/D 中做更細的欄位篩選，再進行縮減版重跑。

