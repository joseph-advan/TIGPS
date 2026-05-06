from __future__ import annotations

import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parents[2]
CORE_DIR_CANDIDATES = [
    SCRIPT_DIR.parent / "Interpersonal_features",
    SCRIPT_DIR.parent / "logistic_baseline_added_Interpersonal_features",
]
CORE_DIR = None
for _p in CORE_DIR_CANDIDATES:
    if _p.exists():
        CORE_DIR = _p
        break
if CORE_DIR is None:
    raise FileNotFoundError(f"Cannot find core dir. Tried: {CORE_DIR_CANDIDATES}")
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
import run_interpersonal_feature_logistic_comparison as core  # noqa: E402


OUT_DIR = SCRIPT_DIR / "outputs"
FEATURE_OUT = OUT_DIR / "features"
DIAG_OUT = OUT_DIR / "diagnostics"
RESULT_OUT = OUT_DIR / "model_results"

SEEDS = [42, 52, 62, 72, 82]
TEST_SIZE = 0.2
VAL_SIZE_WITHIN_TRAINVAL = 0.25

HIDDEN_DIM = 64
DROPOUT = 0.3
LEARNING_RATE = 1e-2
WEIGHT_DECAY = 1e-4
MAX_EPOCHS = 220
PATIENCE = 30

DEVICE = torch.device("cpu")


@dataclass(frozen=True)
class Scenario:
    name: str
    feature_year: str
    target_year: str
    target_group_id: str
    edge_year: str


SCENARIOS = [
    Scenario(name="w2_self", feature_year="W2", target_year="W2", target_group_id="v55", edge_year="W2"),
    Scenario(name="w3_self", feature_year="W3", target_year="W3", target_group_id="54", edge_year="W3"),
    Scenario(name="w2_predict_w3", feature_year="W2", target_year="W3", target_group_id="54", edge_year="W2"),
]


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


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def ensure_dirs() -> None:
    for p in [OUT_DIR, FEATURE_OUT, DIAG_OUT, RESULT_OUT]:
        p.mkdir(parents=True, exist_ok=True)


