import load_data
import torch
from torch_geometric.utils import homophily
import numpy as np

def check_homophily():
    print("Loading Data...")
    data = load_data.load_gnn_data()
    
    if data is None:
        return

    # Edge Homophily for regression (continuous variable) can be measured by 
    # correlation between source and target node values.
    
    edge_index = data.edge_index
    y = data.y.squeeze()
    
    src = edge_index[0]
    tgt = edge_index[1]
    
    src_y = y[src].numpy()
    tgt_y = y[tgt].numpy()
    
    # Calculate Pearson Correlation between friends' mental health
    correlation = np.corrcoef(src_y, tgt_y)[0, 1]
    
    print(f"\n--- Graph Homophily Analysis ---")
    print(f"Number of Edges: {edge_index.shape[1]}")
    print(f"Mental Health Score Correlation between Connected Nodes (Friends): {correlation:.4f}")
    
    # Interpretation
    if abs(correlation) < 0.1:
        print(">> LOW HOMOPHILY: Friends' mental health scores are barely correlated.")
        print(">> IMPACT: Standard GCN might perform POORLY because it smooths/mixes features across edges, diluting simple strong features.")
        print(">> SUGGESTION: Use GAT (Graph Attention Network) or add Residual Connections to preserve node's own features.")
    else:
        print(">> MODERATE/HIGH HOMOPHILY: Graph structure should help.")

if __name__ == "__main__":
    check_homophily()
