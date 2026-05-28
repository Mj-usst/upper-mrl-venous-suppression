#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests


def parse_args():
    p = argparse.ArgumentParser(description="Reader-study statistics with paired differences and Holm-Bonferroni correction.")
    p.add_argument("--ratings-csv", required=True, help="Long CSV with reader_id,case_id,condition and endpoint columns")
    p.add_argument("--condition-a", default="original")
    p.add_argument("--condition-b", default="suppressed")
    p.add_argument("--endpoints", nargs="+", required=True)
    p.add_argument("--output-csv", required=True)
    return p.parse_args()


def paired_summary(df: pd.DataFrame, endpoint: str, a: str, b: str):
    key_cols = ["reader_id", "case_id"]
    wide = df.pivot_table(index=key_cols, columns="condition", values=endpoint, aggfunc="first").dropna()
    if a not in wide.columns or b not in wide.columns:
        raise ValueError(f"Endpoint {endpoint}: missing condition {a} or {b}")
    diff = wide[b] - wide[a]

    # Mixed-effects modeling can be unstable for small public demo data, so the
    # repository reports a robust paired summary plus a paired t-test fallback.
    # For final manuscript analysis, use the institution's validated MRMC script.
    from scipy.stats import ttest_rel, wilcoxon

    t_p = ttest_rel(wide[b], wide[a], nan_policy="omit").pvalue
    try:
        w_p = wilcoxon(wide[b], wide[a]).pvalue
    except Exception:
        w_p = np.nan
    return {
        "endpoint": endpoint,
        "n_pairs": int(len(wide)),
        f"{a}_mean": float(wide[a].mean()),
        f"{b}_mean": float(wide[b].mean()),
        "mean_difference_b_minus_a": float(diff.mean()),
        "median_difference_b_minus_a": float(diff.median()),
        "paired_t_p": float(t_p),
        "wilcoxon_p": float(w_p) if np.isfinite(w_p) else np.nan,
    }


def main():
    args = parse_args()
    df = pd.read_csv(args.ratings_csv)
    rows = [paired_summary(df, ep, args.condition_a, args.condition_b) for ep in args.endpoints]
    out = pd.DataFrame(rows)
    _, p_holm, _, _ = multipletests(out["paired_t_p"].values, method="holm")
    out["paired_t_p_holm"] = p_holm
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(out)


if __name__ == "__main__":
    main()
