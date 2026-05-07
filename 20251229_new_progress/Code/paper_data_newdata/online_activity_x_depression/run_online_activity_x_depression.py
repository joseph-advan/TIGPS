from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


THIS_FILE = Path(__file__).resolve()
OUT_DIR = THIS_FILE.parent
BASE_DIR = THIS_FILE.parents[3]

W2_PATH = BASE_DIR / r"Data\testing_clean\W2\TIGPS_W2_studentdata_ver6.csv"
W3_PATH = BASE_DIR / r"Data\testing_clean\W3\TIGPS_W3_student_studentdata_ver5.csv"

REVERSE_CONFIG_PATH = OUT_DIR / "reverse_items_config.json"
FEATURE_W2_PATH = OUT_DIR / "wave_features_w2.csv"
FEATURE_W3_PATH = OUT_DIR / "wave_features_w3.csv"
STAGE1_PATH = OUT_DIR / "stage1_main_effects.csv"
STAGE2_PATH = OUT_DIR / "stage2_cross_year.csv"
STAGE3_WITHIN_PATH = OUT_DIR / "stage3_within_highrisk_protective_effects.csv"
STAGE3_INT_PATH = OUT_DIR / "stage3_interaction_models.csv"
REPORT_PATH = OUT_DIR / "analysis_report.md"


@dataclass(frozen=True)
class WaveConfig:
    wave: str
    data_path: Path
    class_col: str | None
    seat_col: str
    online_activity_cols: list[str]
    nomination_cols: list[str]
    depression_cols: list[str]
    family_cols: list[str]
    self_worth_cols: list[str]


W2_CFG = WaveConfig(
    wave="w2",
    data_path=W2_PATH,
    class_col="class",
    seat_col="v13",
    online_activity_cols=["v21_3", "v21_4", "v21_5", "v21_6"],
    nomination_cols=[f"v14_1_0{i}" for i in range(1, 6)] + [f"v14_2_0{i}" for i in range(1, 6)],
    depression_cols=[f"v55_{i}" for i in range(1, 15)],
    family_cols=[f"v5_{i}" for i in range(1, 7)],
    self_worth_cols=[f"v52_{i}" for i in range(1, 4)],
)

W3_CFG = WaveConfig(
    wave="w3",
    data_path=W3_PATH,
    class_col=None,  # W3 has no clean class column; mapped by student_id from W2.
    seat_col="7",
    online_activity_cols=[f"21-{i}" for i in range(3, 7)],
    nomination_cols=[f"8-1_{i}" for i in range(0, 5)] + [f"8-4_{i}" for i in range(0, 5)],
    depression_cols=[f"54-{i}" for i in range(1, 15)],
    family_cols=[f"4-{i}" for i in range(1, 7)],
    self_worth_cols=[f"52-{i}" for i in range(1, 4)],
)


DEFAULT_REVERSE_CONFIG: dict[str, Any] = {
    "w2": {
        "family": {"reverse_items": [], "min": 1, "max": 4},
        "self_worth": {"reverse_items": [], "min": 1, "max": 4},
        "depression": {"reverse_items": [], "min": 1, "max": 5},
    },
    "w3": {
        "family": {"reverse_items": [], "min": 1, "max": 4},
        "self_worth": {"reverse_items": [], "min": 1, "max": 4},
        "depression": {"reverse_items": [], "min": 1, "max": 5},
    },
}


def load_reverse_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_REVERSE_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
        return DEFAULT_REVERSE_CONFIG
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("reverse_items_config.json must be a JSON object.")
    return data


def normalize_student_id(df: pd.DataFrame) -> pd.DataFrame:
    if "student_id" not in df.columns:
        raise KeyError("Missing student_id column.")
    out = df.copy()
    sid = out["student_id"].astype(str).str.strip()
    sid = sid.replace({"": np.nan, "nan": np.nan, "None": np.nan, "<NA>": np.nan})
    out["student_id"] = sid
    out = out[out["student_id"].notna()].copy()
    out = out.drop_duplicates(subset=["student_id"], keep="first").copy()
    return out


