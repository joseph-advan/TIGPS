import pandas as pd
import os

def map_questions():
    # Paths
    corr_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check\w3_correlation_screening_spearman.csv"
    questions_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2025data\TIGPS_W3_學生問卷題目列表_fromfulltext.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check"
    
    print("Loading data...")
    # Load Correlations
    try:
        df_corr = pd.read_csv(corr_path)
    except Exception as e:
        print(f"Error loading correlations: {e}")
        return

    # Load Questions
    # Try different encodings for Chinese characters
    try:
        df_questions = pd.read_csv(questions_path, encoding='utf-8-sig')
    except:
        try:
            df_questions = pd.read_csv(questions_path, encoding='cp950')
        except Exception as e:
            print(f"Error loading questions: {e}")
            return
            
    print(f"Loaded Questions Columns: {list(df_questions.columns)}")
    
    # Identify Question Code and Text Columns
    # Assuming standard format or trying to detect
    # Based on previous context, columns might be 'internal_name' or similar for ID, and 'full_text' for text
    # Let's try to standardize
    
    # Clean correlation item names if needed (e.g. ensure string)
    df_corr['Item'] = df_corr['Item'].astype(str).str.strip()
    
    
    # Direct mapping based on file inspection
    code_col = '題號'
    text_col = '完整題目名稱'
    
    if code_col not in df_questions.columns:
        print(f"Error: '{code_col}' not found. Columns: {list(df_questions.columns)}")
        return

    print(f"Using Code Column: '{code_col}' and Text Column: '{text_col}'")
    
    # Debug: Check for target codes
    sample_targets = ['50-1', '50', '52-2', '52']
    print(f"Checking for existence of {sample_targets} in '{code_col}':")
    for t in sample_targets:
        exists = df_questions[code_col].astype(str).str.contains(t, regex=False).any()
        print(f"  '{t}': {exists}")
    
    # Prepare mapping dataframe
    df_q_clean = df_questions[[code_col, text_col]].copy()
    df_q_clean.columns = ['Item', 'Question_Text']
    df_q_clean['Item'] = df_q_clean['Item'].astype(str).str.strip()
    
    # Merge
    merged = pd.merge(df_corr, df_q_clean, on='Item', how='left')
    
    # Top 20
    top_20 = merged.head(20)
    
    print("\n--- Top 20 Correlated Items with Meaning ---")
    print(top_20[['Item', 'Correlation', 'Question_Text']].to_markdown(index=False, floatfmt=".4f"))
    
    # Save
    output_path = os.path.join(output_dir, "w3_correlation_with_text.csv")
    merged.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved mapping results to {output_path}")

if __name__ == "__main__":
    map_questions()
