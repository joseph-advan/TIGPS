import pandas as pd
import json

input_csv = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\2025_rawdata\changefile\TIGPS_W3_student_convertedviacode_20260103_fulltext.csv'
output_json = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\2025_rawdata\changefile\csv_value_analysis.json'

def analyze_csv():
    try:
        # Read CSV, assume utf-8-sig
        df = pd.read_csv(input_csv, encoding='utf-8-sig')
        
        # Store unique values for each column
        col_values = {}
        for col in df.columns:
            # Get unique values, drop NA, convert to sorted list of strings
            uniques = sorted([str(x) for x in df[col].dropna().unique()])
            col_values[col] = tuple(uniques) # Use tuple to be hashable
            
        # Group columns by their unique values
        value_groups = {}
        for col, values in col_values.items():
            if values not in value_groups:
                value_groups[values] = []
            value_groups[values].append(col)
            
        # Prepare output structure
        output_data = []
        for values, cols in value_groups.items():
            output_data.append({
                "options": list(values),
                "columns": cols
            })
            
        # Sort by number of columns (descending) to see most common scales first
        output_data.sort(key=lambda x: len(x['columns']), reverse=True)
        
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Analysis complete. Found {len(output_data)} distinct value groups.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_csv()
