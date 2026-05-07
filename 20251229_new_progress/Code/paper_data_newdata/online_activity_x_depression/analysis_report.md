# Online Activity x Depression Study Summary

## Data and core definitions
- W2 file: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv`
- W3 file: `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv`
- Nomination count rule: count filled nomination slots (seat number > 0).
- Incoming nomination rule: count how many times a student's seat is nominated within same class.
- Main nomination grouping (3 types, z>0): outgoing / incoming / total nominations.
- Activity grouping: high if online activity sum > wave median.

## Diagnostics
- W2 students: 6603, class valid rate: 100.00%
- W3 students: 6603, class mapped rate: 100.00%
- W2 activity median: 15.0000
- W3 activity median: 19.0000

## Output files
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\wave_features_w2.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\wave_features_w3.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\stage1_main_effects.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\stage2_cross_year.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\stage3_within_highrisk_protective_effects.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\stage3_interaction_models.csv`
- `C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data_newdata\online_activity_x_depression\reverse_items_config.json`
