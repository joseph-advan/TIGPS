from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

import run_interpersonal_feature_logistic_comparison as core


THIS_FILE = Path(__file__).resolve()
OUT_ROOT = THIS_FILE.parent / "outputs" / "model_results"
OUT_ROOT.mkdir(parents=True, exist_ok=True)


GROUP_DEF: dict[str, list[str]] = {
    "A": [
        "ip_out_online_friend",
        "ip_in_online_friend",
        "ip_out_online_enemy",
        "ip_in_online_enemy",
        "ip_out_offline_friend",
        "ip_in_offline_friend",
        "ip_out_offline_enemy",
        "ip_in_offline_enemy",
    ],
    "B": [
        "ip_out_friend_total",
        "ip_out_enemy_total",
        "ip_in_friend_total",
        "ip_in_enemy_total",
    ],
    "C": [
        "ip_out_friend_online_minus_offline",
        "ip_out_enemy_online_minus_offline",
        "ip_in_friend_online_minus_offline",
        "ip_in_enemy_online_minus_offline",
    ],
    "D": [
        "ip_reciprocal_friend_count",
        "ip_reciprocal_enemy_count",
        "ip_liked_by_me_but_enemy_to_me_count",
        "ip_enemy_by_me_but_likes_me_count",
        "ip_same_target_friend_and_enemy_count",
    ],
}

D_KEYS = ["D1", "D2", "D3", "D4", "D5"]
D_KEY_TO_FEATURE = {f"D{i + 1}": GROUP_DEF["D"][i] for i in range(5)}

SETTING_ORDER = [
    "baseline_drop",
    "drop_plus_A",
    "drop_plus_B",
    "drop_plus_C",
    "drop_plus_D1",
    "drop_plus_D2",
    "drop_plus_D3",
    "drop_plus_D4",
    "drop_plus_D5",
]

SCENARIO_ORDER = ["w2_self", "w3_self", "w2_predict_w3"]

FEATURE_DESC = {
    "ip_reciprocal_friend_count": "互相提名 friend 的人數",
    "ip_reciprocal_enemy_count": "互相提名 enemy 的人數",
    "ip_liked_by_me_but_enemy_to_me_count": "我提名 friend、對方提名我 enemy 的人數",
    "ip_enemy_by_me_but_likes_me_count": "我提名 enemy、對方提名我 friend 的人數",
    "ip_same_target_friend_and_enemy_count": "同一目標同時被提名 friend 與 enemy 的人數",
}


def setting_label(x: str) -> str:
    mapping = {
        "baseline_drop": "Drop Baseline",
        "drop_plus_A": "Drop + A",
        "drop_plus_B": "Drop + B",
        "drop_plus_C": "Drop + C",
        "drop_plus_D1": "Drop + D1",
        "drop_plus_D2": "Drop + D2",
        "drop_plus_D3": "Drop + D3",
        "drop_plus_D4": "Drop + D4",
        "drop_plus_D5": "Drop + D5",
    }
    return mapping.get(x, x)


def scenario_label(x: str) -> str:
    mapping = {
        "w2_self": "W2 -> W2",
        "w3_self": "W3 -> W3",
        "w2_predict_w3": "W2 -> W3",
    }
    return mapping.get(x, x)


def _md_table(df: pd.DataFrame, cols: list[str]) -> str:
    out = df[cols].copy()
    for col in out.columns:
        if pd.api.types.is_float_dtype(out[col]):
            out[col] = out[col].map(lambda v: f"{v:.6f}")
    return out.to_markdown(index=False)


