from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


SCRIPT_PATH = Path(__file__).resolve()
TABLE1_DIR = SCRIPT_PATH.parents[1]
TABLES_DIR = TABLE1_DIR.parent
ROOT = TABLE1_DIR.parents[3]
TABLE_SCRIPTS_DIR = TABLES_DIR / "scripts"
if str(TABLE_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(TABLE_SCRIPTS_DIR))

import build_table2_table3_drop_decomposition as t23  # noqa: E402


W2_DATA = ROOT / "Data" / "testing_clean" / "W2" / "TIGPS_W2_studentdata_ver6.csv"
W3_DATA = ROOT / "Data" / "testing_clean" / "W3" / "TIGPS_W3_student_studentdata_ver5.csv"
CONFIG_PATH = TABLE1_DIR / "config" / "table1_scoring_config.json"
OUTPUTS_DIR = TABLE1_DIR / "outputs"
ONLINE_OUT = OUTPUTS_DIR / "01_online_activity_observed"
ONLINE_ADJUSTED_OUT = OUTPUTS_DIR / "02_online_activity_class_adjusted_network"
DISTRESS_OUT = OUTPUTS_DIR / "03_psychological_distress_observed"
DISTRESS_ADJUSTED_OUT = OUTPUTS_DIR / "04_psychological_distress_class_adjusted_network"
DIAG_OUT = TABLE1_DIR / "diagnostics"
INTERPERSONAL_FEATURE_DIR = ROOT / "Code" / "paper_data_newdata" / "Interpersonal_features" / "outputs" / "features"
INTERPERSONAL_FEATURE_FILES = {
    "W2": INTERPERSONAL_FEATURE_DIR / "interpersonal_features_w2.csv",
    "W3": INTERPERSONAL_FEATURE_DIR / "interpersonal_features_w3.csv",
}

GROUP_HIGH_ONLINE = "High Online Activity"
GROUP_LOW_ONLINE = "Low Online Activity"
GROUP_HIGH_DISTRESS = "High Psychological Distress"
GROUP_LOW_DISTRESS = "Low Psychological Distress"

# Presentation order for Table 1. This is intentionally different from the
# model-input order so that related concepts appear together in the manuscript.
FEATURE_PRESENTATION_ORDER = {
    "Gender (Demographic Variable)": 10,
    "Gender: Male (vs Female)": 10,
    "Parental Marital Status / Family Structure": 11,
    "Perceived Social Status (Subjective Social Status)": 12,
    "Family Cohesion and Support (Family Functioning)": 20,
    "Parenting Practices and Parent-Child Interaction Quality (Support/Conflict/Monitoring)": 21,
    "Parenting Practices and Parent–Child Interaction Quality (Support/Conflict/Monitoring)": 21,
    "Parental Involvement in Schooling and Academic Monitoring": 22,
    "Perceived Effectiveness of School-based Digital/Technology Learning": 23,
    "Self-Worth and Positive Self-Concept": 30,
    "Self-Awareness": 31,
    "Self-Management": 32,
    "Motivation & Goal Setting": 33,
    "Social Awareness & Relationship Skills": 34,
    "Help-Seeking": 35,
    "Responsible Decision-Making": 36,
    "Problematic Internet Use and Internet Dependence": 40,
    "Online Coping and Support Seeking under Distress": 41,
    "Online Coping and Emotion Regulation under Distress": 41,
    "Online Ideal Self-Presentation": 42,
    "Real-life Self-Satisfaction": 43,
    "Online-Offline Discrepancy & Immersion": 44,
    "Selective Positive Sharing": 45,
    "Digital Image Enhancement": 46,
    "Authentic and Less-Ideal Self-Presentation": 46,
    "Social Feedback Dependency": 47,
    "Covert Social Media Monitoring and Passive Participation": 47,
    "Online Upward Social Comparison": 48,
    "Online Perspective Seeking": 49,
    "Fear of Missing Out & Social Anxiety": 50,
    "Instant Response Pressure": 51,
    "Distress from Missing Online Events": 51,
    "Cyberbullying Victimization (including Misinformation-related)": 60,
    "Cyberbullying Perpetration (including Misinformation-related)": 61,
    "Physical/Offline Bullying Victimization": 62,
    "Offline Bullying Victimization": 62,
    "Physical/Offline Bullying Perpetration": 63,
    "Offline Bullying Perpetration": 63,
    "Delinquent and Health-Risk Behaviors": 70,
    "Delinquent and Risk Behaviors": 70,
    "Online Total Nominations, Observed Count": 78,
    "Offline Total Nominations, Observed Count": 79,
    "Outgoing Friendship Nominations, Observed Count": 80,
    "Incoming Friendship Nominations, Observed Count": 81,
    "Outgoing Negative Nominations, Observed Count": 82,
    "Incoming Negative Nominations, Observed Count": 83,
    "Reciprocal Friendship Ties, Observed Count": 84,
    "Reciprocal Negative Ties, Observed Count": 85,
    "Sent Positive Tie Ratio, Observed": 86,
    "Received Positive Tie Ratio, Observed": 87,
    "Sent Network Valence, Observed": 88,
    "Received Network Valence, Observed": 89,
    "Online Total Nominations, Respondent-Class-Normalized": 78,
    "Offline Total Nominations, Respondent-Class-Normalized": 79,
    "Outgoing Friendship Nominations, Respondent-Class-Normalized": 80,
    "Incoming Friendship Nominations, Respondent-Class-Normalized": 81,
    "Outgoing Negative Nominations, Respondent-Class-Normalized": 82,
    "Incoming Negative Nominations, Respondent-Class-Normalized": 83,
    "Reciprocal Friendship Ties, Respondent-Class-Normalized": 84,
    "Reciprocal Negative Ties, Respondent-Class-Normalized": 85,
    "Sent Positive Tie Ratio": 86,
    "Received Positive Tie Ratio": 87,
    "Sent Network Valence, Respondent-Class-Normalized": 88,
    "Received Network Valence, Respondent-Class-Normalized": 89,
}

