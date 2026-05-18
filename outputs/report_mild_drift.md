# Reliability Report - Mild Drift
## Verdict: [READY] - 85.2/100

---

## Component Scores
| Component | Score |
|---|---|
| Intent Drift | 61.6/100 |
| Confidence | 88.5/100 |
| Fallback Rate | 84.5/100 |
| Latency | 29.0/100 |
| Attempts | 93.3/100 |
| Bi Readiness | 100.0/100 |
| Transfer Rate | 82.5/100 |


---

## Intent Drift
| Metric | Value |
|---|---|
| JS Distance | 0.1921 |
| JS Divergence | 0.0369 |
| New Intents | 11 |
| Missing Intents | 0 |
| Avg Input Length A | 41.29 words |
| Avg Input Length B | 68.86 words |
| Turns Delta | 0.783 |

New intents detected: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---
## Confidence Shift

| Metric | Value |
|---|---|
| Mean Confidence A | 0.8022 |
| Mean Confidence B | 0.7712 |
| Mean Delta | -0.031 |
| KS Statistic | 0.0765 |
| KS p-value | 1.6e-05 |
| Significant Shift | True |
| Low Confidence Rate A | 0.018 |
| Low Confidence Rate B | 0.0685 |
| Low Confidence Delta | 0.0505 |

---

## Fallback & Latency

| Metric | Value |
|---|---|
| Fallback Rate Delta | 0.0155 |
| Spike Detected | False |
| Latency Delta (ms) | 373.81 |
| Latency KS Statistic | 0.473 |
| Intent Attempts Delta | 0.1335 |

---

## BI Readiness

| Metric | Value |
|---|---|
| Intent Coverage Rate | 1.0 |
| Unmapped Intent Rate | 0.5789 |
| Resolution Rate Delta | -0.079 |
| Transfer Rate Delta | 0.035 |
| Channel JS Distance | 0.0199 |
| Turns Delta | 0.783 |

Unmapped intents: `account_balance_check, card_management, credit_inquiry, document_request, fund_movement, insurance_claim, investment_advice, payment_processing, profile_update, transaction_dispute, unknown`

---

## Operational Interpretation

# Operational Interpretation: LLM Agent Migration Assessment

The data is safe for BI reporting with appropriate monitoring in place, as the system demonstrates stable core performance across channels and maintains complete intent coverage despite the transition. The most concerning signal is the significant latency increase, which suggests the LLM agent requires substantially more processing time than the rule-based system—this could impact user experience if not addressed and should be tracked closely in production. Additionally, the moderate shift in intent distributions and introduction of new intents indicate the agent is classifying requests somewhat differently than before, which warrants validation that these new classifications are accurate rather than artifacts of the model. We recommend the data engineering team establish a real-time alerting dashboard that flags any sudden jumps in low-confidence predictions or fallback rates beyond current levels, and conduct a focused audit comparing the LLM's intent classifications against ground truth labels for the 11 new intent categories to ensure quality hasn't degraded in exchange for coverage.
