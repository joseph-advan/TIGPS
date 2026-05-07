# Current Split Subscale Review with W3 Counterpart Check

This file reviews the split subscales currently defined in `Feature_Decomposition/build_binary_drop_then_split_baseline.py`. The W3 counterpart check uses direct item-number correspondence and verifies that the columns exist in `TIGPS_W3_student_studentdata_ver5.csv`.

## Key Findings

- Current code splits 5 W2 parent groups into 13 subscale features.
- All currently split W2 items have direct W3 counterpart columns in W3 ver5 when using direct parent-group mapping: `v23 -> 25`, `v25 -> 26`, `v26 -> 27`, `v27 -> 28`, `v54 -> 53`.
- The earlier comparison table misses some direct mappings, especially for `v23`, `v25`, and `v27_4`; therefore it should not be used alone to judge W3 completeness for these split groups.
- Current model code applies the split specs only to W2 scenarios. The `w3_self` scenario currently does not split W3 groups into corresponding subscales.
- `v54`/W3 `53` has more items than the current split uses. Current split uses only items 1-9; items 10-20 need a substantive decision before modeling.
- W3 group `25` includes extra item `25-0` about whether the respondent has a social media account; it is not a direct counterpart of W2 `v23_1`-`v23_9` and is not included in the current split.

## Subscale Summary

| parent_group_w2   |   parent_group_w3 | formal_english_name                                           | formal_chinese_name                                       | subscale_current_name   |   n_w2_items | w2_items                                                    | direct_w3_items                                    | w2_columns_complete_in_ver6   | w3_columns_complete_in_ver5   | w2_question_texts_complete   | w3_question_texts_complete   | complete_w3_counterpart   |   missing_w3_columns_or_question_texts |
|:------------------|------------------:|:--------------------------------------------------------------|:----------------------------------------------------------|:------------------------|-------------:|:------------------------------------------------------------|:---------------------------------------------------|:------------------------------|:------------------------------|:-----------------------------|:-----------------------------|:--------------------------|---------------------------------------:|
| v23               |                25 | Social Media Use: Selective Sharing and Impression Management | 社群媒體使用行為：選擇性分享與印象管理                    | v23_A                   |            3 | v23_1;v23_2;v23_3                                           | 25-1;25-2;25-3                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v23               |                25 | Social Media Use: Selective Sharing and Impression Management | 社群媒體使用行為：選擇性分享與印象管理                    | v23_B                   |            3 | v23_4;v23_5;v23_6                                           | 25-4;25-5;25-6                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v23               |                25 | Social Media Use: Selective Sharing and Impression Management | 社群媒體使用行為：選擇性分享與印象管理                    | v23_C                   |            3 | v23_7;v23_8;v23_9                                           | 25-7;25-8;25-9                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v25               |                26 | Social Media Self-Presentation and Online Image Management    | 社群媒體自我呈現與網路形象管理                            | v25_A                   |            3 | v25_1;v25_2;v25_3                                           | 26-1;26-2;26-3                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v25               |                26 | Social Media Self-Presentation and Online Image Management    | 社群媒體自我呈現與網路形象管理                            | v25_B                   |            3 | v25_4;v25_5;v25_6                                           | 26-4;26-5;26-6                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v25               |                26 | Social Media Self-Presentation and Online Image Management    | 社群媒體自我呈現與網路形象管理                            | v25_C                   |            9 | v25_7;v25_8;v25_9;v25_10;v25_11;v25_12;v25_13;v25_14;v25_15 | 26-7;26-8;26-9;26-10;26-11;26-12;26-13;26-14;26-15 | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v26               |                27 | Online Social Comparison and Perspective Seeking              | 線上社會比較與觀點搜尋                                    | v26_A                   |            3 | v26_1;v26_2;v26_3                                           | 27-1;27-2;27-3                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v26               |                27 | Online Social Comparison and Perspective Seeking              | 線上社會比較與觀點搜尋                                    | v26_B                   |            3 | v26_4;v26_5;v26_6                                           | 27-4;27-5;27-6                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v27               |                28 | Online Peer Interaction Anxiety (Fear of Missing Out, FOMO)   | 網路同儕互動焦慮（錯失恐懼／FOMO）                        | v27_A                   |            3 | v27_1;v27_2;v27_3                                           | 28-1;28-2;28-3                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v27               |                28 | Online Peer Interaction Anxiety (Fear of Missing Out, FOMO)   | 網路同儕互動焦慮（錯失恐懼／FOMO）                        | v27_B                   |            1 | v27_4                                                       | 28-4                                               | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v54               |                53 | Social and Emotional Learning (SEL) Competencies              | 社會與情緒學習能力（SEL：情緒覺察、調節、人際與目標管理） | v54_A                   |            3 | v54_1;v54_2;v54_3                                           | 53-1;53-2;53-3                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v54               |                53 | Social and Emotional Learning (SEL) Competencies              | 社會與情緒學習能力（SEL：情緒覺察、調節、人際與目標管理） | v54_B                   |            3 | v54_4;v54_5;v54_6                                           | 53-4;53-5;53-6                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |
| v54               |                53 | Social and Emotional Learning (SEL) Competencies              | 社會與情緒學習能力（SEL：情緒覺察、調節、人際與目標管理） | v54_C                   |            3 | v54_7;v54_8;v54_9                                           | 53-7;53-8;53-9                                     | True                          | True                          | True                         | True                         | True                      |                                    nan |

