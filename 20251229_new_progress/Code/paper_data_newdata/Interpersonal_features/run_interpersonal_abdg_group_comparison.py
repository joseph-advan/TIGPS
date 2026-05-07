from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

import run_interpersonal_feature_logistic_comparison as core


THIS_FILE = Path(__file__).resolve()
OUT_ROOT = THIS_FILE.parent / "outputs" / "model_results"
OUT_ROOT.mkdir(parents=True, exist_ok=True)


# Group definitions requested by user: A, B, D, G only.
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
    "D": [
        "ip_out_friend_online_minus_offline",
        "ip_out_enemy_online_minus_offline",
        "ip_in_friend_online_minus_offline",
        "ip_in_enemy_online_minus_offline",
    ],
    "G": [
        "ip_reciprocal_friend_count",
        "ip_reciprocal_enemy_count",
        "ip_liked_by_me_but_enemy_to_me_count",
        "ip_enemy_by_me_but_likes_me_count",
        "ip_same_target_friend_and_enemy_count",
    ],
}


def setting_label(x: str) -> str:
    m = {
        "baseline_drop": "Drop Baseline",
        "drop_plus_A": "Drop + A",
        "drop_plus_B": "Drop + B",
        "drop_plus_D": "Drop + D",
        "drop_plus_G": "Drop + G",
        "drop_plus_ABDG": "Drop + ABDG",
    }
    return m.get(x, x)


def scenario_label(x: str) -> str:
    m = {
        "w2_self": "W2 -> W2",
        "w3_self": "W3 -> W3",
        "w2_predict_w3": "W2 -> W3",
    }
    return m.get(x, x)


