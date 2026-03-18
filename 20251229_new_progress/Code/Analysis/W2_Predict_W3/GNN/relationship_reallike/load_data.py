import pandas as pd
import torch
from torch_geometric.data import Data
import numpy as np
import os

def load_gnn_data():
    # --- Configuration ---
    # Adjust paths as necessary relative to this script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Assuming this script is in Code/Analysis/GNN/relationship_reallike
    # Data is in Data/2024data
    DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../../Data/2024data"))
    RELATIONSHIP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../EDA/relationship"))
    
    W2_STUDENT_PATH = os.path.join(DATA_DIR, "TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv")
    OFFLINE_LIKE_PATH = os.path.join(RELATIONSHIP_DIR, "Offline_Like.csv")
    
    # Top 20 Features from correlation analysis
    NODE_FEATURES = [
        'v51', 'v59_5', 'v52_3', 'v57_4', 'v52_2', 
        'v57_3', 'v50', 'v57_2', 'v52', 'v57_1', 
        'v52_1', 'v57_5', 'v24_2', 'v8_08', 'v28_6', 
        'v39_2', 'v5_5', 'v8_05', 'v24_6', 'v35_2'
    ]
    
    print(f"Loading Student Data from: {W2_STUDENT_PATH}")
    try:
        student_df = pd.read_csv(W2_STUDENT_PATH, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error loading student data: {e}")
        return None

    # --- 1. Prepare Target and Features ---
    # Calculate Mental Health Score (Target)
    mh_cols = [f"v55_{i}" for i in range(1, 15)]
    student_df['mh_score'] = student_df[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    
    # Filter valid students (must have target and student_id)
    student_df = student_df.dropna(subset=['mh_score', 'student_id']).copy()
    
    # Ensure features are numeric and fill missing with 0 (or median)
    for col in NODE_FEATURES:
        student_df[col] = pd.to_numeric(student_df[col], errors='coerce').fillna(0)
    
    # Create Node Feature Matrix (X) and Label (y)
    # We need a stable ordering of nodes. Let's start by observing all student_ids.
    # Map student_id -> node_index
    unique_student_ids = sorted(student_df['student_id'].unique())
    id_map = {sid: i for i, sid in enumerate(unique_student_ids)}
    
    num_nodes = len(unique_student_ids)
    print(f"Total Nodes (Students): {num_nodes}")
    
    # x: [num_nodes, num_features]
    # y: [num_nodes, 1]
    # We need to reindex student_df to match id_map order
    student_df.set_index('student_id', inplace=True)
    student_df = student_df.reindex(unique_student_ids)
    
    x = torch.tensor(student_df[NODE_FEATURES].values, dtype=torch.float)
    y = torch.tensor(student_df['mh_score'].values, dtype=torch.float).view(-1, 1)
    
    # --- 2. Build Mapping for Edges (Nominees) ---
    # We need to map (School, Class, Seat) -> student_id (then -> node_index)
    # W2 Seat provided as 'v13'
    
    print("Building ID Mapping dictionary...")
    # Key: (school_id, class, v13), Value: student_id
    mapping_dict = {}
    
    # Check for v13 uniqueness
    # Group by School, Class, v13 and check count
    # Note: 'class' in CSV might be float or string 801.0
    
    def clean_class(val):
        s = str(val).strip()
        if s.endswith('.0'): return s[:-2]
        return s

    student_df['class_clean'] = student_df['class'].apply(clean_class)
    student_df['school_clean'] = pd.to_numeric(student_df['school_id'], errors='coerce').fillna(-1).astype(int)
    student_df['seat_clean'] = pd.to_numeric(student_df['v13'], errors='coerce').fillna(-1).astype(int)
    
    # Iterate to build map
    duplicates_count = 0
    valid_map_count = 0
    
    # Reset index to access student_id column again
    student_df_reset = student_df.reset_index()
    
    for idx, row in student_df_reset.iterrows():
        sid = row['student_id']
        school = row['school_clean']
        cls = row['class_clean']
        seat = row['seat_clean']
        
        if school == -1 or cls == "nan" or seat == -1:
            continue
            
        key = (school, cls, seat)
        if key in mapping_dict:
            # Collision found!
            # print(f"Warning: Duplicate seat detected for {key}. Existing: {mapping_dict[key]}, New: {sid}")
            duplicates_count += 1
        else:
            mapping_dict[key] = sid
            valid_map_count += 1
            
    print(f"Mapping entries created: {valid_map_count}")
    if duplicates_count > 0:
        print(f"WARNING: {duplicates_count} duplicate seat assignments detected in W2 data. These targets might be ambiguous.")

    # --- 3. Process Edges ---
    print(f"Loading Edges from: {OFFLINE_LIKE_PATH}")
    try:
        edges_df = pd.read_csv(OFFLINE_LIKE_PATH)
    except Exception as e:
        print(f"Error loading edges: {e}")
        return None
        
    source_indices = []
    target_indices = []
    
    matched_edges = 0
    failed_edges = 0
    
    for _, row in edges_df.iterrows():
        # Source
        src_sid = row['student_id']
        if src_sid not in id_map:
            continue # Source student not in our mental health dataset
            
        src_idx = id_map[src_sid]
        
        # Target
        # Target is identified by school_id, class, nominated_seat_no
        tgt_school = int(pd.to_numeric(row['school_id'], errors='coerce') or -1)
        tgt_class = clean_class(row['class'])
        tgt_seat = int(pd.to_numeric(row['nominated_seat_no'], errors='coerce') or -1)
        
        key = (tgt_school, tgt_class, tgt_seat)
        
        if key in mapping_dict:
            tgt_sid = mapping_dict[key]
            if tgt_sid in id_map:
                tgt_idx = id_map[tgt_sid]
                
                source_indices.append(src_idx)
                target_indices.append(tgt_idx)
                matched_edges += 1
            else:
                # Target exists in mapping but filtered out from MH data (e.g. missing score)
                failed_edges += 1
        else:
            # Try Fallback: Parse Student ID? 
            # Risk: We don't know the student ID of the target, that's what we are looking for.
            # So we can't parse it. The map is essential.
            failed_edges += 1

    print(f"Graph Construction:")
    print(f"  Matched Edges: {matched_edges}")
    print(f"  Unmatched/Filtered Edges: {failed_edges}")
    
    edge_index = torch.tensor([source_indices, target_indices], dtype=torch.long)
    
    # --- 4. Create Masks ---
    # 80/10/10 Split
    indices = np.random.permutation(num_nodes)
    train_size = int(0.8 * num_nodes)
    val_size = int(0.1 * num_nodes)
    
    train_idx = indices[:train_size]
    val_idx = indices[train_size:train_size + val_size]
    test_idx = indices[train_size + val_size:]
    
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[train_idx] =True
    
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask[val_idx] = True
    
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask[test_idx] = True
    
    # Create Data Object
    data = Data(x=x, edge_index=edge_index, y=y)
    data.train_mask = train_mask
    data.val_mask = val_mask
    data.test_mask = test_mask
    
    print("Data Object Created.")
    return data

if __name__ == "__main__":
    data = load_gnn_data()
    if data:
        print(data)
