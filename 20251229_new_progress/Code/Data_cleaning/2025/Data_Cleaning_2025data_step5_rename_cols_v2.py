#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning 2025 Step 5 (v2): Rename Columns with Mapping File
# 
# **Objective:** 
# Rename columns in `TIGPS_W3_student_studentdata_ver1_encoded.csv` using the mapping file `TIGPS_W3_學生問卷題目列表_fromfulltext.csv`.
# Requirements:
# 1. No 'v' prefix.
# 2. Use the '題號' column from the mapping file.
# 3. Handle duplicates (since mapping file maps multiple options to same code sometimes).
# 
# **Input:**
# - Data: `.../Data/2025data/TIGPS_W3_student_studentdata_ver1_encoded.csv`
# - Mapping: `.../Data/2025data/TIGPS_W3_學生問卷題目列表_fromfulltext.csv`
# 
# **Output:**
# - `.../Data/2025data/TIGPS_W3_student_studentdata_ver2_cleaned_cols.csv`

# In[ ]:


import pandas as pd
import os
import warnings

base_dir = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress"
data_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_studentdata_ver1_encoded.csv")
map_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_學生問卷題目列表_fromfulltext.csv")
output_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_studentdata_ver2_cleaned_cols.csv")

print(f"Loading Data: {data_path}")
df = pd.read_csv(data_path)
print(f"Data Columns: {df.shape[1]}")

print(f"Loading Mapping: {map_path}")
# Read mapping with utf-8 or cp950 (usually big5/cp950 for spreadsheets in tw)
# Try utf-8 first (since previous view worked)
try:
    df_map = pd.read_csv(map_path, encoding='utf-8')
except:
    df_map = pd.read_csv(map_path, encoding='cp950')
    
print(f"Mapping Rows: {len(df_map)}")
print(df_map.head())


# ## Build Mapping Dictionary
# Goal: Map `Data Column Name` -> `New Code`.
# We match by string.

# In[ ]:


# Normalize strings to ensure match (strip whitespace)
df_map['完整題目名稱'] = df_map['完整題目名稱'].astype(str).str.strip()
df_map['題號'] = df_map['題號'].astype(str).str.strip()

# Create lookup dict
text_to_code = dict(zip(df_map['完整題目名稱'], df_map['題號']))

# Generate new column names
new_cols_list = []
col_counts = {}

for col in df.columns:
    col_clean = col.strip()
    
    # 1. Lookup
    if col_clean in text_to_code:
        code = text_to_code[col_clean]
        
        # Handle 'No ID' or special values
        if code == 'No ID':
            if 'TIGPS ID' in col_clean:
                final_name = 'TIGPS_ID'
            else:
                # If it's something like '其他' without a code, keep original or verify?
                # Current logic: keep key words if code is missing, or keep original name
                # Mapping file row 57: '其他' -> 'No ID'
                # User said: 參照... 去改
                # Maybe keep original name if No ID?
                final_name = col_clean
        else:
            final_name = code
    else:
        # Not found in mapping: Keep original, warn
        # Or try fuzzy match? For now, strict match.
        final_name = col_clean
        # print(f"[Warning] No mapping found for: {col_clean[:20]}...")

    # 2. Dedup
    # Many columns map to "8-1" or "39"
    # Logic: append index if seen before
    if final_name in col_counts:
        col_counts[final_name] += 1
        # If the duplicate is because of sub-options (like 10-1-(1)), 
        # usually the *order* in the file matches the order in mapping.
        # Appending _1, _2 is safe.
        if final_name not in ['TIGPS_ID', 'Unnamed: 0']:
            # Only append suffix to codes
            unique_name = f"{final_name}_{col_counts[final_name]}"
        else:
            unique_name = f"{final_name}.{col_counts[final_name]}"
    else:
        col_counts[final_name] = 0
        unique_name = final_name
        
    new_cols_list.append(unique_name)

print("Renaming Preview:")
print(list(zip(df.columns[:10], new_cols_list[:10])))

# Check for massive duplication issues
from collections import Counter
dupes = [item for item, count in Counter(new_cols_list).items() if count > 1]
if dupes:
    print(f"WARNING: Final list still has duplicates: {dupes}")
else:
    print("Final column list is unique.")


# In[ ]:


# Apply and Save
df.columns = new_cols_list
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"Saved to: {output_path}")