INTERPERSONAL_TABLE1_FEATURES = [
    {
        "column": "ip_online_total",
        "name": "Online Total Nominations, Observed Count",
        "items": "Observed online friendship and online negative nominations, sent and received",
    },
    {
        "column": "ip_offline_total",
        "name": "Offline Total Nominations, Observed Count",
        "items": "Observed offline friendship and offline negative nominations, sent and received",
    },
    {
        "column": "ip_out_friend_total",
        "name": "Outgoing Friendship Nominations, Observed Count",
        "items": "Observed online + offline friend nominations sent",
    },
    {
        "column": "ip_in_friend_total",
        "name": "Incoming Friendship Nominations, Observed Count",
        "items": "Observed online + offline friend nominations received",
    },
    {
        "column": "ip_out_enemy_total",
        "name": "Outgoing Negative Nominations, Observed Count",
        "items": "Observed online + offline negative nominations sent",
    },
    {
        "column": "ip_in_enemy_total",
        "name": "Incoming Negative Nominations, Observed Count",
        "items": "Observed online + offline negative nominations received",
    },
    {
        "column": "ip_reciprocal_friend_count",
        "name": "Reciprocal Friendship Ties, Observed Count",
        "items": "Observed mutual friendship nominations",
    },
    {
        "column": "ip_reciprocal_enemy_count",
        "name": "Reciprocal Negative Ties, Observed Count",
        "items": "Observed mutual negative nominations",
    },
    {
        "column": "ip_sent_like_ratio",
        "name": "Sent Positive Tie Ratio",
        "items": "Observed friend nominations sent / all observed nominations sent",
    },
    {
        "column": "ip_received_like_ratio",
        "name": "Received Positive Tie Ratio",
        "items": "Observed friend nominations received / all observed nominations received",
    },
    {
        "column": "ip_sent_net",
        "name": "Sent Network Valence, Observed",
        "items": "Observed friend nominations sent minus observed negative nominations sent",
    },
    {
        "column": "ip_received_net",
        "name": "Received Network Valence, Observed",
        "items": "Observed friend nominations received minus observed negative nominations received",
    },
]