def safe_auc(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(roc_auc_score(y_true, y_prob))


def to_sparse_row_normalized_adj(
    n_nodes: int,
    src_idx: np.ndarray,
    dst_idx: np.ndarray,
) -> torch.Tensor:
    # Message passing to dst from src, i.e. row=dst, col=src.
    if len(src_idx) == 0:
        indices = torch.zeros((2, 0), dtype=torch.long, device=DEVICE)
        values = torch.zeros((0,), dtype=torch.float32, device=DEVICE)
        return torch.sparse_coo_tensor(indices, values, (n_nodes, n_nodes), device=DEVICE).coalesce()

    row = dst_idx.astype(np.int64)
    col = src_idx.astype(np.int64)
    deg = np.bincount(row, minlength=n_nodes).astype(np.float32)
    deg[deg == 0.0] = 1.0
    values = 1.0 / deg[row]

    indices = torch.tensor(np.vstack([row, col]), dtype=torch.long, device=DEVICE)
    vals = torch.tensor(values, dtype=torch.float32, device=DEVICE)
    return torch.sparse_coo_tensor(indices, vals, (n_nodes, n_nodes), device=DEVICE).coalesce()


def build_graph_for_nodes(edge_df: pd.DataFrame, node_ids: list[str]) -> tuple[torch.Tensor, dict[str, Any]]:
    id2idx = {sid: i for i, sid in enumerate(node_ids)}
    src = edge_df["student_id_src"].astype(str)
    dst = edge_df["student_id_dst"].astype(str)
    keep = src.isin(id2idx) & dst.isin(id2idx) & (src != dst)
    sub = edge_df.loc[keep, ["student_id_src", "student_id_dst"]].drop_duplicates().copy()

    if sub.empty:
        adj = to_sparse_row_normalized_adj(len(node_ids), np.array([], dtype=np.int64), np.array([], dtype=np.int64))
        diag = {"n_edges_after_filter": 0, "edge_density": 0.0}
        return adj, diag

    src_idx = sub["student_id_src"].map(id2idx).to_numpy(dtype=np.int64)
    dst_idx = sub["student_id_dst"].map(id2idx).to_numpy(dtype=np.int64)

    adj = to_sparse_row_normalized_adj(len(node_ids), src_idx=src_idx, dst_idx=dst_idx)
    diag = {
        "n_edges_after_filter": int(len(sub)),
        "edge_density": float(len(sub) / max(1, len(node_ids) * (len(node_ids) - 1))),
    }
    return adj, diag


def prepare_task_payload(
    scenario: Scenario,
    merged: pd.DataFrame,
    year_raw: dict[str, pd.DataFrame],
    year_edges: dict[str, pd.DataFrame],
) -> dict[str, Any]:
    feature_df = year_raw[scenario.feature_year]
    target_df = year_raw[scenario.target_year]

    drop_groups = core.select_group_ids(year=scenario.feature_year, use_drop=True)
    feat_cols, missing_by_group = core.collect_feature_columns(
        merged=merged,
        data_year=scenario.feature_year,
        data_df=feature_df,
        group_ids=drop_groups,
    )

    target_table, target_meta = core.build_target_table_median(
        merged=merged,
        target_year=scenario.target_year,
        target_group_id=scenario.target_group_id,
        target_df=target_df,
    )

    model_df = core.prepare_model_table(
        features_df=feature_df[["student_id"] + feat_cols],
        target_table=target_table,
        feature_cols=feat_cols,
    ).copy()
    model_df["student_id"] = model_df["student_id"].astype(str)

    node_ids = model_df["student_id"].tolist()
    y = model_df["target_class"].astype(int).to_numpy()
    x_raw = model_df[feat_cols].apply(pd.to_numeric, errors="coerce")
    all_na_cols = [c for c in x_raw.columns if x_raw[c].isna().all()]
    if all_na_cols:
        x_raw = x_raw.drop(columns=all_na_cols)
    feat_cols_used = [c for c in feat_cols if c not in set(all_na_cols)]
    if not feat_cols_used:
        raise RuntimeError(f"[{scenario.name}] no usable feature columns after dropping all-NA columns.")

    adj, graph_diag = build_graph_for_nodes(year_edges[scenario.edge_year], node_ids=node_ids)

    payload = {
        "scenario": scenario.name,
        "feature_year": scenario.feature_year,
        "target_year": scenario.target_year,
        "edge_year": scenario.edge_year,
        "target_group_id": scenario.target_group_id,
        "target_meta": target_meta,
        "feat_cols": feat_cols_used,
        "dropped_all_na_features": all_na_cols,
        "missing_by_group": missing_by_group,
        "node_ids": node_ids,
        "x_raw": x_raw,
        "y": y,
        "adj": adj,
        "graph_diag": graph_diag,
    }
    return payload


def run_one_seed(payload: dict[str, Any], seed: int) -> dict[str, Any]:
    set_seed(seed)

    x_raw: pd.DataFrame = payload["x_raw"]
    y: np.ndarray = payload["y"]
    n = len(y)
    all_idx = np.arange(n)

    trval_idx, test_idx = train_test_split(
        all_idx,
        test_size=TEST_SIZE,
        random_state=seed,
        stratify=y,
    )
    tr_idx, val_idx = train_test_split(
        trval_idx,
        test_size=VAL_SIZE_WITHIN_TRAINVAL,
        random_state=seed,
        stratify=y[trval_idx],
    )

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    x_train = imputer.fit_transform(x_raw.iloc[tr_idx])
    scaler.fit(x_train)
    x_all = scaler.transform(imputer.transform(x_raw))

    x_t = torch.tensor(x_all, dtype=torch.float32, device=DEVICE)
    y_t = torch.tensor(y.astype(np.float32), dtype=torch.float32, device=DEVICE)
    adj_t = payload["adj"]

    tr_t = torch.tensor(tr_idx, dtype=torch.long, device=DEVICE)
    val_t = torch.tensor(val_idx, dtype=torch.long, device=DEVICE)
    te_t = torch.tensor(test_idx, dtype=torch.long, device=DEVICE)

    model = GraphSAGE(in_dim=x_t.shape[1], hidden_dim=HIDDEN_DIM, out_dim=1, dropout=DROPOUT).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    criterion = nn.BCEWithLogitsLoss()

    best_state = None
    best_val_loss = math.inf
    best_epoch = -1
    stale = 0

    for epoch in range(1, MAX_EPOCHS + 1):
        model.train()
        optimizer.zero_grad()
        logits = model(x_t, adj_t).squeeze(1)
        loss = criterion(logits[tr_t], y_t[tr_t])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            val_logits = model(x_t, adj_t).squeeze(1)
            val_loss = criterion(val_logits[val_t], y_t[val_t]).item()
        if val_loss < best_val_loss - 1e-8:
            best_val_loss = val_loss
            best_epoch = epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            stale = 0
        else:
            stale += 1
            if stale >= PATIENCE:
                break

    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        logits = model(x_t, adj_t).squeeze(1).cpu().numpy()
    probs = 1.0 / (1.0 + np.exp(-logits))
    pred = (probs >= 0.5).astype(int)

    y_test = y[test_idx]
    p_test = pred[test_idx]
    s_test = probs[test_idx]

    out = {
        "seed": seed,
        "best_epoch": int(best_epoch),
        "n_train": int(len(tr_idx)),
        "n_val": int(len(val_idx)),
        "n_test": int(len(test_idx)),
        "test_accuracy": float(accuracy_score(y_test, p_test)),
        "test_f1": float(f1_score(y_test, p_test, zero_division=0)),
        "test_auc": safe_auc(y_test, s_test),
    }
    return out


def main() -> None:
    ensure_dirs()

    merged_path = core.pick_first_existing_path(core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")

    w2_raw = core.normalize_student_id(pd.read_csv(core.W2_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    w3_raw = core.normalize_student_id(pd.read_csv(core.W3_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    roster = core.load_roster()

    w2_rel_cols = [c for cols in core.W2_RELATION_COLUMNS.values() for c in cols]
    w3_rel_cols = [c for cols in core.W3_RELATION_COLUMNS.values() for c in cols]
    w2_rel_in = w2_raw[["student_id"] + [c for c in w2_rel_cols if c in w2_raw.columns]].copy()
    w3_rel_in = w3_raw[["student_id"] + [c for c in w3_rel_cols if c in w3_raw.columns]].copy()

    w2_edges, w2_edge_diag = core.build_relation_edges(w2_rel_in, core.W2_RELATION_COLUMNS, roster, year_tag="W2")
    w3_edges, w3_edge_diag = core.build_relation_edges(w3_rel_in, core.W3_RELATION_COLUMNS, roster, year_tag="W3")
    w2_edges.to_csv(FEATURE_OUT / "w2_relation_edges_graphsage.csv", index=False, encoding="utf-8-sig")
    w3_edges.to_csv(FEATURE_OUT / "w3_relation_edges_graphsage.csv", index=False, encoding="utf-8-sig")

    year_raw = {"W2": w2_raw, "W3": w3_raw}
    year_edges = {"W2": w2_edges, "W3": w3_edges}

    all_seed_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    task_diagnostics: dict[str, Any] = {
        "edge_build_w2": w2_edge_diag,
        "edge_build_w3": w3_edge_diag,
        "data_paths": {
            "w2": str(core.W2_DATA_PATH),
            "w3": str(core.W3_DATA_PATH),
            "mapping": str(merged_path),
            "basic_info": str(core.BASIC_INFO_PATH),
        },
    }

    for sc in SCENARIOS:
        payload = prepare_task_payload(sc, merged=merged, year_raw=year_raw, year_edges=year_edges)
        seed_metrics = []
        for seed in SEEDS:
            m = run_one_seed(payload, seed=seed)
            row = {"scenario": sc.name, **m}
            all_seed_rows.append(row)
            seed_metrics.append(row)

        sdf = pd.DataFrame(seed_metrics)
        summary_rows.append(
            {
                "scenario": sc.name,
                "feature_year": sc.feature_year,
                "target_year": sc.target_year,
                "edge_year": sc.edge_year,
                "target_group_id": sc.target_group_id,
                "target_median_cutoff": float(payload["target_meta"]["target_median_cutoff"]),
                "target_positive_rate": float(payload["target_meta"]["target_positive_rate"]),
                "n_nodes_modeling": int(len(payload["node_ids"])),
                "n_edges_graph": int(payload["graph_diag"]["n_edges_after_filter"]),
                "edge_density": float(payload["graph_diag"]["edge_density"]),
                "n_features_used": int(len(payload["feat_cols"])),
                "test_accuracy_mean": float(sdf["test_accuracy"].mean()),
                "test_accuracy_std": float(sdf["test_accuracy"].std(ddof=0)),
                "test_f1_mean": float(sdf["test_f1"].mean()),
                "test_f1_std": float(sdf["test_f1"].std(ddof=0)),
                "test_auc_mean": float(sdf["test_auc"].mean(skipna=True)),
                "test_auc_std": float(sdf["test_auc"].std(ddof=0, skipna=True)),
                "best_epoch_mean": float(sdf["best_epoch"].mean()),
                "best_epoch_std": float(sdf["best_epoch"].std(ddof=0)),
            }
        )

        task_diagnostics[sc.name] = {
            "feature_year": sc.feature_year,
            "target_year": sc.target_year,
            "edge_year": sc.edge_year,
            "target_group_id": sc.target_group_id,
            "target_meta": payload["target_meta"],
            "missing_by_group": payload["missing_by_group"],
            "dropped_all_na_features": payload["dropped_all_na_features"],
            "n_nodes_modeling": len(payload["node_ids"]),
            "n_features_used": len(payload["feat_cols"]),
            "graph_diag": payload["graph_diag"],
            "feature_columns": payload["feat_cols"],
        }

    seed_df = pd.DataFrame(all_seed_rows).sort_values(["scenario", "seed"]).reset_index(drop=True)
    summary_df = pd.DataFrame(summary_rows).sort_values("scenario").reset_index(drop=True)

    seed_path = RESULT_OUT / "graphsage_three_tasks_seed_metrics.csv"
    summary_path = RESULT_OUT / "graphsage_three_tasks_summary.csv"
    md_path = RESULT_OUT / "graphsage_three_tasks_summary.md"
    diag_path = DIAG_OUT / "graphsage_three_tasks_diagnostics.json"

    seed_df.to_csv(seed_path, index=False, encoding="utf-8-sig")
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")
    diag_path.write_text(json.dumps(task_diagnostics, ensure_ascii=False, indent=2), encoding="utf-8-sig")

    name_map = {"w2_self": "W2 -> W2", "w3_self": "W3 -> W3", "w2_predict_w3": "W2 -> W3"}
    show = summary_df.copy()
    show["task"] = show["scenario"].map(name_map)
    for c in [
        "test_accuracy_mean",
        "test_accuracy_std",
        "test_f1_mean",
        "test_f1_std",
        "test_auc_mean",
        "test_auc_std",
        "edge_density",
    ]:
        show[c] = show[c].map(lambda v: f"{v:.6f}")
    show["target_median_cutoff"] = show["target_median_cutoff"].map(lambda v: f"{v:.4f}")
    show["target_positive_rate"] = show["target_positive_rate"].map(lambda v: f"{v:.6f}")
    show["best_epoch_mean"] = show["best_epoch_mean"].map(lambda v: f"{v:.2f}")
    show["best_epoch_std"] = show["best_epoch_std"].map(lambda v: f"{v:.2f}")

    lines = []
    lines.append("# GraphSAGE Baseline (Three Tasks)")
    lines.append("")
    lines.append("## Data")
    lines.append(f"- W2: `{core.W2_DATA_PATH}`")
    lines.append(f"- W3: `{core.W3_DATA_PATH}`")
    lines.append(f"- Mapping: `{merged_path}`")
    lines.append(f"- Basic info: `{core.BASIC_INFO_PATH}`")
    lines.append("")
    lines.append("## Graph")
    lines.append("- Edges are built from nomination columns (online/offline friend/enemy).")
    lines.append("- GraphSAGE uses incoming neighbor aggregation with row-normalized sparse adjacency.")
    lines.append("")
    lines.append("## Results (mean/std over 5 seeds)")
    lines.append(
        show[
            [
                "task",
                "test_accuracy_mean",
                "test_accuracy_std",
                "test_f1_mean",
                "test_f1_std",
                "test_auc_mean",
                "test_auc_std",
                "n_nodes_modeling",
                "n_edges_graph",
                "n_features_used",
                "target_median_cutoff",
            ]
        ].to_markdown(index=False)
    )
    lines.append("")
    lines.append("## Output Files")
    lines.append(f"- `{seed_path}`")
    lines.append(f"- `{summary_path}`")
    lines.append(f"- `{diag_path}`")
    lines.append(f"- `{FEATURE_OUT / 'w2_relation_edges_graphsage.csv'}`")
    lines.append(f"- `{FEATURE_OUT / 'w3_relation_edges_graphsage.csv'}`")
    lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")

    print("Done.")
    print("Wrote:", seed_path)
    print("Wrote:", summary_path)
    print("Wrote:", md_path)
    print("Wrote:", diag_path)
    print("Wrote:", FEATURE_OUT / "w2_relation_edges_graphsage.csv")
    print("Wrote:", FEATURE_OUT / "w3_relation_edges_graphsage.csv")


if __name__ == "__main__":
    main()
