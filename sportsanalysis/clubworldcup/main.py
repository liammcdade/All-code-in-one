def fractional_to_probability(fractional_odds):
    """
    Converts fractional odds (e.g., '1/33') to implied probability.
    """
    num, denom = map(int, fractional_odds.split('/'))
    return denom / (num + denom)

def normalize_probabilities(probabilities):
    """
    Normalizes a list of probabilities so they sum to 1.
    """
    total = sum(probabilities)
    return [p / total for p in probabilities]

# Input: update these odds as needed
odds = {
    "Paris Saint-Germain": "1/1000",
    "Draw": "80/1",
    "Real Madrid": "200/1"
}

# Calculate implied probabilities for each outcome
implied_probs = [fractional_to_probability(odds[outcome]) for outcome in odds]

# Normalize probabilities so they sum to 100%
normalized_probs = normalize_probabilities(implied_probs)

# Display results
print("Implied probabilities (normalized):")
for outcome, prob in zip(odds, normalized_probs):
    print(f"{outcome:20}: {prob*100:.3f}%")
