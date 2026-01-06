#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning 2025 Step 5: Rename Columns
# 
# **Objective:** 
# Simplify column names in `TIGPS_W3_student_studentdata_ver1_encoded.csv` by keeping only the question code/symbol (removing the question text).
# 
# **Input:**
# - `.../Data/2025data/TIGPS_W3_student_studentdata_ver1_encoded.csv`
# 
# **Output:**
# - `.../Data/2025data/TIGPS_W3_student_studentdata_ver1_cleaned_cols.csv`

# In[ ]:


import pandas as pd
import os
import re

base_dir = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress"
input_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_studentdata_ver1_encoded.csv")
output_path = os.path.join(base_dir, r"Data\2025data\TIGPS_W3_student_studentdata_ver1_cleaned_cols.csv")

print(f"Reading: {input_path}")
df = pd.read_csv(input_path)
print(f"Original Columns (first 5): {df.columns[:5].tolist()}")


# ## Define Cleaning Logic
# Refined Logic:
# 1. Remove Chinese characters.
# 2. Remove non-structure characters (keep alphanumeric, dot, dash, parentheses, underscore).
# 3. Add 'v' prefix if results starts with digit.

# In[ ]:


def clean_col_name(col_name):
    if col_name.strip() == "TIGPS ID":
        return "TIGPS_ID"
    if "Unnamed" in col_name:
        return col_name
        
    # Strategy: Remove Chinese and non-structure characters
    # Keep digits, dots, dashes, parentheses, underscores
    
    # 1. Start by replacing Chinese range with empty string
    cleaned = re.sub(r'[\u4e00-\u9fff]+', '', col_name)
    
    # 2. Keep only alphanumeric and structural chars
    # Also remove ? [ ] { } which might be part of the text
    cleaned = re.sub(r'[^a-zA-Z0-9\-\.\(\)_]', '', cleaned)
    
    # 3. Clean leading/trailing junk
    cleaned = cleaned.strip('.').strip('-').strip('_')
    
    # If the result is distinct enough, us it.
    # Add 'v' if starts with digit to match variable naming conventions
    if cleaned and cleaned[0].isdigit():
        cleaned = f"v{cleaned}"
        
    return cleaned

# Test on a few columns
new_cols = {}
for c in df.columns:
    new_cols[c] = clean_col_name(c)

print("Mapping Preview (Sample):")
sample_keys = [k for k in df.columns if '(' in k or '-' in k][:10]
for k in sample_keys:
    print(f"'{k[:40]}...' -> '{new_cols[k]}'")
    
# Check for duplicates again
new_col_list = list(new_cols.values())
if len(new_col_list) != len(set(new_col_list)):
    print("\nWARNING: Duplicate column names still exist!")
    from collections import Counter
    dupes = [item for item, count in Counter(new_col_list).items() if count > 1]
    print(f"Duplicates sample: {dupes[:5]}")
    
    # Fallback: append index to duplicates
    seen = {}
    final_cols = {}
    for old_col, new_col in new_cols.items():
        if new_col in seen:
            seen[new_col] += 1
            final_col = f"{new_col}_{seen[new_col]}"
        else:
            seen[new_col] = 0
            final_col = new_col
        final_cols[old_col] = final_col
    new_cols = final_cols
    print("Applied suffix to resolve duplicates.")
else:
    print("No duplicate column names.")


# In[ ]:


# Apply Renaming
df_renamed = df.rename(columns=new_cols)

# Save
df_renamed.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nSaved renamed file to:\n{output_path}")

