import random
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics
import pandas as pd # For creating Series for plotting
import plotext as plt # For terminal plotting


@dataclass
class TennisPlayer:
    """Data class for tennis player statistics."""
    name: str
    rank: int
    country: str
    age: int
    height: int  # in cm
    weight: int  # in kg
    hand: str  # Right, Left, Ambidextrous
    surface_preference: str  # Hard, Clay, Grass, All
    serve_rating: float  # 1-10
    return_rating: float  # 1-10
    forehand_rating: float  # 1-10
    backhand_rating: float  # 1-10
    movement_rating: float  # 1-10
    mental_rating: float  # 1-10
    fitness_rating: float  # 1-10
    titles: int = 0
    grand_slams: int = 0
    win_loss_record: Tuple[int, int] = (0, 0)


@dataclass
class MatchResult:
    """Data class for tennis match results."""
    tournament: str
    round: str
    player1: str
    player2: str
    player1_sets: int
    player2_sets: int
    player1_games: List[int]
    player2_games: List[int]
    duration_minutes: int
    date: str
    surface: str
    winner: str


@dataclass
class Tournament:
    """Data class for tennis tournament information."""
    name: str
    surface: str
    category: str  # Grand Slam, Masters 1000, ATP 500, etc.
    location: str
    prize_money: float
    points: int
    draw_size: int


