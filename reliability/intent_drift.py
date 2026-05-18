"""
reliability/itnent_drift.py
Measures intent taxanomy drift between Period A and Period using Jensen-Shannon divergence.

All tracks raw input length shift and turns delta.
"""


import pandas as pd 
import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.stats import ks_2samp

def compute_distribution(series: pd.Series) -> dict:
    return series.dropna().value_counts(normalize=True).to_dict()


def align_distributions(dist_a: dict, dist_b: dict) -> tuple:
    all_intents = sorted(set(dist_a.keys()) | set(dist_b.keys()))
    p = np.array([dist_a.get(i, 0.0) for i in all_intents])
    q = np.array([dist_b.get(i, 0.0) for i in all_intents])
    return p, q, all_intents


def run(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    dist_a = compute_distribution(df_a["intent"])
    dist_b = compute_distribution(df_b["intent"])

    p, q, vocab   = align_distributions(dist_a, dist_b)
    js_distance   = float(jensenshannon(p, q))
    js_divergence = js_distance ** 2

    new_intents     = set(dist_b.keys()) - set(dist_a.keys())
    missing_intents = set(dist_a.keys()) - set(dist_b.keys())

    # Input length shift
    ks_stat, ks_p = ks_2samp(
        df_a["raw_input_length"].dropna(),
        df_b["raw_input_length"].dropna()
    )
    avg_input_a = df_a["raw_input_length"].mean()
    avg_input_b = df_b["raw_input_length"].mean()

    # Turns shift
    avg_turns_a = df_a["turns"].mean()
    avg_turns_b = df_b["turns"].mean()

    return {
        "module":                 "intent_drift",
        "js_distance":            round(js_distance, 4),
        "js_divergence":          round(js_divergence, 4),
        "vocab_size_a":           len(dist_a),
        "vocab_size_b":           len(dist_b),
        "new_intents":            sorted(new_intents),
        "missing_intents":        sorted(missing_intents),
        "new_intent_count":       len(new_intents),
        "missing_intent_count":   len(missing_intents),
        "avg_input_length_a":     round(float(avg_input_a), 2),
        "avg_input_length_b":     round(float(avg_input_b), 2),
        "input_length_ks_stat":   round(float(ks_stat), 4),
        "input_length_ks_pvalue": round(float(ks_p), 6),
        "avg_turns_a":            round(float(avg_turns_a), 4),
        "avg_turns_b":            round(float(avg_turns_b), 4),
        "turns_delta":            round(float(avg_turns_b - avg_turns_a), 4),
    }