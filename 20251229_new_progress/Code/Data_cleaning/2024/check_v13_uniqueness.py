import pandas as pd
import os

def check_v13_uniqueness():
    # Path configuration
    file_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    
    print(f"Loading data from: {file_path}")
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Clean Class Column (remove .0)
    def clean_class(val):
        s = str(val).strip()
        if s.endswith('.0'):
            return s[:-2]
        return s

    df['class_clean'] = df['class'].apply(clean_class)
    
    # Fill NaN in v13 and school_id for accurate grouping
    df['v13'] = pd.to_numeric(df['v13'], errors='coerce').fillna(-1).astype(int)
    df['school_id'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int)

    # Filter out rows where v13 is missing (-1) as they are irrelevant for seat mapping
    valid_df = df[df['v13'] != -1].copy()
    print(f"Total rows: {len(df)}")
    print(f"Rows with valid v13: {len(valid_df)}")

    # Check 1: Uniqueness of (Class + v13) - Ignoring School
    print("\n--- Check 1: Uniqueness of (Class + v13) ---")
    duplicates_class_v13 = valid_df[valid_df.duplicated(subset=['class_clean', 'v13'], keep=False)]
    if not duplicates_class_v13.empty:
        print(f"Found {len(duplicates_class_v13)} entries with duplicate (Class + v13).")
        print("Sample duplicates:")
        print(duplicates_class_v13[['school_id', 'class_clean', 'v13', 'student_id', 'name']].sort_values(['class_clean', 'v13']).head(10).to_markdown(index=False))
    else:
        print("No duplicates found for (Class + v13).")

    # Check 2: Uniqueness of (School + Class + v13) - The stricter check
    print("\n--- Check 2: Uniqueness of (School + Class + v13) ---")
    duplicates_school_class_v13 = valid_df[valid_df.duplicated(subset=['school_id', 'class_clean', 'v13'], keep=False)]
    
    if not duplicates_school_class_v13.empty:
        print(f"Found {len(duplicates_school_class_v13)} entries with duplicate (School + Class + v13).")
        print("Sample duplicates:")
        print(duplicates_school_class_v13[['school_id', 'class_clean', 'v13', 'student_id', 'name']].sort_values(['school_id', 'class_clean', 'v13']).head(20).to_markdown(index=False))
        
        # Save duplicates to CSV for review
        output_csv = "duplicates_v13_report.csv"
        duplicates_school_class_v13.to_csv(output_csv, index=False)
        print(f"\nFull list of duplicates saved to: {os.path.abspath(output_csv)}")
    else:
        print("No duplicates found for (School + Class + v13). This combination is UNIQUE.")

    return

if __name__ == "__main__":
    check_v13_uniqueness()
