"""
validate_banking77.py
Validates the intent drift module on BANKING77 public dataset.
BANKING&& contains ~13K banking queries across 77 intent categories.

The drift is simulated by splitting the dataset into 2 halves and 
progressively masking intent categories to mimin real-world drift.

This validates that the JS divergence metric generalized beyond 
synthetic data to a real-world financial-intent dataset.
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
from reliability import intent_drift

SEED = 42
rng  = np.random.default_rng(SEED)


def load_banking77() -> pd.DataFrame:
    print("Loading BANKING77 dataset...")
    ds = load_dataset("legacy-datasets/banking77", split="train")
    df = ds.to_pandas()
    df.columns = ["text", "label"]

    label_names = ds.features["label"].names
    df["intent"] = df["label"].apply(lambda x: label_names[x])
    df["raw_input_length"] = df["text"].str.split().str.len()
    df["turns"] = 1
    return df


def make_split(df: pd.DataFrame, mask_pct: float = 0.0) -> tuple:
    """
    Split into 2 halves (Period A and Period B).
    mask_pct: proportion of intents in Period B to replace with 'unknown'
    to simulate drift.
    """
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    mid  = len(df) // 2
    df_a = df.iloc[:mid].copy()
    df_b = df.iloc[mid:].copy()

    if mask_pct > 0:
        intents_b    = df_b["intent"].unique()
        n_mask       = int(len(intents_b) * mask_pct)
        mask_intents = rng.choice(intents_b, size=n_mask, replace=False)
        df_b.loc[df_b["intent"].isin(mask_intents), "intent"] = "unknown"

    return df_a, df_b


def main():
    df = load_banking77()
    print(f"Loaded {len(df)} records, {df['intent'].nunique()} unique intents\n")

    scenarios = {
        "baseline":       0.00,
        "mild_drift":     0.10,
        "moderate_drift": 0.30,
        "severe_drift":   0.50,
    }

    rows = []
    for scenario, mask_pct in scenarios.items(): 
        df_a, df_b = make_split(df, mask_pct=mask_pct)
        result     = intent_drift.run(df_a, df_b)

        rows.append({ 
            "scenario":       scenario,
            "masked_intents": f"{int(mask_pct*100)}%",
            "js_distance":    result["js_distance"],
            "js_divergence":  result["js_divergence"],
            "new_intents":    result["new_intent_count"],
            "missing_intents":result["missing_intent_count"],
            "turns_delta":    result["turns_delta"],
        })

    
    df_results = pd.DataFrame(rows)
    print("=== BANKING77 Validation — Intent Drift Results ===\n")
    print(df_results.to_string(index=False))

    df_results.to_csv("outputs/banking77_validation.csv", index=False)
    print("\nSaved to outputs/banking77_validation.csv")


if __name__ == "__main__":
    main()
