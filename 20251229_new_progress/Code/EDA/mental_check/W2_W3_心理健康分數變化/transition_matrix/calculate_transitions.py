import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2


def analyze_transitions():
    # Paths
    w2_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\other\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    w3_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\other\TIGPS_W3_studentdata_ver5_cleaned_cols_removed_missing_common_only(cleaned_q_21).csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check\change_between_years\transition_matrix"
    os.makedirs(output_dir, exist_ok=True)

    print("Loading data...")
    df_w2 = pd.read_csv(w2_path, on_bad_lines="skip", engine="python")
    df_w3 = pd.read_csv(w3_path, on_bad_lines="skip", engine="python")

    # Calculate Scores
    w2_cols = [f"v55_{i}" for i in range(1, 15)]
    w3_cols = [f"54-{i}" for i in range(1, 15)]

    df_w2["Score_W2"] = df_w2[w2_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
    df_w3["Score_W3"] = df_w3[w3_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)

    # Categories: 14-19, 20-29, 30+
    def categorize(score):
        if pd.isna(score):
            return None
        if 14 <= score <= 19:
            return "14-19"
        if 20 <= score <= 29:
            return "20-29"
        if score >= 30:
            return "30+"
        return None

    df_w2["Risk_W2"] = df_w2["Score_W2"].apply(categorize)
    df_w3["Risk_W3"] = df_w3["Score_W3"].apply(categorize)

    # Merge (paired students)
    df_w2["merge_id"] = df_w2["student_id"].astype(str).str.strip()
    id_col_w3 = "student_id" if "student_id" in df_w3.columns else "TIGPS_ID"
    df_w3["merge_id"] = df_w3[id_col_w3].astype(str).str.strip()

    merged = pd.merge(
        df_w2[["merge_id", "Risk_W2"]],
        df_w3[["merge_id", "Risk_W3"]],
        on="merge_id",
        how="inner",
    ).dropna()
    print(f"Analyzed {len(merged)} students (valid scores in both years).")

    order = ["14-19", "20-29", "30+"]

    # Counts per year (same students)
    counts_w2 = merged["Risk_W2"].value_counts().reindex(order).fillna(0).astype(int)
    counts_w3 = merged["Risk_W3"].value_counts().reindex(order).fillna(0).astype(int)
    total = len(merged)

    risk_counts = pd.DataFrame(
        {
            "Category": order,
            "W2_count": counts_w2.values,
            "W2_pct": counts_w2.values / total * 100,
            "W3_count": counts_w3.values,
            "W3_pct": counts_w3.values / total * 100,
        }
    )

    # Transition Matrix (Counts)
    trans_counts = (
        pd.crosstab(merged["Risk_W2"], merged["Risk_W3"])
        .reindex(index=order, columns=order)
        .fillna(0)
        .astype(int)
    )

    # Transition Matrix (Probabilities - Row Normalized)
    trans_probs = trans_counts.div(trans_counts.sum(axis=1), axis=0) * 100

    print("\n--- Risk Group Counts (Same Students) ---")
    print(risk_counts.to_markdown(index=False, floatfmt=".1f"))

    print("\n--- Transition Matrix (Counts) ---")
    print(trans_counts.to_markdown())

    print("\n--- Transition Matrix (Percentages %) ---")
    print(trans_probs.to_markdown(floatfmt=".1f"))

    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        trans_probs,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        cbar_kws={"label": "Transition Probability (%)"},
    )
    plt.title("Mental Health Risk Transition (W2 -> W3)", fontsize=16)
    plt.xlabel("W3 Status (2025)", fontsize=12)
    plt.ylabel("W2 Status (2024)", fontsize=12)

    plot_path = os.path.join(output_dir, "risk_transition_heatmap.png")
    plt.savefig(plot_path)
    plt.close()

    # Stuart-Maxwell test for marginal homogeneity (paired categorical)
    def stuart_maxwell_test(table):
        t = table.values.astype(float)
        k = t.shape[0]
        if k < 2:
            return np.nan, 0, np.nan
        r = t.sum(axis=1)
        c = t.sum(axis=0)
        d = (r - c)[: k - 1]
        v = np.zeros((k - 1, k - 1))
        for i in range(k - 1):
            for j in range(k - 1):
                if i == j:
                    v[i, i] = r[i] + c[i] - 2 * t[i, i]
                else:
                    v[i, j] = -(t[i, j] + t[j, i])
        stat = float(d.T @ np.linalg.pinv(v) @ d)
        df = k - 1
        p = 1 - chi2.cdf(stat, df)
        return stat, df, p

    sm_stat, sm_df, sm_p = stuart_maxwell_test(trans_counts)
    test_df = pd.DataFrame(
        {
            "test": ["Stuart-Maxwell (marginal homogeneity)"],
            "statistic": [sm_stat],
            "df": [sm_df],
            "p_value": [sm_p],
            "n": [total],
        }
    )

    print("\n--- Stuart-Maxwell Test ---")
    print(test_df.to_markdown(index=False, floatfmt=".4f"))

    # Save outputs
    risk_counts.to_csv(os.path.join(output_dir, "risk_group_counts.csv"), index=False, encoding="utf-8-sig")
    trans_counts.to_csv(os.path.join(output_dir, "transition_counts.csv"))
    trans_probs.to_csv(os.path.join(output_dir, "transition_probs.csv"))
    test_df.to_csv(os.path.join(output_dir, "risk_group_test.csv"), index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    analyze_transitions()
