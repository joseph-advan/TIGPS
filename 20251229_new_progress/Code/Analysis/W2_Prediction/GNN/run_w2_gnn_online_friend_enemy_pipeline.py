
from __future__ import annotations

import json
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress")
W2_PATH = BASE_DIR / r"Data\2024data\TIGPS_W2_studentdata_ver11.csv"
MERGED_Q_PATH = BASE_DIR / r"Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv"
OUT_DIR = BASE_DIR / r"Code\Analysis\W2_Prediction\GNN\results_w2_v14_online_friend_enemy_20260330"

RELATION_COLUMNS: dict[str, list[str]] = {
    "online_friend": [f"v14_1_{i:02d}" for i in range(1, 6)],
    "online_enemy": [f"v14_2_{i:02d}" for i in range(1, 6)],
    "offline_friend": [f"v14_3_{i:02d}" for i in range(1, 6)],
    "offline_enemy": [f"v14_4_{i:02d}" for i in range(1, 6)],
}
RELATION_ORDER = ["online_friend", "online_enemy", "offline_friend", "offline_enemy"]
TARGET_V55_ITEMS = [f"v55_{i}" for i in range(1, 15)]

FEATURE_GROUPS_W2 = [
    "v57", "v27", "v42", "v6", "v5", "v49", "v38", "v40", "v52", "v50", "v28", "v25", "v34",
    "v19", "v1", "v3", "v23", "v36", "v521", "v26", "v54", "v51", "v22",
]

SEEDS = [42, 52, 62, 72, 82]
TEST_SIZE = 0.2
VAL_SIZE_WITHIN_TRAINVAL = 0.25

HIDDEN_DIM = 64
DROPOUT = 0.3
LEARNING_RATE = 1e-2
WEIGHT_DECAY = 1e-4
MAX_EPOCHS = 250
PATIENCE = 30

RIDGE_ALPHAS = np.logspace(-4, 4, 81)
DEVICE = torch.device("cpu")

GNN_MODEL_ORDER = ["gcn_merge", "gcn_separate", "sage_merge", "sage_separate", "gat_merge", "gat_separate"]
ALL_MODEL_ORDER = ["baseline_non_graph"] + GNN_MODEL_ORDER


def make_cols(prefix: str, start: int, end: int) -> list[str]:
    return [f"{prefix}_{i}" for i in range(start, end + 1)]


SUBSCALE_SPECS: dict[str, dict[str, Any]] = {
    "v25_A": {"source_group_id": "v25", "item_cols": make_cols("v25", 1, 3)},
    "v25_B": {"source_group_id": "v25", "item_cols": make_cols("v25", 4, 6)},
    "v25_C": {"source_group_id": "v25", "item_cols": make_cols("v25", 7, 15)},
    "v26_A": {"source_group_id": "v26", "item_cols": make_cols("v26", 1, 3)},
    "v26_B": {"source_group_id": "v26", "item_cols": make_cols("v26", 4, 6)},
    "v27_A": {"source_group_id": "v27", "item_cols": make_cols("v27", 1, 3)},
    "v27_B": {"source_group_id": "v27", "item_cols": ["v27_4"]},
    "v54_A": {"source_group_id": "v54", "item_cols": make_cols("v54", 1, 3)},
    "v54_B": {"source_group_id": "v54", "item_cols": make_cols("v54", 4, 6)},
    "v54_C": {"source_group_id": "v54", "item_cols": make_cols("v54", 7, 9)},
    "v23_A": {"source_group_id": "v23", "item_cols": make_cols("v23", 1, 3)},
    "v23_B": {"source_group_id": "v23", "item_cols": make_cols("v23", 4, 6)},
    "v23_C": {"source_group_id": "v23", "item_cols": make_cols("v23", 7, 9)},
}
SPLIT_SOURCE_GROUP_IDS = {meta["source_group_id"] for meta in SUBSCALE_SPECS.values()}


@dataclass
class Split:
    seed: int
    train_idx: np.ndarray
    val_idx: np.ndarray
    test_idx: np.ndarray


class GCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        self.lin1 = nn.Linear(in_dim, hidden_dim, bias=False)
        self.lin2 = nn.Linear(hidden_dim, out_dim, bias=False)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        h = torch.sparse.mm(adj, x)
        h = self.lin1(h)
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        h = torch.sparse.mm(adj, h)
        return self.lin2(h)


class MultiRelationGCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, num_rel: int, dropout: float) -> None:
        super().__init__()
        self.rel1 = nn.ModuleList([nn.Linear(in_dim, hidden_dim, bias=False) for _ in range(num_rel)])
        self.rel2 = nn.ModuleList([nn.Linear(hidden_dim, out_dim, bias=False) for _ in range(num_rel)])
        self.dropout = dropout

    def forward(self, x: torch.Tensor, adjs: list[torch.Tensor]) -> torch.Tensor:
        h = 0
        for i, adj in enumerate(adjs):
            h = h + self.rel1[i](torch.sparse.mm(adj, x))
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        out = 0
        for i, adj in enumerate(adjs):
            out = out + self.rel2[i](torch.sparse.mm(adj, h))
        return out


