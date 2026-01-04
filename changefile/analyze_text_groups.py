
import json
import re

input_json = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\changefile\csv_value_analysis.json'

def check_text_groups():
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Total groups: {len(data)}")
    
    suspicious_text_groups = []
    
    for i, group in enumerate(data):
        options = group['options']
        columns = group['columns']
        
        # This mirrors the logic in generate_mapping_plan.py
        is_id = any("ID" in col for col in columns) or len(options) > 20
        
        if is_id:
            # We want to flag groups that MIGHT be convertable.
            # 1. If it looks like numeric ranges or counts (e.g. containing numbers)
            # 2. If it contains known scale words but was split due to noise
            
            # Check for numeric content
            numeric_options = [opt for opt in options if re.search(r'\d', str(opt))]
            
            # Check for scale keywords
            scale_keywords = ['同意', '符合', '滿意', '快樂', '健康', '沒有', '有']
            has_scale_keyword = any(any(k in str(opt) for k in scale_keywords) for opt in options)
            
            suspicious_text_groups.append({
                "group_index": i + 1,
                "reason": "Marked as Text/ID",
                "columns_count": len(columns),
                "example_column": columns[0],
                "options_count": len(options),
                "example_options": options[:10],
                "has_numbers": len(numeric_options) > 0,
                "has_scale_keywords": has_scale_keyword
            })

    print(f"Found {len(suspicious_text_groups)} groups marked as Text/ID.")
    print("-" * 40)
    for g in suspicious_text_groups:
        print(f"Group {g['group_index']}: {g['example_column']}")
        print(f"  Columns: {g['columns_count']}, Options: {g['options_count']}")
        print(f"  Sample Options: {g['example_options']}")
        print(f"  Has Numbers: {g['has_numbers']}, Has Scale Keywords: {g['has_scale_keywords']}")
        print("-" * 40)

if __name__ == "__main__":
    check_text_groups()
