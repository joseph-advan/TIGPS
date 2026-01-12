import pandas as pd
import os

def find_correlations_spearman():
    # Path
    w3_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check"
    
    print("Loading W3 data...")
    try:
        df = pd.read_csv(w3_path, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error: {e}")
        return

    # Define Mental Health Items
    mh_cols = [f"54-{i}" for i in range(1, 15)]
    
    # Calculate Target: Total Score
    if not all(col in df.columns for col in mh_cols):
        print("Mental health columns missing.")
        return

    df['MH_Total_Score'] = df[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    
    # Select Numeric Columns
    numeric_df = df.select_dtypes(include=['number'])
    numeric_df = numeric_df.drop(columns=mh_cols, errors='ignore')
    
    print(f"Calculating SPEARMAN correlations for {len(numeric_df.columns)} variables against Mental Health Total Score...")
    
    # Compute correlations using SPEARMAN
    # method='spearman' handles non-normal distributions better by using ranks
    correlations = numeric_df.corrwith(df['MH_Total_Score'], method='spearman')
    
    # Convert to DataFrame
    corr_df = correlations.reset_index()
    corr_df.columns = ['Item', 'Correlation']
    
    # Drop target
    corr_df = corr_df[corr_df['Item'] != 'MH_Total_Score']
    
    # Sort
    corr_df['Abs_Correlation'] = corr_df['Correlation'].abs()
    corr_df = corr_df.sort_values(by='Abs_Correlation', ascending=False)
    
    # Save
    results_path = os.path.join(output_dir, "w3_correlation_screening_spearman.csv")
    corr_df.to_csv(results_path, index=False)
    
    # Display Top 20
    print("\n--- Top 20 Correlated Items (Spearman) ---")
    print(corr_df[['Item', 'Correlation']].head(20).to_markdown(index=False, floatfmt=".4f"))
    
    print(f"\nFull results saved to: {results_path}")

if __name__ == "__main__":
    find_correlations_spearman()
