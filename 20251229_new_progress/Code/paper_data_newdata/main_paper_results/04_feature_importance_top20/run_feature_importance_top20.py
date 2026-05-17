from __future__ import annotations

import json
import shutil
import textwrap
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


SCRIPT_PATH = Path(__file__).resolve()
SECTION_DIR = SCRIPT_PATH.parent
PAPER_RESULTS_DIR = SECTION_DIR.parent
PAPER_DATA_DIR = PAPER_RESULTS_DIR.parent

SOURCE_XLSX = (
    PAPER_RESULTS_DIR
    / "03_interpersonal_incremental_modeling"
    / "outputs"
    / "interpersonal_feature_selection_summary.xlsx"
)

OUT_DIR = SECTION_DIR / "outputs"
DIAG_DIR = OUT_DIR / "diagnostics"
FIG_DIR = OUT_DIR / "figures"
MAIN_XLSX = OUT_DIR / "lasso_top20_feature_importance_with_categories.xlsx"
SUMMARY_MD = OUT_DIR / "LASSO_TOP20_FEATURE_IMPORTANCE_SUMMARY.md"
DIAGNOSTICS_JSON = DIAG_DIR / "lasso_top20_feature_importance_diagnostics.json"

MAIN_FEATURE_SET = "decomposed_plus_12_interpersonal"
TOP_N = 20


CATEGORY_RULES = [
    ("Interpersonal Network", lambda code, name: str(code).startswith("ip_")),
    ("SEL / Resilience", lambda code, name: str(code).startswith("v54") or str(code) == "v52"),
    ("Family / Parenting", lambda code, name: str(code) in {"v5", "v6", "v19"}),
    (
        "Online / Digital Life",
        lambda code, name: str(code).startswith(("v22", "v23", "v25", "v26", "v27"))
        or str(code) in {"v28", "v49"},
    ),
    ("Bullying / Victimization", lambda code, name: str(code) in {"v34", "v36", "v38", "v40"}),
    ("Delinquency / Risk Behavior", lambda code, name: str(code) == "v42"),
    ("Demographic / Social Status", lambda code, name: str(code) in {"v1", "1", "v1_male", "1_male", "v3"}),
]

CATEGORY_ORDER = [
    "SEL / Resilience",
    "Family / Parenting",
    "Online / Digital Life",
    "Bullying / Victimization",
    "Interpersonal Network",
    "Demographic / Social Status",
    "Delinquency / Risk Behavior",
    "Other",
]

CATEGORY_COLORS = {
    "SEL / Resilience": "#2F6B4F",
    "Family / Parenting": "#B56B45",
    "Online / Digital Life": "#2F5F98",
    "Bullying / Victimization": "#A33A3A",
    "Interpersonal Network": "#6C5A9E",
    "Demographic / Social Status": "#6B7280",
    "Delinquency / Risk Behavior": "#9A7B22",
    "Other": "#8A8A8A",
}

MODEL_ORDER = {
    "LASSO Logistic": 1,
    "Ridge Logistic": 2,
    "Multivariable Logistic": 3,
}

TASK_ORDER = {"W2 -> W2": 1, "W2 -> W3": 2}


def reset_outputs() -> None:
    out_resolved = OUT_DIR.resolve()
    section_resolved = SECTION_DIR.resolve()
    if out_resolved.parent != section_resolved:
        raise RuntimeError(f"Refusing to remove unexpected output path: {out_resolved}")
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def categorize(feature_code: Any, variable: Any) -> str:
    code = "" if pd.isna(feature_code) else str(feature_code)
    name = "" if pd.isna(variable) else str(variable)
    for category, rule in CATEGORY_RULES:
        if rule(code, name):
            return category
    return "Other"