class GraphSAGE(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        self.self1 = nn.Linear(in_dim, hidden_dim, bias=False)
        self.nei1 = nn.Linear(in_dim, hidden_dim, bias=False)
        self.self2 = nn.Linear(hidden_dim, out_dim, bias=False)
        self.nei2 = nn.Linear(hidden_dim, out_dim, bias=False)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        h_nei = torch.sparse.mm(adj, x)
        h = self.self1(x) + self.nei1(h_nei)
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        h_nei2 = torch.sparse.mm(adj, h)
        return self.self2(h) + self.nei2(h_nei2)


class MultiRelationGraphSAGE(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, num_rel: int, dropout: float) -> None:
        super().__init__()
        self.self1 = nn.Linear(in_dim, hidden_dim, bias=False)
        self.rel1 = nn.ModuleList([nn.Linear(in_dim, hidden_dim, bias=False) for _ in range(num_rel)])
        self.self2 = nn.Linear(hidden_dim, out_dim, bias=False)
        self.rel2 = nn.ModuleList([nn.Linear(hidden_dim, out_dim, bias=False) for _ in range(num_rel)])
        self.dropout = dropout

    def forward(self, x: torch.Tensor, adjs: list[torch.Tensor]) -> torch.Tensor:
        h = self.self1(x)
        for i, adj in enumerate(adjs):
            h = h + self.rel1[i](torch.sparse.mm(adj, x))
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        out = self.self2(h)
        for i, adj in enumerate(adjs):
            out = out + self.rel2[i](torch.sparse.mm(adj, h))
        return out


class SparseGATLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, dropout: float, negative_slope: float = 0.2) -> None:
        super().__init__()
        self.w = nn.Linear(in_dim, out_dim, bias=False)
        self.a_src = nn.Parameter(torch.empty(out_dim))
        self.a_dst = nn.Parameter(torch.empty(out_dim))
        self.dropout = dropout
        self.negative_slope = negative_slope
        nn.init.xavier_uniform_(self.w.weight)
        nn.init.xavier_uniform_(self.a_src.view(1, -1))
        nn.init.xavier_uniform_(self.a_dst.view(1, -1))

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        src = edge_index[0]
        dst = edge_index[1]
        h = self.w(x)
        e = (h[src] * self.a_src).sum(dim=-1) + (h[dst] * self.a_dst).sum(dim=-1)
        e = F.leaky_relu(e, negative_slope=self.negative_slope)

        n = x.size(0)
        max_per_dst = torch.full((n,), -1e30, device=x.device)
        max_per_dst.scatter_reduce_(0, dst, e, reduce="amax", include_self=True)
        exp_e = torch.exp(e - max_per_dst[dst])
        denom = torch.zeros((n,), device=x.device)
        denom.scatter_add_(0, dst, exp_e)
        alpha = exp_e / (denom[dst] + 1e-12)
        alpha = F.dropout(alpha, p=self.dropout, training=self.training)

        out = torch.zeros((n, h.size(1)), device=x.device)
        out.scatter_add_(0, dst.unsqueeze(1).expand(-1, h.size(1)), alpha.unsqueeze(1) * h[src])
        return out


class GATMerge(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        self.gat1 = SparseGATLayer(in_dim, hidden_dim, dropout)
        self.gat2 = SparseGATLayer(hidden_dim, out_dim, dropout)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        h = self.gat1(x, edge_index)
        h = F.elu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        return self.gat2(h, edge_index)


class GATSeparate(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, num_rel: int, dropout: float) -> None:
        super().__init__()
        self.rel1 = nn.ModuleList([SparseGATLayer(in_dim, hidden_dim, dropout) for _ in range(num_rel)])
        self.rel2 = nn.ModuleList([SparseGATLayer(hidden_dim, out_dim, dropout) for _ in range(num_rel)])
        self.dropout = dropout

    def forward(self, x: torch.Tensor, edge_indexes: list[torch.Tensor]) -> torch.Tensor:
        h = 0
        for i, ei in enumerate(edge_indexes):
            h = h + self.rel1[i](x, ei)
        h = F.elu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        out = 0
        for i, ei in enumerate(edge_indexes):
            out = out + self.rel2[i](h, ei)
        return out

def set_torch_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)


def clear_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def build_gnn_model(model_name: str, in_dim: int) -> nn.Module:
    n_rel = len(RELATION_ORDER)
    if model_name == "gcn_merge":
        return GCN(in_dim, HIDDEN_DIM, 1, DROPOUT).to(DEVICE)
    if model_name == "gcn_separate":
        return MultiRelationGCN(in_dim, HIDDEN_DIM, 1, n_rel, DROPOUT).to(DEVICE)
    if model_name == "sage_merge":
        return GraphSAGE(in_dim, HIDDEN_DIM, 1, DROPOUT).to(DEVICE)
    if model_name == "sage_separate":
        return MultiRelationGraphSAGE(in_dim, HIDDEN_DIM, 1, n_rel, DROPOUT).to(DEVICE)
    if model_name == "gat_merge":
        return GATMerge(in_dim, HIDDEN_DIM, 1, DROPOUT).to(DEVICE)
    if model_name == "gat_separate":
        return GATSeparate(in_dim, HIDDEN_DIM, 1, n_rel, DROPOUT).to(DEVICE)
    raise ValueError(f"Unsupported model_name: {model_name}")


def forward_by_model(
    model_name: str,
    model: nn.Module,
    x: torch.Tensor,
    adj_merged: torch.Tensor,
    adj_list: list[torch.Tensor],
    edge_merged: torch.Tensor,
    edge_list: list[torch.Tensor],
) -> torch.Tensor:
    if model_name in {"gcn_merge", "sage_merge"}:
        return model(x, adj_merged)
    if model_name in {"gcn_separate", "sage_separate"}:
        return model(x, adj_list)
    if model_name == "gat_merge":
        return model(x, edge_merged)
    if model_name == "gat_separate":
        return model(x, edge_list)
    raise ValueError(f"Unsupported model_name: {model_name}")


def candidate_item_names(item: str) -> list[str]:
    cands = [item]
    if "-" in item:
        cands.append(item.replace("-", "_"))
    if "_" in item:
        cands.append(item.replace("_", "-"))
    return list(dict.fromkeys(cands))


def resolve_existing_items(df: pd.DataFrame, items: list[str]) -> tuple[list[str], list[str]]:
    colset = set(df.columns)
    found: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()
    for item in items:
        actual = None
        for cand in candidate_item_names(item):
            if cand in colset:
                actual = cand
                break
        if actual is None:
            missing.append(item)
            continue
        if actual not in seen:
            found.append(actual)
            seen.add(actual)
    return found, missing


def compute_mean_score(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, list[str], list[str]]:
    found, missing = resolve_existing_items(df, items)
    if not found:
        return pd.Series(np.nan, index=df.index, dtype=float), found, missing
    data = df[found].apply(pd.to_numeric, errors="coerce")
    score = data.mean(axis=1, skipna=True)
    score[data.notna().sum(axis=1) == 0] = np.nan
    return score, found, missing


