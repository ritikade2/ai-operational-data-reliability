"""
llm_interpreter.py
Uses Claude API to interpret the reliability score and generate
an operational recommendation for data engineers and BI teams

The LLM interprets the findings - it does not decide them
The score and verdict are always deterministic.
"""

import anthropic
import json

def interpret(scenario: str, report: dict) -> str:
    agg = report["aggregated"]
    mod = report["modules"]
    score = agg["reliability_score"]
    verdict = agg["verdict"]

    summary = f"""
Scenario: {scenario}
Reliability Score: {score}/100
Verdict: {verdict}

Key Metrics:
- Intent JS distance: {mod["intent_drift"]["js_distance"]} (how different intent distributions are)
- New intents in Period B: {mod["intent_drift"]["new_intent_count"]}
- Confidence KS Statistic: {mod["confidence"]["ks_statistic"]}
- Low confidence rate delta: {mod["confidence"]["low_confidence_delta"]}
- Fallback rate delta: {mod["fallback_rate"]["fallback_rate_delta"]}
- Spike detected: {mod["fallback_rate"]["spike_detected"]}
- Latency delta (ms): {mod["fallback_rate"]["latency_delta_ms"]}
- Intent attempts delta: {mod["fallback_rate"]["attempts_delta"]}
- Intent coverage rate: {mod["bi_readiness"]["intent_coverage_rate"]}
- Transfer rate delta: {mod["bi_readiness"]["transfer_rate_delta"]}
- Turns Delta: {mod["bi_readiness"]["turns_delta"]}
- Channel JS distance: {mod["bi_readiness"]["channel_js_distance"]}
"""
    
    prompt = f"""
You are an AI data reliability analyst helping enterprise data engineering and BI teams.

A reliability framework has evaluated the transition from a rule-based classification to an 
LLM-powered agent system. Here are the results:
{summary}

Write a concise operational interpretation (4-6 sentences) that:
1. States whether the data is safe for BI reporting and why
2. Highlight most concerning signals
3. Gives a concrete recommendation for the data engineering team
4. Uses plain English - no jargons, no bullet points, just clear prose 

Do not repeat the numbers back. Interpret what they mean operationally. 
"""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text 

def run_all(scenarios: list, outputs_dir: str = "outputs") -> None:
    for scenario in scenarios:
        path = f"{outputs_dir}/report_{scenario}.json"
        with open(path, "r") as f:
            report = json.load(f)
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario.upper()}")
        print(f"Score: {report['aggregated']['reliability_score']} — {report['aggregated']['verdict']}")
        print(f"{'-'*60}")

        interpretation = interpret(scenario, report)
        print(interpretation)

        # Save interpretation back into the report
        report["llm_interpretation"] = interpretation
        with open(path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
    print(f"\nInterpretations saved to {outputs_dir}/")


if __name__ == "__main__":
    scenarios = ["baseline", "mild_drift", "moderate_drift", "severe_drift"]
    run_all(scenarios)