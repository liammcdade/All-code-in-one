# --- Wimbledon 2025 Men's Winner Odds (fractional format) ---
wimbledon_odds = {
    "Carlos Alcaraz": "4/5",
    "Jannik Sinner": "2/1",
    "Novak Djokovic": "9/2",
    "Taylor Fritz": "16/1"
}

def fractional_to_probability(fraction):
    num, denom = map(int, fraction.split('/'))
    return denom / (num + denom)

# --- Implied probabilities ---
implied_probs = {player: fractional_to_probability(odds) for player, odds in wimbledon_odds.items()}

# --- Normalize to sum to 100% ---
total_prob = sum(implied_probs.values())
normalized_probs = {player: prob / total_prob for player, prob in implied_probs.items()}

print("Wimbledon 2025 Men's Title Probabilities (normalized):")
for player, prob in sorted(normalized_probs.items(), key=lambda x: x[1], reverse=True):
    print(f"{player:20}: {prob * 100:.2f}%")
