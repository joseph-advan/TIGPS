from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parent

W2_DATA = ROOT / "Data" / "testing_clean" / "W2" / "TIGPS_W2_studentdata_ver6.csv"
W3_DATA = ROOT / "Data" / "testing_clean" / "W3" / "TIGPS_W3_student_studentdata_ver5.csv"
TABLE1_PLAN = ROOT / "Code" / "paper_data_newdata" / "tables" / "table1" / "config" / "table1_variable_plan_draft.csv"
TABLE1_CONFIG = ROOT / "Code" / "paper_data_newdata" / "tables" / "table1" / "config" / "table1_scoring_config.json"
SUBSCALE_CONFIG = ROOT / "Code" / "paper_data_newdata" / "Feature_Decomposition" / "subscale_definitions_w2_w3.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2
LOGIT_CS = np.logspace(-4, 4, 41)
MIN_VALID_FRACTION = 0.5
TARGET_W2_ITEMS = [f"v55_{i}" for i in range(1, 15)]
TARGET_W3_ITEMS = [f"54-{i}" for i in range(1, 15)]

DECOMPOSED_VARIABLE_NAMES = {
    "Online Peer Interaction Anxiety (FOMO)",
    "Social Media Self-Presentation and Online Image Management",
    "Social Media Use: Selective Sharing and Impression Management",
    "Online Social Comparison and Perspective Seeking",
    "Social and Emotional Learning (SEL) Competencies",
}
OUTCOME_VARIABLE_NAME = "Psychological Distress Symptoms (Depression/Anxiety/Self-harm Ideation)"


