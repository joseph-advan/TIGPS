from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
TEST_SIZE = 0.2
LOGIT_CS = np.logspace(-4, 4, 41)
EPS = 1e-9
FULL_NUM_RE = re.compile(r"^\s*[-+]?\d+(?:\.\d+)?\s*$")


@dataclass(frozen=True)
class Scenario:
    name: str
    feature_year: str
    target_year: str
    target_group_id: str


THIS_FILE = Path(__file__).resolve()
OUT_ROOT = THIS_FILE.parent
OUT_FEATURE_DIR = OUT_ROOT / "outputs" / "features"
OUT_MODEL_DIR = OUT_ROOT / "outputs" / "model_results"
OUT_DIAG_DIR = OUT_ROOT / "outputs" / "diagnostics"
BASE_DIR = THIS_FILE.parents[3]

W2_DATA_PATH = BASE_DIR / r"Data\2024data\TIGPS_W2_studentdata_ver12.csv"
W3_DATA_PATH = BASE_DIR / r"Data\2025data\W3_studentdata_ver11.csv"
BASIC_INFO_PATH = BASE_DIR / r"Data\otherData\W2W3_Student_Basic_Info.csv"
MERGED_PATH_CANDIDATES = [
    BASE_DIR / r"Code\EDA\other\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
    BASE_DIR / r"Code\EDA\tying_to_catigoricalize_q\other\merged_question_list_w2_w3.csv",
]

W2_RELATION_COLUMNS = {
    "online_friend": [f"v14_1_0{i}" for i in range(1, 6)],
    "online_enemy": [f"v14_2_0{i}" for i in range(1, 6)],
    "offline_friend": [f"v14_3_0{i}" for i in range(1, 6)],
    "offline_enemy": [f"v14_4_0{i}" for i in range(1, 6)],
}
W3_RELATION_COLUMNS = {
    "online_friend": [f"8-1_{i}" for i in range(0, 5)],
    "online_enemy": [f"8-2_{i}" for i in range(0, 5)],
    "offline_friend": [f"8-3_{i}" for i in range(0, 5)],
    "offline_enemy": [f"8-4_{i}" for i in range(0, 5)],
}

W2_FEATURE_GROUP_IDS = [
    "v57", "v27", "v42", "v6", "v5", "v49", "v38", "v40",
    "v52", "v50", "v28", "v25", "v34", "v19", "v1", "v3",
    "v23", "v36", "v521", "v26", "v54", "v51", "v22",
]
W3_FEATURE_GROUP_IDS = [
    "55", "28", "39", "5", "4", "48", "34", "36",
    "52", "49", "29", "26", "30", "11", "1", "3",
    "59", "25", "32", "51", "27", "53", "50", "24",
]
W2_DROP_GROUP_IDS = {"v57", "v52", "v50", "v51"}
W3_DROP_GROUP_IDS = {"55", "52", "49", "50"}

SCENARIOS = [
    Scenario(name="w2_self", feature_year="W2", target_year="W2", target_group_id="v55"),
    Scenario(name="w3_self", feature_year="W3", target_year="W3", target_group_id="54"),
    Scenario(name="w2_predict_w3", feature_year="W2", target_year="W3", target_group_id="54"),
]


def pick_first_existing_path(candidates: list[Path]) -> Path:
    for p in candidates:
        if p.exists():
            return p
    joined = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(f"No mapping file found. Tried:\n{joined}")


def normalize_student_id(df: pd.DataFrame) -> pd.DataFrame:
    if "student_id" not in df.columns:
        raise KeyError("Column 'student_id' is required.")
    out = df.copy()
    sid = out["student_id"].astype(str).str.strip()
    sid = sid.replace({"": np.nan, "nan": np.nan, "None": np.nan, "<NA>": np.nan})
    out["student_id"] = sid
    return out


def normalize_token(x: Any) -> str:
    if pd.isna(x):
        return ""
    s = str(x).strip()
    if not s:
        return ""
    if FULL_NUM_RE.match(s):
        try:
            n = float(s)
        except Exception:
            return s
        if float(n).is_integer():
            return str(int(n))
        return f"{n:.10f}".rstrip("0").rstrip(".")
    return s


