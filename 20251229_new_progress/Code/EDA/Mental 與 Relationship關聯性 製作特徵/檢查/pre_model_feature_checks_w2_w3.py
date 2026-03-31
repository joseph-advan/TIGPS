from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class WaveConfig:
    wave: str
    feature_path: Path
    student_path: Path
    score_cols: List[str]
    feature_cols: List[str]


ROOT = Path(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress")
SCRIPT_DIR = ROOT / r"Code\EDA\Mental 與 Relationship關聯性 製作特徵\檢查"
OUTPUT_DIR = SCRIPT_DIR / "outputs_ver9rerun_20260326"


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


CONFIGS = [
    WaveConfig(
        wave="W2",
        feature_path=ROOT
        / r"Code\EDA\relationship\兩年提名比例\其他\01_W2_student_8features_ver9rerun_20260326.csv",
        student_path=ROOT / r"Data\2024data\TIGPS_W2_studentdata_ver9.csv",
        score_cols=[f"v55_{i}" for i in range(1, 15)],
        feature_cols=W2_FEATURES,
    ),
    WaveConfig(
        wave="W3",
        feature_path=ROOT
        / r"Code\EDA\relationship\兩年提名比例\其他\01_W3_student_8features_ver9rerun_20260326.csv",
        student_path=ROOT / r"Data\2025data\W3_studentdata_ver9.csv",
        score_cols=[f"54-{i}" for i in range(1, 15)],
        feature_cols=W3_FEATURES,
    ),
]


def _to_numeric_df(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def _standardize(s: pd.Series) -> pd.Series:
    std = s.std(ddof=0)
    if pd.isna(std) or std == 0:
        return pd.Series(np.nan, index=s.index)
    return (s - s.mean()) / std


def _fit_simple_ols(y: pd.Series, x: pd.Series) -> Dict[str, float]:
    m = pd.concat([y, x], axis=1).dropna()
    if len(m) < 3:
        return {
            "n": len(m),
            "beta": np.nan,
            "intercept": np.nan,
            "r2": np.nan,
            "p_value_beta": np.nan,
        }

    yv = m.iloc[:, 0].to_numpy(dtype=float)
    xv = m.iloc[:, 1].to_numpy(dtype=float)
    x_mat = np.column_stack([np.ones(len(xv)), xv])
    coef, _, _, _ = np.linalg.lstsq(x_mat, yv, rcond=None)
    y_hat = x_mat @ coef
    sse = float(np.sum((yv - y_hat) ** 2))
    sst = float(np.sum((yv - np.mean(yv)) ** 2))
    r2 = np.nan if sst == 0 else (1 - sse / sst)

    # p-value for slope
    df_resid = len(xv) - 2
    if df_resid > 0:
        mse = sse / df_resid
        xtx_inv = np.linalg.pinv(x_mat.T @ x_mat)
        se_beta = np.sqrt(mse * xtx_inv[1, 1])
        t_val = coef[1] / se_beta if se_beta > 0 else np.nan
        p_val = 2 * (1 - stats.t.cdf(abs(t_val), df=df_resid)) if np.isfinite(t_val) else np.nan
    else:
        p_val = np.nan

    return {
        "n": len(m),
        "beta": float(coef[1]),
        "intercept": float(coef[0]),
        "r2": float(r2),
        "p_value_beta": float(p_val) if pd.notna(p_val) else np.nan,
    }


def _fit_multivariate_standardized(y: pd.Series, x_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    m = pd.concat([y, x_df], axis=1).dropna()
    if len(m) < (x_df.shape[1] + 2):
        out = pd.DataFrame(
            {
                "feature": x_df.columns,
                "std_beta": [np.nan] * x_df.shape[1],
                "abs_std_beta_rank": [np.nan] * x_df.shape[1],
            }
        )
        return out, {"n": len(m), "r2": np.nan, "adj_r2": np.nan}

    yv = m.iloc[:, 0]
    xv = m.iloc[:, 1:]
    y_std = _standardize(yv).to_numpy(dtype=float)
    x_std = xv.apply(_standardize).to_numpy(dtype=float)

    keep = np.isfinite(y_std) & np.all(np.isfinite(x_std), axis=1)
    y_std = y_std[keep]
    x_std = x_std[keep]

    n = len(y_std)
    p = x_std.shape[1]
    if n < (p + 2):
        out = pd.DataFrame(
            {
                "feature": x_df.columns,
                "std_beta": [np.nan] * p,
                "abs_std_beta_rank": [np.nan] * p,
            }
        )
        return out, {"n": n, "r2": np.nan, "adj_r2": np.nan}

    x_mat = np.column_stack([np.ones(n), x_std])
    coef, _, _, _ = np.linalg.lstsq(x_mat, y_std, rcond=None)
    y_hat = x_mat @ coef
    sse = float(np.sum((y_std - y_hat) ** 2))
    sst = float(np.sum((y_std - np.mean(y_std)) ** 2))
    r2 = np.nan if sst == 0 else (1 - sse / sst)
    adj_r2 = np.nan if n <= p + 1 else 1 - (1 - r2) * (n - 1) / (n - p - 1)

    beta = coef[1:]
    beta_df = pd.DataFrame({"feature": x_df.columns, "std_beta": beta})
    beta_df["abs_std_beta_rank"] = beta_df["std_beta"].abs().rank(ascending=False, method="min")
    beta_df = beta_df.sort_values("abs_std_beta_rank").reset_index(drop=True)
    metrics = {"n": n, "r2": float(r2), "adj_r2": float(adj_r2)}
    return beta_df, metrics


def _calc_vif(x_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in x_df.columns:
        y = x_df[col]
        others = [c for c in x_df.columns if c != col]
        m = pd.concat([y, x_df[others]], axis=1).dropna()
        if len(m) < 3:
            rows.append({"feature": col, "vif": np.nan, "r2_of_feature_on_others": np.nan})
            continue

        yv = m[col].to_numpy(dtype=float)
        xv = m[others].to_numpy(dtype=float)
        xv = np.column_stack([np.ones(len(xv)), xv])
        coef, _, _, _ = np.linalg.lstsq(xv, yv, rcond=None)
        y_hat = xv @ coef
        sse = float(np.sum((yv - y_hat) ** 2))
        sst = float(np.sum((yv - np.mean(yv)) ** 2))
        r2 = np.nan if sst == 0 else (1 - sse / sst)
        vif = np.nan if (pd.isna(r2) or (1 - r2) <= 0) else float(1 / (1 - r2))
        rows.append({"feature": col, "vif": vif, "r2_of_feature_on_others": float(r2)})

    out = pd.DataFrame(rows).sort_values("vif", ascending=False).reset_index(drop=True)
    return out


def _feature_target_correlations(y: pd.Series, x_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in x_df.columns:
        m = pd.concat([y, x_df[col]], axis=1).dropna()
        if len(m) < 3:
            rows.append(
                {
                    "feature": col,
                    "n_pair": len(m),
                    "pearson_r": np.nan,
                    "pearson_p": np.nan,
                    "spearman_rho": np.nan,
                    "spearman_p": np.nan,
                }
            )
            continue

        yv = m.iloc[:, 0]
        xv = m.iloc[:, 1]
        pearson_r, pearson_p = stats.pearsonr(xv, yv)
        spearman_rho, spearman_p = stats.spearmanr(xv, yv, nan_policy="omit")
        rows.append(
            {
                "feature": col,
                "n_pair": len(m),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_rho": spearman_rho,
                "spearman_p": spearman_p,
            }
        )

    out = pd.DataFrame(rows)
    out["abs_spearman_rank"] = out["spearman_rho"].abs().rank(ascending=False, method="min")
    out = out.sort_values("abs_spearman_rank").reset_index(drop=True)
    return out


def _outlier_iqr_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in df.columns:
        s = df[col].dropna()
        if s.empty:
            rows.append(
                {
                    "variable": col,
                    "q1": np.nan,
                    "q3": np.nan,
                    "iqr": np.nan,
                    "lower_bound": np.nan,
                    "upper_bound": np.nan,
                    "outlier_n": np.nan,
                    "outlier_pct": np.nan,
                }
            )
            continue

        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        out_n = int(((s < lower) | (s > upper)).sum())
        out_pct = out_n / len(s) * 100
        rows.append(
            {
                "variable": col,
                "q1": q1,
                "q3": q3,
                "iqr": iqr,
                "lower_bound": lower,
                "upper_bound": upper,
                "outlier_n": out_n,
                "outlier_pct": out_pct,
            }
        )
    return pd.DataFrame(rows)


def run_wave_checks(cfg: WaveConfig, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    feature_df = pd.read_csv(cfg.feature_path, dtype={"student_id": str}, low_memory=False)
    student_df = pd.read_csv(cfg.student_path, dtype={"student_id": str}, low_memory=False)

    for col in cfg.score_cols:
        if col not in student_df.columns:
            raise KeyError(f"{cfg.wave}: score column not found: {col}")
    for col in cfg.feature_cols:
        if col not in feature_df.columns:
            raise KeyError(f"{cfg.wave}: feature column not found: {col}")

    feature_keep = feature_df[["student_id"] + cfg.feature_cols].copy()
    feature_keep["student_id"] = feature_keep["student_id"].astype(str).str.strip()
    feature_keep = _to_numeric_df(feature_keep, cfg.feature_cols)

    student_keep = student_df[["student_id"] + cfg.score_cols].copy()
    student_keep["student_id"] = student_keep["student_id"].astype(str).str.strip()
    student_keep = _to_numeric_df(student_keep, cfg.score_cols)
    target_col = f"{cfg.wave}_depression_total"
    student_keep[target_col] = student_keep[cfg.score_cols].sum(axis=1, min_count=1)
    student_keep = student_keep[["student_id", target_col]]

    merged = feature_keep.merge(student_keep, on="student_id", how="inner")

    duplicate_feature_id_n = int(feature_keep["student_id"].duplicated().sum())
    duplicate_student_id_n = int(student_keep["student_id"].duplicated().sum())
    merged_dup_n = int(merged["student_id"].duplicated().sum())

    var_cols = cfg.feature_cols + [target_col]
    miss = merged[var_cols].isna().sum().rename("missing_n").to_frame()
    miss["missing_pct"] = miss["missing_n"] / len(merged) * 100
    miss = miss.reset_index().rename(columns={"index": "variable"})

    complete = merged.dropna(subset=var_cols).copy()
    desc = complete[var_cols].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T.reset_index()
    desc = desc.rename(columns={"index": "variable"})

    outlier_tbl = _outlier_iqr_table(complete[var_cols])
    corr_ft = _feature_target_correlations(complete[target_col], complete[cfg.feature_cols])
    corr_ff_pearson = complete[cfg.feature_cols].corr(method="pearson")
    corr_ff_spearman = complete[cfg.feature_cols].corr(method="spearman")
    vif_df = _calc_vif(complete[cfg.feature_cols])

    # Univariate OLS: each feature separately
    uni_rows = []
    for col in cfg.feature_cols:
        r = _fit_simple_ols(complete[target_col], complete[col])
        r["feature"] = col
        uni_rows.append(r)
    uni_df = pd.DataFrame(uni_rows)[["feature", "n", "beta", "intercept", "r2", "p_value_beta"]]
    uni_df = uni_df.sort_values("r2", ascending=False).reset_index(drop=True)

    # Multivariate OLS with standardized features
    beta_df, mv_metrics = _fit_multivariate_standardized(complete[target_col], complete[cfg.feature_cols])
    mv_metrics_df = pd.DataFrame(
        {
            "metric": ["n_complete", "r2", "adj_r2"],
            "value": [mv_metrics["n"], mv_metrics["r2"], mv_metrics["adj_r2"]],
        }
    )

    # Quality and assumption flags
    max_missing = float(miss["missing_pct"].max()) if not miss.empty else np.nan
    max_vif = float(vif_df["vif"].max()) if not vif_df.empty else np.nan
    high_corr_pairs = int((corr_ff_spearman.abs() > 0.8).sum().sum() - len(cfg.feature_cols))
    high_corr_pairs = max(high_corr_pairs // 2, 0)
    max_outlier = float(outlier_tbl["outlier_pct"].max()) if not outlier_tbl.empty else np.nan
    target_skew = float(complete[target_col].skew()) if len(complete) > 2 else np.nan

    flags = pd.DataFrame(
        [
            {"check": "max_missing_pct", "value": max_missing, "rule_of_thumb": "< 5% preferred"},
            {"check": "max_vif", "value": max_vif, "rule_of_thumb": "< 5 ideal, 5-10 warning, >10 high"},
            {"check": "n_feature_pairs_abs_spearman_gt_0_8", "value": high_corr_pairs, "rule_of_thumb": "0 preferred"},
            {"check": "max_outlier_pct_iqr_rule", "value": max_outlier, "rule_of_thumb": "smaller is better"},
            {"check": "target_skewness", "value": target_skew, "rule_of_thumb": "|skew| < 1 usually acceptable"},
            {"check": "n_merged", "value": len(merged), "rule_of_thumb": "larger is better"},
            {"check": "n_complete_cases", "value": len(complete), "rule_of_thumb": "close to n_merged preferred"},
            {"check": "duplicate_student_id_in_feature_file", "value": duplicate_feature_id_n, "rule_of_thumb": "should be 0"},
            {"check": "duplicate_student_id_in_student_file", "value": duplicate_student_id_n, "rule_of_thumb": "should be 0"},
            {"check": "duplicate_student_id_after_merge", "value": merged_dup_n, "rule_of_thumb": "should be 0"},
        ]
    )

    # Save outputs
    miss.to_csv(out_dir / f"{cfg.wave}_01_missingness.csv", index=False, encoding="utf-8-sig")
    desc.to_csv(out_dir / f"{cfg.wave}_02_descriptive_stats_complete_cases.csv", index=False, encoding="utf-8-sig")
    outlier_tbl.to_csv(out_dir / f"{cfg.wave}_03_outlier_iqr_check.csv", index=False, encoding="utf-8-sig")
    corr_ft.to_csv(out_dir / f"{cfg.wave}_04_feature_target_correlations.csv", index=False, encoding="utf-8-sig")
    corr_ff_pearson.to_csv(out_dir / f"{cfg.wave}_05_feature_feature_corr_pearson.csv", encoding="utf-8-sig")
    corr_ff_spearman.to_csv(out_dir / f"{cfg.wave}_06_feature_feature_corr_spearman.csv", encoding="utf-8-sig")
    vif_df.to_csv(out_dir / f"{cfg.wave}_07_vif_check.csv", index=False, encoding="utf-8-sig")
    uni_df.to_csv(out_dir / f"{cfg.wave}_08_univariate_ols.csv", index=False, encoding="utf-8-sig")
    beta_df.to_csv(out_dir / f"{cfg.wave}_09_multivariate_std_beta.csv", index=False, encoding="utf-8-sig")
    mv_metrics_df.to_csv(out_dir / f"{cfg.wave}_10_multivariate_model_metrics.csv", index=False, encoding="utf-8-sig")
    flags.to_csv(out_dir / f"{cfg.wave}_11_pre_model_flags.csv", index=False, encoding="utf-8-sig")


def write_readme(out_dir: Path) -> None:
    text = (
        "建模前檢查輸出說明\n"
        "================\n\n"
        "目的：檢查 8 個 relationship 特徵是否適合用來分析心理健康風險分數（憂鬱總分）。\n"
        "每個波次（W2, W3）各輸出 11 個檔案。\n\n"
        "檔案說明：\n"
        "01_missingness.csv：缺失值比例\n"
        "02_descriptive_stats_complete_cases.csv：完整樣本描述統計\n"
        "03_outlier_iqr_check.csv：IQR 離群值檢查\n"
        "04_feature_target_correlations.csv：特徵與目標分數的 Pearson/Spearman\n"
        "05_feature_feature_corr_pearson.csv：特徵間 Pearson 相關矩陣\n"
        "06_feature_feature_corr_spearman.csv：特徵間 Spearman 相關矩陣\n"
        "07_vif_check.csv：多重共線性（VIF）\n"
        "08_univariate_ols.csv：單一特徵回歸（各自影響）\n"
        "09_multivariate_std_beta.csv：多變量標準化係數（同時納入 8 特徵）\n"
        "10_multivariate_model_metrics.csv：多變量模型 R2 / adj R2\n"
        "11_pre_model_flags.csv：重點風險指標與門檻提醒\n\n"
        "建議流程：\n"
        "先看 11_pre_model_flags -> 04_feature_target_correlations -> 07_vif_check -> 09/10 模型結果。\n"
    )
    (out_dir / "00_README_建模前檢查說明.txt").write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for cfg in CONFIGS:
        run_wave_checks(cfg, OUTPUT_DIR)
    write_readme(OUTPUT_DIR)
    print(f"Done. Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

