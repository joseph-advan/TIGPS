import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GATConv, Linear
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import torch.nn.functional as F
import numpy as np
import os

def run_gnn_w2_w3():
    # --- Paths ---
    W2_DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2024data/TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    W3_DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2025data/TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"
    RELATIONSHIP_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Code/EDA/relationship/Offline_Like.csv"

    print("1. Loading Data...")
    try:
        w2_df = pd.read_csv(W2_DATA_PATH, on_bad_lines='skip', engine='python')
        w3_df = pd.read_csv(W3_DATA_PATH, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error: {e}")
        return

    # --- Features (W2) ---
    NODE_FEATURES = [
        'v51', 'v59_5', 'v52_3', 'v57_4', 'v52_2', 
        'v57_3', 'v50', 'v57_2', 'v52', 'v57_1', 
        'v52_1', 'v57_5', 'v24_2', 'v8_08', 'v28_6', 
        'v39_2', 'v5_5', 'v8_05', 'v24_6', 'v35_2'
    ]
    MH_ITEMS_W2 = [f"v55_{i}" for i in range(1, 15)]
    w2_df['w2_mh_score'] = w2_df[MH_ITEMS_W2].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    
    feature_cols = NODE_FEATURES + ['w2_mh_score']
    for col in feature_cols:
        w2_df[col] = pd.to_numeric(w2_df[col], errors='coerce').fillna(w2_df[col].median())
    
    scaler = StandardScaler()
    w2_df[feature_cols] = scaler.fit_transform(w2_df[feature_cols])
    x_full = w2_df[['student_id'] + feature_cols].copy()

    # --- Target (W3) ---
    MH_ITEMS_W3 = [f"54-{i}" for i in range(1, 15)]
    w3_df['target_w3'] = w3_df[MH_ITEMS_W3].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    y_full = w3_df[['student_id', 'target_w3']].dropna()

    # --- Merge ---
    merged = pd.merge(x_full, y_full, on='student_id', how='inner')
    unique_ids = sorted(merged['student_id'].unique())
    id_map = {sid: i for i, sid in enumerate(unique_ids)}
    num_nodes = len(unique_ids)
    print(f"Intersection Data Points (W2+W3): {num_nodes}")

    final_df = merged.set_index('student_id').reindex(unique_ids)
    x = torch.tensor(final_df[feature_cols].values, dtype=torch.float)
    y = torch.tensor(final_df['target_w3'].values, dtype=torch.float).view(-1, 1)

    # --- Graph ---
    print("2. Building Graph...")
    edges_df = pd.read_csv(RELATIONSHIP_PATH)
    lookup = {}
    def clean_cls(v): return str(v).replace('.0', '').strip()
    w2_df['s_clean'] = pd.to_numeric(w2_df['school_id'], errors='coerce').fillna(-1).astype(int)
    w2_df['c_clean'] = w2_df['class'].apply(clean_cls)
    w2_df['seat_clean'] = pd.to_numeric(w2_df['v13'], errors='coerce').fillna(-1).astype(int)
    for idx, row in w2_df.iterrows():
        if row['s_clean'] == -1: continue
        lookup[(row['s_clean'], row['c_clean'], row['seat_clean'])] = row['student_id']

    src, tgt = [], []
    for _, row in edges_df.iterrows():
        if row['student_id'] not in id_map: continue
        ts = int(pd.to_numeric(row['school_id'], errors='coerce') or -1)
        tc = clean_cls(row['class'])
        tn = int(pd.to_numeric(row['nominated_seat_no'], errors='coerce') or -1)
        key = (ts, tc, tn)
        if key in lookup:
            tgt_sid = lookup[key]
            if tgt_sid in id_map:
                src.append(id_map[row['student_id']])
                tgt.append(id_map[tgt_sid])
    
    edge_index = torch.tensor([src, tgt], dtype=torch.long)
    print(f"Edges: {len(src)}")

    # --- Model ---
    class GATResNet(torch.nn.Module):
        def __init__(self, num_features, hidden=32, heads=4):
            super().__init__()
            self.gat1 = GATConv(num_features, hidden, heads=heads, dropout=0.5)
            self.lin1 = Linear(num_features, hidden * heads)
            self.gat2 = GATConv(hidden * heads, 1, heads=1, concat=False, dropout=0.5)
            self.lin2 = Linear(hidden * heads, 1)
        def forward(self, x, edge_index):
            h = F.elu(self.gat1(x, edge_index) + self.lin1(x))
            out = self.gat2(h, edge_index) + self.lin2(h)
            return out

    device = torch.device('cpu')
    model = GATResNet(x.shape[1]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

    # Split
    np.random.seed(42)
    indices = np.random.permutation(num_nodes)
    train_idx = indices[:int(0.8*num_nodes)]
    test_idx = indices[int(0.8*num_nodes):]

    print("3. Training...")
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        out = model(x, edge_index)
        loss = F.mse_loss(out[train_idx], y[train_idx])
        loss.backward()
        optimizer.step()
    
    model.eval()
    pred = model(x, edge_index)[test_idx].detach().numpy()
    true = y[test_idx].detach().numpy()
    r2 = r2_score(true, pred)
    print(f"Final Test R2 (W2->W3): {r2:.4f}")

if __name__ == "__main__":
    run_gnn_w2_w3()
