# Feature Decomposition

This folder documents and evaluates the current drop + decomposition feature strategy used in the main-paper analysis.

## Current Scope

- Predictor wave: W2 only.
- Prediction tasks: W2 predictors -> W2 high psychological distress; W2 predictors -> W3 high psychological distress.
- W3 subscale definitions are retained only as questionnaire mapping/reference.
- Latest v54 decision: `v54_18` belongs to Responsible Decision-Making, not Self-Awareness.

## Physical Structure

Core scripts and configs stay in the root because downstream model scripts import or read them directly. Documentation and generated outputs are grouped into subfolders.

```text
Feature_Decomposition/
├─ README.md
├─ build_binary_drop_then_split_baseline.py
├─ run_subscale_cronbach_alpha_reliability.py
├─ run_v54_sel_deep_dive.py
├─ subscale_definitions_w2_w3.json
├─ subscale_definitions_w2_w3_table.csv
├─ W2_W3_subscale_definitions_record.md
├─ docs/
└─ outputs/
```

For the detailed Chinese structure guide, see:

- `docs/FEATURE_DECOMPOSITION_STRUCTURE_ZH.md`

## Root-Level Core Files

| File | Purpose |
|---|---|
| `subscale_definitions_w2_w3.json` | Machine-readable source of the current W2/W3 subscale definitions. W2 is used for modeling; W3 is reference only. |
| `subscale_definitions_w2_w3_table.csv` | Flat table export of the same definitions, easier to inspect in Excel. |
| `W2_W3_subscale_definitions_record.md` | Human-readable formal record explaining how groups were split and naming each subscale in Chinese and English. |
| `build_binary_drop_then_split_baseline.py` | Compares drop-only features vs drop + decomposed features for W2->W2 and W2->W3. |
| `run_subscale_cronbach_alpha_reliability.py` | Calculates W2-only Cronbach's alpha and item diagnostics for configured subscales. |
| `run_v54_sel_deep_dive.py` | SEL/v54-specific reliability deep dive used to validate the revised v54 grouping. |

## docs/

| File | Purpose |
|---|---|
| `docs/FEATURE_DECOMPOSITION_STRUCTURE_ZH.md` | Chinese folder structure guide and recommended reading order. |
| `docs/v54_revision_rerun_change_summary.md` | Records the v54 revision, downstream rerun scope, and major result changes. |

## outputs/model_performance/

| File | Purpose |
|---|---|
| `outputs/model_performance/binary_drop_then_split_summary.md` | Main readable summary of drop-only vs drop + decomposition model performance. |
| `outputs/model_performance/binary_drop_then_split_summary.csv` | Machine-readable performance summary. |
| `outputs/model_performance/binary_drop_then_split_details.json` | Detailed model inputs, outputs, and configuration snapshot. |

## outputs/reliability/

| File | Purpose |
|---|---|
| `outputs/reliability/subscale_cronbach_alpha_reliability.xlsx` | Workbook with W2 subscale alpha, parent-scale alpha, item diagnostics, and review flags. |
| `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md` | Readable reliability summary. |
| `outputs/reliability/subscale_cronbach_alpha_reliability_details.json` | Machine-readable reliability details. |

## outputs/v54_deep_dive/

| File | Purpose |
|---|---|
| `outputs/v54_deep_dive/v54_sel_deep_dive_reliability.xlsx` | V54-specific reliability workbook. |
| `outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md` | V54-specific reliability summary. |

## Recommended Reading Order

1. `W2_W3_subscale_definitions_record.md`
2. `outputs/reliability/subscale_cronbach_alpha_reliability_summary.md`
3. `outputs/v54_deep_dive/v54_sel_deep_dive_reliability_summary.md`
4. `outputs/model_performance/binary_drop_then_split_summary.md`
5. `docs/v54_revision_rerun_change_summary.md`

## Current Interpretation

The decomposition strategy is evaluated in two ways:

1. Prediction performance: whether splitting broad W2 predictor groups into subscales improves W2->W2 and W2->W3 model performance.
2. Reliability: whether each configured W2 subscale has acceptable internal consistency according to Cronbach's alpha and item diagnostics.

Subscales with lower alpha are not automatically removed. They should be reviewed against item wording, theory, and downstream predictive value.
