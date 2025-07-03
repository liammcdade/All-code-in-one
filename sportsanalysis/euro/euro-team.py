import pandas as pd
import numpy as np
import os
import time
from pathlib import Path
from typing import List
from sklearn.preprocessing import MinMaxScaler
from tabulate import tabulate
import logging

def main() -> None:
    """Analyze and display normalized squad metrics for Euro 2024 teams with live updates."""
    logging.basicConfig(level=logging.INFO)
    data_path = Path("euro 2024/euro2024-country.csv")
    try:
        df = pd.read_csv(data_path).rename(columns=str.strip)
    except FileNotFoundError:
        logging.error(f"File not found: {data_path}")
        return
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return

    numeric_cols = [
        "Age", "Poss", "MP", "Starts", "Min", "90s", "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt",
        "CrdY", "CrdR", "xG", "npxG", "xAG", "npxG+xAG", "PrgC", "PrgP"
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df = df[df["Min"] > 0].dropna(subset=["Squad"])

    # Derived per-player stats
    for col, new in [
        ("Gls", "Goals_per_90"),
        ("Ast", "Assists_per_90"),
        ("PrgC", "PrgC_per_90"),
        ("PrgP", "PrgP_per_90"),
    ]:
        df[new] = df[col] / (df["Min"] / 90)
    df = df.assign(
        xG_diff=df["Gls"] - df["xG"],
        xGA_diff=df["G+A"] - (df["xG"] + df["xAG"]),
        npxGxAG_per_90=df["npxG+xAG"] / (df["Min"] / 90),
        Discipline=(df["CrdY"] + 2 * df["CrdR"]) / df["Min"],
    )

    # Aggregate per squad
    agg = (
        df.groupby("Squad")
        .agg(
            {
                "Goals_per_90": "mean",
                "Assists_per_90": "mean",
                "xG_diff": "mean",
                "xGA_diff": "mean",
                "npxGxAG_per_90": "mean",
                "Poss": "mean",
                "PrgC_per_90": "mean",
                "PrgP_per_90": "mean",
                "Discipline": "mean",
            }
        )
        .reset_index()
    )

    metrics = agg.columns[1:]  # All except 'Squad'

    # Normalize
    scaler = MinMaxScaler()
    norm = pd.DataFrame(scaler.fit_transform(agg[metrics]), columns=metrics)
    norm["Squad"] = agg["Squad"]
    norm["Discipline"] *= -1  # Lower is better

    # Initialize score tracking
    score_tracker = pd.DataFrame({"Squad": norm["Squad"], "CumulativeScore": 0.0})

    # Live update loop
    for i, w in enumerate(np.arange(0.05, 1.05, 0.05), 1):
        score_tracker["CumulativeScore"] += (norm[metrics] * w).sum(axis=1)
        score_tracker["AvgScore"] = score_tracker["CumulativeScore"] / i

        # Sort and display
        display_df = (
            score_tracker[["Squad", "AvgScore"]]
            .sort_values("AvgScore", ascending=False)
            .reset_index(drop=True)
        )
        os.system("cls" if os.name == "nt" else "clear")
        print(f"🔄 Weight: {w:.2f} | Iteration {i}/20\n")
        print(
            tabulate(
                display_df.head(24), headers="keys", tablefmt="fancy_grid", showindex=True
            )
        )
        time.sleep(0.3)  # Delay for effect; adjust as needed

if __name__ == "__main__":
    main()
