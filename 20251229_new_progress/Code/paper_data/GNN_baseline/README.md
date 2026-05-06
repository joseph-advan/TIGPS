# GraphSAGE Baseline（三種任務）

本資料夾用 `GraphSAGE` 針對三種二元分類任務建立 GNN baseline，資料來源與目標欄位和你前面的 median split logistic baseline 一致。

## 任務定義

1. `w2_self`：用 W2 特徵預測 W2 目標（`v55` 中位數切分）
2. `w3_self`：用 W3 特徵預測 W3 目標（`54` 中位數切分）
3. `w2_predict_w3`：用 W2 特徵預測 W3 目標（`54` 中位數切分）

## 關係邊（Graph Edges）

- W2：
  - `v14_1_01~v14_1_05`（網路朋友）
  - `v14_2_01~v14_2_05`（網路敵人）
  - `v14_3_01~v14_3_05`（現實朋友）
  - `v14_4_01~v14_4_05`（現實敵人）
- W3：
  - `8-1_0~8-1_4`（網路朋友）
  - `8-2_0~8-2_4`（網路敵人）
  - `8-3_0~8-3_4`（現實朋友）
  - `8-4_0~8-4_4`（現實敵人）

每筆 nomination 會先依 `school_id + class + 座號` 對回 `student_id`，形成有向邊 `student_id_src -> student_id_dst`。  
同源同目標同關係類型的重複邊會去重複。

## 特徵與模型

- 特徵：沿用 drop baseline 的題項特徵（非 interpersonal engineered features）
- 目標：各任務目標總分以中位數切 0/1
- 模型：2-layer GraphSAGE（incoming neighbor aggregation）
- 評估：5 seeds（`42,52,62,72,82`），輸出 mean/std

## 執行方式

```powershell
python "C:\Users\user\Desktop\TIGPS_Plan_data\20251229_new_progress\Code\paper_data\GNN_baseline\run_graphsage_three_tasks.py"
```

## 輸出結構

- `outputs/features/`
  - `w2_relation_edges_graphsage.csv`
  - `w3_relation_edges_graphsage.csv`
- `outputs/diagnostics/`
  - `graphsage_three_tasks_diagnostics.json`
- `outputs/model_results/`
  - `graphsage_three_tasks_seed_metrics.csv`
  - `graphsage_three_tasks_summary.csv`
  - `graphsage_three_tasks_summary.md`

## 主要程式

- `run_graphsage_three_tasks.py`：資料準備、建圖、訓練、評估與輸出