INTERPERSONAL_TABLE1_NORMALIZED_FEATURES = [
    {
        "column": "ip_online_total_rate_class",
        "name": "Online Total Nominations, Respondent-Class-Normalized",
        "items": "Observed online friendship and online negative nominations, sent and received / same-class respondents minus 1",
    },
    {
        "column": "ip_offline_total_rate_class",
        "name": "Offline Total Nominations, Respondent-Class-Normalized",
        "items": "Observed offline friendship and offline negative nominations, sent and received / same-class respondents minus 1",
    },
    {
        "column": "ip_out_friend_total_rate_class",
        "name": "Outgoing Friendship Nominations, Respondent-Class-Normalized",
        "items": "Observed online + offline friend nominations sent / same-class respondents minus 1",
    },
    {
        "column": "ip_in_friend_total_rate_class",
        "name": "Incoming Friendship Nominations, Respondent-Class-Normalized",
        "items": "Observed online + offline friend nominations received / same-class respondents minus 1",
    },
    {
        "column": "ip_out_enemy_total_rate_class",
        "name": "Outgoing Negative Nominations, Respondent-Class-Normalized",
        "items": "Observed online + offline negative nominations sent / same-class respondents minus 1",
    },
    {
        "column": "ip_in_enemy_total_rate_class",
        "name": "Incoming Negative Nominations, Respondent-Class-Normalized",
        "items": "Observed online + offline negative nominations received / same-class respondents minus 1",
    },
    {
        "column": "ip_reciprocal_friend_count_rate_class",
        "name": "Reciprocal Friendship Ties, Respondent-Class-Normalized",
        "items": "Observed mutual friendship nominations / same-class respondents minus 1",
    },
    {
        "column": "ip_reciprocal_enemy_count_rate_class",
        "name": "Reciprocal Negative Ties, Respondent-Class-Normalized",
        "items": "Observed mutual negative nominations / same-class respondents minus 1",
    },
    {
        "column": "ip_sent_like_ratio",
        "name": "Sent Positive Tie Ratio",
        "items": "Observed friend nominations sent / all observed nominations sent",
    },
    {
        "column": "ip_received_like_ratio",
        "name": "Received Positive Tie Ratio",
        "items": "Observed friend nominations received / all observed nominations received",
    },
    {
        "column": "ip_sent_net_rate_class",
        "name": "Sent Network Valence, Respondent-Class-Normalized",
        "items": "Observed friend nominations sent minus observed negative nominations sent / same-class respondents minus 1",
    },
    {
        "column": "ip_received_net_rate_class",
        "name": "Received Network Valence, Respondent-Class-Normalized",
        "items": "Observed friend nominations received minus observed negative nominations received / same-class respondents minus 1",
    },
]


def format_n_pct(n: int, denom: int) -> str:
    if denom <= 0:
        return "NA"
    return f"{n} ({n / denom * 100:.1f}%)"


def format_mean_sd(values: pd.Series) -> str:
    values = pd.to_numeric(values, errors="coerce").dropna()
    if values.empty:
        return "NA"
    return f"{values.mean():.2f} ({values.std(ddof=1):.2f})"


def format_p_value(value: float | None) -> str:
    if value is None or pd.isna(value):
        return ""
    if value < 0.001:
        return "<0.001"
    return f"{float(value):.3f}"


def format_effect_size(value: float | None) -> str:
    if value is None or pd.isna(value):
        return ""
    return f"{float(value):.3f}"


def markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.fillna("").iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "/") for col in cols) + " |")
    return "\n".join(lines)


def write_xlsx(df: pd.DataFrame, path: Path, sheet_name: str = "Table1") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
        worksheet = writer.book[sheet_name[:31]]
        worksheet.freeze_panes = "A2"
        for column_cells in worksheet.columns:
            max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_len + 2, 12), 70)


def cramers_v_from_table(table: pd.DataFrame) -> float | None:
    if table.empty or table.shape[0] < 2 or table.shape[1] < 2:
        return None
    try:
        chi2, _, _, _ = stats.chi2_contingency(table)
        n = table.to_numpy().sum()
        denom = n * min(table.shape[0] - 1, table.shape[1] - 1)
        if denom <= 0:
            return None
        return float((chi2 / denom) ** 0.5)
    except Exception:
        return None


def categorical_p_value(series: pd.Series, group: pd.Series) -> float | None:
    valid = series.notna() & group.notna()
    if valid.sum() == 0:
        return None
    table = pd.crosstab(group[valid], series[valid])
    if table.shape[0] != 2 or table.shape[1] < 2:
        return None
    try:
        _, p_value, _, _ = stats.chi2_contingency(table)
        return float(p_value)
    except Exception:
        return None


