import pandas as pd
import os

def map_questions_w2():
    # Paths
    corr_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check\w2_correlation_screening_spearman.csv"
    questions_path = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_學生問卷題目列表_clean_no_topic.csv"
    output_dir = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\EDA\mental_check"
    
    print("Loading data...")
    try:
        df_corr = pd.read_csv(corr_path)
    except Exception as e:
        print(f"Error loading correlations: {e}")
        return

    try:
        df_questions = pd.read_csv(questions_path, encoding='utf-8-sig') # Try standard first
    except:
        try:
            df_questions = pd.read_csv(questions_path, encoding='cp950')
        except Exception as e:
            print(f"Error loading questions: {e}")
            return
            
    print(f"Loaded Questions Columns: {list(df_questions.columns)}")
    
    # Direct mapping based on file inspection (W2)
    # Based on output: ['題號', '純題目']
    code_col = '題號'
    text_col = '純題目'
    
    if code_col not in df_questions.columns:
        print(f"Error: '{code_col}' not found. Columns: {list(df_questions.columns)}")
        return

    print(f"Using Code Column: '{code_col}' and Text Column: '{text_col}'")
    
    # Debug: Check for target codes
    sample_targets = ['50-1', '50', 'v54', '54', '59-5', '59'] # Adjusting targets based on potential W2 W3 diff
    # W2 uses v55 items mental health? Wait, user said v55_1~14. Let's see what correlated.
    # We should check for whatever top correlates appeared.
    # Previous script just printed them to console, I assume I'll see them now.
    
    # Prepare mapping dataframe
    df_q_clean = df_questions[[code_col, text_col]].copy()
    df_q_clean.columns = ['Item', 'Question_Text']
    df_q_clean['Item'] = df_q_clean['Item'].astype(str).str.strip()
    df_corr['Item'] = df_corr['Item'].astype(str).str.strip()
    
    # Merge
    merged = pd.merge(df_corr, df_q_clean, on='Item', how='left')
    
    # Top 20
    print("\n--- Top 20 Correlated Items (W2) ---")
    print(merged[['Item', 'Correlation', 'Question_Text']].head(20).to_markdown(index=False, floatfmt=".4f"))
    
    # Save
    output_path = os.path.join(output_dir, "w2_correlation_with_text.csv")
    merged.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved W2 mapping to {output_path}")

if __name__ == "__main__":
    map_questions_w2()
