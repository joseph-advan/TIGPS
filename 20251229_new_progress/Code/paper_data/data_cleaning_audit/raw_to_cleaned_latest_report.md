# Raw Data to Cleaned Data Audit (W2)

## 0. Scope

- Raw data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\other\TIGPS_W2_studentdata_ver0.csv`
- Cleaned data: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver11.csv`
- Matching key: `student_oid`
- Matched sample size: `7023`
- This report is regenerated to fix encoding/readability issues.

## 1. Main Cleaning Rules (excluding v14*, v58*, v59*, v61, v62; v15/v3 are independent groups here)

This section lists full observed raw-label to cleaned-value mappings for each group (not truncated examples).

### G_V15_INDEPENDENT
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v15`
- Purpose: independent item-level option analysis (full option list).
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `6` pairs):
  - `1. 全班五名以內` -> `1.0` (`n=1428`)
  - `2. 全班六至十名` -> `2.0` (`n=1430`)
  - `3. 全班十一至二十名` -> `3.0` (`n=2543`)
  - `4. 全班二十一至三十名` -> `4.0` (`n=1273`)
  - `5. 全班三十名以後` -> `5.0` (`n=338`)
  - `-9` -> `<EMPTY>` (`n=11`)

### G_V3_INDEPENDENT
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v3`
- Purpose: independent item-level option analysis (full option list).
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `11` pairs):
  - `1. 1最底層` -> `1.0` (`n=114`)
  - `2. 2` -> `2.0` (`n=144`)
  - `3. 3` -> `3.0` (`n=250`)
  - `4. 4` -> `4.0` (`n=555`)
  - `5. 5` -> `5.0` (`n=1911`)
  - `6. 6` -> `6.0` (`n=1736`)
  - `7. 7` -> `7.0` (`n=1300`)
  - `8. 8` -> `8.0` (`n=550`)
  - `9. 9` -> `9.0` (`n=157`)
  - `10. 10最頂層` -> `10.0` (`n=296`)
  - `-9` -> `<EMPTY>` (`n=10`)

### G01
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v10, v11, v12, v19, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v4, v43, v44, v45, v49, v5, v51, v52, v54, v6, v7, v9`
- Covered column count: `152`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4`; sentinel: `-9->EMPTY`
- Consistency check: raw label mapping ambiguity count = `0`
- 下列依選項語意分組，並在每個子項目列出包含題組。

#### G01-1 信任程度
- 包含題組：`v30, v31, v32, v33`
- `1. 總是可以信任的` -> `1.0` (`n=2393`)
- `2. 大部分時候可以信任` -> `2.0` (`n=7510`)
- `3. 大部分時候必須小心` -> `3.0` (`n=7583`)
- `4. 總是必須小心` -> `4.0` (`n=10498`)

#### G01-2 嚴格程度
- 包含題組：`v7b`
- `1. 一點都不嚴` -> `1.0` (`n=7373`)
- `2. 不太嚴` -> `2.0` (`n=13542`)
- `3. 還算嚴` -> `3.0` (`n=12918`)
- `4. 管得很嚴` -> `4.0` (`n=8192`)

#### G01-3 恰當程度
- 包含題組：`v7a`
- `1. 很不恰當` -> `1.0` (`n=4182`)
- `2. 不太恰當` -> `2.0` (`n=6232`)
- `3. 還算恰當` -> `3.0` (`n=17321`)
- `4. 很恰當` -> `4.0` (`n=14313`)

#### G01-4 發生頻率
- 包含題組：`v6, v22, v43`
- `1. 從未` -> `1.0` (`n=32072`)
- `2. 偶爾` -> `2.0` (`n=35962`)
- `3. 有時` -> `3.0` (`n=32654`)
- `4. 經常` -> `4.0` (`n=25360`)

#### G01-5 快樂程度
- 包含題組：`v51`
- `1. 很不快樂` -> `1.0` (`n=272`)
- `2. 不太快樂` -> `2.0` (`n=967`)
- `3. 還算快樂` -> `3.0` (`n=3622`)
- `4. 很快樂` -> `4.0` (`n=2142`)

