import pandas as pd
import os

def list_duplicates():
    # Path to data
    file_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024"
    output_csv = os.path.join(output_dir, "v13_duplicates_full_list.csv")
    
    print(f"Loading data from: {file_path}")
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Helper to clean class names (remove .0)
    def clean_class(val):
        s = str(val).strip()
        if s.endswith('.0'):
            return s[:-2]
        return s

    df['class_clean'] = df['class'].apply(clean_class)
    
    # Ensure school_id is integer-like string
    df['school_id_clean'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int).astype(str)
    
    # Ensure v13 is integer
    df['v13_clean'] = pd.to_numeric(df['v13'], errors='coerce').fillna(-1).astype(int)
    
    # Filter valid seats
    valid_df = df[df['v13_clean'] != -1].copy()
    
    # Find Duplicates based on School, Class, Seat
    # keep=False marks ALL duplicates as True
    dup_mask = valid_df.duplicated(subset=['school_id_clean', 'class_clean', 'v13_clean'], keep=False)
    
    duplicates = valid_df[dup_mask].copy()
    
    # Sort for easier reading: School -> Class -> Seat -> StudentID
    duplicates = duplicates.sort_values(by=['school_id_clean', 'class_clean', 'v13_clean', 'student_id'])
    
    # Select relevant columns for the report
    cols_to_show = ['school_id', 'school_name', 'class_clean', 'v13', 'student_id', 'name']
    # Check if 'name' exists, otherwise omit
    if 'name' not in duplicates.columns:
        cols_to_show.remove('name')
        
    final_report = duplicates[cols_to_show]
    
    print(f"\nTotal Duplicated Entries Found: {len(final_report)}")
    print(f"Number of groups involved: {len(final_report) // 2} (approx)")
    
    # Save to CSV
    final_report.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Full duplicate list saved to: {output_csv}")
    
    # Display first few rows
    print("\n--- Sample of Duplicates ---")
    print(final_report.head(20).to_markdown(index=False))

if __name__ == "__main__":
    list_duplicates()
