from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress")
W2_PATH = (
    BASE_DIR
    / r"Data\2024data\TIGPS_W2_studentdata_ver6_cleaned_mental_common_only(standerdized).csv"
)
OUT_DIR = BASE_DIR / r"Code\EDA\W2_cronbach_reliability"
OUT_SUMMARY = OUT_DIR / "v25_v26_v27_reliability_ver6_summary.txt"


def cronbach_alpha(df: pd.DataFrame) -> float:
    """Cronbach's alpha using listwise-complete rows."""
    x = df.dropna(axis=0, how="any")
    if x.shape[0] == 0:
        return np.nan
    k = x.shape[1]
    if k < 2:
        return np.nan
    item_vars = x.var(ddof=1, axis=0)
    total_scores = x.sum(axis=1)
    total_var = total_scores.var(ddof=1)
    if total_var == 0 or np.isnan(total_var):
        return np.nan
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def make_cols(prefix: str, idxs: list[int]) -> list[str]:
    return [f"{prefix}_{i}" for i in idxs]


def analyze_multi_item_set(
    df: pd.DataFrame,
    item_cols: list[str],
) -> dict[str, object]:
    missing_cols = [c for c in item_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    data = df[item_cols].apply(pd.to_numeric, errors="coerce")
    n_total = int(len(data))
    listwise = data.dropna(axis=0, how="any")
    n_complete = int(len(listwise))
    alpha = cronbach_alpha(data)

    alpha_if_deleted_rows = []
    for col in item_cols:
        remaining = data[[c for c in item_cols if c != col]]
        alpha_del = cronbach_alpha(remaining)
        alpha_if_deleted_rows.append(
            {
                "item": col,
                "alpha_if_deleted": alpha_del,
                "n_non_missing": int(data[col].notna().sum()),
                "mean": float(data[col].mean()) if data[col].notna().any() else np.nan,
                "std": float(data[col].std(ddof=1)) if data[col].notna().sum() >= 2 else np.nan,
                "min": float(data[col].min()) if data[col].notna().any() else np.nan,
                "max": float(data[col].max()) if data[col].notna().any() else np.nan,
            }
        )
    alpha_if_deleted_df = pd.DataFrame(alpha_if_deleted_rows)

    return {
        "item_cols": item_cols,
        "n_total": n_total,
        "n_complete": n_complete,
        "alpha": alpha,
        "alpha_if_deleted_df": alpha_if_deleted_df,
    }


def analyze_single_item(df: pd.DataFrame, col: str) -> dict[str, object]:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")
    s = pd.to_numeric(df[col], errors="coerce")
    return {
        "item": col,
        "n_total": int(len(s)),
        "n_non_missing": int(s.notna().sum()),
        "mean": float(s.mean()) if s.notna().any() else np.nan,
        "std": float(s.std(ddof=1)) if s.notna().sum() >= 2 else np.nan,
        "min": float(s.min()) if s.notna().any() else np.nan,
        "median": float(s.median()) if s.notna().any() else np.nan,
        "max": float(s.max()) if s.notna().any() else np.nan,
    }


def fmt_num(x: object, digits: int = 3) -> str:
    try:
        if pd.isna(x):
            return "nan"
    except Exception:
        pass
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return str(x)


def write_multi_item_section(f, title: str, result: dict[str, object]) -> None:
    item_cols = result["item_cols"]
    alpha_if_deleted_df = result["alpha_if_deleted_df"]

    f.write(f"{title}\n")
    f.write(f"Items: {', '.join(item_cols)}\n")
    f.write(f"Total rows: {result['n_total']}\n")
    f.write(f"Complete rows (listwise): {result['n_complete']}\n")
    f.write(f"Cronbach alpha (listwise): {fmt_num(result['alpha'])}\n")
    f.write("Alpha if item deleted:\n")
    for _, r in alpha_if_deleted_df.iterrows():
        f.write(f"- {r['item']}: {fmt_num(r['alpha_if_deleted'])}\n")
    f.write("Item descriptive stats:\n")
    for _, r in alpha_if_deleted_df.iterrows():
        f.write(
            f"- {r['item']}: n={int(r['n_non_missing'])}, "
            f"mean={fmt_num(r['mean'])}, std={fmt_num(r['std'])}, "
            f"min={fmt_num(r['min'])}, max={fmt_num(r['max'])}\n"
        )
    f.write("\n")


def write_single_item_section(f, title: str, result: dict[str, object]) -> None:
    f.write(f"{title}\n")
    f.write(f"Item: {result['item']}\n")
    f.write(f"Total rows: {result['n_total']}\n")
    f.write(f"Non-missing rows: {result['n_non_missing']}\n")
    f.write("Cronbach alpha: not defined for single-item measure\n")
    f.write(
        f"Descriptive stats: mean={fmt_num(result['mean'])}, median={fmt_num(result['median'])}, "
        f"std={fmt_num(result['std'])}, min={fmt_num(result['min'])}, max={fmt_num(result['max'])}\n"
    )
    f.write("\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(W2_PATH, low_memory=False)

    # Requested analyses
    v25_full = analyze_multi_item_set(df, make_cols("v25", list(range(1, 16))))

    v26_1_6 = analyze_multi_item_set(df, make_cols("v26", [1, 2, 3, 4, 5, 6]))
    v26_1_3 = analyze_multi_item_set(df, make_cols("v26", [1, 2, 3]))
    v26_4_6 = analyze_multi_item_set(df, make_cols("v26", [4, 5, 6]))

    # v27 full == alpha(1-4), plus v27_1-3 and v27_4 as single item.
    v27_1_4 = analyze_multi_item_set(df, make_cols("v27", [1, 2, 3, 4]))
    v27_1_3 = analyze_multi_item_set(df, make_cols("v27", [1, 2, 3]))
    v27_4_single = analyze_single_item(df, "v27_4")

    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("W2 ver6 Cronbach Reliability Summary (v25, v26, v27)\n")
        f.write(f"Data: {W2_PATH}\n\n")

        write_multi_item_section(f, "[v25] Full scale alpha + alpha if item deleted", v25_full)

        write_multi_item_section(f, "[v26] alpha(1-6)", v26_1_6)
        write_multi_item_section(f, "[v26] alpha(1-3)", v26_1_3)
        write_multi_item_section(f, "[v26] alpha(4-6)", v26_4_6)

        write_multi_item_section(
            f,
            "[v27] Full scale alpha (same as alpha(1-4)) + alpha if item deleted",
            v27_1_4,
        )
        write_multi_item_section(f, "[v27] alpha(1-3)", v27_1_3)
        write_single_item_section(f, "[v27] item 4 as single item", v27_4_single)

    print(f"Wrote summary: {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
