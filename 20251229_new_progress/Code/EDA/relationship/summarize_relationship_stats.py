import pandas as pd
import os

def summarize_stats():
    # Paths
    w2_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    rel_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
    output_dir = rel_dir 
    
    print("Loading Respondent Data (W2)...")
    df_w2 = pd.read_csv(w2_path, on_bad_lines='skip', engine='python')
    
    # --- Clean ID Logic (String Class) ---
    def clean_class(val):
        if pd.isna(val):
            return "MISSING"
        s = str(val).strip()
        if s.endswith('.0'):
            return s[:-2]
        return s

    df_w2['school_id'] = pd.to_numeric(df_w2['school_id'], errors='coerce').fillna(-1).astype(int)
    df_w2['v13'] = pd.to_numeric(df_w2['v13'], errors='coerce').fillna(-1).astype(int)
    df_w2['class_str'] = df_w2['class'].apply(clean_class)
    
    # Valid Respondents Set
    mask = (df_w2['school_id'] != -1) & (df_w2['v13'] != -1) & (df_w2['class_str'] != "MISSING") & (df_w2['class_str'] != "")
    df_valid = df_w2[mask].copy()
    
    valid_respondents = set(zip(
        df_valid['school_id'],
        df_valid['class_str'],
        df_valid['v13']
    ))
    
    print(f"Valid Respondents: {len(valid_respondents)}")

    # --- Process Files ---
    files = {
        "Online_Like": "Online_Like.csv",
        "Online_Dislike": "Online_Dislike.csv",
        "Offline_Like": "Offline_Like.csv",
        "Offline_Dislike": "Offline_Dislike.csv"
    }
    
    stats_data = []

    print("\nCalculating Statistics...")
    for label, fname in files.items():
        fpath = os.path.join(rel_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        df = pd.read_csv(fpath)
        
        # Clean Columns for Matching
        df['school_id'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int)
        df['nominated_seat_no'] = pd.to_numeric(df['nominated_seat_no'], errors='coerce').fillna(-1).astype(int)
        df['class_str'] = df['class'].apply(clean_class)
        
        # 1. Total Nominations (Edges)
        # We consider a nomination valid if we can identify the target (School, Class, Seat).
        # Although the file was already cleaned for missing seats, let's just count total rows effectively.
        total_edges = len(df)
        
        # 2. Unique Nominees
        # Valid targets only
        clean_mask = (df['school_id'] != -1) & (df['nominated_seat_no'] != -1) & (df['class_str'] != "MISSING")
        df_clean = df[clean_mask].copy()
        
        unique_nominees = df_clean[['school_id', 'class_str', 'nominated_seat_no']].drop_duplicates()
        total_unique = len(unique_nominees)
        
        # 3. Respondent Checks
        unique_nominees['is_respondent'] = unique_nominees.apply(
            lambda x: (x['school_id'], x['class_str'], x['nominated_seat_no']) in valid_respondents, 
            axis=1
        )
        
        respondent_count = unique_nominees['is_respondent'].sum()
        respondent_rate = (respondent_count / total_unique * 100) if total_unique > 0 else 0
        
        # 4. "Average Nominations Given" (Optional Interpretation of "大家列的人數")
        # How many nominations were made on average?
        # Num Edges / Num Nominators (Unique student_ids in the rel file)
        # Note: 'student_id' in rel file is the nominator.
        unique_nominators = df['student_id'].nunique()
        res_per_nominator = (total_edges / unique_nominators) if unique_nominators > 0 else 0
        
        stats_data.append({
            "Relationship": label,
            "Total_Nominations (Edges)": total_edges,
            "Unique_Nominees (People)": total_unique,
            "Unique_Nominators": unique_nominators,
            "Avg_Nominations_Per_Person": round(res_per_nominator, 2),
            "Nominees_Who_Are_Respondents": respondent_count,
            "Respondent_Rate (%)": round(respondent_rate, 1)
        })

    # Save
    out_df = pd.DataFrame(stats_data)
    output_path = os.path.join(output_dir, "relationship_comprehensive_summary.csv")
    out_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print("\n--- Summary Table ---")
    print(out_df.to_markdown(index=False))
    print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    summarize_stats()
