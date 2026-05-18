# Reliability Report - Baseline
## Verdict: [READY] - 100.0/100

---

## Component Scores
| Component | Score |
|---|---|
| Intent Drift | 93.4/100 |
| Confidence | 96.7/100 |
| Fallback Rate | 100.0/100 |
| Latency | 41.9/100 |
| Attempts | 99.9/100 |
| Bi Readiness | 100.0/100 |
| Transfer Rate | 85.2/100 |


---

## Intent Drift
| Metric | Value |
|---|---|
| JS Distance | 0.0328 |
| JS Divergence | 0.0011 |
| New Intents | 0 |
| Missing Intents | 0 |
| Avg Input Length A | 41.29 words |
| Avg Input Length B | 62.64 words |
| Turns Delta | 0.5075 |

New intents detected: `None`

---
## Confidence Shift

| Metric | Value |
|---|---|
| Mean Confidence A | 0.8022 |
| Mean Confidence B | 0.8003 |
| Mean Delta | -0.0019 |
| KS Statistic | 0.022 |
| KS p-value | 0.718514 |
| Significant Shift | False |
| Low Confidence Rate A | 0.018 |
| Low Confidence Rate B | 0.0235 |
| Low Confidence Delta | 0.0055 |

---

## Fallback & Latency

| Metric | Value |
|---|---|
| Fallback Rate Delta | 0.0 |
| Spike Detected | False |
| Latency Delta (ms) | 234.84 |
| Latency KS Statistic | 0.387 |
| Intent Attempts Delta | 0.0015 |

---

## BI Readiness

| Metric | Value |
|---|---|
| Intent Coverage Rate | 1.0 |
| Unmapped Intent Rate | 0.0 |
| Resolution Rate Delta | -0.0675 |
| Transfer Rate Delta | 0.0295 |
| Channel JS Distance | 0.0202 |
| Turns Delta | 0.5075 |

Unmapped intents: `None`

---

## Operational Interpretation

# Operational Interpretation

The data is safe for BI reporting at this time. The baseline scenario shows excellent stability across all critical dimensions, with intent distributions, confidence levels, and system behavior remaining virtually unchanged between periods. The most concerning signal is the notable increase in latency, which adds roughly a quarter-second to each interaction—this won't break functionality but could accumulate into user experience issues at scale. The slight uptick in conversation turns suggests the LLM agent may require more back-and-forth exchanges than the rule-based system, which warrants monitoring to ensure this doesn't become a pattern. The data engineering team should establish a baseline latency threshold now (around 235ms above current) and implement alerts if it grows further, while also tracking whether multi-turn conversations are driven by legitimate complexity or reflect degraded first-pass accuracy. Continue monitoring these metrics weekly to catch any drift before it impacts downstream analytics.
