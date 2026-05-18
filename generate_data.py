"""
generate_data.py
Generates synthetic enterprise AI-agent operational logs for two periods:
  Period A — rule-based classification system (clean, stable intents)
  Period B — LLM-powered agent system (with injected drift)

Four drift scenarios: baseline (0%), mild (10%), moderate (30%), severe (50%)

Columns:
  session_id, timestamp, period, system_type, channel,
  intent, confidence_score, is_fallback, transfer_reason,
  transferred_to_human, turns, raw_input_length,
  intent_attempts, response_latency_ms,
  call_duration_sec, resolved
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

SEED = 42
rng = np.random.default_rng(SEED)

PERIOD_A_INTENTS = [
    "check_balance", "make_payment", "dispute_charge", "update_address",
    "request_statement", "freeze_card", "loan_inquiry", "transfer_funds",
]

PERIOD_B_INTENTS_STABLE = [
    "check_balance", "make_payment", "dispute_charge", "update_address",
    "request_statement", "freeze_card", "loan_inquiry", "transfer_funds",
]

PERIOD_B_INTENTS_DRIFTED = [
    "account_balance_check", "payment_processing", "transaction_dispute",
    "profile_update", "document_request", "card_management",
    "credit_inquiry", "fund_movement", "investment_advice",
    "insurance_claim", "unknown",
]

CHANNELS = ["voice", "chat", "mobile_app"]
CHANNEL_WEIGHTS = [0.55, 0.30, 0.15]

TRANSFER_REASONS = ["low_confidence", "unresolved", "customer_request", "timeout", "none"]


def generate_timestamps(n, start, end):
    start_ts = datetime.strptime(start, "%Y-%m-%d")
    end_ts   = datetime.strptime(end, "%Y-%m-%d")
    delta    = (end_ts - start_ts).total_seconds()
    offsets  = rng.uniform(0, delta, size=n)
    return [start_ts + timedelta(seconds=float(o)) for o in offsets]


def generate_period_a(n=2000):
    """
    Period A: rule-based classification system.
    High confidence, stable intents, low fallback, low transfer rate.
    """
    intents    = rng.choice(PERIOD_A_INTENTS, size=n,
                            p=[0.20, 0.18, 0.12, 0.10, 0.10, 0.10, 0.10, 0.10])
    confidence = rng.beta(8, 2, size=n).round(3)
    is_fallback = (intents == "unknown").astype(int)

    transferred = rng.choice([1, 0], size=n, p=[0.08, 0.92])
    transfer_reason = [
        rng.choice(["unresolved", "customer_request", "timeout", "none"],
                   p=[0.3, 0.4, 0.2, 0.1]) if t == 1 else "none"
        for t in transferred
    ]

    timestamps = generate_timestamps(n, "2023-01-01", "2023-06-30")

    return pd.DataFrame({
        "session_id":          [f"A-{i:05d}" for i in range(n)],
        "timestamp":           timestamps,
        "period":              "A",
        "system_type":         "rule_based",
        "channel":             rng.choice(CHANNELS, size=n, p=CHANNEL_WEIGHTS),
        "intent":              intents,
        "confidence_score":    confidence,
        "intent_attempts":     rng.integers(1, 3, size=n),   # rule-based rarely retries
        "turns":               rng.integers(1, 4, size=n),
        "raw_input_length":    rng.integers(5, 80, size=n),  # words
        "response_latency_ms": rng.integers(100, 800, size=n),
        "is_fallback":         is_fallback,
        "transferred_to_human": transferred,
        "transfer_reason":     transfer_reason,
        "call_duration_sec":   rng.integers(30, 480, size=n),
        "resolved":            rng.choice([1, 0], size=n, p=[0.88, 0.12]),
    })


def generate_period_b(n=2000, drift_pct=0.0):
    """
    Period B: LLM-powered agent system.
    drift_pct controls proportion of drifted records.
    Drifted records have:
      - noisier confidence (beta 3,3)
      - higher fallback rate
      - more intent attempts
      - longer latency
      - higher transfer rate
    """
    n_drifted = int(n * drift_pct)
    n_stable  = n - n_drifted

    # Stable portion
    stable_intents  = rng.choice(PERIOD_B_INTENTS_STABLE, size=n_stable,
                                 p=[0.20, 0.18, 0.12, 0.10, 0.10, 0.10, 0.10, 0.10])
    stable_conf     = rng.beta(8, 2, size=n_stable).round(3)
    stable_attempts = rng.integers(1, 3, size=n_stable)
    stable_latency  = rng.integers(200, 1200, size=n_stable)
    stable_turns    = rng.integers(1, 5, size=n_stable)
    stable_input    = rng.integers(5, 120, size=n_stable)
    stable_transfer = rng.choice([1, 0], size=n_stable, p=[0.10, 0.90])

    # Drifted portion — messier
    drift_weights   = [0.12, 0.12, 0.10, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.10]
    drifted_intents  = rng.choice(PERIOD_B_INTENTS_DRIFTED, size=n_drifted, p=drift_weights)
    drifted_conf     = rng.beta(3, 3, size=n_drifted).round(3)
    drifted_attempts = rng.integers(2, 5, size=n_drifted)   # more retries
    drifted_latency  = rng.integers(800, 3000, size=n_drifted)  # slower
    drifted_turns    = rng.integers(3, 8, size=n_drifted)   # more back-and-forth
    drifted_input    = rng.integers(40, 200, size=n_drifted) # longer inputs
    drifted_transfer = rng.choice([1, 0], size=n_drifted, p=[0.28, 0.72])  # more transfers

    # Concatenate and shuffle
    all_intents  = np.concatenate([stable_intents,  drifted_intents])
    all_conf     = np.concatenate([stable_conf,     drifted_conf])
    all_attempts = np.concatenate([stable_attempts, drifted_attempts])
    all_latency  = np.concatenate([stable_latency,  drifted_latency])
    all_turns    = np.concatenate([stable_turns,    drifted_turns])
    all_input    = np.concatenate([stable_input,    drifted_input])
    all_transfer = np.concatenate([stable_transfer, drifted_transfer])

    idx = rng.permutation(n)
    all_intents  = all_intents[idx]
    all_conf     = all_conf[idx]
    all_attempts = all_attempts[idx]
    all_latency  = all_latency[idx]
    all_turns    = all_turns[idx]
    all_input    = all_input[idx]
    all_transfer = all_transfer[idx]

    is_fallback = (all_intents == "unknown").astype(int)

    transfer_reason = [
        rng.choice(["low_confidence", "unresolved", "customer_request", "timeout"],
                   p=[0.40, 0.30, 0.20, 0.10]) if t == 1 else "none"
        for t in all_transfer
    ]

    timestamps = generate_timestamps(n, "2023-07-01", "2023-12-31")

    return pd.DataFrame({
        "session_id":           [f"B-{i:05d}" for i in range(n)],
        "timestamp":            timestamps,
        "period":               "B",
        "system_type":          "llm_agent",
        "channel":              rng.choice(CHANNELS, size=n, p=CHANNEL_WEIGHTS),
        "intent":               all_intents,
        "confidence_score":     all_conf,
        "intent_attempts":      all_attempts,
        "turns":                all_turns,
        "raw_input_length":     all_input,
        "response_latency_ms":  all_latency,
        "is_fallback":          is_fallback,
        "transferred_to_human": all_transfer,
        "transfer_reason":      transfer_reason,
        "call_duration_sec":    rng.integers(30, 720, size=n),
        "resolved":             rng.choice([1, 0], size=n, p=[0.82, 0.18]),
    })


SCENARIOS = {
    "baseline":      0.00,
    "mild_drift":    0.10,
    "moderate_drift":0.30,
    "severe_drift":  0.50,
}


def main():
    os.makedirs("data", exist_ok=True)

    period_a = generate_period_a(n=2000)
    period_a.to_csv("data/period_a.csv", index=False)
    print(f"Period A: {len(period_a)} records -> data/period_a.csv")
    print(f"  columns: {period_a.columns.tolist()}\n")

    for scenario, drift_pct in SCENARIOS.items():
        period_b = generate_period_b(n=2000, drift_pct=drift_pct)
        path = f"data/period_b_{scenario}.csv"
        period_b.to_csv(path, index=False)
        print(f"Period B ({scenario:15s}, drift={int(drift_pct*100):2d}%): "
              f"{len(period_b)} records -> {path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