## Item-Level W2 to W3 Mapping

### v23_A (Social Media Use: Selective Sharing and Impression Management)

| w2_item   | w2_question_text                                                                                           | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                                     |
|:----------|:-----------------------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:---------------------------------------------------------------------------------------------------------------------|
| v23_1     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (1)我只會發布自己看起來高興、愉快的照片               | 25-1             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-1.我只會發佈自己看起來高興、愉快的照片。               |
| v23_2     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (2)我會刻意選擇自己看起來好看的照片發佈               | 25-2             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-2.我會刻意選擇自己看起來好看的照片發佈。               |
| v23_3     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (3)我會發佈對自己形象加分的訊息，即使那不是真實的情況 | 25-3             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-3.我會發佈對自己形象加分的訊息，即使那不是真實的情況。 |

### v23_B (Social Media Use: Selective Sharing and Impression Management)

| w2_item   | w2_question_text                                                                                       | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                                |
|:----------|:-------------------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:----------------------------------------------------------------------------------------------------------------|
| v23_4     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (4)我不會介意發佈自己不太好看的照片               | 25-4             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-4我不會介意發佈自己不太好看的照片。               |
| v23_5     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (5)我不介意發佈可能對自己形象扣分的貼文           | 25-5             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-5我不介意發佈可能對自己形象扣分的貼文。           |
| v23_6     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (6)我不介意在我的社群媒體上寫下發生在我身上的壞事 | 25-6             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-6我不介意在我的社群媒體上寫下發生在我身上的壞事。 |

### v23_C (Social Media Use: Selective Sharing and Impression Management)

| w2_item   | w2_question_text                                                                                                       | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                                                 |
|:----------|:-----------------------------------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| v23_7     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (7)我會用不被發現的方式，瀏覽人們在網路上的訊息                   | 25-7             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-7.我會用不被發現的方式，瀏覽人們在網路上的訊息。                   |
| v23_8     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (8)我會隱藏自己正在線上活動的紀錄                                 | 25-8             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-8.我會隱藏自己正在線上活動的紀錄。                                 |
| v23_9     | 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 (9)我會避免加入朋友們在社群媒體上的對話，即便我正在看著他們的訊息 | 25-9             | True                     | 25. 關於你在社群媒體上的行為，以下敘述符不符合你的情況。 - 25-9.我會避免加入朋友們在社群媒體上的對話，即便我正在看著他們的訊息。 |

