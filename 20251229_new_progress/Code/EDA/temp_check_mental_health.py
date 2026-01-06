import pandas as pd
import os

def check_columns(df, cols, dataset_name):
    print(f"--- Checking {dataset_name} ---")
    print(f"Total rows: {len(df)}")
    
    missing_cols = [c for c in cols if c not in df.columns]
    if missing_cols:
        print(f"WARNING: The following columns were not found in the dataframe: {missing_cols}")
        cols = [c for c in cols if c in df.columns]
    
    if not cols:
        print("No columns to check.")
        return

    # Missing values
    missing_counts = df[cols].isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    
    print("\nMissing Values:")
    for col in cols:
        count = missing_counts[col]
        pct = missing_pct[col]
        print(f"{col}: {count} ({pct:.2f}%)")
    
    print("\nValue Counts & Anomalies Check (showing min/max/unique count):")
    for col in cols:
        valid_data = df[col].dropna()
        if len(valid_data) > 0:
            unique_vals = sorted(valid_data.unique())
            print(f"\nColumn: {col}")
            print(f"Unique values count: {len(unique_vals)}")
            print(f"Min: {min(unique_vals)}, Max: {max(unique_vals)}")
            print(f"Unique Values (first 20): {unique_vals[:20]}")
            # Check for values that might be outliers (e.g. 99, -1, or outside 1-5 scale if applicable)
            # Assuming Likert scale, usually 1-4 or 1-5.
            value_counts = valid_data.value_counts().sort_index()
            print("Value counts:")
            print(value_counts)
        else:
            print(f"\nColumn: {col} - ALL EMPTY")

# W2
w2_path = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver3_encoded.csv"
if os.path.exists(w2_path):
    print(f"Loading W2: {w2_path}")
    try:
        df_w2 = pd.read_csv(w2_path, low_memory=False)
        w2_cols = [f'v55_{i}' for i in range(1, 15)]
        check_columns(df_w2, w2_cols, "Wave 2 (W2)")
    except Exception as e:
        print(f"Error reading W2 file: {e}")
else:
    print(f"File not found: {w2_path}")

print("\n" + "="*30 + "\n")

# W3
w3_path = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress\Data\2025data\TIGPS_W3_student_studentdata_ver2_cleaned_cols.csv"
if os.path.exists(w3_path):
    print(f"Loading W3: {w3_path}")
    try:
        df_w3 = pd.read_csv(w3_path, low_memory=False)
        # Note: W3 columns identified as '54-1' to '54-14'
        w3_cols = [f'54-{i}' for i in range(1, 15)]
        check_columns(df_w3, w3_cols, "Wave 3 (W3)")
    except Exception as e:
        print(f"Error reading W3 file: {e}")
else:
    print(f"File not found: {w3_path}")
