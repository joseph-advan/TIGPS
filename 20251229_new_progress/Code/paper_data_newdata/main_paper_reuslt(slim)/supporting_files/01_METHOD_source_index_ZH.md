# Methodology and Data Audit Source Index

## Purpose

This folder summarizes final methodology records for the main paper, including data cleaning and feature decomposition.

## Data Cleaning Documents

| File | Purpose |
|---|---|
| `01_data_cleaning_methods_detailed_ZH.md` | Detailed step-by-step data-cleaning documentation. |
| `02_data_cleaning_source_index_ZH.md` | Index of source records in `Data/testing_clean`. |
| `03_feature_decomposition_methods_ZH.md` | Paper-facing feature construction and decomposition methodology. |
| `04_feature_inventory_ZH.md` | Paper-facing feature inventory with question IDs, Chinese names, English names, and usage notes. |

## Primary Final Data Files

| Wave | Final file |
|---|---|
| W2 | `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv` |
| W3 | `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv` |

## Primary Cleaning Evidence

| Source file | Role |
|---|---|
| `Data/testing_clean/W2_W3_complete_data_cleaning_steps_through_W2ver6_W3ver5.md` | Complete human-readable cleaning record. |
| `Data/testing_clean/w2_ver6_w3_ver5_cleaning_summary.json` | Machine-readable final cleaning summary. |
| `Data/testing_clean/W2/w2_ver6_nomination_cleaning_summary.md` | W2 peer nomination cleaning record. |
| `Data/testing_clean/W3/w3_ver5_nomination_cleaning_summary.md` | W3 peer nomination cleaning record. |
| `Data/testing_clean/W3/w3_ver5_gender_recode_to_w2_convention.md` | W3 gender harmonization record. |

## Feature Decomposition Evidence

| Source file | Role |
|---|---|
| `Code/paper_data_newdata/Feature_Decomposition/W2_W3_subscale_definitions_record.md` | Full source record of W2/W3 subscale definitions. |
| `Code/paper_data_newdata/Feature_Decomposition/subscale_definitions_w2_w3.json` | Machine-readable source config used by modeling scripts. |
| `Code/paper_data_newdata/Feature_Decomposition/outputs/model_performance/binary_drop_then_split_summary.md` | Drop-only vs drop + decomposition performance summary. |
| `Code/paper_data_newdata/Feature_Decomposition/outputs/reliability/subscale_cronbach_alpha_reliability_summary.md` | W2 subscale reliability summary. |
| `Code/paper_data_newdata/Feature_Decomposition/outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md` | V54 SEL reliability deep-dive summary. |
| `main_paper_results/00_methodology_and_data_audit/feature_decomposition_supporting_files/` | Minimal copied supporting files for manuscript reference. |

## Feature Inventory Evidence

| Source file | Role |
|---|---|
| `main_paper_results/00_methodology_and_data_audit/04_feature_inventory_ZH.md` | Main feature inventory summary. |
| `main_paper_results/00_methodology_and_data_audit/feature_inventory_supporting_files/main_paper_feature_inventory.xlsx` | Full feature inventory workbook. |
| `main_paper_results/00_methodology_and_data_audit/feature_inventory_supporting_files/main_paper_feature_inventory.csv` | CSV version of the full feature inventory. |