def load_coefficients() -> pd.DataFrame:
    if not SOURCE_XLSX.exists():
        raise FileNotFoundError(f"Missing source coefficient workbook: {SOURCE_XLSX}")
    df = pd.read_excel(SOURCE_XLSX, sheet_name="AllCoefficientsLong")
    df = df[df["Feature Set"].eq(MAIN_FEATURE_SET)].copy()
    df["Abs Std. B"] = pd.to_numeric(df["Abs Std. B"], errors="coerce")
    df["Std. B"] = pd.to_numeric(df["Std. B"], errors="coerce")
    df["Relative Importance %"] = pd.to_numeric(df["Relative Importance %"], errors="coerce")
    df["Rank by Abs Std. B"] = pd.to_numeric(df["Rank by Abs Std. B"], errors="coerce")
    df["Direction"] = df["Std. B"].apply(lambda v: "Positive" if pd.notna(v) and v > 0 else ("Negative" if pd.notna(v) and v < 0 else "Zero"))
    df["Category"] = [categorize(code, var) for code, var in zip(df["Feature Code"], df["Variable"])]
    df["Variable"] = df["Variable"].astype(str).str.replace("Parent?hild", "Parent-Child", regex=False)
    df["Task Order"] = df["Task"].map(TASK_ORDER).fillna(99)
    df["Model Order"] = df["Model"].map(MODEL_ORDER).fillna(99)
    df = df.sort_values(["Task Order", "Model Order", "Rank by Abs Std. B", "Feature Code"]).reset_index(drop=True)
    return df


def top_n(df: pd.DataFrame, model: str, n: int = TOP_N) -> pd.DataFrame:
    sub = df[df["Model"].eq(model)].copy()
    out = sub[sub["Rank by Abs Std. B"].le(n)].copy()
    out = out.sort_values(["Task Order", "Rank by Abs Std. B", "Feature Code"])
    cols = [
        "Task",
        "Model",
        "Rank by Abs Std. B",
        "Variable",
        "Feature Code",
        "Category",
        "Std. B",
        "Abs Std. B",
        "Relative Importance %",
        "Direction",
        "Selected by LASSO",
        "Is Interpersonal Feature",
        "Items",
    ]
    return out[[c for c in cols if c in out.columns]]


def lasso_top20_by_task(lasso_top20: pd.DataFrame, task: str) -> pd.DataFrame:
    return lasso_top20[lasso_top20["Task"].eq(task)].copy()


