"""
reliability/bi_readiness.py
Evaluated whether the AI agent output data is stable enough for business intelligence reporting.
Checks:
    - Intent label coverage (% of Period A intents still present in Period B)
    - Unmapped intent rate (new Period B intents with no Period A equivalent)
    - Resolution rate stability
    - Transfer-to-human rate shift
    - Transfer reason breakdown
    - Channel distribution stability (JS divergence)
    - Avg turns per interaction shift
    - Grain consistency (duplicate session check)
"""

import pandas as pd
from scipy.spatial.distance import jensenshannon
import numpy as np


def run(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    # Intent coverage
    intents_a = set(df_a["intent"].dropna().unique())
    intents_b = set(df_b["intent"].dropna().unique())
    covered = intents_a & intents_b
    coverage_rate = len(covered) / len(intents_a) if intents_a else 1.0
    unmapped = intents_b - intents_a
    unmapped_rate = len(unmapped) / len(intents_b) if intents_b else 0.0

    # Resolution rate
    resolution_a = df_a["resolved"].mean()
    resolution_b = df_b["resolved"].mean()

    # Transfer to human rate
    transfer_a = df_a["transferred_to_human"].mean()
    transfer_b = df_b["transferred_to_human"].mean()

    # Transfer reason breakdown (Period B only)
    transfer_reasons = (
        df_b[df_b["transferred_to_human"] == 1]["transfer_reason"]
        .dropna()
        .value_counts(normalize=True)
        .round(4)
        .to_dict()
    )

    # Channel distribution shifts (Jensen-Shannon divergence)
    chan_a = df_a["channel"].dropna().value_counts(normalize=True).to_dict()
    chan_b = df_b["channel"].dropna().value_counts(normalize=True).to_dict()
    all_channels = sorted(set(chan_a.keys()) | set(chan_b.keys()))
    p = np.array([chan_a.get(c, 0.0) for c in all_channels])
    q = np.array([chan_b.get(c, 0.0) for c in all_channels])
    channel_js = float(jensenshannon(p, q))

    # Turns per interaction shift
    avg_turns_a = df_a["turns"].mean()
    avg_turns_b = df_b["turns"].mean()

    # Grain consistency
    duplicate_a = df_a.duplicated(subset=["session_id"]).mean()
    duplicate_b = df_b.duplicated(subset=["session_id"]).mean()

    return {
        "module":                    "bi_readiness",
        "intent_coverage_rate":      round(float(coverage_rate), 4),
        "unmapped_intent_rate":      round(float(unmapped_rate), 4),
        "unmapped_intents":          sorted(unmapped),
        "covered_intents":           sorted(covered),
        "resolution_rate_a":         round(float(resolution_a), 4),
        "resolution_rate_b":         round(float(resolution_b), 4),
        "resolution_rate_delta":     round(float(resolution_b - resolution_a), 4),
        "transfer_rate_a":           round(float(transfer_a), 4),
        "transfer_rate_b":           round(float(transfer_b), 4),
        "transfer_rate_delta":       round(float(transfer_b - transfer_a), 4),
        "transfer_reasons_period_b": transfer_reasons,
        "channel_js_distance":       round(channel_js, 4),
        "avg_turns_a":               round(float(avg_turns_a), 4),
        "avg_turns_b":               round(float(avg_turns_b), 4),
        "turns_delta":               round(float(avg_turns_b - avg_turns_a), 4),
        "duplicate_session_rate_a":  round(float(duplicate_a), 4),
        "duplicate_session_rate_b":  round(float(duplicate_b), 4),
    }