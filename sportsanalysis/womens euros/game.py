"""
Women's Euros Match Odds Analyzer
Converts fractional odds to percentage chance for each outcome.
"""

def fractional_to_probability(fraction):
    num, denom = map(int, fraction.split('/'))
    return denom / (num + denom)

# Odds for Sweden (Women) vs England (Women)
odds = {
    "Sweden": "5/1",
    "Draw": "4/11",
    "England": "4/1"
}

# Calculate implied probabilities
probs = {team: fractional_to_probability(odds_str) for team, odds_str in odds.items()}
total_prob = sum(probs.values())

# Normalize to get actual chance
actual_chances = {team: prob / total_prob for team, prob in probs.items()}


print("Women's Euros: Sweden vs England")


print("\n Chance to Win (%):")
for team, chance in actual_chances.items():
    print(f"  {team:10}: {chance*100:.2f}%")

    # ...existing code...