def categorical_effect_size(series: pd.Series, group: pd.Series) -> float | None:
    valid = series.notna() & group.notna()
    if valid.sum() == 0:
        return None
    return cramers_v_from_table(pd.crosstab(group[valid], series[valid]))


def binary_p_value(series: pd.Series, group: pd.Series) -> float | None:
    valid = series.notna() & group.notna()
    if valid.sum() == 0:
        return None
    binary = series[valid].eq(1)
    table = pd.crosstab(group[valid], binary)
    for col in [False, True]:
        if col not in table.columns:
            table[col] = 0
    table = table.reindex(columns=[False, True], fill_value=0)
    if table.shape[0] != 2:
        return None
    try:
        _, p_value, _, expected = stats.chi2_contingency(table)
        if table.shape == (2, 2) and (expected < 5).any():
            _, p_value = stats.fisher_exact(table)
        return float(p_value)
    except Exception:
        return None


def binary_effect_size(series: pd.Series, group: pd.Series) -> float | None:
    valid = series.notna() & group.notna()
    if valid.sum() == 0:
        return None
    binary = series[valid].eq(1)
    table = pd.crosstab(group[valid], binary)
    for col in [False, True]:
        if col not in table.columns:
            table[col] = 0
    table = table.reindex(columns=[False, True], fill_value=0)
    return cramers_v_from_table(table)


def continuous_p_value(score: pd.Series, group: pd.Series, high_label: str, low_label: str) -> float | None:
    high = pd.to_numeric(score[group.eq(high_label)], errors="coerce").dropna()
    low = pd.to_numeric(score[group.eq(low_label)], errors="coerce").dropna()
    if len(high) < 2 or len(low) < 2:
        return None
    try:
        _, p_value = stats.ttest_ind(high, low, equal_var=False, nan_policy="omit")
        return float(p_value)
    except Exception:
        return None


def continuous_effect_size(score: pd.Series, group: pd.Series, high_label: str, low_label: str) -> float | None:
    high = pd.to_numeric(score[group.eq(high_label)], errors="coerce").dropna()
    low = pd.to_numeric(score[group.eq(low_label)], errors="coerce").dropna()
    if len(high) < 2 or len(low) < 2:
        return None
    pooled_var = ((len(high) - 1) * high.var(ddof=1) + (len(low) - 1) * low.var(ddof=1)) / (len(high) + len(low) - 2)
    if pooled_var <= 0 or pd.isna(pooled_var):
        return None
    return float((high.mean() - low.mean()) / (pooled_var ** 0.5))


def label_for_category(variable: str, raw_value: Any, config: dict[str, Any], wave: str) -> str:
    try:
        key = str(int(raw_value)) if pd.notna(raw_value) and float(raw_value).is_integer() else str(raw_value)
    except Exception:
        key = str(raw_value)
    if variable in {"Gender (Demographic Variable)", "Gender: Male (vs Female)"}:
        if key == "0":
            return "Female"
        if key == "1":
            return "Male"
        return config["category_labels"]["gender"]["labels"].get(key, key)
    if variable == "Parental Marital Status / Family Structure":
        family_key = "w2_labels" if wave == "W2" else "w3_labels"
        return config["category_labels"]["family_structure"][family_key].get(key, key)
    return key


def is_gender_or_family(feature: pd.Series) -> bool:
    source_group = str(feature.get("source_group_id", ""))
    return source_group in {"v1", "1", "v2", "3"}


def is_binary_feature(values: pd.Series) -> bool:
    valid = pd.to_numeric(values, errors="coerce").dropna().unique()
    valid_set = set(float(v) for v in valid)
    return bool(valid_set) and valid_set.issubset({0.0, 1.0})