def parse_positive_int(x: Any) -> int | None:
    s = normalize_token(x)
    if not s:
        return None
    try:
        n = int(float(s))
    except Exception:
        return None
    if n <= 0:
        return None
    return n


def load_roster() -> pd.DataFrame:
    roster = pd.read_csv(BASIC_INFO_PATH, low_memory=False, dtype=str, encoding="utf-8-sig")
    roster = normalize_student_id(roster)
    keep = roster[["student_id", "school_id", "class", "v13"]].copy()
    keep["school_id"] = keep["school_id"].map(normalize_token)
    keep["class"] = keep["class"].map(normalize_token)
    keep["seat"] = keep["v13"].map(parse_positive_int)
    keep = keep.drop(columns=["v13"])
    keep = keep.dropna(subset=["student_id"]).drop_duplicates(subset=["student_id"], keep="first")
    return keep


def build_seat_lookup(roster: pd.DataFrame) -> tuple[dict[tuple[str, str, int], str], int]:
    valid = roster.dropna(subset=["seat"]).copy()
    group_counts = (
        valid.groupby(["school_id", "class", "seat"], dropna=False)["student_id"].nunique().reset_index(name="n_sid")
    )
    ambiguous = int((group_counts["n_sid"] > 1).sum())
    unique_keys = group_counts[group_counts["n_sid"] == 1][["school_id", "class", "seat"]].copy()
    merged = unique_keys.merge(valid, on=["school_id", "class", "seat"], how="left")
    merged = merged.drop_duplicates(subset=["school_id", "class", "seat"], keep="first")
    lookup = {
        (str(r["school_id"]), str(r["class"]), int(r["seat"])): str(r["student_id"])
        for _, r in merged.iterrows()
    }
    return lookup, ambiguous


