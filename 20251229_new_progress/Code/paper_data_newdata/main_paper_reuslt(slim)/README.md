# GNN 青少年心理困擾預測 — 論文結果 (slim)

使用圖神經網絡與機器學習預測青少年心理困擾風險：社交網絡、個人能力與數位生活的角色。

本資料夾為論文寫作用的 slim 版本，只保留主線分析結果、圖檔與最終定稿。

## 閱讀順序

請先讀指南檔：

1. `00_GUIDE_paper_analysis_flow_for_advisor_ZH.md` — 論文分析流程
2. `00_GUIDE_slim_index_and_file_usage_ZH.md` — 檔案索引與使用說明

## 檔案命名規則

| 前綴 | 內容 |
|:--|:--|
| `00_GUIDE_` | 閱讀順序、論文流程、檔案使用說明 |
| `01_METHOD_` | 資料清理、feature decomposition、feature inventory、Cronbach alpha |
| `02_MODEL_` | 模型表現比較 |
| `03_TABLE1_` | Table 1 descriptive group differences |
| `04_INTERPERSONAL_` | interpersonal incremental modeling |
| `05_LASSO_` | LASSO Top 20 與 relative importance |
| `06_CATEGORY_` | category-level interpretation |
| `07_INTERACTION_` | Online Activity interaction analysis |

## 資料夾

- `figures/` — 主文圖檔與說明
- `supporting_files/` — 附錄、CSV、source index、詳細 workbook
- `20260524補充資料/` — 補充分析資料

## 主要文件

- 論文定稿：`使用圖神經網絡與機器學習預測青少年心理困擾風險_社交網絡、個人能力與數位生活的角色_蔡加恩_2026.5.28.v3final.docx`
- 論文 Markdown：`paper.md`
- 論文大綱：`PAPER_OUTLINE_ZH.md`

## 注意

`_archive/` 為本機保留資料（舊版草稿、重複圖檔、簡報檔），已由 `.gitignore` 排除，不會推上 GitHub。