def parse_columns(value: object) -> list[str]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text.startswith("__"):
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def to_numeric_frame(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df[columns].apply(pd.to_numeric, errors="coerce")


def min_valid_count(n_items: int, min_valid_fraction: float = MIN_VALID_FRACTION) -> int:
    return max(1, int(math.ceil(n_items * min_valid_fraction)))


def apply_reverse(values: pd.DataFrame, reverse_columns: list[str], min_value: float, max_value: float) -> pd.DataFrame:
    out = values.copy()
    for col in reverse_columns:
        if col in out.columns:
            out[col] = min_value + max_value - out[col]
    return out


def scale_score(
    df: pd.DataFrame,
    columns: list[str],
    reverse_columns: list[str] | None = None,
    min_value: float = 1.0,
    max_value: float = 4.0,
    agg: str = "mean",
) -> pd.Series:
    existing = [col for col in columns if col in df.columns]
    if not existing:
        return pd.Series(pd.NA, index=df.index, dtype="Float64")
    values = to_numeric_frame(df, existing)
    if reverse_columns:
        values = apply_reverse(values, reverse_columns, min_value, max_value)
    valid_count = values.notna().sum(axis=1)
    min_valid = min_valid_count(len(existing))
    if agg == "sum":
        score = values.sum(axis=1, min_count=min_valid)
    elif agg == "mean":
        score = values.mean(axis=1, skipna=True)
        score[valid_count < min_valid] = np.nan
    else:
        raise ValueError(f"Unsupported aggregation: {agg}")
    return pd.to_numeric(score, errors="coerce")


def format_float(value: float | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return ""
    return f"{float(value):.{digits}f}"


def format_p(value: float | None) -> str:
    if value is None or pd.isna(value):
        return ""
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def safe_exp(value: float | None) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(np.exp(value))
    except Exception:
        return None


def markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    show = df if max_rows is None else df.head(max_rows)
    cols = list(show.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, row in show.iterrows():
        vals = [str(row[col]).replace("|", "/") for col in cols]
        lines.append("| " + " | ".join(vals) + " |")
    if max_rows is not None and len(df) > max_rows:
        lines.append(f"\nShowing first {max_rows} of {len(df)} rows. See CSV for full table.")
    return "\n".join(lines)


def normalize_key(value: object) -> str:
    if pd.isna(value):
        return ""
    try:
        numeric = float(value)
        if numeric.is_integer():
            return str(int(numeric))
    except Exception:
        pass
    return str(value).strip()


def labeled_category(series: pd.Series, labels: dict[str, str]) -> pd.Series:
    out = series.map(lambda x: labels.get(normalize_key(x), normalize_key(x)) if pd.notna(x) else np.nan)
    out = out.replace({"": np.nan, "nan": np.nan, "None": np.nan})
    return out


def make_target(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, pd.Series, dict[str, Any]]:
    score = scale_score(df, items, agg="sum")
    median = float(score.median(skipna=True))
    binary = pd.Series(np.nan, index=df.index, dtype="float")
    binary[score.notna()] = score[score.notna()].ge(median).astype(int)
    diag = {
        "target_items": items,
        "target_score_aggregation": "sum",
        "target_min_valid_items": min_valid_count(len(items)),
        "target_median_cutoff": median,
        "target_non_missing": int(score.notna().sum()),
        "target_positive": int(binary.eq(1).sum()),
        "target_negative": int(binary.eq(0).sum()),
    }
    return score, binary, diag


def online_activity_sum(df: pd.DataFrame, items: list[str]) -> pd.Series:
    existing = [col for col in items if col in df.columns]
    if len(existing) != len(items):
        return pd.Series(np.nan, index=df.index, dtype="float")
    values = to_numeric_frame(df, existing)
    return values.sum(axis=1, min_count=len(items))


def add_numeric_feature(
    X: pd.DataFrame,
    feature_defs: list[dict[str, Any]],
    code: str,
    name: str,
    values: pd.Series,
    source_type: str,
    items: list[str],
    wave: str,
) -> None:
    X[code] = pd.to_numeric(values, errors="coerce")
    feature_defs.append(
        {
            "wave": wave,
            "feature_code": code,
            "feature_name": name,
            "model_column": code,
            "source_type": source_type,
            "items": ";".join(items),
            "reference_category": "",
            "n_non_missing": int(X[code].notna().sum()),
            "n_unique_non_missing": int(X[code].dropna().nunique()),
        }
    )


def add_categorical_feature(
    X: pd.DataFrame,
    feature_defs: list[dict[str, Any]],
    code_prefix: str,
    name: str,
    series: pd.Series,
    labels: dict[str, str],
    wave: str,
    reference_category: str | None = None,
) -> None:
    labeled = labeled_category(series, labels)
    cats = sorted([cat for cat in labeled.dropna().unique()], key=lambda x: str(x))
    if len(cats) < 2:
        return
    reference = reference_category if reference_category in cats else cats[0]
    cats = [cat for cat in cats if cat != reference]
    for cat in cats:
        safe_cat = str(cat).replace(" ", "_").replace("/", "_").replace(",", "").replace("-", "_")
        col = f"{code_prefix}_{safe_cat}"
        X[col] = np.where(labeled.isna(), np.nan, labeled.eq(cat).astype(float))
        feature_defs.append(
            {
                "wave": wave,
                "feature_code": code_prefix,
                "feature_name": f"{name}: {cat} vs {reference}",
                "model_column": col,
                "source_type": "categorical_dummy",
                "items": series.name or code_prefix,
                "reference_category": reference,
                "n_non_missing": int(pd.Series(X[col]).notna().sum()),
                "n_unique_non_missing": int(pd.Series(X[col]).dropna().nunique()),
            }
        )


def get_parenting_reverse(config: dict[str, Any], wave_key: str) -> tuple[list[str], float, float]:
    cfg = config["reverse_coding"]["parenting_practices_parent_child_interaction_quality"]
    return list(cfg[f"{wave_key}_reverse_items"]), float(cfg["min_value"]), float(cfg["max_value"])


def build_features_for_wave(
    wave: str,
    df: pd.DataFrame,
    plan: pd.DataFrame,
    table1_config: dict[str, Any],
    subscale_config: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    wave_key = "w2" if wave == "W2" else "w3"
    column_key = "w2_columns" if wave == "W2" else "w3_columns"
    online_items = table1_config["online_activity_grouping"][f"{wave_key}_items"]
    X = pd.DataFrame(index=df.index)
    feature_defs: list[dict[str, Any]] = []

    add_numeric_feature(
        X,
        feature_defs,
        "online_activity_sum",
        "Online Activity Sum",
        online_activity_sum(df, online_items),
        "online_activity_sum_complete_4_items",
        list(online_items),
        wave,
    )

    gender_labels = table1_config["category_labels"]["gender"]["labels"]
    family_labels = table1_config["category_labels"]["family_structure"][f"{wave_key}_labels"]
    parenting_reverse, parenting_min, parenting_max = get_parenting_reverse(table1_config, wave_key)

    for _, row in plan.sort_values("order").iterrows():
        variable = str(row["variable"])
        if variable in {"Group size / analytic N", OUTCOME_VARIABLE_NAME}:
            continue
        if variable in DECOMPOSED_VARIABLE_NAMES:
            continue
        columns = [col for col in parse_columns(row[column_key]) if col in df.columns]
        if not columns:
            continue
        var_type = row["variable_type"]

        if variable == "Gender":
            add_categorical_feature(
                X,
                feature_defs,
                "gender",
                variable,
                df[columns[0]],
                gender_labels,
                wave,
                reference_category="Female",
            )
        elif variable == "Parental Marital Status / Family Structure":
            add_categorical_feature(
                X,
                feature_defs,
                "family_structure",
                variable,
                df[columns[0]],
                family_labels,
                wave,
                reference_category="Married, living together",
            )
        elif var_type == "binary":
            add_numeric_feature(X, feature_defs, columns[0], variable, pd.to_numeric(df[columns[0]], errors="coerce"), "binary", columns, wave)
        elif var_type in {"single_item_ordinal", "multi_item_scale"}:
            reverse_cols: list[str] = []
            min_value, max_value = 1.0, 4.0
            if variable == "Parenting Practices and Parent-Child Interaction Quality":
                reverse_cols = parenting_reverse
                min_value, max_value = parenting_min, parenting_max
            values = scale_score(df, columns, reverse_cols, min_value, max_value, agg="mean")
            code = columns[0] if len(columns) == 1 else str(row["w2_columns" if wave == "W2" else "w3_columns"]).split(";")[0].split("-")[0].split("_")[0]
            # Stable feature code by first column plus short suffix when needed.
            code = f"scale_{len(feature_defs):02d}_{code}" if len(columns) > 1 else code
            add_numeric_feature(X, feature_defs, code, variable, values, str(var_type), columns, wave)

    wave_subscales = subscale_config["waves"][wave]
    for parent_code, group in wave_subscales.items():
        for sub_code, sub in group["subscales"].items():
            cols = [col for col in sub["items"] if col in df.columns]
            values = scale_score(df, cols, agg="mean")
            name = f"{group['formal_group_name_en']} - {sub['subscale_name_en']}"
            add_numeric_feature(X, feature_defs, sub_code, name, values, "decomposed_subscale", cols, wave)

    feature_df = pd.DataFrame(feature_defs)
    diag = {
        "wave": wave,
        "n_rows": int(len(df)),
        "n_predictor_columns": int(X.shape[1]),
        "n_predictor_definitions": int(len(feature_df)),
        "all_missing_predictors": feature_df.loc[feature_df["n_non_missing"].eq(0), "model_column"].tolist(),
        "constant_predictors": feature_df.loc[feature_df["n_unique_non_missing"].le(1), "model_column"].tolist(),
    }
    keep_cols = [col for col in X.columns if X[col].notna().sum() > 0 and X[col].dropna().nunique() > 1]
    if len(keep_cols) != X.shape[1]:
        X = X[keep_cols].copy()
        feature_df = feature_df[feature_df["model_column"].isin(keep_cols)].reset_index(drop=True)
    return X, feature_df, diag


def fit_univariate(y: pd.Series, X: pd.DataFrame, feature_defs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, meta in feature_defs.iterrows():
        col = meta["model_column"]
        model_df = pd.DataFrame({"y": y, "x": X[col]}).dropna()
        row = meta.to_dict()
        row.update({"univariate_n": int(len(model_df)), "univariate_status": ""})
        if len(model_df) < 50 or model_df["y"].nunique() < 2 or model_df["x"].nunique() < 2:
            row.update({"univariate_status": "insufficient_variation"})
            rows.append(row)
            continue
        try:
            fit = sm.Logit(model_df["y"], sm.add_constant(model_df[["x"]], has_constant="add")).fit(disp=False, maxiter=200)
            b = float(fit.params["x"])
            se = float(fit.bse["x"])
            p = float(fit.pvalues["x"])
            ci_low, ci_high = fit.conf_int().loc["x"].tolist()
            row.update(
                {
                    "univariate_b": b,
                    "univariate_se": se,
                    "univariate_p": p,
                    "univariate_or": safe_exp(b),
                    "univariate_or_ci_low": safe_exp(ci_low),
                    "univariate_or_ci_high": safe_exp(ci_high),
                    "univariate_status": "ok",
                }
            )
        except Exception as exc:
            row.update({"univariate_status": f"failed: {type(exc).__name__}"})
        rows.append(row)
    return pd.DataFrame(rows)


def fit_multivariable(y: pd.Series, X: pd.DataFrame, feature_defs: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    model_df = pd.concat([y.rename("y"), X], axis=1).dropna()
    diag = {
        "multivariable_n": int(len(model_df)),
        "multivariable_n_positive": int(model_df["y"].eq(1).sum()) if len(model_df) else 0,
        "multivariable_n_negative": int(model_df["y"].eq(0).sum()) if len(model_df) else 0,
        "multivariable_status": "not_run",
    }
    rows = feature_defs.copy()
    if len(model_df) < 50 or model_df["y"].nunique() < 2:
        diag["multivariable_status"] = "insufficient_rows_or_target_variation"
        return rows, diag
    try:
        fit = sm.Logit(model_df["y"], sm.add_constant(model_df[X.columns], has_constant="add")).fit(disp=False, maxiter=300)
        diag["multivariable_status"] = "ok"
        diag["multivariable_pseudo_r2"] = float(fit.prsquared)
        diag["multivariable_aic"] = float(fit.aic)
        for idx, meta in rows.iterrows():
            col = meta["model_column"]
            if col not in fit.params.index:
                continue
            b = float(fit.params[col])
            se = float(fit.bse[col])
            p = float(fit.pvalues[col])
            ci_low, ci_high = fit.conf_int().loc[col].tolist()
            rows.loc[idx, "multivariable_b"] = b
            rows.loc[idx, "multivariable_se"] = se
            rows.loc[idx, "multivariable_p"] = p
            rows.loc[idx, "multivariable_or"] = safe_exp(b)
            rows.loc[idx, "multivariable_or_ci_low"] = safe_exp(ci_low)
            rows.loc[idx, "multivariable_or_ci_high"] = safe_exp(ci_high)
            rows.loc[idx, "multivariable_n"] = int(len(model_df))
            rows.loc[idx, "multivariable_status"] = "ok"
    except Exception as exc:
        diag["multivariable_status"] = f"failed: {type(exc).__name__}: {exc}"
    return rows, diag


def clean_table2(univ: pd.DataFrame, multi: pd.DataFrame, multi_diag: dict[str, Any]) -> pd.DataFrame:
    merged = univ.copy()
    for col in [
        "multivariable_b", "multivariable_se", "multivariable_p", "multivariable_or",
        "multivariable_or_ci_low", "multivariable_or_ci_high", "multivariable_n", "multivariable_status",
    ]:
        if col in multi.columns:
            merged[col] = multi[col].values
    if "multivariable_n" not in merged.columns:
        merged["multivariable_n"] = multi_diag.get("multivariable_n", "")
    out = pd.DataFrame({
        "Variable": merged["feature_name"],
        "Feature Code": merged["model_column"],
        "Source Type": merged["source_type"],
        "Items": merged["items"],
        "Univariate N": merged.get("univariate_n", ""),
        "Univariate B": merged.get("univariate_b", np.nan).map(format_float),
        "Univariate SE": merged.get("univariate_se", np.nan).map(format_float),
        "Univariate p-value": merged.get("univariate_p", np.nan).map(format_p),
        "Univariate OR": merged.get("univariate_or", np.nan).map(format_float),
        "Univariate OR 95% CI": [
            f"{format_float(lo)}-{format_float(hi)}" if pd.notna(lo) and pd.notna(hi) else ""
            for lo, hi in zip(merged.get("univariate_or_ci_low", pd.Series(np.nan, index=merged.index)), merged.get("univariate_or_ci_high", pd.Series(np.nan, index=merged.index)))
        ],
        "Multivariable N": merged.get("multivariable_n", multi_diag.get("multivariable_n", "")),
        "Multivariable B": merged.get("multivariable_b", np.nan).map(format_float),
        "Multivariable SE": merged.get("multivariable_se", np.nan).map(format_float),
        "Multivariable p-value": merged.get("multivariable_p", np.nan).map(format_p),
        "Multivariable OR": merged.get("multivariable_or", np.nan).map(format_float),
        "Multivariable OR 95% CI": [
            f"{format_float(lo)}-{format_float(hi)}" if pd.notna(lo) and pd.notna(hi) else ""
            for lo, hi in zip(merged.get("multivariable_or_ci_low", pd.Series(np.nan, index=merged.index)), merged.get("multivariable_or_ci_high", pd.Series(np.nan, index=merged.index)))
        ],
        "Univariate Status": merged.get("univariate_status", ""),
        "Multivariable Status": merged.get("multivariable_status", multi_diag.get("multivariable_status", "")),
    })
    return out


def specificity_score(y_true, y_pred) -> float:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return float(tn / (tn + fp)) if (tn + fp) else 0.0


def sensitivity_score(y_true, y_pred) -> float:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return float(tp / (tp + fn)) if (tp + fn) else 0.0


def model_metrics(y_true: pd.Series, prob: np.ndarray) -> dict[str, float]:
    pred = (prob >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, pred)),
        "sensitivity": sensitivity_score(y_true, pred),
        "specificity": specificity_score(y_true, pred),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
        "auc": float(roc_auc_score(y_true, prob)),
    }


def make_pipeline(model) -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", model),
        ]
    )


def fit_model_comparison(y: pd.Series, X: pd.DataFrame, feature_defs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid = y.notna()
    yv = y[valid].astype(int)
    Xv = X.loc[valid].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        Xv, yv, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=yv
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    models = {
        "Multivariable Logistic": LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000),
        "LASSO Logistic": LogisticRegressionCV(Cs=LOGIT_CS, penalty="l1", solver="saga", cv=cv, scoring="roc_auc", max_iter=20000, n_jobs=None, random_state=RANDOM_STATE),
        "Ridge Logistic": LogisticRegressionCV(Cs=LOGIT_CS, penalty="l2", solver="lbfgs", cv=cv, scoring="roc_auc", max_iter=10000, n_jobs=None),
    }

    perf_rows = []
    coef_frames = []
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "f1": "f1",
        "auc": "roc_auc",
        "sensitivity": make_scorer(sensitivity_score),
        "specificity": make_scorer(specificity_score),
    }

    for model_name, model in models.items():
        pipe = make_pipeline(model)
        pipe.fit(X_train, y_train)
        prob = pipe.predict_proba(X_test)[:, 1]
        test = model_metrics(y_test, prob)
        fitted = pipe.named_steps["model"]
        selected_c = getattr(fitted, "C_", [np.nan])[0] if hasattr(fitted, "C_") else np.nan

        # Use selected C for cross-validated performance to avoid nested CV complexity.
        if model_name == "Multivariable Logistic":
            cv_model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000)
        elif model_name == "LASSO Logistic":
            cv_model = LogisticRegression(C=float(selected_c), penalty="l1", solver="saga", max_iter=20000, random_state=RANDOM_STATE)
        else:
            cv_model = LogisticRegression(C=float(selected_c), penalty="l2", solver="lbfgs", max_iter=10000)
        cv_pipe = make_pipeline(cv_model)
        cv_scores = cross_validate(cv_pipe, Xv, yv, cv=cv, scoring=scoring, n_jobs=None)

        perf = {
            "Model": model_name,
            "N": int(len(Xv)),
            "N features": int(Xv.shape[1]),
            "Selected C": format_float(selected_c, 6),
            "Test AUC": format_float(test["auc"]),
            "Test Accuracy": format_float(test["accuracy"]),
            "Test Sensitivity": format_float(test["sensitivity"]),
            "Test Specificity": format_float(test["specificity"]),
            "Test F1": format_float(test["f1"]),
            "Test Balanced Accuracy": format_float(test["balanced_accuracy"]),
        }
        for metric in scoring:
            perf[f"CV {metric} mean"] = format_float(float(np.mean(cv_scores[f"test_{metric}"])))
            perf[f"CV {metric} SD"] = format_float(float(np.std(cv_scores[f"test_{metric}"], ddof=1)))
        perf_rows.append(perf)

        coefs = fitted.coef_[0]
        coef_frame = feature_defs[["model_column", "feature_name", "source_type", "items"]].copy()
        coef_frame["Model"] = model_name
        coef_frame["Standardized Coefficient"] = coefs
        if model_name == "LASSO Logistic":
            coef_frame["Selected by LASSO"] = np.abs(coefs) > 1e-8
        coef_frames.append(coef_frame)

    perf_df = pd.DataFrame(perf_rows)
    coef_long = pd.concat(coef_frames, ignore_index=True)
    coef_wide = feature_defs[["model_column", "feature_name", "source_type", "items"]].copy()
    coef_wide = coef_wide.rename(columns={"feature_name": "Variable", "model_column": "Feature Code", "source_type": "Source Type", "items": "Items"})
    for model_name in models:
        sub = coef_long[coef_long["Model"].eq(model_name)].set_index("model_column")
        coef_wide[f"{model_name} Std. B"] = coef_wide["Feature Code"].map(sub["Standardized Coefficient"]).map(lambda x: format_float(x, 4))
    lasso_sub = coef_long[coef_long["Model"].eq("LASSO Logistic")].set_index("model_column")
    selected_map = coef_wide["Feature Code"].map(lasso_sub["Selected by LASSO"])
    coef_wide["Selected by LASSO"] = selected_map.map(lambda value: bool(value) if pd.notna(value) else False)
    return coef_wide, perf_df