#### G01-6 同意程度
- 包含題組：`v4, v9, v26, v27, v29, v44, v49, v52, v54`
- `1. 很不同意` -> `1.0` (`n=33520`)
- `2. 不太同意` -> `2.0` (`n=63082`)
- `3. 還算同意` -> `3.0` (`n=166662`)
- `4. 很同意` -> `4.0` (`n=87073`)

#### G01-7 符合程度
- 包含題組：`v5, v10, v11, v12, v19, v23, v24, v25, v28, v45`
- `1. 很不符合` -> `1.0` (`n=106542`)
- `2. 不太符合` -> `2.0` (`n=127976`)
- `3. 還算符合` -> `3.0` (`n=156042`)
- `4. 很符合` -> `4.0` (`n=78739`)

#### G01-8 缺值代碼
- 包含題組：`v10, v11, v12, v19, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v4, v43, v44, v45, v49, v5, v51, v52, v54, v6, v7a, v7b, v9`
- `-9` -> `<EMPTY>` (`n=2752`)

### G02
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v42, v48, v8`
- Covered column count: `35`
- Rule (prefix/sentinel mapping): `0->0, 1->1`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `3` pairs):
  - `0. 不是` -> `0.0` (`n=188423`)
  - `1. 是` -> `1.0` (`n=57045`)
  - `-9` -> `<EMPTY>` (`n=337`)

### G03
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v35, v37, v39, v41`
- Covered column count: `30`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4`; sentinel: `-9->EMPTY, -6->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `6` pairs):
  - `1. 從未` -> `1.0` (`n=15772`)
  - `2. 偶爾` -> `2.0` (`n=9196`)
  - `3. 有時` -> `3.0` (`n=3893`)
  - `4. 經常` -> `4.0` (`n=1678`)
  - `-6` -> `<EMPTY>` (`n=179810`)
  - `-9` -> `<EMPTY>` (`n=341`)

### G04
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v20, v47`
- Covered column count: `21`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `11` pairs):
  - `1. 從未` -> `1.0` (`n=33277`)
  - `1. 非常不同意` -> `1.0` (`n=4137`)
  - `2. 不同意` -> `2.0` (`n=3911`)
  - `2. 偶爾` -> `2.0` (`n=17951`)
  - `3. 普通` -> `3.0` (`n=19706`)
  - `3. 有時` -> `3.0` (`n=14649`)
  - `4. 同意` -> `4.0` (`n=20301`)
  - `4. 經常` -> `4.0` (`n=14633`)
  - `5. 不適用` -> `5.0` (`n=3693`)
  - `5. 非常同意` -> `5.0` (`n=14720`)
  - `-9` -> `<EMPTY>` (`n=505`)

### G05
- `change_class`: `ordinal_shift_plus1`
- Covered question groups: `v55`
- Covered column count: `14`
- Rule (prefix/sentinel mapping): `0->1, 1->2, 2->3, 3->4, 4->5`; sentinel: `-`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `5` pairs):
  - `0. 完全沒有或少於一天` -> `1.0` (`n=69089`)
  - `1. 最近1週一到兩天` -> `2.0` (`n=16347`)
  - `2. 最近1週三到四天` -> `3.0` (`n=6115`)
  - `3. 最近1週五到七天` -> `4.0` (`n=2850`)
  - `4. 最近兩週幾乎天天` -> `5.0` (`n=3921`)

### G06
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v20`
- Covered column count: `12`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5`; sentinel: `-9->EMPTY, -4->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `7` pairs):
  - `1. 從未` -> `1.0` (`n=30129`)
  - `2. 偶爾` -> `2.0` (`n=17868`)
  - `3. 有時` -> `3.0` (`n=15641`)
  - `4. 經常` -> `4.0` (`n=17530`)
  - `5. 不適用` -> `5.0` (`n=3025`)
  - `-4` -> `<EMPTY>` (`n=12`)
  - `-9` -> `<EMPTY>` (`n=71`)

### G07
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v17`
- Covered column count: `7`
- Rule (prefix/sentinel mapping): `0->0, 1->1`; sentinel: `-9->EMPTY, -6->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `4` pairs):
  - `0. 不是` -> `0.0` (`n=21927`)
  - `1. 是` -> `1.0` (`n=11526`)
  - `-6` -> `<EMPTY>` (`n=15666`)
  - `-9` -> `<EMPTY>` (`n=42`)

