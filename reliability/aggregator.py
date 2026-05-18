"""
reliability/aggregator.py
Combines all module results into a single reliability score (0-100)
and a readiness verdict: Ready/ Caution/ Not Ready.
Scoring components and weights:
    - Intent drift (JS distance): 30%
    - Confidence shift (KS statistic): 20%
    - Fallback rate delta: 15%
    - Latency shift (KS statistic): 10%
    - Intent attempts delta: 10%
    - BI readiness (intent coverage rate): 10%
    - Transfer rate delta: 5%
"""

WEIGHTS = {
    "intent_drift": 0.30,
    "confidence": 0.20,
    "fallback_rate": 0.15,
    "latency": 0.10,
    "attempts": 0.10,
    "bi_readiness": 0.20,
    "transfer_rate": 0.05
}

THRESHOLDS = {
    "ready":   80,
    "caution": 50,
}

def score_intent_drift(r: dict) -> float:
    """JS distance 0-1 ==> higher distance = lower score"""
    js = r.get("js_distance", 0.0)
    return max(0.0, 1.0 - (js * 2))  # Scale to [0, 1], with 0.5 JS = 0 score

def score_confidence(r: dict) -> float:
    """KS statistic 0–1 → larger shift = lower score."""
    ks = r.get("ks_statistic", 0.0)
    return max(0.0, 1.0 - (ks * 1.5))

def score_fallback(r: dict) -> float:
    """Fallback rate delta → spike = lower score."""
    delta = r.get("fallback_rate_delta", 0.0)
    return max(0.0, 1.0 - (delta * 10))


def score_latency(r: dict) -> float:
    """Latency KS statistic → large shift = lower score."""
    ks = r.get("latency_ks_statistic", 0.0)
    return max(0.0, 1.0 - (ks * 1.5))


def score_attempts(r: dict) -> float:
    """Intent attempts delta → more retries = lower score."""
    delta = r.get("attempts_delta", 0.0)
    return max(0.0, 1.0 - (delta * 0.5))


def score_bi_readiness(r: dict) -> float:
    """Intent coverage rate directly → lower coverage = lower score."""
    return r.get("intent_coverage_rate", 1.0)


def score_transfer(r: dict) -> float:
    """Transfer rate delta → more transfers = lower score."""
    delta = r.get("transfer_rate_delta", 0.0)
    return max(0.0, 1.0 - (delta * 5))


def aggregate(intent_drift, confidence, fallback_rate, bi_readiness) -> dict:
    component_scores = {
        "intent_drift":  score_intent_drift(intent_drift),
        "confidence":    score_confidence(confidence),
        "fallback_rate": score_fallback(fallback_rate),
        "latency":       score_latency(fallback_rate),
        "attempts":      score_attempts(fallback_rate),
        "bi_readiness":  score_bi_readiness(bi_readiness),
        "transfer_rate": score_transfer(bi_readiness),
    }

    weighted = sum(
        component_scores[k] * WEIGHTS[k]
        for k in component_scores
    )
    score = min(100.0, round(weighted * 100, 1)) # capping score to 100

    if score >= THRESHOLDS["ready"]:
        verdict = "Ready"
    elif score >= THRESHOLDS["caution"]:
        verdict = "Caution"
    else:
        verdict = "Not Ready"

    return {
        "reliability_score": score,
        "verdict":           verdict,
        "component_scores":  {k: round(v * 100, 1) for k, v in component_scores.items()},
        "weights":           WEIGHTS,
        "thresholds":        THRESHOLDS,
    }