class TennisData:
    """Contains tennis data and configuration."""
    
    # Sample ATP players data
    ATP_PLAYERS = [
        TennisPlayer("Novak Djokovic", 1, "Serbia", 36, 188, 77, "Right", "All", 9.2, 9.5, 9.8, 9.3, 9.7, 9.9, 9.8, 98, 24, (1089, 213)),
        TennisPlayer("Carlos Alcaraz", 2, "Spain", 20, 183, 80, "Right", "All", 8.8, 9.3, 9.7, 9.0, 9.9, 8.5, 9.2, 12, 2, (155, 43)),
        TennisPlayer("Daniil Medvedev", 3, "Russia", 27, 198, 83, "Right", "Hard", 9.0, 9.4, 9.1, 9.2, 9.3, 8.8, 9.0, 20, 1, (350, 143)),
        TennisPlayer("Jannik Sinner", 4, "Italy", 22, 188, 76, "Right", "Hard", 8.9, 9.2, 9.4, 8.8, 9.6, 8.7, 9.1, 10, 0, (200, 75)),
        TennisPlayer("Andrey Rublev", 5, "Russia", 26, 188, 75, "Right", "Hard", 8.7, 8.9, 9.2, 8.5, 8.8, 8.0, 8.9, 15, 0, (320, 180)),
        TennisPlayer("Stefanos Tsitsipas", 6, "Greece", 25, 193, 89, "Right", "Clay", 8.8, 8.7, 9.3, 8.9, 9.1, 8.2, 8.8, 10, 0, (300, 150)),
        TennisPlayer("Alexander Zverev", 7, "Germany", 26, 198, 90, "Right", "Hard", 9.1, 8.8, 9.0, 9.1, 9.2, 7.8, 8.7, 21, 0, (380, 160)),
        TennisPlayer("Holger Rune", 8, "Denmark", 20, 188, 77, "Right", "Clay", 8.5, 8.9, 9.1, 8.7, 9.4, 8.1, 8.6, 4, 0, (120, 60)),
        TennisPlayer("Hubert Hurkacz", 9, "Poland", 26, 196, 81, "Right", "Hard", 9.3, 8.2, 8.8, 8.6, 8.5, 8.3, 8.8, 7, 0, (200, 120)),
        TennisPlayer("Taylor Fritz", 10, "USA", 25, 196, 86, "Right", "Hard", 8.9, 8.4, 9.0, 8.3, 8.7, 8.1, 8.5, 6, 0, (180, 110))
    ]
    
    # Sample WTA players data
    WTA_PLAYERS = [
        TennisPlayer("Iga Swiatek", 1, "Poland", 22, 176, 65, "Right", "Clay", 8.5, 9.4, 9.6, 8.8, 9.7, 9.2, 9.3, 17, 4, (280, 60)),
        TennisPlayer("Aryna Sabalenka", 2, "Belarus", 25, 182, 80, "Right", "Hard", 9.2, 8.8, 9.4, 8.5, 8.9, 8.7, 9.0, 13, 2, (350, 150)),
        TennisPlayer("Coco Gauff", 3, "USA", 19, 175, 65, "Right", "Hard", 8.8, 9.1, 8.9, 8.7, 9.5, 8.9, 9.1, 6, 1, (180, 80)),
        TennisPlayer("Elena Rybakina", 4, "Kazakhstan", 24, 184, 65, "Right", "Hard", 9.4, 8.6, 9.2, 8.4, 8.8, 8.5, 8.9, 6, 1, (200, 100)),
        TennisPlayer("Jessica Pegula", 5, "USA", 29, 170, 65, "Right", "Hard", 8.3, 9.0, 8.8, 8.6, 8.7, 8.8, 8.6, 4, 0, (250, 150)),
        TennisPlayer("Ons Jabeur", 6, "Tunisia", 29, 167, 65, "Right", "Clay", 8.1, 8.9, 8.7, 8.8, 8.9, 8.6, 8.5, 4, 0, (300, 180)),
        TennisPlayer("Marketa Vondrousova", 7, "Czech Republic", 24, 174, 65, "Left", "Clay", 7.8, 8.8, 8.6, 8.9, 8.6, 8.4, 8.3, 2, 1, (180, 120)),
        TennisPlayer("Karolina Muchova", 8, "Czech Republic", 27, 180, 70, "Right", "All", 8.2, 8.7, 8.8, 8.5, 8.8, 8.3, 8.4, 1, 0, (150, 100)),
        TennisPlayer("Maria Sakkari", 9, "Greece", 28, 172, 65, "Right", "Hard", 8.4, 8.5, 8.7, 8.3, 8.9, 8.1, 8.5, 1, 0, (200, 150)),
        TennisPlayer("Barbora Krejcikova", 10, "Czech Republic", 27, 178, 65, "Right", "Clay", 7.9, 8.6, 8.5, 8.7, 8.4, 8.2, 8.3, 7, 1, (180, 110))
    ]
    
    # Tournament data
    TOURNAMENTS = [
        Tournament("Australian Open", "Hard", "Grand Slam", "Melbourne", 50000000, 2000, 128),
        Tournament("French Open", "Clay", "Grand Slam", "Paris", 45000000, 2000, 128),
        Tournament("Wimbledon", "Grass", "Grand Slam", "London", 40000000, 2000, 128),
        Tournament("US Open", "Hard", "Grand Slam", "New York", 50000000, 2000, 128),
        Tournament("Indian Wells", "Hard", "Masters 1000", "California", 8000000, 1000, 96),
        Tournament("Miami Open", "Hard", "Masters 1000", "Miami", 8000000, 1000, 96),
        Tournament("Monte Carlo", "Clay", "Masters 1000", "Monaco", 6000000, 1000, 56),
        Tournament("Madrid Open", "Clay", "Masters 1000", "Madrid", 7000000, 1000, 96),
        Tournament("Rome Masters", "Clay", "Masters 1000", "Rome", 7000000, 1000, 96),
        Tournament("Canadian Open", "Hard", "Masters 1000", "Toronto/Montreal", 6000000, 1000, 56)
    ]


