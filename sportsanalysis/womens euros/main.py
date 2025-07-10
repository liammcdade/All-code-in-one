# Input fractional odds
fractional_odds = {
    'Spain Women': 10/11,
    'England Women': 5/1,
    'France Women': 5/1,
    'Germany Women': 7/1,
    'Sweden Women': 14/1,
    'Norway Women': 25/1,
    'Italy Women': 33/1,
    'Switzerland Women': 50/1,
    'Netherlands Women': 100/1,
    'Portugal Women': 500/1,
    'Wales Women': 2000/1
}

# Convert fractional odds to implied probabilities
def implied_probability(odd):
    return 1 / (odd + 1)

# Calculate and normalize
implied_probs = {team: implied_probability(odd) for team, odd in fractional_odds.items()}
total = sum(implied_probs.values())
normalized_probs = {team: prob / total for team, prob in implied_probs.items()}

print("\nWomens Euros 2025 Title Probabilities (normalized):")

# Output
for team, prob in normalized_probs.items():
    print(f"{team}: {prob:.4f} ({prob * 100:.2f}%)")
