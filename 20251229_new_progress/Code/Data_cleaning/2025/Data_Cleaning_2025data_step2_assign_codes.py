#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning 2025 Step 1: Assign Numeric Codes
# 
# **Objective:** 
# Read the draft categorical options list (`2025_categorical_options_draft.csv`) and automatically fill in the `Proposed_Numeric_Code` based on predefined logic rules.
# 
# **Output:** `2025_categorical_mapping_filled.csv`

# In[ ]:


import pandas as pd
import numpy as np

input_path = "2025_categorical_options_draft.csv"
output_path = "2025_categorical_mapping_filled.csv"

try:
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows.")
except FileNotFoundError:
    print(f"File not found: {input_path}")


# ## Define Mapping Logic

# In[ ]:


def get_code(value, col_name=None):
    val_str = str(value).strip()
    
    # --- 1. Standard Binary & Yes/No ---
    if val_str in ['沒有', '不曾', '不會', '沒發生過', '否']:
        return 0
    if val_str in ['有', '曾經有', '會', '是']:
        return 1
    
    # --- 2. Gender ---
    if val_str == '男': return 1
    if val_str == '女': return 2
    if val_str in ['男性', '女性']: return 1 if val_str=='男性' else 2
    
    # --- 3. Frequency (4-point) ---
    if val_str == '從未': return 1
    if val_str == '偶爾': return 2
    if val_str == '有時': return 3
    if val_str == '經常': return 4
    
    # --- 4. Agreement (Standard 4-point & 5-point mixed) ---
    # 5-point: Very Disagree(1) -> Disagree(2) -> Neutral(3)? -> Agree(4) -> Very Agree(5)
    # 4-point: Very Disagree(1) -> Disagree(2) -> Agree(3) -> Very Agree(4)
    mapping_agree = {
        '非常不同意': 1, '不太同意': 2, '同意': 3, '很同意': 4, '非常同意': 5,
        '很不同意': 1, '還算同意': 3, # '不太同意' overlaps = 2, '很同意' overlaps = 4
        '很不符合': 1, '不太符合': 2, '還算符合': 3, '很符合': 4,
        '很不滿意': 1, '不太滿意': 2, '還算滿意': 3, '很滿意': 4,
        '很不快樂': 1, '不太快樂': 2, '還算快樂': 3, '很快樂': 4,
        '很不健康': 1, '不太健康': 2, '還算健康': 3, '很健康': 4,
        '非常不好': 1, '不太好': 2, '還算': 3, '非常好': 4, # Sleep quality likely
        '不適用': 0, '沒使用過': 0
    }
    if val_str in mapping_agree:
        return mapping_agree[val_str]
        
    # --- 5. Communication Frequency (6-point) ---
    comm_map = {
        '無此人': 0,
        '幾乎沒有': 1,
        '每周1、2次': 2,
        '每周3、4次': 3,
        '每天1次': 4,
        '每天好幾次': 5
    }
    if val_str in comm_map:
        return comm_map[val_str]
        
    # --- 6. Drink Frequency (7-point) ---
    # Heuristic: Check digits in string
    drink_map = {
        '都沒有喝': 0,
        '一天不到1次': 1, '每天1次': 2, '每天2次': 3, '每天3次': 4, '每天4次': 5, '每天5次（含）以上': 6,
        # Bottle counts
        '1-7瓶/罐': 1, '8-14瓶/罐': 2, '15-21瓶/罐': 3, '22-28瓶/罐': 4, '29-35瓶/罐': 5, '36瓶/罐以上': 6,
        '1-7瓶': 1, '8-14瓶': 2, '15-21瓶': 3, '22-28瓶': 4, '29-35瓶': 5, '36瓶以上': 6,
        # Cup counts
        '1-2杯': 1, '3-4杯': 2, '5-6杯': 3, '7-8杯': 4, '9-10': 5, '11杯以上': 6
    }
    if val_str in drink_map:
        return drink_map[val_str]
        
    # --- 7. Grades (5-point) ---
    grade_map = {
        '全班三十名以後': 1,
        '全班二十一至三十名': 2,
        '全班十一至二十名': 3,
        '全班六至十名': 4,
        '全班五名以內': 5
    }
    if val_str in grade_map:
        return grade_map[val_str]
        
    # --- 8. Education Levels (7-point) ---
    edu_map = {
        '國中畢業': 1,
        '高中（職）畢業': 2,
        '專科畢業（五專、二專）': 3, '專科': 3,
        '大學或技術學院畢業（四技、二技）': 4,
        '碩士畢業': 5,
        '博士畢業': 6,
        '公立高中': 2, '私立高中': 2, '高職': 2, '軍校': 2, # Rough mapping for school types if needed, or keep 0?
        '我不打算繼續升學': 0, '不知道': 0, '其他': 0, '其他，請說明': 0
    }
    if val_str in edu_map:
        return edu_map[val_str]

    # --- 9. AI Frequency (5-point) ---
    ai_freq_map = {
        '完全沒有或少於一天': 1, '從未': 1,
        '最近1週一到兩天': 2, '每週 1-2 次': 2, '一個月1-2次': 2, 
        '最近1週三到四天': 3, '每週 3-4 次': 3, '一周1-2次': 3, 
        '最近1週五到七天': 4, '每週 5-6 次': 4, '一學期1-2次': 1.5, 
        '最近兩週幾乎天天': 5, '幾乎每天教': 5, '每天': 5
    }
    if val_str in ai_freq_map:
        return ai_freq_map[val_str]
    
    # --- 10. Capability (4-point AI) ---
    cap_map = {
        '完全做不到': 1,
        '能做到一些': 2, 
        '大部份能做到': 3,
        '完全能做到': 4
    }
    if val_str in cap_map:
        return cap_map[val_str]
    
    # --- 11. Change Amount (v12) ---
    change_map = {
        '有改變，比以前少': 1,
        '沒有改變，原本就這樣': 2,
        '有改變，比以前多': 3
    }
    if val_str in change_map:
        return change_map[val_str]

    # --- 12. Well-being Frequency (v55 - 5-point) ---
    # Logic: Never(1) -> Some(2) -> Less than half(3) -> More than half(4) -> Most(5)
    # Note: WHO-5 often 0-5, but we stick to 1-based consistency or match text logic
    wb_map = {
        '從來沒有': 1,
        '有時候': 2,
        '少於一半的時間': 3,
        '一半以上的時間': 4,
        '大部分的時間': 5
    }
    if val_str in wb_map:
        return wb_map[val_str]

    # Default: None
    return None


# ## Apply Mapping

# In[ ]:


# Copy df to avoid setting on copy warning
df_filled = df.copy()

# Apply logic
df_filled['Proposed_Numeric_Code'] = df_filled.apply(lambda row: get_code(row['Value']), axis=1)

# Check status
filled_count = df_filled['Proposed_Numeric_Code'].notna().sum()
total_count = len(df_filled)
print(f"Filled {filled_count} out of {total_count} rows ({filled_count/total_count:.1%})")

# Show samples of Unfilled
unfilled = df_filled[df_filled['Proposed_Numeric_Code'].isna()]
if not unfilled.empty:
    print("\nSample Unfilled Values:")
    print(unfilled['Value'].unique()[:20])


# ## Save Result

# In[ ]:


# Determine Type for Code column (Int with NaN support -> Int64, or Float)
# We'll keep as float/object to allow blank in CSV or explicit NaN
df_filled.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"Saved to {output_path}")

