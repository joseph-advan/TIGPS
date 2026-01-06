#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning 2025 Step 3: Apply Categorical Mapping
# 
# **Objective:** 
# Use the verified mapping table (`2025_categorical_mapping_filled.csv`) to convert the raw full-text 2025 data (`TIGPS_W3_student_convertedviacode_20260103_fulltext.csv`) into a numerically encoded dataset.
# 
# **Inputs:**
# 1. Raw Data: `.../Data/2025data/TIGPS_W3_student_convertedviacode_20260103_fulltext.csv`
# 2. Mapping Table: `.../Code/Data_cleaning/2025/2025_categorical_mapping_filled.csv`
# 
# **Output:**
# - Encoded Data: `.../Data/2025data/TIGPS_W3_student_convertedviacode_20260103_encoded.csv`

# In[ ]:


import pandas as pd
import numpy as np
import os

# --- Paths ---
# Adjust relative paths based on notebook location: Code/Data_cleaning/2025/
base_dir = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress"
raw_data_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_convertedviacode_20260103_fulltext.csv")
mapping_path = os.path.join(base_dir, r"Code\Data_cleaning\2025\2025_categorical_mapping_filled.csv")
output_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_convertedviacode_20260103_encoded.csv")

# Load Data
print("Loading data...")
try:
    df = pd.read_csv(raw_data_path)
    mapping_df = pd.read_csv(mapping_path)
    print(f"Raw data shape: {df.shape}")
    print(f"Mapping table rows: {len(mapping_df)}")
except FileNotFoundError as e:
    print(f"Error: {e}")


# ## Build Mapping Rules

# In[ ]:


conversion_dict = {}
skipped_cols = []

# Group mapping table by Column Name
for col, group in mapping_df.groupby('Column Name'):
    # Check for skip marker
    if any(group['Value'] == '(High Cardinality - Skipped)'):
        skipped_cols.append(col)
        continue
        
    # Create map for this column: Value -> Proposed_Numeric_Code
    # Ensure code is treated as float first to handle NaNs, then maybe int later
    col_map = group.set_index('Value')['Proposed_Numeric_Code'].to_dict()
    conversion_dict[col] = col_map

print(f"Defined mappings for {len(conversion_dict)} columns.")
print(f"Skipped {len(skipped_cols)} high-cardinality columns (e.g., {skipped_cols[:3]}).")


# ## Apply Conversion

# In[ ]:


df_encoded = df.copy()
converted_log = []

for col, col_map in conversion_dict.items():
    if col in df_encoded.columns:
        # Use map to convert. Unmapped values become NaN.
        # This effectively handles both conversion and cleaning of unexpected values.
        original_values = df_encoded[col].count()
        
        df_encoded[col] = df_encoded[col].map(col_map)
        
        new_values = df_encoded[col].count()
        converted_log.append({
            'Column': col,
            'Original_Count': original_values,
            'Converted_Count': new_values,
            'Missing_Created': original_values - new_values
        })

print("Conversion complete.")


# ## Verify & Save

# In[ ]:


# Show summary of potential data loss (unmapped values)
log_df = pd.DataFrame(converted_log)
lossy_cols = log_df[log_df['Missing_Created'] > 0]
if not lossy_cols.empty:
    print(f"WARNING: {len(lossy_cols)} columns had values that were not in the mapping (turned to NaN).")
    print(lossy_cols.sort_values('Missing_Created', ascending=False).head())
else:
    print("All values mapped successfully (no new missing values).")

# Save
df_encoded.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nSaved encoded file to:\n{output_path}")

