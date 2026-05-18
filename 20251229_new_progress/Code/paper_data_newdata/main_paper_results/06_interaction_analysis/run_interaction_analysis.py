from __future__ import annotations

import json
import math
import shutil
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from sklearn.metrics import accuracy_score, roc_auc_score


SCRIPT_PATH = Path(__file__).resolve()
SECTION_DIR = SCRIPT_PATH.parent
PAPER_RESULTS_DIR = SECTION_DIR.parent
ROOT = SCRIPT_PATH.parents[4]
CODE_DIR = ROOT / "Code" / "paper_data_newdata"
TABLES_SCRIPT_DIR = CODE_DIR / "tables" / "scripts"
TABLE1_SCRIPT_DIR = CODE_DIR / "tables" / "table1" / "scripts"
for script_dir in [TABLES_SCRIPT_DIR, TABLE1_SCRIPT_DIR]:
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

import build_table2_table3_drop_decomposition as t23  # noqa: E402
import build_table1_drop_decomposition as t1  # noqa: E402


OUT_DIR = SECTION_DIR / "outputs"
DIAG_DIR = OUT_DIR / "diagnostics"
TEACHER_COMBINED_XLSX = OUT_DIR / "teacher_formula_interaction_models_combined.xlsx"
TEACHER_COMBINED_SUMMARY_MD = OUT_DIR / "TEACHER_FORMULA_INTERACTION_SUMMARY_ZH.md"
TEACHER_COMBINED_DIAGNOSTICS_JSON = DIAG_DIR / "teacher_formula_interaction_diagnostics.json"
ONLINE_ACTIVITY_XLSX = OUT_DIR / "teacher_formula_online_activity_interaction_models.xlsx"
ONLINE_ACTIVITY_SUMMARY_MD = OUT_DIR / "TEACHER_FORMULA_ONLINE_ACTIVITY_INTERACTION_SUMMARY_ZH.md"
ONLINE_ACTIVITY_DIAGNOSTICS_JSON = DIAG_DIR / "teacher_formula_online_activity_interaction_diagnostics.json"
PROBLEMATIC_INTERNET_USE_XLSX = OUT_DIR / "teacher_formula_problematic_internet_use_interaction_models.xlsx"
PROBLEMATIC_INTERNET_USE_SUMMARY_MD = OUT_DIR / "TEACHER_FORMULA_PROBLEMATIC_INTERNET_USE_INTERACTION_SUMMARY_ZH.md"
PROBLEMATIC_INTERNET_USE_DIAGNOSTICS_JSON = DIAG_DIR / "teacher_formula_problematic_internet_use_interaction_diagnostics.json"

TOP20_XLSX = (
    PAPER_RESULTS_DIR
    / "04_feature_importance_top20"
    / "outputs"
    / "lasso_top20_feature_importance_with_categories.xlsx"
)

ONLINE_ACTIVITY_ITEMS_W2 = ["v21_3", "v21_4", "v21_5", "v21_6"]
PROBLEMATIC_INTERNET_USE_FEATURE_CODE = "v28"
PROBLEMATIC_INTERNET_USE_MODEL_COLUMN = "feature_v28"
INTERPERSONAL_SPECS = t1.INTERPERSONAL_TABLE1_FEATURES
INTERPERSONAL_VERSION = "observed_count"

MODERATOR_SPECS = [
    {
        "id": "online_activity",
        "name": "Online Activity",
        "high_label": "High Online Activity",
        "low_label": "Low Online Activity",
        "high_group_text": "high-online group",
        "low_group_text": "low-online group",
        "xlsx": ONLINE_ACTIVITY_XLSX,
        "summary_md": ONLINE_ACTIVITY_SUMMARY_MD,
        "diagnostics_json": ONLINE_ACTIVITY_DIAGNOSTICS_JSON,
        "definition_sheet_name": "OnlineActivityDefinition",
        "definition_label": "W2 Online Activity",
        "main_question": "Among the LASSO top 20 features from section 04, which features are risk-amplifying or protective among high-online-activity students?",
        "model_description": "Distress ~ LASSO Top20 Feature + W2 High Online Activity + Feature x W2 High Online Activity + Gender.",
        "skip_feature_codes": set(),
    },
    {
        "id": "problematic_internet_use",
        "name": "Problematic Internet Use",
        "high_label": "High Problematic Internet Use",
        "low_label": "Low Problematic Internet Use",
        "high_group_text": "high-problematic-internet-use group",
        "low_group_text": "low-problematic-internet-use group",
        "xlsx": PROBLEMATIC_INTERNET_USE_XLSX,
        "summary_md": PROBLEMATIC_INTERNET_USE_SUMMARY_MD,
        "diagnostics_json": PROBLEMATIC_INTERNET_USE_DIAGNOSTICS_JSON,
        "definition_sheet_name": "PIUDefinition",
        "definition_label": "W2 Problematic Internet Use / Internet Dependence",
        "main_question": "Among the LASSO top 20 features from section 04, which features are risk-amplifying or protective among students with high problematic internet use?",
        "model_description": "Distress ~ LASSO Top20 Feature + W2 High Problematic Internet Use + Feature x W2 High Problematic Internet Use + Gender.",
        "skip_feature_codes": {PROBLEMATIC_INTERNET_USE_FEATURE_CODE},
    },
]

TASKS = [
    {
        "Task": "W2 -> W2",
        "Feature Wave": "W2",
        "Target Wave": "W2",
        "Feature Target Group": "v55",
        "Target Items": t23.TARGET_W2_ITEMS,
    },
    {
        "Task": "W2 -> W3",
        "Feature Wave": "W2",
        "Target Wave": "W3",
        "Feature Target Group": "54",
        "Target Items": t23.TARGET_W3_ITEMS,
    },
]

def reset_outputs() -> None:
    out_resolved = OUT_DIR.resolve()
    section_resolved = SECTION_DIR.resolve()
    if out_resolved.parent != section_resolved:
        raise RuntimeError(f"Refusing to remove unexpected output path: {out_resolved}")
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    DIAG_DIR.mkdir(parents=True, exist_ok=True)


