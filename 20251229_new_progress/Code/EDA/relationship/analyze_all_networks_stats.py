import pandas as pd
import os

def analyze_all_networks_stats():
    # Paths
    base_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
    files = {
        "Offline_Like": os.path.join(base_dir, "Offline_Like.csv"),
        "Offline_Dislike": os.path.join(base_dir, "Offline_Dislike.csv"),
        "Online_Like": os.path.join(base_dir, "Online_Like.csv"),
        "Online_Dislike": os.path.join(base_dir, "Online_Dislike.csv")
    }

    def clean_class(val):
        if pd.isna(val): return "MISSING"
        s = str(val).strip()
        if s.endswith('.0'): return s[:-2]
        return s

    print(f"{'Network Name':<20} | {'Nominators':<12} | {'Nominees (Unique)':<25} | {'Total Edges':<12}")
    print("-" * 80)

    results_list = []

    for name, path in files.items():
        if not os.path.exists(path):
            print(f"{name:<20} | {'FILE NOT FOUND':<12} | {'-':<25} | {'-'}")
            continue
            
        df = pd.read_csv(path)
        
        # 1. Count Nominators (student_id)
        if 'student_id' in df.columns:
            nominators_count = df['student_id'].nunique()
        else:
            nominators_count = 0

        # 2. Count Nominees (Target: School + Class + Seat)
        if all(col in df.columns for col in ['school_id', 'class', 'nominated_seat_no']):
            df['school_id_clean'] = pd.to_numeric(df['school_id'], errors='coerce').fillna(-1).astype(int)
            df['seat_clean'] = pd.to_numeric(df['nominated_seat_no'], errors='coerce').fillna(-1).astype(int)
            df['class_clean'] = df['class'].apply(clean_class)
            
            mask = (df['school_id_clean'] != -1) & (df['seat_clean'] != -1) & (df['class_clean'] != "MISSING")
            valid_targets = df[mask]
            
            unique_targets = valid_targets[['school_id_clean', 'class_clean', 'seat_clean']].drop_duplicates()
            nominees_count = len(unique_targets)
        else:
            nominees_count = 0

        print(f"{name:<20} | {nominators_count:<12} | {nominees_count:<25} | {len(df):<12}")
        
        results_list.append({
            'Network': name,
            'Nominators_Count': nominators_count,
            'Nominees_Count': nominees_count,
            'Total_Edges': len(df)
        })

    print("-" * 80)
    
    # Save to CSV
    if results_list:
        df_out = pd.DataFrame(results_list)
        out_csv = os.path.join(base_dir, "..", "relationship_reallike", "network_statistics_summary.csv")
        # Ensure output dir exists (it is relationship_reallike)
        out_folder = os.path.dirname(out_csv)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
            
        df_out.to_csv(out_csv, index=False)
        print(f"Statistics saved to: {out_csv}")

if __name__ == "__main__":
    analyze_all_networks_stats()
