import os
import sys
from typing import Dict, List

import numpy as np
import pandas as pd

# Optional deps
try:
    import torch
    import torch.nn.functional as F
    from torch_geometric.data import Data
    from torch_geometric.nn import GATConv
except Exception as exc:  # pragma: no cover
    print("[Error] Missing torch/torch_geometric. Please install them first.")
    print(exc)
    sys.exit(1)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


BASE_DIR = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress"

W2_PATH = os.path.join(
    BASE_DIR,
    r"Data\2024data\TIGPS_W2_studentdata_ver6_cleaned_mental_common_only(standerdized).csv",
)
W3_PATH = os.path.join(
    BASE_DIR,
    r"Data\2025data\TIGPS_W3_studentdata_ver6_cleaned_cols_removed_missing_common_only(cleaned_q_21)(standerdized).csv",
)

QUESTION_LIST_PATH = os.path.join(
    BASE_DIR, r"Code\EDA\tying_to_catigoricalize_q\merged_question_list_w2_w3.csv"
)

CROSSYEAR_PRIMARY = os.path.join(
    BASE_DIR,
    r"Code\EDA\mental_check\Correlation_with_mental_qs_and_other_qs\02_crossyear_spearman_W2_to_W3_MH.csv",
)
CROSSYEAR_FALLBACK = os.path.join(
    BASE_DIR,
    r"Code\EDA\mental_check\Correlation_with_mental_qs_and_other_qs\02_sorted_by_rho_crossyear_W2_to_W3_MH.csv",
)

REL_PATH = os.path.join(BASE_DIR, r"Code\EDA\relationship\Offline_Like.csv")

OUT_DIR = os.path.join(
    BASE_DIR,
    r"Code\Analysis\GNN\Mental分組測試\GAT\Relationshiup_Offline_Like\題組",
)

OUT_METRICS = os.path.join(OUT_DIR, "metrics_gat.csv")
OUT_PRED = os.path.join(OUT_DIR, "predictions.csv")
OUT_NODE_MAP = os.path.join(OUT_DIR, "node_index_map.csv")
OUT_FEATURES = os.path.join(OUT_DIR, "features_used.csv")
OUT_DATA_SUMMARY = os.path.join(OUT_DIR, "data_summary.txt")

W3_MH_COLS = [f"54-{i}" for i in range(1, 15)]


def normalize_group_id(val) -> str:
    if pd.isna(val):
        return ""
    s = str(val).strip()
    if not s or s.lower() in {"nan", "none"}:
        return ""
    if s.lower().startswith("v"):
        return s
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except Exception:
        pass
    if s.endswith(".0"):
        return s[:-2]
    return s


