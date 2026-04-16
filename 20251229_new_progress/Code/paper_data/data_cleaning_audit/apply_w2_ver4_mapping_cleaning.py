from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd


LEAD_NUM_RE = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)")
FULL_NUM_RE = re.compile(r"^\s*[+-]?\d+(?:\.\d+)?\s*$")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass
class GroupRule:
    group_id: str
    change_class: str
    columns: List[str]
    raw_text_map: Dict[str, str]
    raw_numprefix_map: Dict[str, str]
    raw_sentinel_map: Dict[str, str]


def split_cols(text: str) -> List[str]:
    return [x.strip() for x in str(text).split(";") if x.strip()]


def normalize_number_token(token: str) -> str:
    token = str(token).strip()
    try:
        value = float(token)
    except Exception:
        return token
    if value.is_integer():
        return str(int(value))
    out = f"{value:.10f}".rstrip("0").rstrip(".")
    return "0" if out in ("-0", "") else out


def extract_leading_number(text: str) -> str | None:
    m = LEAD_NUM_RE.match(text)
    if not m:
        return None
    return normalize_number_token(m.group(1))


def decode_clean_value(raw_clean_value: str) -> str:
    if raw_clean_value == "CLEAN_EMPTY":
        return ""
    if raw_clean_value.startswith("CLEAN_NUM:"):
        return normalize_number_token(raw_clean_value.split(":", 1)[1])
    if raw_clean_value.startswith("CLEAN_TEXT:"):
        return raw_clean_value.split(":", 1)[1]
    return raw_clean_value


def build_group_rules(mapping_csv: Path, available_columns: Iterable[str]) -> List[GroupRule]:
    mapping_df = pd.read_csv(mapping_csv, dtype=str, encoding="utf-8-sig").fillna("")
    available = set(available_columns)
    rules: List[GroupRule] = []

    for _, row in mapping_df.iterrows():
        pattern_text = row["mapping_pattern_json"]
        if not pattern_text.strip():
            continue
        pattern = json.loads(pattern_text)

        col_candidates = split_cols(row["columns"]) + split_cols(row["source_columns"])
        deduped_candidates = []
        seen = set()
        for c in col_candidates:
            if c in seen:
                continue
            seen.add(c)
            deduped_candidates.append(c)
        cols = [c for c in deduped_candidates if c in available]
        if not cols:
            continue

        raw_text_map: Dict[str, str] = {}
        raw_numprefix_map: Dict[str, str] = {}
        raw_sentinel_map: Dict[str, str] = {}

        for raw_key, clean_value in pattern.items():
            if raw_key.startswith("RAW_TEXT:"):
                raw_text_map[raw_key.split(":", 1)[1].strip()] = decode_clean_value(clean_value)
            elif raw_key.startswith("RAW_NUMPREFIX:"):
                raw_numprefix_map[normalize_number_token(raw_key.split(":", 1)[1])] = decode_clean_value(clean_value)
            elif raw_key.startswith("RAW_SENT:"):
                raw_sentinel_map[normalize_number_token(raw_key.split(":", 1)[1])] = decode_clean_value(clean_value)

        rules.append(
            GroupRule(
                group_id=row["group_id"],
                change_class=row["change_class"],
                columns=cols,
                raw_text_map=raw_text_map,
                raw_numprefix_map=raw_numprefix_map,
                raw_sentinel_map=raw_sentinel_map,
            )
        )
    return rules


def map_single_value(value: str, rule: GroupRule) -> str:
    if pd.isna(value):
        return ""
    raw = str(value).strip()
    if raw == "":
        return ""

    if raw in rule.raw_text_map:
        return rule.raw_text_map[raw]

    if FULL_NUM_RE.match(raw):
        n = normalize_number_token(raw)
        if n in rule.raw_sentinel_map:
            return rule.raw_sentinel_map[n]
        if n in rule.raw_numprefix_map:
            return rule.raw_numprefix_map[n]

    lead = extract_leading_number(raw)
    if lead is not None:
        if lead in rule.raw_sentinel_map:
            return rule.raw_sentinel_map[lead]
        if lead in rule.raw_numprefix_map:
            return rule.raw_numprefix_map[lead]

    return raw


