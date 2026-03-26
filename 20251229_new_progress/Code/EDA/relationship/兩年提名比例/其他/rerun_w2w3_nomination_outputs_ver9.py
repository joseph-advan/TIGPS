from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel, wilcoxon
from statsmodels.stats.multitest import multipletests


BASE_DIR = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship\兩年提名比例"
)
W2_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver9.csv"
)
W3_PATH = Path(
    r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver9.csv"
)

# W3 ver9 does not carry explicit school/class columns.
# We recover them by student_id mapping from W2 (validated 7045/7045 overlap).
OUT_DIR = BASE_DIR / "ver9_rerun_20260326"
SUFFIX = "ver9rerun_20260326"


W2_NOM_COLS = {
    "online_friend": ["v14_1_01", "v14_1_02", "v14_1_03", "v14_1_04", "v14_1_05"],
    "online_enemy": ["v14_2_01", "v14_2_02", "v14_2_03", "v14_2_04", "v14_2_05"],
    "offline_friend": ["v14_3_01", "v14_3_02", "v14_3_03", "v14_3_04", "v14_3_05"],
    "offline_enemy": ["v14_4_01", "v14_4_02", "v14_4_03", "v14_4_04", "v14_4_05"],
}

W3_NOM_COLS = {
    "online_friend": ["8-1_0", "8-1_1", "8-1_2", "8-1_3", "8-1_4"],
    "online_enemy": ["8-2_0", "8-2_1", "8-2_2", "8-2_3", "8-2_4"],
    "offline_friend": ["8-3_0", "8-3_1", "8-3_2", "8-3_3", "8-3_4"],
    "offline_enemy": ["8-4_0", "8-4_1", "8-4_2", "8-4_3", "8-4_4"],
}

FEATURES = [
    "out_online_friend",
    "in_online_friend",
    "out_online_enemy",
    "in_online_enemy",
    "out_offline_friend",
    "in_offline_friend",
    "out_offline_enemy",
    "in_offline_enemy",
]

FEATURE_ZH = {
    "out_online_friend": "提名線上朋友",
    "in_online_friend": "被提名線上朋友",
    "out_online_enemy": "提名線上敵人",
    "in_online_enemy": "被提名線上敵人",
    "out_offline_friend": "提名線下朋友",
    "in_offline_friend": "被提名線下朋友",
    "out_offline_enemy": "提名線下敵人",
    "in_offline_enemy": "被提名線下敵人",
}

BUCKETS = ["0", "1", "2", "3", "4", "5", "6-10", "11+"]


@dataclass
class WaveContext:
    wave: str
    df_raw: pd.DataFrame
    df_roster: pd.DataFrame
    nom_cols: Dict[str, List[str]]
    seat_col_name: str
    seat_output_col_name: str


def norm_key_part(v: object) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if s == "":
        return ""
    try:
        f = float(s)
        if np.isfinite(f) and f.is_integer():
            return str(int(f))
    except Exception:
        pass
    return s


def parse_positive_seat(v: object) -> int | None:
    if pd.isna(v):
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        f = float(s)
    except Exception:
        return None
    if not np.isfinite(f):
        return None
    iv = int(f)
    if iv <= 0:
        return None
    return iv


def build_w2_roster(w2_df: pd.DataFrame) -> pd.DataFrame:
    out = w2_df[["student_id", "school_id", "class", "v13"]].copy()
    out = out.rename(columns={"v13": "seat"})
    return out


def build_w3_roster(w3_df: pd.DataFrame, w2_roster: pd.DataFrame) -> pd.DataFrame:
    w2_meta = w2_roster[["student_id", "school_id", "class"]].copy()
    w2_meta["student_id"] = w2_meta["student_id"].astype(str)
    w3_tmp = w3_df[["student_id", "7"]].copy()
    w3_tmp["student_id"] = w3_tmp["student_id"].astype(str)
    out = w3_tmp.merge(w2_meta, on="student_id", how="left", validate="1:1")
    miss = out["school_id"].isna().sum()
    if miss:
        raise ValueError(f"W3 student_id not found in W2 mapping: {miss}")
    out = out.rename(columns={"7": "seat"})
    out = out[["student_id", "school_id", "class", "seat"]]
    return out


