import numpy as np
from collections import defaultdict, Counter
import random

# --- TEAM/PLAYER ALIAS MAP (not used, but kept for reference) ---
TEAM_ALIASES = {
    "Palmeiras": ["Palmeiras", "br Palmeiras"],
    "FC Porto": ["FC Porto", "Porto"],
    "Al Ahly SC": ["Al Ahly", "eg Al Ahly", "eg EGY Al Ahly", "Al Ahly SC"],
    "Inter Miami CF": ["Inter Miami", "us Inter Miami", "us USA Inter Miami", "Inter Miami CF"],
    "Paris Saint-Germain": ["Paris Saint-Germain", "fr Paris Saint-Germain", "Paris S-G"],
    "Atletico Madrid": ["Atletico Madrid", "es Atletico Madrid", "es ESP Atletico Madrid", "Atlético Madrid"],
    "Botafogo": ["Botafogo", "br Botafogo"],
    "Seattle Sounders": ["Seattle Sounders", "us Seattle Sounders"],
    "Bayern Munich": ["Bayern Munich", "de Bayern Munich"],
    "Benfica": ["Benfica", "pt Benfica"],
    "Boca Juniors": ["Boca Juniors", "ar Boca Juniors"],
    "Auckland City": ["Auckland City", "nz Auckland City"],
    "Flamengo": ["Flamengo", "br Flamengo"],
    "Chelsea FC": ["Chelsea FC", "en Chelsea FC", "Chelsea"],
    "Espérance Sportive de Tunis": ["Espérance Sportive de Tunis", "tn Espérance Sportive de Tunis", "Tunis"],
    "Los Angeles FC": ["Los Angeles FC", "us Los Angeles FC", "LAFC"],
    "River Plate": ["River Plate", "ar River Plate"],
    "Inter Milan": ["Inter Milan", "it Inter Milan", "Inter"],
    "CF Monterrey": ["CF Monterrey", "mx CF Monterrey", "Monterrey"],
    "Urawa Red Diamonds": ["Urawa Red Diamonds", "jp Urawa Red Diamonds", "Urawa Reds"],
    "Fluminense": ["Fluminense", "br Fluminense"],
    "Borussia Dortmund": ["Borussia Dortmund", "de Borussia Dortmund", "Dortmund"],
    "Ulsan HD FC": ["Ulsan HD FC", "kr Ulsan HD FC", "Ulsan HD"],
    "Mamelodi Sundowns": ["Mamelodi Sundowns", "za Mamelodi Sundowns", "Sundowns"],
    "Manchester City": ["Manchester City", "en Manchester City"],
    "Juventus": ["Juventus", "it Juventus"],
    "Wydad AC": ["Wydad AC", "ma Wydad AC"],
    "Al Ain FC": ["Al Ain FC", "ae Al Ain FC"],
    "Real Madrid": ["Real Madrid", "es Real Madrid"],
    "Al Hilal SFC": ["Al Hilal SFC", "sa Al Hilal SFC", "Al-Hilal"],
    "Pachuca": ["Pachuca", "mx Pachuca"],
    "Red Bull Salzburg": ["Red Bull Salzburg", "at Red Bull Salzburg", "RB Salzburg"],
}
ALIAS_TO_TEAM = {alias.lower(): team for team, aliases in TEAM_ALIASES.items() for alias in aliases}