def build_relation_edges(
    relation_df: pd.DataFrame,
    relation_cols: dict[str, list[str]],
    roster: pd.DataFrame,
    year_tag: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    base = relation_df.merge(roster[["student_id", "school_id", "class"]], on="student_id", how="left")
    seat_lookup, ambiguous_keys = build_seat_lookup(roster)
    edges: list[dict[str, Any]] = []

    stat = {
        "year": year_tag,
        "n_students_input": int(base["student_id"].nunique()),
        "n_rows_input": int(len(base)),
        "ambiguous_lookup_keys": ambiguous_keys,
        "raw_nomination_cells": 0,
        "valid_positive_seat_cells": 0,
        "accepted_edges_before_dedup": 0,
        "dropped_invalid_or_empty": 0,
        "dropped_lookup_not_found": 0,
        "dropped_self_nomination": 0,
    }

    for relation_type, cols in relation_cols.items():
        existing = [c for c in cols if c in base.columns]
        for col in existing:
            series = base[col]
            stat["raw_nomination_cells"] += int(series.notna().sum())
            for idx, raw_val in series.items():
                seat = parse_positive_int(raw_val)
                if seat is None:
                    stat["dropped_invalid_or_empty"] += 1
                    continue
                stat["valid_positive_seat_cells"] += 1

                row = base.loc[idx]
                src = row["student_id"]
                school_id = normalize_token(row.get("school_id", ""))
                class_id = normalize_token(row.get("class", ""))
                if not src or not school_id or not class_id:
                    stat["dropped_lookup_not_found"] += 1
                    continue
                dst = seat_lookup.get((school_id, class_id, seat))
                if not dst:
                    stat["dropped_lookup_not_found"] += 1
                    continue
                if dst == src:
                    stat["dropped_self_nomination"] += 1
                    continue
                stat["accepted_edges_before_dedup"] += 1
                edges.append(
                    {
                        "year": year_tag,
                        "student_id_src": src,
                        "student_id_dst": dst,
                        "relation_type": relation_type,
                        "source_column": col,
                        "nominated_seat": seat,
                        "school_id": school_id,
                        "class": class_id,
                    }
                )

    edge_df = pd.DataFrame(edges)
    if edge_df.empty:
        edge_df = pd.DataFrame(
            columns=[
                "year",
                "student_id_src",
                "student_id_dst",
                "relation_type",
                "source_column",
                "nominated_seat",
                "school_id",
                "class",
            ]
        )
    dedup_df = edge_df.drop_duplicates(subset=["year", "student_id_src", "student_id_dst", "relation_type"], keep="first")
    stat["accepted_edges_after_dedup"] = int(len(dedup_df))
    stat["dedup_removed"] = int(len(edge_df) - len(dedup_df))
    return dedup_df, stat


def safe_ratio(a: pd.Series, b: pd.Series) -> pd.Series:
    return a / (b + EPS)


def _dict_of_sets(group: pd.core.groupby.generic.DataFrameGroupBy, value_col: str) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for k, g in group:
        out[str(k)] = set(g[value_col].astype(str))
    return out


def build_interpersonal_features(
    roster: pd.DataFrame,
    edge_df: pd.DataFrame,
    year_tag: str,
) -> tuple[pd.DataFrame, list[str]]:
    students = roster[["student_id", "school_id", "class"]].drop_duplicates(subset=["student_id"], keep="first").copy()
    rel_types = ["online_friend", "online_enemy", "offline_friend", "offline_enemy"]

    for rel in rel_types:
        sub = edge_df[edge_df["relation_type"] == rel]
        out_count = sub.groupby("student_id_src").size().rename(f"ip_out_{rel}")
        in_count = sub.groupby("student_id_dst").size().rename(f"ip_in_{rel}")
        students = students.merge(out_count, left_on="student_id", right_index=True, how="left")
        students = students.merge(in_count, left_on="student_id", right_index=True, how="left")

    for c in [c for c in students.columns if c.startswith("ip_")]:
        students[c] = students[c].fillna(0.0).astype(float)

    students["ip_out_friend_total"] = students["ip_out_online_friend"] + students["ip_out_offline_friend"]
    students["ip_out_enemy_total"] = students["ip_out_online_enemy"] + students["ip_out_offline_enemy"]
    students["ip_in_friend_total"] = students["ip_in_online_friend"] + students["ip_in_offline_friend"]
    students["ip_in_enemy_total"] = students["ip_in_online_enemy"] + students["ip_in_offline_enemy"]

    students["ip_sent_like_ratio"] = safe_ratio(students["ip_out_friend_total"], students["ip_out_friend_total"] + students["ip_out_enemy_total"])
    students["ip_received_like_ratio"] = safe_ratio(students["ip_in_friend_total"], students["ip_in_friend_total"] + students["ip_in_enemy_total"])
    students["ip_sent_net"] = students["ip_out_friend_total"] - students["ip_out_enemy_total"]
    students["ip_received_net"] = students["ip_in_friend_total"] - students["ip_in_enemy_total"]

    students["ip_out_friend_online_minus_offline"] = students["ip_out_online_friend"] - students["ip_out_offline_friend"]
    students["ip_out_enemy_online_minus_offline"] = students["ip_out_online_enemy"] - students["ip_out_offline_enemy"]
    students["ip_in_friend_online_minus_offline"] = students["ip_in_online_friend"] - students["ip_in_offline_friend"]
    students["ip_in_enemy_online_minus_offline"] = students["ip_in_online_enemy"] - students["ip_in_offline_enemy"]

    class_size = (
        roster.groupby(["school_id", "class"], dropna=False)["student_id"]
        .nunique()
        .rename("ip_class_size")
        .reset_index()
    )
    students = students.merge(class_size, on=["school_id", "class"], how="left")
    students["ip_class_size"] = students["ip_class_size"].fillna(1).astype(float)
    students["ip_class_size_minus1"] = (students["ip_class_size"] - 1.0).clip(lower=1.0)

    count_cols = [c for c in students.columns if c.startswith("ip_in_") or c.startswith("ip_out_")]
    count_cols = [c for c in count_cols if students[c].dtype.kind in "if" and not c.endswith("ratio")]
    for c in count_cols:
        students[f"{c}_rate_class"] = students[c] / students["ip_class_size_minus1"]

    friend_out = edge_df[edge_df["relation_type"].isin(["online_friend", "offline_friend"])]
    enemy_out = edge_df[edge_df["relation_type"].isin(["online_enemy", "offline_enemy"])]
    friend_in = friend_out.rename(columns={"student_id_src": "student_id_dst", "student_id_dst": "student_id_src"})
    enemy_in = enemy_out.rename(columns={"student_id_src": "student_id_dst", "student_id_dst": "student_id_src"})

    out_friend_targets = _dict_of_sets(friend_out.groupby("student_id_src"), "student_id_dst")
    out_enemy_targets = _dict_of_sets(enemy_out.groupby("student_id_src"), "student_id_dst")
    in_friend_sources = _dict_of_sets(friend_in.groupby("student_id_src"), "student_id_dst")
    in_enemy_sources = _dict_of_sets(enemy_in.groupby("student_id_src"), "student_id_dst")

    recip_friend = []
    recip_enemy = []
    liked_but_enemy = []
    enemy_but_liked = []
    mixed_out = []
    for sid in students["student_id"].astype(str):
        of = out_friend_targets.get(sid, set())
        oe = out_enemy_targets.get(sid, set())
        inf = in_friend_sources.get(sid, set())
        ine = in_enemy_sources.get(sid, set())
        recip_friend.append(float(len(of & inf)))
        recip_enemy.append(float(len(oe & ine)))
        liked_but_enemy.append(float(len(of & ine)))
        enemy_but_liked.append(float(len(oe & inf)))
        mixed_out.append(float(len(of & oe)))

    students["ip_reciprocal_friend_count"] = recip_friend
    students["ip_reciprocal_enemy_count"] = recip_enemy
    students["ip_liked_by_me_but_enemy_to_me_count"] = liked_but_enemy
    students["ip_enemy_by_me_but_likes_me_count"] = enemy_but_liked
    students["ip_same_target_friend_and_enemy_count"] = mixed_out
    for c in [
        "ip_reciprocal_friend_count",
        "ip_reciprocal_enemy_count",
        "ip_liked_by_me_but_enemy_to_me_count",
        "ip_enemy_by_me_but_likes_me_count",
        "ip_same_target_friend_and_enemy_count",
    ]:
        students[f"{c}_rate_class"] = students[c] / students["ip_class_size_minus1"]

    students["year"] = year_tag
    students = students.sort_values(["school_id", "class", "student_id"]).reset_index(drop=True)
    feature_cols = [c for c in students.columns if c.startswith("ip_")]
    return students[["student_id"] + feature_cols].copy(), feature_cols


def resolve_group_items(merged: pd.DataFrame, year: str, group_id: str) -> list[str]:
    sub = merged[
        (merged["Year"].astype(str).str.strip() == str(year).strip())
        & (merged["Group_ID"].astype(str).str.strip() == str(group_id).strip())
    ]
    return sub["Question_ID"].dropna().astype(str).str.strip().tolist()


def candidate_item_names(item: str) -> list[str]:
    out = [item]
    if "-" in item:
        out.append(item.replace("-", "_"))
    if "_" in item:
        out.append(item.replace("_", "-"))
    return list(dict.fromkeys(out))


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


def collect_feature_columns(
    merged: pd.DataFrame,
    data_year: str,
    data_df: pd.DataFrame,
    group_ids: list[str],
) -> tuple[list[str], dict[str, list[str]]]:
    feature_cols: list[str] = []
    missing_by_group: dict[str, list[str]] = {}
    seen: set[str] = set()
    for gid in group_ids:
        items = resolve_group_items(merged=merged, year=data_year, group_id=gid)
        found, missing = resolve_existing_items(data_df, items)
        if missing:
            missing_by_group[gid] = missing
        for c in found:
            if c not in seen:
                feature_cols.append(c)
                seen.add(c)
    return feature_cols, missing_by_group


def build_target_table_median(
    merged: pd.DataFrame,
    target_year: str,
    target_group_id: str,
    target_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    target_items = resolve_group_items(merged=merged, year=target_year, group_id=target_group_id)
    target_cols, missing = resolve_existing_items(target_df, target_items)
    if not target_cols:
        raise ValueError(f"No target columns found for year={target_year}, group_id={target_group_id}.")
    mat = target_df[target_cols].apply(pd.to_numeric, errors="coerce")
    score = mat.sum(axis=1, min_count=1)
    valid_score = score.dropna()
    if valid_score.empty:
        raise ValueError(f"Target score is empty after numeric conversion for {target_year}-{target_group_id}.")
    cutoff = float(valid_score.median())
    target_class = (score >= cutoff).astype(float)
    target_class[score.isna()] = np.nan
    out = pd.DataFrame(
        {
            "student_id": target_df["student_id"].astype(str),
            "target_score_sum": score,
            "target_class": target_class,
        }
    )
    dist = target_class.dropna().astype(int).value_counts().sort_index().to_dict()
    meta = {
        "target_items_resolved": target_cols,
        "target_items_missing": missing,
        "target_median_cutoff": cutoff,
        "target_class_distribution": dist,
        "target_positive_rate": float(target_class.dropna().mean()),
    }
    return out, meta


def prepare_model_table(
    features_df: pd.DataFrame,
    target_table: pd.DataFrame,
    feature_cols: list[str],
) -> pd.DataFrame:
    out = features_df[["student_id"] + feature_cols].merge(target_table, on="student_id", how="inner")
    out = out.drop_duplicates(subset=["student_id"], keep="first").copy()
    out = out.dropna(subset=["target_class"]).copy()
    return out


def run_logistic_binary(
    model_df: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[dict[str, Any], Pipeline | None, pd.DataFrame | None, pd.Series | None]:
    if model_df.empty:
        return {"skipped_reason": "empty_model_df"}, None, None, None

    x_full = model_df[feature_cols].apply(pd.to_numeric, errors="coerce")
    non_empty_features = [c for c in x_full.columns if x_full[c].notna().any()]
    dropped_all_missing = [c for c in feature_cols if c not in non_empty_features]
    if not non_empty_features:
        return {"skipped_reason": "all_features_missing", "dropped_all_missing_feature_cols": dropped_all_missing}, None, None, None

    x = x_full[non_empty_features]
    y = model_df["target_class"].astype(float)
    if y.nunique(dropna=True) < 2:
        return {"skipped_reason": "target_not_binary", "dropped_all_missing_feature_cols": dropped_all_missing}, None, None, None

    stratify = y if y.nunique(dropna=True) == 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=stratify
    )

    tune_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegressionCV(
                    Cs=LOGIT_CS,
                    cv=5,
                    scoring="roc_auc",
                    max_iter=3000,
                    n_jobs=1,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )
    tune_pipe.fit(x_train, y_train)
    best_c = float(tune_pipe.named_steps["model"].C_[0])

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(C=best_c, max_iter=3000, n_jobs=1, random_state=RANDOM_STATE)),
        ]
    )
    model.fit(x_train, y_train)

    y_train_pred = model.predict(x_train)
    y_test_pred = model.predict(x_test)
    y_train_prob = model.predict_proba(x_train)[:, 1]
    y_test_prob = model.predict_proba(x_test)[:, 1]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_validate(
        model, x, y, cv=cv, scoring=["accuracy", "f1", "roc_auc"], n_jobs=1, return_train_score=False
    )

    metrics: dict[str, Any] = {
        "n_rows_modeling": int(len(model_df)),
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "n_features_requested": int(len(feature_cols)),
        "n_features_used": int(len(non_empty_features)),
        "dropped_all_missing_feature_cols": dropped_all_missing,
        "c_selected": best_c,
        "train_accuracy": float(accuracy_score(y_train, y_train_pred)),
        "train_f1": float(f1_score(y_train, y_train_pred, zero_division=0)),
        "train_auc": float(roc_auc_score(y_train, y_train_prob)),
        "test_accuracy": float(accuracy_score(y_test, y_test_pred)),
        "test_f1": float(f1_score(y_test, y_test_pred, zero_division=0)),
        "test_auc": float(roc_auc_score(y_test, y_test_prob)),
        "cv5_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
        "cv5_accuracy_std": float(np.std(cv_scores["test_accuracy"])),
        "cv5_f1_mean": float(np.mean(cv_scores["test_f1"])),
        "cv5_f1_std": float(np.std(cv_scores["test_f1"])),
        "cv5_auc_mean": float(np.mean(cv_scores["test_roc_auc"])),
        "cv5_auc_std": float(np.std(cv_scores["test_roc_auc"])),
    }
    return metrics, model, x_test, y_test


