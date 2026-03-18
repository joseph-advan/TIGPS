import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.impute import SimpleImputer
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

OUT_DIR = os.path.join(
    BASE_DIR, r"Code\Analysis\ML_baseline\Mental分組測試\Regression\單題目"
)
OUT_OLS_STD = os.path.join(OUT_DIR, "ols_ttest.csv")
OUT_OLS_HC3 = os.path.join(OUT_DIR, "ols_ttest_hc3.csv")
OUT_SUMMARY = os.path.join(OUT_DIR, "ols_data_summary.txt")
OUT_FEATURES = os.path.join(OUT_DIR, "selected_items.csv")

W3_MH_COLS = [f"54-{i}" for i in range(1, 15)]


def build_ols_tables(X: pd.DataFrame, y: pd.Series, feature_cols):
    X_imp = SimpleImputer(strategy="median").fit_transform(X)
    X_std = StandardScaler().fit_transform(X_imp)
    X_const = sm.add_constant(X_std, has_constant="add")

    model = sm.OLS(y, X_const).fit()
    model_hc3 = model.get_robustcov_results(cov_type="HC3")

    names = ["const"] + feature_cols

    def to_df(res) -> pd.DataFrame:
        ci = res.conf_int()
        ci_arr = ci.to_numpy() if hasattr(ci, "to_numpy") else np.asarray(ci)
        return pd.DataFrame(
            {
                "feature": names,
                "coef": res.params,
                "std_err": res.bse,
                "t": res.tvalues,
                "p_value": res.pvalues,
                "ci_low": ci_arr[:, 0],
                "ci_high": ci_arr[:, 1],
            }
        )

    return to_df(model), to_df(model_hc3)


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

    # Selected items (from previous run)
    items_df = pd.read_csv(OUT_FEATURES)
    item_cols = items_df["Question_ID"].dropna().astype(str).tolist()

    # Keep only items that exist in W2
    item_cols = [c for c in item_cols if c in w2.columns]

    # Build feature matrix
    X = w2[item_cols].apply(pd.to_numeric, errors="coerce")
    X["merge_id"] = w2["student_id"].astype(str).str.strip()
    data = pd.merge(X, w3_target, on="merge_id", how="inner")
    data = data.dropna(subset=["y_w3_mh"])

    feature_cols = [c for c in data.columns if c not in {"merge_id", "y_w3_mh"}]
    X_all = data[feature_cols]
    y_all = data["y_w3_mh"].astype(float)

    ols_std, ols_hc3 = build_ols_tables(X_all, y_all, feature_cols)
    ols_std.to_csv(OUT_OLS_STD, index=False, encoding="utf-8-sig")
    ols_hc3.to_csv(OUT_OLS_HC3, index=False, encoding="utf-8-sig")

    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write(f"Total rows after merge: {len(data)}\n")
        f.write(f"Features used: {len(feature_cols)}\n")
        f.write("Note: OLS uses median imputation + standard scaling.\n")

    print(f"Wrote OLS (standard): {OUT_OLS_STD}")
    print(f"Wrote OLS (HC3): {OUT_OLS_HC3}")
    print(f"Wrote summary: {OUT_SUMMARY}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[Error] {exc}")
        sys.exit(1)
