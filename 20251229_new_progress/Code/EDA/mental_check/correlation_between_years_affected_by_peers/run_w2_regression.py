import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import zscore
import os

def run_w2_only():
    DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2024data/TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    REL_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Code/EDA/relationship/Offline_Like.csv"

    print("Loading W2...")
    try:
        df = pd.read_csv(DATA_PATH, on_bad_lines='skip', engine='python')
        edges = pd.read_csv(REL_PATH)
    except Exception as e:
        print(e)
        return

    # 1. Own Score
    mh = [f"v55_{i}" for i in range(1, 15)]
    df['score'] = df[mh].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    df = df.dropna(subset=['score', 'student_id'])
    
    # 2. Peer Map
    loc_map = {}
    id_scores = df.set_index('student_id')['score'].to_dict()
    
    for _, r in df.iterrows():
        try:
            k = (int(r['school_id']), str(r['class']).replace('.0','').strip(), int(r['v13']))
            loc_map[k] = r['student_id']
        except: pass
        
    peers = {}
    for _, r in edges.iterrows():
        sid = r['student_id']
        try:
            tk = (int(r['school_id']), str(r['class']).replace('.0','').strip(), int(r['nominated_seat_no']))
            if tk in loc_map:
                tid = loc_map[tk]
                if tid in id_scores:
                    if sid not in peers: peers[sid] = []
                    peers[sid].append(id_scores[tid])
        except: pass
        
    p_df = pd.DataFrame([{'student_id': k, 'peer_avg': np.mean(v)} for k, v in peers.items()])
    
    # 3. Merge
    final = pd.merge(df[['student_id', 'score']], p_df, on='student_id')
    print(f"Sample: {len(final)}")
    
    # 4. Std
    final['Z_Self'] = zscore(final['score'])
    final['Z_Peer'] = zscore(final['peer_avg'])
    
    # 5. OLS
    X = sm.add_constant(final['Z_Peer'])
    y = final['Z_Self']
    
    model = sm.OLS(y, X).fit()
    print(model.summary())
    print("\n--- RESULT ---")
    print(f"Beta (Influence): {model.params['Z_Peer']:.4f}")
    print(f"P-Value: {model.pvalues['Z_Peer']:.4e}")

if __name__ == "__main__":
    run_w2_only()
