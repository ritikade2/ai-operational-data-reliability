"""
reliability/confidence.py
Detects shifts in model confidence score distributions between periods
Uses:
    - Mean/std comparison
    - KS test for distribution shift
    - Low-confidence rate (score below threshold)
"""

import pandas as pd 
import numpy as np 
from scipy.stats import ks_2samp

CONFIDENCE_THRESHOLD = 0.5

def run(df_a: pd.DataFrame, df_b: pd.DataFrame) -> dict:
    conf_a = df_a["confidence_score"].dropna()
    conf_b = df_b["confidence_score"].dropna()

    mean_a, mean_b = conf_a.mean(), conf_b.mean()
    std_a, std_b = conf_a.std(), conf_b.std()
    ks_stat, ks_pvalue = ks_2samp(conf_a, conf_b)

    low_conf_rate_a = (conf_a < CONFIDENCE_THRESHOLD).mean()
    low_conf_rate_b = (conf_b < CONFIDENCE_THRESHOLD).mean()

    return {
        "module": "confidence", 
        "mean_a": round(float(mean_a), 4),
        "mean_b": round(float(mean_b), 4),
        "mean_delta": round(float(mean_b - mean_a), 4),
        "std_a": round(float(std_a), 4),
        "std_b": round(float(std_b), 4),
        "ks_statistic": round(float(ks_stat), 4),
        "ks_pvalue": round(float(ks_pvalue), 6),
        "significant_shift": bool(ks_pvalue <0.05),
        "low_confidence_rate_a": round(float(low_conf_rate_a), 4),
        "low_confidence_rate_b": round(float(low_conf_rate_b), 4),
        "low_confidence_delta": round(float(low_conf_rate_b - low_conf_rate_a), 4)
    }