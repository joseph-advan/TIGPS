from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress")
BASE_DIR = ROOT / r"Code\EDA\Mental 與 Relationship關聯性 製作特徵\檢查"
OUT_DIR = BASE_DIR / "derived_feature_candidates_ver9rerun_20260326"


W2_FEATURE_PATH = ROOT / r"Code\EDA\relationship\兩年提名比例\其他\01_W2_student_8features_ver9rerun_20260326.csv"
W3_FEATURE_PATH = ROOT / r"Code\EDA\relationship\兩年提名比例\其他\01_W3_student_8features_ver9rerun_20260326.csv"
W2_STUDENT_PATH = ROOT / r"Data\2024data\TIGPS_W2_studentdata_ver9.csv"
W3_STUDENT_PATH = ROOT / r"Data\2025data\W3_studentdata_ver9.csv"


W2_FEATURES = [
    "W2_out_online_friend",
    "W2_in_online_friend",
    "W2_out_online_enemy",
    "W2_in_online_enemy",
    "W2_out_offline_friend",
    "W2_in_offline_friend",
    "W2_out_offline_enemy",
    "W2_in_offline_enemy",
]

W3_FEATURES = [
    "W3_out_online_friend",
    "W3_in_online_friend",
    "W3_out_online_enemy",
    "W3_in_online_enemy",
    "W3_out_offline_friend",
    "W3_in_offline_friend",
    "W3_out_offline_enemy",
    "W3_in_offline_enemy",
]