def resolve_group_items(merged_q: pd.DataFrame, year: str, group_id: str) -> list[str]:
    sub = merged_q[
        (merged_q["Year"].astype(str).str.strip() == year)
        & (merged_q["Group_ID"].astype(str).str.strip() == group_id)
    ]
    return sub["Question_ID"].dropna().astype(str).str.strip().tolist()


def build_node_features(w2: pd.DataFrame, merged_q: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []

    for gid in FEATURE_GROUPS_W2:
        if gid in SPLIT_SOURCE_GROUP_IDS:
            continue
        items = resolve_group_items(merged_q, "W2", gid)
        score, used, missing = compute_mean_score(w2, items)
        tmp_col = f"__tmp_feature_{gid}"
        w2[tmp_col] = score
        if used:
            rows.append(
                {
                    "feature_name": gid,
                    "source_group_id": gid,
                    "feature_type": "whole_group",
                    "items_requested": "; ".join(items),
                    "items_used": "; ".join(used),
                    "missing_items": "; ".join(missing),
                    "tmp_col": tmp_col,
                }
            )

    for feat, meta in SUBSCALE_SPECS.items():
        items = list(meta["item_cols"])
        score, used, missing = compute_mean_score(w2, items)
        tmp_col = f"__tmp_feature_{feat}"
        w2[tmp_col] = score
        if used:
            rows.append(
                {
                    "feature_name": feat,
                    "source_group_id": meta["source_group_id"],
                    "feature_type": "subscale",
                    "items_requested": "; ".join(items),
                    "items_used": "; ".join(used),
                    "missing_items": "; ".join(missing),
                    "tmp_col": tmp_col,
                }
            )

    feat_defs = pd.DataFrame(rows)
    split_order = {
        "v25": ["v25_A", "v25_B", "v25_C"],
        "v26": ["v26_A", "v26_B"],
        "v27": ["v27_A", "v27_B"],
        "v54": ["v54_A", "v54_B", "v54_C"],
        "v23": ["v23_A", "v23_B", "v23_C"],
    }
    existing = set(feat_defs["feature_name"].tolist())
    ordered: list[str] = []
    for gid in FEATURE_GROUPS_W2:
        if gid in split_order:
            for sub in split_order[gid]:
                if sub in existing:
                    ordered.append(sub)
        elif gid in existing:
            ordered.append(gid)
    feat_defs = feat_defs.set_index("feature_name").loc[ordered].reset_index()

    features = pd.DataFrame(
        {
            "student_id": w2["student_id"].astype(str).str.strip(),
            "school_id": pd.to_numeric(w2["school_id"], errors="coerce"),
            "class": pd.to_numeric(w2["class"], errors="coerce"),
            "seat_v13": pd.to_numeric(w2["v13"], errors="coerce"),
        }
    )
    for _, row in feat_defs.iterrows():
        features[f"feat_{row['feature_name']}"] = pd.to_numeric(w2[row["tmp_col"]], errors="coerce")
    return features, feat_defs

def normalize_intlike(v: Any) -> str | None:
    if pd.isna(v):
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        f = float(s)
        if math.isfinite(f):
            i = int(round(f))
            if abs(f - i) < 1e-6:
                return str(i)
    except Exception:
        pass
    if re.fullmatch(r"\d+", s):
        return str(int(s))
    return s


def parse_seat_value(v: Any) -> tuple[int | None, str]:
    if pd.isna(v):
        return None, "empty"
    s = str(v).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return None, "empty"
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m:
        return None, "invalid_format"
    try:
        num = float(m.group())
    except Exception:
        return None, "invalid_format"
    if num <= 0:
        return None, "zero_or_negative"
    return int(round(num)), "ok"


def build_seat_mapping(w2: pd.DataFrame) -> tuple[dict[tuple[str, str, int], str], pd.DataFrame]:
    tmp = pd.DataFrame(
        {
            "student_id": w2["student_id"].astype(str).str.strip(),
            "school_key": w2["school_id"].apply(normalize_intlike),
            "class_key": w2["class"].apply(normalize_intlike),
            "seat_num": pd.to_numeric(w2["v13"], errors="coerce"),
        }
    )
    tmp["seat_num"] = tmp["seat_num"].round().astype("Int64")
    tmp = tmp.dropna(subset=["school_key", "class_key", "seat_num"]).copy()

    key_to_ids: dict[tuple[str, str, int], set[str]] = {}
    for r in tmp.itertuples(index=False):
        key = (str(r.school_key), str(r.class_key), int(r.seat_num))
        key_to_ids.setdefault(key, set()).add(str(r.student_id))

    conflicts = []
    mapping: dict[tuple[str, str, int], str] = {}
    for k, ids in key_to_ids.items():
        sorted_ids = sorted(ids)
        mapping[k] = sorted_ids[0]
        if len(sorted_ids) > 1:
            conflicts.append(
                {
                    "school_key": k[0],
                    "class_key": k[1],
                    "seat": k[2],
                    "student_id_candidates": "; ".join(sorted_ids),
                    "candidate_count": len(sorted_ids),
                }
            )
    return mapping, pd.DataFrame(conflicts)


def extract_relation_edges(
    w2: pd.DataFrame,
    mapping: dict[tuple[str, str, int], str],
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    edge_rows: list[dict[str, Any]] = []
    unmatched_rows: list[dict[str, Any]] = []
    attempt_counts = {rel: 0 for rel in RELATION_ORDER}

    relation_cols = [c for rel in RELATION_ORDER for c in RELATION_COLUMNS[rel]]
    use_cols = ["student_id", "school_id", "class"] + relation_cols
    sub = w2[use_cols].copy().rename(columns={"class": "class_id"})
    sub["student_id"] = sub["student_id"].astype(str).str.strip()

    for r in sub.itertuples(index=False):
        src = str(r.student_id).strip()
        school_key = normalize_intlike(r.school_id)
        class_key = normalize_intlike(r.class_id)
        if school_key is None or class_key is None:
            continue

        for relation in RELATION_ORDER:
            cols = RELATION_COLUMNS[relation]
            for slot_i, col in enumerate(cols, start=1):
                raw_val = getattr(r, col)
                seat, reason = parse_seat_value(raw_val)
                if reason in {"empty", "zero_or_negative"}:
                    continue
                attempt_counts[relation] += 1

                if reason != "ok" or seat is None:
                    unmatched_rows.append(
                        {
                            "src_student_id": src,
                            "src_school_key": school_key,
                            "src_class_key": class_key,
                            "relation": relation,
                            "slot": slot_i,
                            "raw_value": raw_val,
                            "parsed_seat": np.nan if seat is None else seat,
                            "reason": reason,
                        }
                    )
                    continue

                key = (school_key, class_key, int(seat))
                dst = mapping.get(key)
                if dst is None:
                    unmatched_rows.append(
                        {
                            "src_student_id": src,
                            "src_school_key": school_key,
                            "src_class_key": class_key,
                            "relation": relation,
                            "slot": slot_i,
                            "raw_value": raw_val,
                            "parsed_seat": seat,
                            "reason": "dst_not_found",
                        }
                    )
                    continue

                edge_rows.append(
                    {
                        "src_student_id": src,
                        "dst_student_id": dst,
                        "relation": relation,
                        "slot": slot_i,
                        "parsed_seat": seat,
                        "raw_value": raw_val,
                    }
                )

    return pd.DataFrame(edge_rows), pd.DataFrame(unmatched_rows), attempt_counts


def dedup_and_weight(edge_df: pd.DataFrame, relation: str | None = None) -> pd.DataFrame:
    df = edge_df.copy()
    if relation is not None:
        df = df[df["relation"] == relation].copy()
    if df.empty:
        return pd.DataFrame(columns=["src_student_id", "dst_student_id", "weight"])
    return (
        df.groupby(["src_student_id", "dst_student_id"], as_index=False)
        .size()
        .rename(columns={"size": "weight"})
    )


def build_sparse_norm_adj(
    num_nodes: int,
    src_idx: np.ndarray,
    dst_idx: np.ndarray,
    weights: np.ndarray | None = None,
) -> torch.Tensor:
    if weights is None:
        weights = np.ones(len(src_idx), dtype=np.float32)
    else:
        weights = weights.astype(np.float32)

    all_src = np.concatenate([src_idx, dst_idx, np.arange(num_nodes, dtype=np.int64)])
    all_dst = np.concatenate([dst_idx, src_idx, np.arange(num_nodes, dtype=np.int64)])
    all_w = np.concatenate([weights, weights, np.ones(num_nodes, dtype=np.float32)])

    mat = sp.coo_matrix((all_w, (all_src, all_dst)), shape=(num_nodes, num_nodes), dtype=np.float32).tocsr()
    deg = np.asarray(mat.sum(axis=1)).reshape(-1)
    deg_inv_sqrt = np.zeros_like(deg, dtype=np.float32)
    nz = deg > 0
    deg_inv_sqrt[nz] = np.power(deg[nz], -0.5)
    norm = sp.diags(deg_inv_sqrt) @ mat @ sp.diags(deg_inv_sqrt)
    norm = norm.tocoo()

    idx = torch.tensor(np.vstack([norm.row, norm.col]), dtype=torch.long, device=DEVICE)
    vals = torch.tensor(norm.data, dtype=torch.float32, device=DEVICE)
    return torch.sparse_coo_tensor(idx, vals, size=(num_nodes, num_nodes), device=DEVICE).coalesce()


def build_edge_index(num_nodes: int, src_idx: np.ndarray, dst_idx: np.ndarray) -> torch.Tensor:
    if len(src_idx) > 0:
        all_src = np.concatenate([src_idx, dst_idx])
        all_dst = np.concatenate([dst_idx, src_idx])
    else:
        all_src = np.array([], dtype=np.int64)
        all_dst = np.array([], dtype=np.int64)

    loops = np.arange(num_nodes, dtype=np.int64)
    all_src = np.concatenate([all_src, loops])
    all_dst = np.concatenate([all_dst, loops])

    pairs = np.unique(np.column_stack([all_src, all_dst]), axis=0)
    return torch.tensor(pairs.T, dtype=torch.long, device=DEVICE)


def metric_classification(y_true: np.ndarray, prob: np.ndarray) -> dict[str, float]:
    pred = (prob >= 0.5).astype(int)
    auc = float(roc_auc_score(y_true, prob)) if len(np.unique(y_true)) >= 2 else np.nan
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "auc": auc,
    }


def metric_regression(y_true: np.ndarray, pred: np.ndarray, cutoff: float) -> dict[str, float]:
    cls_true = (y_true >= cutoff).astype(int)
    cls_pred = (pred >= cutoff).astype(int)
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, pred))),
        "mae": float(mean_absolute_error(y_true, pred)),
        "r2": float(r2_score(y_true, pred)),
        "median_class_acc_from_score": float(accuracy_score(cls_true, cls_pred)),
    }

