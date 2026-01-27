import pandas as pd
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GATConv, Linear
import numpy as np
import os
from sklearn.metrics import r2_score

# --- Loading Logic (Reused) ---
DATA_DIR = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data"
REL_DIR = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
W2_PATH = os.path.join(DATA_DIR, "TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv")
EDGE_PATH = os.path.join(REL_DIR, "Offline_Like.csv")

def load_data():
    print("Loading Data...")
    try:
        df = pd.read_csv(W2_PATH, on_bad_lines='skip', engine='python')
    except: return None
    
    mh = [f"v55_{i}" for i in range(1,15)]
    df['score'] = df[mh].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    df = df.dropna(subset=['score', 'student_id'])
    
    feats = ['v51','v59_5','v52_3','v57_4','v52_2','v57_3','v50','v57_2','v52','v57_1',
             'v52_1','v57_5','v24_2','v8_08','v28_6','v39_2','v5_5','v8_05','v24_6','v35_2']
    
    for c in feats: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    
    uids = sorted(df['student_id'].unique())
    id_map = {sid: i for i, sid in enumerate(uids)}
    
    df.set_index('student_id', inplace=True)
    df = df.reindex(uids)
    
    x = torch.tensor(df[feats].values, dtype=torch.float)
    y = torch.tensor(df['score'].values, dtype=torch.float).view(-1, 1)
    
    # Graph
    edges = pd.read_csv(EDGE_PATH)
    lookup = {}
    
    df['sc'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int)
    df['cc'] = df['class'].astype(str).str.replace('.0','').str.strip()
    df['st'] = pd.to_numeric(df['v13'], errors='coerce').fillna(-1).astype(int)
    
    df = df.reset_index()
    for _, r in df.iterrows():
        if r['sc'] != -1: lookup[(r['sc'], r['cc'], r['st'])] = r['student_id']
            
    src, tgt = [], []
    for _, r in edges.iterrows():
        if r['student_id'] in id_map:
            try:
                tk = (int(r['school_id']), str(r['class']).replace('.0','').strip(), int(r['nominated_seat_no']))
                if tk in lookup and lookup[tk] in id_map:
                    src.append(id_map[r['student_id']])
                    tgt.append(id_map[lookup[tk]])
            except: pass
            
    edge_index = torch.tensor([src, tgt], dtype=torch.long)
    
    # Split
    np.random.seed(42)
    idx = np.random.permutation(len(uids))
    tr = int(0.8*len(uids))
    va = int(0.1*len(uids))
    
    data = Data(x=x, edge_index=edge_index, y=y)
    data.tr = torch.zeros(len(uids), dtype=torch.bool)
    data.va = torch.zeros(len(uids), dtype=torch.bool)
    data.te = torch.zeros(len(uids), dtype=torch.bool)
    
    data.tr[idx[:tr]] = True
    data.va[idx[tr:tr+va]] = True
    data.te[idx[tr+va:]] = True
    
    return data

# --- Model ---
class GATResNet(torch.nn.Module):
    def __init__(self, num_features, hidden_channels, heads=4):
        super().__init__()
        self.gat1 = GATConv(num_features, hidden_channels, heads=heads, dropout=0.5)
        self.lin1 = Linear(num_features, hidden_channels * heads)
        self.gat2 = GATConv(hidden_channels * heads, 1, heads=1, concat=False, dropout=0.5)
        self.lin2 = Linear(hidden_channels * heads, 1)

    def forward(self, x, edge_index):
        h = F.elu(self.gat1(x, edge_index) + self.lin1(x))
        h = F.dropout(h, p=0.5, training=self.training)
        out = self.gat2(h, edge_index) + self.lin2(h)
        return out

def run():
    data = load_data()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # Force CPU for safety if needed, check env
    # Try CPU primarily for small tasks to avoid CUDA init errors if env not ready
    device = torch.device('cpu') 
    
    print("Training with 8 Heads...")
    model = GATResNet(data.num_features, 32, heads=8).to(device)
    data = data.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=5e-4)
    
    for ep in range(300):
        model.train()
        opt.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.mse_loss(out[data.tr], data.y[data.tr])
        loss.backward()
        opt.step()
        
    model.eval()
    pred = model(data.x, data.edge_index)[data.te].detach().numpy()
    true = data.y[data.te].detach().numpy()
    r2 = r2_score(true, pred)
    print(f"Final Test R2 (8 Heads): {r2:.4f}")

if __name__ == "__main__":
    run()
