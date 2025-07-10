import random

# Full driver list and current points
drivers = [
    ("O. Piastri", 234),
    ("L. Norris", 226),
    ("M. Verstappen", 165),
    ("G. Russell", 147),
    ("C. Leclerc", 119),
    ("L. Hamilton", 103),
    ("A. Antonelli", 63),
    ("A. Albon", 46),
    ("N. Hulkenberg", 37),
    ("E. Ocon", 23),
    ("I. Hadjar", 21),
    ("L. Stroll", 20),
    ("P. Gasly", 19),
    ("F. Alonso", 16),
    ("C. Sainz", 13),
    ("L. Lawson", 12),
    ("Y. Tsunoda", 10),
    ("O. Bearman", 6),
    ("G. Bortoleto", 4),
    ("F. Colapinto", 0),
    ("J. Doohan", 0)
]

driver_names = [d[0] for d in drivers]
base_points = {d[0]: d[1] for d in drivers}

# F1 points for top 10
scoring = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

races_left = 11
simulations = 10000

within_25_trio = 0
within_25_pair = 0

# Add a win counter for each driver
win_counter = {name: 0 for name in driver_names}

for _ in range(simulations):
    sim_points = base_points.copy()
    for _ in range(races_left):
        if random.random() < 0.0745:
            finish = random.sample(driver_names, len(driver_names))
        else:
            weights = [sim_points[name] + 1 for name in driver_names]
            finish = random.choices(
                population=driver_names,
                weights=weights,
                k=len(driver_names)
            )
            seen = set()
            finish = [x for x in finish if not (x in seen or seen.add(x))]
        for idx, driver in enumerate(finish[:10]):
            sim_points[driver] += scoring[idx]
    # Check all three within 25
    piastri = sim_points["O. Piastri"]
    norris = sim_points["L. Norris"]
    verstappen = sim_points["M. Verstappen"]
    if max(piastri, norris, verstappen) - min(piastri, norris, verstappen) <= 25:
        within_25_trio += 1
    if abs(piastri - norris) <= 25:
        within_25_pair += 1
    # Determine winner(s)
    max_points = max(sim_points.values())
    winners = [name for name, pts in sim_points.items() if pts == max_points]
    for winner in winners:
        win_counter[winner] += 1 / len(winners)  # Split if tie

trio_percent = within_25_trio / simulations * 100
pair_percent = within_25_pair / simulations * 100

print(f"Chance Piastri, Norris, and Verstappen are within 25 points of each other before the final race: {trio_percent:.2f}%")
print(f"Chance Piastri and Norris are within 25 points of each other before the final race: {pair_percent:.2f}%")
print("\nChance of each driver winning the championship:")

for name in driver_names:
    win_percent = win_counter[name] / simulations * 100
    print(f"{name}: {win_percent:.2f}%")