### v25_A (Social Media Self-Presentation and Online Image Management)

| w2_item   | w2_question_text                                                                 | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                          |
|:----------|:---------------------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------------|
| v25_1     | 以下描述符不符合你的個人經驗感受呢？ (1)我喜歡自己在網路上的形象                 | 26-1             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-1.我喜歡自己在網路上的形象。                 |
| v25_2     | 以下描述符不符合你的個人經驗感受呢？ (2)我在網路上可以表現出我最好的一面         | 26-2             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-2.我在網路上可以表現出我最好的一面。         |
| v25_3     | 以下描述符不符合你的個人經驗感受呢？ (3)在網路世界中我覺得自己可以成為理想的自己 | 26-3             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-3.在網路世界中我覺得自己可以成為理想的自己。 |

### v25_B (Social Media Self-Presentation and Online Image Management)

| w2_item   | w2_question_text                                                                 | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                          |
|:----------|:---------------------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------------|
| v25_4     | 以下描述符不符合你的個人經驗感受呢？ (4)我喜歡自己在現實生活裡的形象             | 26-4             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-4.我喜歡自己在現實生活裡的形象。             |
| v25_5     | 以下描述符不符合你的個人經驗感受呢？ (5)我在現實生活裡可以表現出我最好的一面     | 26-5             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-5.我在現實生活裡可以表現出我最好的一面。     |
| v25_6     | 以下描述符不符合你的個人經驗感受呢？ (6)在現實生活裡我覺得自己可以成為理想的自己 | 26-6             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-6.在現實生活裡我覺得自己可以成為理想的自己。 |

### v25_C (Social Media Self-Presentation and Online Image Management)

| w2_item   | w2_question_text                                                                              | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                       |
|:----------|:----------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:-------------------------------------------------------------------------------------------------------|
| v25_7     | 以下描述符不符合你的個人經驗感受呢？ (7)我在網路世界裡經常會扮演成不一樣的角色                | 26-7             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-7.我在網路世界裡經常會扮演成不一樣的角色。                |
| v25_8     | 以下描述符不符合你的個人經驗感受呢？ (8)我在不同的社群媒體中（如臉書、IG）會有不一樣的形象    | 26-8             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-8.我在不同的社群媒體中（如臉書、IG）會有不一樣的形象。    |
| v25_9     | 以下描述符不符合你的個人經驗感受呢？ (9)我喜歡在網路上擁有多種不一樣的身分、形象或樣貌        | 26-9             | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-9.我喜歡在網路上擁有多種不一樣的身分、形象或樣貌。        |
| v25_10    | 以下描述符不符合你的個人經驗感受呢？ (10)我在網路上呈現自我的方式，與在現實生活的自我並不相同 | 26-10            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-10.我在網路上呈現自我的方式，與在現實生活的自我並不相同。 |
| v25_11    | 以下描述符不符合你的個人經驗感受呢？ (11)我覺得我在網絡世界和現實世界中是不同的人             | 26-11            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-11.我覺得我在網路世界和現實世界中是不同的人。             |
| v25_12    | 以下描述符不符合你的個人經驗感受呢？ (12)我在網路世界中表現出與現實世界中截然不同的言行舉止   | 26-12            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-12.我在網路世界中表現出與現實世界中截然不同的言行舉止。   |
| v25_13    | 以下描述符不符合你的個人經驗感受呢？ (13)比起在現實生活，我覺得自己在網路上比較輕鬆自在       | 26-13            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-13.比起在現實生活，我覺得自己在網路上比較輕鬆自在。       |
| v25_14    | 以下描述符不符合你的個人經驗感受呢？ (14)我喜歡在網路上的生活，勝過於現實中的生活             | 26-14            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-14.我喜歡在網路上的生活，勝過於現實中的生活。             |
| v25_15    | 以下描述符不符合你的個人經驗感受呢？ (15)如果可以，我希望自己可以一直待在網路上               | 26-15            | True                     | 26.以下描述符不符合你的個人經驗感受呢？ - 26-15.如果可以，我希望自己可以一直待在網路上。               |