def _sort_for_output(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    sort_cols: list[str] = []
    if "scenario" in out.columns:
        out["scenario"] = pd.Categorical(out["scenario"], categories=SCENARIO_ORDER, ordered=True)
        sort_cols.append("scenario")
    if "setting" in out.columns:
        out["setting"] = pd.Categorical(out["setting"], categories=SETTING_ORDER, ordered=True)
        sort_cols.append("setting")
    if sort_cols:
        out = out.sort_values(sort_cols).reset_index(drop=True)
    if "scenario" in out.columns:
        out["scenario"] = out["scenario"].astype(str)
    if "setting" in out.columns:
        out["setting"] = out["setting"].astype(str)
    return out


def main() -> None:
    merged_path = core.pick_first_existing_path(core.MERGED_PATH_CANDIDATES)
    merged = pd.read_csv(merged_path, dtype=str, encoding="utf-8-sig")

    w2_raw = core.normalize_student_id(pd.read_csv(core.W2_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    w3_raw = core.normalize_student_id(pd.read_csv(core.W3_DATA_PATH, low_memory=False, dtype=str, encoding="utf-8-sig"))
    roster = core.load_roster()

    w2_feats, w3_feats, diagnostics, w2_ip_cols, w3_ip_cols = core.build_interpersonal_augmented_tables(
        w2_raw=w2_raw,
        w3_raw=w3_raw,
        roster=roster,
    )

    year_to_raw = {"W2": w2_raw, "W3": w3_raw}
    year_to_ip = {"W2": w2_feats, "W3": w3_feats}
    year_to_ip_cols = {"W2": w2_ip_cols, "W3": w3_ip_cols}

    year_group_cols: dict[str, dict[str, list[str]]] = {}
    for year, ip_cols in year_to_ip_cols.items():
        group_cols: dict[str, list[str]] = {}
        for group_name in ["A", "B", "C", "D"]:
            group_cols[group_name] = [c for c in GROUP_DEF[group_name] if c in ip_cols]
        for d_key in D_KEYS:
            feature_name = D_KEY_TO_FEATURE[d_key]
            group_cols[d_key] = [feature_name] if feature_name in ip_cols else []
        year_group_cols[year] = group_cols

    results: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []

    for scenario in core.SCENARIOS:
        target_df = year_to_raw[scenario.target_year]
        target_table, target_meta = core.build_target_table_median(
            merged=merged,
            target_year=scenario.target_year,
            target_group_id=scenario.target_group_id,
            target_df=target_df,
        )

        feature_df = year_to_raw[scenario.feature_year]
        drop_groups = core.select_group_ids(year=scenario.feature_year, use_drop=True)
        base_cols_drop, missing_drop = core.collect_feature_columns(
            merged=merged,
            data_year=scenario.feature_year,
            data_df=feature_df,
            group_ids=drop_groups,
        )

        ip_df = year_to_ip[scenario.feature_year]
        gcols = year_group_cols[scenario.feature_year]
        settings = [
            ("baseline_drop", []),
            ("drop_plus_A", gcols["A"]),
            ("drop_plus_B", gcols["B"]),
            ("drop_plus_C", gcols["C"]),
            ("drop_plus_D1", gcols["D1"]),
            ("drop_plus_D2", gcols["D2"]),
            ("drop_plus_D3", gcols["D3"]),
            ("drop_plus_D4", gcols["D4"]),
            ("drop_plus_D5", gcols["D5"]),
        ]

        for setting_name, extra_cols in settings:
            feature_table = feature_df[["student_id"] + base_cols_drop].copy()
            if extra_cols:
                feature_table = feature_table.merge(ip_df[["student_id"] + extra_cols], on="student_id", how="left")
            feature_cols = base_cols_drop + extra_cols

            model_df = core.prepare_model_table(
                features_df=feature_table,
                target_table=target_table,
                feature_cols=feature_cols,
            )
            metrics, _model, _x_test, _y_test = core.run_logistic_binary(
                model_df=model_df,
                feature_cols=feature_cols,
            )

            row = {
                "scenario": scenario.name,
                "setting": setting_name,
                "feature_year": scenario.feature_year,
                "target_year": scenario.target_year,
                "target_group_id": scenario.target_group_id,
                "target_median_cutoff": target_meta["target_median_cutoff"],
                "target_positive_rate": target_meta["target_positive_rate"],
                "n_base_features_drop": len(base_cols_drop),
                "n_group_features_added": len(extra_cols),
                "group_features_added": ";".join(extra_cols),
                **metrics,
            }
            results.append(row)
            details.append(
                {
                    "scenario": scenario.name,
                    "setting": setting_name,
                    "target_meta": target_meta,
                    "missing_drop_groups_items": missing_drop,
                    "extra_group_features": extra_cols,
                    "metrics": metrics,
                }
            )

    summary_df = _sort_for_output(pd.DataFrame(results))

    delta_rows: list[dict[str, Any]] = []
    for scenario in SCENARIO_ORDER:
        sub = summary_df[summary_df["scenario"] == scenario].copy()
        baseline = sub[sub["setting"] == "baseline_drop"]
        if baseline.empty:
            continue
        base_acc = float(baseline["test_accuracy"].iloc[0])
        base_f1 = float(baseline["test_f1"].iloc[0])
        base_auc = float(baseline["test_auc"].iloc[0])

        for _, r in sub.iterrows():
            delta_rows.append(
                {
                    "scenario": scenario,
                    "setting": r["setting"],
                    "delta_test_accuracy_vs_drop": float(r["test_accuracy"] - base_acc),
                    "delta_test_f1_vs_drop": float(r["test_f1"] - base_f1),
                    "delta_test_auc_vs_drop": float(r["test_auc"] - base_auc),
                }
            )

    delta_df = _sort_for_output(pd.DataFrame(delta_rows))

    summary_csv = OUT_ROOT / "abcd_dsplit_vs_drop_baseline_summary.csv"
    delta_csv = OUT_ROOT / "abcd_dsplit_vs_drop_baseline_deltas.csv"
    detail_json = OUT_ROOT / "abcd_dsplit_vs_drop_baseline_details.json"
    report_md = OUT_ROOT / "abcd_dsplit_vs_drop_baseline_report_zh.md"

    summary_df.to_csv(summary_csv, index=False, encoding="utf-8-sig")
    delta_df.to_csv(delta_csv, index=False, encoding="utf-8-sig")
    with detail_json.open("w", encoding="utf-8-sig") as f:
        json.dump(
            {
                "data_paths": {
                    "w2_data_path": str(core.W2_DATA_PATH),
                    "w3_data_path": str(core.W3_DATA_PATH),
                    "basic_info_path": str(core.BASIC_INFO_PATH),
                    "mapping_path": str(merged_path),
                },
                "diagnostics": diagnostics,
                "group_definition": GROUP_DEF,
                "d_split_definition": D_KEY_TO_FEATURE,
                "year_group_columns_used": year_group_cols,
                "records": details,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    report_lines: list[str] = []
    report_lines.append("# ABCD（D 拆成 D1~D5）與 Drop Baseline 比較報告")
    report_lines.append("")
    report_lines.append("## 1. 設定")
    report_lines.append("- 本次比較設定：Drop Baseline、A、B、C、D1、D2、D3、D4、D5。")
    report_lines.append("- 三個情境：W2 -> W2、W3 -> W3、W2 -> W3。")
    report_lines.append("")

    setting_tbl = pd.DataFrame(
        [
            {"設定": "Drop Baseline", "加入特徵數": 0, "加入特徵": ""},
            {"設定": "Drop + A", "加入特徵數": len(GROUP_DEF["A"]), "加入特徵": "; ".join(GROUP_DEF["A"])},
            {"設定": "Drop + B", "加入特徵數": len(GROUP_DEF["B"]), "加入特徵": "; ".join(GROUP_DEF["B"])},
            {"設定": "Drop + C", "加入特徵數": len(GROUP_DEF["C"]), "加入特徵": "; ".join(GROUP_DEF["C"])},
            {"設定": "Drop + D1", "加入特徵數": 1, "加入特徵": D_KEY_TO_FEATURE["D1"]},
            {"設定": "Drop + D2", "加入特徵數": 1, "加入特徵": D_KEY_TO_FEATURE["D2"]},
            {"設定": "Drop + D3", "加入特徵數": 1, "加入特徵": D_KEY_TO_FEATURE["D3"]},
            {"設定": "Drop + D4", "加入特徵數": 1, "加入特徵": D_KEY_TO_FEATURE["D4"]},
            {"設定": "Drop + D5", "加入特徵數": 1, "加入特徵": D_KEY_TO_FEATURE["D5"]},
        ]
    )
    report_lines.append(_md_table(setting_tbl, ["設定", "加入特徵數", "加入特徵"]))
    report_lines.append("")

    d_desc_tbl = pd.DataFrame(
        [
            {"D子組": "D1", "特徵": D_KEY_TO_FEATURE["D1"], "說明": FEATURE_DESC[D_KEY_TO_FEATURE["D1"]]},
            {"D子組": "D2", "特徵": D_KEY_TO_FEATURE["D2"], "說明": FEATURE_DESC[D_KEY_TO_FEATURE["D2"]]},
            {"D子組": "D3", "特徵": D_KEY_TO_FEATURE["D3"], "說明": FEATURE_DESC[D_KEY_TO_FEATURE["D3"]]},
            {"D子組": "D4", "特徵": D_KEY_TO_FEATURE["D4"], "說明": FEATURE_DESC[D_KEY_TO_FEATURE["D4"]]},
            {"D子組": "D5", "特徵": D_KEY_TO_FEATURE["D5"], "說明": FEATURE_DESC[D_KEY_TO_FEATURE["D5"]]},
        ]
    )
    report_lines.append("### D1~D5 定義")
    report_lines.append(_md_table(d_desc_tbl, ["D子組", "特徵", "說明"]))
    report_lines.append("")

    report_lines.append("## 2. 各設定平均表現")
    overall = summary_df.groupby("setting", as_index=False).agg(
        mean_test_accuracy=("test_accuracy", "mean"),
        mean_test_f1=("test_f1", "mean"),
        mean_test_auc=("test_auc", "mean"),
    )
    overall = _sort_for_output(overall)
    overall["設定"] = overall["setting"].map(setting_label)
    report_lines.append(_md_table(overall, ["設定", "mean_test_accuracy", "mean_test_f1", "mean_test_auc"]))
    report_lines.append("")

    report_lines.append("## 3. 各情境比較（相對 Drop Baseline）")
    for scenario in SCENARIO_ORDER:
        sub = summary_df[summary_df["scenario"] == scenario].copy()
        sub = sub.merge(delta_df[delta_df["scenario"] == scenario], on=["scenario", "setting"], how="left")
        sub = _sort_for_output(sub)
        sub["設定"] = sub["setting"].map(setting_label)
        drop_acc = float(sub[sub["setting"] == "baseline_drop"]["test_accuracy"].iloc[0])

        report_lines.append(f"### {scenario_label(scenario)}")
        report_lines.append(f"- Drop Baseline accuracy: **{drop_acc:.6f}**")
        report_lines.append(
            _md_table(
                sub,
                [
                    "設定",
                    "test_accuracy",
                    "delta_test_accuracy_vs_drop",
                    "test_f1",
                    "delta_test_f1_vs_drop",
                    "test_auc",
                    "delta_test_auc_vs_drop",
                    "n_group_features_added",
                    "group_features_added",
                ],
            )
        )
        report_lines.append("")

    report_lines.append("## 4. 輸出檔案")
    report_lines.append(f"- Summary CSV: `{summary_csv}`")
    report_lines.append(f"- Delta CSV: `{delta_csv}`")
    report_lines.append(f"- Details JSON: `{detail_json}`")
    report_lines.append(f"- Markdown 報告: `{report_md}`")
    report_lines.append("")

    report_md.write_text("\n".join(report_lines) + "\n", encoding="utf-8-sig")

    print("Done.")
    print("Wrote:", summary_csv)
    print("Wrote:", delta_csv)
    print("Wrote:", detail_json)
    print("Wrote:", report_md)


if __name__ == "__main__":
    main()