def load_question_list() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_LIST_PATH)
    required = {"Year", "Group_ID", "Question_ID"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in question list: {missing}")
    df["Year"] = df["Year"].astype(str)
    df["Group_ID"] = df["Group_ID"].apply(normalize_group_id)
    df["Question_ID"] = df["Question_ID"].astype(str)
    return df


def load_crossyear() -> pd.DataFrame:
    if os.path.exists(CROSSYEAR_PRIMARY):
        path = CROSSYEAR_PRIMARY
    elif os.path.exists(CROSSYEAR_FALLBACK):
        path = CROSSYEAR_FALLBACK
    else:
        raise FileNotFoundError(CROSSYEAR_PRIMARY)
    df = pd.read_csv(path)
    df["Group_ID"] = df["Group_ID"].apply(normalize_group_id)
    return df


def build_group_items(question_list: pd.DataFrame, group_ids: List[str]) -> Dict[str, List[str]]:
    q = question_list[question_list["Year"] == "W2"].copy()
    q = q[q["Group_ID"].isin(group_ids)]
    return q.groupby("Group_ID")["Question_ID"].apply(list).to_dict()


def compute_group_scores(df: pd.DataFrame, group_items: Dict[str, List[str]]) -> pd.DataFrame:
    scores = {}
    for gid, items in group_items.items():
        cols = [c for c in items if c in df.columns]
        if not cols:
            continue
        scores[f"group_{gid}"] = df[cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    return pd.DataFrame(scores)


def build_node_table(w2: pd.DataFrame, w3: pd.DataFrame) -> pd.DataFrame:
    # Target Y: W3 MH mean
    w3_mh = w3[W3_MH_COLS].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    w3_id_col = "student_id" if "student_id" in w3.columns else "TIGPS_ID"
    w3_target = pd.DataFrame(
        {"merge_id": w3[w3_id_col].astype(str).str.strip(), "y_w3_mh": w3_mh}
    )

    # Scheme A
    cross = load_crossyear()
    filtered = cross[(cross["q_value"] < 0.05) & (cross["valid_row_pct"] >= 0.5)].copy()

    group_ids = filtered["Group_ID"].dropna().astype(str).tolist()
    qlist = load_question_list()
    group_items = build_group_items(qlist, group_ids)
    group_scores = compute_group_scores(w2, group_items)

    w2_ids = w2["student_id"].astype(str).str.strip()
    X = group_scores.copy()
    X["merge_id"] = w2_ids
    data = pd.merge(X, w3_target, on="merge_id", how="inner")
    data = data.dropna(subset=["y_w3_mh"])
    return data


def build_edge_index(w2: pd.DataFrame, node_ids: List[str]) -> np.ndarray:
    def clean_class(val):
        s = str(val).strip()
        if s.endswith(".0"):
            return s[:-2]
        return s

    df_map = w2.copy()
    df_map["school_id"] = pd.to_numeric(df_map["school_id"], errors="coerce").fillna(-1).astype(int)
    df_map["v13"] = pd.to_numeric(df_map["v13"], errors="coerce").fillna(-1).astype(int)
    df_map["class_str"] = df_map["class"].apply(clean_class)
    df_map["student_id_str"] = df_map["student_id"].astype(str).str.strip()

    valid = df_map[
        (df_map["school_id"] != -1)
        & (df_map["v13"] != -1)
        & (df_map["class_str"] != "MISSING")
    ]

    seat_to_id = {
        (row["school_id"], row["class_str"], row["v13"]): row["student_id_str"]
        for _, row in valid.iterrows()
    }

    node_index = {sid: i for i, sid in enumerate(node_ids)}

    rel = pd.read_csv(REL_PATH)
    rel["school_id"] = pd.to_numeric(rel["school_id"], errors="coerce").fillna(-1).astype(int)
    rel["nominated_seat_no"] = pd.to_numeric(rel["nominated_seat_no"], errors="coerce").fillna(-1).astype(int)
    rel["class_str"] = rel["class"].apply(clean_class)
    rel["student_id"] = rel["student_id"].astype(str).str.strip()

    edges = []
    for _, row in rel.iterrows():
        src = row["student_id"]
        key = (row["school_id"], row["class_str"], row["nominated_seat_no"])
        tgt = seat_to_id.get(key)
        if src in node_index and tgt in node_index:
            i = node_index[src]
            j = node_index[tgt]
            edges.append((i, j))
            edges.append((j, i))  # undirected

    if not edges:
        raise ValueError("No edges found after mapping. Check seat mapping.")

    return np.array(edges, dtype=np.int64).T


class GAT(torch.nn.Module):
    def __init__(self, in_dim: int, hidden: int = 64, heads: int = 4, dropout: float = 0.3):
        super().__init__()
        self.gat1 = GATConv(in_dim, hidden, heads=heads, dropout=dropout)
        self.gat2 = GATConv(hidden * heads, 1, heads=1, concat=False, dropout=dropout)
        self.dropout = dropout

    def forward(self, x, edge_index):
        x = self.gat1(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.gat2(x, edge_index)
        return x.view(-1)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    w2 = pd.read_csv(W2_PATH, low_memory=False)
    w3 = pd.read_csv(W3_PATH, low_memory=False)

    data = build_node_table(w2, w3)
    feature_cols = [c for c in data.columns if c not in {"merge_id", "y_w3_mh"}]

    pd.DataFrame({"feature": feature_cols}).to_csv(
        OUT_FEATURES, index=False, encoding="utf-8-sig"
    )

    node_ids = data["merge_id"].tolist()
    node_map = pd.DataFrame({"node_index": range(len(node_ids)), "student_id": node_ids})
    node_map.to_csv(OUT_NODE_MAP, index=False, encoding="utf-8-sig")

    edge_index = build_edge_index(w2, node_ids)

    X = data[feature_cols].apply(pd.to_numeric, errors="coerce").values
    y = data["y_w3_mh"].astype(float).values

    idx_all = np.arange(len(y))
    idx_train, idx_test = train_test_split(idx_all, test_size=0.2, random_state=42)
    idx_train, idx_val = train_test_split(idx_train, test_size=0.125, random_state=42)  # 70/10/20

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    X_train = imputer.fit_transform(X[idx_train])
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(imputer.transform(X[idx_val]))
    X_test = scaler.transform(imputer.transform(X[idx_test]))

    X_scaled = np.zeros_like(X, dtype=float)
    X_scaled[idx_train] = X_train
    X_scaled[idx_val] = X_val
    X_scaled[idx_test] = X_test

    train_mask = torch.zeros(len(y), dtype=torch.bool)
    val_mask = torch.zeros(len(y), dtype=torch.bool)
    test_mask = torch.zeros(len(y), dtype=torch.bool)
    train_mask[idx_train] = True
    val_mask[idx_val] = True
    test_mask[idx_test] = True

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data_t = Data(
        x=torch.tensor(X_scaled, dtype=torch.float),
        edge_index=torch.tensor(edge_index, dtype=torch.long),
        y=torch.tensor(y, dtype=torch.float),
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
    ).to(device)

    model = GAT(in_dim=X.shape[1]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    best_val = float("inf")
    best_state = None
    patience = 20
    wait = 0
    max_epochs = 300

    for epoch in range(1, max_epochs + 1):
        model.train()
        optimizer.zero_grad()
        pred = model(data_t.x, data_t.edge_index)
        loss = F.mse_loss(pred[data_t.train_mask], data_t.y[data_t.train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            val_pred = model(data_t.x, data_t.edge_index)
            val_loss = F.mse_loss(val_pred[data_t.val_mask], data_t.y[data_t.val_mask]).item()

        if val_loss < best_val - 1e-6:
            best_val = val_loss
            best_state = model.state_dict()
            wait = 0
        else:
            wait += 1
            if wait >= patience:
                break

    if best_state is not None:
        model.load_state_dict(best_state)

    model.eval()
    with torch.no_grad():
        preds = model(data_t.x, data_t.edge_index).cpu().numpy()

    y_true = data_t.y.cpu().numpy()

    def metrics(mask: np.ndarray) -> Dict[str, float]:
        y_m = y_true[mask]
        p_m = preds[mask]
        return {
            "r2": r2_score(y_m, p_m),
            "mae": mean_absolute_error(y_m, p_m),
            "rmse": mean_squared_error(y_m, p_m, squared=False),
        }

    train_m = metrics(train_mask.cpu().numpy())
    val_m = metrics(val_mask.cpu().numpy())
    test_m = metrics(test_mask.cpu().numpy())

    metrics_df = pd.DataFrame(
        [
            {"split": "train", **train_m},
            {"split": "val", **val_m},
            {"split": "test", **test_m},
        ]
    ).round(4)
    metrics_df.to_csv(OUT_METRICS, index=False, encoding="utf-8-sig")

    pred_df = pd.DataFrame(
        {
            "student_id": node_ids,
            "y_true": y_true,
            "y_pred": preds,
            "split": np.where(train_mask.cpu().numpy(), "train",
                              np.where(val_mask.cpu().numpy(), "val", "test")),
        }
    )
    pred_df.to_csv(OUT_PRED, index=False, encoding="utf-8-sig")

    with open(OUT_DATA_SUMMARY, "w", encoding="utf-8") as f:
        f.write(f"Nodes: {len(node_ids)}\n")
        f.write(f"Edges (directed): {edge_index.shape[1]}\n")
        f.write(f"Features: {X.shape[1]}\n")
        f.write(f"Train/Val/Test: {train_mask.sum().item()}/{val_mask.sum().item()}/{test_mask.sum().item()}\n")
        f.write(f"Best val MSE: {best_val:.6f}\n")
        f.write(f"Early stop at epoch: {epoch}\n")

    print(f"Wrote metrics: {OUT_METRICS}")
    print(f"Wrote predictions: {OUT_PRED}")
    print(f"Wrote node map: {OUT_NODE_MAP}")
    print(f"Wrote features: {OUT_FEATURES}")
    print(f"Wrote summary: {OUT_DATA_SUMMARY}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[Error] {exc}")
        sys.exit(1)
