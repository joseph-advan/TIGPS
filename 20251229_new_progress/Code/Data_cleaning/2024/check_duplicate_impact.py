import pandas as pd
import os

def check_duplicate_impact():
    # Paths
    # 1. The list of duplicates we just generated
    duplicates_file = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\Data_cleaning\2024\v13_duplicates_full_list.csv"
    
    # 2. Network files directory
    network_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\relationship"
    network_files = {
        "Offline_Like": "Offline_Like.csv",
        "Offline_Dislike": "Offline_Dislike.csv",
        "Online_Like": "Online_Like.csv",
        "Online_Dislike": "Online_Dislike.csv"
    }

    print("--- Loading Duplicate Targets ---")
    try:
        dup_df = pd.read_csv(duplicates_file)
    except Exception as e:
        print(f"Error loading duplicates file: {e}")
        return

    # Helper to clean class names (remove .0)
    def clean_class(val):
        s = str(val).strip()
        if s.endswith('.0'):
            return s[:-2]
        return s

    # Prepare the set of ambiguous targets: (school_id, class, seat)
    # dup_df columns: school_id, school_name, class_clean, v13, ...
    # We use 'class_clean' because the duplicate script already cleaned it.
    
    ambiguous_targets = set()
    for _, row in dup_df.iterrows():
        sid = int(row['school_id'])
        cls = str(row['class_clean'])
        seat = int(row['v13'])
        ambiguous_targets.add((sid, cls, seat))
        
    print(f"Loaded {len(ambiguous_targets)} unique ambiguous target keys (School, Class, Seat).")
    # Note: len(dup_df) is ~200+, but unique keys will be ~100+ because each key has >=2 students.

    print("\n--- Checking Impact on Networks ---")
    total_affected_edges = 0
    
    results = []

    for net_name, filename in network_files.items():
        file_path = os.path.join(network_dir, filename)
        if not os.path.exists(file_path):
            print(f"Warning: {filename} not found.")
            continue
            
        try:
            net_df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
            
        # Network df needs cleaning to match keys
        # Columns: ... school_id, class, nominated_seat_no ...
        
        # 1. Clean School ID
        net_df['school_clean'] = pd.to_numeric(net_df['school_id'], errors='coerce').fillna(-1).astype(int)
        
        # 2. Clean Class
        net_df['class_clean'] = net_df['class'].apply(clean_class)
        
        # 3. Clean Seat (Nominated Seat)
        net_df['seat_clean'] = pd.to_numeric(net_df['nominated_seat_no'], errors='coerce').fillna(-1).astype(int)
        
        # Determine if each edge points to an ambiguous target
        def is_ambiguous(row):
            key = (row['school_clean'], row['class_clean'], row['seat_clean'])
            return key in ambiguous_targets

        net_df['is_ambiguous'] = net_df.apply(is_ambiguous, axis=1)
        
        affected_count = net_df['is_ambiguous'].sum()
        total_edges = len(net_df)
        percentage = (affected_count / total_edges * 100) if total_edges > 0 else 0
        
        print(f"Network: {net_name:<15} | Affected Edges: {affected_count:<5} / {total_edges:<7} ({percentage:.2f}%)")
        
        results.append({
            "Network": net_name,
            "Affected_Edges": affected_count,
            "Total_Edges": total_edges,
            "Percentage": percentage
        })
        
        total_affected_edges += affected_count

    print("-" * 50)
    print(f"TOTAL Affected Edges across all 4 networks: {total_affected_edges}")
    
    # Optional: could save specific affected edges to inspect, but count is the main request.

if __name__ == "__main__":
    check_duplicate_impact()