### G08
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v21`
- Covered column count: `6`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9, 10->10, 11->11, 12->12`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `13` pairs):
  - `1. 沒有` -> `1.0` (`n=7794`)
  - `2. 0.5小時以內` -> `2.0` (`n=9389`)
  - `3. 0.5-1小時以內` -> `3.0` (`n=7405`)
  - `4. 1-1.5小時以內` -> `4.0` (`n=5082`)
  - `5. 1.5-2小時以內` -> `5.0` (`n=4282`)
  - `6. 2-2.5小時以內` -> `6.0` (`n=1620`)
  - `7. 2.5-3小時以內` -> `7.0` (`n=1698`)
  - `8. 3-3.5小時以內` -> `8.0` (`n=1114`)
  - `9. 3.5-4小時以內` -> `9.0` (`n=719`)
  - `10. 4-4.5小時以內` -> `10.0` (`n=347`)
  - `11. 4.5-5小時以內` -> `11.0` (`n=481`)
  - `12. 5小時以上` -> `12.0` (`n=2074`)
  - `-9` -> `<EMPTY>` (`n=133`)

### G09
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v56`
- Covered column count: `6`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `8` pairs):
  - `1. 1完全不同意` -> `1.0` (`n=2836`)
  - `2. 2` -> `2.0` (`n=3036`)
  - `3. 3` -> `3.0` (`n=4919`)
  - `4. 4` -> `4.0` (`n=9278`)
  - `5. 5` -> `5.0` (`n=7471`)
  - `6. 6` -> `6.0` (`n=5137`)
  - `7. 7完全同意` -> `7.0` (`n=9365`)
  - `-9` -> `<EMPTY>` (`n=96`)

### G11
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v53`
- Covered column count: `5`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `4` pairs):
  - `1. 不符合` -> `1.0` (`n=1816`)
  - `2. 有些符合` -> `2.0` (`n=15349`)
  - `3. 符合` -> `3.0` (`n=17825`)
  - `-9` -> `<EMPTY>` (`n=125`)

### G12
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v57`
- Covered column count: `5`
- Rule (prefix/sentinel mapping): `0->0, 1->1, 2->2, 3->3, 4->4`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `6` pairs):
  - `0. 從來沒有` -> `0.0` (`n=1567`)
  - `1. 有時候` -> `1.0` (`n=8388`)
  - `2. 少於一半的時間` -> `2.0` (`n=4782`)
  - `3. 一半以上的時間` -> `3.0` (`n=9307`)
  - `4. 大部分的時間` -> `4.0` (`n=10941`)
  - `-9` -> `<EMPTY>` (`n=130`)

### G10
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v18`
- Covered column count: `4`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9, 10->10`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `11` pairs):
  - `1. 1完全不會期望` -> `1.0` (`n=2850`)
  - `2. 2` -> `2.0` (`n=1625`)
  - `3. 3` -> `3.0` (`n=1833`)
  - `4. 4` -> `4.0` (`n=2248`)
  - `5. 5` -> `5.0` (`n=5965`)
  - `6. 6` -> `6.0` (`n=2974`)
  - `7. 7` -> `7.0` (`n=2952`)
  - `8. 8` -> `8.0` (`n=2295`)
  - `9. 9` -> `9.0` (`n=1390`)
  - `10. 10十分期望` -> `10.0` (`n=3864`)
  - `-9` -> `<EMPTY>` (`n=96`)

### G13
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v17, v46`
- Covered column count: `4`
- Rule (prefix/sentinel mapping): `1->1, 2->2`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `5` pairs):
  - `1. 否` -> `1.0` (`n=11129`)
  - `1. 有` -> `1.0` (`n=4780`)
  - `2. 是` -> `2.0` (`n=9868`)
  - `2. 沒有` -> `2.0` (`n=2202`)
  - `-9` -> `<EMPTY>` (`n=113`)

### G15
- `change_class`: `deterministic_categorical_recode`
- Covered question groups: `v34, v36, v38, v40`
- Covered column count: `4`
- Rule (prefix/sentinel mapping): `1->1, 2->0`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `3` pairs):
  - `1. 曾經有` -> `1.0` (`n=3980`)
  - `2. 不曾` -> `0.0` (`n=24072`)
  - `-9` -> `<EMPTY>` (`n=40`)