def make_group_strata(group_ids: np.ndarray, y_cls: np.ndarray) -> pd.DataFrame:
    gdf = pd.DataFrame({"group_id": group_ids, "y_cls": y_cls})
    stats = (
        gdf.groupby("group_id", as_index=False)
        .agg(group_size=("y_cls", "size"), pos_rate=("y_cls", "mean"))
        .sort_values("group_id")
        .reset_index(drop=True)
    )

    n_groups = len(stats)
    q_pos = max(2, min(5, n_groups))
    q_size = max(2, min(3, n_groups))
    try:
        pos_bin = pd.qcut(stats["pos_rate"], q=q_pos, duplicates="drop").astype(str)
    except Exception:
        pos_bin = pd.Series(["all"] * n_groups)
    try:
        size_bin = pd.qcut(stats["group_size"], q=q_size, duplicates="drop").astype(str)
    except Exception:
        size_bin = pd.Series(["all"] * n_groups)

    stats["strata"] = pos_bin + "|" + size_bin
    vc = stats["strata"].value_counts()
    stats.loc[stats["strata"].map(vc) < 2, "strata"] = "other"
    return stats


def split_groups(group_stats: pd.DataFrame, test_size: float, seed: int) -> tuple[set[str], set[str]]:
    groups = group_stats["group_id"].astype(str).to_numpy()
    strata = group_stats["strata"].astype(str).to_numpy()
    stratify = strata if len(np.unique(strata)) > 1 else None
    try:
        g_train, g_test = train_test_split(groups, test_size=test_size, random_state=seed, stratify=stratify)
    except Exception:
        g_train, g_test = train_test_split(groups, test_size=test_size, random_state=seed, shuffle=True)
    return set(g_train), set(g_test)


