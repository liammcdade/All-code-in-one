import pandas as pd

# --- Config ---
files = {
    "Jannik Sinner": {"file": "sportsanalysis/tennis/sinner.csv", "odds": "1/1"},
    "Carlos Alcaraz": {"file": "sportsanalysis/tennis/alcaraz.csv", "odds": "3/4"}
}
weights_by_year = {
    2025: 1.00,
    2024: 0.90,
    2023: 0.75,
    2022: 0.60,
    2021: 0.45,
    2020: 0.30
}

# Stats columns you want to consider (all percentages and TPW)
metrics = ["Win%", "Set%", "Game%", "TB%", "Hld%", "Brk%", "1st%", "2nd%", "TPW"]

alpha = 0.7  # weighting odds 70%, stats 30%

def fractional_to_implied_prob(fraction):
    num, denom = map(int, fraction.split('/'))
    return round(denom / (num + denom) * 100, 2)

def process_player(path, odds_fraction, player_name):
    df = pd.read_csv(path)

    # Clean data
    df = df[pd.to_numeric(df["Year"], errors="coerce").notnull()]
    df["Year"] = df["Year"].astype(int)
    df = df[df["Year"].isin(weights_by_year.keys())]
    df["Weight"] = df["Year"].map(weights_by_year)

    # Convert percentage strings to floats
    for col in metrics:
        df[col] = df[col].str.rstrip('%').astype(float)

    # Weighted averages per stat
    total_weight = df["Weight"].sum()
    weighted_stats = {col: round((df[col] * df["Weight"]).sum() / total_weight, 2) for col in metrics}

    avg_weighted_stat = round(sum(weighted_stats.values()) / len(weighted_stats), 2)

    odds_prob = fractional_to_implied_prob(odds_fraction)

    # Final blended score
    final_score = round((odds_prob * alpha) + (avg_weighted_stat * (1 - alpha)), 2)

    result = {
        "Player": player_name,
        "Bookmaker Odds": odds_fraction,
        "Implied Odds %": odds_prob,
        "Weighted Stats Score": avg_weighted_stat,
        "Final Match Win %": final_score,
        **weighted_stats
    }
    return result

# Process both players
results = []
for player, info in files.items():
    results.append(process_player(info["file"], info["odds"], player))

# Normalize final scores so they sum to 100%
final_scores = [r["Final Match Win %"] for r in results]
total_final = sum(final_scores)
for r in results:
    r["Final Match Win %"] = round(r["Final Match Win %"] / total_final * 100, 2)

# Output results
output_df = pd.DataFrame(results).set_index("Player")
output_df.to_csv("match_prediction.csv")

print("✅ Match prediction complete. Output saved to match_prediction.csv\n")
print(output_df[["Implied Odds %", "Weighted Stats Score", "Final Match Win %"]])
