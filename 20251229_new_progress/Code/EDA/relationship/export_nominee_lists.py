import pandas as pd
import os

def export_enhanced_nominee_lists():
    # Paths
    w2_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    rel_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
    output_dir = rel_dir 
    
    print("Loading Respondent Data (W2)...")
    df_w2 = pd.read_csv(w2_path, on_bad_lines='skip', engine='python')
    
    # helper for class string cleaning
    def clean_class(val):
        if pd.isna(val):
            return "MISSING"
        s = str(val).strip()
        if s.endswith('.0'):
            return s[:-2]
        return s

    # 1. Build Valid Respondent Set
    df_w2['school_id'] = pd.to_numeric(df_w2['school_id'], errors='coerce').fillna(-1).astype(int)
    df_w2['v13'] = pd.to_numeric(df_w2['v13'], errors='coerce').fillna(-1).astype(int)
    df_w2['class_str'] = df_w2['class'].apply(clean_class)
    
    # Filter valid
    mask = (df_w2['school_id'] != -1) & (df_w2['v13'] != -1) & (df_w2['class_str'] != "MISSING") & (df_w2['class_str'] != "")
    df_valid = df_w2[mask].copy()
    
    # Create set of tuples (School, Class, Seat) -> Respondent Row Index or just True
    valid_respondents = set(zip(
        df_valid['school_id'],
        df_valid['class_str'],
        df_valid['v13']
    ))
    
    print(f"Valid Respondents Loaded: {len(valid_respondents)}")

    # 2. Process Relationships with Flags
    files = {
        "Online_Like": "Online_Like.csv",
        "Online_Dislike": "Online_Dislike.csv",
        "Offline_Like": "Offline_Like.csv",
        "Offline_Dislike": "Offline_Dislike.csv"
    }
    
    # Dictionary to store unique nominees: 
    # Key: (school_id, class_str, seat_no)
    # Value: { 'school_id':..., 'class_name':..., 'seat_no':..., 'in_Online_Like': False, ... }
    nominees_map = {}
    
    print("Processing relationship files...")
    
    for rel_name, fname in files.items():
        fpath = os.path.join(rel_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        print(f"  Reading {fname}...")
        df = pd.read_csv(fpath)
        
        # Clean columns
        df['school_id'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int)
        df['nominated_seat_no'] = pd.to_numeric(df['nominated_seat_no'], errors='coerce').fillna(-1).astype(int)
        df['class_str'] = df['class'].apply(clean_class)
        
        # Filter valid nominees
        clean_mask = (df['school_id'] != -1) & (df['nominated_seat_no'] != -1) & (df['class_str'] != "MISSING")
        df_clean = df[clean_mask]
        
        for _, row in df_clean.iterrows():
            key = (row['school_id'], row['class_str'], row['nominated_seat_no'])
            
            if key not in nominees_map:
                nominees_map[key] = {
                    'school_id': row['school_id'],
                    'class_name': row['class_str'],
                    'seat_no': row['nominated_seat_no'],
                    'in_Online_Like': False,
                    'in_Online_Dislike': False,
                    'in_Offline_Like': False,
                    'in_Offline_Dislike': False
                }
            
            # Mark the flag
            nominees_map[key][f"in_{rel_name}"] = True
            
    # Convert to DataFrame
    df_all_nominees = pd.DataFrame(list(nominees_map.values()))
    
    if df_all_nominees.empty:
        print("No nominees found.")
        return
        
    print(f"Total Unique Nominees Found: {len(df_all_nominees)}")
    
    # 3. Split by Respondent Status
    def check_respondent(row):
        return (row['school_id'], row['class_name'], row['seat_no']) in valid_respondents
    
    df_all_nominees['is_respondent'] = df_all_nominees.apply(check_respondent, axis=1)
    
    df_respondents = df_all_nominees[df_all_nominees['is_respondent']].copy()
    df_non_respondents = df_all_nominees[~df_all_nominees['is_respondent']].copy()
    
    # Drop the helper col
    df_respondents = df_respondents.drop(columns=['is_respondent'])
    df_non_respondents = df_non_respondents.drop(columns=['is_respondent'])
    
    # Sort
    sort_cols = ['school_id', 'class_name', 'seat_no']
    df_respondents = df_respondents.sort_values(sort_cols)
    df_non_respondents = df_non_respondents.sort_values(sort_cols)
    
    # Convert bool columns to int (1/0)
    bool_cols = [c for c in df_respondents.columns if c.startswith('in_')]
    for c in bool_cols:
        df_respondents[c] = df_respondents[c].astype(int)
        df_non_respondents[c] = df_non_respondents[c].astype(int)
    
    # Save
    path_resp = os.path.join(output_dir, "nominees_respondents_detailed.csv")
    path_non = os.path.join(output_dir, "nominees_non_respondents_detailed.csv")
    
    df_respondents.to_csv(path_resp, index=False, encoding='utf-8-sig')
    df_non_respondents.to_csv(path_non, index=False, encoding='utf-8-sig')
    
    print(f"\nSaved Detailed Lists:")
    print(f"   Respondents: {len(df_respondents)} -> {path_resp}")
    print(f"   Non-Respondents: {len(df_non_respondents)} -> {path_non}")

if __name__ == "__main__":
    export_enhanced_nominee_lists()