def normalize_int_token(v: Any, *, allow_zero: bool = False) -> str | None:
    if pd.isna(v):
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        f = float(s)
        if not np.isfinite(f):
            return None
        i = int(round(f))
        if abs(f - i) > 1e-9:
            return None
        if i < 0:
            return None
        if i == 0 and not allow_zero:
            return None
        return str(i)
    except Exception:
        return None


def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def strict_row_mean(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    return df[cols].apply(pd.to_numeric, errors="coerce").mean(axis=1, skipna=False)


def strict_row_sum(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    return df[cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, skipna=False)


def apply_reverse_items(
    df: pd.DataFrame, cols: list[str], reverse_items: list[str], min_val: float, max_val: float
) -> pd.DataFrame:
    out = df.copy()
    existing = [c for c in reverse_items if c in out.columns and c in cols]
    for c in existing:
        x = pd.to_numeric(out[c], errors="coerce")
        out[c] = np.where(x.notna(), min_val + max_val - x, np.nan)
    return out


def cohen_d(x: pd.Series, y: pd.Series) -> float:
    x = pd.to_numeric(x, errors="coerce").dropna()
    y = pd.to_numeric(y, errors="coerce").dropna()
    n1, n2 = len(x), len(y)
    if n1 < 2 or n2 < 2:
        return float("nan")
    s1, s2 = x.std(ddof=1), y.std(ddof=1)
    pooled = ((n1 - 1) * s1 * s1 + (n2 - 1) * s2 * s2) / (n1 + n2 - 2)
    if pooled <= 0 or pd.isna(pooled):
        return float("nan")
    return float((x.mean() - y.mean()) / np.sqrt(pooled))


def compare_groups(
    values_low: pd.Series,
    values_high: pd.Series,
    *,
    analysis_id: str,
    stage: str,
    wave: str,
    group_def: str,
) -> dict[str, Any]:
    a = pd.to_numeric(values_low, errors="coerce").dropna()
    b = pd.to_numeric(values_high, errors="coerce").dropna()
    out: dict[str, Any] = {
        "analysis_id": analysis_id,
        "stage": stage,
        "wave": wave,
        "group_def": group_def,
        "n_low": int(len(a)),
        "n_high": int(len(b)),
        "mean_low": float(a.mean()) if len(a) > 0 else np.nan,
        "mean_high": float(b.mean()) if len(b) > 0 else np.nan,
        "sd_low": float(a.std(ddof=1)) if len(a) > 1 else np.nan,
        "sd_high": float(b.std(ddof=1)) if len(b) > 1 else np.nan,
        "mean_diff_high_minus_low": np.nan,
        "t_stat_welch": np.nan,
        "p_value_welch": np.nan,
        "cohen_d": np.nan,
    }
    if len(a) >= 2 and len(b) >= 2:
        t = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
        out["mean_diff_high_minus_low"] = float(b.mean() - a.mean())
        out["t_stat_welch"] = float(t.statistic)
        out["p_value_welch"] = float(t.pvalue)
        out["cohen_d"] = cohen_d(a, b)
    return out


def build_nomination_counts(df: pd.DataFrame, class_col: str, seat_col: str, nom_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    out["class_norm"] = out[class_col].map(lambda v: normalize_int_token(v, allow_zero=False))
    out["seat_norm"] = out[seat_col].map(lambda v: normalize_int_token(v, allow_zero=False))

    incoming: dict[tuple[str, str], int] = {}
    out_counts: list[int] = []
    for _, row in out.iterrows():
        cls = row["class_norm"]
        c = 0
        for col in nom_cols:
            seat = normalize_int_token(row.get(col), allow_zero=False)
            if seat is None:
                continue
            c += 1
            if cls is not None:
                key = (cls, seat)
                incoming[key] = incoming.get(key, 0) + 1
        out_counts.append(c)
    out["nom_out_count"] = out_counts

    in_counts: list[int] = []
    for _, row in out.iterrows():
        cls = row["class_norm"]
        seat = row["seat_norm"]
        if cls is None or seat is None:
            in_counts.append(np.nan)
        else:
            in_counts.append(int(incoming.get((cls, seat), 0)))
    out["nom_in_count"] = in_counts
    out["nom_total_count"] = out["nom_out_count"] + out["nom_in_count"]
    return out


def zscore_by_class(df: pd.DataFrame, class_col: str, value_col: str) -> pd.Series:
    x = pd.to_numeric(df[value_col], errors="coerce")
    g = df[class_col]
    mean = x.groupby(g).transform("mean")
    std = x.groupby(g).transform(lambda s: s.std(ddof=0))
    z = (x - mean) / std
    z.loc[(std == 0) & x.notna()] = 0.0
    return z


def require_columns(df: pd.DataFrame, cols: list[str], label: str) -> None:
    miss = [c for c in cols if c not in df.columns]
    if miss:
        raise KeyError(f"{label}: missing columns: {miss}")


def build_wave_features(
    cfg: WaveConfig,
    reverse_cfg: dict[str, Any],
    *,
    class_map_from_w2: pd.Series | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw = pd.read_csv(cfg.data_path, low_memory=False)
    df = normalize_student_id(raw)

    if cfg.class_col is not None:
        require_columns(df, [cfg.class_col], f"{cfg.wave} class")
        df["class_for_nom"] = df[cfg.class_col]
    else:
        if class_map_from_w2 is None:
            raise ValueError("class_map_from_w2 is required for W3 processing.")
        df["class_for_nom"] = df["student_id"].map(class_map_from_w2)

    require_columns(
        df,
        [cfg.seat_col] + cfg.online_activity_cols + cfg.nomination_cols + cfg.depression_cols + cfg.family_cols + cfg.self_worth_cols,
        f"{cfg.wave} variables",
    )

    wave_rev = reverse_cfg.get(cfg.wave, {})
    fam_rev = wave_rev.get("family", {})
    self_rev = wave_rev.get("self_worth", {})
    dep_rev = wave_rev.get("depression", {})

    df = apply_reverse_items(
        df,
        cfg.family_cols,
        list(fam_rev.get("reverse_items", [])),
        float(fam_rev.get("min", 1)),
        float(fam_rev.get("max", 4)),
    )
    df = apply_reverse_items(
        df,
        cfg.self_worth_cols,
        list(self_rev.get("reverse_items", [])),
        float(self_rev.get("min", 1)),
        float(self_rev.get("max", 4)),
    )
    df = apply_reverse_items(
        df,
        cfg.depression_cols,
        list(dep_rev.get("reverse_items", [])),
        float(dep_rev.get("min", 1)),
        float(dep_rev.get("max", 5)),
    )

    df["online_activity_sum"] = strict_row_sum(df, cfg.online_activity_cols)
    df["family_mean"] = strict_row_mean(df, cfg.family_cols)
    df["self_worth_mean"] = strict_row_mean(df, cfg.self_worth_cols)
    df["depression_mean"] = strict_row_mean(df, cfg.depression_cols)

    df = build_nomination_counts(df, "class_for_nom", cfg.seat_col, cfg.nomination_cols)
    df["nom_out_z"] = zscore_by_class(df, "class_norm", "nom_out_count")
    df["nom_in_z"] = zscore_by_class(df, "class_norm", "nom_in_count")
    df["nom_total_z"] = zscore_by_class(df, "class_norm", "nom_total_count")

    activity_med = float(df["online_activity_sum"].median(skipna=True))
    nom_out_z_med = float(df["nom_out_z"].median(skipna=True))
    nom_in_z_med = float(df["nom_in_z"].median(skipna=True))
    nom_total_z_med = float(df["nom_total_z"].median(skipna=True))
    family_med = float(df["family_mean"].median(skipna=True))
    self_worth_med = float(df["self_worth_mean"].median(skipna=True))

    df["high_activity"] = np.where(df["online_activity_sum"].notna(), (df["online_activity_sum"] > activity_med).astype(int), np.nan)
    df["high_nomination_out_main"] = np.where(df["nom_out_z"].notna(), (df["nom_out_z"] > 0).astype(int), np.nan)
    df["high_nomination_in_main"] = np.where(df["nom_in_z"].notna(), (df["nom_in_z"] > 0).astype(int), np.nan)
    df["high_nomination_total_main"] = np.where(df["nom_total_z"].notna(), (df["nom_total_z"] > 0).astype(int), np.nan)
    df["high_nomination_out_median"] = np.where(df["nom_out_z"].notna(), (df["nom_out_z"] > nom_out_z_med).astype(int), np.nan)
    df["high_nomination_in_median"] = np.where(df["nom_in_z"].notna(), (df["nom_in_z"] > nom_in_z_med).astype(int), np.nan)
    df["high_nomination_total_median"] = np.where(
        df["nom_total_z"].notna(), (df["nom_total_z"] > nom_total_z_med).astype(int), np.nan
    )
    df["high_family"] = np.where(df["family_mean"].notna(), (df["family_mean"] > family_med).astype(int), np.nan)
    df["high_self_worth"] = np.where(df["self_worth_mean"].notna(), (df["self_worth_mean"] > self_worth_med).astype(int), np.nan)

    diagnostics = {
        "wave": cfg.wave,
        "n_students": int(len(df)),
        "activity_median": activity_med,
        "nomination_out_z_median": nom_out_z_med,
        "nomination_in_z_median": nom_in_z_med,
        "nomination_total_z_median": nom_total_z_med,
        "family_median": family_med,
        "self_worth_median": self_worth_med,
        "mapped_class_rate": float(df["class_for_nom"].notna().mean() * 100.0),
        "valid_class_rate": float(df["class_norm"].notna().mean() * 100.0),
        "valid_seat_rate": float(df["seat_norm"].notna().mean() * 100.0),
    }
    return df, diagnostics


def run_interaction_models(df: pd.DataFrame, *, wave: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for risk_col in ["high_activity", "high_nomination_out_main", "high_nomination_in_main", "high_nomination_total_main"]:
        for protector_col in ["family_mean", "self_worth_mean"]:
            dat = df[[risk_col, protector_col, "depression_mean"]].copy()
            dat = dat.dropna(axis=0, how="any")
            dat = dat.rename(columns={risk_col: "risk_bin", protector_col: "protect"})
            if len(dat) < 30:
                rows.append(
                    {
                        "wave": wave,
                        "risk_col": risk_col,
                        "protector_col": protector_col,
                        "n_model": int(len(dat)),
                        "interaction_beta": np.nan,
                        "interaction_p": np.nan,
                        "r2": np.nan,
                        "model_error": "too_few_rows",
                    }
                )
                continue
            dat["risk_bin"] = dat["risk_bin"].astype(int)
            dat["protect_c"] = dat["protect"] - dat["protect"].mean()
            try:
                m = smf.ols("depression_mean ~ risk_bin + protect_c + risk_bin:protect_c", data=dat).fit()
                term = "risk_bin:protect_c"
                rows.append(
                    {
                        "wave": wave,
                        "risk_col": risk_col,
                        "protector_col": protector_col,
                        "n_model": int(len(dat)),
                        "interaction_beta": float(m.params.get(term, np.nan)),
                        "interaction_p": float(m.pvalues.get(term, np.nan)),
                        "r2": float(m.rsquared),
                        "model_error": "",
                    }
                )
            except Exception as exc:
                rows.append(
                    {
                        "wave": wave,
                        "risk_col": risk_col,
                        "protector_col": protector_col,
                        "n_model": int(len(dat)),
                        "interaction_beta": np.nan,
                        "interaction_p": np.nan,
                        "r2": np.nan,
                        "model_error": str(exc),
                    }
                )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rev_cfg = load_reverse_config(REVERSE_CONFIG_PATH)

    w2_df, w2_diag = build_wave_features(W2_CFG, rev_cfg)
    class_map = w2_df.set_index("student_id")["class_for_nom"]
    w3_df, w3_diag = build_wave_features(W3_CFG, rev_cfg, class_map_from_w2=class_map)

    stage1_rows: list[dict[str, Any]] = []
    for wave_name, df in [("w2", w2_df), ("w3", w3_df)]:
        a = compare_groups(
            df.loc[df["high_activity"] == 0, "depression_mean"],
            df.loc[df["high_activity"] == 1, "depression_mean"],
            analysis_id=f"{wave_name}_activity_main",
            stage="stage1",
            wave=wave_name,
            group_def="high_activity = online_activity_sum > wave_median",
        )
        b = compare_groups(
            df.loc[df["high_nomination_out_main"] == 0, "depression_mean"],
            df.loc[df["high_nomination_out_main"] == 1, "depression_mean"],
            analysis_id=f"{wave_name}_nomination_out_main",
            stage="stage1",
            wave=wave_name,
            group_def="high_nomination_out_main = class_z_nom_out > 0",
        )
        c = compare_groups(
            df.loc[df["high_nomination_in_main"] == 0, "depression_mean"],
            df.loc[df["high_nomination_in_main"] == 1, "depression_mean"],
            analysis_id=f"{wave_name}_nomination_in_main",
            stage="stage1",
            wave=wave_name,
            group_def="high_nomination_in_main = class_z_nom_in > 0",
        )
        d = compare_groups(
            df.loc[df["high_nomination_total_main"] == 0, "depression_mean"],
            df.loc[df["high_nomination_total_main"] == 1, "depression_mean"],
            analysis_id=f"{wave_name}_nomination_total_main",
            stage="stage1",
            wave=wave_name,
            group_def="high_nomination_total_main = class_z_nom_total > 0",
        )
        stage1_rows.extend([a, b, c, d])

    stage2_rows: list[dict[str, Any]] = []
    stage2_rows.append(
        compare_groups(
            w2_df.loc[w2_df["high_activity"] == 1, "depression_mean"],
            w3_df.loc[w3_df["high_activity"] == 1, "depression_mean"],
            analysis_id="cross_year_high_activity",
            stage="stage2",
            wave="w2_vs_w3",
            group_def="W2 high_activity vs W3 high_activity",
        )
    )
    stage2_rows.append(
        compare_groups(
            w2_df.loc[w2_df["high_nomination_total_main"] == 1, "depression_mean"],
            w3_df.loc[w3_df["high_nomination_total_main"] == 1, "depression_mean"],
            analysis_id="cross_year_high_nomination_total_main",
            stage="stage2",
            wave="w2_vs_w3",
            group_def="W2 high_nomination_total_main vs W3 high_nomination_total_main",
        )
    )

    stage3_within_rows: list[dict[str, Any]] = []
    for wave_name, df in [("w2", w2_df), ("w3", w3_df)]:
        for risk_col in ["high_activity", "high_nomination_out_main", "high_nomination_in_main", "high_nomination_total_main"]:
            risk_df = df[df[risk_col] == 1].copy()
            if risk_df.empty:
                continue
            fam_thr = float(risk_df["family_mean"].median(skipna=True))
            fam_high = np.where(risk_df["family_mean"].notna(), (risk_df["family_mean"] > fam_thr).astype(int), np.nan)
            fam_row = compare_groups(
                risk_df.loc[fam_high == 0, "depression_mean"],
                risk_df.loc[fam_high == 1, "depression_mean"],
                analysis_id=f"{wave_name}_{risk_col}_family",
                stage="stage3_within",
                wave=wave_name,
                group_def=f"within {risk_col}=1, family_mean > subgroup_median",
            )
            fam_row["risk_col"] = risk_col
            fam_row["protector_col"] = "family_mean"
            fam_row["protector_threshold"] = fam_thr
            stage3_within_rows.append(fam_row)

            worth_thr = float(risk_df["self_worth_mean"].median(skipna=True))
            worth_high = np.where(risk_df["self_worth_mean"].notna(), (risk_df["self_worth_mean"] > worth_thr).astype(int), np.nan)
            worth_row = compare_groups(
                risk_df.loc[worth_high == 0, "depression_mean"],
                risk_df.loc[worth_high == 1, "depression_mean"],
                analysis_id=f"{wave_name}_{risk_col}_self_worth",
                stage="stage3_within",
                wave=wave_name,
                group_def=f"within {risk_col}=1, self_worth_mean > subgroup_median",
            )
            worth_row["risk_col"] = risk_col
            worth_row["protector_col"] = "self_worth_mean"
            worth_row["protector_threshold"] = worth_thr
            stage3_within_rows.append(worth_row)

    stage3_int_rows = run_interaction_models(w2_df, wave="w2") + run_interaction_models(w3_df, wave="w3")

    keep_cols = [
        "student_id",
        "class_for_nom",
        "class_norm",
        "seat_norm",
        "online_activity_sum",
        "nom_out_count",
        "nom_in_count",
        "nom_total_count",
        "nom_out_z",
        "nom_in_z",
        "nom_total_z",
        "depression_mean",
        "family_mean",
        "self_worth_mean",
        "high_activity",
        "high_nomination_out_main",
        "high_nomination_in_main",
        "high_nomination_total_main",
        "high_nomination_out_median",
        "high_nomination_in_median",
        "high_nomination_total_median",
        "high_family",
        "high_self_worth",
    ]
    w2_df[keep_cols].to_csv(FEATURE_W2_PATH, index=False, encoding="utf-8-sig")
    w3_df[keep_cols].to_csv(FEATURE_W3_PATH, index=False, encoding="utf-8-sig")
    pd.DataFrame(stage1_rows).to_csv(STAGE1_PATH, index=False, encoding="utf-8-sig")
    pd.DataFrame(stage2_rows).to_csv(STAGE2_PATH, index=False, encoding="utf-8-sig")
    pd.DataFrame(stage3_within_rows).to_csv(STAGE3_WITHIN_PATH, index=False, encoding="utf-8-sig")
    pd.DataFrame(stage3_int_rows).to_csv(STAGE3_INT_PATH, index=False, encoding="utf-8-sig")

    report_lines: list[str] = []
    report_lines.append("# Online Activity x Depression Study Summary")
    report_lines.append("")
    report_lines.append("## Data and core definitions")
    report_lines.append(f"- W2 file: `{W2_PATH}`")
    report_lines.append(f"- W3 file: `{W3_PATH}`")
    report_lines.append("- Nomination count rule: count filled nomination slots (seat number > 0).")
    report_lines.append("- Incoming nomination rule: count how many times a student's seat is nominated within same class.")
    report_lines.append("- Main nomination grouping (3 types, z>0): outgoing / incoming / total nominations.")
    report_lines.append("- Activity grouping: high if online activity sum > wave median.")
    report_lines.append("")
    report_lines.append("## Diagnostics")
    report_lines.append(f"- W2 students: {w2_diag['n_students']}, class valid rate: {w2_diag['valid_class_rate']:.2f}%")
    report_lines.append(f"- W3 students: {w3_diag['n_students']}, class mapped rate: {w3_diag['mapped_class_rate']:.2f}%")
    report_lines.append(f"- W2 activity median: {w2_diag['activity_median']:.4f}")
    report_lines.append(f"- W3 activity median: {w3_diag['activity_median']:.4f}")
    report_lines.append("")
    report_lines.append("## Output files")
    report_lines.append(f"- `{FEATURE_W2_PATH}`")
    report_lines.append(f"- `{FEATURE_W3_PATH}`")
    report_lines.append(f"- `{STAGE1_PATH}`")
    report_lines.append(f"- `{STAGE2_PATH}`")
    report_lines.append(f"- `{STAGE3_WITHIN_PATH}`")
    report_lines.append(f"- `{STAGE3_INT_PATH}`")
    report_lines.append(f"- `{REVERSE_CONFIG_PATH}`")
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8-sig")

    print("Done.")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
