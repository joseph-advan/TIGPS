import os
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    w2_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver9.csv"
    w3_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\W3_studentdata_ver9.csv"
    out_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check\W2_W3_心理健康分數變化\transition_matrix_new"
    os.makedirs(out_dir, exist_ok=True)

    tag = "ver9rerun_20260326"

    # Columns used previously for depression total score
    w2_score_cols = [f"v55_{i}" for i in range(1, 15)]
    w3_score_cols = [f"54-{i}" for i in range(1, 15)]

    df_w2 = pd.read_csv(w2_path, low_memory=False)
    df_w3 = pd.read_csv(w3_path, low_memory=False)

    missing_w2 = [c for c in w2_score_cols if c not in df_w2.columns]
    missing_w3 = [c for c in w3_score_cols if c not in df_w3.columns]
    if missing_w2:
        raise KeyError(f"W2 missing columns: {missing_w2}")
    if missing_w3:
        raise KeyError(f"W3 missing columns: {missing_w3}")

    if "student_id" not in df_w2.columns or "student_id" not in df_w3.columns:
        raise KeyError("Both W2 and W3 must contain student_id for pairing.")

    df_w2["depression_total_w2"] = df_w2[w2_score_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
    df_w3["depression_total_w3"] = df_w3[w3_score_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)

    w2_median = float(df_w2["depression_total_w2"].median(skipna=True))
    w3_median = float(df_w3["depression_total_w3"].median(skipna=True))

    def split_group(series: pd.Series, cutoff: float):
        out = pd.Series(index=series.index, dtype="object")
        out[series >= cutoff] = "High (>= median)"
        out[series < cutoff] = "Low (< median)"
        return out

    df_w2["dep_group_w2"] = split_group(df_w2["depression_total_w2"], w2_median)
    df_w3["dep_group_w3"] = split_group(df_w3["depression_total_w3"], w3_median)

    w2_keep = df_w2[["student_id", "depression_total_w2", "dep_group_w2"]].copy()
    w3_keep = df_w3[["student_id", "depression_total_w3", "dep_group_w3"]].copy()
    w2_keep["merge_id"] = w2_keep["student_id"].astype(str).str.strip()
    w3_keep["merge_id"] = w3_keep["student_id"].astype(str).str.strip()

    paired = pd.merge(
        w2_keep[["merge_id", "depression_total_w2", "dep_group_w2"]],
        w3_keep[["merge_id", "depression_total_w3", "dep_group_w3"]],
        on="merge_id",
        how="inner",
    )

    paired_valid = paired.dropna(subset=["dep_group_w2", "dep_group_w3"]).copy()

    group_order = ["Low (< median)", "High (>= median)"]

    trans_counts = (
        pd.crosstab(paired_valid["dep_group_w2"], paired_valid["dep_group_w3"])
        .reindex(index=group_order, columns=group_order)
        .fillna(0)
        .astype(int)
    )

    trans_row_pct = trans_counts.div(trans_counts.sum(axis=1), axis=0) * 100
    trans_total_pct = trans_counts / trans_counts.values.sum() * 100

    paired_n = len(paired_valid)
    counts_w2 = paired_valid["dep_group_w2"].value_counts().reindex(group_order).fillna(0).astype(int)
    counts_w3 = paired_valid["dep_group_w3"].value_counts().reindex(group_order).fillna(0).astype(int)

    group_counts = pd.DataFrame(
        {
            "group": group_order,
            "w2_count": counts_w2.values,
            "w2_pct_of_paired": (counts_w2.values / paired_n * 100),
            "w3_count": counts_w3.values,
            "w3_pct_of_paired": (counts_w3.values / paired_n * 100),
        }
    )

    transition_long = (
        trans_counts.stack()
        .rename("count")
        .reset_index()
        .rename(columns={"dep_group_w2": "w2_group", "dep_group_w3": "w3_group"})
    )
    transition_long["pct_of_w2_row"] = transition_long.apply(
        lambda r: (r["count"] / trans_counts.loc[r["w2_group"]].sum() * 100)
        if trans_counts.loc[r["w2_group"]].sum() > 0
        else 0.0,
        axis=1,
    )
    transition_long["pct_of_total_paired"] = transition_long["count"] / paired_n * 100

    summary_df = pd.DataFrame(
        {
            "metric": [
                "w2_median_cutoff",
                "w3_median_cutoff",
                "paired_students_with_valid_scores",
                "w2_total_rows",
                "w3_total_rows",
            ],
            "value": [
                w2_median,
                w3_median,
                paired_n,
                len(df_w2),
                len(df_w3),
            ],
        }
    )

    # Save CSV outputs
    summary_path = os.path.join(out_dir, f"01_summary_median_cutoff_and_n_{tag}.csv")
    group_counts_path = os.path.join(out_dir, f"02_group_counts_w2_w3_paired_{tag}.csv")
    trans_counts_path = os.path.join(out_dir, f"03_transition_counts_w2_to_w3_{tag}.csv")
    trans_row_pct_path = os.path.join(out_dir, f"04_transition_row_pct_w2_to_w3_{tag}.csv")
    trans_total_pct_path = os.path.join(out_dir, f"05_transition_total_pct_w2_to_w3_{tag}.csv")
    trans_long_path = os.path.join(out_dir, f"06_transition_long_with_pct_{tag}.csv")

    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")
    group_counts.to_csv(group_counts_path, index=False, encoding="utf-8-sig")
    trans_counts.to_csv(trans_counts_path, encoding="utf-8-sig")
    trans_row_pct.to_csv(trans_row_pct_path, encoding="utf-8-sig")
    trans_total_pct.to_csv(trans_total_pct_path, encoding="utf-8-sig")
    transition_long.to_csv(trans_long_path, index=False, encoding="utf-8-sig")

    # Heatmap
    plt.figure(figsize=(7, 6))
    sns.heatmap(trans_counts, annot=True, fmt="d", cmap="Blues", cbar_kws={"label": "Count"})
    plt.title("Depression Group Transition (W2 -> W3)\nMedian split by each year")
    plt.xlabel("W3 Group")
    plt.ylabel("W2 Group")
    plt.tight_layout()
    heatmap_path = os.path.join(out_dir, f"07_transition_counts_heatmap_{tag}.png")
    plt.savefig(heatmap_path, dpi=200)
    plt.close()

    # Readme
    readme_path = os.path.join(out_dir, f"00_README_transition_matrix_{tag}.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("Transition matrix (median split) outputs\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"W2 median cutoff: {w2_median}\n")
        f.write(f"W3 median cutoff: {w3_median}\n")
        f.write(f"Paired valid students: {paired_n}\n")
        f.write("\nFiles:\n")
        f.write("01_summary_median_cutoff_and_n_*.csv: cutoffs and sample sizes\n")
        f.write("02_group_counts_w2_w3_paired_*.csv: high/low counts in each year (paired sample)\n")
        f.write("03_transition_counts_w2_to_w3_*.csv: transition count matrix\n")
        f.write("04_transition_row_pct_w2_to_w3_*.csv: row-normalized transition percentages\n")
        f.write("05_transition_total_pct_w2_to_w3_*.csv: percentage of all paired students\n")
        f.write("06_transition_long_with_pct_*.csv: long-format transition table\n")
        f.write("07_transition_counts_heatmap_*.png: transition count heatmap\n")

    print("Done.")
    print(f"W2 median: {w2_median}")
    print(f"W3 median: {w3_median}")
    print(f"Paired valid N: {paired_n}")
    print("\nTransition counts:\n", trans_counts)


if __name__ == "__main__":
    main()