def category_summary(lasso_top20: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for task, sub in lasso_top20.groupby("Task", sort=False):
        for cat in CATEGORY_ORDER:
            g = sub[sub["Category"].eq(cat)]
            if g.empty:
                continue
            rows.append(
                {
                    "Task": task,
                    "Category": cat,
                    "N Top 20 Features": int(len(g)),
                    "Relative Importance Sum %": float(g["Relative Importance %"].sum(skipna=True)),
                    "Mean Relative Importance %": float(g["Relative Importance %"].mean(skipna=True)),
                    "Top Feature": g.sort_values("Rank by Abs Std. B").iloc[0]["Variable"],
                    "Top Feature Rank": int(g["Rank by Abs Std. B"].min()),
                }
            )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["_task_order"] = out["Task"].map(TASK_ORDER).fillna(99)
    out["_category_order"] = out["Category"].map({c: i for i, c in enumerate(CATEGORY_ORDER, 1)}).fillna(99)
    out = out.sort_values(["_task_order", "_category_order"]).drop(columns=["_task_order", "_category_order"])
    return out.reset_index(drop=True)


def category_pivot(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return summary
    count = summary.pivot(index="Category", columns="Task", values="N Top 20 Features")
    imp = summary.pivot(index="Category", columns="Task", values="Relative Importance Sum %")
    out = pd.DataFrame(index=CATEGORY_ORDER)
    for task in TASK_ORDER:
        out[f"{task} N Top 20"] = count.get(task)
        out[f"{task} Relative Importance Sum %"] = imp.get(task)
    out = out.dropna(how="all").reset_index(names="Category")
    return out


def shared_top20(lasso_top20: pd.DataFrame) -> pd.DataFrame:
    w2 = lasso_top20[lasso_top20["Task"].eq("W2 -> W2")].copy()
    w3 = lasso_top20[lasso_top20["Task"].eq("W2 -> W3")].copy()
    shared = w2.merge(
        w3,
        on="Feature Code",
        how="inner",
        suffixes=(" W2->W2", " W2->W3"),
    )
    if shared.empty:
        return shared
    rows = []
    for _, row in shared.iterrows():
        rows.append(
            {
                "Feature Code": row["Feature Code"],
                "Variable": row["Variable W2->W2"],
                "Category": row["Category W2->W2"],
                "W2 -> W2 Rank": row["Rank by Abs Std. B W2->W2"],
                "W2 -> W2 Std. B": row["Std. B W2->W2"],
                "W2 -> W2 Relative Importance %": row["Relative Importance % W2->W2"],
                "W2 -> W3 Rank": row["Rank by Abs Std. B W2->W3"],
                "W2 -> W3 Std. B": row["Std. B W2->W3"],
                "W2 -> W3 Relative Importance %": row["Relative Importance % W2->W3"],
                "Same Direction": row["Direction W2->W2"] == row["Direction W2->W3"],
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["W2 -> W2 Rank", "W2 -> W3 Rank"]).reset_index(drop=True)


def interpersonal_summary(df: pd.DataFrame) -> pd.DataFrame:
    lasso = df[(df["Model"].eq("LASSO Logistic")) & (df["Is Interpersonal Feature"].astype(bool))].copy()
    rows = []
    for task, sub in lasso.groupby("Task", sort=False):
        selected = sub[sub["Selected by LASSO"].astype(bool)]
        top20 = sub[sub["Rank by Abs Std. B"].le(TOP_N)]
        removed = sub[~sub["Selected by LASSO"].astype(bool)]
        rows.append(
            {
                "Task": task,
                "N Interpersonal Features": int(len(sub)),
                "N Selected by LASSO": int(len(selected)),
                "N Removed by LASSO": int(len(removed)),
                "N in LASSO Top 20": int(len(top20)),
                "Interpersonal Relative Importance Sum %": float(sub["Relative Importance %"].sum(skipna=True)),
                "Top Interpersonal Feature": sub.sort_values("Rank by Abs Std. B").iloc[0]["Variable"],
                "Top Interpersonal Rank": int(sub["Rank by Abs Std. B"].min()),
                "Removed Features": "; ".join(removed["Variable"].astype(str).tolist()),
            }
        )
    return pd.DataFrame(rows)


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
                max_len = max(max_len, min(len(val), 72))
            ws.column_dimensions[letter].width = max(12, max_len + 2)
    wb.save(path)


def write_workbook(sheets: dict[str, pd.DataFrame]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(MAIN_XLSX, engine="openpyxl") as writer:
        for sheet, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet[:31], index=False)
    format_workbook(MAIN_XLSX)


def wrap_label(value: Any, width: int = 24) -> str:
    text = "" if pd.isna(value) else str(value)
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def save_lasso_top20_bar_chart(df: pd.DataFrame, task: str) -> Path:
    sub = lasso_top20_by_task(df, task).sort_values("Rank by Abs Std. B")
    safe_task = task.lower().replace(" ", "").replace("->", "_to_")
    path = FIG_DIR / f"lasso_top20_relative_importance_{safe_task}.png"
    if sub.empty:
        return path

    fig, ax = plt.subplots(figsize=(18, 8))
    colors = [CATEGORY_COLORS.get(cat, CATEGORY_COLORS["Other"]) for cat in sub["Category"]]
    ax.bar(range(len(sub)), sub["Relative Importance %"], color=colors)
    ax.set_title(f"LASSO Top 20 Relative Importance: {task}", fontsize=16, weight="bold")
    ax.set_ylabel("Relative Importance (%)")
    ax.set_xlabel("Variable")
    ax.set_xticks(range(len(sub)))
    ax.set_xticklabels([wrap_label(v, 18) for v in sub["Variable"]], rotation=65, ha="right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=CATEGORY_COLORS[cat])
        for cat in CATEGORY_ORDER
        if cat in set(sub["Category"])
    ]
    labels = [cat for cat in CATEGORY_ORDER if cat in set(sub["Category"])]
    ax.legend(handles, labels, loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_category_summary_chart(category_wide: pd.DataFrame) -> Path:
    path = FIG_DIR / "lasso_top20_category_relative_importance_summary.png"
    if category_wide.empty:
        return path

    plot_df = category_wide.set_index("Category")
    cols = [c for c in plot_df.columns if c.endswith("Relative Importance Sum %")]
    fig, ax = plt.subplots(figsize=(13, 7))
    x = range(len(plot_df.index))
    width = 0.36
    for i, col in enumerate(cols):
        offset = (i - (len(cols) - 1) / 2) * width
        label = col.replace(" Relative Importance Sum %", "")
        ax.bar([v + offset for v in x], plot_df[col], width=width, label=label)
    ax.set_title("LASSO Top 20 Relative Importance by Conceptual Category", fontsize=15, weight="bold")
    ax.set_ylabel("Relative Importance Sum (%)")
    ax.set_xlabel("Conceptual Category")
    ax.set_xticks(list(x))
    ax.set_xticklabels([wrap_label(v, 18) for v in plot_df.index], rotation=35, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def save_shared_top20_chart(shared: pd.DataFrame) -> Path:
    path = FIG_DIR / "shared_lasso_top20_relative_importance.png"
    if shared.empty:
        return path

    plot_df = shared.sort_values("W2 -> W2 Rank").copy()
    fig, ax = plt.subplots(figsize=(15, 8))
    y = range(len(plot_df))
    height = 0.36
    ax.barh([v + height / 2 for v in y], plot_df["W2 -> W2 Relative Importance %"], height=height, label="W2 -> W2")
    ax.barh([v - height / 2 for v in y], plot_df["W2 -> W3 Relative Importance %"], height=height, label="W2 -> W3")
    ax.set_title("Shared LASSO Top 20 Features Across Prediction Tasks", fontsize=15, weight="bold")
    ax.set_xlabel("Relative Importance (%)")
    ax.set_yticks(list(y))
    ax.set_yticklabels([wrap_label(v, 34) for v in plot_df["Variable"]], fontsize=9)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def write_chart_index(paths: list[Path]) -> pd.DataFrame:
    rows = []
    for path in paths:
        rows.append(
            {
                "Figure": path.name,
                "Path": str(path),
                "Purpose": {
                    "lasso_top20_relative_importance_w2_to_w2.png": "Top 20 LASSO predictors for W2 -> W2.",
                    "lasso_top20_relative_importance_w2_to_w3.png": "Top 20 LASSO predictors for W2 -> W3.",
                    "lasso_top20_category_relative_importance_summary.png": "Category-level relative-importance comparison across tasks.",
                    "shared_lasso_top20_relative_importance.png": "Variables appearing in both W2 -> W2 and W2 -> W3 LASSO Top 20 lists.",
                }.get(path.name, ""),
            }
        )
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows available._"
    show = df if max_rows is None else df.head(max_rows)
    return show.to_markdown(index=False)


def write_summary(
    lasso_top20: pd.DataFrame,
    category_sum: pd.DataFrame,
    category_wide: pd.DataFrame,
    shared: pd.DataFrame,
    ip_summary: pd.DataFrame,
    figure_paths: list[Path],
) -> None:
    lines = [
        "# LASSO Top 20 Feature Importance Summary",
        "",
        "## Purpose",
        "",
        "This section identifies the most important predictors after the interpersonal incremental modeling step. The main table uses the LASSO model with the drop + decomposition + 12 interpersonal feature set.",
        "",
        "## Main Interpretation",
        "",
        "- `03_interpersonal_incremental_modeling` asks whether the 12 interpersonal indicators improve model performance.",
        "- `04_feature_importance_top20` asks which variables actually appear among the strongest LASSO predictors.",
        "- LASSO is the primary model here because it can shrink weak features to zero and therefore supports feature-selection interpretation.",
        "",
        "## Main Outputs",
        "",
        f"- Workbook: `{MAIN_XLSX}`",
        f"- Source coefficients: `{SOURCE_XLSX}`",
        f"- Figures folder: `{FIG_DIR}`",
        "",
        "## Figures",
        "",
        md_table(write_chart_index(figure_paths)),
        "",
        "## Category-Level Summary",
        "",
        md_table(category_wide),
        "",
        "## Shared LASSO Top 20 Features Across W2 -> W2 and W2 -> W3",
        "",
        md_table(shared),
        "",
        "## Interpersonal Features in LASSO",
        "",
        md_table(ip_summary),
        "",
        "## W2 -> W2 LASSO Top 20",
        "",
        md_table(lasso_top20_by_task(lasso_top20, "W2 -> W2")),
        "",
        "## W2 -> W3 LASSO Top 20",
        "",
        md_table(lasso_top20_by_task(lasso_top20, "W2 -> W3")),
        "",
        "## Suggested Paper Logic",
        "",
        "The Top 20 results should be read after the interpersonal incremental model. If interpersonal variables rarely appear in the LASSO Top 20 and their total relative importance is modest, the paper can argue that interpersonal network indicators show limited incremental predictive contribution compared with individual-level SEL/resilience, family, online/digital life, and bullying-related predictors.",
        "",
        "Category summaries should be used to shift the discussion from individual questionnaire items to conceptual domains. The most stable domains across W2 -> W2 and W2 -> W3 are the strongest candidates for the manuscript's main interpretation and for the later interaction-analysis section.",
        "",
    ]
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def write_diagnostics(df: pd.DataFrame, sheets: dict[str, pd.DataFrame]) -> None:
    payload = {
        "source_xlsx": str(SOURCE_XLSX),
        "main_feature_set": MAIN_FEATURE_SET,
        "top_n": TOP_N,
        "n_source_rows": int(len(df)),
        "tasks": sorted(df["Task"].dropna().unique().tolist()),
        "models": sorted(df["Model"].dropna().unique().tolist()),
        "categories": CATEGORY_ORDER,
        "figures": [str(p) for p in sorted(FIG_DIR.glob("*.png"))],
        "sheets": {name: {"rows": int(len(sheet_df)), "columns": list(sheet_df.columns)} for name, sheet_df in sheets.items()},
    }
    DIAGNOSTICS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    reset_outputs()
    coef = load_coefficients()
    lasso_top20 = top_n(coef, "LASSO Logistic")
    ridge_top20 = top_n(coef, "Ridge Logistic")
    logistic_top20 = top_n(coef, "Multivariable Logistic")
    cat_sum = category_summary(lasso_top20)
    cat_wide = category_pivot(cat_sum)
    shared = shared_top20(lasso_top20)
    ip_sum = interpersonal_summary(coef)
    figure_paths = [
        save_lasso_top20_bar_chart(lasso_top20, "W2 -> W2"),
        save_lasso_top20_bar_chart(lasso_top20, "W2 -> W3"),
        save_category_summary_chart(cat_wide),
        save_shared_top20_chart(shared),
    ]

    readme = pd.DataFrame(
        [
            {
                "Item": "Primary model",
                "Description": "LASSO Logistic using decomposed + 12 interpersonal features.",
            },
            {
                "Item": "Primary tasks",
                "Description": "W2 -> W2 and W2 -> W3.",
            },
            {
                "Item": "Relative Importance %",
                "Description": "abs(standardized coefficient) divided by the sum of abs(standardized coefficients) within each task/model, multiplied by 100.",
            },
            {
                "Item": "Category Summary",
                "Description": "Counts and relative-importance sums for LASSO Top 20 features by conceptual domain.",
            },
        ]
    )

    sheets = {
        "ReadMe": readme,
        "LASSO_Top20_Combined": lasso_top20,
        "LASSO_Top20_W2toW2": lasso_top20_by_task(lasso_top20, "W2 -> W2"),
        "LASSO_Top20_W2toW3": lasso_top20_by_task(lasso_top20, "W2 -> W3"),
        "CategorySummary": cat_sum,
        "CategorySummaryWide": cat_wide,
        "SharedTop20": shared,
        "InterpersonalSummary": ip_sum,
        "Ridge_Top20_Reference": ridge_top20,
        "Logistic_Top20_Reference": logistic_top20,
        "FigureIndex": write_chart_index(figure_paths),
    }
    write_workbook(sheets)
    write_summary(lasso_top20, cat_sum, cat_wide, shared, ip_sum, figure_paths)
    write_diagnostics(coef, sheets)

    print(f"Wrote {MAIN_XLSX}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"Wrote {DIAGNOSTICS_JSON}")
    print("\nCategory summary:")
    print(cat_wide.to_string(index=False))
    print("\nInterpersonal summary:")
    print(ip_sum.to_string(index=False))


if __name__ == "__main__":
    main()
