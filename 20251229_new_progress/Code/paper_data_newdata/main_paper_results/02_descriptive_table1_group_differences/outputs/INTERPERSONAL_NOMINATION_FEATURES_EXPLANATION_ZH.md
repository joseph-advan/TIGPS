# Interpersonal Nomination Features Explanation

## 目的

這份文件說明 Table 1 與後續模型中使用的 12 個提名相關人際網絡特徵。這些特徵來自學生在同班同學中的線上/線下、正向/負向提名。

目前 03 模型使用的是 observed 版本，也就是未除以同班人數的原始觀察提名數或比例。

## 版本說明

### Observed Count / Observed

這是目前 03 模型使用的版本。

它代表學生實際送出或收到的提名數、互相提名數、正向比例，或正向減負向的淨值。

### Respondent-Class-Normalized

這是 Table 1 中另外保留的描述版本。

它會把 count 類特徵除以：

```text
same-class respondents minus 1
```

也就是用同班有填問卷的人數調整班級大小差異。這個版本適合做 sensitivity 或描述比較，但目前 03 模型已改成 observed 版本。

## 12 個 observed 提名特徵

| Feature Code | Feature Name | 中文解釋 | 計算概念 |
|---|---|---|---|
| `ip_online_total` | Online Total Nominations, Observed Count | 線上總提名數 | 線上朋友提名與線上負向提名的送出與收到總和 |
| `ip_offline_total` | Offline Total Nominations, Observed Count | 線下總提名數 | 線下朋友提名與線下負向提名的送出與收到總和 |
| `ip_out_friend_total` | Outgoing Friendship Nominations, Observed Count | 送出的朋友提名數 | 學生主動提名別人為朋友的總數，包含線上與線下 |
| `ip_in_friend_total` | Incoming Friendship Nominations, Observed Count | 收到的朋友提名數 | 學生被別人提名為朋友的總數，包含線上與線下 |
| `ip_out_enemy_total` | Outgoing Negative Nominations, Observed Count | 送出的負向提名數 | 學生主動提名別人為負向對象的總數，包含線上與線下 |
| `ip_in_enemy_total` | Incoming Negative Nominations, Observed Count | 收到的負向提名數 | 學生被別人提名為負向對象的總數，包含線上與線下 |
| `ip_reciprocal_friend_count` | Reciprocal Friendship Ties, Observed Count | 互相朋友提名數 | 學生和同學彼此互相提名為朋友的數量 |
| `ip_reciprocal_enemy_count` | Reciprocal Negative Ties, Observed Count | 互相負向提名數 | 學生和同學彼此互相負向提名的數量 |
| `ip_sent_like_ratio` | Sent Positive Tie Ratio | 送出提名中的正向比例 | 送出的朋友提名數 / 送出的全部提名數 |
| `ip_received_like_ratio` | Received Positive Tie Ratio | 收到提名中的正向比例 | 收到的朋友提名數 / 收到的全部提名數 |
| `ip_sent_net` | Sent Network Valence, Observed | 送出提名淨值 | 送出的朋友提名數減去送出的負向提名數 |
| `ip_received_net` | Received Network Valence, Observed | 收到提名淨值 | 收到的朋友提名數減去收到的負向提名數 |

## 特徵分類邏輯

### 1. 線上與線下提名總量

`ip_online_total` 與 `ip_offline_total` 用來描述一個學生在人際提名網絡中的整體線上/線下活躍程度。

這兩個特徵不是單純正向或負向，而是把朋友提名與負向提名都加總起來，因此比較像是整體互動量。

### 2. 送出與收到的朋友提名

`ip_out_friend_total` 與 `ip_in_friend_total` 描述正向同儕連結。

- 送出朋友提名較多：代表學生主動指出更多正向同儕關係。
- 收到朋友提名較多：代表學生被更多同儕視為正向關係對象。

### 3. 送出與收到的負向提名

`ip_out_enemy_total` 與 `ip_in_enemy_total` 描述負向同儕連結。

- 送出負向提名較多：代表學生主觀上指出更多負向同儕關係。
- 收到負向提名較多：代表學生被更多同儕視為負向關係對象。

### 4. 互相提名

`ip_reciprocal_friend_count` 與 `ip_reciprocal_enemy_count` 描述關係是否是雙向的。

互相朋友提名代表雙方都認定彼此是正向關係；互相負向提名代表雙方都認定彼此是負向關係。

### 5. 正向比例

`ip_sent_like_ratio` 與 `ip_received_like_ratio` 是比例，不是 count。

它們用來看一個學生的提名結構偏正向或偏負向。

例如：

```text
ip_sent_like_ratio = friend nominations sent / all nominations sent
```

如果值越高，代表學生送出的提名中正向提名比例越高。

### 6. 網絡淨值

`ip_sent_net` 與 `ip_received_net` 是正向提名數減去負向提名數。

正值代表正向提名多於負向提名；負值代表負向提名多於正向提名。

## 和 03 模型的一致性

03 的 `decomposed_plus_12_interpersonal` 模型目前使用上述 12 個 observed features。

因此如果要讓 Table 1 和 03 模型完全一致，請優先閱讀：

```text
table1_w2_to_w2_observed_network.xlsx
table1_w2_to_w3_observed_network.xlsx
```

`class_adjusted_network` 版本仍可作為補充描述，但它不是目前 03 模型使用的主要版本。