### G17
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v60`
- Covered column count: `2`
- Rule (prefix/sentinel mapping): `0->0, 1->1, 2->2, 3->3, 4->4, 5->5, 6->6`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `13` pairs):
  - `0` -> `0.0` (`n=4041`)
  - `1. 沒有` -> `1.0` (`n=8369`)
  - `2. 1-2杯` -> `2.0` (`n=688`)
  - `2. 1-7瓶` -> `2.0` (`n=342`)
  - `3. 3-4杯` -> `3.0` (`n=165`)
  - `3. 8-14瓶` -> `3.0` (`n=85`)
  - `4. 15-21瓶` -> `4.0` (`n=26`)
  - `4. 5-6杯` -> `4.0` (`n=76`)
  - `5. 22-28瓶` -> `5.0` (`n=6`)
  - `5. 7-8杯` -> `5.0` (`n=31`)
  - `6. 29-35瓶` -> `6.0` (`n=44`)
  - `6. 9-10杯` -> `6.0` (`n=57`)
  - `-9` -> `<EMPTY>` (`n=116`)

### G20
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v1`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `1->1, 2->2`; sentinel: `-`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `2` pairs):
  - `1. 女` -> `1` (`n=3480`)
  - `2. 男` -> `2` (`n=3543`)

### G21
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v2`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `-5->-5, 1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9, 10->10, 11->11`; sentinel: `-99->EMPTY, -9->EMPTY, -7->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `15` pairs):
  - `1. 結婚，且同住一起` -> `1.0` (`n=5421`)
  - `2. 結婚，因工作分隔兩地` -> `2.0` (`n=198`)
  - `3. 結婚，但分居` -> `3.0` (`n=139`)
  - `4. 離婚，且分居` -> `4.0` (`n=830`)
  - `5. 離婚，但同住一起` -> `5.0` (`n=65`)
  - `6. 未婚，但同住一起` -> `6.0` (`n=39`)
  - `7. 未婚，且分居` -> `7.0` (`n=38`)
  - `8. 親生父親過世` -> `8.0` (`n=163`)
  - `9. 親生母親過世` -> `9.0` (`n=48`)
  - `10. 親生父母均過世` -> `10.0` (`n=8`)
  - `11. 其他` -> `11.0` (`n=32`)
  - `-5` -> `-5.0` (`n=1`)
  - `-7` -> `<EMPTY>` (`n=5`)
  - `-9` -> `<EMPTY>` (`n=32`)
  - `-99` -> `<EMPTY>` (`n=4`)

### G22
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v16`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6`; sentinel: `-9->EMPTY, -7->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `8` pairs):
  - `1. 至少班上前幾名` -> `1.0` (`n=1354`)
  - `2. 至少中上` -> `2.0` (`n=1831`)
  - `3. 要有班上的平均水準` -> `3.0` (`n=938`)
  - `4. 及格就好` -> `4.0` (`n=1241`)
  - `5. 沒有特別要求` -> `5.0` (`n=1373`)
  - `6. 其他` -> `6.0` (`n=245`)
  - `-7` -> `<EMPTY>` (`n=3`)
  - `-9` -> `<EMPTY>` (`n=38`)

### G23
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v50`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4`; sentinel: `-`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `4` pairs):
  - `1. 很不滿意` -> `1.0` (`n=267`)
  - `2. 不太滿意` -> `2.0` (`n=791`)
  - `3. 還算滿意` -> `3.0` (`n=3744`)
  - `4. 很滿意` -> `4.0` (`n=2221`)

### G28
- `change_class`: `label_to_numeric_plus_missing_standardization`
- Covered question groups: `v63`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9`; sentinel: `-9->EMPTY`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `10` pairs):
  - `1` -> `1.0` (`n=119`)
  - `2` -> `2.0` (`n=589`)
  - `3` -> `3.0` (`n=1428`)
  - `4` -> `4.0` (`n=2179`)
  - `5` -> `5.0` (`n=1459`)
  - `6` -> `6.0` (`n=831`)
  - `7` -> `7.0` (`n=263`)
  - `8` -> `8.0` (`n=42`)
  - `9` -> `9.0` (`n=50`)
  - `-9` -> `<EMPTY>` (`n=63`)

