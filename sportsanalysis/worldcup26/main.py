# World Cup winner fractional odds
fractional_odds = {
    'Spain': 11/2,
    'England': 13/2,
    'France': 13/2,
    'Brazil': 7/1,
    'Argentina': 8/1,
    'Germany': 9/1,
    'Portugal': 14/1,
    'Netherlands': 20/1,
    'Italy': 25/1,
    'Uruguay': 25/1,
    'Colombia': 33/1,
    'USA': 33/1,
    'Belgium': 40/1,
    'Mexico': 50/1,
    'Croatia': 66/1,
    'Morocco': 66/1,
    'Switzerland': 66/1,
    'Algeria': 100/1,
    'Austria': 100/1,
    'Canada': 100/1,
    'Denmark': 100/1,
    'Japan': 100/1,
    'Norway': 100/1,
    'Senegal': 100/1,
    'Sweden': 100/1,
    'Turkey': 100/1,
    'Chile': 150/1,
    'Ecuador': 150/1,
    'Egypt': 150/1,
    'Ivory Coast': 150/1,
    'Nigeria': 150/1,
    'Serbia': 150/1,
    'South Korea': 150/1,
    'Czech Republic': 200/1,
    'Ghana': 200/1,
    'Hungary': 200/1,
    'Paraguay': 200/1,
    'Peru': 200/1,
    'Bosnia & Herzegovina': 250/1,
    'Cameroon': 250/1,
    'Greece': 250/1,
    'Poland': 250/1,
    'Romania': 250/1,
    'Scotland': 250/1,
    'Slovakia': 250/1,
    'Ukraine': 250/1,
    'Australia': 500/1,
    'Iran': 500/1,
    'New Zealand': 500/1,
    'Northern Ireland': 500/1,
    'Republic of Ireland': 500/1,
    'Saudi Arabia': 500/1,
    'South Africa': 500/1,
    'Tunisia': 500/1,
    'Uzbekistan': 500/1,
    'Venezuela': 500/1,
    'Wales': 500/1,
    'Jordan': 1000/1
}

# Convert fractional odds to implied probabilities
def implied_probability(odd):
    return 1 / (odd + 1)

# Calculate implied probabilities
implied_probs = {team: implied_probability(odd) for team, odd in fractional_odds.items()}

# Normalize to sum to 1
total = sum(implied_probs.values())
normalized_probs = {team: prob / total for team, prob in implied_probs.items()}

# Sort by highest probability
normalized_probs_sorted = dict(sorted(normalized_probs.items(), key=lambda item: item[1], reverse=True))

# Output in percentage format
for team, prob in normalized_probs_sorted.items():
    print(f"{team}: {prob:.4f} ({prob * 100:.2f}%)")
