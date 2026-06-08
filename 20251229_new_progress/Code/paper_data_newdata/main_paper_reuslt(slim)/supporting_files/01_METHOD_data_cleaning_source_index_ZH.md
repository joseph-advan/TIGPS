# Data Cleaning Source Index

## Purpose

This file identifies the source records used to document the data-cleaning methodology. It is intended to reduce confusion caused by multiple intermediate versions in `Data/testing_clean`.

Feature decomposition is not covered here.

## Final Cleaned Analysis Datasets

These are the final cleaned student-level datasets used in the current main-paper analyses.

| Wave | File | Use |
|---|---|---|
| W2 / 2024 | `Data/testing_clean/W2/TIGPS_W2_studentdata_ver6.csv` | Final W2 cleaned and aligned student data |
| W3 / 2025 | `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver5.csv` | Final W3 cleaned and aligned student data |

## Final Cross-Wave Alignment Records

| File | What it records |
|---|---|
| `Data/testing_clean/w2_ver6_w3_ver5_common_student_ids.csv` | Final 6603 common student IDs retained in both waves |
| `Data/testing_clean/w2_ver6_w3_ver5_cleaning_summary.json` | Machine-readable summary of final W2/W3 alignment and peer nomination cleaning |
| `Data/testing_clean/W2_W3_complete_data_cleaning_steps_through_W2ver6_W3ver5.md` | Main human-readable complete cleaning documentation from raw data to W2 ver6 / W3 ver5 |

## W2 Cleaning Evidence

| File | What it records | Use in methodology |
|---|---|---|
| `Data/testing_clean/W2/w2_ver3_removed_step1_conflict.csv` | W2 removed rows from selected-question anomaly/conflict step | Audit evidence only |
| `Data/testing_clean/W2/w2_ver3_removed_step2_v13_anomaly.csv` | W2 removed rows for seat-number anomaly step | Audit evidence only |
| `Data/testing_clean/W2/w2_ver3_cleaning_summary.txt` | W2 cleaning summary through early row-removal steps | Source for W2 cleaning history |
| `Data/testing_clean/W2/w2_ver4_class_mapping_summary.txt` | W2 class mapping summary | Source for class standardization |
| `Data/testing_clean/W2/w2_ver4_class_mapping_table.csv` | W2 class mapping table | Audit evidence for class conversion |
| `Data/testing_clean/W2/w2_ver5_mapping_cleaning_summary.txt` | W2 questionnaire response encoding summary | Source for response encoding |
| `Data/testing_clean/W2/w2_ver6_nomination_cleaning_summary.md` | W2 final peer nomination cleaning summary | Main W2 nomination source |
| `Data/testing_clean/W2/w2_ver6_nomination_cleaning_event_log.csv` | Cell-level W2 nomination cleaning event log | Detailed audit evidence |
| `Data/testing_clean/W2/w2_ver6_peer_nomination_edges.csv` | Final W2 peer nomination edge list | Input for interpersonal network features |
| `Data/testing_clean/W2/w2_ver6_nomination_cleaning_group_summary.csv` | W2 nomination group-level summary | Audit evidence |
| `Data/testing_clean/W2/w2_ver6_nomination_cleaning_column_summary.csv` | W2 nomination column-level summary | Audit evidence |
| `Data/testing_clean/W2/w2_ver6_aligned_roster_duplicate_seats.csv` | W2 duplicate seat roster check | Final validation evidence |

## W3 Cleaning Evidence

| File | What it records | Use in methodology |
|---|---|---|
| `Data/testing_clean/W3/ver3_header_rename_summary.txt` | W3 column renaming from Chinese headers to question codes | Source for W3 renaming step |
| `Data/testing_clean/W3/ver4_change_log.md` | W3 response encoding and row-removal change log | Source for W3 ver4 cleaning |
| `Data/testing_clean/W3/ver4_encoding_codebook.csv` | W3 encoding codebook | Audit evidence for W3 coding |
| `Data/testing_clean/W3/ver4_removed_gt60_rows.csv` | W3 rows removed due to nomination values greater than 60 | Source for impossible nomination-value removal |
| `Data/testing_clean/W3/w3_ver5_gender_recode_to_w2_convention.md` | W3 final gender recoding to match W2 convention | Main gender harmonization source |
| `Data/testing_clean/W3/w3_ver5_gender_recode_to_w2_convention_counts.xlsx` | Counts before/after W3 gender recoding | Audit evidence |
| `Data/testing_clean/W3/w3_ver5_nomination_cleaning_summary.md` | W3 final peer nomination cleaning summary | Main W3 nomination source |
| `Data/testing_clean/W3/w3_ver5_nomination_cleaning_event_log.csv` | Cell-level W3 nomination cleaning event log | Detailed audit evidence |
| `Data/testing_clean/W3/w3_ver5_peer_nomination_edges.csv` | Final W3 peer nomination edge list | Input for interpersonal network features |
| `Data/testing_clean/W3/w3_ver5_nomination_cleaning_group_summary.csv` | W3 nomination group-level summary | Audit evidence |
| `Data/testing_clean/W3/w3_ver5_nomination_cleaning_column_summary.csv` | W3 nomination column-level summary | Audit evidence |
| `Data/testing_clean/W3/w3_ver5_aligned_roster_duplicate_seats.csv` | W3 duplicate seat roster check | Final validation evidence |

## Intermediate Version Files

The following files are useful for audit history but should not be treated as current final analysis inputs:

| Folder / pattern | Status |
|---|---|
| `Data/testing_clean/W2/TIGPS_W2_studentdata_ver0.csv` to `ver5.csv` | Intermediate W2 versions before the final `ver6` file |
| `Data/testing_clean/W3/TIGPS_W3_student_studentdata_ver00.csv` to `ver4.csv` | Intermediate W3 versions before the final `ver5` file |
| `Data/testing_clean/final_aligned_w2ver5_w3ver4/` | Older aligned output based on W2 ver5 / W3 ver4 before final nomination cleaning and gender harmonization |
| `Data/testing_clean/final_aligned_w2ver5_w3ver4_revised_nomination_qc/` | Older revised nomination QC output; useful for audit history, but current main analyses use W2 ver6 / W3 ver5 |

## Recommended Citation Within Project Notes

When describing the final data-cleaning workflow, cite these three records first:

1. `Data/testing_clean/W2_W3_complete_data_cleaning_steps_through_W2ver6_W3ver5.md`
2. `Data/testing_clean/w2_ver6_w3_ver5_cleaning_summary.json`
3. `Code/paper_data_newdata/main_paper_results/00_methodology_and_data_audit/01_data_cleaning_methods_detailed_ZH.md`
