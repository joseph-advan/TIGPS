from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from scipy import stats


TABLE1_DIR = Path(__file__).resolve().parents[1]
ROOT = TABLE1_DIR.parents[3]
OUTPUT_DIR = TABLE1_DIR / "outputs"
CONFIG_DIR = TABLE1_DIR / "config"
DIAGNOSTICS_DIR = TABLE1_DIR / "diagnostics"

W2_DATA = ROOT / "Data" / "testing_clean" / "W2" / "TIGPS_W2_studentdata_ver6.csv"
W3_DATA = ROOT / "Data" / "testing_clean" / "W3" / "TIGPS_W3_student_studentdata_ver5.csv"
PLAN_PATH = CONFIG_DIR / "table1_variable_plan_draft.csv"
CONFIG_PATH = CONFIG_DIR / "table1_scoring_config.json"


def parse_columns(value: str) -> list[str]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text or text.startswith("__"):
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def to_numeric_frame(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df[columns].apply(pd.to_numeric, errors="coerce")


def format_n_pct(n: int, denom: int) -> str:
    if denom <= 0:
        return "NA"
    return f"{n} ({n / denom * 100:.1f}%)"


def format_mean_sd(values: pd.Series) -> str:
    values = pd.to_numeric(values, errors="coerce").dropna()
    if values.empty:
        return "NA"
    return f"{values.mean():.2f} ({values.std(ddof=1):.2f})"


def format_p_value(p_value: float | None) -> str:
    if p_value is None or pd.isna(p_value):
        return ""
    if p_value < 0.001:
        return "<0.001"
    return f"{p_value:.3f}"


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


def continuous_p_value(score: pd.Series, group: pd.Series) -> float | None:
    high = pd.to_numeric(score[group.eq("High Online Activity")], errors="coerce").dropna()
    low = pd.to_numeric(score[group.eq("Low Online Activity")], errors="coerce").dropna()
    if len(high) < 2 or len(low) < 2:
        return None
    try:
        _, p_value = stats.ttest_ind(high, low, equal_var=False, nan_policy="omit")
        return float(p_value)
    except Exception:
        return None


def markdown_table(df: pd.DataFrame) -> str:
    lines = []
    cols = list(df.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in cols) + " |")
    return "\n".join(lines)


def classify_online_activity(df: pd.DataFrame, items: list[str]) -> tuple[pd.Series, dict[str, object]]:
    activity_items = to_numeric_frame(df, items)
    valid_count = activity_items.notna().sum(axis=1)
    complete = valid_count.eq(len(items))
    activity_sum = activity_items.sum(axis=1, min_count=len(items))
    median = activity_sum.median(skipna=True)
    group = pd.Series(pd.NA, index=df.index, dtype="object")
    group[complete & activity_sum.gt(median)] = "High Online Activity"
    group[complete & activity_sum.le(median)] = "Low Online Activity"
    diagnostics = {
        "items": items,
        "median": float(median),
        "rows": int(len(df)),
        "classified": int(group.notna().sum()),
        "high": int(group.eq("High Online Activity").sum()),
        "low": int(group.eq("Low Online Activity").sum()),
        "unclassified": int(group.isna().sum()),
        "all_items_valid": int(complete.sum()),
        "partial_missing": int(((valid_count > 0) & (valid_count < len(items))).sum()),
        "all_missing": int(valid_count.eq(0).sum()),
        "item_missing_counts": {col: int(activity_items[col].isna().sum()) for col in items},
    }
    return group, diagnostics


def apply_reverse(
    values: pd.DataFrame, columns: list[str], reverse_columns: list[str], min_value: float, max_value: float
) -> pd.DataFrame:
    out = values.copy()
    for col in reverse_columns:
        if col in out.columns:
            out[col] = min_value + max_value - out[col]
    return out


def scale_score(
    df: pd.DataFrame,
    columns: list[str],
    reverse_columns: list[str] | None,
    min_value: float,
    max_value: float,
    min_valid_fraction: float,
) -> pd.Series:
    values = to_numeric_frame(df, columns)
    if reverse_columns:
        values = apply_reverse(values, columns, reverse_columns, min_value, max_value)
    min_valid = max(1, int(len(columns) * min_valid_fraction + 0.999999))
    valid_count = values.notna().sum(axis=1)
    score = values.mean(axis=1, skipna=True)
    score[valid_count < min_valid] = pd.NA
    return score


def category_label(variable: str, raw_value: object, config: dict[str, object], reverse_key: str) -> str:
    if variable == "Gender":
        labels = config["category_labels"]["gender"]["labels"]
        key = str(int(raw_value)) if pd.notna(raw_value) and float(raw_value).is_integer() else str(raw_value)
        return labels.get(key, key)
    if variable == "Parental Marital Status / Family Structure":
        family_cfg = config["category_labels"]["family_structure"]
        labels = family_cfg[f"{reverse_key}_labels"]
        key = str(int(raw_value)) if pd.notna(raw_value) and float(raw_value).is_integer() else str(raw_value)
        return labels.get(key, key)
    if pd.notna(raw_value):
        try:
            numeric = float(raw_value)
            if numeric.is_integer():
                return str(int(numeric))
        except Exception:
            pass
    return str(raw_value)


