import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def analyze_transitions():
    # Paths
    w2_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    w3_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check"
    
    print("Loading data...")
    df_w2 = pd.read_csv(w2_path, on_bad_lines='skip', engine='python')
    df_w3 = pd.read_csv(w3_path, on_bad_lines='skip', engine='python')

    # Calculate Scores
    w2_cols = [f"v55_{i}" for i in range(1, 15)]
    w3_cols = [f"54-{i}" for i in range(1, 15)]
    
    df_w2['Score_W2'] = df_w2[w2_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    df_w3['Score_W3'] = df_w3[w3_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)

    # Categories
    # Green (Low): 14-19
    # Yellow (Med): 20-29
    # Red (High): 30+
    def categorize(score):
        if pd.isna(score): return None
        if score <= 19: return 'Green (Low)'
        if score <= 29: return 'Yellow (Med)'
        return 'Red (High)'

    df_w2['Risk_W2'] = df_w2['Score_W2'].apply(categorize)
    df_w3['Risk_W3'] = df_w3['Score_W3'].apply(categorize)

    # Merge
    # Normalize IDs
    df_w2['merge_id'] = df_w2['student_id'].astype(str).str.strip()
    id_col_w3 = 'student_id' if 'student_id' in df_w3.columns else 'TIGPS_ID'
    df_w3['merge_id'] = df_w3[id_col_w3].astype(str).str.strip()
    
    merged = pd.merge(df_w2[['merge_id', 'Risk_W2']], df_w3[['merge_id', 'Risk_W3']], on='merge_id', how='inner').dropna()
    print(f"Analyzed {len(merged)} students.")

    # Transition Matrix (Counts)
    order = ['Green (Low)', 'Yellow (Med)', 'Red (High)']
    trans_counts = pd.crosstab(merged['Risk_W2'], merged['Risk_W3']).reindex(index=order, columns=order).fillna(0).astype(int)
    
    # Transition Matrix (Probabilities - Row Normalized)
    trans_probs = trans_counts.div(trans_counts.sum(axis=1), axis=0) * 100

    print("\n--- Transition Matrix (Counts) ---")
    print(trans_counts.to_markdown())
    
    print("\n--- Transition Matrix (Percentages %) ---")
    print(trans_probs.to_markdown(floatfmt=".1f"))

    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(trans_probs, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Transition Probability (%)'})
    plt.title('Mental Health Risk Transition (W2 -> W3)', fontsize=16)
    plt.xlabel('W3 Status (2025)', fontsize=12)
    plt.ylabel('W2 Status (2024)', fontsize=12)
    
    plot_path = os.path.join(output_dir, "risk_transition_heatmap.png")
    plt.savefig(plot_path)
    plt.close()
    
    # Save CSVs
    trans_counts.to_csv(os.path.join(output_dir, "transition_counts.csv"))
    trans_probs.to_csv(os.path.join(output_dir, "transition_probs.csv"))

    # Generate Report Text
    report_path = r"C:\Users\user\.gemini\antigravity\brain\fa800e3d-4dba-491f-b7e3-a3e2c18d9ae4\transition_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Mental Health Risk Transition Analysis\n\n")
        f.write("## Risk Categories\n")
        f.write("- 🟢 **Green (Low Risk)**: Score 14 - 19\n")
        f.write("- 🟡 **Yellow (Medium Risk)**: Score 20 - 29\n")
        f.write("- 🔴 **Red (High Risk)**: Score 30+\n\n")
        
        f.write("## Transition Matrix (Counts)\n")
        f.write("Shows the number of students moving between categories.\n\n")
        f.write(trans_counts.to_markdown() + "\n\n")
        
        f.write("## Transition Matrix (Percentages)\n")
        f.write("Shows the probability (%) of moving to a W3 category given a W2 category.\n\n")
        f.write(trans_probs.to_markdown(floatfmt=".1f") + "\n\n")
        
        f.write("## Visualization\n")
        f.write("![Transition Heatmap](risk_transition_heatmap.png)\n\n")
        
        f.write("## Key Interpretations\n")
        
        # Determine stability
        green_retention = trans_probs.loc['Green (Low)', 'Green (Low)']
        red_retention = trans_probs.loc['Red (High)', 'Red (High)']
        
        f.write(f"### 1. Stability of Low Risk Group\n")
        f.write(f"- **{green_retention:.1f}%** of students who were Low Risk (Green) in W2 **remained** Low Risk in W3.\n")
        f.write(f"- This indicates a high level of stability for healthy students.\n\n")
        
        f.write(f"### 2. Persistence of High Risk Group\n")
        f.write(f"- **{red_retention:.1f}%** of students who were High Risk (Red) in W2 **remained** High Risk in W3.\n")
        red_improved = trans_probs.loc['Red (High)', ['Green (Low)', 'Yellow (Med)']].sum()
        f.write(f"- However, **{red_improved:.1f}%** of high-risk students showed improvement (moved to Yellow or Green).\n\n")

        f.write(f"### 3. Deterioration\n")
        green_worsened = trans_probs.loc['Green (Low)', ['Yellow (Med)', 'Red (High)']].sum()
        f.write(f"- **{green_worsened:.1f}%** of initially Low Risk students worsened to Medium or High Risk.\n")

    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    analyze_transitions()
