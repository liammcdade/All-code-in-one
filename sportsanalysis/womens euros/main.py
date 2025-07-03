import random
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class TeamStats:
    """Data class for team statistics."""
    group: str
    team: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = 0
    points: int = 0


class TournamentData:
    """Contains all tournament data and configuration."""
    
    # Initial team data
    INITIAL_TEAMS = [
        {'Group': 'A', 'Team': 'Norway',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'A', 'Team': 'Switzerland','P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'A', 'Team': 'Iceland',    'P': 1, 'W': 0, 'D': 0, 'L': 1, 'GF': 0, 'GA': 1, 'GD': -1, 'Pts': 0},
        {'Group': 'A', 'Team': 'Finland',    'P': 1, 'W': 1, 'D': 0, 'L': 0, 'GF': 1, 'GA': 0, 'GD': 1, 'Pts': 0},
        {'Group': 'B', 'Team': 'Spain',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'B', 'Team': 'Italy',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'B', 'Team': 'Belgium',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'B', 'Team': 'Portugal',   'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'C', 'Team': 'Germany',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'C', 'Team': 'Sweden',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'C', 'Team': 'Denmark',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'C', 'Team': 'Poland',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'D', 'Team': 'England',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 6, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'D', 'Team': 'France',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'D', 'Team': 'Netherlands','P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
        {'Group': 'D', 'Team': 'Wales',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    ]
    
    # Group stage fixtures
    GROUP_FIXTURES = [
        # Group A
        ("Norway", "Switzerland"), ("Norway", "Iceland"), ("Switzerland", "Finland"), 
        ("Norway", "Finland"), ("Switzerland", "Iceland"),
        # Group B
        ("Spain", "Italy"), ("Belgium", "Portugal"), ("Spain", "Belgium"), 
        ("Italy", "Portugal"), ("Spain", "Portugal"), ("Italy", "Belgium"),
        # Group C
        ("Germany", "Sweden"), ("Denmark", "Poland"), ("Germany", "Denmark"), 
        ("Sweden", "Poland"), ("Germany", "Poland"), ("Sweden", "Denmark"),
        # Group D
        ("England", "France"), ("Netherlands", "Wales"), ("England", "Netherlands"), 
        ("France", "Wales"), ("England", "Wales"), ("France", "Netherlands"),
    ]
    
    # FIFA/UEFA Women's Rankings (lower number = stronger team)
    FIFA_UEFA_RANKINGS = {
        'England': 1, 'Spain': 2, 'France': 3, 'Germany': 4, 'Sweden': 5, 'Netherlands': 6, 
        'Italy': 7, 'Norway': 8, 'Denmark': 9, 'Belgium': 10, 'Switzerland': 11, 
        'Portugal': 12, 'Iceland': 13, 'Finland': 14, 'Poland': 15, 'Wales': 16
    }


class TournamentTable:
    """Manages the tournament table and standings."""
    
    def __init__(self):
        self.table = self._create_table()
    
    def _create_table(self) -> Dict[str, Dict[str, Any]]:
        """Create table from initial data."""
        table = {}
        for row in TournamentData.INITIAL_TEAMS:
            team = row['Team']
            table[team] = row.copy()
        return table
    
    def reset(self) -> None:
        """Reset all team statistics to zero."""
        for team in self.table:
            self.table[team].update({
                'P': 0, 'W': 0, 'D': 0, 'L': 0, 
                'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0
            })
    
    def update_match(self, team1: str, team2: str, goals1: int, goals2: int) -> None:
        """Update table with match result."""
        # Update games played
        self.table[team1]['P'] += 1
        self.table[team2]['P'] += 1
        
        # Update goals
        self.table[team1]['GF'] += goals1
        self.table[team1]['GA'] += goals2
        self.table[team2]['GF'] += goals2
        self.table[team2]['GA'] += goals1
        
        # Update goal difference
        self.table[team1]['GD'] = self.table[team1]['GF'] - self.table[team1]['GA']
        self.table[team2]['GD'] = self.table[team2]['GF'] - self.table[team2]['GA']
        
        # Update wins, draws, losses, and points
        if goals1 > goals2:
            self.table[team1]['W'] += 1
            self.table[team2]['L'] += 1
            self.table[team1]['Pts'] += 3
        elif goals1 < goals2:
            self.table[team2]['W'] += 1
            self.table[team1]['L'] += 1
            self.table[team2]['Pts'] += 3
        else:
            self.table[team1]['D'] += 1
            self.table[team2]['D'] += 1
            self.table[team1]['Pts'] += 1
            self.table[team2]['Pts'] += 1
    
    def get_group_standings(self) -> Dict[str, List[Tuple[str, Dict[str, Any]]]]:
        """Get standings grouped by group, sorted by points."""
        groups = {}
        for team, stats in self.table.items():
            groups.setdefault(stats['Group'], []).append((team, stats))
        
        standings = {}
        for group, teams in groups.items():
            teams.sort(key=lambda x: (-x[1]['Pts'], -x[1]['GD'], -x[1]['GF'], x[0]))
            standings[group] = teams
        return standings
    
    def print_table(self, sort_by_group: bool = True) -> None:
        """Print the tournament table."""
        columns = ['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
        print("Group, Team, " + ", ".join(columns))
        
        if sort_by_group:
            teams = list(self.table.items())
            teams.sort(key=lambda x: (x[1]['Group'], -x[1]['Pts'], -x[1]['GD'], -x[1]['GF'], x[0]))
        else:
            teams = self.table.items()
        
        for team, stats in teams:
            stat_str = " ".join([f"{col}:{stats[col]}" for col in columns])
            print(f"{stats['Group']}, {team}, {stat_str}")


class MatchSimulator:
    """Handles match simulation logic."""
    
    @staticmethod
    def simulate_match(team1: str, team2: str) -> Tuple[int, int]:
        """Simulate a single match result based on team rankings."""
        r1 = TournamentData.FIFA_UEFA_RANKINGS.get(team1, 20)
        r2 = TournamentData.FIFA_UEFA_RANKINGS.get(team2, 20)
        
        # Calculate win probability based on ranking difference
        diff = r2 - r1
        p1 = 0.5 + 0.12 * diff
        p1 = max(0.05, min(0.9, p1))
        p2 = 1 - p1
        
        # Determine match outcome
        outcome = random.choices(['win1', 'draw', 'win2'], weights=[p1, 0.18, p2])[0]
        
        # Generate goals based on outcome
        if outcome == 'win1':
            goals1, goals2 = random.randint(1, 3), random.randint(0, 1)
        elif outcome == 'win2':
            goals1, goals2 = random.randint(0, 1), random.randint(1, 3)
        else:  # draw
            goals1 = goals2 = random.randint(0, 2)
        
        return goals1, goals2
    
    @staticmethod
    def simulate_group_stage(table: TournamentTable) -> None:
        """Simulate all group stage matches."""
        for team1, team2 in TournamentData.GROUP_FIXTURES:
            goals1, goals2 = MatchSimulator.simulate_match(team1, team2)
            table.update_match(team1, team2, goals1, goals2)


class TournamentSimulator:
    """Handles full tournament simulation."""
    
    @staticmethod
    def simulate_tournament(num_simulations: int = 1000) -> Dict[str, int]:
        """Simulate full tournament multiple times and return win counts."""
        win_counts = {team: 0 for team in TournamentData.FIFA_UEFA_RANKINGS}
        
        for _ in range(num_simulations):
            table = TournamentTable()
            MatchSimulator.simulate_group_stage(table)
            standings = table.get_group_standings()
            
            # Get qualifiers (top 2 from each group)
            qualifiers = []
            for group in sorted(standings):
                qualifiers.extend([standings[group][0][0], standings[group][1][0]])
            
            # Simulate knockout stages
            winner = TournamentSimulator._simulate_knockout_stage(qualifiers)
            win_counts[winner] += 1
        
        return win_counts
    
    @staticmethod
    def _simulate_knockout_stage(teams: List[str]) -> str:
        """Simulate knockout stage and return winner."""
        next_round = teams[:]
        random.shuffle(next_round)
        
        while len(next_round) > 1:
            winners = []
            for i in range(0, len(next_round), 2):
                if i + 1 >= len(next_round):
                    winners.append(next_round[i])
                else:
                    team1, team2 = next_round[i], next_round[i + 1]
                    winner = TournamentSimulator._simulate_knockout_match(team1, team2)
                    winners.append(winner)
            next_round = winners
        
        return next_round[0]
    
    @staticmethod
    def _simulate_knockout_match(team1: str, team2: str) -> str:
        """Simulate a single knockout match."""
        r1 = TournamentData.FIFA_UEFA_RANKINGS.get(team1, 20)
        r2 = TournamentData.FIFA_UEFA_RANKINGS.get(team2, 20)
        p1 = 0.5 + 0.12 * (r2 - r1)
        p1 = max(0.05, min(0.9, p1))
        return team1 if random.random() < p1 else team2
    
    @staticmethod
    def print_win_probabilities(win_counts: Dict[str, int], num_simulations: int) -> None:
        """Print tournament win probabilities."""
        print(f"\n--- Tournament Win Probabilities ({num_simulations} simulations) ---")
        for team, count in sorted(win_counts.items(), key=lambda x: -x[1]):
            probability = count / num_simulations
            print(f"{team:15}: {probability:.2%}")


def main():
    """Main function to run tournament simulation."""
    num_simulations = 1000
    win_counts = TournamentSimulator.simulate_tournament(num_simulations)
    TournamentSimulator.print_win_probabilities(win_counts, num_simulations)


if __name__ == "__main__":
    main()
