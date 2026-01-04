import json
import re

input_json = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\2025_rawdata\changefile\csv_value_analysis.json'
output_md = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\2025_rawdata\changefile\mapping_plan_draft.md'

def suggest_mapping(options):
    # Define semantic orders for known sets (Smallest/Negative -> Largest/Positive)
    semantic_orders = [
        # Frequency (Simple)
        ['從未', '偶爾', '有時', '經常'],
        
        # Conformity 3-point
        ['很不符合', '不太符合', '很符合'],
        
        # Agreement 4-point
        ['很不同意', '不太同意', '還算同意', '很同意'],
        
        # Frequency (Days/Weeks)
        ['完全沒有或少於一天', '最近1週一到兩天', '最近1週三到四天', '最近1週五到七天', '最近兩週幾乎天天'],
        
        # Ability
        ['完全做不到', '能做到一些', '大部份能做到', '完全能做到'],
        
        # Change
        ['有改變，比以前少', '沒有改變，原本就這樣', '有改變，比以前多'],
        
        # Frequency (5-point including 'Never happened')
        ['從未', '沒發生過', '偶爾', '有時', '經常'],
        
        # Frequency (Counts) - Putting "No such person" at 1 (as 0-like category) or end?
        # User asked start from 1. Let's order by frequency magnitude.
        # '無此人' (N/A) often handled separately, but we'll put it first as 1.
        ['無此人', '幾乎沒有', '每周1、2次', '每周3、4次', '每天1次', '每天好幾次'],
        
        # Agreement 5-point
        ['非常不同意', '不太同意', '同意', '很同意', '非常同意'],
        
        # Frequency (Teaching)
        ['從未', '一學期1-2次', '一個月1-2次', '一周1-2次', '幾乎每天教'],
        
        # Time Duration (Hours) - Manual sort required for ranges
        ['沒有', '0.5小時以內', '0.5-1小時', '1-1.5小時', '1.5-2小時', '2-2.5小時', '2.5-3小時', '3-3.5小時', '3.5-4小時', '4-4.5小時', '4.5-5小時', '5小時以上'],
        
        # Proportion
        ['從來沒有', '有時候', '少於一半的時間', '一半以上的時間', '大部分的時間'],
        
        # Experience (Yes/No-ish)
        ['不曾', '曾經有'],
        
        # Usage Conformity
        ['沒使用過', '很不符合', '不太符合', '很符合'],
        
        # Gender
        ['男', '女'],
        
        # Binary
        ['沒有', '有'],
        
        # Yes/No/Unknown
        ['不知道', '沒有', '有'],
        
        # AI Knowledge
        ['不知道', '知道'],
    ]

    sorted_opts = None
    option_set = set(options)
    
    # Check if we have a predefined semantic order for this set
    for order in semantic_orders:
        if set(order) == option_set:
            sorted_opts = order
            break
            
    # Fallback: maintain sorted alphabetical if no semantic match
    if not sorted_opts:
        # Try to detect if it's numeric-ish (e.g. "10", "20")
        try:
            sorted_opts = sorted(options, key=lambda x: float(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else x)
        except:
            sorted_opts = sorted(options)

    mapping = {}
    for i, opt in enumerate(sorted_opts):
        mapping[opt] = i + 1
        
    return mapping

def generate_md():
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    lines = []
    lines.append("# Data Conversion Mapping Plan\n")
    lines.append("Please review the proposed mappings below. Each section represents a group of questions that share the same answer options.\n")
    lines.append("For each unique set of options, please confirm or assign the numeric code.\n")
    
    for i, group in enumerate(data):
        options = group['options']
        columns = group['columns']
        
        # Identify if this is likely an ID or open text field (too many unique values or specific headers)
        is_id = any("ID" in col for col in columns) or len(options) > 20
        
        lines.append(f"## Group {i+1}")
        lines.append(f"**Columns ({len(columns)}):**")
        for col in columns[:3]:
            lines.append(f"- {col}")
        if len(columns) > 3:
            lines.append(f"- ... and {len(columns)-3} more")
            
        lines.append("\n**Options & Proposed Mapping:**")
        
        if is_id:
            lines.append("> [!NOTE]")
            lines.append("> These appear to be IDs or open-ended text. **Action: Keep as text?**")
        else:
            mapping = suggest_mapping(options)
            lines.append("| Text Value | Numeric Code |")
            lines.append("| :--- | :--- |")
            for opt, code in mapping.items():
                lines.append(f"| {opt} | {code} |")
                
        lines.append("\n---\n")
        
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print(f"Generated {output_md}")

if __name__ == "__main__":
    generate_md()
