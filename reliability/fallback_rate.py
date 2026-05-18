"""
reliability/fallback_rate.py
Tracks unknwon intent and fallback rates across periods. 
A spike in fallback/unknown signals the AI agent 
is encountering queries it cannot classify reliably.
"""

import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

FALLBACK_LABELS   = {"unknown", "fallback", "out_of_scope", "other"}
SPIKE_THRESHOLD   = 0.04
LATENCY_THRESHOLD = 1500


def compute_stats(df: pd.DataFrame) -> dict:
    flag_rate     = df["is_fallback"].mean()
    label_rate    = df["intent"].str.lower().isin(FALLBACK_LABELS).mean()
    combined_rate = df.apply(
        lambda r: r["is_fallback"] == 1 or r["intent"].lower() in FALLBACK_LABELS,
        axis=1
    ).mean()
    avg_attempts  = df["intent_attempts"].mean()
    avg_latency   = df["response_latency_ms"].mean()
    high_latency  = (df["response_latency_ms"] > LATENCY_THRESHOLD).mean()
    transfer_rate = df["transferred_to_human"].mean()
    reason_counts = df["transfer_reason"].value_counts(normalize=True).to_dict()

    return {
        "total_records":           len(df),
        "fallback_flag_rate":      round(float(flag_rate), 4),
        "fallback_label_rate":     round(float(label_rate), 4),
        "combined_fallback_rate":  round(float(combined_rate), 4),
        "avg_intent_attempts":     round(float(avg_attempts), 4),
        "avg_response_latency_ms": round(float(avg_latency), 2),
        "high_latency_rate":       round(float(high_latency), 4),
        "transfer_rate":           round(float(transfer_rate), 4),
        "transfer_reasons":        {k: round(v, 4) for k, v in reason_counts.items()},
    }


def run(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    stats_a = compute_stats(df_a)
    stats_b = compute_stats(df_b)

    delta          = stats_b["combined_fallback_rate"] - stats_a["combined_fallback_rate"]
    latency_delta  = stats_b["avg_response_latency_ms"] - stats_a["avg_response_latency_ms"]
    attempts_delta = stats_b["avg_intent_attempts"] - stats_a["avg_intent_attempts"]

    ks_stat, ks_p = ks_2samp(
        df_a["response_latency_ms"].dropna(),
        df_b["response_latency_ms"].dropna()
    )

    return {
        "module":               "fallback_rate",
        "period_a":             stats_a,
        "period_b":             stats_b,
        "fallback_rate_delta":  round(float(delta), 4),
        "spike_detected":       delta > SPIKE_THRESHOLD,
        "spike_threshold":      SPIKE_THRESHOLD,
        "latency_delta_ms":     round(float(latency_delta), 2),
        "latency_ks_statistic": round(float(ks_stat), 4),
        "latency_ks_pvalue":    round(float(ks_p), 6),
        "attempts_delta":       round(float(attempts_delta), 4),
    }