def select_group_ids(year: str, use_drop: bool) -> list[str]:
    if year == "W2":
        return [g for g in W2_FEATURE_GROUP_IDS if (g not in W2_DROP_GROUP_IDS or not use_drop)]
    if year == "W3":
        return [g for g in W3_FEATURE_GROUP_IDS if (g not in W3_DROP_GROUP_IDS or not use_drop)]
    raise ValueError(f"Unsupported year: {year}")


def build_interpersonal_augmented_tables(
    w2_raw: pd.DataFrame,
    w3_raw: pd.DataFrame,
    roster: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any], list[str], list[str]]:
    w2_rel_cols = [c for cols in W2_RELATION_COLUMNS.values() for c in cols]
    w3_rel_cols = [c for cols in W3_RELATION_COLUMNS.values() for c in cols]

    w2_relation_input = w2_raw[["student_id"] + [c for c in w2_rel_cols if c in w2_raw.columns]].copy()
    w3_relation_input = w3_raw[["student_id"] + [c for c in w3_rel_cols if c in w3_raw.columns]].copy()

    w2_edges, w2_diag = build_relation_edges(w2_relation_input, W2_RELATION_COLUMNS, roster, year_tag="W2")
    w3_edges, w3_diag = build_relation_edges(w3_relation_input, W3_RELATION_COLUMNS, roster, year_tag="W3")

    w2_feats, w2_feat_cols = build_interpersonal_features(roster=roster, edge_df=w2_edges, year_tag="W2")
    w3_feats, w3_feat_cols = build_interpersonal_features(roster=roster, edge_df=w3_edges, year_tag="W3")

    OUT_FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    w2_edges.to_csv(OUT_FEATURE_DIR / "w2_relation_edges.csv", index=False, encoding="utf-8-sig")
    w3_edges.to_csv(OUT_FEATURE_DIR / "w3_relation_edges.csv", index=False, encoding="utf-8-sig")
    w2_feats.to_csv(OUT_FEATURE_DIR / "interpersonal_features_w2.csv", index=False, encoding="utf-8-sig")
    w3_feats.to_csv(OUT_FEATURE_DIR / "interpersonal_features_w3.csv", index=False, encoding="utf-8-sig")

    diagnostics = {
        "w2_relation_build": w2_diag,
        "w3_relation_build": w3_diag,
        "n_interpersonal_features_w2": len(w2_feat_cols),
        "n_interpersonal_features_w3": len(w3_feat_cols),
        "w2_relation_columns_found": [c for c in w2_rel_cols if c in w2_raw.columns],
        "w3_relation_columns_found": [c for c in w3_rel_cols if c in w3_raw.columns],
    }
    return w2_feats, w3_feats, diagnostics, w2_feat_cols, w3_feat_cols