class TennisSimulator:
    """Handles tennis match simulation."""
    
    @staticmethod
    def calculate_match_probability(player1: TennisPlayer, player2: TennisPlayer, surface: str) -> float:
        """Calculate probability of player1 winning against player2 on given surface."""
        # Base probability from rankings
        rank_diff = player2.rank - player1.rank
        base_prob = 0.5 + (rank_diff * 0.02)
        
        # Surface adjustment
        surface_bonus1 = 0
        surface_bonus2 = 0
        
        if player1.surface_preference == surface or player1.surface_preference == "All":
            surface_bonus1 = 0.1
        if player2.surface_preference == surface or player2.surface_preference == "All":
            surface_bonus2 = 0.1
        
        # Skill adjustment
        skill_diff = (
            (player1.serve_rating + player1.return_rating + player1.forehand_rating + 
             player1.backhand_rating + player1.movement_rating + player1.mental_rating + 
             player1.fitness_rating) -
            (player2.serve_rating + player2.return_rating + player2.forehand_rating + 
             player2.backhand_rating + player2.movement_rating + player2.mental_rating + 
             player2.fitness_rating)
        ) / 70.0
        
        final_prob = base_prob + surface_bonus1 - surface_bonus2 + skill_diff * 0.1
        return max(0.1, min(0.9, final_prob))
    
    @staticmethod
    def simulate_set() -> Tuple[int, int]:
        """Simulate a single set."""
        games1 = 0
        games2 = 0
        
        while True:
            # Simulate game
            if random.random() < 0.6:  # Server advantage
                if games1 < games2:
                    games1 += 1
                else:
                    games2 += 1
            else:
                if games1 < games2:
                    games2 += 1
                else:
                    games1 += 1
            
            # Check for set win
            if games1 >= 6 and games1 - games2 >= 2:
                return games1, games2
            elif games2 >= 6 and games2 - games1 >= 2:
                return games1, games2
            elif games1 == 7 and games2 == 6:
                return games1, games2
            elif games2 == 7 and games1 == 6:
                return games1, games2
    
    @staticmethod
    def simulate_match(player1: TennisPlayer, player2: TennisPlayer, tournament: Tournament, round_name: str = "First Round") -> MatchResult:
        """Simulate a complete tennis match."""
        win_prob = TennisSimulator.calculate_match_probability(player1, player2, tournament.surface)
        
        sets1 = 0
        sets2 = 0
        games1_list = []
        games2_list = []
        
        # Best of 3 or 5 sets
        max_sets = 5 if tournament.category == "Grand Slam" else 3
        sets_to_win = 3 if max_sets == 5 else 2
        
        while sets1 < sets_to_win and sets2 < sets_to_win:
            # Simulate set
            games1, games2 = TennisSimulator.simulate_set()
            games1_list.append(games1)
            games2_list.append(games2)
            
            # Determine set winner
            if games1 > games2:
                sets1 += 1
            else:
                sets2 += 1
        
        # Determine match winner
        winner = player1.name if sets1 > sets2 else player2.name
        
        # Calculate match duration (rough estimate)
        total_games = sum(games1_list) + sum(games2_list)
        duration_minutes = total_games * 4 + random.randint(30, 90)
        
        return MatchResult(
            tournament=tournament.name,
            round=round_name,
            player1=player1.name,
            player2=player2.name,
            player1_sets=sets1,
            player2_sets=sets2,
            player1_games=games1_list,
            player2_games=games2_list,
            duration_minutes=duration_minutes,
            date=datetime.now().strftime("%Y-%m-%d"),
            surface=tournament.surface,
            winner=winner
        )