### v26_A (Online Social Comparison and Perspective Seeking)

| w2_item   | w2_question_text                                                                                       | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                                |
|:----------|:-------------------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:----------------------------------------------------------------------------------------------------------------|
| v26_1     | 關於你在網路上的意見表達，以下敘述你同不同意？ (1)我經常會在網路上和他人比較自己在生活上獲得的成就     | 27-1             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-1.我經常會在網路上和他人比較自己在生活上獲得的成就。     |
| v26_2     | 關於你在網路上的意見表達，以下敘述你同不同意？ (2)我總是在網路上留意他人的表現，並和自己的表現進行比較 | 27-2             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-2.我總是在網路上留意他人的表現，並和自己的表現進行比較。 |
| v26_3     | 關於你在網路上的意見表達，以下敘述你同不同意？ (3)我經常在網路上和他人比較自己受歡迎的程度             | 27-3             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-3.我經常在網路上和他人比較自己受歡迎的程度。             |

### v26_B (Online Social Comparison and Perspective Seeking)

| w2_item   | w2_question_text                                                                                               | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                                                        |
|:----------|:---------------------------------------------------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------------------------------------------|
| v26_4     | 關於你在網路上的意見表達，以下敘述你同不同意？ (4)如果我想要更瞭解某些事情，我會試著去網路上看看別人的想法     | 27-4             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-4.如果我想要更瞭解某些事情，我會試著去網路上看看別人的想法。     |
| v26_5     | 關於你在網路上的意見表達，以下敘述你同不同意？ (5)我總是好奇網路上的人們在和我遇到相同的問題時會怎麼想或怎麼做 | 27-5             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-5.我總是好奇網路上的人們在和我遇到相同的問題時會怎麼想或怎麼做。 |
| v26_6     | 關於你在網路上的意見表達，以下敘述你同不同意？ (6)我喜歡在網路上看看其他人的不同觀點和經歷                     | 27-6             | True                     | 27.關於你在網路上的意見表達，以下敘述你同不同意？ - 27-6.我喜歡在網路上看看其他人的不同觀點和經歷。                     |

### v27_A (Online Peer Interaction Anxiety (Fear of Missing Out, FOMO))

| w2_item   | w2_question_text                                                                 | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                          |
|:----------|:---------------------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------------------|
| v27_1     | 你同不同意以下說法？ (1)沒跟上朋友們在網路上聊天或開玩笑的話題，會讓我感到很焦慮 | 28-1             | True                     | 28.你同不同意以下說法？ - 28-1.沒跟上朋友們在網路上聊天或開玩笑的話題，會讓我感到很焦慮。 |
| v27_2     | 你同不同意以下說法？ (2)錯過和朋友們在網路上的聚會，會讓我感到很困擾             | 28-2             | True                     | 28.你同不同意以下說法？ - 28-2.錯過和朋友們在網路上的聚會，會讓我感到很困擾。             |
| v27_3     | 你同不同意以下說法？ (3)我會隨時透過網路追蹤朋友們的行蹤和做的事情               | 28-3             | True                     | 28.你同不同意以下說法？ - 28-3.我會隨時透過網路追蹤朋友們的行蹤和做的事情                 |

### v27_B (Online Peer Interaction Anxiety (Fear of Missing Out, FOMO))

| w2_item   | w2_question_text                                                       | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                              |
|:----------|:-----------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------|
| v27_4     | 你同不同意以下說法？ (4)沒跟上網路上的首播、直播或活動，我會感到很困擾 | 28-4             | True                     | 28.你同不同意以下說法？ - 28-4.沒跟上網路上的首播、直播或活動，我會感到很困擾 |