def _to_num(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def _zscore(s: pd.Series) -> pd.Series:
    std = s.std(ddof=0)
    if pd.isna(std) or std == 0:
        return pd.Series(np.nan, index=s.index)
    return (s - s.mean()) / std


def _safe_ratio(num: pd.Series, den: pd.Series, eps: float = 1.0) -> pd.Series:
    return (num + eps) / (den + eps)


def _evaluate_feature(y: pd.Series, x: pd.Series) -> Dict[str, float]:
    m = pd.concat([y, x], axis=1).dropna()
    if len(m) < 3:
        return {
            "n_pair": len(m),
            "mean": np.nan,
            "std": np.nan,
            "skew": np.nan,
            "pearson_r": np.nan,
            "pearson_p": np.nan,
            "spearman_rho": np.nan,
            "spearman_p": np.nan,
            "ols_r2": np.nan,
        }

    yv = m.iloc[:, 0]
    xv = m.iloc[:, 1]
    pearson_r, pearson_p = stats.pearsonr(xv, yv)
    spearman_rho, spearman_p = stats.spearmanr(xv, yv, nan_policy="omit")

    x_mean = float(xv.mean())
    x_std = float(xv.std(ddof=1))
    x_skew = float(xv.skew())

    # Univariate OLS R2
    x_mat = np.column_stack([np.ones(len(xv)), xv.to_numpy(dtype=float)])
    y_arr = yv.to_numpy(dtype=float)
    coef, _, _, _ = np.linalg.lstsq(x_mat, y_arr, rcond=None)
    y_hat = x_mat @ coef
    sse = float(np.sum((y_arr - y_hat) ** 2))
    sst = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
    r2 = np.nan if sst == 0 else (1 - sse / sst)

    return {
        "n_pair": len(m),
        "mean": x_mean,
        "std": x_std,
        "skew": x_skew,
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "spearman_rho": float(spearman_rho),
        "spearman_p": float(spearman_p),
        "ols_r2": float(r2),
    }


def _pca_first_component(df: pd.DataFrame, cols: List[str]) -> Tuple[pd.Series, pd.DataFrame]:
    x = df[cols].copy()
    z = x.apply(_zscore)
    keep = np.all(np.isfinite(z.to_numpy(dtype=float)), axis=1)
    z_valid = z.loc[keep]
    if z_valid.empty:
        score = pd.Series(np.nan, index=df.index, name="pca1_8feat")
        loadings = pd.DataFrame({"feature": cols, "loading_pc1": [np.nan] * len(cols)})
        return score, loadings

    cov = np.cov(z_valid.to_numpy(dtype=float), rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    idx = np.argsort(eigvals)[::-1]
    pc1 = eigvecs[:, idx[0]]
    score_valid = z_valid.to_numpy(dtype=float) @ pc1
    score = pd.Series(np.nan, index=df.index, name="pca1_8feat")
    score.loc[z_valid.index] = score_valid

    loadings = pd.DataFrame({"feature": cols, "loading_pc1": pc1})
    loadings["abs_loading_rank"] = loadings["loading_pc1"].abs().rank(ascending=False, method="min")
    loadings = loadings.sort_values("abs_loading_rank").reset_index(drop=True)
    return score, loadings


def _build_derived(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    c = {name.split("_", 1)[1]: name for name in cols}
    d = pd.DataFrame(index=df.index)

    d["friend_total"] = (
        df[c["out_online_friend"]]
        + df[c["in_online_friend"]]
        + df[c["out_offline_friend"]]
        + df[c["in_offline_friend"]]
    )
    d["enemy_total"] = (
        df[c["out_online_enemy"]]
        + df[c["in_online_enemy"]]
        + df[c["out_offline_enemy"]]
        + df[c["in_offline_enemy"]]
    )
    d["social_load_total"] = d["friend_total"] + d["enemy_total"]
    d["friend_minus_enemy"] = d["friend_total"] - d["enemy_total"]
    d["enemy_minus_friend"] = -d["friend_minus_enemy"]
    d["enemy_ratio_of_total"] = d["enemy_total"] / d["social_load_total"].replace(0, np.nan)

    d["online_total"] = (
        df[c["out_online_friend"]]
        + df[c["in_online_friend"]]
        + df[c["out_online_enemy"]]
        + df[c["in_online_enemy"]]
    )
    d["offline_total"] = (
        df[c["out_offline_friend"]]
        + df[c["in_offline_friend"]]
        + df[c["out_offline_enemy"]]
        + df[c["in_offline_enemy"]]
    )
    d["online_minus_offline"] = d["online_total"] - d["offline_total"]

    d["out_total"] = (
        df[c["out_online_friend"]]
        + df[c["out_online_enemy"]]
        + df[c["out_offline_friend"]]
        + df[c["out_offline_enemy"]]
    )
    d["in_total"] = (
        df[c["in_online_friend"]]
        + df[c["in_online_enemy"]]
        + df[c["in_offline_friend"]]
        + df[c["in_offline_enemy"]]
    )
    d["out_minus_in"] = d["out_total"] - d["in_total"]
    d["in_minus_out"] = -d["out_minus_in"]

    d["enemy_to_friend_ratio"] = _safe_ratio(d["enemy_total"], d["friend_total"], eps=1.0)
    d["friend_to_enemy_ratio"] = _safe_ratio(d["friend_total"], d["enemy_total"], eps=1.0)

    return d


def run_wave(
    wave: str,
    feature_path: Path,
    feature_cols: List[str],
    student_path: Path,
    score_cols: List[str],
) -> None:
    f = pd.read_csv(feature_path, dtype={"student_id": str}, low_memory=False)
    s = pd.read_csv(student_path, dtype={"student_id": str}, low_memory=False)

    for c in feature_cols:
        if c not in f.columns:
            raise KeyError(f"{wave}: missing feature column: {c}")
    for c in score_cols:
        if c not in s.columns:
            raise KeyError(f"{wave}: missing score column: {c}")

    keep_f = f[["student_id"] + feature_cols].copy()
    keep_f["student_id"] = keep_f["student_id"].astype(str).str.strip()
    keep_f = _to_num(keep_f, feature_cols)

    keep_s = s[["student_id"] + score_cols].copy()
    keep_s["student_id"] = keep_s["student_id"].astype(str).str.strip()
    keep_s = _to_num(keep_s, score_cols)
    target_col = f"{wave}_depression_total"
    keep_s[target_col] = keep_s[score_cols].sum(axis=1, min_count=1)
    keep_s = keep_s[["student_id", target_col]]

    merged = keep_f.merge(keep_s, on="student_id", how="inner")
    raw = merged.copy()
    derived = _build_derived(raw, feature_cols)
    pca_score, pca_loadings = _pca_first_component(raw, feature_cols)
    derived["pca1_8feat"] = pca_score
    derived["pca1_8feat_z"] = _zscore(derived["pca1_8feat"])

    full = pd.concat([raw[["student_id", target_col]], raw[feature_cols], derived], axis=1)

    eval_rows = []
    for col in derived.columns:
        r = _evaluate_feature(full[target_col], full[col])
        r["feature"] = col
        eval_rows.append(r)
    eval_df = pd.DataFrame(eval_rows)
    eval_df["abs_spearman_rank"] = eval_df["spearman_rho"].abs().rank(ascending=False, method="min")
    eval_df = eval_df.sort_values(["abs_spearman_rank", "feature"]).reset_index(drop=True)

    # Recommend top candidates under simple rules
    candidates = eval_df.copy()
    candidates["rule_variance_ok"] = candidates["std"] > 0
    candidates["rule_abs_spearman_ge_0_05"] = candidates["spearman_rho"].abs() >= 0.05
    candidates["rule_abs_skew_le_2_5"] = candidates["skew"].abs() <= 2.5
    candidates["recommended"] = (
        candidates["rule_variance_ok"]
        & candidates["rule_abs_spearman_ge_0_05"]
        & candidates["rule_abs_skew_le_2_5"]
    )

    out = OUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    full.to_csv(out / f"{wave}_01_raw_plus_derived_features.csv", index=False, encoding="utf-8-sig")
    eval_df.to_csv(out / f"{wave}_02_derived_feature_evaluation.csv", index=False, encoding="utf-8-sig")
    candidates.to_csv(out / f"{wave}_03_candidate_filter_flags.csv", index=False, encoding="utf-8-sig")
    pca_loadings.to_csv(out / f"{wave}_04_pca1_loadings_from_8features.csv", index=False, encoding="utf-8-sig")


def write_readme() -> None:
    text = (
        "Derived feature engineering and evaluation\n"
        "========================================\n\n"
        "Goal:\n"
        "- Check whether the original 8 relationship variables can be transformed into ONE useful feature.\n"
        "- Provide multiple derived feature options and evaluate their association with depression score.\n\n"
        "Wave outputs (W2 and W3):\n"
        "01_raw_plus_derived_features.csv\n"
        "- student_id, depression_total, original 8 features, and all derived features.\n\n"
        "02_derived_feature_evaluation.csv\n"
        "- One row per derived feature.\n"
        "- Includes: Pearson/Spearman correlation, p-values, skew, and univariate OLS R2.\n"
        "- Sort by abs_spearman_rank (larger association first).\n\n"
        "03_candidate_filter_flags.csv\n"
        "- Quick rule flags to help pick candidate features.\n"
        "- recommended=True means it passes all simple rules.\n\n"
        "04_pca1_loadings_from_8features.csv\n"
        "- PCA first component loading from original 8 features.\n"
        "- pca1_8feat can be used as a single compressed feature.\n\n"
        "Suggested usage:\n"
        "1) Start from 02_derived_feature_evaluation.csv and focus on top 3-5 by abs_spearman_rank.\n"
        "2) Prefer interpretable features first (friend_minus_enemy, enemy_ratio_of_total).\n"
        "3) Use pca1_8feat only when you prefer a compact but less interpretable index.\n"
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "00_README_derived_feature_evaluation.txt").write_text(text, encoding="utf-8")


def main() -> None:
    run_wave(
        wave="W2",
        feature_path=W2_FEATURE_PATH,
        feature_cols=W2_FEATURES,
        student_path=W2_STUDENT_PATH,
        score_cols=[f"v55_{i}" for i in range(1, 15)],
    )
    run_wave(
        wave="W3",
        feature_path=W3_FEATURE_PATH,
        feature_cols=W3_FEATURES,
        student_path=W3_STUDENT_PATH,
        score_cols=[f"54-{i}" for i in range(1, 15)],
    )
    write_readme()
    print(f"Done. Output: {OUT_DIR}")


if __name__ == "__main__":
    main()