def _md_table(df: pd.DataFrame, cols: list[str]) -> str:
    out = df[cols].copy()
    for c in out.columns:
        if pd.api.types.is_float_dtype(out[c]):
            out[c] = out[c].map(lambda v: f"{v:.6f}")
    return out.to_markdown(index=False)


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

    # Keep only A/B/D/G in each year, and build ABDG union.
    year_group_cols: dict[str, dict[str, list[str]]] = {}
    for year, ip_cols in year_to_ip_cols.items():
        gcols: dict[str, list[str]] = {}
        for g, cols in GROUP_DEF.items():
            gcols[g] = [c for c in cols if c in ip_cols]
        abdg = []
        seen = set()
        for g in ["A", "B", "D", "G"]:
            for c in gcols[g]:
                if c not in seen:
                    abdg.append(c)
                    seen.add(c)
        gcols["ABDG"] = abdg
        year_group_cols[year] = gcols

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
            ("drop_plus_D", gcols["D"]),
            ("drop_plus_G", gcols["G"]),
            ("drop_plus_ABDG", gcols["ABDG"]),
        ]

        for st_name, extra_cols in settings:
            if extra_cols:
                feature_table = feature_df[["student_id"] + base_cols_drop].copy()
                feature_table = feature_table.merge(ip_df[["student_id"] + extra_cols], on="student_id", how="left")
                feature_cols = base_cols_drop + extra_cols
            else:
                feature_table = feature_df[["student_id"] + base_cols_drop].copy()
                feature_cols = base_cols_drop

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
                "setting": st_name,
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
                    "setting": st_name,
                    "target_meta": target_meta,
                    "missing_drop_groups_items": missing_drop,
                    "extra_group_features": extra_cols,
                    "metrics": metrics,
                }
            )

    summary_df = pd.DataFrame(results).sort_values(["scenario", "test_accuracy"], ascending=[True, False]).reset_index(drop=True)

    # delta vs drop baseline by scenario
    delta_rows = []
    for sc in summary_df["scenario"].unique():
        sub = summary_df[summary_df["scenario"] == sc].copy()
        base_acc = float(sub[sub["setting"] == "baseline_drop"]["test_accuracy"].iloc[0])
        base_f1 = float(sub[sub["setting"] == "baseline_drop"]["test_f1"].iloc[0])
        base_auc = float(sub[sub["setting"] == "baseline_drop"]["test_auc"].iloc[0])
        for _, r in sub.iterrows():
            delta_rows.append(
                {
                    "scenario": sc,
                    "setting": r["setting"],
                    "delta_test_accuracy_vs_drop": float(r["test_accuracy"] - base_acc),
                    "delta_test_f1_vs_drop": float(r["test_f1"] - base_f1),
                    "delta_test_auc_vs_drop": float(r["test_auc"] - base_auc),
                }
            )
    delta_df = pd.DataFrame(delta_rows)

    summary_csv = OUT_ROOT / "abdg_vs_drop_baseline_summary.csv"
    delta_csv = OUT_ROOT / "abdg_vs_drop_baseline_deltas.csv"
    detail_json = OUT_ROOT / "abdg_vs_drop_baseline_details.json"
    report_md = OUT_ROOT / "abdg_vs_drop_baseline_report_zh.md"

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
                "year_group_columns_used": year_group_cols,
                "records": details,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # Build Chinese report.
    md: list[str] = []
    md.append("# ABDG 人際特徵實驗報告（以 Drop Baseline 為基準）")
    md.append("")
    md.append("## 1. 實驗設定")
    md.append("- 基準模型：Drop Baseline。")
    md.append("- 比較模型：Drop + A、Drop + B、Drop + D、Drop + G、Drop + ABDG。")
    md.append("- 三個任務：W2 -> W2、W3 -> W3、W2 -> W3。")
    md.append("")
    md.append("### A/B/D/G 組別定義")
    group_def_tbl = pd.DataFrame(
        [
            {"組別": "A", "說明": "基本提名 in/out 次數", "欄位數": 8, "欄位": "; ".join(GROUP_DEF["A"])},
            {"組別": "B", "說明": "friend/enemy 合計", "欄位數": 4, "欄位": "; ".join(GROUP_DEF["B"])},
            {"組別": "D", "說明": "online-offline 差值", "欄位數": 4, "欄位": "; ".join(GROUP_DEF["D"])},
            {"組別": "G", "說明": "互惠/衝突次數", "欄位數": 5, "欄位": "; ".join(GROUP_DEF["G"])},
            {
                "組別": "ABDG",
                "說明": "A+B+D+G 合併",
                "欄位數": len(year_group_cols["W2"]["ABDG"]),
                "欄位": "; ".join(year_group_cols["W2"]["ABDG"]),
            },
        ]
    )
    md.append(_md_table(group_def_tbl, ["組別", "說明", "欄位數", "欄位"]))
    md.append("")
    md.append("## 2. 整體平均（跨三任務）")
    overall = summary_df.groupby("setting", as_index=False).agg(
        mean_test_accuracy=("test_accuracy", "mean"),
        mean_test_f1=("test_f1", "mean"),
        mean_test_auc=("test_auc", "mean"),
    )
    overall["設定"] = overall["setting"].map(setting_label)
    overall = overall.sort_values("mean_test_accuracy", ascending=False)
    md.append(_md_table(overall, ["設定", "mean_test_accuracy", "mean_test_f1", "mean_test_auc"]))
    md.append("")
    md.append("## 3. 各任務比較（依 test_accuracy 由高到低）")

    for sc in ["w2_self", "w3_self", "w2_predict_w3"]:
        sub = summary_df[summary_df["scenario"] == sc].copy()
        sub = sub.merge(delta_df[delta_df["scenario"] == sc], on=["scenario", "setting"], how="left")
        sub = sub.sort_values("test_accuracy", ascending=False)
        sub["設定"] = sub["setting"].map(setting_label)

        md.append(f"### {scenario_label(sc)}")
        drop_acc = float(sub[sub["setting"] == "baseline_drop"]["test_accuracy"].iloc[0])
        md.append(f"- Drop Baseline accuracy: **{drop_acc:.6f}**")
        md.append(_md_table(
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
            ],
        ))
        md.append("")

    md.append("## 4. 重點結論")
    md.append("- 可以直接看每個任務中，`delta_test_accuracy_vs_drop` 為正的組別代表比 drop baseline 好。")
    md.append("- `Drop + ABDG` 是四組合併版本；請和單組 A/B/D/G 對照，看是否有疊加效果。")
    md.append("- 如果多數任務中 `Drop + ABDG` 仍低於 baseline，表示四組一起加的噪音可能大於增益。")
    md.append("")
    md.append("## 5. 產出檔案")
    md.append(f"- 摘要：`{summary_csv}`")
    md.append(f"- 差異：`{delta_csv}`")
    md.append(f"- 明細：`{detail_json}`")
    md.append(f"- 本報告：`{report_md}`")
    md.append("")

    report_md.write_text("\n".join(md) + "\n", encoding="utf-8-sig")

    print("Done.")
    print("Wrote:", summary_csv)
    print("Wrote:", delta_csv)
    print("Wrote:", detail_json)
    print("Wrote:", report_md)


if __name__ == "__main__":
    main()