### v54_A (Social and Emotional Learning (SEL) Competencies)

| w2_item   | w2_question_text                                                             | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                                      |
|:----------|:-----------------------------------------------------------------------------|:-----------------|:-------------------------|:--------------------------------------------------------------------------------------|
| v54_1     | 你有多同意下列的敘述？ (1)當我緊張的時候，我可以感覺到身體的變化，如心跳加快 | 53-1             | True                     | 53.你有多同意下列的敘述？ - 53-1.當我緊張的時候，我可以感覺到身體的變化，如心跳加快。 |
| v54_2     | 你有多同意下列的敘述？ (2)當我的情緒讓我無法專注的時候，我會感覺到           | 53-2             | True                     | 53.你有多同意下列的敘述？ - 53-2.當我的情緒讓我無法專注的時候，我會感覺到。           |
| v54_3     | 你有多同意下列的敘述？ (3)我可以感受到自己的情緒                             | 53-3             | True                     | 53.你有多同意下列的敘述？ - 53-3.我可以感受到自己的情緒。                             |

### v54_B (Social and Emotional Learning (SEL) Competencies)

| w2_item   | w2_question_text                                                     | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                              |
|:----------|:---------------------------------------------------------------------|:-----------------|:-------------------------|:------------------------------------------------------------------------------|
| v54_4     | 你有多同意下列的敘述？ (4)當我難過的時候，我知道如何讓自己感覺好一點 | 53-4             | True                     | 53.你有多同意下列的敘述？ - 53-4.當我難過的時候，我知道如何讓自己感覺好一點。 |
| v54_5     | 你有多同意下列的敘述？ (5)我知道如何讓自己平靜下來                   | 53-5             | True                     | 53.你有多同意下列的敘述？ - 53-5.我知道如何讓自己平靜下來。                   |
| v54_6     | 你有多同意下列的敘述？ (6)當我感到沮喪時，我會調整自己以度過低潮     | 53-6             | True                     | 53.你有多同意下列的敘述？ - 53-6.當我感到沮喪時，我會調整自己以度過低潮。     |

### v54_C (Social and Emotional Learning (SEL) Competencies)

| w2_item   | w2_question_text                                           | direct_w3_item   | w3_item_exists_in_ver5   | w3_question_text                                                    |
|:----------|:-----------------------------------------------------------|:-----------------|:-------------------------|:--------------------------------------------------------------------|
| v54_7     | 你有多同意下列的敘述？ (7)我會為自己設定目標               | 53-7             | True                     | 53.你有多同意下列的敘述？ - 53-7.我會為自己設定目標。               |
| v54_8     | 你有多同意下列的敘述？ (8)我會達成自己所設定的目標         | 53-8             | True                     | 53.你有多同意下列的敘述？ - 53-8.我會達成自己所設定的目標。         |
| v54_9     | 你有多同意下列的敘述？ (9)我會思考達到目標所需要採取的步驟 | 53-9             | True                     | 53.你有多同意下列的敘述？ - 53-9.我會思考達到目標所需要採取的步驟。 |

## Items Not Used by Current Split Specs

| parent_group_w2   |   parent_group_w3 | w2_item   | direct_w3_item   | w2_column_exists   | w3_column_exists   | reason_not_in_current_split                        |
|:------------------|------------------:|:----------|:-----------------|:-------------------|:-------------------|:---------------------------------------------------|
| v23               |                25 | nan       | 25-0             | False              | True               | W3-only or filter item; no direct W2 column exists |
| v54               |                53 | v54_10    | 53-10            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_11    | 53-11            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_12    | 53-12            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_13    | 53-13            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_14    | 53-14            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_15    | 53-15            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_16    | 53-16            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_17    | 53-17            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_18    | 53-18            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_19    | 53-19            | True               | True               | not included in current W2 split specs             |
| v54               |                53 | v54_20    | 53-20            | True               | True               | not included in current W2 split specs             |
