# Feature_Decomposition Folder Structure

Last updated: 2026-05-20

這份文件整理 `Feature_Decomposition` 資料夾目前的實體架構與每個檔案的用途。

## Current Physical Structure

目前已改成「核心檔案保留在根目錄，說明文件與輸出結果放進子資料夾」。

```text
Feature_Decomposition/
├─ README.md
├─ .editorconfig
├─ build_binary_drop_then_split_baseline.py
├─ run_subscale_cronbach_alpha_reliability.py
├─ run_v54_sel_deep_dive.py
├─ subscale_definitions_w2_w3.json
├─ subscale_definitions_w2_w3_table.csv
├─ W2_W3_subscale_definitions_record.md
├─ docs/
│  ├─ FEATURE_DECOMPOSITION_STRUCTURE_ZH.md
│  └─ v54_revision_rerun_change_summary.md
└─ outputs/
   ├─ model_performance/
   │  ├─ binary_drop_then_split_summary.md
   │  ├─ binary_drop_then_split_summary.csv
   │  └─ binary_drop_then_split_details.json
   ├─ reliability/
   │  ├─ subscale_cronbach_alpha_reliability.xlsx
   │  ├─ subscale_cronbach_alpha_reliability_summary.md
   │  └─ subscale_cronbach_alpha_reliability_details.json
   └─ v54_deep_dive/
      ├─ v54_sel_deep_dive_reliability.xlsx
      └─ v54_sel_deep_dive_reliability_summary.md
```

## Why Core Files Stay In The Root

根目錄仍保留三類核心檔案：

- 可被其他程式 import 的 Python scripts。
- 後續分析會直接讀取的 JSON/CSV config。
- 最重要的人類可讀拆題組紀錄。

這樣做是為了避免破壞既有分析腳本。以下資料夾仍會引用根目錄裡的 `build_binary_drop_then_split_baseline.py` 或 `subscale_definitions_w2_w3.json`：

- `GNN_baseline`
- `Ridge_lasso`
- `tables/scripts`
- `main_paper_results`

## 1. Root-Level Core Files

| File | Role |
|---|---|
| `README.md` | 資料夾總覽與建議閱讀順序。 |
| `.editorconfig` | 編輯器與 encoding 設定。 |
| `build_binary_drop_then_split_baseline.py` | 核心 decomposition 腳本；比較 drop-only 與 drop + decomposition。 |
| `run_subscale_cronbach_alpha_reliability.py` | W2 小題組 Cronbach's alpha 檢查。 |
| `run_v54_sel_deep_dive.py` | v54 SEL 題組 deep dive。 |
| `subscale_definitions_w2_w3.json` | 機器讀取的拆題組設定檔。 |
| `subscale_definitions_w2_w3_table.csv` | 拆題組設定的表格版，方便人工檢查。 |
| `W2_W3_subscale_definitions_record.md` | 正式拆題組紀錄，包含中英文小題組名稱與題目列表。 |

最重要的正式紀錄是：

`W2_W3_subscale_definitions_record.md`

## 2. docs/

`docs/` 放補充說明與決策紀錄。

| File | Role |
|---|---|
| `docs/FEATURE_DECOMPOSITION_STRUCTURE_ZH.md` | 目前這份文件，說明資料夾架構。 |
| `docs/v54_revision_rerun_change_summary.md` | 記錄 v54 修改、Cronbach's alpha 結果，以及 01-06 重跑後的主要變化。 |

## 3. outputs/model_performance/

這裡放「拆題組是否改善模型表現」的結果。

| File | Role |
|---|---|
| `outputs/model_performance/binary_drop_then_split_summary.md` | 人類可讀的 performance summary。 |
| `outputs/model_performance/binary_drop_then_split_summary.csv` | 表格版 performance summary。 |
| `outputs/model_performance/binary_drop_then_split_details.json` | 詳細模型結果與 config snapshot。 |

目前重點結果：

| Task | Drop-only CV5 AUC | Drop + decomposition CV5 AUC | Difference |
|---|---:|---:|---:|
| W2 -> W2 | 0.790897 | 0.810315 | +0.019418 |
| W2 -> W3 | 0.698156 | 0.707296 | +0.009140 |

## 4. outputs/reliability/

這裡放所有 W2 小題組的 Cronbach's alpha 檢查。

| File | Role |
|---|---|
| `outputs/reliability/subscale_cronbach_alpha_reliability.xlsx` | 完整 workbook，包含 subscale alpha、parent scale alpha、item diagnostics、review flags。 |
| `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md` | 人類可讀 reliability summary。 |
| `outputs/reliability/subscale_cronbach_alpha_reliability_details.json` | 詳細 reliability 結果。 |

## 5. outputs/v54_deep_dive/

這裡只放 v54 SEL 題組的 deep dive。

| File | Role |
|---|---|
| `outputs/v54_deep_dive/v54_sel_deep_dive_reliability.xlsx` | v54 專門 reliability workbook。 |
| `outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md` | v54 專門 summary。 |

目前 v54 最新拆法：

| Subscale | Items | Cronbach's alpha | Interpretation |
|---|---|---:|---|
| Self-Awareness | `v54_1, v54_2, v54_3` | 0.857 | Good |
| Self-Management | `v54_4, v54_5, v54_6` | 0.896 | Good |
| Motivation & Goal Setting | `v54_7, v54_8, v54_9` | 0.904 | Good |
| Social Awareness & Relationship Skills | `v54_10, v54_11, v54_13, v54_14, v54_15` | 0.834 | Good |
| Help-Seeking | `v54_12, v54_16` | 0.661 | Questionable but usable |
| Responsible Decision-Making | `v54_17, v54_18, v54_19, v54_20` | 0.827 | Good |

## Recommended Reading Order

如果要快速理解目前拆題組方法，建議依序看：

1. `README.md`
2. `W2_W3_subscale_definitions_record.md`
3. `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md`
4. `outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md`
5. `outputs/model_performance/binary_drop_then_split_summary.md`
6. `docs/v54_revision_rerun_change_summary.md`

## What To Use In The Paper

方法論可以引用：

- `W2_W3_subscale_definitions_record.md`
- `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md`
- `outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md`

結果段落可以引用：

- `outputs/model_performance/binary_drop_then_split_summary.md`
- `docs/v54_revision_rerun_change_summary.md`

補充材料可以使用：

- `subscale_definitions_w2_w3_table.csv`
- `outputs/reliability/subscale_cronbach_alpha_reliability.xlsx`
- `outputs/v54_deep_dive/v54_sel_deep_dive_reliability.xlsx`
