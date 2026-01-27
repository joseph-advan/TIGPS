import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import load_data # This imports our data loading script (load_data.py)
import numpy as np
import sys
import os

# Suppress prints from load_data
sys.stdout = open(os.devnull, 'w')
data = load_data.load_gnn_data()
sys.stdout = sys.__stdout__

class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, 1) 

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x

def train_and_evaluate():
    if data is None:
        print("Failed to load data.")
        return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = GCN(num_features=data.num_features, hidden_channels=16).to(device)
    curr_data = data.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    # Train silently
    model.train()
    for epoch in range(200):
        optimizer.zero_grad()
        out = model(curr_data.x, curr_data.edge_index)
        loss = F.mse_loss(out[curr_data.train_mask], curr_data.y[curr_data.train_mask])
        loss.backward()
        optimizer.step()

    # Evaluation
    model.eval()
    with torch.no_grad():
        out = model(curr_data.x, curr_data.edge_index)
        test_mse = F.mse_loss(out[curr_data.test_mask], curr_data.y[curr_data.test_mask])
        test_mae = F.l1_loss(out[curr_data.test_mask], curr_data.y[curr_data.test_mask])
        
        # Baseline
        train_mean = curr_data.y[curr_data.train_mask].mean()
        baseline_preds = torch.full_like(curr_data.y[curr_data.test_mask], train_mean)
        baseline_mse = F.mse_loss(baseline_preds, curr_data.y[curr_data.test_mask])
        baseline_mae = F.l1_loss(baseline_preds, curr_data.y[curr_data.test_mask])
        
        from sklearn.metrics import r2_score
        y_true = curr_data.y[curr_data.test_mask].cpu().numpy()
        y_pred = out[curr_data.test_mask].cpu().numpy()
        test_r2 = r2_score(y_true, y_pred)

        print(f"GNN Test MSE: {test_mse:.4f}")
        print(f"GNN Test MAE: {test_mae:.4f}")
        print(f"GNN Test R2: {test_r2:.4f}")
        print(f"Baseline MSE: {baseline_mse:.4f}")
        print(f"Baseline MAE: {baseline_mae:.4f}")
        
        improvement = (baseline_mse - test_mse) / baseline_mse * 100
        print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    train_and_evaluate()
