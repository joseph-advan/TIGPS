import pandas as pd
import os

def extract_relationships():
    # 1. Configuration
    file_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Loading data...")
    df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    
    # 2. Define Groups
    # Key: Output Filename, Value: Column Prefix
    groups = {
        "Online_Like": "v14_1",
        "Online_Dislike": "v14_2",
        "Offline_Like": "v14_3",
        "Offline_Dislike": "v14_4"
    }
    
    # 3. Process Each Group
    for label, prefix in groups.items():
        print(f"Processing {label}...")
        
        results = []
        
        # Iterate through each student
        for idx, row in df.iterrows():
            nominator_id = row['student_id']
            school_id = row['school_id']
            class_id = row['class']
            nominator_seat = row['v13'] # Seat number
            
            # Iterate ranks 1 to 5
            for rank in range(1, 6):
                col_name = f"{prefix}_0{rank}"
                if col_name in df.columns:
                    nominee_seat = row[col_name]
                    
                    # Valid nomination check (not NaN, not 0 if seat 0 is invalid?)
                    # Assuming seat numbers are positive integers.
                    if pd.notna(nominee_seat) and nominee_seat != 0:
                        results.append({
                            "student_id": nominator_id,
                            "school_id": school_id,
                            "class": class_id,
                            "v13": nominator_seat,
                            "nominated_seat_no": int(nominee_seat),
                            "rank": rank
                        })
        
        # Save to CSV
        output_file = os.path.join(output_dir, f"{label}.csv")
        out_df = pd.DataFrame(results)
        
        # Ensure integer types for clean output
        if not out_df.empty:
            # 1. Coerce to numeric (handles strings, mixed types)
            out_df['v13'] = pd.to_numeric(out_df['v13'], errors='coerce')
            out_df['nominated_seat_no'] = pd.to_numeric(out_df['nominated_seat_no'], errors='coerce')
            
            # 2. Check for NaNs before casting
            initial_len = len(out_df)
            out_df = out_df.dropna(subset=['v13', 'nominated_seat_no'])
            dropped_len = initial_len - len(out_df)
            if dropped_len > 0:
                print(f"  Dropped {dropped_len} edges due to missing/invalid seat numbers.")

            # 3. Cast to integer
            out_df['v13'] = out_df['v13'].astype(int)
            out_df['nominated_seat_no'] = out_df['nominated_seat_no'].astype(int)
            
        out_df.to_csv(output_file, index=False)
        print(f"  Saved {len(out_df)} edges to {output_file}")

if __name__ == "__main__":
    extract_relationships()
