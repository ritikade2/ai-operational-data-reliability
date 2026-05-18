"""
generate_report.py
This generates a markdown report for each scenario combining deterministic scores and LLM interpretation.
"""

import json
import os

SCENARIOS = ["baseline", "mild_drift", "moderate_drift", "severe_drift"]

VERDICT_BADGE = {
    "Ready": "[READY]",
    "Caution": "[CAUTION]",
    "Not Ready": "[NOT READY]"
}

def generate(scenario: str, outputs_dir: str = "outputs") -> None:
    with open(f"{outputs_dir}/report_{scenario}.json") as f:
        report = json.load(f)

    agg = report["aggregated"]
    mod = report["modules"]
    interp = report.get("llm_interpretation", "_Not yet generated._")
    badge = VERDICT_BADGE.get(agg["verdict"], agg["verdict"])
    md = f"""# Reliability Report - {scenario.replace("_", " ").title()}
## Verdict: {badge} - {agg["reliability_score"]}/100

---

## Component Scores
| Component | Score |
|---|---|
"""
    for k, v in agg["component_scores"].items():
        md += f"| {k.replace('_', ' ').title()} | {v}/100 |\n"

    md += f"""

---

## Intent Drift
| Metric | Value |
|---|---|
| JS Distance | {mod["intent_drift"]["js_distance"]} |
| JS Divergence | {mod["intent_drift"]["js_divergence"]} |
| New Intents | {mod["intent_drift"]["new_intent_count"]} |
| Missing Intents | {mod["intent_drift"]["missing_intent_count"]} |
| Avg Input Length A | {mod["intent_drift"]["avg_input_length_a"]} words |
| Avg Input Length B | {mod["intent_drift"]["avg_input_length_b"]} words |
| Turns Delta | {mod["intent_drift"]["turns_delta"]} |

New intents detected: `{", ".join(mod["intent_drift"]["new_intents"]) or "None"}`

---
## Confidence Shift

| Metric | Value |
|---|---|
| Mean Confidence A | {mod["confidence"]["mean_a"]} |
| Mean Confidence B | {mod["confidence"]["mean_b"]} |
| Mean Delta | {mod["confidence"]["mean_delta"]} |
| KS Statistic | {mod["confidence"]["ks_statistic"]} |
| KS p-value | {mod["confidence"]["ks_pvalue"]} |
| Significant Shift | {mod["confidence"]["significant_shift"]} |
| Low Confidence Rate A | {mod["confidence"]["low_confidence_rate_a"]} |
| Low Confidence Rate B | {mod["confidence"]["low_confidence_rate_b"]} |
| Low Confidence Delta | {mod["confidence"]["low_confidence_delta"]} |

---

## Fallback & Latency

| Metric | Value |
|---|---|
| Fallback Rate Delta | {mod["fallback_rate"]["fallback_rate_delta"]} |
| Spike Detected | {mod["fallback_rate"]["spike_detected"]} |
| Latency Delta (ms) | {mod["fallback_rate"]["latency_delta_ms"]} |
| Latency KS Statistic | {mod["fallback_rate"]["latency_ks_statistic"]} |
| Intent Attempts Delta | {mod["fallback_rate"]["attempts_delta"]} |

---

## BI Readiness

| Metric | Value |
|---|---|
| Intent Coverage Rate | {mod["bi_readiness"]["intent_coverage_rate"]} |
| Unmapped Intent Rate | {mod["bi_readiness"]["unmapped_intent_rate"]} |
| Resolution Rate Delta | {mod["bi_readiness"]["resolution_rate_delta"]} |
| Transfer Rate Delta | {mod["bi_readiness"]["transfer_rate_delta"]} |
| Channel JS Distance | {mod["bi_readiness"]["channel_js_distance"]} |
| Turns Delta | {mod["bi_readiness"]["turns_delta"]} |

Unmapped intents: `{", ".join(mod["bi_readiness"]["unmapped_intents"]) or "None"}`

---

## Operational Interpretation

{interp}
"""

    out_path = f"{outputs_dir}/report_{scenario}.md"
    with open(out_path, "w") as f:
        f.write(md)
    print(f"Report saved: {out_path}")


def main():
    outputs_dir = "outputs"
    for scenario in SCENARIOS:
        generate(scenario, outputs_dir)

if __name__ == "__main__":
    main()