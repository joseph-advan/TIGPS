import pandas as pd
import numpy as np
from scipy import stats
import os

def simple_peer_analysis():
    # Paths
    w2_peer_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship_reallike\w2_peer_mental_health_stats.csv"
    w3_data_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"
    
    # 1. Load Peer Data (W2)
    print(f"Loading Peer Stats: {w2_peer_path}")
    try:
        peer_df = pd.read_csv(w2_peer_path)
    except Exception as e:
        print(f"Error loading peer stats: {e}")
        return

    # 2. Load W3 Data (Outcome)
    print(f"Loading W3 Data: {w3_data_path}")
    try:
        w3_df = pd.read_csv(w3_data_path, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error loading W3 data: {e}")
        return

    # 3. Calculate W3 Mental Health Score
    # Columns "54-1" to "54-14" (based on previous scripts)
    mh_cols = [f"54-{i}" for i in range(1, 15)]
    w3_df['w3_mh_score'] = w3_df[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    
    # Filter valid W3 scores
    w3_df = w3_df.dropna(subset=['w3_mh_score', 'student_id'])
    
    # 4. Merge
    merged_df = pd.merge(peer_df, w3_df[['student_id', 'w3_mh_score']], on='student_id', how='inner')
    print(f"Merged Data Points: {len(merged_df)}")
    
    # 5. Simple Group Comparison
    # Split students into "Friends have Low Depression" vs "Friends have High Depression"
    # Using Median Split on 'w2_peer_avg_mh_score'
    median_peer_score = merged_df['w2_peer_avg_mh_score'].median()
    
    group_low = merged_df[merged_df['w2_peer_avg_mh_score'] <= median_peer_score]['w3_mh_score']
    group_high = merged_df[merged_df['w2_peer_avg_mh_score'] > median_peer_score]['w3_mh_score']
    
    output_str = ""
    output_str += f"\n--- Median Split Statistics (Median Peer Score: {median_peer_score:.2f}) ---\n"
    output_str += f"Group 1 (Low Peer Dep): {group_low.mean():.2f}\n"
    output_str += f"Group 2 (High Peer Dep): {group_high.mean():.2f}\n"
    
    # 6. T-Test
    t_stat, p_val = stats.ttest_ind(group_high, group_low, equal_var=False)
    
    output_str += f"\n--- T-Test Results ---\n"
    output_str += f"T-statistic: {t_stat:.4f}\n"
    output_str += f"P-value: {p_val:.4e}\n"
    
    if p_val < 0.05:
        output_str += "\n>> SIGNIFICANT DIFFERENCE FOUND!\n"
        output_str += "Students with more depressed friends have significantly higher depression scores themselves in the next year.\n"
    else:
        output_str += "\n>> NO SIGNIFICANT DIFFERENCE.\n"
    
    # 7. Correlation
    corr = merged_df['w2_peer_avg_mh_score'].corr(merged_df['w3_mh_score'])
    output_str += f"\n--- Simple Correlation (Pearson) ---\n"
    output_str += f"Correlation between Friend's W2 Score and Own W3 Score: {corr:.4f}\n"

    print(output_str)
    with open(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship_reallike\simple_stat_results.txt", "w", encoding="utf-8") as f:
        f.write(output_str)

if __name__ == "__main__":
    simple_peer_analysis()
