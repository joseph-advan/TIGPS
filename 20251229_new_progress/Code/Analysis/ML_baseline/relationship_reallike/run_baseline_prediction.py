import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os

def run_prediction():
    W2_DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2024data/TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    W3_DATA_PATH = r"C:/Users/user/Desktop/TIGPS_Plan_data/20251229_new_progress/Data/2025data/TIGPS_W3_studentdata_ver4_cleaned_cols_removed_missing_common_only.csv"

    print("Loading data...")
    try:
        w2_df = pd.read_csv(W2_DATA_PATH, on_bad_lines='skip', engine='python')
        w3_df = pd.read_csv(W3_DATA_PATH, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(e)
        return

    # W2 Features
    MH_ITEMS_W2 = [f"v55_{i}" for i in range(1, 15)]
    w2_df['w2_mh_score'] = w2_df[MH_ITEMS_W2].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    
    TOP_20_FEATURES = [
        'v51', 'v59_5', 'v52_3', 'v57_4', 'v52_2', 
        'v57_3', 'v50', 'v57_2', 'v52', 'v57_1', 
        'v52_1', 'v57_5', 'v24_2', 'v8_08', 'v28_6', 
        'v39_2', 'v5_5', 'v8_05', 'v24_6', 'v35_2'
    ]
    X_cols = TOP_20_FEATURES + ['w2_mh_score']
    X_raw = w2_df[['student_id'] + X_cols].copy()

    # W3 Target
    mh_cols_w3 = [f"54-{i}" for i in range(1, 15)]
    w3_df['target_w3'] = w3_df[mh_cols_w3].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    y_raw = w3_df[['student_id', 'target_w3']].dropna()

    # Merge
    merged = pd.merge(X_raw, y_raw, on='student_id', how='inner')
    print(f"Merged samples: {len(merged)}")

    X = merged[X_cols].apply(pd.to_numeric, errors='coerce')
    y = merged['target_w3']

    # Preprocessing
    imputer = SimpleImputer(strategy='median')
    X_imp = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_imp), columns=X.columns)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

    # Train
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    print(f"\n--- Linear Regression (W2 -> W3) ---")
    print(f"R2: {r2_score(y_test, y_pred_lr):.4f}")

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    print(f"\n--- Random Forest (W2 -> W3) ---")
    print(f"R2: {r2_score(y_test, y_pred_rf):.4f}")

if __name__ == "__main__":
    run_prediction()
