import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import load_data # This imports our data loading script (load_data.py)
import numpy as np

# A simple 2-layer GCN Model for regression
class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, 1) # Output 1 value (mental health score)

    def forward(self, x, edge_index):
        # First Graph Convolution Layer
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)
        
        # Second Graph Convolution Layer
        x = self.conv2(x, edge_index)
        return x

def train_and_evaluate():
    print("Initializing GNN Training...")
    
    # 1. Load Data
    # load_data.py should be in the same directory. 
    # It returns a PyG Data object.
    data = load_data.load_gnn_data()
    
    if data is None:
        print("Failed to load data.")
        return

    # Check if GPU is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    model = GCN(num_features=data.num_features, hidden_channels=16).to(device)
    data = data.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    print("\n--- Model Architecture ---")
    print(model)
    
    print("\n--- Starting Training ---")
    model.train()
    for epoch in range(200):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        
        # Calculate Loss using the Training Mask
        loss = F.mse_loss(out[data.train_mask], data.y[data.train_mask])
        
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            val_loss = F.mse_loss(out[data.val_mask], data.y[data.val_mask])
            print(f'Epoch: {epoch+1:03d}, Train MSE: {loss:.4f}, Val MSE: {val_loss:.4f}')

    print("\n--- Evaluation on Test Set ---")
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        test_mse = F.mse_loss(out[data.test_mask], data.y[data.test_mask])
        test_mae = F.l1_loss(out[data.test_mask], data.y[data.test_mask])
        
        print(f'Test MSE: {test_mse:.4f}')
        print(f'Test MAE: {test_mae:.4f}')
        
        # Compare with Mean Baseline (predicting the mean of training set for everyone)
        train_mean = data.y[data.train_mask].mean()
        baseline_preds = torch.full_like(data.y[data.test_mask], train_mean)
        baseline_mse = F.mse_loss(baseline_preds, data.y[data.test_mask])
        baseline_mae = F.l1_loss(baseline_preds, data.y[data.test_mask])
        
        print(f'\n--- Baseline Comparison (Mean Predictor) ---')
        print(f'Baseline MSE: {baseline_mse:.4f}')
        print(f'Baseline MAE: {baseline_mae:.4f}')
        
        improvement = (baseline_mse - test_mse) / baseline_mse * 100
        print(f'\nModel Improvement over Baseline (MSE): {improvement:.2f}%')

if __name__ == "__main__":
    train_and_evaluate()