# --- TEAM DATA (with current stats, these are used as the starting point for the simulation) ---
# Each tuple represents: (id, name, group, matches_played, wins, draws, losses, goals_for, goals_against, points)
TEAMS = [
    (1, "Palmeiras", "A", 2, 1, 1, 0, 2, 0, 4),
    (2, "FC Porto", "A", 2, 0, 1, 1, 1, 2, 1),
    (3, "Al Ahly SC", "A", 2, 0, 1, 1, 0, 2, 1),
    (4, "Inter Miami CF", "A", 2, 1, 1, 0, 2, 1, 4),
    (5, "Paris Saint-Germain", "B", 2, 1, 0, 1, 4, 1, 3),
    (6, "Atletico Madrid", "B", 2, 1, 0, 1, 3, 5, 3),
    (7, "Botafogo", "B", 2, 2, 0, 0, 3, 1, 6),
    (8, "Seattle Sounders", "B", 2, 0, 0, 2, 2, 5, 0),
    (9, "Bayern Munich", "C", 2, 2, 0, 0, 12, 1, 6),
    (10, "Benfica", "C", 2, 1, 1, 0, 8, 2, 4),
    (11, "Boca Juniors", "C", 2, 0, 1, 1, 3, 4, 1),
    (12, "Auckland City", "C", 2, 0, 0, 2, 0, 16, 0),
    (13, "Flamengo", "D", 2, 2, 0, 0, 5, 1, 6),
    (14, "Chelsea FC", "D", 2, 1, 0, 1, 3, 3, 3),
    (15, "Espérance Sportive de Tunis", "D", 2, 1, 0, 1, 1, 2, 3),
    (16, "Los Angeles FC", "D", 2, 0, 0, 2, 0, 3, 0),
    (17, "River Plate", "E", 2, 1, 1, 0, 3, 1, 4),
    (18, "Inter Milan", "E", 2, 1, 1, 0, 3, 2, 4),
    (19, "CF Monterrey", "E", 2, 0, 2, 0, 1, 1, 2),
    (20, "Urawa Red Diamonds", "E", 2, 0, 0, 2, 2, 5, 0),
    (21, "Fluminense", "F", 2, 1, 1, 0, 4, 2, 4),
    (22, "Borussia Dortmund", "F", 2, 1, 1, 0, 4, 3, 4),
    (23, "Ulsan HD FC", "F", 2, 0, 0, 2, 2, 5, 0),
    (24, "Mamelodi Sundowns", "F", 2, 1, 0, 1, 4, 4, 3),
    (25, "Manchester City", "G", 2, 2, 0, 0, 4, 0, 6),
    (26, "Juventus", "G", 2, 1, 1, 0, 6, 1, 4),
    (27, "Wydad AC", "G", 2, 0, 0, 2, 0, 3, 0),
    (28, "Al Ain FC", "G", 2, 0, 0, 2, 0, 7, 0),
    # Updated Group H teams based on user input
    (29, "Real Madrid", "H", 2, 1, 1, 0, 4, 2, 4),
    (30, "Al Hilal SFC", "H", 2, 0, 2, 0, 1, 1, 2),
    (31, "Pachuca", "H", 2, 0, 0, 2, 2, 5, 0),
    (32, "Red Bull Salzburg", "H", 2, 1, 1, 0, 2, 1, 4),
]

class Team:
    """
    Represents a football team with its statistics in a group stage.
    """
    def __init__(self, id, name, group, mp, w, d, l, gf, ga, pts):
        self.id = id
        self.name = name
        self.group = group
        self.mp = mp  # Matches Played
        self.w = w    # Wins
        self.d = d    # Draws
        self.l = l    # Losses
        self.gf = gf  # Goals For
        self.ga = ga  # Goals Against
        self.pts = pts # Points

    def goal_diff(self):
        """Calculates the goal difference (GF - GA)."""
        return self.gf - self.ga

    def __repr__(self):
        """String representation of the Team object."""
        return f"{self.name} (Pts:{self.pts} GD:{self.goal_diff()} GF:{self.gf} GA:{self.ga})"

def get_groups(teams):
    """
    Organizes teams into groups based on their 'group' attribute.

    Args:
        teams (list): A list of Team objects.

    Returns:
        defaultdict: A dictionary where keys are group names and values are lists of Team objects in that group.
    """
    group_map = defaultdict(list)
    for t in teams:
        group_map[t.group].append(t)
    return group_map

def get_remaining_matches(group_teams):
    """
    Determines the remaining matches for a given group, assuming a round-robin format
    where each team plays every other team once. This function approximates the
    remaining matches based on matches played, as exact previous pairings are unknown.

    Args:
        group_teams (list): A list of Team objects within a single group.

    Returns:
        list: A list of tuples, where each tuple (i, j) represents a match
              between group_teams[i] and group_teams[j].
    """
    n = len(group_teams)
    # Generate all possible unique matches in a round-robin format
    all_matches = [(i, j) for i in range(n) for j in range(i+1, n)]

    # This section is a simplification and might not perfectly reflect real-world
    # played matches if the initial data isn't a strict round-robin partial state.
    # It attempts to "account" for matches already played by each team.
    played_matches_track = set()
    team_matches_played_count = {team.name: team.mp for team in group_teams}
    
    # Create a mapping from team index to team name for easy lookup
    idx_to_team_name = {i: group_teams[i].name for i in range(n)}

    # Greedily mark matches as 'played' to match the 'mp' count.
    # This is an approximation since specific past pairings are not given.
    simulated_played_matches = []
    
    # A simple way to generate 'dummy' played matches for the simulation's internal logic.
    # We iterate through all possible matches and if both teams involved still have
    # 'matches_played' to account for, we consider that match as 'played'.
    temp_played_counts = {team.name: 0 for team in group_teams}
    
    for i, j in all_matches:
        team1_name = idx_to_team_name[i]
        team2_name = idx_to_team_name[j]
        
        if temp_played_counts[team1_name] < team_matches_played_count[team1_name] and \
           temp_played_counts[team2_name] < team_matches_played_count[team2_name]:
            simulated_played_matches.append((i, j))
            temp_played_counts[team1_name] += 1
            temp_played_counts[team2_name] += 1
    
    # Remaining matches are those in 'all_matches' that were not "simulated played"
    remaining = [m for m in all_matches if m not in simulated_played_matches]
    return remaining


