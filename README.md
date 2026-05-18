# AI Operational Data Reliability

A monitoring framework that evaluates whether AI-generated operational data is reliable enough for enterprise analytics and BI reporting.
    
## The Problem

Enterprises are rapidly replacing rule-based classification systems with LLM-powered agents. 
When this happens, the structure and meaning of operal data changes. The intent labels shift, confidence scores degrade, fallback rates spike, and response latency increases. Without a systematic way to detect this drift, BI dashboards and downstream analytics become unreliable. 

This framework detects when AI-agent output data has drifted enough to be untrustworthy for reporting, i.e. before bad data reaches decision-makers.

## How it works

The framework evaluates four reliability dimensions:
| Module | What it measures |
|---|---|
| Intent Drift | Jensen-Shannon divergence between intent distributions, new/missing intent detection, input length shift (KS test), average turns per interaction delta |
| Confidence Shift | KS test on confidence score distributions, mean and std delta, low-confidence rate shift, statistical significance (p-value) |
| Fallback & Latency | Fallback rate delta, spike detection, response latency shift (KS test), high-latency rate, intent attempts delta, transfer reason breakdown |
| BI Readiness | Intent label coverage rate, unmapped intent rate, resolution rate delta, transfer-to-human rate shift, channel distribution stability (JS divergence), turns delta, grain consistency (duplicate session check) |

Each module produces a component score. An aggregator combines them into a single **Reliability Score (0-100)** and a verdict:

- `[READY]` — Safe for BI reporting
- `[CAUTION]` — Proceed with validation controls
- `[NOT READY]` — Do not use for reporting until drift is resolved

An LLM interpretation layer then explains the score in natural language with concrete recommendations for the data engineering team.

## Results
Evaluated across four controlled drift scenarios on synthetic enterprise data and validated on the public BANKING77 dataset (~10K records, 77 intents).

### Synthetic Data

| Scenario | Injected Drift | Reliability Score | JS Distance | KS Statistic | Verdict |
|---|---|---|---|---|---|
| Baseline | 0% | 100.0 | 0.033 | 0.022 | [READY] |
| Mild | 10% | 85.2 | 0.192 | 0.077 | [READY] |
| Moderate | 30% | 65.1 | 0.344 | 0.211 | [CAUTION] |
| Severe | 50% | 49.1 | 0.465 | 0.328 | [NOT READY] |

### BANKING77 Validation

| Scenario | Masked Intents | JS Distance | JS Divergence |
|---|---|---|---|
| Baseline | 0% | 0.074 | 0.005 |
| Mild | 10% | 0.253 | 0.064 |
| Moderate | 30% | 0.472 | 0.223 |
| Severe | 50% | 0.590 | 0.348 |

All metrics increase monotonically with injected drift across both datasets, confirming the framework reliabily detects and grades drift severity.

## Project Structure
```
ai-operational-data-reliability/
├── generate_data.py          # synthetic enterprise logs, 4 drift scenarios
├── build_db.py               # load CSVs into DuckDB
├── main.py                   # orchestrator, runs all modules
├── llm_interpreter.py        # Claude/OpenAI interprets the reliability score
├── generate_report.py        # generates markdown reports per scenario
├── validate_banking77.py     # validates intent drift on public dataset
├── reliability/
│   ├── intent_drift.py       # Jensen-Shannon divergence
│   ├── confidence.py         # KS test on confidence distributions
│   ├── fallback_rate.py      # fallback spike, latency, intent attempts
│   ├── bi_readiness.py       # coverage, transfer rate, channel stability
│   └── aggregator.py         # weighted reliability score + verdict
├── data/                     # generated CSV files and DuckDB
└── outputs/                  # JSON reports, markdown reports, summary CSV
```
## Setup

```bash
git clone https://github.com/ritikade2/ai-operational-data-reliability
cd ai-operational-data-reliability
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

```bash
# Generate synthetic data
python3 generate_data.py

# Load into DuckDB
python3 build_db.py

# Run reliability framework
python3 main.py

# Generate LLM interpretations
python3 llm_interpreter.py

# Generate markdown reports
python3 generate_report.py

# Validate on BANKING77
python3 validate_banking77.py
```

## Tech Stack

- Python, pandas, numpy
- scipy (Jensen-Shannon divergence, KS test)
- DuckDB
- scikit-learn
- Anthropic Claude API (LLM interpretation layer)
- BANKING77 (public validation dataset)

## Use Cases

This framework applies to any enterprise migrating operational systems
to AI agents, including:

- Banking and financial services virtual assistants
- Insurance claims and support agents
- Healthcare scheduling and triage agents
- Retail and e-commerce support agents
- Internal BI copilots and analytics assistants

## License

MIT

