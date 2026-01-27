import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import zscore
import os

def run_std_regression():
    # Paths
    W2_PEER_STATS_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Code/EDA/relationship_reallike/w2_peer_mental_health_stats.csv"
    W3_DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2025data/TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"

    print("Loading data...")
    peer_df = pd.read_csv(W2_PEER_STATS_PATH)
    w3_df = pd.read_csv(W3_DATA_PATH, on_bad_lines='skip', engine='python')

    # Calc W3 Score
    cols = [f"54-{i}" for i in range(1, 15)]
    w3_df['w3_mh_score'] = w3_df[cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    w3_df = w3_df.dropna(subset=['w3_mh_score', 'student_id'])

    # Merge
    merged = pd.merge(peer_df, w3_df[['student_id', 'w3_mh_score']], on='student_id', how='inner')
    
    # Select cols
    data_reg = merged[['w2_own_mh_score', 'w2_peer_avg_mh_score', 'w3_mh_score']].dropna()
    print(f"Data points: {len(data_reg)}")

    # Standardize
    data_std = data_reg.copy()
    for col in data_std.columns:
        data_std[col] = zscore(data_std[col])

    X = data_std[['w2_own_mh_score', 'w2_peer_avg_mh_score']]
    X = sm.add_constant(X)
    y = data_std['w3_mh_score']

    # Run Model
    model = sm.OLS(y, X).fit()
    print(model.summary())

    # Report
    b_own = model.params['w2_own_mh_score']
    b_peer = model.params['w2_peer_avg_mh_score']
    
    print(f"\n--- Standardized Beta Results ---")
    print(f"Beta Own: {b_own:.4f}")
    print(f"Beta Peer: {b_peer:.4f}")
    if b_peer != 0:
        print(f"Ratio: {b_own/b_peer:.1f}x")

if __name__ == "__main__":
    run_std_regression()
