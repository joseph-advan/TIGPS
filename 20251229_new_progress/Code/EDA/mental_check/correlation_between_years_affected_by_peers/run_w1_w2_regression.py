import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import zscore
import os

def run_regression():
    W1_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2024data/TIGPS_W1_studentdata_ver5_cleaned_mental_common_only.csv"
    W2_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2024data/TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    REL_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Code/EDA/relationship/Offline_Like.csv"

    print("Loading...")
    try:
        w1 = pd.read_csv(W1_PATH, on_bad_lines='skip', engine='python')
        w2 = pd.read_csv(W2_PATH, on_bad_lines='skip', engine='python')
        edges = pd.read_csv(REL_PATH)
    except Exception as e:
        print(e)
        return

    # Scores
    mh_cols = [f"v55_{i}" for i in range(1, 15)]
    w1['w1_score'] = w1[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    w2['w2_score'] = w2[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)

    w1_v = w1.dropna(subset=['w1_score', 'student_id'])[['student_id', 'w1_score']]
    w2_v = w2.dropna(subset=['w2_score', 'student_id'])[['student_id', 'w2_score', 'school_id', 'class', 'v13']]

    # Peer
    id_map = w2_v.set_index('student_id')['w2_score'].to_dict()
    loc_map = {}
    for _, r in w2_v.iterrows():
        if pd.isna(r['school_id']): continue
        try:
            loc_key = (int(r['school_id']), str(r['class']).replace('.0','').strip(), int(r['v13']))
            loc_map[loc_key] = r['student_id']
        except: pass

    peer_map = {}
    for _, r in edges.iterrows():
        sid = r['student_id']
        try:
            tgt = (int(r['school_id']), str(r['class']).replace('.0','').strip(), int(r['nominated_seat_no']))
            if tgt in loc_map and loc_map[tgt] in id_map:
                if sid not in peer_map: peer_map[sid] = []
                peer_map[sid].append(id_map[loc_map[tgt]])
        except: pass

    p_data = [{'student_id': k, 'w2_peer': np.mean(v)} for k, v in peer_map.items()]
    p_df = pd.DataFrame(p_data)

    # Merge
    m = pd.merge(w2_v, p_df, on='student_id')
    final = pd.merge(m, w1_v, on='student_id')
    print(f"Sample: {len(final)}")

    # Std
    final['Z_Self_W2'] = zscore(final['w2_score'])
    final['Z_Self_W1'] = zscore(final['w1_score'])
    final['Z_Peer_W2'] = zscore(final['w2_peer'])

    # OLS
    X = final[['Z_Self_W1', 'Z_Peer_W2']]
    X = sm.add_constant(X)
    y = final['Z_Self_W2']
    
    model = sm.OLS(y, X).fit()
    print(model.summary())
    
    print("\n--- BETAS ---")
    print(f"History (W1): {model.params['Z_Self_W1']:.4f}")
    print(f"Peer (W2)   : {model.params['Z_Peer_W2']:.4f}")

if __name__ == "__main__":
    run_regression()