def build_group_disjoint_split(group_ids: np.ndarray, y_cls: np.ndarray, seed: int) -> tuple[Split, dict[str, Any]]:
    all_idx = np.arange(len(group_ids))
    gstats = make_group_strata(group_ids, y_cls)

    for attempt in range(50):
        eff_seed = seed + attempt * 101
        train_val_groups, test_groups = split_groups(gstats, TEST_SIZE, eff_seed)
        gstats_tv = gstats[gstats["group_id"].astype(str).isin(train_val_groups)].copy()
        train_groups, val_groups = split_groups(gstats_tv, VAL_SIZE_WITHIN_TRAINVAL, eff_seed + 17)

        train_idx = all_idx[np.isin(group_ids, list(train_groups))]
        val_idx = all_idx[np.isin(group_ids, list(val_groups))]
        test_idx = all_idx[np.isin(group_ids, list(test_groups))]

        if len(train_idx) == 0 or len(val_idx) == 0 or len(test_idx) == 0:
            continue
        if len(np.unique(y_cls[train_idx])) < 2 or len(np.unique(y_cls[val_idx])) < 2 or len(np.unique(y_cls[test_idx])) < 2:
            continue

        details = {
            "seed": seed,
            "effective_seed": eff_seed,
            "train_n": len(train_idx),
            "val_n": len(val_idx),
            "test_n": len(test_idx),
            "train_groups_n": len(train_groups),
            "val_groups_n": len(val_groups),
            "test_groups_n": len(test_groups),
            "overlap_train_test_groups": len(train_groups & test_groups),
            "overlap_train_val_groups": len(train_groups & val_groups),
            "overlap_val_test_groups": len(val_groups & test_groups),
            "train_pos_n": int(y_cls[train_idx].sum()),
            "val_pos_n": int(y_cls[val_idx].sum()),
            "test_pos_n": int(y_cls[test_idx].sum()),
        }
        return Split(seed=seed, train_idx=train_idx, val_idx=val_idx, test_idx=test_idx), details

    raise RuntimeError(f"Unable to build valid group-disjoint split for seed={seed}")


def train_eval_baseline(
    X: np.ndarray,
    y_cls: np.ndarray,
    y_sum: np.ndarray,
    cut_sum: float,
    split: Split,
    seed: int,
) -> list[dict[str, Any]]:
    tr, te = split.train_idx, split.test_idx
    imp = SimpleImputer(strategy="median")
    scl = StandardScaler()
    X_train = scl.fit_transform(imp.fit_transform(X[tr]))
    X_test = scl.transform(imp.transform(X[te]))

    rows: list[dict[str, Any]] = []
    clf = LogisticRegression(max_iter=5000, solver="lbfgs", random_state=seed)
    clf.fit(X_train, y_cls[tr])
    prob = clf.predict_proba(X_test)[:, 1]
    for k, v in metric_classification(y_cls[te], prob).items():
        rows.append({"seed": seed, "model": "baseline_non_graph", "task": "classification", "metric": k, "value": v})

    reg = RidgeCV(alphas=RIDGE_ALPHAS, cv=5)
    reg.fit(X_train, y_sum[tr])
    pred = reg.predict(X_test)
    for k, v in metric_regression(y_sum[te], pred, cutoff=cut_sum).items():
        rows.append({"seed": seed, "model": "baseline_non_graph", "task": "regression_sum", "metric": k, "value": v})
    return rows


def train_eval_gnn_classification(
    model_name: str,
    X_full: torch.Tensor,
    y_cls: torch.Tensor,
    split: Split,
    adj_merged: torch.Tensor,
    adj_list: list[torch.Tensor],
    edge_merged: torch.Tensor,
    edge_list: list[torch.Tensor],
    seed: int,
) -> tuple[dict[str, float], int]:
    set_torch_seed(seed)
    model = build_gnn_model(model_name, X_full.shape[1])

    opt = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    tr = torch.tensor(split.train_idx, dtype=torch.long, device=DEVICE)
    va = torch.tensor(split.val_idx, dtype=torch.long, device=DEVICE)
    te = torch.tensor(split.test_idx, dtype=torch.long, device=DEVICE)

    best_state = None
    best_val = -np.inf
    best_epoch = 0
    bad = 0
    y_val_np = y_cls[va].cpu().numpy()

    for ep in range(1, MAX_EPOCHS + 1):
        model.train()
        opt.zero_grad()
        logits = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)
        loss = F.binary_cross_entropy_with_logits(logits[tr], y_cls[tr])
        loss.backward()
        opt.step()

        model.eval()
        with torch.no_grad():
            val_logits = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)[va]
            val_prob = torch.sigmoid(val_logits).cpu().numpy()
            val_metric = float(roc_auc_score(y_val_np, val_prob)) if len(np.unique(y_val_np)) >= 2 else float(accuracy_score(y_val_np, (val_prob >= 0.5).astype(int)))

        if val_metric > best_val + 1e-6:
            best_val = val_metric
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            best_epoch = ep
            bad = 0
        else:
            bad += 1
            if bad >= PATIENCE:
                break

    assert best_state is not None
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_logits = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)[te]
    return metric_classification(y_cls[te].cpu().numpy(), torch.sigmoid(test_logits).cpu().numpy()), best_epoch