def count_cjk_columns(df: pd.DataFrame, columns: List[str]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for c in columns:
        s = df[c].fillna("").astype(str).str.strip()
        count = int(s.map(lambda x: bool(x) and bool(CJK_RE.search(x))).sum())
        if count > 0:
            out[c] = count
    return out


def collect_non_numeric_values(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    rows = []
    for c in columns:
        s = df[c].fillna("").astype(str).str.strip()
        non_empty = s[s != ""]
        bad = non_empty[~non_empty.str.match(FULL_NUM_RE)]
        if bad.empty:
            continue
        vc = bad.value_counts()
        rows.append(
            {
                "column": c,
                "non_numeric_rows": int(len(bad)),
                "non_numeric_unique": int(bad.nunique()),
                "top_examples": " | ".join([f"{idx} (n={int(cnt)})" for idx, cnt in vc.head(10).items()]),
            }
        )
    if not rows:
        return pd.DataFrame(columns=["column", "non_numeric_rows", "non_numeric_unique", "top_examples"])
    return pd.DataFrame(rows).sort_values(["non_numeric_rows", "column"], ascending=[False, True]).reset_index(drop=True)


def run(input_csv: Path, mapping_csv: Path, output_csv: Path, summary_txt: Path, residual_csv: Path) -> None:
    df = pd.read_csv(input_csv, dtype=str, encoding="utf-8-sig")
    v_cols = [c for c in df.columns if c.startswith("v")]
    rules = build_group_rules(mapping_csv, df.columns)

    cjk_before = count_cjk_columns(df, v_cols)
    non_numeric_before = collect_non_numeric_values(df, v_cols)

    changed_cells_total = 0
    changed_by_col = Counter()
    changed_by_group = Counter()
    mapped_columns = set()

    for rule in rules:
        for col in rule.columns:
            mapped_columns.add(col)
            src = df[col].fillna("").astype(str).str.strip()
            mapped = src.map(lambda x: map_single_value(x, rule))
            changed_mask = src != mapped
            n_changed = int(changed_mask.sum())
            if n_changed > 0:
                changed_cells_total += n_changed
                changed_by_col[col] += n_changed
                changed_by_group[rule.group_id] += n_changed
            df[col] = mapped

    cjk_after = count_cjk_columns(df, v_cols)
    non_numeric_after = collect_non_numeric_values(df, v_cols)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    non_numeric_after.to_csv(residual_csv, index=False, encoding="utf-8-sig")

    unmapped_v_cols = sorted(set(v_cols) - mapped_columns)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with summary_txt.open("w", encoding="utf-8-sig") as f:
        f.write(f"W2 ver4 mapping cleaning summary ({now})\n")
        f.write(f"Input: {input_csv}\n")
        f.write(f"Mapping reference: {mapping_csv}\n")
        f.write(f"Output: {output_csv}\n")
        f.write(f"Residual non-numeric report: {residual_csv}\n\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Columns: {len(df.columns)}\n")
        f.write(f"v* columns: {len(v_cols)}\n")
        f.write(f"Mapped columns (present in file): {len(mapped_columns)}\n")
        f.write(f"Unmapped v* columns: {len(unmapped_v_cols)}\n")
        if unmapped_v_cols:
            f.write("Unmapped v* columns list:\n")
            f.write(", ".join(unmapped_v_cols) + "\n")
        f.write("\n")
        f.write(f"Changed cells total: {changed_cells_total}\n")
        f.write("Changed cells by group:\n")
        for gid, cnt in sorted(changed_by_group.items(), key=lambda x: (-x[1], x[0])):
            f.write(f"- {gid}: {cnt}\n")
        f.write("\n")
        f.write("Top changed columns:\n")
        for col, cnt in changed_by_col.most_common(40):
            f.write(f"- {col}: {cnt}\n")
        f.write("\n")
        f.write(f"v* columns with Chinese text BEFORE: {len(cjk_before)}\n")
        f.write(f"v* columns with Chinese text AFTER: {len(cjk_after)}\n")
        if cjk_after:
            f.write("Columns still containing Chinese text after mapping (column: rows):\n")
            for c, cnt in sorted(cjk_after.items(), key=lambda x: (-x[1], x[0])):
                f.write(f"- {c}: {cnt}\n")
        f.write("\n")
        f.write(f"v* columns with non-numeric values BEFORE: {len(non_numeric_before)}\n")
        f.write(f"v* columns with non-numeric values AFTER: {len(non_numeric_after)}\n")
        f.write("\nDone.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply raw_to_cleaned mapping rules to W2 ver4 and build ver5.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--mapping", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--residual", required=True, type=Path)
    args = parser.parse_args()
    run(args.input, args.mapping, args.output, args.summary, args.residual)


if __name__ == "__main__":
    main()