def load_project_inputs() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    merged_path = t23.core.pick_first_existing_path(t23.core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")
    for col in ["Year", "Group_ID", "Question_ID"]:
        if col in merged.columns:
            merged[col] = merged[col].astype(str).str.strip()
    datasets = {
        "W2": t23.core.normalize_student_id(pd.read_csv(t23.W2_DATA, encoding="utf-8-sig", low_memory=False)),
        "W3": t23.core.normalize_student_id(pd.read_csv(t23.W3_DATA, encoding="utf-8-sig", low_memory=False)),
    }
    return merged, datasets


def make_high_online_activity_w2(w2: pd.DataFrame) -> tuple[pd.Series, pd.Series, dict[str, Any]]:
    values = w2[ONLINE_ACTIVITY_ITEMS_W2].apply(pd.to_numeric, errors="coerce")
    complete = values.notna().sum(axis=1).eq(len(ONLINE_ACTIVITY_ITEMS_W2))
    score = values.sum(axis=1, min_count=len(ONLINE_ACTIVITY_ITEMS_W2))
    median = float(score.loc[complete].median(skipna=True))
    binary = pd.Series(np.nan, index=w2.index, dtype=float)
    binary.loc[complete] = score.loc[complete].gt(median).astype(float)
    diag = {
        "online_activity_items": ONLINE_ACTIVITY_ITEMS_W2,
        "online_activity_definition": "sum(v21_3 to v21_6) > W2 median",
        "online_activity_complete_rows": int(complete.sum()),
        "online_activity_median": median,
        "high_online_n": int(binary.eq(1).sum()),
        "low_online_n": int(binary.eq(0).sum()),
        "missing_online_n": int(binary.isna().sum()),
    }
    return score, binary, diag


def make_high_problematic_internet_use_w2(X: pd.DataFrame) -> tuple[pd.Series, pd.Series, dict[str, Any]]:
    if PROBLEMATIC_INTERNET_USE_MODEL_COLUMN not in X.columns:
        raise KeyError(f"Missing {PROBLEMATIC_INTERNET_USE_MODEL_COLUMN}; cannot build v28 median split.")
    score = pd.to_numeric(X[PROBLEMATIC_INTERNET_USE_MODEL_COLUMN], errors="coerce")
    complete = score.notna()
    median = float(score.loc[complete].median(skipna=True))
    binary = pd.Series(np.nan, index=X.index, dtype=float)
    binary.loc[complete] = score.loc[complete].gt(median).astype(float)
    diag = {
        "problematic_internet_use_feature_code": PROBLEMATIC_INTERNET_USE_FEATURE_CODE,
        "problematic_internet_use_model_column": PROBLEMATIC_INTERNET_USE_MODEL_COLUMN,
        "problematic_internet_use_definition": "feature_v28 > W2 median",
        "problematic_internet_use_complete_rows": int(complete.sum()),
        "problematic_internet_use_median": median,
        "high_problematic_internet_use_n": int(binary.eq(1).sum()),
        "low_problematic_internet_use_n": int(binary.eq(0).sum()),
        "missing_problematic_internet_use_n": int(binary.isna().sum()),
        "skipped_self_interaction_feature_code": PROBLEMATIC_INTERNET_USE_FEATURE_CODE,
        "skipped_self_interaction_reason": "v28 is used as the moderator split, so v28 itself is excluded as a focal feature in this moderator analysis.",
    }
    return score, binary, diag


def infer_category(code: str) -> str:
    if code.startswith("v54") or code == "v52":
        return "SEL / Resilience"
    if code in {"v5", "v6", "v19"}:
        return "Family / Parenting"
    if code.startswith(("v22", "v23", "v25", "v26", "v27")) or code in {"v28", "v49"}:
        return "Online / Digital Life"
    if code in {"v34", "v36", "v38", "v40"}:
        return "Bullying / Victimization"
    if code == "v42":
        return "Delinquency / Risk Behavior"
    return "Other"


def load_top20_features(feature_defs: pd.DataFrame) -> pd.DataFrame:
    if not TOP20_XLSX.exists():
        raise FileNotFoundError(f"Missing LASSO top20 workbook: {TOP20_XLSX}")
    defs = feature_defs.copy()
    defs["feature_code"] = defs["feature_code"].astype(str)
    top20 = pd.read_excel(TOP20_XLSX, sheet_name="LASSO_Top20_Combined")
    top20["Feature Code"] = top20["Feature Code"].astype(str)
    top20 = top20.sort_values(["Task", "Rank by Abs Std. B", "Feature Code"])
    rows: list[dict[str, Any]] = []
    for _, top in top20.iterrows():
        code = str(top["Feature Code"])
        match_def = defs[defs["feature_code"].eq(code)]
        if match_def.empty:
            continue
        feature_meta = match_def.iloc[0].to_dict()
        rows.append(
            {
                "Task": top["Task"],
                "Feature Code": code,
                "Variable": top.get("Variable", feature_meta.get("feature_name", code)),
                "Model Column": feature_meta.get("model_column", f"feature_{code}"),
                "Category": top.get("Category", infer_category(code)),
                "LASSO Top20 Rank": top.get("Rank by Abs Std. B", np.nan),
                "LASSO Std. B": top.get("Std. B", np.nan),
                "LASSO Relative Importance %": top.get("Relative Importance %", np.nan),
                "LASSO Direction": top.get("Direction", ""),
                "Selected by LASSO": top.get("Selected by LASSO", np.nan),
                "Is Interpersonal Feature": top.get("Is Interpersonal Feature", np.nan),
                "Items": top.get("Items", feature_meta.get("items", "")),
                "Source Type": feature_meta.get("source_type", ""),
            }
        )
    return pd.DataFrame(rows)


def make_target_for_task(
    task: dict[str, Any],
    datasets: dict[str, pd.DataFrame],
    feature_df: pd.DataFrame,
) -> tuple[pd.Series, dict[str, Any]]:
    target_df = datasets[task["Target Wave"]]
    _, y_raw, diag = t23.make_target(target_df, task["Target Items"])
    target_map = pd.DataFrame({"student_id": target_df["student_id"], "target": y_raw}).drop_duplicates("student_id", keep="first")
    y = feature_df[["student_id"]].merge(target_map, on="student_id", how="left")["target"]
    y.index = feature_df.index
    return y, diag


def is_binary_series(values: pd.Series) -> bool:
    unique = pd.to_numeric(values, errors="coerce").dropna().unique()
    if len(unique) == 0:
        return False
    return set(float(v) for v in unique).issubset({0.0, 1.0})


def prepare_model_frame(
    task: dict[str, Any],
    feature_df: pd.DataFrame,
    X: pd.DataFrame,
    y: pd.Series,
    high_online: pd.Series,
    feature: pd.Series,
    feature_code: str,
    feature_name: str,
    moderator_spec: dict[str, Any],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = pd.DataFrame(
        {
            "student_id": feature_df["student_id"],
            "y": pd.to_numeric(y, errors="coerce"),
            "high_online": pd.to_numeric(high_online, errors="coerce"),
            "feature_raw": pd.to_numeric(feature, errors="coerce"),
        },
        index=feature_df.index,
    )
    if "feature_v1_male" in X.columns and feature_code != "v1_male":
        frame["gender_male"] = pd.to_numeric(X["feature_v1_male"], errors="coerce")

    required = ["y", "high_online", "feature_raw"]
    if "gender_male" in frame.columns:
        required.append("gender_male")
    frame = frame.dropna(subset=required).copy()

    binary = is_binary_series(frame["feature_raw"])
    if binary:
        frame["feature_model"] = frame["feature_raw"]
        scale_note = "binary_0_1"
        raw_mean = float(frame["feature_raw"].mean())
        raw_sd = float(frame["feature_raw"].std(ddof=0)) if len(frame) > 1 else np.nan
    else:
        raw_mean = float(frame["feature_raw"].mean())
        raw_sd = float(frame["feature_raw"].std(ddof=0))
        if raw_sd == 0 or pd.isna(raw_sd):
            frame["feature_model"] = np.nan
        else:
            frame["feature_model"] = (frame["feature_raw"] - raw_mean) / raw_sd
        scale_note = "z_score"

    frame = frame.dropna(subset=["feature_model"]).copy()
    frame["feature_x_high_online"] = frame["feature_model"] * frame["high_online"]

    diag = {
        "Task": task["Task"],
        "Moderator": moderator_spec["name"],
        "Feature": feature_name,
        "Feature Code": feature_code,
        "N model rows": int(len(frame)),
        "Target positive n": int(frame["y"].eq(1).sum()),
        "Target negative n": int(frame["y"].eq(0).sum()),
        f"{moderator_spec['high_label']} n": int(frame["high_online"].eq(1).sum()),
        f"{moderator_spec['low_label']} n": int(frame["high_online"].eq(0).sum()),
        "Feature scale": scale_note,
        "Feature raw mean": raw_mean,
        "Feature raw SD": raw_sd,
        "Feature raw min": float(frame["feature_raw"].min()) if len(frame) else np.nan,
        "Feature raw max": float(frame["feature_raw"].max()) if len(frame) else np.nan,
    }
    return frame, diag


def fit_interaction_logit(frame: pd.DataFrame) -> tuple[Any | None, str, pd.DataFrame, list[str]]:
    terms = ["feature_model", "high_online", "feature_x_high_online"]
    if "gender_male" in frame.columns and frame["gender_male"].nunique(dropna=True) > 1:
        terms.append("gender_male")
    model_df = frame.dropna(subset=["y"] + terms).copy()
    if len(model_df) < 100 or model_df["y"].nunique() < 2:
        return None, "insufficient_n_or_target_variation", model_df, terms
    for term in terms:
        if model_df[term].nunique(dropna=True) < 2:
            return None, f"insufficient_variation: {term}", model_df, terms
    try:
        fit = sm.Logit(model_df["y"], sm.add_constant(model_df[terms], has_constant="add")).fit(disp=False, maxiter=300)
        return fit, "ok", model_df, terms
    except Exception as exc:
        try:
            fit = sm.GLM(
                model_df["y"],
                sm.add_constant(model_df[terms], has_constant="add"),
                family=sm.families.Binomial(),
            ).fit()
            return fit, f"glm_fallback_after_logit_error: {type(exc).__name__}", model_df, terms
        except Exception as exc2:
            return None, f"fit_failed: {type(exc).__name__}; glm_failed: {type(exc2).__name__}", model_df, terms


def normal_p_from_z(z: float) -> float:
    if pd.isna(z):
        return np.nan
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def term_stats(fit: Any | None, term: str) -> dict[str, float]:
    if fit is None or term not in fit.params.index:
        return {"B": np.nan, "SE": np.nan, "p-value": np.nan}
    return {
        "B": float(fit.params[term]),
        "SE": float(fit.bse[term]),
        "p-value": float(fit.pvalues[term]),
    }


def high_online_slope_stats(fit: Any | None) -> dict[str, float]:
    if fit is None or "feature_model" not in fit.params.index or "feature_x_high_online" not in fit.params.index:
        return {"B": np.nan, "SE": np.nan, "p-value": np.nan}
    b = float(fit.params["feature_model"] + fit.params["feature_x_high_online"])
    cov = fit.cov_params()
    var = (
        float(cov.loc["feature_model", "feature_model"])
        + float(cov.loc["feature_x_high_online", "feature_x_high_online"])
        + 2.0 * float(cov.loc["feature_model", "feature_x_high_online"])
    )
    se = math.sqrt(var) if var >= 0 else np.nan
    z = b / se if se and not pd.isna(se) else np.nan
    return {"B": b, "SE": se, "p-value": normal_p_from_z(z)}


def safe_auc(y: pd.Series, prob: pd.Series) -> float:
    try:
        if y.nunique(dropna=True) < 2:
            return np.nan
        return float(roc_auc_score(y, prob))
    except Exception:
        return np.nan


def model_metrics(fit: Any | None, model_df: pd.DataFrame, terms: list[str]) -> dict[str, float]:
    if fit is None or model_df.empty:
        return {"AUC apparent": np.nan, "Accuracy apparent": np.nan}
    prob = pd.Series(fit.predict(sm.add_constant(model_df[terms], has_constant="add")), index=model_df.index)
    return {
        "AUC apparent": safe_auc(model_df["y"], prob),
        "Accuracy apparent": float(accuracy_score(model_df["y"], prob.ge(0.5).astype(int))),
    }


def moderator_effect_at_feature_levels(fit: Any | None, moderator_spec: dict[str, Any]) -> list[dict[str, Any]]:
    if fit is None:
        return []
    rows: list[dict[str, Any]] = []
    interaction = term_stats(fit, "feature_x_high_online")
    moderator = term_stats(fit, "high_online")
    for label, feature_value in [("Low feature (-1 SD)", -1.0), ("Mean feature", 0.0), ("High feature (+1 SD)", 1.0)]:
        b = moderator["B"] + interaction["B"] * feature_value
        rows.append(
            {
                "Feature Level": label,
                "Feature Model Value": feature_value,
                f"{moderator_spec['high_label']} B at Feature Level": b,
            }
        )
    return rows


def direction_label(b: float, p: float, group: str) -> str:
    if pd.isna(b) or pd.isna(p):
        return "Not available"
    if p >= 0.05:
        return f"Not statistically clear in {group}"
    if b < 0:
        return f"Protective association in {group}"
    return f"Risk association in {group}"


def interaction_label(low_b: float, high_b: float, diff_b: float, p: float, high_label: str) -> str:
    if pd.isna(low_b) or pd.isna(high_b) or pd.isna(diff_b) or pd.isna(p):
        return "Not available"
    if p >= 0.10:
        return "No clear high-vs-low slope difference"

    strength = "significantly" if p < 0.05 else "marginally"
    prefix = f"{high_label} slope is"
    if low_b > 0 and high_b > 0:
        direction = "weaker as a risk association" if abs(high_b) < abs(low_b) else "stronger as a risk association"
    elif low_b < 0 and high_b < 0:
        direction = "stronger as a protective association" if abs(high_b) > abs(low_b) else "weaker as a protective association"
    elif low_b >= 0 and high_b < 0:
        direction = "shifted from risk/non-protective to protective"
    elif low_b < 0 and high_b >= 0:
        direction = "shifted from protective to risk/non-protective"
    else:
        direction = "different from low-online slope"
    return f"{prefix} {strength} {direction}"


def linear_combination_stats(fit: Any | None, weights: dict[str, float]) -> dict[str, float]:
    if fit is None:
        return {"B": np.nan, "SE": np.nan, "p-value": np.nan}
    for term in weights:
        if term not in fit.params.index:
            return {"B": np.nan, "SE": np.nan, "p-value": np.nan}
    b = float(sum(float(weight) * float(fit.params[term]) for term, weight in weights.items()))
    cov = fit.cov_params()
    var = 0.0
    for term_i, weight_i in weights.items():
        for term_j, weight_j in weights.items():
            var += float(weight_i) * float(weight_j) * float(cov.loc[term_i, term_j])
    se = math.sqrt(var) if var >= 0 else np.nan
    z = b / se if se and not pd.isna(se) else np.nan
    return {"B": b, "SE": se, "p-value": normal_p_from_z(z)}


def odds_ratio(b: float) -> float:
    if pd.isna(b):
        return np.nan
    try:
        return float(math.exp(b))
    except OverflowError:
        return np.nan


def teacher_interpretation(b1: float, b3: float, slope0: float, slope1: float, p3: float, high_label: str) -> str:
    if pd.isna(b1) or pd.isna(b3) or pd.isna(slope0) or pd.isna(slope1) or pd.isna(p3):
        return "Not available"
    if p3 < 0.05:
        strength = "significantly"
    elif p3 < 0.10:
        strength = "marginally"
    else:
        return "No clear interaction evidence; b3 is not statistically clear."

    if slope0 > 0 and slope1 > 0:
        direction = "weaker risk slope" if abs(slope1) < abs(slope0) else "stronger risk slope"
    elif slope0 < 0 and slope1 < 0:
        direction = "stronger protective slope" if abs(slope1) > abs(slope0) else "weaker protective slope"
    elif slope0 >= 0 and slope1 < 0:
        direction = "shift from risk/non-protective to protective slope"
    elif slope0 < 0 and slope1 >= 0:
        direction = "shift from protective to risk/non-protective slope"
    else:
        direction = "different slope"
    return f"{high_label}=1 has a {strength} {direction} compared with {high_label}=0."


def build_teacher_row(
    task: dict[str, Any],
    cand: pd.Series,
    frame: pd.DataFrame,
    diag: dict[str, Any],
    moderator_spec: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    fit, status, model_df, terms = fit_interaction_logit(frame)
    metrics = model_metrics(fit, model_df, terms)
    high_label = moderator_spec["high_label"]
    low_label = moderator_spec["low_label"]

    b0 = term_stats(fit, "const")
    b1 = term_stats(fit, "feature_model")
    b2 = term_stats(fit, "high_online")
    b3 = term_stats(fit, "feature_x_high_online")
    intercept0 = b0
    intercept1 = linear_combination_stats(fit, {"const": 1.0, "high_online": 1.0})
    slope0 = b1
    slope1 = linear_combination_stats(fit, {"feature_model": 1.0, "feature_x_high_online": 1.0})
    gender = term_stats(fit, "gender_male") if "gender_male" in terms else {"B": np.nan, "SE": np.nan, "p-value": np.nan}

    common = {
        "Task": task["Task"],
        "Moderator": moderator_spec["name"],
        "Moderator High Group Label": high_label,
        "Moderator Low Group Label": low_label,
        "Feature": cand["Variable"],
        "Feature Code": cand["Feature Code"],
        "Category": cand["Category"],
        "Feature scale": diag["Feature scale"],
        "N": int(len(model_df)),
        "Target positive n": int(model_df["y"].eq(1).sum()) if not model_df.empty else 0,
        "Target negative n": int(model_df["y"].eq(0).sum()) if not model_df.empty else 0,
        f"{high_label} n": int(model_df["high_online"].eq(1).sum()) if not model_df.empty else 0,
        f"{low_label} n": int(model_df["high_online"].eq(0).sum()) if not model_df.empty else 0,
        "LASSO Top20 Rank": cand.get("LASSO Top20 Rank", np.nan),
        "LASSO Std. B": cand.get("LASSO Std. B", np.nan),
        "LASSO Relative Importance %": cand.get("LASSO Relative Importance %", np.nan),
        "LASSO Direction": cand.get("LASSO Direction", ""),
        "Is Interpersonal Feature": cand.get("Is Interpersonal Feature", np.nan),
        "Items": cand.get("Items", ""),
        "Fit status": status,
        "Model formula": "logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates",
        "Covariate note": "Gender male dummy adjusted when focal feature is not gender; intercept is for gender_male=0 when gender is adjusted.",
    }

    row = {
        **common,
        "b0 Intercept B": b0["B"],
        "b0 Intercept SE": b0["SE"],
        "b0 Intercept p-value": b0["p-value"],
        "b1 Feature Main Effect B": b1["B"],
        "b1 Feature Main Effect SE": b1["SE"],
        "b1 Feature Main Effect p-value": b1["p-value"],
        "b2 Moderator Main Effect B": b2["B"],
        "b2 Moderator Main Effect SE": b2["SE"],
        "b2 Moderator Main Effect p-value": b2["p-value"],
        "b3 Feature x Moderator B": b3["B"],
        "b3 Feature x Moderator SE": b3["SE"],
        "b3 Feature x Moderator p-value": b3["p-value"],
        "Gender Male B": gender["B"],
        "Gender Male SE": gender["SE"],
        "Gender Male p-value": gender["p-value"],
        "Intercept when Moderator=0": intercept0["B"],
        "Intercept when Moderator=0 SE": intercept0["SE"],
        "Intercept when Moderator=0 p-value": intercept0["p-value"],
        "Slope when Moderator=0": slope0["B"],
        "Slope when Moderator=0 SE": slope0["SE"],
        "Slope when Moderator=0 p-value": slope0["p-value"],
        "Intercept when Moderator=1": intercept1["B"],
        "Intercept when Moderator=1 SE": intercept1["SE"],
        "Intercept when Moderator=1 p-value": intercept1["p-value"],
        "Slope when Moderator=1": slope1["B"],
        "Slope when Moderator=1 SE": slope1["SE"],
        "Slope when Moderator=1 p-value": slope1["p-value"],
        "Slope Difference Moderator1 minus Moderator0": b3["B"],
        "Slope Difference p-value": b3["p-value"],
        "OR Slope Moderator=0": odds_ratio(slope0["B"]),
        "OR Slope Moderator=1": odds_ratio(slope1["B"]),
        "OR Interaction b3": odds_ratio(b3["B"]),
        "AUC apparent": metrics["AUC apparent"],
        "Accuracy apparent": metrics["Accuracy apparent"],
        "Teacher Formula Interpretation": teacher_interpretation(
            b1["B"],
            b3["B"],
            slope0["B"],
            slope1["B"],
            b3["p-value"],
            high_label,
        ),
    }

    term_rows = build_coefficient_terms(common, fit, terms, intercept1, slope1, metrics, moderator_spec)
    prediction_rows = build_predicted_probability_rows(common, fit, terms, diag["Feature scale"], moderator_spec)
    return row, term_rows, prediction_rows


def build_coefficient_terms(
    common: dict[str, Any],
    fit: Any | None,
    terms: list[str],
    intercept1: dict[str, float],
    slope1: dict[str, float],
    metrics: dict[str, float],
    moderator_spec: dict[str, Any],
) -> list[dict[str, Any]]:
    if fit is None:
        return [{**common, "Coefficient Label": "", "Raw Term": "", "B": np.nan, "SE": np.nan, "p-value": np.nan, **metrics}]
    labels = {
        "const": "b0 Intercept",
        "feature_model": "b1 Feature Main Effect",
        "high_online": "b2 Moderator Main Effect",
        "feature_x_high_online": "b3 Feature x Moderator",
        "gender_male": "Covariate: Gender Male",
    }
    rows: list[dict[str, Any]] = []
    for term in ["const", "feature_model", "high_online", "feature_x_high_online", "gender_male"]:
        if term not in fit.params.index:
            continue
        st = term_stats(fit, term)
        rows.append({**common, "Coefficient Label": labels[term], "Raw Term": term, "B": st["B"], "SE": st["SE"], "p-value": st["p-value"], **metrics})
    rows.extend(
        [
            {
                **common,
                "Coefficient Label": "Derived: Intercept when Moderator=1 = b0 + b2",
                "Raw Term": "const + high_online",
                "B": intercept1["B"],
                "SE": intercept1["SE"],
                "p-value": intercept1["p-value"],
                **metrics,
            },
            {
                **common,
                "Coefficient Label": "Derived: Slope when Moderator=1 = b1 + b3",
                "Raw Term": "feature_model + feature_x_high_online",
                "B": slope1["B"],
                "SE": slope1["SE"],
                "p-value": slope1["p-value"],
                **metrics,
            },
        ]
    )
    return rows


def inverse_logit(value: float) -> float:
    if pd.isna(value):
        return np.nan
    if value >= 0:
        z = math.exp(-value)
        return float(1 / (1 + z))
    z = math.exp(value)
    return float(z / (1 + z))


def build_predicted_probability_rows(
    common: dict[str, Any],
    fit: Any | None,
    terms: list[str],
    feature_scale: str,
    moderator_spec: dict[str, Any],
) -> list[dict[str, Any]]:
    if fit is None:
        return []
    feature_values = [0.0, 1.0] if feature_scale == "binary_0_1" else [-2.0, -1.0, 0.0, 1.0, 2.0]
    rows: list[dict[str, Any]] = []
    for moderator_value in [0.0, 1.0]:
        for feature_value in feature_values:
            values = {
                "const": 1.0,
                "feature_model": feature_value,
                "high_online": moderator_value,
                "feature_x_high_online": feature_value * moderator_value,
                "gender_male": 0.0,
            }
            linear_predictor = 0.0
            for term, coefficient in fit.params.items():
                linear_predictor += float(coefficient) * float(values.get(term, 0.0))
            rows.append(
                {
                    **common,
                    "Moderator Value": int(moderator_value),
                    "Moderator Group": moderator_spec["high_label"] if moderator_value == 1 else moderator_spec["low_label"],
                    "Feature Model Value": feature_value,
                    "Feature Value Label": "1" if feature_scale == "binary_0_1" and feature_value == 1 else "0" if feature_scale == "binary_0_1" else f"{feature_value:+.0f} SD",
                    "Gender Male Setting": 0 if "gender_male" in terms else np.nan,
                    "Gender Setting Note": "Predicted probability shown at gender_male=0 when gender is an adjustment covariate." if "gender_male" in terms else "No separate gender adjustment in this model.",
                    "Linear Predictor Logit": linear_predictor,
                    "Predicted Probability": inverse_logit(linear_predictor),
                }
            )
    return rows


def build_base_inputs() -> tuple[pd.DataFrame, dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame, dict[str, Any], pd.DataFrame]:
    merged, datasets = load_project_inputs()
    feature_df = datasets["W2"]
    X, feature_defs, feature_diag = t23.build_drop_decomposition_features(feature_df, merged, "W2", "v55")
    X, feature_defs, feature_diag = t1.add_interpersonal_features(
        "W2",
        feature_df,
        X,
        feature_defs,
        feature_diag,
        INTERPERSONAL_SPECS,
        INTERPERSONAL_VERSION,
    )
    candidates = load_top20_features(feature_defs)
    return feature_df, datasets, X, feature_defs, feature_diag, candidates


def build_outputs_for_moderator(
    *,
    moderator_spec: dict[str, Any],
    feature_df: pd.DataFrame,
    datasets: dict[str, pd.DataFrame],
    X: pd.DataFrame,
    feature_defs: pd.DataFrame,
    feature_diag: dict[str, Any],
    candidates: pd.DataFrame,
    moderator_binary: pd.Series,
    moderator_diag: dict[str, Any],
) -> dict[str, pd.DataFrame]:
    coefficient_rows: list[dict[str, Any]] = []
    term_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    diag_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    skip_feature_codes = set(moderator_spec.get("skip_feature_codes", set()))

    for task in TASKS:
        y, target_diag = make_target_for_task(task, datasets, feature_df)
        task_candidates = candidates[candidates["Task"].eq(task["Task"])].copy()
        for _, cand in task_candidates.iterrows():
            feature_code = str(cand["Feature Code"])
            if feature_code in skip_feature_codes:
                skipped = {
                    "Task": task["Task"],
                    "Moderator": moderator_spec["name"],
                    "Feature": cand["Variable"],
                    "Feature Code": feature_code,
                    "Reason": (
                        f"{feature_code} is used to define {moderator_spec['high_label']} / "
                        f"{moderator_spec['low_label']}; self-interaction is excluded."
                    ),
                }
                skipped_rows.append(skipped)
                diag_rows.append({**skipped, "Status": "skipped_self_interaction"})
                continue
            model_col = str(cand["Model Column"])
            if model_col not in X.columns:
                diag_rows.append(
                    {
                        "Task": task["Task"],
                        "Moderator": moderator_spec["name"],
                        "Feature": cand["Variable"],
                        "Feature Code": feature_code,
                        "Status": f"missing model column: {model_col}",
                    }
                )
                continue
            frame, diag = prepare_model_frame(
                task=task,
                feature_df=feature_df,
                X=X,
                y=y,
                high_online=moderator_binary,
                feature=X[model_col],
                feature_code=feature_code,
                feature_name=str(cand["Variable"]),
                moderator_spec=moderator_spec,
            )
            diag = {**diag, **{f"target_{k}": v for k, v in target_diag.items()}}
            diag_rows.append(diag)
            coefficient_row, coefficients_long, predicted = build_teacher_row(task, cand, frame, diag, moderator_spec)
            coefficient_rows.append(coefficient_row)
            term_rows.extend(coefficients_long)
            prediction_rows.extend(predicted)

    coefficients = pd.DataFrame(coefficient_rows)
    terms_long = pd.DataFrame(term_rows)
    predicted_prob = pd.DataFrame(prediction_rows)
    diagnostics = pd.DataFrame(diag_rows)
    skipped_df = pd.DataFrame(skipped_rows)

    if not coefficients.empty:
        coefficients["Interaction significant p<.05"] = pd.to_numeric(coefficients["b3 Feature x Moderator p-value"], errors="coerce").lt(0.05)
        coefficients["Interaction marginal p<.10"] = pd.to_numeric(coefficients["b3 Feature x Moderator p-value"], errors="coerce").lt(0.10)
        coefficients = coefficients.sort_values(
            ["Task", "b3 Feature x Moderator p-value", "Feature Code"],
            ascending=[True, True, True],
        ).reset_index(drop=True)

    readme = pd.DataFrame(
        [
            {
                "Item": "Teacher formula",
                "Description": "logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates.",
            },
            {
                "Item": "Moderator=0 intercept and slope",
                "Description": "Intercept = b0; slope = b1.",
            },
            {
                "Item": "Moderator=1 intercept and slope",
                "Description": "Intercept = b0 + b2; slope = b1 + b3.",
            },
            {
                "Item": "Outcome scale",
                "Description": "Because the outcome is binary high psychological distress, B values are logistic-regression log-odds coefficients.",
            },
            {
                "Item": "Feature scaling",
                "Description": "Continuous features are z-scored; binary features remain 0/1.",
            },
        ]
    )

    return {
        "ReadMe": readme,
        "TeacherFormulaCoefficients": coefficients,
        "CoefficientTermsLong": terms_long,
        "PredictedProbabilities": predicted_prob,
        "LASSOTop20Features": candidates,
        "SkippedFeatures": skipped_df,
        "Diagnostics": diagnostics,
        moderator_spec["definition_sheet_name"]: pd.DataFrame([moderator_diag]),
        "FeatureSetDiagnostics": pd.DataFrame([feature_diag]),
    }


def format_workbook(path: Path) -> None:
    wb = load_workbook(path)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D9E2F3")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = border
        for col_cells in ws.columns:
            letter = get_column_letter(col_cells[0].column)
            max_len = 0
            for cell in col_cells:
                val = "" if cell.value is None else str(cell.value)
                max_len = max(max_len, min(len(val), 80))
            ws.column_dimensions[letter].width = max(12, max_len + 2)
    wb.save(path)


def format_p(value: Any) -> str:
    if pd.isna(value):
        return ""
    value = float(value)
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows available._"
    show = df if max_rows is None else df.head(max_rows)
    out = show.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            if "p-value" in col:
                out[col] = out[col].map(format_p)
            else:
                out[col] = out[col].map(lambda v: "" if pd.isna(v) else f"{float(v):.4f}")
    return out.to_markdown(index=False)


def formula_explanation(row: pd.Series, moderator_spec: dict[str, Any]) -> list[str]:
    feature = str(row["Feature"])
    task = str(row["Task"])
    high_label = str(moderator_spec["high_label"])
    low_label = str(moderator_spec["low_label"])
    b0 = float(row["b0 Intercept B"])
    b1 = float(row["b1 Feature Main Effect B"])
    b2 = float(row["b2 Moderator Main Effect B"])
    b3 = float(row["b3 Feature x Moderator B"])
    p3 = float(row["b3 Feature x Moderator p-value"])
    int0 = float(row["Intercept when Moderator=0"])
    slope0 = float(row["Slope when Moderator=0"])
    int1 = float(row["Intercept when Moderator=1"])
    slope1 = float(row["Slope when Moderator=1"])
    or0 = float(row["OR Slope Moderator=0"])
    or1 = float(row["OR Slope Moderator=1"])
    or3 = float(row["OR Interaction b3"])

    if slope0 > 0 and slope1 > 0:
        direction = "兩組都是風險斜率"
        change = "較弱" if abs(slope1) < abs(slope0) else "較強"
    elif slope0 < 0 and slope1 < 0:
        direction = "兩組都是保護斜率"
        change = "較強" if abs(slope1) > abs(slope0) else "較弱"
    elif slope0 >= 0 and slope1 < 0:
        direction = "低組為風險或接近無效，高組轉為保護斜率"
        change = "方向改變"
    elif slope0 < 0 and slope1 >= 0:
        direction = "低組為保護斜率，高組轉為風險或接近無效"
        change = "方向改變"
    else:
        direction = "兩組斜率方向不同"
        change = "不同"

    return [
        f"### {task}: {feature}",
        "",
        "老師公式：",
        "",
        "```text",
        "logit(P(High Psychological Distress = 1))",
        "= b0 + b1 * Feature + b2 * ModeratorHigh + b3 * Feature * ModeratorHigh + covariates",
        "```",
        "",
        "代入本結果：",
        "",
        "```text",
        f"b0 = {b0:.4f}",
        f"b1 = {b1:.4f}",
        f"b2 = {b2:.4f}",
        f"b3 = {b3:.4f}, p = {format_p(p3)}",
        "",
        "logit(P(High Psychological Distress = 1))",
        f"= {b0:.4f} + ({b1:.4f}) * Feature + ({b2:.4f}) * ModeratorHigh + ({b3:.4f}) * Feature * ModeratorHigh + covariates",
        "```",
        "",
        f"當 `{moderator_spec['name']} = 0`，也就是 `{low_label}`：",
        "",
        "```text",
        f"intercept = b0 = {int0:.4f}",
        f"slope = b1 = {slope0:.4f}",
        "```",
        "",
        f"當 `{moderator_spec['name']} = 1`，也就是 `{high_label}`：",
        "",
        "```text",
        f"intercept = b0 + b2 = {b0:.4f} + {b2:.4f} = {int1:.4f}",
        f"slope = b1 + b3 = {b1:.4f} + {b3:.4f} = {slope1:.4f}",
        "```",
        "",
        "解釋：",
        "",
        f"- `b3 = {b3:.4f}` 且 `p = {format_p(p3)}`，表示 `{high_label}` 會顯著改變 `{feature}` 與高心理困擾之間的斜率。",
        f"- `{low_label}` 中，`{feature}` 每增加 1 SD，高心理困擾的 log-odds 改變 `{slope0:.4f}`，對應 OR = `{or0:.3f}`。",
        f"- `{high_label}` 中，`{feature}` 每增加 1 SD，高心理困擾的 log-odds 改變 `{slope1:.4f}`，對應 OR = `{or1:.3f}`。",
        f"- interaction OR = `exp(b3) = {or3:.3f}`。",
        f"- 整體來看，{direction}；在 `{high_label}` 中，這個 feature 的斜率比 `{low_label}` {change}。",
        "",
    ]


def formula_explanations(significant: pd.DataFrame, moderator_spec: dict[str, Any]) -> str:
    if significant.empty:
        return "_沒有 b3 p < .05 的顯著 interaction 結果。_"
    lines: list[str] = []
    for _, row in significant.iterrows():
        lines.extend(formula_explanation(row, moderator_spec))
    return "\n".join(lines)


def write_summary(sheets: dict[str, pd.DataFrame], moderator_spec: dict[str, Any]) -> None:
    coef = sheets["TeacherFormulaCoefficients"].copy()
    display_cols = [
        "Task",
        "Feature",
        "Category",
        "b1 Feature Main Effect B",
        "b2 Moderator Main Effect B",
        "b3 Feature x Moderator B",
        "b3 Feature x Moderator p-value",
        "Intercept when Moderator=0",
        "Slope when Moderator=0",
        "Intercept when Moderator=1",
        "Slope when Moderator=1",
        "Teacher Formula Interpretation",
    ]
    significant = coef[pd.to_numeric(coef["b3 Feature x Moderator p-value"], errors="coerce").lt(0.05)].copy()
    lines = [
        f"# Teacher Formula Interaction Summary: {moderator_spec['name']}",
        "",
        "## 模型",
        "",
        "`logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates`",
        "",
        "## 老師公式對應",
        "",
        "- Moderator = 0: `intercept = b0`, `slope = b1`。",
        "- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。",
        "- 因為 outcome 是 binary high psychological distress，所以 B 是 log-odds coefficient。",
        "- 連續特徵已標準化為 z-score，因此 slope 表示該特徵每增加 1 SD 的 log-odds 變化。",
        "",
        "## b3 interaction 顯著結果 p < .05",
        "",
        md_table(significant[display_cols] if not significant.empty else significant),
        "",
        "## 顯著結果公式代入與解釋",
        "",
        formula_explanations(significant, moderator_spec),
        "",
        "## Outputs",
        "",
        f"- Workbook: `{moderator_spec['xlsx']}`",
        f"- Diagnostics: `{moderator_spec['diagnostics_json']}`",
    ]
    moderator_spec["summary_md"].write_text("\n".join(lines), encoding="utf-8")


def write_outputs(sheets: dict[str, pd.DataFrame], moderator_spec: dict[str, Any]) -> None:
    output_xlsx = moderator_spec["xlsx"]
    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as writer:
        for sheet, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet[:31])
    format_workbook(output_xlsx)
    write_summary(sheets, moderator_spec)
    payload = {
        "moderator": moderator_spec["name"],
        "output_xlsx": str(output_xlsx),
        "summary_md": str(moderator_spec["summary_md"]),
        "top20_xlsx": str(TOP20_XLSX),
        "sheets": {name: {"rows": int(len(df)), "columns": list(df.columns)} for name, df in sheets.items()},
    }
    moderator_spec["diagnostics_json"].write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_combined_outputs(all_sheets: dict[str, dict[str, pd.DataFrame]]) -> None:
    with pd.ExcelWriter(TEACHER_COMBINED_XLSX, engine="openpyxl") as writer:
        for moderator_id, sheets in all_sheets.items():
            prefix = "Online" if moderator_id == "online_activity" else "PIU"
            sheets["TeacherFormulaCoefficients"].to_excel(writer, index=False, sheet_name=f"{prefix}_Coefficients")
            sheets["PredictedProbabilities"].to_excel(writer, index=False, sheet_name=f"{prefix}_PredictedProb")
            sheets["SkippedFeatures"].to_excel(writer, index=False, sheet_name=f"{prefix}_Skipped")
        pd.concat(
            [sheets["TeacherFormulaCoefficients"] for sheets in all_sheets.values()],
            ignore_index=True,
        ).to_excel(writer, index=False, sheet_name="All_Coefficients")
    format_workbook(TEACHER_COMBINED_XLSX)
    payload = {
        "combined_xlsx": str(TEACHER_COMBINED_XLSX),
        "moderators": list(all_sheets.keys()),
        "rows": {k: int(len(v["TeacherFormulaCoefficients"])) for k, v in all_sheets.items()},
    }
    TEACHER_COMBINED_DIAGNOSTICS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_combined_summary(all_sheets: dict[str, dict[str, pd.DataFrame]]) -> None:
    lines = [
        "# Teacher Formula Interaction Analysis Summary",
        "",
        "## 這次 06 的重點",
        "",
        "這版 06 依照老師指定的公式重新整理：",
        "",
        "`logit(P(High Psychological Distress=1)) = b0 + b1*Feature + b2*ModeratorHigh + b3*Feature*ModeratorHigh + covariates`",
        "",
        "- Moderator = 0: `intercept = b0`, `slope = b1`。",
        "- Moderator = 1: `intercept = b0 + b2`, `slope = b1 + b3`。",
        "- `b3` 是真正的 interaction effect，檢查 moderator 是否改變 feature 對 high psychological distress 的斜率。",
        "",
    ]
    display_cols = [
        "Task",
        "Moderator",
        "Feature",
        "b1 Feature Main Effect B",
        "b2 Moderator Main Effect B",
        "b3 Feature x Moderator B",
        "b3 Feature x Moderator p-value",
        "Slope when Moderator=0",
        "Slope when Moderator=1",
        "Teacher Formula Interpretation",
    ]
    for moderator_id, sheets in all_sheets.items():
        coef = sheets["TeacherFormulaCoefficients"].copy()
        significant = coef[pd.to_numeric(coef["b3 Feature x Moderator p-value"], errors="coerce").lt(0.05)]
        marginal = coef[
            pd.to_numeric(coef["b3 Feature x Moderator p-value"], errors="coerce").between(0.05, 0.10, inclusive="left")
        ]
        lines.extend(
            [
                f"## {moderator_id}",
                "",
                "### b3 interaction 顯著結果 p < .05",
                "",
                md_table(significant[display_cols] if not significant.empty else significant),
                "",
                "### b3 interaction 邊緣顯著結果 .05 <= p < .10",
                "",
                md_table(marginal[display_cols] if not marginal.empty else marginal),
                "",
            ]
        )
    lines.extend(
        [
            "## Outputs",
            "",
            f"- Combined workbook: `{TEACHER_COMBINED_XLSX}`",
            f"- Online Activity workbook: `{ONLINE_ACTIVITY_XLSX}`",
            f"- Problematic Internet Use workbook: `{PROBLEMATIC_INTERNET_USE_XLSX}`",
        ]
    )
    TEACHER_COMBINED_SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    reset_outputs()
    feature_df, datasets, X, feature_defs, feature_diag, candidates = build_base_inputs()
    _, high_online, online_diag = make_high_online_activity_w2(feature_df)
    _, high_problematic, problematic_diag = make_high_problematic_internet_use_w2(X)
    moderator_inputs = {
        "online_activity": (high_online, online_diag),
        "problematic_internet_use": (high_problematic, problematic_diag),
    }

    all_sheets: dict[str, dict[str, pd.DataFrame]] = {}
    for moderator_spec in MODERATOR_SPECS:
        moderator_binary, moderator_diag = moderator_inputs[moderator_spec["id"]]
        sheets = build_outputs_for_moderator(
            moderator_spec=moderator_spec,
            feature_df=feature_df,
            datasets=datasets,
            X=X,
            feature_defs=feature_defs,
            feature_diag=feature_diag,
            candidates=candidates,
            moderator_binary=moderator_binary,
            moderator_diag=moderator_diag,
        )
        write_outputs(sheets, moderator_spec)
        all_sheets[moderator_spec["id"]] = sheets
        print(f"Wrote {moderator_spec['xlsx']}")
        print(f"Wrote {moderator_spec['summary_md']}")
        print(f"Wrote {moderator_spec['diagnostics_json']}")
        main_cols = [
            "Task",
            "Feature",
            "b1 Feature Main Effect B",
            "b2 Moderator Main Effect B",
            "b3 Feature x Moderator B",
            "b3 Feature x Moderator p-value",
            "Slope when Moderator=0",
            "Slope when Moderator=1",
        ]
        print(f"\nTop teacher-formula rows for {moderator_spec['name']}:")
        print(sheets["TeacherFormulaCoefficients"][main_cols].head(12).to_string(index=False))

    write_combined_outputs(all_sheets)
    write_combined_summary(all_sheets)
    print(f"Wrote {TEACHER_COMBINED_XLSX}")
    print(f"Wrote {TEACHER_COMBINED_SUMMARY_MD}")
    print(f"Wrote {TEACHER_COMBINED_DIAGNOSTICS_JSON}")

if __name__ == "__main__":
    main()