class TennisAnalyzer:
    """Analyzes tennis statistics and provides insights."""
    
    def __init__(self):
        self.atp_players = TennisData.ATP_PLAYERS.copy()
        self.wta_players = TennisData.WTA_PLAYERS.copy()
        self.tournaments = TennisData.TOURNAMENTS.copy()
    
    def get_player_by_name(self, name: str, tour: str = "ATP") -> Optional[TennisPlayer]:
        """Get player by name from specified tour."""
        players = self.atp_players if tour.upper() == "ATP" else self.wta_players
        for player in players:
            if player.name == name:
                return player
        return None
    
    def get_tournament_by_name(self, name: str) -> Optional[Tournament]:
        """Get tournament by name."""
        for tournament in self.tournaments:
            if tournament.name == name:
                return tournament
        return None
    
    def analyze_player(self, player_name: str, tour: str = "ATP") -> Dict[str, Any]:
        """Analyze individual player performance."""
        player = self.get_player_by_name(player_name, tour)
        if not player:
            return {"error": "Player not found"}
        
        # Calculate overall rating
        overall_rating = (
            player.serve_rating + player.return_rating + player.forehand_rating +
            player.backhand_rating + player.movement_rating + player.mental_rating +
            player.fitness_rating
        ) / 7.0
        
        # Surface analysis
        surface_ratings = {}
        for surface in ["Hard", "Clay", "Grass"]:
            if player.surface_preference == surface or player.surface_preference == "All":
                surface_ratings[surface] = overall_rating + 0.2
            else:
                surface_ratings[surface] = overall_rating - 0.1
        
        # Win percentage
        total_matches = player.win_loss_record[0] + player.win_loss_record[1]
        win_percentage = (player.win_loss_record[0] / total_matches * 100) if total_matches > 0 else 0
        
        return {
            "player": asdict(player),
            "analysis": {
                "overall_rating": overall_rating,
                "surface_ratings": surface_ratings,
                "win_percentage": win_percentage,
                "career_highlights": {
                    "titles": player.titles,
                    "grand_slams": player.grand_slams,
                    "total_matches": total_matches
                }
            }
        }
    
    def head_to_head_analysis(self, player1_name: str, player2_name: str, tour: str = "ATP") -> Dict[str, Any]:
        """Analyze head-to-head matchup between two players."""
        player1 = self.get_player_by_name(player1_name, tour)
        player2 = self.get_player_by_name(player2_name, tour)
        
        if not player1 or not player2:
            return {"error": "One or both players not found"}
        
        # Calculate win probabilities on different surfaces
        surfaces = ["Hard", "Clay", "Grass"]
        surface_probabilities = {}
        
        for surface in surfaces:
            prob = TennisSimulator.calculate_match_probability(player1, player2, surface)
            surface_probabilities[surface] = {
                "player1_win_prob": prob,
                "player2_win_prob": 1 - prob
            }
        
        # Overall matchup analysis
        overall_prob = TennisSimulator.calculate_match_probability(player1, player2, "Hard")
        
        return {
            "player1": asdict(player1),
            "player2": asdict(player2),
            "matchup_analysis": {
                "overall_player1_win_prob": overall_prob,
                "surface_probabilities": surface_probabilities,
                "key_factors": {
                    "serve_advantage": "Player1" if player1.serve_rating > player2.serve_rating else "Player2",
                    "return_advantage": "Player1" if player1.return_rating > player2.return_rating else "Player2",
                    "movement_advantage": "Player1" if player1.movement_rating > player2.movement_rating else "Player2",
                    "mental_advantage": "Player1" if player1.mental_rating > player2.mental_rating else "Player2"
                }
            }
        }
    
    def simulate_tournament(self, tournament_name: str, tour: str = "ATP") -> Dict[str, Any]:
        """Simulate a complete tournament."""
        tournament = self.get_tournament_by_name(tournament_name)
        if not tournament:
            return {"error": "Tournament not found"}
        
        players = self.atp_players if tour.upper() == "ATP" else self.wta_players
        draw_size = min(tournament.draw_size, len(players))
        tournament_players = players[:draw_size]
        
        # Create bracket
        rounds = []
        current_round = tournament_players.copy()
        round_names = ["First Round", "Second Round", "Third Round", "Fourth Round", 
                      "Quarterfinals", "Semifinals", "Final"]
        
        for i, round_name in enumerate(round_names):
            if len(current_round) <= 1:
                break
            
            round_matches = []
            next_round = []
            
            # Simulate matches in current round
            for j in range(0, len(current_round), 2):
                if j + 1 < len(current_round):
                    player1 = current_round[j]
                    player2 = current_round[j + 1]
                    
                    match = TennisSimulator.simulate_match(player1, player2, tournament, round_name)
                    round_matches.append(asdict(match))
                    
                    # Winner advances
                    winner = player1 if match.winner == player1.name else player2
                    next_round.append(winner)
                else:
                    # Bye
                    next_round.append(current_round[j])
            
            rounds.append({
                "round_name": round_name,
                "matches": round_matches
            })
            
            current_round = next_round
        
        # Determine champion
        champion = current_round[0] if current_round else None
        
        return {
            "tournament": asdict(tournament),
            "champion": asdict(champion) if champion else None,
            "rounds": rounds
        }
    
    def get_ranking_analysis(self, tour: str = "ATP") -> Dict[str, Any]:
        """Analyze current rankings."""
        players = self.atp_players if tour.upper() == "ATP" else self.wta_players
        
        # Top 10 analysis
        top_10 = players[:10]
        
        # Age analysis
        ages = [p.age for p in top_10]
        avg_age = statistics.mean(ages)
        
        # Surface preferences
        surface_prefs = {}
        for player in top_10:
            pref = player.surface_preference
            surface_prefs[pref] = surface_prefs.get(pref, 0) + 1
        
        # Country distribution
        countries = {}
        for player in top_10:
            country = player.country
            countries[country] = countries.get(country, 0) + 1
        
        return {
            "tour": tour,
            "top_10": [asdict(p) for p in top_10],
            "analysis": {
                "average_age": avg_age,
                "surface_preferences": surface_prefs,
                "country_distribution": countries,
                "youngest_player": min(top_10, key=lambda p: p.age),
                "oldest_player": max(top_10, key=lambda p: p.age)
            }
        }


