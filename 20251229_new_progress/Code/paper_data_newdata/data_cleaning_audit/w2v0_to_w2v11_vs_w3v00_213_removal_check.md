# W2v0/W2v11 vs W3v00 ID Matching Check

## Key Result
- `|W2v0 IDs| = 8892`
- `|W2v11 IDs| = 7023`
- `|W3v00 TIGPS IDs| = 7713`
- `|W2v0 ? W3v00| = 7236`
- `|W2v0 ? W3v00 - W2v11| = 213` (this 213 list)

Interpretation: matching W3 IDs explains most removals, but not all. There are 213 IDs that exist in W3v00 but were still removed before W2v11.

## 213-ID List File
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\data_cleaning_audit\w2v0_in_w3v00_but_removed_from_w2v11_213_ids.csv`

## 213 Group Profile (from W2v0)
- Mean sentinel count across all `v*` columns: `59.17`
- Median sentinel count across all `v*` columns: `39`
- Has sentinel in `v13*`: `0.423`
- Has sentinel in `v55*`: `0.286`
- Has sentinel in `v61*`: `0.329`
- Has sentinel in `v62*`: `0.319`
- Has sentinel in `v59*`: `0.315`
- Has sentinel in `v60*`: `0.221`
- Has sentinel in `v56*`: `0.207`

## Top Columns With Higher Sentinel Rate In 213 Group
| column | removed_213_rate | kept_7023_rate | diff |
|---|---:|---:|---:|
| v13 | 0.423 | 0.000 | 0.423 |
| v61 | 0.329 | 0.023 | 0.306 |
| v62 | 0.319 | 0.025 | 0.294 |
| v55_4 | 0.286 | 0.000 | 0.286 |
| v55_1 | 0.282 | 0.000 | 0.282 |
| v55_2 | 0.282 | 0.000 | 0.282 |
| v55_3 | 0.282 | 0.000 | 0.282 |
| v55_5 | 0.282 | 0.000 | 0.282 |
| v55_6 | 0.282 | 0.000 | 0.282 |
| v55_7 | 0.282 | 0.000 | 0.282 |
| v55_8 | 0.282 | 0.000 | 0.282 |
| v55_9 | 0.282 | 0.000 | 0.282 |
| v55_10 | 0.282 | 0.000 | 0.282 |
| v55_11 | 0.282 | 0.000 | 0.282 |
| v55_12 | 0.282 | 0.000 | 0.282 |
| v55_13 | 0.282 | 0.000 | 0.282 |
| v55_14 | 0.282 | 0.000 | 0.282 |
| v59_2h | 0.310 | 0.045 | 0.265 |
| v59_2m | 0.310 | 0.045 | 0.265 |
| v60_1 | 0.221 | 0.008 | 0.212 |
