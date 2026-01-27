import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.impute import SimpleImputer
import os

def run_baseline():
    DATA_PATH = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Data\2024data\TIGPS_W2_studentdata_ver5_cleaned_mental_common_only.csv"
    
    TOP_20_FEATURES = [
        'v51', 'v59_5', 'v52_3', 'v57_4', 'v52_2', 
        'v57_3', 'v50', 'v57_2', 'v52', 'v57_1', 
        'v52_1', 'v57_5', 'v24_2', 'v8_08', 'v28_6', 
        'v39_2', 'v5_5', 'v8_05', 'v24_6', 'v35_2'
    ]
    
    print("Loading data...")
    try:
        df = pd.read_csv(DATA_PATH, on_bad_lines='skip', engine='python')
    except Exception as e:
        print(f"Error: {e}")
        return

    mh_cols = [f"v55_{i}" for i in range(1, 15)]
    df['target'] = df[mh_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1, min_count=1)
    df_clean = df.dropna(subset=['target']).copy()
    
    X = df_clean[TOP_20_FEATURES].apply(pd.to_numeric, errors='coerce')
    y = df_clean['target']
    
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    r2_rf = r2_score(y_test, y_pred_rf)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    
    print(f"\n--- Random Forest Baseline ---")
    print(f"MSE: {mse_rf:.4f}")
    print(f"MAE: {mae_rf:.4f}")
    print(f"R2: {r2_rf:.4f}")

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    r2_lr = r2_score(y_test, y_pred_lr)
    
    print(f"\n--- Linear Regression Baseline ---")
    print(f"R2: {r2_lr:.4f}")

if __name__ == "__main__":
    run_baseline()
