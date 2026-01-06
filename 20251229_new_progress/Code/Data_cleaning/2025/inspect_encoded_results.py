
import pandas as pd
import numpy as np
import sys

# Force UTF-8 output for console
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress\Data\2025data\TIGPS_W3_student_convertedviacode_20260103_encoded.csv"
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

print(f"--- Dataset Info ---")
print(f"Shape: {df.shape}")
print(f"Columns: {len(df.columns)}")

# 1. Object Columns (potential unmapped data)
obj_cols = df.select_dtypes(include=['object']).columns
print(f"\n--- Object Columns ({len(obj_cols)}) ---")
for col in obj_cols:
    # Print first 20 chars of col name + example value
    example = df[col].dropna().iloc[0] if not df[col].dropna().empty else "All NaNs"
    print(f"Col: {col[:40]}... | Example: {str(example)[:20]}")

# 2. Numeric Anomalies
num_cols = df.select_dtypes(include=[np.number])
print(f"\n--- Numeric Statistical Checks ---")

# Check for negative values
min_vals = num_cols.min()
neg_cols = min_vals[min_vals < 0]
if not neg_cols.empty:
    print(f"\n[!] Columns with Negative Values ({len(neg_cols)}):")
    for col, val in neg_cols.items():
        print(f"  {col[:40]}... : {val}")
else:
    print("\n[OK] No negative values found.")

# Check for large values (> 100) - likely Weight, Height, or outlier codes
max_vals = num_cols.max()
large_cols = max_vals[max_vals > 100]
if not large_cols.empty:
    print(f"\n[!] Columns with Values > 100 ({len(large_cols)}):")
    for col, val in large_cols.items():
        print(f"  {col[:40]}... : {val}")
else:
    print("\n[OK] No values > 100 found.")

# 3. Check specific recent fixes (v12, v55)
print(f"\n--- Specific Checks ---")
v12_cols = [c for c in df.columns if "12-" in c[:5]] # roughly matching
v55_cols = [c for c in df.columns if "55-" in c[:5]]

print(f"v12-like columns found: {len(v12_cols)}")
for c in v12_cols[:3]:
    print(f"  {c[:30]}... Mean: {df[c].mean():.2f}")

print(f"v55-like columns found: {len(v55_cols)}")
for c in v55_cols[:3]:
    print(f"  {c[:30]}... Mean: {df[c].mean():.2f}")