def team_strength(t):
    """
    Calculates a numerical strength metric for a team based on its current stats.
    Higher points, higher goal difference, higher goals for, and lower goals against contribute to higher strength.
    """
    return t.pts * 100 + t.goal_diff() * 10 + t.gf - t.ga

def simulate_group(group_teams, n_sim=10000):
    """
    Simulates the remaining matches in a group multiple times to estimate
    knockout qualification probabilities for each team.

    Args:
        group_teams (list): A list of Team objects within a single group.
        n_sim (int): The number of simulations to run.

    Returns:
        dict: A dictionary where keys are team names and values are their
              qualification probabilities (percentage of simulations where they finish in the top 2).
    """
    n = len(group_teams)
    team_names = [t.name for t in group_teams]
    # Initialize qualification counts for each team to 0
    qualify_counts = Counter({name: 0 for name in team_names})
    # Get the list of matches that still need to be simulated
    matches_to_simulate = get_remaining_matches(group_teams)

    for _ in range(n_sim):
        # Create a deep copy of team stats for this specific simulation
        # This ensures that each simulation starts from the initial state
        # and modifications during a simulation don't affect others.
        sim_stats = {t.name: dict(pts=t.pts, w=t.w, d=t.d, l=t.l, gf=t.gf, ga=t.ga) for t in group_teams}

        # Simulate each remaining match
        for i, j in matches_to_simulate:
            t1_original = group_teams[i] # Original team object to get initial strength reference
            t2_original = group_teams[j]

            # Calculate strengths for the current simulation based on their *current* accumulated stats
            # For a more dynamic simulation, these strengths could be recalculated after each match,
            # but for simplicity, we use the initial strengths to determine match outcomes.
            s1 = team_strength(t1_original)
            s2 = team_strength(t2_original)

            # Probabilities based on relative strength, with a baseline draw chance
            total_strength = max(s1 + s2, 1) # Avoid division by zero if both strengths are 0
            
            p1_win = 0.0 # Default probability for team 1 winning
            p2_win = 0.0 # Default probability for team 2 winning
            p_draw = 0.20 # Base 20% draw chance

            # Distribute the remaining 80% based on relative strength
            remaining_prob_for_win = 1.0 - p_draw
            if total_strength > 0: # Ensure we don't divide by zero if both strengths are zero
                p1_win = (s1 / total_strength) * remaining_prob_for_win
                p2_win = (s2 / total_strength) * remaining_prob_for_win
            else:
                # If both strengths are zero, split remaining probability evenly
                p1_win = remaining_prob_for_win / 2
                p2_win = remaining_prob_for_win / 2

            # Normalize probabilities to sum to 1 in case of minor floating point issues
            norm_factor = p1_win + p2_win + p_draw
            if norm_factor > 0: # Prevent division by zero
                p1_win /= norm_factor
                p2_win /= norm_factor
                p_draw /= norm_factor
            else: # Fallback for extremely unlikely scenario where all are zero
                p1_win, p2_win, p_draw = 1/3, 1/3, 1/3


            # Add 23.76% pure randomness: 1/3 win, 1/3 draw, 1/3 loss
            # This makes the outcome less predictable and more "football-like"
            if random.random() < 0.2376:
                r_random = random.random()
                if r_random < 1/3:
                    # Team 1 wins by a small margin (e.g., 1-0)
                    sim_stats[t1_original.name]['pts'] += 3
                    sim_stats[t1_original.name]['w'] += 1
                    sim_stats[t1_original.name]['gf'] += 1
                    sim_stats[t2_original.name]['ga'] += 1
                    sim_stats[t2_original.name]['l'] += 1
                elif r_random < 2/3:
                    # Draw (e.g., 1-1)
                    sim_stats[t1_original.name]['pts'] += 1
                    sim_stats[t2_original.name]['pts'] += 1
                    sim_stats[t1_original.name]['d'] += 1
                    sim_stats[t2_original.name]['d'] += 1
                    sim_stats[t1_original.name]['gf'] += 1
                    sim_stats[t2_original.name]['gf'] += 1
                    sim_stats[t1_original.name]['ga'] += 1
                    sim_stats[t2_original.name]['ga'] += 1
                else:
                    # Team 2 wins by a small margin (e.g., 0-1)
                    sim_stats[t2_original.name]['pts'] += 3
                    sim_stats[t2_original.name]['w'] += 1
                    sim_stats[t2_original.name]['gf'] += 1
                    sim_stats[t1_original.name]['ga'] += 1
                    sim_stats[t1_original.name]['l'] += 1
            else:
                # Outcome based on calculated probabilities (strength-based)
                r_prob = random.random()
                if r_prob < p1_win:
                    # Team 1 wins
                    sim_stats[t1_original.name]['pts'] += 3
                    sim_stats[t1_original.name]['w'] += 1
                    sim_stats[t1_original.name]['gf'] += 1 # Simplified goal scoring
                    sim_stats[t2_original.name]['ga'] += 1 # Simplified goal scoring
                    sim_stats[t2_original.name]['l'] += 1
                elif r_prob < p1_win + p_draw:
                    # Draw
                    sim_stats[t1_original.name]['pts'] += 1
                    sim_stats[t2_original.name]['pts'] += 1
                    sim_stats[t1_original.name]['d'] += 1
                    sim_stats[t2_original.name]['d'] += 1
                    sim_stats[t1_original.name]['gf'] += 1 # Simplified goal scoring
                    sim_stats[t2_original.name]['gf'] += 1 # Simplified goal scoring
                    sim_stats[t1_original.name]['ga'] += 1 # Simplified goal scoring
                    sim_stats[t2_original.name]['ga'] += 1 # Simplified goal scoring
                else:
                    # Team 2 wins
                    sim_stats[t2_original.name]['pts'] += 3
                    sim_stats[t2_original.name]['w'] += 1
                    sim_stats[t2_original.name]['gf'] += 1 # Simplified goal scoring
                    sim_stats[t1_original.name]['ga'] += 1 # Simplified goal scoring
                    sim_stats[t1_original.name]['l'] += 1

        # After all matches in this simulation, rank teams based on final stats
        # Tie-breaking rules: 1. Points, 2. Goal Difference, 3. Goals For, 4. Alphabetical Name
        ranked = sorted(group_teams, key=lambda t: (
            sim_stats[t.name]['pts'],
            sim_stats[t.name]['gf'] - sim_stats[t.name]['ga'],
            sim_stats[t.name]['gf'],
            t.name # Tie-breaker by name (alphabetical)
        ), reverse=True)

        # The top 2 teams qualify from each group
        for idx in range(min(2, len(ranked))):
            qualify_counts[ranked[idx].name] += 1

    # Convert the counts to probabilities by dividing by the total number of simulations
    probs = {name: qualify_counts[name] / n_sim for name in team_names}
    return probs

def print_group_qualification_probs(teams, n_sim=10000):
    """
    Calculates and prints the knockout qualification probabilities for all teams
    across all groups.

    Args:
        teams (list): A list of all Team objects.
        n_sim (int): The number of simulations to run per group.
    """
    group_map = get_groups(teams)
    print("\n=== Knockout Qualification Probabilities (Simulated) ===")
    for group_name in sorted(group_map.keys()):
        group_teams = group_map[group_name]
        probs = simulate_group(group_teams, n_sim)
        print(f"\nGroup {group_name}")
        # Sort teams by their qualification probability in descending order for display
        for t in sorted(group_teams, key=lambda t: -probs[t.name]):
            print(f"{t.name:<28} : {probs[t.name]*100:6.2f}% chance to finish top 2 (qualify)")

if __name__ == "__main__":
    # Create Team objects from the predefined TEAMS data
    teams = [Team(*row) for row in TEAMS]
    # Run the simulation and print the results
    print_group_qualification_probs(teams, n_sim=10000)