### G29
- `change_class`: `format_or_numeric_cast_only`
- Covered question groups: `v13`
- Covered column count: `1`
- Rule (prefix/sentinel mapping): `1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9, 10->10, 11->11, 12->12, 13->13, 14->14, 15->15, 16->16, 17->17, 18->18, 19->19, 20->20, 21->21, 22->22, 23->23, 24->24, 25->25, 26->26, 27->27, 28->28, 29->29, 30->30, 31->31, 32->32, 33->33, 34->34, 35->35, 36->36, 37->37, 38->38, 39->39, 40->40, 41->41, 42->42, 43->43, 44->44, 45->45, 46->46, 47->47, 48->48, 49->49, 50->50, 56->56`; sentinel: `-`
- Other explicit mapping rules: `-`
- Consistency check: raw label mapping ambiguity count = `0`
- Full observed mapping list (total `51` pairs):
  - `1` -> `1.0` (`n=237`)
  - `2` -> `2.0` (`n=250`)
  - `3` -> `3.0` (`n=253`)
  - `4` -> `4.0` (`n=253`)
  - `5` -> `5.0` (`n=251`)
  - `6` -> `6.0` (`n=255`)
  - `7` -> `7.0` (`n=257`)
  - `8` -> `8.0` (`n=253`)
  - `9` -> `9.0` (`n=257`)
  - `10` -> `10.0` (`n=241`)
  - `11` -> `11.0` (`n=252`)
  - `12` -> `12.0` (`n=237`)
  - `13` -> `13.0` (`n=231`)
  - `14` -> `14.0` (`n=221`)
  - `15` -> `15.0` (`n=221`)
  - `16` -> `16.0` (`n=201`)
  - `17` -> `17.0` (`n=213`)
  - `18` -> `18.0` (`n=194`)
  - `19` -> `19.0` (`n=191`)
  - `20` -> `20.0` (`n=188`)
  - `21` -> `21.0` (`n=218`)
  - `22` -> `22.0` (`n=203`)
  - `23` -> `23.0` (`n=207`)
  - `24` -> `24.0` (`n=199`)
  - `25` -> `25.0` (`n=183`)
  - `26` -> `26.0` (`n=188`)
  - `27` -> `27.0` (`n=172`)
  - `28` -> `28.0` (`n=147`)
  - `29` -> `29.0` (`n=127`)
  - `30` -> `30.0` (`n=103`)
  - `31` -> `31.0` (`n=80`)
  - `32` -> `32.0` (`n=70`)
  - `33` -> `33.0` (`n=84`)
  - `34` -> `34.0` (`n=67`)
  - `35` -> `35.0` (`n=51`)
  - `36` -> `36.0` (`n=46`)
  - `37` -> `37.0` (`n=40`)
  - `38` -> `38.0` (`n=31`)
  - `39` -> `39.0` (`n=28`)
  - `40` -> `40.0` (`n=28`)
  - `41` -> `41.0` (`n=24`)
  - `42` -> `42.0` (`n=16`)
  - `43` -> `43.0` (`n=12`)
  - `44` -> `44.0` (`n=13`)
  - `45` -> `45.0` (`n=7`)
  - `46` -> `46.0` (`n=7`)
  - `47` -> `47.0` (`n=5`)
  - `48` -> `48.0` (`n=6`)
  - `49` -> `49.0` (`n=3`)
  - `50` -> `50.0` (`n=1`)
  - `56` -> `56.0` (`n=1`)

## 2. v15 (Standalone)

- `change_class`: `label_to_numeric_plus_missing_standardization`
- Raw valid option count (excluding sentinel codes): `5`
- Cleaned valid option count: `5`
- `raw_negative_count`: `11`, `raw_sentinel_count`: `11`, `cleaned_empty_count`: `11`
- `raw_abnormal_count`: `0`

## 3. v3 (Standalone)

- `change_class`: `label_to_numeric_plus_missing_standardization`
- Raw valid option count (excluding sentinel codes): `10`
- Cleaned valid option count: `10`
- `raw_negative_count`: `10`, `raw_sentinel_count`: `10`, `cleaned_empty_count`: `10`
- `raw_abnormal_count`: `0`