def train_eval_gnn_regression(
    model_name: str,
    X_full: torch.Tensor,
    y: torch.Tensor,
    cutoff: float,
    split: Split,
    adj_merged: torch.Tensor,
    adj_list: list[torch.Tensor],
    edge_merged: torch.Tensor,
    edge_list: list[torch.Tensor],
    seed: int,
) -> tuple[dict[str, float], int]:
    set_torch_seed(seed)
    model = build_gnn_model(model_name, X_full.shape[1])

    opt = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    tr = torch.tensor(split.train_idx, dtype=torch.long, device=DEVICE)
    va = torch.tensor(split.val_idx, dtype=torch.long, device=DEVICE)
    te = torch.tensor(split.test_idx, dtype=torch.long, device=DEVICE)

    best_state = None
    best_rmse = np.inf
    best_epoch = 0
    bad = 0
    y_val_np = y[va].cpu().numpy()

    for ep in range(1, MAX_EPOCHS + 1):
        model.train()
        opt.zero_grad()
        pred = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)
        loss = F.mse_loss(pred[tr], y[tr])
        loss.backward()
        opt.step()

        model.eval()
        with torch.no_grad():
            val_pred = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)[va].cpu().numpy()
            val_rmse = float(np.sqrt(mean_squared_error(y_val_np, val_pred)))

        if val_rmse < best_rmse - 1e-6:
            best_rmse = val_rmse
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            best_epoch = ep
            bad = 0
        else:
            bad += 1
            if bad >= PATIENCE:
                break

    assert best_state is not None
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_pred = forward_by_model(model_name, model, X_full, adj_merged, adj_list, edge_merged, edge_list).squeeze(1)[te].cpu().numpy()
    return metric_regression(y[te].cpu().numpy(), test_pred, cutoff=cutoff), best_epoch


def aggregate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["model", "task", "metric"], as_index=False)["value"].agg(["mean", "std"]).reset_index()
    return out.rename(columns={"mean": "value_mean", "std": "value_std"})