def classify_online_activity(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, dict[str, Any]]:
    values = df[items].apply(pd.to_numeric, errors="coerce")
    valid_count = values.notna().sum(axis=1)
    complete = valid_count.eq(len(items))
    activity_sum = values.sum(axis=1, min_count=len(items))
    median = float(activity_sum.median(skipna=True))
    group = pd.Series(pd.NA, index=df.index, dtype="object")
    group.loc[complete & activity_sum.gt(median)] = GROUP_HIGH_ONLINE
    group.loc[complete & activity_sum.le(median)] = GROUP_LOW_ONLINE
    diag = {
        "grouping": "online_activity",
        "items": items,
        "median": median,
        "rows": int(len(df)),
        "classified": int(group.notna().sum()),
        "high": int(group.eq(GROUP_HIGH_ONLINE).sum()),
        "low": int(group.eq(GROUP_LOW_ONLINE).sum()),
        "unclassified": int(group.isna().sum()),
    }
    return group, diag


def classify_psychological_distress(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, dict[str, Any]]:
    score, binary, diag = t23.make_target(df, items)
    group = pd.Series(pd.NA, index=df.index, dtype="object")
    group.loc[binary.eq(1)] = GROUP_HIGH_DISTRESS
    group.loc[binary.eq(0)] = GROUP_LOW_DISTRESS
    return group, {"grouping": "psychological_distress", **diag}