def run_wave(wave: str, df: pd.DataFrame, plan: pd.DataFrame, table1_config: dict[str, Any], subscale_config: dict[str, Any]) -> dict[str, Any]:
    slug = "w2_2024" if wave == "W2" else "w3_2025"
    target_items = TARGET_W2_ITEMS if wave == "W2" else TARGET_W3_ITEMS
    target_score, y, target_diag = make_target(df, target_items)
    X, feature_defs, feature_diag = build_features_for_wave(wave, df, plan, table1_config, subscale_config)

    univ = fit_univariate(y, X, feature_defs)
    multi, multi_diag = fit_multivariable(y, X, feature_defs)
    table2 = clean_table2(univ, multi, multi_diag)
    coef_table, perf_table = fit_model_comparison(y, X, feature_defs)

    table2.to_csv(OUT_DIR / f"table2_{slug}_logistic.csv", index=False, encoding="utf-8-sig")
    coef_table.to_csv(OUT_DIR / f"table3a_{slug}_coefficient_comparison.csv", index=False, encoding="utf-8-sig")
    perf_table.to_csv(OUT_DIR / f"table3b_{slug}_model_performance.csv", index=False, encoding="utf-8-sig")
    feature_defs.to_csv(OUT_DIR / f"feature_dictionary_{slug}.csv", index=False, encoding="utf-8-sig")

    (OUT_DIR / f"table2_{slug}_logistic.md").write_text(
        "\n".join([
            f"# Table 2: {wave} Logistic Regression for Psychological Distress",
            "",
            f"- Outcome score: sum of {len(target_items)} psychological distress items.",
            f"- Binary outcome: score >= wave-specific median cutoff ({target_diag['target_median_cutoff']}).",
            "- Univariate models use one predictor at a time.",
            "- Multivariable model uses complete cases across all predictors in this table.",
            "- Multi-item predictors require at least 50% valid items.",
            "",
            markdown_table(table2, max_rows=60),
            "",
        ]),
        encoding="utf-8",
    )
    (OUT_DIR / f"table3a_{slug}_coefficient_comparison.md").write_text(
        "\n".join([
            f"# Table 3A: {wave} Standardized Coefficient Comparison",
            "",
            "Coefficients are from standardized predictors with median imputation, for model-comparison purposes.",
            "",
            markdown_table(coef_table, max_rows=80),
            "",
        ]),
        encoding="utf-8",
    )
    (OUT_DIR / f"table3b_{slug}_model_performance.md").write_text(
        "\n".join([
            f"# Table 3B: {wave} Model Performance Comparison",
            "",
            "Performance uses an 80/20 stratified test split and 5-fold cross-validation.",
            "",
            markdown_table(perf_table),
            "",
        ]),
        encoding="utf-8",
    )

    return {"wave": wave, **target_diag, **feature_diag, **multi_diag}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plan = pd.read_csv(TABLE1_PLAN, encoding="utf-8-sig")
    table1_config = json.loads(TABLE1_CONFIG.read_text(encoding="utf-8"))
    subscale_config = json.loads(SUBSCALE_CONFIG.read_text(encoding="utf-8"))
    w2 = pd.read_csv(W2_DATA, encoding="utf-8-sig", low_memory=False)
    w3 = pd.read_csv(W3_DATA, encoding="utf-8-sig", low_memory=False)

    diagnostics = [run_wave("W2", w2, plan, table1_config, subscale_config), run_wave("W3", w3, plan, table1_config, subscale_config)]
    diag_df = pd.DataFrame(diagnostics)
    diag_df.to_csv(OUT_DIR / "table2_table3_diagnostics.csv", index=False, encoding="utf-8-sig")

    notes = [
        "# Table 2 and Table 3 Generation Notes",
        "",
        "## Inputs",
        "",
        f"- W2 data: `{W2_DATA.relative_to(ROOT)}`",
        f"- W3 data: `{W3_DATA.relative_to(ROOT)}`",
        f"- Table 1 variable plan: `{TABLE1_PLAN.relative_to(ROOT)}`",
        f"- Table 1 scoring config: `{TABLE1_CONFIG.relative_to(ROOT)}`",
        f"- Subscale config: `{SUBSCALE_CONFIG.relative_to(ROOT)}`",
        "",
        "## Outcome",
        "",
        "- W2 outcome items: `v55_1` to `v55_14`.",
        "- W3 outcome items: `54-1` to `54-14`.",
        "- Outcome score aggregation: sum.",
        "- Binary outcome: score >= wave-specific median cutoff.",
        "",
        "## Predictors",
        "",
        "- Predictors start from the Table 1 variable plan, excluding the psychological distress outcome.",
        "- Decomposed groups replace their parent scale scores: FOMO, social media self-presentation, social media use, online social comparison, and SEL.",
        "- Online Activity Sum is added as a predictor using complete four-item sums.",
        "- Multi-item scale predictors require at least 50% valid items.",
        "- Parenting items use the same reverse coding as Table 1.",
        "- W2 `v52` is used as Self-Rated Health; W2 `v52_1` to `v52_3` are retained as Self-Worth.",
        "- Gender reference category is Female. Family Structure reference category is Married, living together.",
        "",
        "## Table 2",
        "",
        "- Univariate logistic regression: one predictor at a time.",
        "- Multivariable logistic regression: complete-case model across all predictors.",
        "- Reported columns: B, SE, p-value, OR, and OR 95% CI.",
        "",
        "## Table 3",
        "",
        "- Table 3A compares standardized coefficients from multivariable logistic, LASSO logistic, and Ridge logistic.",
        "- Table 3B compares model performance using an 80/20 stratified test split and 5-fold cross-validation.",
        "- LASSO/Ridge coefficients do not have traditional SE/p-values; they are reported as standardized coefficients for model comparison.",
    ]
    (OUT_DIR / "README_table2_table3.md").write_text("\n".join(notes), encoding="utf-8")
    print("Wrote Table 2/3 outputs to", OUT_DIR)
    print(diag_df.to_string(index=False))


if __name__ == "__main__":
    main()
