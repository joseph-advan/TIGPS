from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
TABLES_DIR = SCRIPT_PATH.parents[1]
ROOT = SCRIPT_PATH.parents[4]
CODE_DIR = ROOT / "Code" / "paper_data_newdata"
TABLE1_SCRIPT_DIR = TABLES_DIR / "table1" / "scripts"
if str(TABLE1_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(TABLE1_SCRIPT_DIR))
if str(SCRIPT_PATH.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PATH.parent))

import build_table1_drop_decomposition as t1  # noqa: E402
import build_table2_table3_drop_decomposition as t23  # noqa: E402


OUT_PATH = TABLES_DIR / "table3" / "outputs" / "table3_social_network_sensitivity_model_performance.xlsx"


def add_network_features(
    wave: str,
    df: pd.DataFrame,
    X: pd.DataFrame,
    feature_defs: pd.DataFrame,
    specs: list[dict[str, str]],
    label: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ip_path = t1.INTERPERSONAL_FEATURE_FILES[wave]
    ip = t23.core.normalize_student_id(pd.read_csv(ip_path, encoding="utf-8-sig", low_memory=False))
    keep_cols = ["student_id"] + [spec["column"] for spec in specs if spec["column"] in ip.columns]
    ip = ip[keep_cols].drop_duplicates(subset=["student_id"], keep="first")
    merged = df[["student_id"]].merge(ip, on="student_id", how="left")

    X_out = X.copy()
    rows: list[dict[str, Any]] = []
    for spec in specs:
        source_col = spec["column"]
        if source_col not in merged.columns:
            continue
        model_col = f"network_{label}_{source_col}"
        X_out[model_col] = pd.to_numeric(merged[source_col], errors="coerce")
        rows.append(
            {
                "model_column": model_col,
                "feature_code": source_col,
                "feature_name": spec["name"],
                "source_type": f"social_network_{label}",
                "items": spec["items"],
            }
        )
    defs_out = pd.concat([feature_defs, pd.DataFrame(rows)], ignore_index=True)
    return X_out, defs_out


def run_wave_setting(
    wave: str,
    title: str,
    df: pd.DataFrame,
    merged: pd.DataFrame,
    setting: str,
    specs: list[dict[str, str]] | None,
) -> pd.DataFrame:
    target_items = t23.TARGET_W2_ITEMS if wave == "W2" else t23.TARGET_W3_ITEMS
    target_group = "v55" if wave == "W2" else "54"
    _, y, _ = t23.make_target(df, target_items)
    X, feature_defs, _ = t23.build_drop_decomposition_features(df, merged, wave, target_group)
    if specs is not None:
        X, feature_defs = add_network_features(wave, df, X, feature_defs, specs, setting)
    _, perf = t23.fit_model_comparison(y, X, feature_defs)
    perf.insert(0, "Feature Set", setting)
    perf.insert(0, "Wave", title)
    return perf


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged_path = t23.core.pick_first_existing_path(t23.core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")
    for c in ["Year", "Group_ID", "Question_ID"]:
        if c in merged.columns:
            merged[c] = merged[c].astype(str).str.strip()

    datasets = {
        "W2": t23.core.normalize_student_id(pd.read_csv(t23.W2_DATA, encoding="utf-8-sig", low_memory=False)),
        "W3": t23.core.normalize_student_id(pd.read_csv(t23.W3_DATA, encoding="utf-8-sig", low_memory=False)),
    }
    titles = {"W2": "W2 2024", "W3": "W3 2025"}
    settings = [
        ("baseline_individual_only", None),
        ("plus_observed_network", t1.INTERPERSONAL_TABLE1_FEATURES),
        ("plus_respondent_class_normalized_network", t1.INTERPERSONAL_TABLE1_NORMALIZED_FEATURES),
    ]

    frames = []
    for wave, df in datasets.items():
        for setting, specs in settings:
            frames.append(run_wave_setting(wave, titles[wave], df, merged, setting, specs))
    out = pd.concat(frames, ignore_index=True)

    ordered = [
        "Wave",
        "Feature Set",
        "Model",
        "N",
        "N features",
        "Selected C",
        "CV auc mean",
        "CV auc SD",
        "CV accuracy mean",
        "CV accuracy SD",
        "CV balanced_accuracy mean",
        "CV balanced_accuracy SD",
        "CV precision mean",
        "CV precision SD",
        "CV recall mean",
        "CV recall SD",
        "CV f1 mean",
        "CV f1 SD",
        "Test AUC",
        "Test Accuracy",
        "Test Balanced Accuracy",
        "Test Precision",
        "Test Recall",
        "Test F1",
    ]
    out = out[[c for c in ordered if c in out.columns]]

    with pd.ExcelWriter(OUT_PATH, engine="openpyxl") as writer:
        out.to_excel(writer, index=False, sheet_name="ModelSensitivity")
        worksheet = writer.book["ModelSensitivity"]
        worksheet.freeze_panes = "A2"
        for column_cells in worksheet.columns:
            max_len = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_len + 2, 12), 45)

    print(f"Wrote {OUT_PATH}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