def build_roster_map(df_roster: pd.DataFrame) -> Dict[Tuple[str, str, str], List[str]]:
    d: Dict[Tuple[str, str, str], List[str]] = {}
    for row in df_roster.itertuples(index=False):
        k = (
            norm_key_part(row.school_id),
            norm_key_part(row._2),
            norm_key_part(row.seat),
        )
        d.setdefault(k, []).append(str(row.student_id))
    return d


def build_student_meta(df_roster: pd.DataFrame) -> Dict[str, Dict[str, object]]:
    m: Dict[str, Dict[str, object]] = {}
    for row in df_roster.itertuples(index=False):
        m[str(row.student_id)] = {
            "school_id": row.school_id,
            "class": row._2,
            "seat": row.seat,
        }
    return m


def extract_edges_and_unmatched(ctx: WaveContext) -> Tuple[pd.DataFrame, pd.DataFrame]:
    roster_map = build_roster_map(ctx.df_roster)
    student_meta = build_student_meta(ctx.df_roster)

    edges = []
    unmatched = []

    for row in ctx.df_raw.to_dict(orient="records"):
        sid = str(row.get("student_id"))
        meta = student_meta.get(sid)
        if meta is None:
            continue

        school_id = meta["school_id"]
        class_val = meta["class"]
        nominator_seat = parse_positive_seat(meta["seat"])

        for nom_type, cols in ctx.nom_cols.items():
            for col in cols:
                raw_v = row.get(col)
                seat = parse_positive_seat(raw_v)
                if seat is None:
                    continue

                key = (norm_key_part(school_id), norm_key_part(class_val), str(seat))
                cand = roster_map.get(key, [])
                if len(cand) == 1:
                    edges.append(
                        {
                            "wave": ctx.wave,
                            "nominator_student_id": sid,
                            "target_student_id": cand[0],
                            "nomination_type": nom_type,
                            "nomination_column": col,
                            "nominated_raw": raw_v,
                            "nominated_seat": seat,
                            "school_id": school_id,
                            "class": class_val,
                            "nominator_seat": nominator_seat,
                        }
                    )
                else:
                    reason = "not_in_list" if len(cand) == 0 else "ambiguous_duplicate_seat"
                    unmatched.append(
                        {
                            "wave": ctx.wave,
                            "nominator_student_id": sid,
                            "school_id": school_id,
                            "class": class_val,
                            "nominator_seat": nominator_seat,
                            "nomination_type": nom_type,
                            "nomination_column": col,
                            "nominated_raw": raw_v,
                            "nominated_seat": seat,
                            "reason": reason,
                        }
                    )

    return pd.DataFrame(edges), pd.DataFrame(unmatched)


def build_8features(ctx: WaveContext, edges_df: pd.DataFrame) -> pd.DataFrame:
    base = ctx.df_roster[["student_id", "school_id", "class", "seat"]].copy()
    base = base.rename(columns={"seat": ctx.seat_output_col_name})
    for f in FEATURES:
        base[f"{ctx.wave}_{f}"] = 0

    if edges_df.empty:
        return base

    out_map = {
        "online_friend": f"{ctx.wave}_out_online_friend",
        "online_enemy": f"{ctx.wave}_out_online_enemy",
        "offline_friend": f"{ctx.wave}_out_offline_friend",
        "offline_enemy": f"{ctx.wave}_out_offline_enemy",
    }
    in_map = {
        "online_friend": f"{ctx.wave}_in_online_friend",
        "online_enemy": f"{ctx.wave}_in_online_enemy",
        "offline_friend": f"{ctx.wave}_in_offline_friend",
        "offline_enemy": f"{ctx.wave}_in_offline_enemy",
    }

    for nom_type, col_name in out_map.items():
        s = (
            edges_df.loc[edges_df["nomination_type"] == nom_type]
            .groupby("nominator_student_id")
            .size()
        )
        if not s.empty:
            base[col_name] = base["student_id"].map(s).fillna(0).astype(int)

    for nom_type, col_name in in_map.items():
        s = (
            edges_df.loc[edges_df["nomination_type"] == nom_type]
            .groupby("target_student_id")
            .size()
        )
        if not s.empty:
            base[col_name] = base["student_id"].map(s).fillna(0).astype(int)

    return base


