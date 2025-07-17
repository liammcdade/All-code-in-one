
"""
UEFA Champions League 2025–26 League Phase Draw Simulator
Models the draw process, pots, and teams for the new format.
"""

import random
from collections import defaultdict

# Team data: (Name, Club Coefficient, Pot)
teams = [
    # Pot 1
    ("Paris Saint-Germain", 118.500, 1),
    ("Real Madrid", 143.500, 1),
    ("Manchester City", 137.750, 1),
    ("Bayern Munich", 135.250, 1),
    ("Liverpool", 125.500, 1),
    ("Inter Milan", 116.250, 1),
    ("Chelsea", 109.000, 1),
    ("Borussia Dortmund", 106.750, 1),
    ("Barcelona", 103.250, 1),
    # Pot 2
    ("Arsenal", 98.000, 2),
    ("Bayer Leverkusen", 95.250, 2),
    ("Atlético Madrid", 93.500, 2),
    ("Atalanta", 82.000, 2),
    ("Villarreal", 82.000, 2),
    ("Juventus", 74.250, 2),
    ("Eintracht Frankfurt", 74.000, 2),
    # Pot 2/3
    ("Tottenham Hotspur", 70.250, 2),
    ("PSV Eindhoven", 69.250, 2),
    # Pot 3
    ("Ajax", 67.250, 3),
    ("Napoli", 61.000, 3),
    ("Sporting CP", 59.000, 3),
    ("Olympiacos", 56.500, 3),
    ("Slavia Prague", 51.000, 3),
    ("Marseille", 48.000, 3),
    # Pot 3/4
    ("Monaco", 41.000, 3),
    ("Galatasaray", 38.250, 3),
    ("Union Saint-Gilloise", 36.000, 3),
    # Pot 4
    ("Athletic Bilbao", 26.750, 4),
    ("Newcastle United", 23.039, 4),
    # ...add remaining qualified teams and qualifiers here...
]

# Organize teams by pot
pots = defaultdict(list)
for name, coeff, pot in teams:
    pots[pot].append((name, coeff))

def print_pots(pots):
    print("UEFA Champions League 2025–26 Pots:")
    for pot_num in sorted(pots.keys()):
        print(f"\nPot {pot_num}:")
        for name, coeff in sorted(pots[pot_num], key=lambda x: -x[1]):
            print(f"  {name:25} CC: {coeff}")

if __name__ == "__main__":
    print_pots(pots)

