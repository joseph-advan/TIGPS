#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning 2025 Step 4: Exploration of Encoded Data
# 
# **Objective:** 
# Inspect the newly created `TIGPS_W3_student_convertedviacode_20260103_encoded.csv` to identify:
# 1. Remaining object columns (non-numeric)
# 2. Missing value patterns
# 3. Anomalies or outliers in numeric columns
# 

# In[ ]:


import pandas as pd
import numpy as np
import os

file_path = r"C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\20251229_new_progress\Data\2025data\TIGPS_W3_student_convertedviacode_20260103_encoded.csv"
print(f"Reading file: {file_path}")
df = pd.read_csv(file_path)
print(f"Shape: {df.shape}")


# ## 1. Data Type Overview

# In[ ]:


print(df.dtypes.value_counts())

# List remaining object columns
obj_cols = df.select_dtypes(include=['object']).columns
print(f"\nRemaining Object Columns ({len(obj_cols)}):")
for col in obj_cols:
    # Show a sample value to understand why it's still object
    sample = df[col].dropna().unique()[:3]
    print(f" - {col}: {sample}")


# ## 2. Missing Value Analysis

# In[ ]:


missing = df.isnull().mean()
print("Columns with > 50% missing:")
high_missing = missing[missing > 0.5]
for col, val in high_missing.sort_values(ascending=False).items():
    print(f"{col}: {val:.2%}")

print(f"\nTotal columns with >50% missing: {len(high_missing)}")


# ## 3. Numeric Anomalies

# In[ ]:


num_df = df.select_dtypes(include=[np.number])
desc = num_df.describe().T

# Check for negative values (placeholders?)
neg_values = desc[desc['min'] < 0]
if not neg_values.empty:
    print("Found columns with negative values:")
    print(neg_values[['min', 'max', 'mean']])
else:
    print("No negative values found in numeric columns.")

# Check for unusually large values (potential outliers)
# Assuming most survey scales are 0-7 or 1-100.
# Identifiers might be large, weight/height might be > 100.
large_values = desc[desc['max'] > 100]
print("\nFound columns with values > 100:")
print(large_values[['min', 'max', 'mean']])