def build_table_for_wave(
    wave_label: str,
    df: pd.DataFrame,
    plan: pd.DataFrame,
    config: dict[str, object],
    online_items: list[str],
    column_key: str,
    reverse_key: str,
) -> tuple[pd.DataFrame, dict[str, object]]:
    group, diagnostics = classify_online_activity(df, online_items)
    working = df.loc[group.notna()].copy()
    working["_online_activity_group"] = group[group.notna()]

    rows: list[dict[str, str]] = [
        {
            "Variable": "N",
            "High Online Activity": str(int(working["_online_activity_group"].eq("High Online Activity").sum())),
            "Low Online Activity": str(int(working["_online_activity_group"].eq("Low Online Activity").sum())),
            "Total": str(int(len(working))),
            "p-value": "",
        }
    ]

    min_valid_fraction = float(config["scale_score_rule"]["minimum_valid_item_fraction"])
    parenting_cfg = config["reverse_coding"]["parenting_practices_parent_child_interaction_quality"]
    parenting_reverse = set(parenting_cfg[f"{reverse_key}_reverse_items"])
    parenting_min = float(parenting_cfg["min_value"])
    parenting_max = float(parenting_cfg["max_value"])

    for _, item in plan.sort_values("order").iterrows():
        variable = item["variable"]
        if variable == "Group size / analytic N":
            continue

        presentation = item["table1_presentation"]
        variable_type = item["variable_type"]
        columns = [col for col in parse_columns(item[column_key]) if col in working.columns]
        if not columns:
            rows.append(
                {
                    "Variable": f"{variable}",
                    "High Online Activity": "NA",
                    "Low Online Activity": "NA",
                    "Total": "NA",
                }
            )
            continue

        if presentation == "n (%)":
            series = pd.to_numeric(working[columns[0]], errors="coerce")
            categories = sorted(series.dropna().unique())
            p_text = format_p_value(categorical_p_value(series, working["_online_activity_group"]))
            for cat in categories:
                label = category_label(variable, cat, config, reverse_key)
                row = {"Variable": f"{variable}: {label}"}
                for group_name, col_name in [
                    ("High Online Activity", "High Online Activity"),
                    ("Low Online Activity", "Low Online Activity"),
                    ("Total", "Total"),
                ]:
                    subset = working if group_name == "Total" else working[working["_online_activity_group"].eq(group_name)]
                    subset_series = pd.to_numeric(subset[columns[0]], errors="coerce")
                    denom = int(subset_series.notna().sum())
                    n = int(subset_series.eq(cat).sum())
                    row[col_name] = format_n_pct(n, denom)
                row["p-value"] = p_text
                p_text = ""
                rows.append(row)

        elif presentation == "yes n (%)" or variable_type == "binary":
            series = pd.to_numeric(working[columns[0]], errors="coerce")
            row = {"Variable": f"{variable}: Yes"}
            row["p-value"] = format_p_value(binary_p_value(series, working["_online_activity_group"]))
            for group_name, col_name in [
                ("High Online Activity", "High Online Activity"),
                ("Low Online Activity", "Low Online Activity"),
                ("Total", "Total"),
            ]:
                subset = working if group_name == "Total" else working[working["_online_activity_group"].eq(group_name)]
                subset_series = pd.to_numeric(subset[columns[0]], errors="coerce")
                denom = int(subset_series.notna().sum())
                n = int(subset_series.eq(1).sum())
                row[col_name] = format_n_pct(n, denom)
            rows.append(row)

        elif presentation == "mean (SD)":
            reverse_columns: list[str] = []
            min_value, max_value = 1.0, 4.0
            if variable == "Parenting Practices and Parent-Child Interaction Quality":
                reverse_columns = [col for col in columns if col in parenting_reverse]
                min_value, max_value = parenting_min, parenting_max

            if len(columns) == 1 and variable_type == "single_item_ordinal":
                score = pd.to_numeric(working[columns[0]], errors="coerce")
            else:
                score = scale_score(working, columns, reverse_columns, min_value, max_value, min_valid_fraction)

            row = {"Variable": f"{variable}, mean (SD)"}
            row["p-value"] = format_p_value(continuous_p_value(score, working["_online_activity_group"]))
            for group_name, col_name in [
                ("High Online Activity", "High Online Activity"),
                ("Low Online Activity", "Low Online Activity"),
                ("Total", "Total"),
            ]:
                mask = pd.Series(True, index=working.index)
                if group_name != "Total":
                    mask = working["_online_activity_group"].eq(group_name)
                row[col_name] = format_mean_sd(score[mask])
            rows.append(row)

        else:
            rows.append(
                {
                    "Variable": f"{variable}",
                    "High Online Activity": "UNSUPPORTED",
                    "Low Online Activity": "UNSUPPORTED",
                    "Total": "UNSUPPORTED",
                    "p-value": "",
                }
            )

    table = pd.DataFrame(rows, columns=["Variable", "High Online Activity", "Low Online Activity", "Total", "p-value"])
    diagnostics["wave"] = wave_label
    return table, diagnostics


