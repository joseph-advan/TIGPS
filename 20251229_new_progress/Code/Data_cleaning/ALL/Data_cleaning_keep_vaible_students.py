#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning: Identify Common Students (W2 & W3)
# 
# **Objective:** 
# Identify students present in both the 2024 (W2) and 2025 (W3) datasets and extract their basic information from the 2024 data.
# 
# **Inputs:**
# 1. **2024 Data (W2):** `.../Data/2024data/TIGPS_W2_studentdata_ver3_encoded.csv`
# 2. **2025 Data (W3):** `.../Data/2025data/TIGPS_W3_student_studentdata_ver1_encoded.csv`
# 
# **Output:**
# - A DataFrame/CSV of common students with W2 basic info.
# 

# In[ ]:


import pandas as pd
import os

# --- Paths ---
base_dir = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress"
w2_path = os.path.join(base_dir, r"Data\2024data\TIGPS_W2_studentdata_ver3_encoded.csv")
w3_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_studentdata_ver1_encoded.csv")

print(f"Loading W2: {w2_path}")
print(f"Loading W3: {w3_path}")

# Load Data
try:
    if not os.path.exists(w2_path):
        print(f"[Error] W2 file not found: {w2_path}")
    if not os.path.exists(w3_path):
        print(f"[Error] W3 file not found: {w3_path}")
        
    df_w2 = pd.read_csv(w2_path, low_memory=False)
    df_w3 = pd.read_csv(w3_path, low_memory=False)
except Exception as e:
    print(f"Error loading data: {e}")
    raise e

print(f"W2 Shape: {df_w2.shape}")
print(f"W3 Shape: {df_w3.shape}")


# ## Find Common IDs

# In[ ]:


# Normalize IDs to string and strip whitespace
# W2 key: 'student_id', W3 key: 'TIGPS ID'

if 'student_id' not in df_w2.columns:
    print("Column 'student_id' missing in W2.")
    print(df_w2.columns)
if 'TIGPS ID' not in df_w3.columns:
    # Fallback check mainly for W3 if name differs
    print("Column 'TIGPS ID' missing in W3. Checking alternatives...")
    print(df_w3.columns[:5])
    # Attempt to find likely ID column
    possible_ids = [c for c in df_w3.columns if 'ID' in c.upper()]
    print(f"Possible ID columns in W3: {possible_ids}")

df_w2['student_id'] = df_w2['student_id'].astype(str).str.strip()
df_w3['TIGPS ID'] = df_w3['TIGPS ID'].astype(str).str.strip()

ids_w2 = set(df_w2['student_id'])
ids_w3 = set(df_w3['TIGPS ID'])

# Intersection
common_ids = ids_w2.intersection(ids_w3)
print(f"Unique IDs in W2: {len(ids_w2)}")
print(f"Unique IDs in W3: {len(ids_w3)}")
print(f"Common IDs found: {len(common_ids)}")


# ## Extract Student Info

# In[ ]:


# Columns to keep from W2
cols_to_keep = ['student_id', 'qb_code', 'q_name', 'school_id', 'school_name', 'class']

# Filter W2 for common IDs
common_students_df = df_w2[df_w2['student_id'].isin(common_ids)].copy()

# Keep only relevant columns if they exist
final_cols = [c for c in cols_to_keep if c in common_students_df.columns]
common_students_df = common_students_df[final_cols]

# Sort
if 'student_id' in common_students_df.columns:
    common_students_df = common_students_df.sort_values('student_id')

print("Top 5 rows of common students data:")
print(common_students_df.head())

# Save result
output_file = os.path.join(base_dir, r"Data\common_students_W2_W3.csv")
common_students_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved list of {len(common_students_df)} common students to:\n{output_file}")