## 4. v58 / v59 / v61 / v62 (Quality Handling Only)

This section only reports missing/negative/abnormal handling. No full option mapping is listed.

| column | raw_negative_count | raw_sentinel_count | cleaned_empty_count | raw_abnormal_count |
|---|---:|---:|---:|---:|
| v58_1h | 28 | 28 | 28 | 0 |
| v58_1m | 28 | 28 | 28 | 0 |
| v58_2h | 51 | 51 | 51 | 0 |
| v58_2m | 51 | 51 | 51 | 0 |
| v59_1h | 76 | 76 | 76 | 0 |
| v59_1m | 76 | 76 | 76 | 0 |
| v59_2h | 314 | 314 | 314 | 0 |
| v59_2m | 314 | 314 | 314 | 0 |
| v59_3h | 0 | 0 | 0 | 6958 |
| v59_3m | 65 | 65 | 65 | 0 |
| v59_4h | 0 | 0 | 0 | 6958 |
| v59_4m | 65 | 65 | 65 | 0 |
| v59_5 | 65 | 65 | 65 | 0 |
| v61 | 161 | 161 | 160 | 0 |
| v62 | 175 | 175 | 174 | 0 |

- Unified rule: sentinel/negative codes (e.g., `-4/-6/-7/-8/-9/-99`) are represented as empty after cleaning.
- Abnormal value definition: non-empty raw value that cannot be parsed to expected numeric format.

## 5. v14* (Quality Handling Only)

| column | raw_negative_count | raw_sentinel_count | cleaned_empty_count | raw_abnormal_count |
|---|---:|---:|---:|---:|
| v14_1_01 | 17 | 17 | 17 | 0 |
| v14_1_02 | 154 | 154 | 154 | 0 |
| v14_1_03 | 179 | 179 | 179 | 0 |
| v14_1_04 | 191 | 191 | 191 | 0 |
| v14_1_05 | 229 | 229 | 229 | 0 |
| v14_2_01 | 13 | 13 | 13 | 0 |
| v14_2_02 | 418 | 418 | 418 | 0 |
| v14_2_03 | 457 | 457 | 457 | 0 |
| v14_2_04 | 512 | 512 | 512 | 0 |
| v14_2_05 | 572 | 572 | 572 | 0 |
| v14_3_01 | 12 | 12 | 12 | 0 |
| v14_3_02 | 144 | 144 | 144 | 0 |
| v14_3_03 | 163 | 163 | 163 | 0 |
| v14_3_04 | 176 | 176 | 176 | 0 |
| v14_3_05 | 210 | 210 | 210 | 0 |
| v14_4_01 | 14 | 14 | 14 | 0 |
| v14_4_02 | 430 | 430 | 430 | 0 |
| v14_4_03 | 475 | 475 | 475 | 0 |
| v14_4_04 | 521 | 521 | 521 | 0 |
| v14_4_05 | 570 | 570 | 570 | 0 |

- v14* is summarized only for missing/negative/abnormal handling; full option mapping is intentionally omitted.

## 6. Identity and Background Fields (school/name/email/phone/student id, etc.)

For these fields, this report only describes empty/negative-like handling, not option-level recoding.

| column | raw_empty_count | cleaned_empty_count | raw_negative_like_count |
|---|---:|---:|---:|
| student_oid | 0 | 0 | 0 |
| student_id | 0 | 0 | 0 |
| qb_code | 0 | 0 | 0 |
| q_name | 0 | 0 | 0 |
| school_id | 0 | 0 | 0 |
| school_name | 0 | 0 | 0 |
| class | 0 | 0 | 0 |
| status | 0 | 0 | 0 |
| name | 0 | 0 | 0 |
| cell | 0 | 0 | 1 |
| cell_who | 0 | 8 | 8 |
| email | 5 | 0 | 0 |

- These are mostly text identification fields; negative numeric semantics are generally not applicable.
- Primary cleaning focus is null standardization and invalid record handling.

## 7. Summary

- Encoding/readability issue has been fixed by regenerating this report in a clean UTF-8-safe structure.
- `v15` and `v3` are standalone sections.
- `v58/v59/v61/v62` and `v14*` are quality-only sections (missing/negative/abnormal), as requested.
