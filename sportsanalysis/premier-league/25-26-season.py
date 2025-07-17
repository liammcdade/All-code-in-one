def fractional_to_probability(fraction):
    num, denom = map(int, fraction.split('/'))
    return denom / (num + denom)

# --- Title Odds ---
premier_league_odds = {
    "Liverpool": "11/5", "Arsenal": "9/4", "Manchester City": "11/4", "Chelsea": "15/2",
    "Newcastle United": "28/1", "Manchester United": "33/1", "Tottenham": "50/1",
    "Aston Villa": "66/1", "Nottingham Forest": "200/1", "AFC Bournemouth": "250/1",
    "Brighton": "250/1", "Everton": "250/1", "Brentford": "500/1", "Crystal Palace": "500/1",
    "Fulham": "500/1", "West Ham United": "500/1", "Wolverhampton Wanderers": "500/1",
    "Leeds United": "750/1", "Burnley": "1000/1", "Sunderland": "1000/1"
}

# --- Top 4 Odds ---
top4_odds = {
    "Liverpool": "1/6", "Arsenal": "1/5", "Manchester City": "2/9", "Newcastle United": "6/5",
    "Chelsea": "6/4", "Aston Villa": "7/2", "Manchester United": "9/2", "Tottenham": "5/1",
    "Brighton": "12/1", "Nottingham Forest": "20/1", "AFC Bournemouth": "25/1",
    "Crystal Palace": "25/1", "Everton": "25/1", "Fulham": "33/1", "West Ham United": "33/1",
    "Brentford": "40/1", "Wolverhampton Wanderers": "50/1", "Leeds United": "100/1",
    "Burnley": "150/1", "Sunderland": "200/1"
}

# --- Top 6 Odds ---
top6_odds = {
    "Liverpool": "1/16", "Arsenal": "1/12", "Manchester City": "1/12", "Chelsea": "2/9",
    "Newcastle United": "1/2", "Manchester United": "6/5", "Aston Villa": "11/8",
    "Tottenham": "6/4", "Brighton": "5/1", "Nottingham Forest": "8/1",
    "AFC Bournemouth": "9/1", "Crystal Palace": "9/1", "Everton": "10/1",
    "Fulham": "11/1", "West Ham United": "12/1", "Brentford": "16/1",
    "Wolverhampton Wanderers": "20/1", "Leeds United": "33/1", "Burnley": "66/1",
    "Sunderland": "80/1"
}

# --- Title Probabilities (normalized) ---
title_probs = {team: fractional_to_probability(odds) for team, odds in premier_league_odds.items()}
title_total = sum(title_probs.values())
title_normalized = {team: prob / title_total for team, prob in title_probs.items()}
title_sorted = sorted(title_normalized.items(), key=lambda x: x[1], reverse=True)

print("\nPremier League title probabilities (normalized):")
for team, prob in title_sorted:
    print(f"{team:25}: {prob*100:.2f}%")

# --- Top 4 Most Likely (sorted and joint probability) ---
top4_probs = {team: fractional_to_probability(odds) for team, odds in top4_odds.items()}
top4_sorted = sorted(top4_probs.items(), key=lambda x: x[1], reverse=True)[:4]
print("\nTop 4 most likely (by Top 4 %):")
print(" | ".join(f"{team} ({prob*100:.1f}%)" for team, prob in top4_sorted))

# Calculate combined probability (naïve joint, assuming independence)
top4_joint_prob = 1.0
for _, prob in top4_sorted:
    top4_joint_prob *= prob
print(f"Combined Top 4 probability (all 4 finish in top 4): {top4_joint_prob*100:.6f}%")

# --- Top 6 Most Likely (sorted and joint probability) ---
top6_probs = {team: fractional_to_probability(odds) for team, odds in top6_odds.items()}
top6_sorted = sorted(top6_probs.items(), key=lambda x: x[1], reverse=True)[:6]
print("\nTop 6 most likely (by Top 6 %):")
print(" | ".join(f"{team} ({prob*100:.1f}%)" for team, prob in top6_sorted))

# Calculate combined probability (naïve joint, assuming independence)
top6_joint_prob = 1.0
for _, prob in top6_sorted:
    top6_joint_prob *= prob
print(f"Combined Top 6 probability (all 6 finish in top 6): {top6_joint_prob*100:.6f}%")
