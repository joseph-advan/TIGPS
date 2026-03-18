import os
import sys
from typing import List

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = r"C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress"

W2_PATH = os.path.join(
    BASE_DIR,
    r"Data\2024data\TIGPS_W2_studentdata_ver6_cleaned_mental_common_only(standerdized).csv",
)
W3_PATH = os.path.join(
    BASE_DIR,
    r"Data\2025data\TIGPS_W3_studentdata_ver6_cleaned_cols_removed_missing_common_only(cleaned_q_21)(standerdized).csv",
)

QUESTION_LIST_PATH = os.path.join(
    BASE_DIR, r"Code\EDA\tying_to_catigoricalize_q\merged_question_list_w2_w3.csv"
)

CROSSYEAR_PRIMARY = os.path.join(
    BASE_DIR,
    r"Code\EDA\mental_check\Correlation_with_mental_qs_and_other_qs\02_crossyear_spearman_W2_to_W3_MH.csv",
)
CROSSYEAR_FALLBACK = os.path.join(
    BASE_DIR,
    r"Code\EDA\mental_check\Correlation_with_mental_qs_and_other_qs\02_sorted_by_rho_crossyear_W2_to_W3_MH.csv",
)

OUT_DIR = os.path.join(
    BASE_DIR, r"Code\Analysis\ML_baseline\Mental分組測試\單題目"
)

OUT_FEATURES = os.path.join(OUT_DIR, "selected_items.csv")
OUT_FILTERED_GROUPS = os.path.join(OUT_DIR, "selected_groups_filtered.csv")
OUT_DATA_SHAPE = os.path.join(OUT_DIR, "data_summary.txt")
OUT_RIDGE_COEF = os.path.join(OUT_DIR, "ridge_coefficients.csv")
OUT_LASSO_COEF = os.path.join(OUT_DIR, "lasso_coefficients.csv")
OUT_METRICS = os.path.join(OUT_DIR, "metrics_ridge_lasso.csv")

W3_MH_COLS = [f"54-{i}" for i in range(1, 15)]


def normalize_group_id(val) -> str:
    if pd.isna(val):
        return ""
    s = str(val).strip()
    if not s or s.lower() in {"nan", "none"}:
        return ""
    if s.lower().startswith("v"):
        return s
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except Exception:
        pass
    if s.endswith(".0"):
        return s[:-2]
    return s


def load_question_list() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_LIST_PATH)
    required = {"Year", "Group_ID", "Question_ID"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in question list: {missing}")
    df["Year"] = df["Year"].astype(str)
    df["Group_ID"] = df["Group_ID"].apply(normalize_group_id)
    df["Question_ID"] = df["Question_ID"].astype(str)
    return df


def load_crossyear() -> pd.DataFrame:
    if os.path.exists(CROSSYEAR_PRIMARY):
        path = CROSSYEAR_PRIMARY
    elif os.path.exists(CROSSYEAR_FALLBACK):
        path = CROSSYEAR_FALLBACK
    else:
        raise FileNotFoundError(CROSSYEAR_PRIMARY)
    df = pd.read_csv(path)
    df["Group_ID"] = df["Group_ID"].apply(normalize_group_id)
    return df


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    w2 = pd.read_csv(W2_PATH, low_memory=False)
    w3 = pd.read_csv(W3_PATH, low_memory=False)

    # Target Y: W3 MH mean
    w3_mh = w3[W3_MH_COLS].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    w3_id_col = "student_id" if "student_id" in w3.columns else "TIGPS_ID"
    w3_target = pd.DataFrame(
        {"merge_id": w3[w3_id_col].astype(str).str.strip(), "y_w3_mh": w3_mh}
    )

    # Feature selection: Scheme A (q<0.05 and valid_row_pct >= 0.5)
    cross = load_crossyear()
    filtered = cross[(cross["q_value"] < 0.05) & (cross["valid_row_pct"] >= 0.5)].copy()
    filtered.to_csv(OUT_FILTERED_GROUPS, index=False, encoding="utf-8-sig")

    group_ids = filtered["Group_ID"].dropna().astype(str).tolist()
    qlist = load_question_list()
    qlist_w2 = qlist[qlist["Year"] == "W2"].copy()
    qlist_w2 = qlist_w2[qlist_w2["Group_ID"].isin(group_ids)]

    # Single-item features
    item_cols = qlist_w2["Question_ID"].dropna().unique().tolist()
    item_cols = [c for c in item_cols if c in w2.columns]

    # Build feature matrix
    X = w2[item_cols].apply(pd.to_numeric, errors="coerce")
    X["merge_id"] = w2["student_id"].astype(str).str.strip()
    data = pd.merge(X, w3_target, on="merge_id", how="inner")
    data = data.dropna(subset=["y_w3_mh"])

    feature_cols = [c for c in data.columns if c not in {"merge_id", "y_w3_mh"}]
    X_all = data[feature_cols]
    y_all = data["y_w3_mh"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42
    )

    ridge = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", RidgeCV(alphas=np.logspace(-3, 3, 50))),
        ]
    )
    lasso = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LassoCV(alphas=np.logspace(-3, 1, 50), max_iter=5000)),
        ]
    )

    ridge.fit(X_train, y_train)
    lasso.fit(X_train, y_train)

    def eval_model(model, name):
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)
        return {
            "model": name,
            "n_features": len(feature_cols),
            "train_r2": r2_score(y_train, pred_train),
            "test_r2": r2_score(y_test, pred_test),
            "train_mae": mean_absolute_error(y_train, pred_train),
            "test_mae": mean_absolute_error(y_test, pred_test),
            "train_rmse": mean_squared_error(y_train, pred_train, squared=False),
            "test_rmse": mean_squared_error(y_test, pred_test, squared=False),
        }

    metrics = pd.DataFrame([eval_model(ridge, "Ridge"), eval_model(lasso, "Lasso")])
    metrics = metrics.round(4)
    metrics.to_csv(OUT_METRICS, index=False, encoding="utf-8-sig")

    ridge_coef = pd.DataFrame(
        {"feature": feature_cols, "coef": ridge.named_steps["model"].coef_}
    ).sort_values("coef", ascending=False)
    ridge_coef["coef"] = ridge_coef["coef"].round(4)
    ridge_coef.to_csv(OUT_RIDGE_COEF, index=False, encoding="utf-8-sig")

    lasso_coef = pd.DataFrame(
        {"feature": feature_cols, "coef": lasso.named_steps["model"].coef_}
    ).sort_values("coef", ascending=False)
    lasso_coef["coef"] = lasso_coef["coef"].round(4)
    lasso_coef.to_csv(OUT_LASSO_COEF, index=False, encoding="utf-8-sig")

    qlist_w2[["Group_ID", "Question_ID"]].to_csv(
        OUT_FEATURES, index=False, encoding="utf-8-sig"
    )

    with open(OUT_DATA_SHAPE, "w", encoding="utf-8") as f:
        f.write(f"Total rows after merge: {len(data)}\n")
        f.write(f"Train rows: {len(X_train)}\n")
        f.write(f"Test rows: {len(X_test)}\n")
        f.write(f"Features used: {len(feature_cols)}\n")

    print(f"Wrote metrics: {OUT_METRICS}")
    print(f"Wrote ridge coefs: {OUT_RIDGE_COEF}")
    print(f"Wrote lasso coefs: {OUT_LASSO_COEF}")
    print(f"Wrote feature list: {OUT_FEATURES}")
    print(f"Wrote data summary: {OUT_DATA_SHAPE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[Error] {exc}")
        sys.exit(1)