def build_feature_context(
    wave: str,
    df: pd.DataFrame,
    merged: pd.DataFrame,
    interpersonal_specs: list[dict[str, str]] | None = None,
    interpersonal_label: str = "observed",
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    target_group = "v55" if wave == "W2" else "54"
    X, feature_defs, feature_diag = t23.build_drop_decomposition_features(df, merged, wave, target_group)
    return add_interpersonal_features(
        wave,
        df,
        X,
        feature_defs,
        feature_diag,
        interpersonal_specs or INTERPERSONAL_TABLE1_FEATURES,
        interpersonal_label,
    )


def add_interpersonal_features(
    wave: str,
    df: pd.DataFrame,
    X: pd.DataFrame,
    feature_defs: pd.DataFrame,
    feature_diag: dict[str, Any],
    interpersonal_specs: list[dict[str, str]],
    interpersonal_label: str,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    path = INTERPERSONAL_FEATURE_FILES[wave]
    if not path.exists():
        feature_diag = {**feature_diag, "table1_interpersonal_status": f"missing: {path}", "table1_interpersonal_version": interpersonal_label}
        return X, feature_defs, feature_diag

    interpersonal = t23.core.normalize_student_id(pd.read_csv(path, encoding="utf-8-sig", low_memory=False))
    interpersonal = interpersonal.drop_duplicates(subset=["student_id"], keep="first")
    merged = df[["student_id"]].merge(interpersonal, on="student_id", how="left")

    X_out = X.copy()
    def_rows = []
    included = []
    missing = []
    derived_count_specs = {
        "ip_online_total": ["ip_out_online_friend", "ip_in_online_friend", "ip_out_online_enemy", "ip_in_online_enemy"],
        "ip_offline_total": ["ip_out_offline_friend", "ip_in_offline_friend", "ip_out_offline_enemy", "ip_in_offline_enemy"],
    }
    for spec in interpersonal_specs:
        source_col = spec["column"]
        if source_col in derived_count_specs and source_col not in merged.columns:
            parts = [pd.to_numeric(merged[c], errors="coerce").fillna(0.0) for c in derived_count_specs[source_col] if c in merged.columns]
            if parts:
                merged[source_col] = sum(parts)
        if source_col == "ip_online_total_rate_class" and source_col not in merged.columns:
            parts = [pd.to_numeric(merged[c], errors="coerce").fillna(0.0) for c in derived_count_specs["ip_online_total"] if c in merged.columns]
            if parts:
                merged[source_col] = sum(parts) / pd.to_numeric(merged["ip_class_size_minus1"], errors="coerce")
        if source_col == "ip_offline_total_rate_class" and source_col not in merged.columns:
            parts = [pd.to_numeric(merged[c], errors="coerce").fillna(0.0) for c in derived_count_specs["ip_offline_total"] if c in merged.columns]
            if parts:
                merged[source_col] = sum(parts) / pd.to_numeric(merged["ip_class_size_minus1"], errors="coerce")
        if source_col == "ip_sent_net_rate_class" and source_col not in merged.columns:
            merged[source_col] = pd.to_numeric(merged["ip_sent_net"], errors="coerce") / pd.to_numeric(
                merged["ip_class_size_minus1"], errors="coerce"
            )
        if source_col == "ip_received_net_rate_class" and source_col not in merged.columns:
            merged[source_col] = pd.to_numeric(merged["ip_received_net"], errors="coerce") / pd.to_numeric(
                merged["ip_class_size_minus1"], errors="coerce"
            )
        if source_col not in merged.columns:
            missing.append(source_col)
            continue
        model_col = f"feature_{source_col}"
        X_out[model_col] = pd.to_numeric(merged[source_col], errors="coerce")
        def_rows.append(
            {
                "model_column": model_col,
                "feature_code": source_col,
                "feature_name": spec["name"],
                "source_type": "interpersonal_feature",
                "source_group_id": source_col,
                "items": spec["items"],
                "score_aggregation": "mean",
            }
        )
        included.append(source_col)

    if def_rows:
        feature_defs = pd.concat([feature_defs, pd.DataFrame(def_rows)], ignore_index=True)

    feature_diag = {
        **feature_diag,
        "table1_interpersonal_status": "ok",
        "table1_interpersonal_version": interpersonal_label,
        "table1_interpersonal_features_added": ";".join(included),
        "table1_interpersonal_features_missing": ";".join(missing),
    }
    return X_out, feature_defs, feature_diag


def presentation_order(feature_defs: pd.DataFrame) -> pd.DataFrame:
    ordered = feature_defs.copy()
    ordered["_presentation_order"] = ordered["feature_name"].map(FEATURE_PRESENTATION_ORDER).fillna(999)
    ordered["_original_order"] = range(len(ordered))
    ordered = ordered.sort_values(["_presentation_order", "_original_order"], kind="stable").drop(
        columns=["_presentation_order", "_original_order"]
    )
    return ordered.reset_index(drop=True)


def build_table(
    wave: str,
    X: pd.DataFrame,
    feature_defs: pd.DataFrame,
    group: pd.Series,
    group_cols: tuple[str, str],
    config: dict[str, Any],
) -> pd.DataFrame:
    high_label, low_label = group_cols
    working_idx = group.notna()
    group_valid = group.loc[working_idx]
    rows: list[dict[str, str]] = [
        {
            "Question ID": "",
            "Variable": "N",
            high_label: str(int(group_valid.eq(high_label).sum())),
            low_label: str(int(group_valid.eq(low_label).sum())),
            "Total": str(int(len(group_valid))),
            "p-value": "",
            "Between-group difference": "",
            "Between-group difference type": "",
        }
    ]

    for _, feature in presentation_order(feature_defs).iterrows():
        variable = str(feature["feature_name"])
        items = str(feature.get("items", "")).replace(";", "; ")
        col = feature["model_column"]
        values = X[col].loc[working_idx]
        g = group_valid

        if is_gender_or_family(feature):
            categories = sorted(pd.to_numeric(values, errors="coerce").dropna().unique())
            p_text = format_p_value(categorical_p_value(values, g))
            effect_text = format_effect_size(categorical_effect_size(values, g))
            for cat in categories:
                label = label_for_category(variable, cat, config, wave)
                row = {"Question ID": items, "Variable": f"{variable}: {label}"}
                for label_name, col_name in [(high_label, high_label), (low_label, low_label), ("Total", "Total")]:
                    subset = values if label_name == "Total" else values[g.eq(label_name)]
                    denom = int(subset.notna().sum())
                    n = int(pd.to_numeric(subset, errors="coerce").eq(cat).sum())
                    row[col_name] = format_n_pct(n, denom)
                row["p-value"] = p_text
                row["Between-group difference"] = effect_text
                row["Between-group difference type"] = "Cramer's V" if effect_text else ""
                p_text = ""
                effect_text = ""
                rows.append(row)
            continue

        if str(feature.get("source_type", "")) != "interpersonal_feature" and is_binary_feature(values):
            row = {"Question ID": items, "Variable": f"{variable}: Yes"}
            row["p-value"] = format_p_value(binary_p_value(values, g))
            row["Between-group difference"] = format_effect_size(binary_effect_size(values, g))
            row["Between-group difference type"] = "Cramer's V" if row["Between-group difference"] else ""
            for label_name, col_name in [(high_label, high_label), (low_label, low_label), ("Total", "Total")]:
                subset = values if label_name == "Total" else values[g.eq(label_name)]
                denom = int(subset.notna().sum())
                n = int(pd.to_numeric(subset, errors="coerce").eq(1).sum())
                row[col_name] = format_n_pct(n, denom)
            rows.append(row)
            continue

        score_label = "count, mean (SD)" if str(feature.get("score_aggregation", "")) == "count" else "mean (SD)"
        row = {"Question ID": items, "Variable": f"{variable}, {score_label}"}
        row["p-value"] = format_p_value(continuous_p_value(values, g, high_label, low_label))
        row["Between-group difference"] = format_effect_size(continuous_effect_size(values, g, high_label, low_label))
        row["Between-group difference type"] = "Cohen's d" if row["Between-group difference"] else ""
        for label_name, col_name in [(high_label, high_label), (low_label, low_label), ("Total", "Total")]:
            subset = values if label_name == "Total" else values[g.eq(label_name)]
            row[col_name] = format_mean_sd(subset)
        rows.append(row)

    return pd.DataFrame(rows, columns=[
        "Question ID",
        "Variable",
        high_label,
        low_label,
        "Total",
        "p-value",
        "Between-group difference",
        "Between-group difference type",
    ])


def write_wave_outputs(out_dir: Path, slug: str, title: str, table: pd.DataFrame, diag: dict[str, Any], grouping_note: str) -> None:
    xlsx_path = out_dir / f"table1_{slug}.xlsx"
    write_xlsx(table, xlsx_path, "Table1")


NETWORK_CONCEPTS_FOR_COMBINED_TABLE = [
    "Outgoing Friendship Nominations",
    "Incoming Friendship Nominations",
    "Outgoing Negative Nominations",
    "Incoming Negative Nominations",
    "Reciprocal Friendship Ties",
    "Reciprocal Negative Ties",
    "Sent Positive Tie Ratio",
    "Received Positive Tie Ratio",
    "Sent Network Valence",
    "Received Network Valence",
]


def is_network_table1_row(variable: Any) -> bool:
    s = str(variable)
    return any(concept in s for concept in NETWORK_CONCEPTS_FOR_COMBINED_TABLE)


def find_network_table1_row(table: pd.DataFrame, concept: str) -> pd.Series | None:
    mask = table["Variable"].astype(str).str.contains(concept, regex=False, na=False)
    if not mask.any():
        return None
    return table.loc[mask].iloc[0].copy()


def relabel_network_table1_row(row: pd.Series, concept: str, version_label: str) -> pd.Series:
    row = row.copy()
    row["Variable"] = f"{concept} ({version_label}), mean (SD)"
    return row


def combine_observed_and_normalized_network_rows(observed_table: pd.DataFrame, normalized_table: pd.DataFrame) -> pd.DataFrame:
    network_mask = observed_table["Variable"].apply(is_network_table1_row)
    insert_at = int(network_mask.idxmax()) if network_mask.any() else len(observed_table)
    non_network = observed_table.loc[~network_mask].copy()
    before = non_network[non_network.index < insert_at]
    after = non_network[non_network.index >= insert_at]

    network_rows: list[pd.Series] = []
    for concept in NETWORK_CONCEPTS_FOR_COMBINED_TABLE:
        observed_row = find_network_table1_row(observed_table, concept)
        normalized_row = find_network_table1_row(normalized_table, concept)
        if observed_row is not None:
            network_rows.append(relabel_network_table1_row(observed_row, concept, "Observed"))
        if normalized_row is not None:
            network_rows.append(relabel_network_table1_row(normalized_row, concept, "Respondent-class-normalized"))

    combined = pd.concat([before, pd.DataFrame(network_rows), after], ignore_index=True)
    return combined[list(observed_table.columns)]


def write_notes(diags: list[dict[str, Any]]) -> None:
    diag_df = pd.DataFrame(diags)
    write_xlsx(diag_df, DIAG_OUT / "table1_drop_decomposition_diagnostics.xlsx", "Diagnostics")
    (DIAG_OUT / "table1_drop_decomposition_diagnostics.json").write_text(
        json.dumps(diags, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    for p in [ONLINE_OUT, DISTRESS_OUT, ONLINE_ADJUSTED_OUT, DISTRESS_ADJUSTED_OUT, DIAG_OUT]:
        p.mkdir(parents=True, exist_ok=True)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    merged_path = t23.core.pick_first_existing_path(t23.core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")
    for c in ["Year", "Group_ID", "Question_ID"]:
        if c in merged.columns:
            merged[c] = merged[c].astype(str).str.strip()

    datasets = {
        "W2": t23.core.normalize_student_id(pd.read_csv(W2_DATA, encoding="utf-8-sig", low_memory=False)),
        "W3": t23.core.normalize_student_id(pd.read_csv(W3_DATA, encoding="utf-8-sig", low_memory=False)),
    }
    online_items = {"W2": ["v21_3", "v21_4", "v21_5", "v21_6"], "W3": ["21-3", "21-4", "21-5", "21-6"]}
    distress_items = {"W2": t23.TARGET_W2_ITEMS, "W3": t23.TARGET_W3_ITEMS}
    slugs = {"W2": "w2_2024", "W3": "w3_2025"}
    titles = {"W2": "W2 2024", "W3": "W3 2025"}
    all_diags: list[dict[str, Any]] = []

    for wave, df in datasets.items():
        X, feature_defs, feature_diag = build_feature_context(
            wave,
            df,
            merged,
            interpersonal_specs=INTERPERSONAL_TABLE1_FEATURES,
            interpersonal_label="observed",
        )

        online_group, online_diag = classify_online_activity(df, online_items[wave])
        online_table = build_table(wave, X, feature_defs, online_group, (GROUP_HIGH_ONLINE, GROUP_LOW_ONLINE), config)
        write_wave_outputs(
            ONLINE_OUT,
            slugs[wave],
            f"{titles[wave]} by Online Activity Group",
            online_table,
            online_diag,
            "Stratification variable: High vs Low Online Activity.",
        )
        all_diags.append({"wave": wave, **online_diag, **feature_diag})

        distress_group, distress_diag = classify_psychological_distress(df, distress_items[wave])
        distress_table = build_table(wave, X, feature_defs, distress_group, (GROUP_HIGH_DISTRESS, GROUP_LOW_DISTRESS), config)
        write_wave_outputs(
            DISTRESS_OUT,
            slugs[wave] + "_psychological_distress",
            f"{titles[wave]} by Psychological Distress Group",
            distress_table,
            distress_diag,
            "Stratification variable: High vs Low Psychological Distress.",
        )
        all_diags.append({"wave": wave, **distress_diag, **feature_diag})

        X_norm, feature_defs_norm, feature_diag_norm = build_feature_context(
            wave,
            df,
            merged,
            interpersonal_specs=INTERPERSONAL_TABLE1_NORMALIZED_FEATURES,
            interpersonal_label="respondent_class_normalized",
        )
        online_norm_table = build_table(
            wave,
            X_norm,
            feature_defs_norm,
            online_group,
            (GROUP_HIGH_ONLINE, GROUP_LOW_ONLINE),
            config,
        )
        write_wave_outputs(
            ONLINE_ADJUSTED_OUT,
            slugs[wave] + "_class_adjusted_network",
            f"{titles[wave]} by Online Activity Group, respondent-class-normalized network indicators",
            online_norm_table,
            online_diag,
            "Interpersonal network count features are normalized by same-class respondents minus one.",
        )
        all_diags.append({"wave": wave, "sensitivity": "respondent_class_normalized", **online_diag, **feature_diag_norm})

        distress_norm_table = build_table(
            wave,
            X_norm,
            feature_defs_norm,
            distress_group,
            (GROUP_HIGH_DISTRESS, GROUP_LOW_DISTRESS),
            config,
        )
        write_wave_outputs(
            DISTRESS_ADJUSTED_OUT,
            slugs[wave] + "_psychological_distress_class_adjusted_network",
            f"{titles[wave]} by Psychological Distress Group, respondent-class-normalized network indicators",
            distress_norm_table,
            distress_diag,
            "Interpersonal network count features are normalized by same-class respondents minus one.",
        )
        all_diags.append({"wave": wave, "sensitivity": "respondent_class_normalized", **distress_diag, **feature_diag_norm})

    write_notes(all_diags)
    print("Wrote drop + decomposition Table 1 outputs.")
    print(pd.DataFrame(all_diags).to_string(index=False))


if __name__ == "__main__":
    main()
