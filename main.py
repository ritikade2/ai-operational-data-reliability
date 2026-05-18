"""
main.py
Orchestrator - runs all reliability modules across all drift scenarios
and produces a summary table + pre-scenario JSON report
"""

import json
import os
import pandas as pd
from reliability import intent_drift, confidence, fallback_rate, bi_readiness, aggregator

SCENARIOS = ["baseline", "mild_drift", "moderate_drift", "severe_drift"]

def load_data(scenario: str) -> tuple:
    df_a = pd.read_csv("data/period_a.csv")
    df_b = pd.read_csv(f"data/period_b_{scenario}.csv")
    return df_a, df_b

def run_scenario(scenario: str) -> dict:
    df_a, df_b = load_data(scenario)

    r_intent   = intent_drift.run(df_a, df_b)
    r_conf     = confidence.run(df_a, df_b)
    r_fallback = fallback_rate.run(df_a, df_b)
    r_bi       = bi_readiness.run(df_a, df_b)
    r_agg      = aggregator.aggregate(r_intent, r_conf, r_fallback, r_bi)

    return {
        "scenario":   scenario,
        "aggregated": r_agg,
        "modules": {
            "intent_drift":  r_intent,
            "confidence":    r_conf,
            "fallback_rate": r_fallback,
            "bi_readiness":  r_bi,
        }
    }

def main():
    os.makedirs("outputs", exist_ok=True)
    summary_rows = []

    for scenario in SCENARIOS:
        result = run_scenario(scenario)

        out_path = f"outputs/report_{scenario}.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, default=str)

        agg = result["aggregated"]
        mod = result["modules"]

        summary_rows.append({
            "scenario": scenario,
            "reliability_score": agg["reliability_score"],
            "verdict": agg["verdict"],
            # intent drift
            "js_distance": mod["intent_drift"]["js_distance"],
            "new_intents": mod["intent_drift"]["new_intent_count"],
            "turns_delta": mod["bi_readiness"]["turns_delta"],
            # confidence
            "ks_statistic": mod["confidence"]["ks_statistic"],
            "mean_conf_delta": mod["confidence"]["mean_delta"],
            "low_conf_delta": mod["confidence"]["low_confidence_delta"],
            # fallback
            "fallback_delta": mod["fallback_rate"]["fallback_rate_delta"],
            "spike_detected": mod["fallback_rate"]["spike_detected"],
            "latency_delta_ms": mod["fallback_rate"]["latency_delta_ms"],
            "attempts_delta": mod["fallback_rate"]["attempts_delta"],
            # bi readiness
            "intent_coverage": mod["bi_readiness"]["intent_coverage_rate"],
            "transfer_delta": mod["bi_readiness"]["transfer_rate_delta"],
            "channel_js": mod["bi_readiness"]["channel_js_distance"],
        })

    df_summary = pd.DataFrame(summary_rows)

    print("\n=== AI Operational Data Reliability — Results Summary ===\n")
    print(df_summary.to_string(index=False))

    df_summary.to_csv("outputs/summary.csv", index=False)
    print("\nFull reports saved to outputs/")

if __name__ == "__main__":
    main()