輸出目錄：C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship\兩年提名比例\ver9_rerun_20260326
W2資料來源：C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver9.csv
W3資料來源：C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver9.csv

重要說明：
W3_studentdata_ver9.csv 沒有明確的 school_id / class 欄位，
此次重跑以 student_id 對應 W2 來補齊 school_id / class（7045/7045 全部對上）。

檔案說明：
00_W2_nominated_not_in_list_ver9rerun_20260326.csv
- W2 中無法唯一配對到受提名者的提名紀錄。
- reason 包含：not_in_list、ambiguous_duplicate_seat。

00_W3_nominated_not_in_list_ver9rerun_20260326.csv
- W3 中無法唯一配對到受提名者的提名紀錄。
- reason 包含：not_in_list、ambiguous_duplicate_seat。

01_W2_student_8features_ver9rerun_20260326.csv
- 每位學生在 W2 的 8 個網絡特徵（out/in × online/offline × friend/enemy）。
- 只計入可唯一配對成功的提名。

01_W3_student_8features_ver9rerun_20260326.csv
- 每位學生在 W3 的 8 個網絡特徵（out/in × online/offline × friend/enemy）。
- 只計入可唯一配對成功的提名。

02_W2W3_student_feature_deltas_ver9rerun_20260326.csv
- 學生層級的 W2/W3 對照與 delta（W3 - W2）。

02_W2W3_8features_detailed_compare_ver9rerun_20260326.csv
- 8 特徵的詳細比較統計（平均、標準差、分位數、增減比例、相關）。

02_W2W3_8features_delta_distribution_ver9rerun_20260326.csv
- 8 特徵各自的 delta 分布（整數變化值的次數與比例）。

02_W2W3_8features_wave_bucket_distribution_ver9rerun_20260326.csv
- W2 與 W3 在分桶（0/1/2/3/4/5/6-10/11+）的分布。

02_W2W3_aggregate_change_summary_ver9rerun_20260326.csv
- 六個總量指標（friend/enemy/online/offline/out/in）的整體變化摘要。

02_W2W3_school_mean_deltas_ver9rerun_20260326.csv
- 以 school_id 匯總的平均變化（各特徵與 friend_total/enemy_total）。

03_W2W3_8features_paired_tests_ver9rerun_20260326.csv
- 8 特徵的成對檢定（Wilcoxon、paired t-test、effect size dz、FDR-BH）。

04_W2W3_ambiguous_duplicate_seat_backtrace_ver9rerun_20260326.csv
- ambiguous_duplicate_seat 的回推明細（每筆對應候選 student_id）。

05_W2W3_duplicate_seat_student_map_from_ambiguous_ver9rerun_20260326.csv
- 有被 ambiguous 提名打到的重複座號鍵值清單（含候選 student_id 與被引用次數）。

05_W2W3_duplicate_seat_student_map_all_roster_ver9rerun_20260326.csv
- 名單中所有重複座號鍵值（不管是否被 ambiguous 提名）。

05_W2W3_duplicate_seat_student_map_not_referenced_by_ambiguous_ver9rerun_20260326.csv
- 名單中有重複座號，但這次沒有被 ambiguous 提名打到的鍵值。
