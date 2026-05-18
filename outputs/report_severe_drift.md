# Reliability Report - Severe Drift
## Verdict: [NOT READY] - 49.1/100

---

## Component Scores
| Component | Score |
|---|---|
| Intent Drift | 6.9/100 |
| Confidence | 50.8/100 |
| Fallback Rate | 54.0/100 |
| Latency | 0.0/100 |
| Attempts | 64.5/100 |
| Bi Readiness | 100.0/100 |
| Transfer Rate | 45.5/100 |


---

## Intent Drift
| Metric | Value |
|---|---|
| JS Distance | 0.4654 |
| JS Divergence | 0.2166 |
| New Intents | 11 |
| Missing Intents | 0 |
| Avg Input Length A | 41.29 words |
| Avg Input Length B | 91.25 words |
| Turns Delta | 1.739 |

New intents detected: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---
## Confidence Shift

| Metric | Value |
|---|---|
| Mean Confidence A | 0.8022 |
| Mean Confidence B | 0.6516 |
| Mean Delta | -0.1506 |
| KS Statistic | 0.328 |
| KS p-value | 0.0 |
| Significant Shift | True |
| Low Confidence Rate A | 0.018 |
| Low Confidence Rate B | 0.268 |
| Low Confidence Delta | 0.25 |

---

## Fallback & Latency

| Metric | Value |
|---|---|
| Fallback Rate Delta | 0.046 |
| Spike Detected | True |
| Latency Delta (ms) | 842.72 |
| Latency KS Statistic | 0.706 |
| Intent Attempts Delta | 0.7095 |

---

## BI Readiness

| Metric | Value |
|---|---|
| Intent Coverage Rate | 1.0 |
| Unmapped Intent Rate | 0.5789 |
| Resolution Rate Delta | -0.074 |
| Transfer Rate Delta | 0.109 |
| Channel JS Distance | 0.0145 |
| Turns Delta | 1.739 |

Unmapped intents: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---

## Operational Interpretation

# Operational Interpretation

The data is **not safe for BI reporting** in its current state because the LLM system is exhibiting fundamental behavioral shifts that make historical comparisons unreliable. The most alarming signals are the significant drift in intent distributions and the emergence of new intent categories that didn't exist before, suggesting the model is responding to different types of requests than it did previously. Combined with a sharp increase in low-confidence predictions and conversation length, this indicates the system is struggling with the new input patterns and may be producing unreliable outputs that would poison downstream analytics.

The data engineering team should immediately pause aggregation of Period B metrics into any existing BI dashboards and instead run a manual audit of a representative sample of the new intent classifications to validate accuracy. Once the root cause of the behavioral shift is identified—whether it's a model update, input distribution change, or prompt modification—establish a quarantine period where LLM classifications are logged separately before being reconciled with the rule-based system for reporting purposes.