def row_to_md_table(df: pd.DataFrame) -> str:
    out = df.copy()
    for c in out.columns:
        if out[c].dtype.kind in "if":
            out[c] = out[c].map(lambda x: f"{x:.6f}")
    return out.to_markdown(index=False)


def main() -> None:
    OUT_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIAG_DIR.mkdir(parents=True, exist_ok=True)

    merged_path = pick_first_existing_path(MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")

    w2_raw = normalize_student_id(pd.read_csv(W2_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    w3_raw = normalize_student_id(pd.read_csv(W3_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    roster = load_roster()

    w2_feats, w3_feats, diagnostics, w2_ip_cols, w3_ip_cols = build_interpersonal_augmented_tables(w2_raw, w3_raw, roster)
    year_to_raw = {"W2": w2_raw, "W3": w3_raw}
    year_to_ip = {"W2": w2_feats, "W3": w3_feats}
    year_to_ip_cols = {"W2": w2_ip_cols, "W3": w3_ip_cols}

    rows: list[dict[str, Any]] = []
    detail_records: list[dict[str, Any]] = []
    perm_records: list[dict[str, Any]] = []

    settings = [
        {"name": "baseline_no_drop", "use_drop": False, "use_interpersonal": False, "interpersonal_only": False},
        {"name": "baseline_drop", "use_drop": True, "use_interpersonal": False, "interpersonal_only": False},
        {"name": "baseline_no_drop_plus_interpersonal", "use_drop": False, "use_interpersonal": True, "interpersonal_only": False},
        {"name": "baseline_drop_plus_interpersonal", "use_drop": True, "use_interpersonal": True, "interpersonal_only": False},
        {"name": "interpersonal_only", "use_drop": False, "use_interpersonal": True, "interpersonal_only": True},
    ]

    for scenario in SCENARIOS:
        target_df = year_to_raw[scenario.target_year]
        target_table, target_meta = build_target_table_median(
            merged=merged,
            target_year=scenario.target_year,
            target_group_id=scenario.target_group_id,
            target_df=target_df,
        )

        feature_df = year_to_raw[scenario.feature_year]
        base_groups = select_group_ids(year=scenario.feature_year, use_drop=False)
        drop_groups = select_group_ids(year=scenario.feature_year, use_drop=True)
        base_cols_no_drop, missing_no_drop = collect_feature_columns(
            merged=merged, data_year=scenario.feature_year, data_df=feature_df, group_ids=base_groups
        )
        base_cols_drop, missing_drop = collect_feature_columns(
            merged=merged, data_year=scenario.feature_year, data_df=feature_df, group_ids=drop_groups
        )
        ip_df = year_to_ip[scenario.feature_year]
        ip_cols = year_to_ip_cols[scenario.feature_year]

        for st in settings:
            if st["interpersonal_only"]:
                chosen_cols = ip_cols.copy()
                feature_table = ip_df.copy()
                missing_map = {}
            else:
                if st["use_drop"]:
                    chosen_cols = base_cols_drop.copy()
                    missing_map = missing_drop
                else:
                    chosen_cols = base_cols_no_drop.copy()
                    missing_map = missing_no_drop
                feature_table = feature_df[["student_id"] + chosen_cols].copy()
                if st["use_interpersonal"]:
                    feature_table = feature_table.merge(ip_df[["student_id"] + ip_cols], on="student_id", how="left")
                    chosen_cols = chosen_cols + ip_cols

            model_df = prepare_model_table(features_df=feature_table, target_table=target_table, feature_cols=chosen_cols)
            metrics, model, x_test, y_test = run_logistic_binary(model_df=model_df, feature_cols=chosen_cols)
            row = {
                "scenario": scenario.name,
                "setting": st["name"],
                "feature_year": scenario.feature_year,
                "target_year": scenario.target_year,
                "target_group_id": scenario.target_group_id,
                "target_median_cutoff": target_meta["target_median_cutoff"],
                "target_positive_rate": target_meta["target_positive_rate"],
                "n_interpersonal_features_available": len(ip_cols),
                "n_base_features_no_drop": len(base_cols_no_drop),
                "n_base_features_drop": len(base_cols_drop),
                **metrics,
            }
            rows.append(row)
            detail_records.append(
                {
                    "scenario": scenario.name,
                    "setting": st["name"],
                    "target_meta": target_meta,
                    "missing_by_group": missing_map,
                    "metrics": metrics,
                    "feature_columns_used": chosen_cols,
                }
            )

            if model is not None and x_test is not None and y_test is not None and st["use_interpersonal"]:
                cols_for_perm = [c for c in x_test.columns if c.startswith("ip_")]
                if cols_for_perm:
                    perm = permutation_importance(
                        estimator=model,
                        X=x_test,
                        y=y_test,
                        n_repeats=20,
                        random_state=RANDOM_STATE,
                        scoring="roc_auc",
                        n_jobs=1,
                    )
                    for i, c in enumerate(x_test.columns):
                        if c not in cols_for_perm:
                            continue
                        perm_records.append(
                            {
                                "scenario": scenario.name,
                                "setting": st["name"],
                                "feature": c,
                                "importance_mean": float(perm.importances_mean[i]),
                                "importance_std": float(perm.importances_std[i]),
                            }
                        )

    summary_df = pd.DataFrame(rows).sort_values(["scenario", "setting"]).reset_index(drop=True)
    summary_df.to_csv(
        OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    with (OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_details.json").open("w", encoding="utf-8-sig") as f:
        json.dump(
            {
                "data_paths": {
                    "w2_data_path": str(W2_DATA_PATH),
                    "w3_data_path": str(W3_DATA_PATH),
                    "basic_info_path": str(BASIC_INFO_PATH),
                    "mapping_path": str(merged_path),
                },
                "relation_diagnostics": diagnostics,
                "records": detail_records,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    perm_df = pd.DataFrame(perm_records)
    if not perm_df.empty:
        perm_df = perm_df.sort_values(["scenario", "setting", "importance_mean"], ascending=[True, True, False]).reset_index(drop=True)
    perm_df.to_csv(OUT_MODEL_DIR / "interpersonal_permutation_importance.csv", index=False, encoding="utf-8-sig")

    md_lines: list[str] = []
    md_lines.append("# Logistic Baseline + Interpersonal Features (Median Split)")
    md_lines.append("")
    md_lines.append("## Data")
    md_lines.append(f"- W2: `{W2_DATA_PATH}`")
    md_lines.append(f"- W3: `{W3_DATA_PATH}`")
    md_lines.append(f"- Basic roster: `{BASIC_INFO_PATH}`")
    md_lines.append(f"- Mapping: `{merged_path}`")
    md_lines.append("")
    md_lines.append("## Interpersonal Feature Engineering")
    md_lines.append("- Relations used: online_friend / online_enemy / offline_friend / offline_enemy (5 nomination slots each year).")
    md_lines.append("- Nominee mapping key: `(school_id, class, seat)` via `W2W3_Student_Basic_Info.csv`.")
    md_lines.append("- Features include in/out counts, ratios, net scores, online-offline deltas, reciprocity/conflict, and class-normalized rates.")
    md_lines.append("")
    md_lines.append("### Edge Build Diagnostics")
    md_lines.append(row_to_md_table(pd.DataFrame([diagnostics["w2_relation_build"], diagnostics["w3_relation_build"]])))
    md_lines.append("")
    md_lines.append("## Model Comparison Summary")
    show_cols = [
        "scenario", "setting", "test_accuracy", "test_f1", "test_auc",
        "cv5_accuracy_mean", "cv5_f1_mean", "cv5_auc_mean", "n_features_used", "n_rows_modeling",
    ]
    md_lines.append(row_to_md_table(summary_df[show_cols]))
    md_lines.append("")
    if not perm_df.empty:
        md_lines.append("## Top Interpersonal Features by Permutation Importance (AUC)")
        top_perm = (
            perm_df.sort_values(["scenario", "setting", "importance_mean"], ascending=[True, True, False])
            .groupby(["scenario", "setting"], as_index=False)
            .head(10)
            .reset_index(drop=True)
        )
        md_lines.append(row_to_md_table(top_perm))
        md_lines.append("")

    (OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_summary.md").write_text(
        "\n".join(md_lines) + "\n", encoding="utf-8-sig"
    )
    (OUT_DIAG_DIR / "feature_generation_diagnostics.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8-sig"
    )

    print("Done.")
    print("Wrote:", OUT_FEATURE_DIR / "interpersonal_features_w2.csv")
    print("Wrote:", OUT_FEATURE_DIR / "interpersonal_features_w3.csv")
    print("Wrote:", OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_summary.csv")
    print("Wrote:", OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_summary.md")
    print("Wrote:", OUT_MODEL_DIR / "logistic_median_split_interpersonal_comparison_details.json")
    print("Wrote:", OUT_MODEL_DIR / "interpersonal_permutation_importance.csv")
    print("Wrote:", OUT_DIAG_DIR / "feature_generation_diagnostics.json")


if __name__ == "__main__":
    main()
