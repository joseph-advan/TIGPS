
import pandas as pd
import re
import csv
import os

input_csv = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\changefile\TIGPS_W3_student_convertedviacode_20260103_fulltext.csv'
output_csv = r'C:\Users\user\Desktop\TIGPS_PLAN_DATA\TIGPS\changefile\question_metadata.csv'

def extract_questions():
    try:
        # Read only the header
        df = pd.read_csv(input_csv, encoding='utf-8-sig', nrows=0)
        columns = df.columns.tolist()
        
        extracted_data = []
        
        for col in columns:
            # Logic to extract "Question Number" (題號)
            # Patterns to look for:
            # 1. "1. ..." -> "1"
            # 2. "5. ... - 5-1. ..." -> "5-1" (take the most specific one)
            # 3. "10-1. ..." -> "10-1"
            
            # Strategy: Look for the *last* occurrence of a pattern like "X." or "X-Y."
            # Many columns are formatted like: "Main Question - Sub Question"
            # We want the Sub Question ID if it exists, otherwise Main Question ID.
            
            # Check for pattern like " 5-1." or "^5-1."
            # Regex: find all digits-plus-dots-dashes at start of segments
            
            # Simple heuristic:
            # Split by " - " just in case it's a sub-question
            parts = col.split(" - ")
            target_part = parts[-1] # The last part usually has the specific question info
            
            # Regex to find starting number: e.g. "5-1." or "1." or "(1)"
            match = re.search(r'^(\d+-\d+|\d+|(?:\(\d+\)))[.]?', target_part.strip())
            
            question_id = ""
            if match:
                question_id = match.group(1)
            else:
                # Fallback: check if the whole column string starts with a number
                match_start = re.search(r'^(\d+-\d+|\d+)[.]?', col)
                if match_start:
                    question_id = match_start.group(1)
            
            # If still nothing, it might be a special column like "TIGPS ID"
            valid_id = question_id if question_id else "No ID"
            
            extracted_data.append([valid_id, col])
            
        # Write to CSV
        with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['題號', '完整題目名稱'])
            writer.writerows(extracted_data)
            
        print(f"Successfully extracted {len(extracted_data)} questions to {output_csv}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_questions()
