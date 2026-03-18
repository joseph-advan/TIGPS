import os
import numpy as np
import pandas as pd


BASE_DIR = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress"
W2_PATH = os.path.join(
    BASE_DIR,
    r"Data\2024data\TIGPS_W2_studentdata_ver6_cleaned_mental_common_only(standerdized).csv",
)

OUT_DIR = os.path.join(BASE_DIR, r"Code\EDA\v25_reliability")
SCALE_PREFIX = "v37"
OUT_SUMMARY = os.path.join(OUT_DIR, f"{SCALE_PREFIX}_reliability_summary.txt")
ITEM_SETS = {
    "1-8": list(range(1, 9)),
}

WRITE_ITEM_STATS_CSV = False
WRITE_ALPHA_IF_DELETED_CSV = False


def cronbach_alpha(df: pd.DataFrame) -> float:
    # Listwise complete cases
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


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(W2_PATH, low_memory=False)
    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write(f"{SCALE_PREFIX.upper()} Reliability (W2)\n")
        f.write("\n")

        for set_name, idxs in ITEM_SETS.items():
            item_cols = [f"{SCALE_PREFIX}_{i}" for i in idxs]
            missing_cols = [c for c in item_cols if c not in df.columns]
            if missing_cols:
                raise ValueError(
                    f"Missing columns for {SCALE_PREFIX} {set_name}: {missing_cols}"
                )

            data = df[item_cols].apply(pd.to_numeric, errors="coerce")
            n_total = len(data)
            n_complete = len(data.dropna(axis=0, how="any"))
            alpha = cronbach_alpha(data)

            # Item stats
            item_stats = []
            for col in item_cols:
                series = data[col]
                item_stats.append(
                    {
                        "item": col,
                        "n_non_missing": int(series.notna().sum()),
                        "mean": series.mean(),
                        "std": series.std(ddof=1),
                        "min": series.min(),
                        "max": series.max(),
                    }
                )
            item_df = pd.DataFrame(item_stats)
            for c in ["mean", "std", "min", "max"]:
                item_df[c] = pd.to_numeric(item_df[c], errors="coerce").round(3)

            set_tag = set_name.replace("-", "_")
            if WRITE_ITEM_STATS_CSV:
                item_stats_path = os.path.join(
                    OUT_DIR, f"{SCALE_PREFIX}_item_stats_{set_tag}.csv"
                )
                item_df.to_csv(item_stats_path, index=False, encoding="utf-8-sig")

            # Alpha if item deleted
            alpha_if_deleted = []
            for col in item_cols:
                remaining = data[[c for c in item_cols if c != col]]
                alpha_del = cronbach_alpha(remaining)
                alpha_if_deleted.append({"item": col, "alpha_if_deleted": alpha_del})
            alpha_del_df = pd.DataFrame(alpha_if_deleted)
            alpha_del_df["alpha_if_deleted"] = pd.to_numeric(
                alpha_del_df["alpha_if_deleted"], errors="coerce"
            ).round(3)
            if WRITE_ALPHA_IF_DELETED_CSV:
                alpha_del_path = os.path.join(
                    OUT_DIR, f"{SCALE_PREFIX}_alpha_if_deleted_{set_tag}.csv"
                )
                alpha_del_df.to_csv(alpha_del_path, index=False, encoding="utf-8-sig")

            # Write summary section
            f.write(f"Items ({SCALE_PREFIX} {set_name}): {', '.join(item_cols)}\n")
            f.write(f"Total rows: {n_total}\n")
            f.write(f"Complete rows (listwise): {n_complete}\n")
            f.write(f"Cronbach alpha (listwise): {alpha:.3f}\n")
            f.write("Alpha if item deleted:\n")
            for _, r in alpha_del_df.iterrows():
                f.write(f"- {r['item']}: {r['alpha_if_deleted']}\n")
            f.write("\n")

            if WRITE_ITEM_STATS_CSV:
                print(f"Wrote item stats: {item_stats_path}")
            if WRITE_ALPHA_IF_DELETED_CSV:
                print(f"Wrote alpha-if-deleted: {alpha_del_path}")

    print(f"Wrote summary: {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