def main() -> None:
    clear_output_dir(OUT_DIR)
    print(f"Output dir: {OUT_DIR}")

    w2 = pd.read_csv(W2_PATH, low_memory=False)
    merged_q = pd.read_csv(MERGED_Q_PATH, dtype=str)
    merged_q["Year"] = merged_q["Year"].astype(str).str.strip()
    merged_q["Group_ID"] = merged_q["Group_ID"].astype(str).str.strip()
    merged_q["Question_ID"] = merged_q["Question_ID"].astype(str).str.strip()

    relation_cols = [c for rel in RELATION_ORDER for c in RELATION_COLUMNS[rel]]
    required_cols = ["student_id", "school_id", "class", "v13"] + relation_cols + TARGET_V55_ITEMS
    missing = [c for c in required_cols if c not in w2.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    print("Phase A: mapping and edges...")
    mapping, conflicts_df = build_seat_mapping(w2)
    edges_raw, unmatched_df, attempt_counts = extract_relation_edges(w2, mapping)
    if edges_raw.empty:
        raise ValueError("No matched edges from v14 relations.")

    edges_raw["is_self_loop"] = edges_raw["src_student_id"] == edges_raw["dst_student_id"]
    edges_no_self = edges_raw[~edges_raw["is_self_loop"]].copy()

    relation_w: dict[str, pd.DataFrame] = {}
    for rel in RELATION_ORDER:
        relation_w[rel] = dedup_and_weight(edges_no_self, rel)

    merged_w = pd.concat(list(relation_w.values()), ignore_index=True)
    if merged_w.empty:
        merged_w = pd.DataFrame(columns=["src_student_id", "dst_student_id", "weight"])
    else:
        merged_w = (
            merged_w.groupby(["src_student_id", "dst_student_id"], as_index=False)["weight"]
            .sum()
            .sort_values(["src_student_id", "dst_student_id"])
            .reset_index(drop=True)
        )

    print("Phase B: node features and labels...")
    feat_df, feat_defs = build_node_features(w2.copy(), merged_q)
    feat_cols = [c for c in feat_df.columns if c.startswith("feat_")] + ["school_id", "class", "seat_v13"]
    feat_df[feat_cols] = feat_df[feat_cols].apply(pd.to_numeric, errors="coerce")

    label_df = pd.DataFrame({"student_id": w2["student_id"].astype(str).str.strip()})
    for c in TARGET_V55_ITEMS:
        label_df[c] = pd.to_numeric(w2[c], errors="coerce")
    label_df["target_sum"] = label_df[TARGET_V55_ITEMS].sum(axis=1, skipna=True)
    nonmiss = label_df[TARGET_V55_ITEMS].notna().sum(axis=1)
    label_df.loc[nonmiss == 0, "target_sum"] = np.nan

    node_df = feat_df.merge(label_df[["student_id", "target_sum"]], on="student_id", how="inner")
    node_df = node_df.dropna(subset=["target_sum"]).copy().reset_index(drop=True)
    node_df["school_key"] = pd.to_numeric(node_df["school_id"], errors="coerce").round().astype("Int64").astype(str)
    node_df["class_key"] = pd.to_numeric(node_df["class"], errors="coerce").round().astype("Int64").astype(str)
    node_df["group_id"] = node_df["school_key"] + "_" + node_df["class_key"]
    node_df["node_idx"] = np.arange(len(node_df), dtype=np.int64)

    id_set = set(node_df["student_id"])
    for rel in RELATION_ORDER:
        relation_w[rel] = relation_w[rel][
            relation_w[rel]["src_student_id"].isin(id_set) & relation_w[rel]["dst_student_id"].isin(id_set)
        ].copy()
    merged_w = merged_w[merged_w["src_student_id"].isin(id_set) & merged_w["dst_student_id"].isin(id_set)].copy()

    id_to_idx = dict(zip(node_df["student_id"], node_df["node_idx"]))

    def map_idx(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            cols = list(df.columns)
            if "src_idx" not in cols:
                cols.append("src_idx")
            if "dst_idx" not in cols:
                cols.append("dst_idx")
            return pd.DataFrame(columns=cols)
        out = df.copy()
        out["src_idx"] = out["src_student_id"].map(id_to_idx)
        out["dst_idx"] = out["dst_student_id"].map(id_to_idx)
        out = out.dropna(subset=["src_idx", "dst_idx"]).copy()
        out["src_idx"] = out["src_idx"].astype(int)
        out["dst_idx"] = out["dst_idx"].astype(int)
        return out

    relation_i: dict[str, pd.DataFrame] = {rel: map_idx(relation_w[rel]) for rel in RELATION_ORDER}
    merged_i = map_idx(merged_w)
    n_nodes = len(node_df)

    adj_by_rel: dict[str, torch.Tensor] = {}
    edge_by_rel: dict[str, torch.Tensor] = {}
    for rel in RELATION_ORDER:
        rel_df = relation_i[rel]
        src = rel_df["src_idx"].to_numpy(np.int64) if not rel_df.empty else np.array([], dtype=np.int64)
        dst = rel_df["dst_idx"].to_numpy(np.int64) if not rel_df.empty else np.array([], dtype=np.int64)
        w = rel_df["weight"].to_numpy(np.float32) if not rel_df.empty else np.array([], dtype=np.float32)
        adj_by_rel[rel] = build_sparse_norm_adj(n_nodes, src, dst, w)
        edge_by_rel[rel] = build_edge_index(n_nodes, src, dst)

    merged_src = merged_i["src_idx"].to_numpy(np.int64) if not merged_i.empty else np.array([], dtype=np.int64)
    merged_dst = merged_i["dst_idx"].to_numpy(np.int64) if not merged_i.empty else np.array([], dtype=np.int64)
    merged_weight = merged_i["weight"].to_numpy(np.float32) if not merged_i.empty else np.array([], dtype=np.float32)

    adj_merged = build_sparse_norm_adj(n_nodes, merged_src, merged_dst, merged_weight)
    edge_merged = build_edge_index(n_nodes, merged_src, merged_dst)
    adj_list = [adj_by_rel[r] for r in RELATION_ORDER]
    edge_list = [edge_by_rel[r] for r in RELATION_ORDER]

    X = node_df[feat_cols].to_numpy(dtype=np.float64)
    y_sum = node_df["target_sum"].to_numpy(dtype=np.float64)
    cut_sum = float(np.median(y_sum))
    y_cls = (y_sum >= cut_sum).astype(int)

    print("Writing audit artifacts...")
    audit_rows = [
        {"item": "w2_rows_raw", "value": len(w2)},
        {"item": "nodes_with_label", "value": len(node_df)},
        {"item": "group_count_school_class", "value": node_df["group_id"].nunique()},
        {"item": "seat_mapping_key_count", "value": len(mapping)},
        {"item": "seat_mapping_conflict_key_count", "value": len(conflicts_df)},
        {"item": "raw_matched_edge_rows_total", "value": len(edges_raw)},
        {"item": "raw_self_loops_total", "value": int(edges_raw["is_self_loop"].sum())},
        {"item": "unmatched_rows_total", "value": len(unmatched_df)},
        {"item": "merged_edges_unique_no_self", "value": len(merged_w)},
        {"item": "global_median_target_sum", "value": cut_sum},
        {"item": "class_1_count", "value": int((y_cls == 1).sum())},
        {"item": "class_0_count", "value": int((y_cls == 0).sum())},
    ]

    for rel in RELATION_ORDER:
        matched_rel = int((edges_raw["relation"] == rel).sum())
        self_rel = int(((edges_raw["relation"] == rel) & (edges_raw["is_self_loop"])).sum())
        unmatched_rel = int((unmatched_df["relation"] == rel).sum()) if not unmatched_df.empty else 0
        audit_rows.append({"item": f"attempted_nominations_{rel}", "value": int(attempt_counts.get(rel, 0))})
        audit_rows.append({"item": f"raw_matched_edge_rows_{rel}", "value": matched_rel})
        audit_rows.append({"item": f"raw_self_loops_{rel}", "value": self_rel})
        audit_rows.append({"item": f"unmatched_rows_{rel}", "value": unmatched_rel})
        audit_rows.append({"item": f"unique_edges_no_self_{rel}", "value": len(relation_w[rel])})

    pd.DataFrame(audit_rows).to_csv(OUT_DIR / "00_data_audit_summary.csv", index=False, encoding="utf-8-sig")
    unmatched_df.to_csv(OUT_DIR / "00_unmatched_nominations.csv", index=False, encoding="utf-8-sig")
    conflicts_df.to_csv(OUT_DIR / "00_mapping_conflicts.csv", index=False, encoding="utf-8-sig")

    for rel in RELATION_ORDER:
        relation_i[rel].to_csv(OUT_DIR / f"01_edges_{rel}_weighted.csv", index=False, encoding="utf-8-sig")
    merged_i.to_csv(OUT_DIR / "01_edges_all_relations_merged_weighted.csv", index=False, encoding="utf-8-sig")

    feat_defs.to_csv(OUT_DIR / "01_feature_definitions.csv", index=False, encoding="utf-8-sig")
    node_df[["node_idx", "student_id", "school_id", "class", "seat_v13", "group_id"]].to_csv(
        OUT_DIR / "01_nodes.csv", index=False, encoding="utf-8-sig"
    )
    node_df[["node_idx", "student_id", "target_sum"]].to_csv(
        OUT_DIR / "01_labels.csv", index=False, encoding="utf-8-sig"
    )

    print("Phase C: train baseline + GNN models...")
    all_rows: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    epoch_rows: list[dict[str, Any]] = []
    groups_arr = node_df["group_id"].astype(str).to_numpy()

    for seed in SEEDS:
        print(f"  seed={seed}")
        split, split_info = build_group_disjoint_split(groups_arr, y_cls, seed)
        split_rows.append(split_info)
        all_rows.extend(train_eval_baseline(X, y_cls, y_sum, cut_sum, split, seed))

        imp = SimpleImputer(strategy="median")
        scl = StandardScaler()
        X_train = scl.fit_transform(imp.fit_transform(X[split.train_idx]))
        _ = X_train
        X_full = scl.transform(imp.transform(X))

        X_t = torch.tensor(X_full, dtype=torch.float32, device=DEVICE)
        y_cls_t = torch.tensor(y_cls.astype(np.float32), dtype=torch.float32, device=DEVICE)
        y_sum_t = torch.tensor(y_sum.astype(np.float32), dtype=torch.float32, device=DEVICE)

        for gnn_model in GNN_MODEL_ORDER:
            cls_m, ep = train_eval_gnn_classification(
                gnn_model, X_t, y_cls_t, split, adj_merged, adj_list, edge_merged, edge_list, seed
            )
            epoch_rows.append({"seed": seed, "model": gnn_model, "task": "classification", "best_epoch": ep})
            for k, v in cls_m.items():
                all_rows.append({"seed": seed, "model": gnn_model, "task": "classification", "metric": k, "value": v})

            sum_m, ep = train_eval_gnn_regression(
                gnn_model, X_t, y_sum_t, cut_sum, split, adj_merged, adj_list, edge_merged, edge_list, seed
            )
            epoch_rows.append({"seed": seed, "model": gnn_model, "task": "regression_sum", "best_epoch": ep})
            for k, v in sum_m.items():
                all_rows.append({"seed": seed, "model": gnn_model, "task": "regression_sum", "metric": k, "value": v})

    seed_df = pd.DataFrame(all_rows)
    agg_df = aggregate_metrics(seed_df)
    split_df = pd.DataFrame(split_rows)
    epoch_df = pd.DataFrame(epoch_rows)

    seed_df.to_csv(OUT_DIR / "02_all_seed_metrics_long.csv", index=False, encoding="utf-8-sig")
    agg_df.to_csv(OUT_DIR / "03_model_metric_mean_std.csv", index=False, encoding="utf-8-sig")
    split_df.to_csv(OUT_DIR / "03_split_info.csv", index=False, encoding="utf-8-sig")
    epoch_df.to_csv(OUT_DIR / "03_gnn_best_epochs.csv", index=False, encoding="utf-8-sig")

    print("Phase D: summary report...")
    key_map = {
        "classification": ["accuracy", "f1", "auc"],
        "regression_sum": ["rmse", "mae", "r2", "median_class_acc_from_score"],
    }
    comp_rows = []
    for task, metrics in key_map.items():
        for metric in metrics:
            sub = agg_df[(agg_df["task"] == task) & (agg_df["metric"] == metric)].copy()
            row = {"task": task, "metric": metric}
            for model in ALL_MODEL_ORDER:
                ss = sub[sub["model"] == model]
                row[f"{model}_mean"] = float(ss["value_mean"].iloc[0]) if not ss.empty else np.nan
                row[f"{model}_std"] = float(ss["value_std"].iloc[0]) if not ss.empty else np.nan

            higher_better = metric in {"accuracy", "f1", "auc", "r2", "median_class_acc_from_score"}
            for gnn_model in GNN_MODEL_ORDER:
                if higher_better:
                    row[f"delta_{gnn_model}_minus_baseline"] = row[f"{gnn_model}_mean"] - row["baseline_non_graph_mean"]
                else:
                    row[f"delta_{gnn_model}_minus_baseline"] = row["baseline_non_graph_mean"] - row[f"{gnn_model}_mean"]
            comp_rows.append(row)
    comp_df = pd.DataFrame(comp_rows)
    comp_df.to_csv(OUT_DIR / "04_key_metric_comparison.csv", index=False, encoding="utf-8-sig")

    with open(OUT_DIR / "04_summary.txt", "w", encoding="utf-8") as f:
        f.write("W2 v14 four-relation GNN pipeline summary\n")
        f.write("=" * 72 + "\n")
        f.write(f"W2 data: {W2_PATH}\n")
        f.write(f"Merged mapping: {MERGED_Q_PATH}\n")
        f.write(f"Seeds: {SEEDS}\n")
        f.write("Split method: group-disjoint by school_id+class\n")
        f.write(f"Nodes: {n_nodes}\n")
        for rel in RELATION_ORDER:
            f.write(f"{rel} edges (unique no-self): {len(relation_w[rel])}\n")
        f.write(f"Merged edges (unique no-self): {len(merged_w)}\n")
        f.write(f"Unmatched nominations: {len(unmatched_df)}\n")
        f.write(f"Mapping conflict keys: {len(conflicts_df)}\n")
        f.write("\nKey metrics (mean +/- std)\n")
        for _, r in comp_df.iterrows():
            parts = []
            for model in ALL_MODEL_ORDER:
                parts.append(f"{model}={r[f'{model}_mean']:.4f}+/-{r[f'{model}_std']:.4f}")
            f.write(f"- {r['task']} / {r['metric']}: " + ", ".join(parts) + "\n")

    with open(OUT_DIR / "00_run_config.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "w2_path": str(W2_PATH),
                "merged_q_path": str(MERGED_Q_PATH),
                "relation_columns": RELATION_COLUMNS,
                "relation_order": RELATION_ORDER,
                "target_items": TARGET_V55_ITEMS,
                "feature_groups": FEATURE_GROUPS_W2,
                "seeds": SEEDS,
                "split_method": "group_disjoint_school_class",
                "test_size": TEST_SIZE,
                "val_size_within_trainval": VAL_SIZE_WITHIN_TRAINVAL,
                "models": ALL_MODEL_ORDER,
                "tasks": ["classification_median_split", "regression_sum"],
                "model": {
                    "hidden_dim": HIDDEN_DIM,
                    "dropout": DROPOUT,
                    "lr": LEARNING_RATE,
                    "weight_decay": WEIGHT_DECAY,
                    "max_epochs": MAX_EPOCHS,
                    "patience": PATIENCE,
                },
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print("Done.")
    print(f"Wrote outputs to: {OUT_DIR}")


if __name__ == "__main__":
    main()