def main():
    """Main function to demonstrate tennis analysis."""
    analyzer = TennisAnalyzer()
    
    print("=== Tennis Analysis Tool ===\n")
    
    # Player analysis
    print("1. Player Analysis - Novak Djokovic:")
    player_analysis = analyzer.analyze_player("Novak Djokovic", "ATP")
    print(f"Overall Rating: {player_analysis['analysis']['overall_rating']:.2f}")
    print(f"Win Percentage: {player_analysis['analysis']['win_percentage']:.1f}%")
    print(f"Grand Slams: {player_analysis['analysis']['career_highlights']['grand_slams']}")
    print()
    
    # Head-to-head analysis
    print("2. Head-to-Head Analysis - Djokovic vs Alcaraz:")
    h2h = analyzer.head_to_head_analysis("Novak Djokovic", "Carlos Alcaraz", "ATP")
    print(f"Overall Win Probability (Djokovic): {h2h['matchup_analysis']['overall_player1_win_prob']:.1%}")
    print(f"Hard Court (Djokovic): {h2h['matchup_analysis']['surface_probabilities']['Hard']['player1_win_prob']:.1%}")
    print(f"Clay Court (Djokovic): {h2h['matchup_analysis']['surface_probabilities']['Clay']['player1_win_prob']:.1%}")
    print()
    
    # Tournament simulation
    print("3. Tournament Simulation - Australian Open:")
    tournament_result = analyzer.simulate_tournament("Australian Open", "ATP")
    if tournament_result.get("champion"):
        print(f"Champion: {tournament_result['champion']['name']}")
        print(f"Rounds played: {len(tournament_result['rounds'])}")
    print()
    
    # Ranking analysis
    print("4. ATP Rankings Analysis:")
    ranking_analysis = analyzer.get_ranking_analysis("ATP")
    print(f"Average Age (Top 10): {ranking_analysis['analysis']['average_age']:.1f}")
    print(f"Surface Preferences: {ranking_analysis['analysis']['surface_preferences']}")
    print(f"Youngest: {ranking_analysis['analysis']['youngest_player']['name']} ({ranking_analysis['analysis']['youngest_player']['age']})")
    print(f"Oldest: {ranking_analysis['analysis']['oldest_player']['name']} ({ranking_analysis['analysis']['oldest_player']['age']})")
    print()

    # Plot Top 10 ATP Players by Overall Rating
    print("5. Top 10 ATP Players by Overall Rating Plot:")
    top_10_atp_players_data = ranking_analysis['top_10'] # This is for ATP by default from previous call
    
    player_ratings = {}
    for player_dict in top_10_atp_players_data:
        # Need to call analyze_player to get the 'overall_rating'
        # This might be slightly inefficient if analyze_player does a lot, but necessary for the rating
        player_details = analyzer.analyze_player(player_dict['name'], "ATP")
        if "analysis" in player_details and "overall_rating" in player_details["analysis"]:
            player_ratings[player_dict['name']] = player_details["analysis"]["overall_rating"]
        else:
            # Fallback or skip if rating not found
            player_ratings[player_dict['name']] = 0


    if player_ratings:
        ratings_series = pd.Series(player_ratings).sort_values(ascending=False)
        plot_generic_top_n(ratings_series, "Top ATP Players by Overall Rating", "Player", "Overall Rating", top_n=10, sort_ascending=False)
    else:
        print("Could not retrieve ratings for plotting.")

    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main()


def plot_generic_top_n(data_series: pd.Series, title: str, xlabel: str, ylabel: str, top_n: int = 10, sort_ascending=False) -> None:
    """Displays a generic bar chart for a pandas Series in the terminal."""
    sorted_series = data_series.sort_values(ascending=sort_ascending)
    top_data = sorted_series.head(top_n)
    items = top_data.index.tolist()
    values = top_data.values.tolist()

    plt.clf()
    plt.bar(items, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()