def write_wave_outputs(wave_slug: str, wave_title: str, table: pd.DataFrame, diagnostics: dict[str, object]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / f"table1_{wave_slug}.csv"
    md_path = OUTPUT_DIR / f"table1_{wave_slug}.md"
    table.to_csv(csv_path, index=False, encoding="utf-8-sig")

    md = [
        f"# Table 1: {wave_title}",
        "",
        "Stratification variable: High vs Low Online Activity.",
        "",
        f"- Median online activity sum: {diagnostics['median']}",
        f"- Classified students: {diagnostics['classified']}",
        f"- Excluded due to incomplete online activity items: {diagnostics['unclassified']}",
        "",
        markdown_table(table),
        "",
    ]
    md_path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    plan = pd.read_csv(PLAN_PATH, encoding="utf-8-sig")

    w2 = pd.read_csv(W2_DATA, encoding="utf-8-sig", low_memory=False)
    w3 = pd.read_csv(W3_DATA, encoding="utf-8-sig", low_memory=False)

    w2_table, w2_diag = build_table_for_wave(
        "W2 2024",
        w2,
        plan,
        config,
        config["online_activity_grouping"]["w2_items"],
        "w2_columns",
        "w2",
    )
    w3_table, w3_diag = build_table_for_wave(
        "W3 2025",
        w3,
        plan,
        config,
        config["online_activity_grouping"]["w3_items"],
        "w3_columns",
        "w3",
    )

    write_wave_outputs("w2_2024", "W2 2024", w2_table, w2_diag)
    write_wave_outputs("w3_2025", "W3 2025", w3_table, w3_diag)

    diagnostics = pd.DataFrame([w2_diag, w3_diag])
    diagnostics.to_csv(
        DIAGNOSTICS_DIR / "table1_online_activity_group_diagnostics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    notes = [
        "# Table 1 Generation Notes",
        "",
        "## Input Data",
        "",
        f"- W2: `{W2_DATA.relative_to(ROOT)}`",
        f"- W3: `{W3_DATA.relative_to(ROOT)}`",
        f"- Variable plan: `{PLAN_PATH.relative_to(ROOT)}`",
        f"- Scoring config: `{CONFIG_PATH.relative_to(ROOT)}`",
        "",
        "## Grouping Rule",
        "",
        "- Students must have all four online activity items valid.",
        "- High Online Activity: `online_activity_sum > wave-specific median`.",
        "- Low Online Activity: `online_activity_sum <= wave-specific median`.",
        "",
        "## Presentation Rule",
        "",
        "- Categorical variables: `n (%)` by response category.",
        "- Binary variables: coded `1` as `Yes n (%)`.",
        "- Single-item ordinal variables: `mean (SD)`.",
        "- Multi-item scales: mean of available items, requiring at least 50% valid items.",
        "- p-values compare High vs Low Online Activity.",
        "- Categorical and binary variables use chi-square tests; binary variables use Fisher's exact test if expected cell counts are below 5.",
        "- Single-item ordinal and multi-item scale variables use Welch two-sample t-tests.",
        "",
        "## Reverse Coding",
        "",
        "- Parenting Practices and Parent-Child Interaction Quality uses reverse coding.",
        "- W2 reverse-coded items: `v6_1`, `v6_5`, `v6_6`, `v6_8`, `v6_9`.",
        "- W3 reverse-coded items: `5-1`, `5-5`, `5-6`, `5-8`, `5-9`.",
        "- Formula: `reversed_value = min + max - original_value`, with `min = 1`, `max = 4`.",
        "",
        "## Gender Label",
        "",
        "- `1 = Male`.",
        "- `2 = Female`.",
        "",
        "## Outputs",
        "",
        "- `table1_w2_2024.csv`",
        "- `table1_w2_2024.md`",
        "- `table1_w3_2025.csv`",
        "- `table1_w3_2025.md`",
        "- `diagnostics/table1_online_activity_group_diagnostics.csv`",
    ]
    (DIAGNOSTICS_DIR / "table1_generation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print("Wrote Table 1 outputs to:", OUTPUT_DIR)
    print("W2 rows:", len(w2_table), "W3 rows:", len(w3_table))


if __name__ == "__main__":
    main()