def pct(count: int, n: int) -> float:
    return (count / n * 100.0) if n else np.nan


def calc_bucket(v: int) -> str:
    if v == 0:
        return "0"
    if v == 1:
        return "1"
    if v == 2:
        return "2"
    if v == 3:
        return "3"
    if v == 4:
        return "4"
    if v == 5:
        return "5"
    if 6 <= v <= 10:
        return "6-10"
    return "11+"


def to_float(x: Iterable[object]) -> np.ndarray:
    return pd.to_numeric(pd.Series(list(x)), errors="coerce").astype(float).to_numpy()


def safe_wilcoxon(delta: np.ndarray) -> Tuple[float, float]:
    nz = delta[np.isfinite(delta)]
    if nz.size == 0:
        return np.nan, np.nan
    if np.allclose(nz, 0):
        return np.nan, np.nan
    stat, p = wilcoxon(nz)
    return float(stat), float(p)


def safe_ttest(w2: np.ndarray, w3: np.ndarray) -> Tuple[float, float]:
    stat, p = ttest_rel(w3, w2, nan_policy="omit")
    if np.isnan(stat):
        return np.nan, np.nan
    return float(stat), float(p)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    w2_raw = pd.read_csv(W2_PATH, low_memory=False)
    w3_raw = pd.read_csv(W3_PATH, low_memory=False)

    w2_roster = build_w2_roster(w2_raw)
    w3_roster = build_w3_roster(w3_raw, w2_roster)

    ctx_w2 = WaveContext("W2", w2_raw, w2_roster, W2_NOM_COLS, "v13", "v13")
    ctx_w3 = WaveContext("W3", w3_raw, w3_roster, W3_NOM_COLS, "7", "7")

    w2_edges, w2_unmatched = extract_edges_and_unmatched(ctx_w2)
    w3_edges, w3_unmatched = extract_edges_and_unmatched(ctx_w3)

    # 00
    p00_w2 = OUT_DIR / f"00_W2_nominated_not_in_list_{SUFFIX}.csv"
    p00_w3 = OUT_DIR / f"00_W3_nominated_not_in_list_{SUFFIX}.csv"
    w2_unmatched.to_csv(p00_w2, index=False, encoding="utf-8-sig")
    w3_unmatched.to_csv(p00_w3, index=False, encoding="utf-8-sig")

    # 01
    w2_feat = build_8features(ctx_w2, w2_edges)
    w3_feat = build_8features(ctx_w3, w3_edges)
    p01_w2 = OUT_DIR / f"01_W2_student_8features_{SUFFIX}.csv"
    p01_w3 = OUT_DIR / f"01_W3_student_8features_{SUFFIX}.csv"
    w2_feat.to_csv(p01_w2, index=False, encoding="utf-8-sig")
    w3_feat.to_csv(p01_w3, index=False, encoding="utf-8-sig")

    # join for 02/03
    merged = w2_feat.merge(
        w3_feat[
            [
                "student_id",
                "school_id",
                "class",
                "7",
            ]
            + [f"W3_{f}" for f in FEATURES]
        ],
        on="student_id",
        how="inner",
        suffixes=("_w2", "_w3"),
        validate="1:1",
    )
    if len(merged) != len(w2_feat):
        raise ValueError("W2/W3 merge is not complete by student_id")

    merged["school_id"] = merged["school_id_w2"]
    merged["class"] = merged["class_w2"]
    merged["v13"] = merged["v13"]
    merged["7"] = merged["7"]

    out_cols = ["student_id", "school_id", "class", "v13", "7"]
    for f in FEATURES:
        merged[f"delta_{f}"] = merged[f"W3_{f}"] - merged[f"W2_{f}"]
        out_cols.extend([f"W2_{f}", f"W3_{f}", f"delta_{f}"])

    student_delta = merged[out_cols].copy()
    p02_student_delta = OUT_DIR / f"02_W2W3_student_feature_deltas_{SUFFIX}.csv"
    student_delta.to_csv(p02_student_delta, index=False, encoding="utf-8-sig")

    # 02 detailed compare
    detailed_rows = []
    for f in FEATURES:
        w2v = to_float(student_delta[f"W2_{f}"])
        w3v = to_float(student_delta[f"W3_{f}"])
        dv = to_float(student_delta[f"delta_{f}"])
        n = len(dv)
        inc = int(np.sum(dv > 0))
        eq = int(np.sum(dv == 0))
        dec = int(np.sum(dv < 0))
        mean_w2 = float(np.mean(w2v))
        mean_w3 = float(np.mean(w3v))
        mean_ch = float(np.mean(dv))
        detailed_rows.append(
            {
                "feature": f,
                "w2_col": f"W2_{f}",
                "w3_col": f"W3_{f}",
                "n": n,
                "mean_w2": mean_w2,
                "mean_w3": mean_w3,
                "mean_change_w3_minus_w2": mean_ch,
                "pct_change_vs_w2": (mean_ch / mean_w2 * 100.0) if mean_w2 != 0 else np.nan,
                "std_w2": float(np.std(w2v, ddof=1)),
                "std_w3": float(np.std(w3v, ddof=1)),
                "std_change": float(np.std(dv, ddof=1)),
                "median_w2": float(np.median(w2v)),
                "median_w3": float(np.median(w3v)),
                "median_change": float(np.median(dv)),
                "q05_change": float(np.quantile(dv, 0.05)),
                "q10_change": float(np.quantile(dv, 0.10)),
                "q25_change": float(np.quantile(dv, 0.25)),
                "q75_change": float(np.quantile(dv, 0.75)),
                "q90_change": float(np.quantile(dv, 0.90)),
                "q95_change": float(np.quantile(dv, 0.95)),
                "min_change": float(np.min(dv)),
                "max_change": float(np.max(dv)),
                "increase_n": inc,
                "increase_pct": pct(inc, n),
                "no_change_n": eq,
                "no_change_pct": pct(eq, n),
                "decrease_n": dec,
                "decrease_pct": pct(dec, n),
                "mae_change": float(np.mean(np.abs(dv))),
                "rmse_change": float(np.sqrt(np.mean(np.square(dv)))),
                "corr_w2_w3": float(pd.Series(w2v).corr(pd.Series(w3v))),
            }
        )
    detailed_df = pd.DataFrame(detailed_rows)
    p02_detailed = OUT_DIR / f"02_W2W3_8features_detailed_compare_{SUFFIX}.csv"
    detailed_df.to_csv(p02_detailed, index=False, encoding="utf-8-sig")

    # 02 delta distribution
    delta_rows = []
    for f in FEATURES:
        dv = pd.to_numeric(student_delta[f"delta_{f}"], errors="coerce").astype(int)
        vc = dv.value_counts().sort_index()
        for dval, c in vc.items():
            delta_rows.append(
                {"feature": f, "delta": int(dval), "count": int(c), "pct": pct(int(c), len(dv))}
            )
    delta_df = pd.DataFrame(delta_rows)
    p02_delta_dist = OUT_DIR / f"02_W2W3_8features_delta_distribution_{SUFFIX}.csv"
    delta_df.to_csv(p02_delta_dist, index=False, encoding="utf-8-sig")

    # 02 bucket distribution
    bucket_rows = []
    for f in FEATURES:
        for wave in ["W2", "W3"]:
            col = f"{wave}_{f}"
            vals = pd.to_numeric(student_delta[col], errors="coerce").fillna(0).astype(int)
            b = vals.map(calc_bucket)
            cnt = b.value_counts().to_dict()
            for bk in BUCKETS:
                c = int(cnt.get(bk, 0))
                bucket_rows.append(
                    {"feature": f, "wave": wave, "bucket": bk, "count": c, "pct": pct(c, len(vals))}
                )
    bucket_df = pd.DataFrame(bucket_rows)
    p02_bucket = OUT_DIR / f"02_W2W3_8features_wave_bucket_distribution_{SUFFIX}.csv"
    bucket_df.to_csv(p02_bucket, index=False, encoding="utf-8-sig")

    # 02 aggregate summary
    tmp = student_delta.copy()
    tmp["W2_friend_total"] = (
        tmp["W2_out_online_friend"]
        + tmp["W2_in_online_friend"]
        + tmp["W2_out_offline_friend"]
        + tmp["W2_in_offline_friend"]
    )
    tmp["W3_friend_total"] = (
        tmp["W3_out_online_friend"]
        + tmp["W3_in_online_friend"]
        + tmp["W3_out_offline_friend"]
        + tmp["W3_in_offline_friend"]
    )
    tmp["W2_enemy_total"] = (
        tmp["W2_out_online_enemy"]
        + tmp["W2_in_online_enemy"]
        + tmp["W2_out_offline_enemy"]
        + tmp["W2_in_offline_enemy"]
    )
    tmp["W3_enemy_total"] = (
        tmp["W3_out_online_enemy"]
        + tmp["W3_in_online_enemy"]
        + tmp["W3_out_offline_enemy"]
        + tmp["W3_in_offline_enemy"]
    )
    tmp["W2_online_total"] = (
        tmp["W2_out_online_friend"]
        + tmp["W2_in_online_friend"]
        + tmp["W2_out_online_enemy"]
        + tmp["W2_in_online_enemy"]
    )
    tmp["W3_online_total"] = (
        tmp["W3_out_online_friend"]
        + tmp["W3_in_online_friend"]
        + tmp["W3_out_online_enemy"]
        + tmp["W3_in_online_enemy"]
    )
    tmp["W2_offline_total"] = (
        tmp["W2_out_offline_friend"]
        + tmp["W2_in_offline_friend"]
        + tmp["W2_out_offline_enemy"]
        + tmp["W2_in_offline_enemy"]
    )
    tmp["W3_offline_total"] = (
        tmp["W3_out_offline_friend"]
        + tmp["W3_in_offline_friend"]
        + tmp["W3_out_offline_enemy"]
        + tmp["W3_in_offline_enemy"]
    )
    tmp["W2_out_total"] = (
        tmp["W2_out_online_friend"]
        + tmp["W2_out_online_enemy"]
        + tmp["W2_out_offline_friend"]
        + tmp["W2_out_offline_enemy"]
    )
    tmp["W3_out_total"] = (
        tmp["W3_out_online_friend"]
        + tmp["W3_out_online_enemy"]
        + tmp["W3_out_offline_friend"]
        + tmp["W3_out_offline_enemy"]
    )
    tmp["W2_in_total"] = (
        tmp["W2_in_online_friend"]
        + tmp["W2_in_online_enemy"]
        + tmp["W2_in_offline_friend"]
        + tmp["W2_in_offline_enemy"]
    )
    tmp["W3_in_total"] = (
        tmp["W3_in_online_friend"]
        + tmp["W3_in_online_enemy"]
        + tmp["W3_in_offline_friend"]
        + tmp["W3_in_offline_enemy"]
    )

    aggregate_specs = [
        ("friend_total", "W2_friend_total", "W3_friend_total"),
        ("enemy_total", "W2_enemy_total", "W3_enemy_total"),
        ("online_total", "W2_online_total", "W3_online_total"),
        ("offline_total", "W2_offline_total", "W3_offline_total"),
        ("out_total", "W2_out_total", "W3_out_total"),
        ("in_total", "W2_in_total", "W3_in_total"),
    ]
    agg_rows = []
    for metric, c2, c3 in aggregate_specs:
        w2v = to_float(tmp[c2])
        w3v = to_float(tmp[c3])
        dv = w3v - w2v
        inc = int(np.sum(dv > 0))
        eq = int(np.sum(dv == 0))
        dec = int(np.sum(dv < 0))
        mean_w2 = float(np.mean(w2v))
        mean_w3 = float(np.mean(w3v))
        mean_ch = float(np.mean(dv))
        agg_rows.append(
            {
                "metric": metric,
                "mean_w2": mean_w2,
                "mean_w3": mean_w3,
                "mean_change_w3_minus_w2": mean_ch,
                "pct_change_vs_w2": (mean_ch / mean_w2 * 100.0) if mean_w2 != 0 else np.nan,
                "median_change": float(np.median(dv)),
                "increase_pct": pct(inc, len(dv)),
                "no_change_pct": pct(eq, len(dv)),
                "decrease_pct": pct(dec, len(dv)),
                "mae_change": float(np.mean(np.abs(dv))),
            }
        )
    agg_df = pd.DataFrame(agg_rows)
    p02_agg = OUT_DIR / f"02_W2W3_aggregate_change_summary_{SUFFIX}.csv"
    agg_df.to_csv(p02_agg, index=False, encoding="utf-8-sig")

    # 02 school mean deltas
    school_tmp = student_delta.copy()
    school_tmp["delta_friend_total"] = (
        school_tmp["delta_out_online_friend"]
        + school_tmp["delta_in_online_friend"]
        + school_tmp["delta_out_offline_friend"]
        + school_tmp["delta_in_offline_friend"]
    )
    school_tmp["delta_enemy_total"] = (
        school_tmp["delta_out_online_enemy"]
        + school_tmp["delta_in_online_enemy"]
        + school_tmp["delta_out_offline_enemy"]
        + school_tmp["delta_in_offline_enemy"]
    )
    school_cols = [
        "delta_out_online_friend",
        "delta_in_online_friend",
        "delta_out_online_enemy",
        "delta_in_online_enemy",
        "delta_out_offline_friend",
        "delta_in_offline_friend",
        "delta_out_offline_enemy",
        "delta_in_offline_enemy",
        "delta_friend_total",
        "delta_enemy_total",
    ]
    school_df = (
        school_tmp.groupby("school_id")
        .agg(n_students=("student_id", "size"), **{c: (c, "mean") for c in school_cols})
        .reset_index()
    )
    p02_school = OUT_DIR / f"02_W2W3_school_mean_deltas_{SUFFIX}.csv"
    school_df.to_csv(p02_school, index=False, encoding="utf-8-sig")

    # 03 paired tests
    paired_rows = []
    w_pvals = []
    for f in FEATURES:
        w2v = to_float(student_delta[f"W2_{f}"])
        w3v = to_float(student_delta[f"W3_{f}"])
        dv = w3v - w2v
        n = len(dv)
        nz = int(np.sum(dv != 0))
        inc = int(np.sum(dv > 0))
        eq = int(np.sum(dv == 0))
        dec = int(np.sum(dv < 0))
        w_stat, w_p = safe_wilcoxon(dv)
        t_stat, t_p = safe_ttest(w2v, w3v)
        std_d = float(np.std(dv, ddof=1))
        dz = float(np.mean(dv) / std_d) if std_d != 0 else np.nan
        paired_rows.append(
            {
                "feature": f,
                "feature_zh": FEATURE_ZH[f],
                "w2_col": f"W2_{f}",
                "w3_col": f"W3_{f}",
                "n_pairs": n,
                "n_nonzero_delta": nz,
                "mean_w2": float(np.mean(w2v)),
                "mean_w3": float(np.mean(w3v)),
                "mean_delta_w3_minus_w2": float(np.mean(dv)),
                "median_delta_w3_minus_w2": float(np.median(dv)),
                "pct_increase": pct(inc, n),
                "pct_no_change": pct(eq, n),
                "pct_decrease": pct(dec, n),
                "wilcoxon_statistic": w_stat,
                "wilcoxon_p_value": w_p,
                "paired_t_statistic": t_stat,
                "paired_t_p_value": t_p,
                "effect_size_dz": dz,
            }
        )
        w_pvals.append(w_p)

    pvals = np.array([np.nan if pd.isna(x) else float(x) for x in w_pvals], dtype=float)
    mask = np.isfinite(pvals)
    fdr = np.full_like(pvals, np.nan, dtype=float)
    if np.any(mask):
        _, p_adj, _, _ = multipletests(pvals[mask], alpha=0.05, method="fdr_bh")
        fdr[mask] = p_adj

    paired_df = pd.DataFrame(paired_rows)
    paired_df["wilcoxon_fdr_bh"] = fdr
    paired_df["sig_wilcoxon_p_lt_0_05"] = paired_df["wilcoxon_p_value"] < 0.05
    paired_df["sig_wilcoxon_fdr_lt_0_05"] = paired_df["wilcoxon_fdr_bh"] < 0.05
    paired_df = paired_df.sort_values("wilcoxon_p_value", na_position="last").reset_index(drop=True)
    p03 = OUT_DIR / f"03_W2W3_8features_paired_tests_{SUFFIX}.csv"
    paired_df.to_csv(p03, index=False, encoding="utf-8-sig")

    # 04 ambiguous backtrace
    def build_candidate_lookup(df_roster: pd.DataFrame) -> Dict[Tuple[str, str, str], List[str]]:
        d: Dict[Tuple[str, str, str], List[str]] = {}
        for r in df_roster.to_dict(orient="records"):
            k = (
                norm_key_part(r.get("school_id")),
                norm_key_part(r.get("class")),
                norm_key_part(r.get("seat")),
            )
            d.setdefault(k, []).append(str(r.get("student_id")))
        return d

    cand_w2 = build_candidate_lookup(w2_roster)
    cand_w3 = build_candidate_lookup(w3_roster)
    amb = pd.concat(
        [
            w2_unmatched.loc[w2_unmatched["reason"] == "ambiguous_duplicate_seat"].copy(),
            w3_unmatched.loc[w3_unmatched["reason"] == "ambiguous_duplicate_seat"].copy(),
        ],
        ignore_index=True,
    )
    bt_rows = []
    for r in amb.to_dict(orient="records"):
        seat = parse_positive_seat(r.get("nominated_seat"))
        if seat is None:
            continue
        class_val = r.get("class")
        key = (norm_key_part(r.get("school_id")), norm_key_part(class_val), str(seat))
        cand = cand_w2.get(key, []) if r.get("wave") == "W2" else cand_w3.get(key, [])
        bt_rows.append(
            {
                "wave": r.get("wave"),
                "nominator_student_id": r.get("nominator_student_id"),
                "school_id": r.get("school_id"),
                "class": class_val,
                "nominator_seat": r.get("nominator_seat"),
                "nomination_type": r.get("nomination_type"),
                "nomination_column": r.get("nomination_column"),
                "nominated_raw": r.get("nominated_raw"),
                "nominated_seat_normalized": seat,
                "reason": r.get("reason"),
                "candidate_count": len(cand),
                "candidate_student_ids": ";".join(cand),
            }
        )
    bt_df = pd.DataFrame(bt_rows)
    p04 = OUT_DIR / f"04_W2W3_ambiguous_duplicate_seat_backtrace_{SUFFIX}.csv"
    bt_df.to_csv(p04, index=False, encoding="utf-8-sig")

    # 05 maps
    map_from_amb = (
        bt_df.groupby(
            [
                "wave",
                "school_id",
                "class",
                "nominated_seat_normalized",
                "candidate_count",
                "candidate_student_ids",
            ],
            dropna=False,
        )
        .size()
        .reset_index(name="ambiguous_rows_ref_count")
        .rename(columns={"nominated_seat_normalized": "seat"})
        .sort_values(["wave", "school_id", "class", "seat"])
        .reset_index(drop=True)
    )
    p05_from_amb = OUT_DIR / f"05_W2W3_duplicate_seat_student_map_from_ambiguous_{SUFFIX}.csv"
    map_from_amb.to_csv(p05_from_amb, index=False, encoding="utf-8-sig")

    all_dup_rows = []
    for wave, ro in [("W2", w2_roster), ("W3", w3_roster)]:
        tmp = ro.copy()
        tmp["school_id_n"] = tmp["school_id"].map(norm_key_part)
        tmp["class_n"] = tmp["class"].map(norm_key_part)
        tmp["seat_n"] = tmp["seat"].map(norm_key_part)
        for _, g in tmp.groupby(["school_id_n", "class_n", "seat_n"]):
            if len(g) > 1:
                all_dup_rows.append(
                    {
                        "wave": wave,
                        "school_id": g["school_id"].iloc[0],
                        "class": g["class"].iloc[0],
                        "seat": g["seat_n"].iloc[0],
                        "candidate_count": int(len(g)),
                        "candidate_student_ids": ";".join(sorted(g["student_id"].astype(str).tolist())),
                    }
                )
    all_dup_df = pd.DataFrame(all_dup_rows).sort_values(
        ["wave", "school_id", "class", "seat"]
    )
    p05_all = OUT_DIR / f"05_W2W3_duplicate_seat_student_map_all_roster_{SUFFIX}.csv"
    all_dup_df.to_csv(p05_all, index=False, encoding="utf-8-sig")

    key_cols = ["wave", "school_id", "class", "seat"]
    a = all_dup_df[key_cols].copy()
    b = map_from_amb[key_cols].copy()
    a["_k"] = a.astype(str).agg("|".join, axis=1)
    b["_k"] = b.astype(str).agg("|".join, axis=1)
    not_ref = all_dup_df.loc[~a["_k"].isin(set(b["_k"]))].copy()
    p05_not_ref = (
        OUT_DIR / f"05_W2W3_duplicate_seat_student_map_not_referenced_by_ambiguous_{SUFFIX}.csv"
    )
    not_ref.to_csv(p05_not_ref, index=False, encoding="utf-8-sig")

    # txt description
    txt_lines = [
        f"Output directory: {OUT_DIR}",
        f"Source W2: {W2_PATH}",
        f"Source W3: {W3_PATH}",
        "",
        "Important note:",
        "W3_studentdata_ver9.csv does not contain explicit school_id/class columns.",
        "This rerun maps W3 school_id/class from W2 by student_id (full 7045/7045 matched).",
        "",
        "File descriptions:",
        f"00_W2_nominated_not_in_list_{SUFFIX}.csv",
        "- W2 nominations that cannot be uniquely mapped by school_id+class+seat.",
        "- reason: not_in_list or ambiguous_duplicate_seat.",
        "",
        f"00_W3_nominated_not_in_list_{SUFFIX}.csv",
        "- W3 nominations that cannot be uniquely mapped by school_id+class+seat.",
        "- reason: not_in_list or ambiguous_duplicate_seat.",
        "",
        f"01_W2_student_8features_{SUFFIX}.csv",
        "- Per-student W2 network 8 features (out/in x online/offline x friend/enemy),",
        "- counted only from uniquely matched nominations.",
        "",
        f"01_W3_student_8features_{SUFFIX}.csv",
        "- Per-student W3 network 8 features (out/in x online/offline x friend/enemy),",
        "- counted only from uniquely matched nominations.",
        "",
        f"02_W2W3_student_feature_deltas_{SUFFIX}.csv",
        "- Student-level paired table of W2, W3, and delta (W3-W2) for 8 features.",
        "",
        f"02_W2W3_8features_detailed_compare_{SUFFIX}.csv",
        "- Feature-level descriptive comparison (mean/std/quantiles/increase-decrease/correlation).",
        "",
        f"02_W2W3_8features_delta_distribution_{SUFFIX}.csv",
        "- Distribution of integer deltas (W3-W2) for each feature.",
        "",
        f"02_W2W3_8features_wave_bucket_distribution_{SUFFIX}.csv",
        "- Bucketed distribution by wave (0,1,2,3,4,5,6-10,11+) for each feature.",
        "",
        f"02_W2W3_aggregate_change_summary_{SUFFIX}.csv",
        "- Aggregate metrics over 6 totals: friend, enemy, online, offline, out, in.",
        "",
        f"02_W2W3_school_mean_deltas_{SUFFIX}.csv",
        "- School-level mean deltas for each feature plus friend_total/enemy_total deltas.",
        "",
        f"03_W2W3_8features_paired_tests_{SUFFIX}.csv",
        "- Paired tests per feature: Wilcoxon, paired t-test, effect size dz, FDR-BH.",
        "",
        f"04_W2W3_ambiguous_duplicate_seat_backtrace_{SUFFIX}.csv",
        "- Backtrace list for ambiguous_duplicate_seat: each ambiguous nomination with candidate student_ids.",
        "",
        f"05_W2W3_duplicate_seat_student_map_from_ambiguous_{SUFFIX}.csv",
        "- Unique duplicate-seat keys that were referenced by ambiguous nominations, with candidate student_ids and reference counts.",
        "",
        f"05_W2W3_duplicate_seat_student_map_all_roster_{SUFFIX}.csv",
        "- All duplicate seat keys in rosters (W2/W3), whether referenced or not.",
        "",
        f"05_W2W3_duplicate_seat_student_map_not_referenced_by_ambiguous_{SUFFIX}.csv",
        "- Duplicate seat keys existing in roster but not referenced by ambiguous nomination records.",
        "",
    ]
    txt_path = OUT_DIR / f"README_file_descriptions_{SUFFIX}.txt"
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")

    produced = sorted([p.name for p in OUT_DIR.glob("*") if p.is_file()])
    print(f"Produced files: {len(produced)}")
    for n in produced:
        print(n)


if __name__ == "__main__":
    main()
