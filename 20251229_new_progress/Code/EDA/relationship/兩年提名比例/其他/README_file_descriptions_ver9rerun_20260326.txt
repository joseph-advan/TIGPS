Output directory: C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship\兩年提名比例\ver9_rerun_20260326
Source W2: C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver9.csv
Source W3: C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver9.csv

Important note:
W3_studentdata_ver9.csv does not contain explicit school_id/class columns.
This rerun maps W3 school_id/class from W2 by student_id (full 7045/7045 matched).

File descriptions:
00_W2_nominated_not_in_list_ver9rerun_20260326.csv
- W2 nominations that cannot be uniquely mapped by school_id+class+seat.
- reason: not_in_list or ambiguous_duplicate_seat.

00_W3_nominated_not_in_list_ver9rerun_20260326.csv
- W3 nominations that cannot be uniquely mapped by school_id+class+seat.
- reason: not_in_list or ambiguous_duplicate_seat.

01_W2_student_8features_ver9rerun_20260326.csv
- Per-student W2 network 8 features (out/in x online/offline x friend/enemy),
- counted only from uniquely matched nominations.

01_W3_student_8features_ver9rerun_20260326.csv
- Per-student W3 network 8 features (out/in x online/offline x friend/enemy),
- counted only from uniquely matched nominations.

02_W2W3_student_feature_deltas_ver9rerun_20260326.csv
- Student-level paired table of W2, W3, and delta (W3-W2) for 8 features.

02_W2W3_8features_detailed_compare_ver9rerun_20260326.csv
- Feature-level descriptive comparison (mean/std/quantiles/increase-decrease/correlation).

02_W2W3_8features_delta_distribution_ver9rerun_20260326.csv
- Distribution of integer deltas (W3-W2) for each feature.

02_W2W3_8features_wave_bucket_distribution_ver9rerun_20260326.csv
- Bucketed distribution by wave (0,1,2,3,4,5,6-10,11+) for each feature.

02_W2W3_aggregate_change_summary_ver9rerun_20260326.csv
- Aggregate metrics over 6 totals: friend, enemy, online, offline, out, in.

02_W2W3_school_mean_deltas_ver9rerun_20260326.csv
- School-level mean deltas for each feature plus friend_total/enemy_total deltas.

03_W2W3_8features_paired_tests_ver9rerun_20260326.csv
- Paired tests per feature: Wilcoxon, paired t-test, effect size dz, FDR-BH.

04_W2W3_ambiguous_duplicate_seat_backtrace_ver9rerun_20260326.csv
- Backtrace list for ambiguous_duplicate_seat: each ambiguous nomination with candidate student_ids.

05_W2W3_duplicate_seat_student_map_from_ambiguous_ver9rerun_20260326.csv
- Unique duplicate-seat keys that were referenced by ambiguous nominations, with candidate student_ids and reference counts.

05_W2W3_duplicate_seat_student_map_all_roster_ver9rerun_20260326.csv
- All duplicate seat keys in rosters (W2/W3), whether referenced or not.

05_W2W3_duplicate_seat_student_map_not_referenced_by_ambiguous_ver9rerun_20260326.csv
- Duplicate seat keys existing in roster but not referenced by ambiguous nomination records.
