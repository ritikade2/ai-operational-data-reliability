# Reliability Report - Moderate Drift
## Verdict: [CAUTION] - 65.1/100

---

## Component Scores
| Component | Score |
|---|---|
| Intent Drift | 31.3/100 |
| Confidence | 68.4/100 |
| Fallback Rate | 66.0/100 |
| Latency | 14.3/100 |
| Attempts | 76.9/100 |
| Bi Readiness | 100.0/100 |
| Transfer Rate | 60.2/100 |


---

## Intent Drift
| Metric | Value |
|---|---|
| JS Distance | 0.3435 |
| JS Divergence | 0.118 |
| New Intents | 11 |
| Missing Intents | 0 |
| Avg Input Length A | 41.29 words |
| Avg Input Length B | 79.75 words |
| Turns Delta | 1.2435 |

New intents detected: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---
## Confidence Shift

| Metric | Value |
|---|---|
| Mean Confidence A | 0.8022 |
| Mean Confidence B | 0.7119 |
| Mean Delta | -0.0902 |
| KS Statistic | 0.2105 |
| KS p-value | 0.0 |
| Significant Shift | True |
| Low Confidence Rate A | 0.018 |
| Low Confidence Rate B | 0.1585 |
| Low Confidence Delta | 0.1405 |

---

## Fallback & Latency

| Metric | Value |
|---|---|
| Fallback Rate Delta | 0.034 |
| Spike Detected | False |
| Latency Delta (ms) | 594.67 |
| Latency KS Statistic | 0.5715 |
| Intent Attempts Delta | 0.4615 |

---

## BI Readiness

| Metric | Value |
|---|---|
| Intent Coverage Rate | 1.0 |
| Unmapped Intent Rate | 0.5789 |
| Resolution Rate Delta | -0.082 |
| Transfer Rate Delta | 0.0795 |
| Channel JS Distance | 0.0116 |
| Turns Delta | 1.2435 |

Unmapped intents: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---

## Operational Interpretation

# Operational Interpretation: LLM Agent Transition Review

The data is **not yet safe for BI reporting** in its current state because the moderate reliability score reflects meaningful shifts in system behavior that could skew business metrics and stakeholder decisions. The most concerning signals are the substantial increase in low-confidence predictions and the emergence of eleven new intent categories that weren't present before—these suggest the LLM is either encountering genuinely novel user patterns or struggling with consistency compared to the rule-based system. The latency spike is also operationally significant, as it may impact user experience and downstream SLA compliance. We recommend the data engineering team implement a quarantine period where LLM classifications are logged in parallel with the legacy rule-based system for the same requests, enabling direct side-by-side validation before committing to BI reporting. Once you've manually reviewed a representative sample of the new intents and confirmed that confidence scores correlate with actual accuracy, you can safely promote this data for business consumption with appropriate caveats about the transition period.
