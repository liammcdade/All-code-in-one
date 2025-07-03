import random
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics


@dataclass
class OlympicAthlete:
    """Data class for Olympic athlete information."""
    name: str
    country: str
    sport: str
    event: str
    age: int
    gender: str
    height: float  # in cm
    weight: float  # in kg
    
    # Performance ratings (1-10)
    strength_rating: float = 5.0
    speed_rating: float = 5.0
    endurance_rating: float = 5.0
    technique_rating: float = 5.0
    mental_rating: float = 5.0
    experience_rating: float = 5.0
    
    # Career stats
    personal_best: float = 0.0
    season_best: float = 0.0
    world_ranking: int = 0
    olympic_appearances: int = 0
    medals_won: int = 0
    gold_medals: int = 0


@dataclass
class OlympicEvent:
    """Data class for Olympic event information."""
    name: str
    sport: str
    gender: str
    event_type: str  # Individual, Team, Relay
    scoring_type: str  # Time, Distance, Points, Judged
    venue: str
    date: str
    participants: List[OlympicAthlete] = None
    
    def __post_init__(self):
        if self.participants is None:
            self.participants = []


@dataclass
class OlympicCountry:
    """Data class for Olympic country information."""
    name: str
    code: str  # 3-letter country code
    population: int
    gdp_per_capita: float
    olympic_history: Dict[str, int] = None  # sport -> medals
    athletes: List[OlympicAthlete] = None
    
    def __post_init__(self):
        if self.olympic_history is None:
            self.olympic_history = {}
        if self.athletes is None:
            self.athletes = []


@dataclass
class EventResult:
    """Data class for Olympic event results."""
    event_name: str
    sport: str
    venue: str
    date: str
    participants: List[str]
    results: List[Dict[str, Any]]
    gold_medalist: str
    silver_medalist: str
    bronze_medalist: str
    world_record: bool = False
    olympic_record: bool = False


@dataclass
class MedalCount:
    """Data class for Olympic medal counts."""
    country: str
    gold: int = 0
    silver: int = 0
    bronze: int = 0
    total: int = 0


class OlympicData:
    """Contains Olympic data and configuration."""
    
    # Sample Olympic countries
    COUNTRIES = [
        OlympicCountry("United States", "USA", 331000000, 69287.54, 
                      {"Swimming": 246, "Athletics": 342, "Gymnastics": 184, "Basketball": 23}),
        OlympicCountry("China", "CHN", 1439000000, 12556.33,
                      {"Swimming": 67, "Athletics": 22, "Gymnastics": 54, "Table Tennis": 60}),
        OlympicCountry("Great Britain", "GBR", 67200000, 46510.28,
                      {"Swimming": 73, "Athletics": 55, "Cycling": 38, "Rowing": 31}),
        OlympicCountry("Russia", "RUS", 144100000, 10126.72,
                      {"Swimming": 52, "Athletics": 78, "Gymnastics": 45, "Wrestling": 62}),
        OlympicCountry("Germany", "GER", 83190000, 51216.84,
                      {"Swimming": 78, "Athletics": 67, "Rowing": 43, "Canoeing": 32}),
        OlympicCountry("Australia", "AUS", 25690000, 60443.29,
                      {"Swimming": 190, "Athletics": 21, "Cycling": 14, "Rowing": 11}),
        OlympicCountry("Netherlands", "NED", 17130000, 52331.98,
                      {"Swimming": 35, "Athletics": 8, "Cycling": 18, "Speed Skating": 42}),
        OlympicCountry("France", "FRA", 67390000, 43658.98,
                      {"Swimming": 38, "Athletics": 14, "Fencing": 42, "Cycling": 41}),
        OlympicCountry("Italy", "ITA", 60360000, 35220.08,
                      {"Swimming": 38, "Athletics": 19, "Fencing": 49, "Cycling": 33}),
        OlympicCountry("Japan", "JPN", 125800000, 39312.22,
                      {"Swimming": 22, "Athletics": 7, "Judo": 84, "Gymnastics": 31})
    ]
    
    # Sample Olympic events
    EVENTS = [
        OlympicEvent("100m Freestyle", "Swimming", "Men", "Individual", "Time", "Aquatic Center", "2024-07-27"),
        OlympicEvent("100m Freestyle", "Swimming", "Women", "Individual", "Time", "Aquatic Center", "2024-07-27"),
        OlympicEvent("100m Sprint", "Athletics", "Men", "Individual", "Time", "Olympic Stadium", "2024-07-30"),
        OlympicEvent("100m Sprint", "Athletics", "Women", "Individual", "Time", "Olympic Stadium", "2024-07-30"),
        OlympicEvent("Long Jump", "Athletics", "Men", "Individual", "Distance", "Olympic Stadium", "2024-08-02"),
        OlympicEvent("Long Jump", "Athletics", "Women", "Individual", "Distance", "Olympic Stadium", "2024-08-02"),
        OlympicEvent("All-Around", "Gymnastics", "Men", "Individual", "Judged", "Gymnastics Arena", "2024-07-29"),
        OlympicEvent("All-Around", "Gymnastics", "Women", "Individual", "Judged", "Gymnastics Arena", "2024-07-29"),
        OlympicEvent("Road Race", "Cycling", "Men", "Individual", "Time", "Road Course", "2024-08-03"),
        OlympicEvent("Road Race", "Cycling", "Women", "Individual", "Time", "Road Course", "2024-08-03"),
        OlympicEvent("Team Pursuit", "Cycling", "Men", "Team", "Time", "Velodrome", "2024-08-04"),
        OlympicEvent("Team Pursuit", "Cycling", "Women", "Team", "Time", "Velodrome", "2024-08-04"),
        OlympicEvent("Basketball", "Basketball", "Men", "Team", "Points", "Basketball Arena", "2024-08-10"),
        OlympicEvent("Basketball", "Basketball", "Women", "Team", "Points", "Basketball Arena", "2024-08-10")
    ]
    
    # Sample athletes
    ATHLETES = [
        # Swimming athletes
        OlympicAthlete("Caeleb Dressel", "USA", "Swimming", "100m Freestyle", 27, "Men", 188, 86,
                      9.0, 9.5, 8.5, 9.8, 9.0, 8.5, 47.02, 47.15, 1, 2, 7, 5),
        OlympicAthlete("Kyle Chalmers", "AUS", "Swimming", "100m Freestyle", 25, "Men", 194, 88,
                      8.5, 9.3, 8.8, 9.2, 8.8, 8.0, 47.08, 47.25, 2, 2, 5, 2),
        OlympicAthlete("Emma McKeon", "AUS", "Swimming", "100m Freestyle", 29, "Women", 170, 65,
                      8.0, 9.2, 8.5, 9.5, 9.2, 9.0, 51.96, 52.10, 1, 3, 11, 7),
        OlympicAthlete("Sarah Sjostrom", "SWE", "Swimming", "100m Freestyle", 30, "Women", 180, 70,
                      8.5, 9.4, 8.0, 9.6, 9.0, 9.5, 51.71, 52.05, 2, 4, 8, 3),
        
        # Athletics athletes
        OlympicAthlete("Fred Kerley", "USA", "Athletics", "100m Sprint", 28, "Men", 185, 79,
                      9.5, 9.8, 8.5, 9.0, 8.8, 7.5, 9.76, 9.78, 1, 1, 2, 1),
        OlympicAthlete("Ferdinand Omanyala", "KEN", "Athletics", "100m Sprint", 27, "Men", 175, 70,
                      9.0, 9.7, 8.0, 8.8, 8.5, 6.5, 9.77, 9.79, 2, 1, 0, 0),
        OlympicAthlete("Sha'Carri Richardson", "USA", "Athletics", "100m Sprint", 23, "Women", 165, 55,
                      8.5, 9.6, 8.0, 9.2, 8.8, 6.0, 10.65, 10.67, 1, 1, 0, 0),
        OlympicAthlete("Elaine Thompson-Herah", "JAM", "Athletics", "100m Sprint", 31, "Women", 167, 57,
                      9.0, 9.7, 8.5, 9.0, 9.2, 8.5, 10.54, 10.56, 2, 3, 5, 3),
        
        # Gymnastics athletes
        OlympicAthlete("Daiki Hashimoto", "JPN", "Gymnastics", "All-Around", 22, "Men", 167, 58,
                      8.5, 9.0, 8.0, 9.8, 9.5, 7.0, 88.465, 88.200, 1, 1, 2, 1),
        OlympicAthlete("Brody Malone", "USA", "Gymnastics", "All-Around", 23, "Men", 170, 65,
                      8.0, 8.8, 7.5, 9.5, 9.0, 6.5, 87.098, 86.500, 3, 1, 0, 0),
        OlympicAthlete("Simone Biles", "USA", "Gymnastics", "All-Around", 26, "Women", 142, 47,
                      8.0, 9.2, 8.5, 9.9, 9.8, 9.5, 58.432, 58.100, 1, 3, 32, 7),
        OlympicAthlete("Rebeca Andrade", "BRA", "Gymnastics", "All-Around", 24, "Women", 150, 48,
                      8.5, 9.0, 8.0, 9.6, 9.2, 7.5, 57.332, 57.000, 2, 1, 2, 1),
        
        # Cycling athletes
        OlympicAthlete("Wout van Aert", "BEL", "Cycling", "Road Race", 29, "Men", 190, 78,
                      9.5, 9.0, 9.2, 8.8, 9.0, 8.5, 0, 0, 1, 1, 0, 0),
        OlympicAthlete("Mathieu van der Poel", "NED", "Cycling", "Road Race", 28, "Men", 184, 75,
                      9.0, 9.3, 8.8, 9.0, 8.8, 8.0, 0, 0, 2, 1, 0, 0),
        OlympicAthlete("Annemiek van Vleuten", "NED", "Cycling", "Road Race", 40, "Women", 168, 58,
                      8.5, 8.8, 9.0, 8.5, 9.5, 9.5, 0, 0, 1, 1, 2, 1),
        OlympicAthlete("Marianne Vos", "NED", "Cycling", "Road Race", 36, "Women", 168, 58,
                      8.0, 9.0, 8.8, 8.8, 9.2, 9.8, 0, 0, 2, 1, 4, 1)
    ]


class OlympicSimulator:
    """Handles Olympic event simulation."""
    
    @staticmethod
    def calculate_athlete_performance(athlete: OlympicAthlete, event: OlympicEvent) -> float:
        """Calculate athlete's performance score for an event."""
        # Base performance based on athlete ratings
        base_performance = (
            athlete.strength_rating * 0.2 +
            athlete.speed_rating * 0.3 +
            athlete.endurance_rating * 0.2 +
            athlete.technique_rating * 0.2 +
            athlete.mental_rating * 0.1
        )
        
        # Experience bonus
        experience_bonus = athlete.experience_rating * 0.1
        
        # Personal best factor
        pb_factor = 1.0
        if athlete.personal_best > 0:
            pb_factor = 1.0 + (athlete.personal_best - athlete.season_best) / athlete.personal_best * 0.1
        
        # Random variation
        variation = random.gauss(0, 0.5)
        
        final_performance = (base_performance + experience_bonus) * pb_factor + variation
        return max(1.0, min(10.0, final_performance))
    
    @staticmethod
    def simulate_individual_event(event: OlympicEvent) -> EventResult:
        """Simulate an individual Olympic event."""
        if not event.participants:
            return None
        
        # Calculate performance scores for all participants
        performances = []
        for athlete in event.participants:
            score = OlympicSimulator.calculate_athlete_performance(athlete, event)
            performances.append({
                "athlete": athlete.name,
                "country": athlete.country,
                "score": score,
                "personal_best": athlete.personal_best,
                "world_ranking": athlete.world_ranking
            })
        
        # Sort by performance (higher is better for most events)
        performances.sort(key=lambda x: x["score"], reverse=True)
        
        # Determine medalists
        gold_medalist = performances[0]["athlete"]
        silver_medalist = performances[1]["athlete"] if len(performances) > 1 else "None"
        bronze_medalist = performances[2]["athlete"] if len(performances) > 2 else "None"
        
        # Check for records (simplified)
        world_record = random.random() < 0.05  # 5% chance
        olympic_record = random.random() < 0.1  # 10% chance
        
        return EventResult(
            event_name=event.name,
            sport=event.sport,
            venue=event.venue,
            date=event.date,
            participants=[p["athlete"] for p in performances],
            results=performances,
            gold_medalist=gold_medalist,
            silver_medalist=silver_medalist,
            bronze_medalist=bronze_medalist,
            world_record=world_record,
            olympic_record=olympic_record
        )
    
    @staticmethod
    def simulate_team_event(event: OlympicEvent) -> EventResult:
        """Simulate a team Olympic event."""
        if not event.participants:
            return None
        
        # Group athletes by country
        country_teams = {}
        for athlete in event.participants:
            if athlete.country not in country_teams:
                country_teams[athlete.country] = []
            country_teams[athlete.country].append(athlete)
        
        # Calculate team scores
        team_performances = []
        for country, athletes in country_teams.items():
            team_score = sum(OlympicSimulator.calculate_athlete_performance(athlete, event) 
                           for athlete in athletes) / len(athletes)
            team_performances.append({
                "country": country,
                "athletes": [a.name for a in athletes],
                "score": team_score
            })
        
        # Sort by team score
        team_performances.sort(key=lambda x: x["score"], reverse=True)
        
        # Determine medalists
        gold_medalist = team_performances[0]["country"]
        silver_medalist = team_performances[1]["country"] if len(team_performances) > 1 else "None"
        bronze_medalist = team_performances[2]["country"] if len(team_performances) > 2 else "None"
        
        return EventResult(
            event_name=event.name,
            sport=event.sport,
            venue=event.venue,
            date=event.date,
            participants=[p["country"] for p in team_performances],
            results=team_performances,
            gold_medalist=gold_medalist,
            silver_medalist=silver_medalist,
            bronze_medalist=bronze_medalist
        )
    
    @staticmethod
    def simulate_event(event: OlympicEvent) -> EventResult:
        """Simulate any Olympic event."""
        if event.event_type == "Individual":
            return OlympicSimulator.simulate_individual_event(event)
        else:
            return OlympicSimulator.simulate_team_event(event)


class OlympicAnalyzer:
    """Analyzes Olympic statistics and provides insights."""
    
    def __init__(self):
        self.countries = self._load_countries()
        self.events = self._load_events()
        self.athletes = self._load_athletes()
    
    def _load_countries(self) -> List[OlympicCountry]:
        """Load countries from data."""
        countries = []
        for country_data in OlympicData.COUNTRIES:
            country = OlympicCountry(**{k: v for k, v in asdict(country_data).items() 
                                      if k not in ['olympic_history', 'athletes']})
            country.olympic_history = country_data.olympic_history
            country.athletes = [a for a in OlympicData.ATHLETES if a.country == country.name]
            countries.append(country)
        return countries
    
    def _load_events(self) -> List[OlympicEvent]:
        """Load events from data."""
        return OlympicData.EVENTS.copy()
    
    def _load_athletes(self) -> List[OlympicAthlete]:
        """Load athletes from data."""
        return OlympicData.ATHLETES.copy()
    
    def get_country_by_name(self, name: str) -> Optional[OlympicCountry]:
        """Get country by name."""
        for country in self.countries:
            if country.name == name:
                return country
        return None
    
    def get_athlete_by_name(self, name: str) -> Optional[OlympicAthlete]:
        """Get athlete by name."""
        for athlete in self.athletes:
            if athlete.name == name:
                return athlete
        return None
    
    def get_event_by_name(self, name: str, gender: str = "Men") -> Optional[OlympicEvent]:
        """Get event by name and gender."""
        for event in self.events:
            if event.name == name and event.gender == gender:
                return event
        return None
    
    def analyze_athlete(self, athlete_name: str) -> Dict[str, Any]:
        """Analyze individual athlete performance."""
        athlete = self.get_athlete_by_name(athlete_name)
        if not athlete:
            return {"error": "Athlete not found"}
        
        # Calculate overall rating
        overall_rating = (
            athlete.strength_rating + athlete.speed_rating + athlete.endurance_rating +
            athlete.technique_rating + athlete.mental_rating + athlete.experience_rating
        ) / 6.0
        
        # Sport-specific analysis
        sport_strengths = {
            "Swimming": athlete.speed_rating + athlete.endurance_rating,
            "Athletics": athlete.speed_rating + athlete.strength_rating,
            "Gymnastics": athlete.technique_rating + athlete.mental_rating,
            "Cycling": athlete.endurance_rating + athlete.strength_rating
        }
        
        # Career analysis
        career_stats = {
            "olympic_appearances": athlete.olympic_appearances,
            "total_medals": athlete.medals_won,
            "gold_medals": athlete.gold_medals,
            "world_ranking": athlete.world_ranking
        }
        
        return {
            "athlete": asdict(athlete),
            "analysis": {
                "overall_rating": overall_rating,
                "sport_strengths": sport_strengths,
                "career_stats": career_stats,
                "medal_efficiency": athlete.gold_medals / max(1, athlete.medals_won)
            }
        }
    
    def get_country_analysis(self, country_name: str) -> Dict[str, Any]:
        """Analyze country's Olympic performance."""
        country = self.get_country_by_name(country_name)
        if not country:
            return {"error": "Country not found"}
        
        # Sport analysis
        sport_medals = country.olympic_history
        total_medals = sum(sport_medals.values())
        best_sport = max(sport_medals.items(), key=lambda x: x[1]) if sport_medals else ("None", 0)
        
        # Athlete analysis
        athletes = country.athletes
        avg_athlete_rating = statistics.mean([
            (a.strength_rating + a.speed_rating + a.endurance_rating + 
             a.technique_rating + a.mental_rating + a.experience_rating) / 6
            for a in athletes
        ]) if athletes else 0
        
        # Top athletes
        top_athletes = sorted(athletes, 
                            key=lambda a: (a.strength_rating + a.speed_rating + a.endurance_rating + 
                                         a.technique_rating + a.mental_rating + a.experience_rating) / 6,
                            reverse=True)[:5]
        
        return {
            "country": asdict(country),
            "analysis": {
                "total_medals": total_medals,
                "best_sport": best_sport[0],
                "best_sport_medals": best_sport[1],
                "avg_athlete_rating": avg_athlete_rating,
                "athlete_count": len(athletes),
                "top_athletes": [asdict(a) for a in top_athletes]
            }
        }
    
    def simulate_olympics(self, events_to_simulate: List[str] = None) -> Dict[str, Any]:
        """Simulate a full Olympic Games."""
        if events_to_simulate is None:
            events_to_simulate = [event.name for event in self.events]
        
        results = []
        medal_counts = {country.name: MedalCount(country.name) for country in self.countries}
        
        # Simulate each event
        for event_name in events_to_simulate:
            for gender in ["Men", "Women"]:
                event = self.get_event_by_name(event_name, gender)
                if not event:
                    continue
                
                # Assign athletes to event
                event.participants = [a for a in self.athletes 
                                    if a.sport == event.sport and a.gender == event.gender]
                
                if event.participants:
                    result = OlympicSimulator.simulate_event(event)
                    if result:
                        results.append(asdict(result))
                        
                        # Update medal counts
                        if result.gold_medalist != "None":
                            if result.gold_medalist in medal_counts:
                                medal_counts[result.gold_medalist].gold += 1
                                medal_counts[result.gold_medalist].total += 1
                        
                        if result.silver_medalist != "None":
                            if result.silver_medalist in medal_counts:
                                medal_counts[result.silver_medalist].silver += 1
                                medal_counts[result.silver_medalist].total += 1
                        
                        if result.bronze_medalist != "None":
                            if result.bronze_medalist in medal_counts:
                                medal_counts[result.bronze_medalist].bronze += 1
                                medal_counts[result.bronze_medalist].total += 1
        
        # Sort medal counts
        sorted_medals = sorted(medal_counts.values(), 
                             key=lambda x: (x.gold, x.silver, x.bronze), reverse=True)
        
        return {
            "olympic_results": results,
            "medal_table": [asdict(medal) for medal in sorted_medals],
            "total_events": len(results)
        }
    
    def predict_medals(self, country_name: str) -> Dict[str, Any]:
        """Predict medal count for a country."""
        country = self.get_country_by_name(country_name)
        if not country:
            return {"error": "Country not found"}
        
        # Analyze country's strengths
        sport_strengths = country.olympic_history
        total_historical_medals = sum(sport_strengths.values())
        
        # Calculate prediction based on historical performance and current athletes
        athlete_strength = len(country.athletes) * 0.1
        historical_factor = total_historical_medals * 0.05
        
        predicted_gold = int(athlete_strength + historical_factor + random.gauss(0, 2))
        predicted_silver = int(predicted_gold * 0.8 + random.gauss(0, 1))
        predicted_bronze = int(predicted_gold * 0.6 + random.gauss(0, 1))
        
        return {
            "country": country_name,
            "prediction": {
                "gold": max(0, predicted_gold),
                "silver": max(0, predicted_silver),
                "bronze": max(0, predicted_bronze),
                "total": max(0, predicted_gold + predicted_silver + predicted_bronze)
            },
            "factors": {
                "athlete_count": len(country.athletes),
                "historical_medals": total_historical_medals,
                "best_sports": list(sport_strengths.keys())[:3]
            }
        }
    
    def get_sport_analysis(self, sport_name: str) -> Dict[str, Any]:
        """Analyze performance in a specific sport."""
        sport_athletes = [a for a in self.athletes if a.sport == sport_name]
        
        if not sport_athletes:
            return {"error": "No athletes found for this sport"}
        
        # Country dominance
        country_performance = {}
        for athlete in sport_athletes:
            if athlete.country not in country_performance:
                country_performance[athlete.country] = {
                    "athletes": 0,
                    "avg_rating": 0,
                    "total_medals": 0
                }
            country_performance[athlete.country]["athletes"] += 1
            country_performance[athlete.country]["total_medals"] += athlete.medals_won
        
        # Calculate average ratings
        for country in country_performance:
            country_athletes = [a for a in sport_athletes if a.country == country]
            avg_rating = statistics.mean([
                (a.strength_rating + a.speed_rating + a.endurance_rating + 
                 a.technique_rating + a.mental_rating + a.experience_rating) / 6
                for a in country_athletes
            ])
            country_performance[country]["avg_rating"] = avg_rating
        
        # Top countries
        top_countries = sorted(country_performance.items(), 
                             key=lambda x: x[1]["avg_rating"], reverse=True)[:5]
        
        return {
            "sport": sport_name,
            "total_athletes": len(sport_athletes),
            "country_analysis": dict(top_countries),
            "top_athletes": [asdict(a) for a in sorted(sport_athletes, 
                                                      key=lambda a: a.world_ranking)[:10]]
        }


def main():
    """Main function to demonstrate Olympic analysis."""
    analyzer = OlympicAnalyzer()
    
    print("=== Olympic Sports Analysis Tool ===\n")
    
    # Athlete analysis
    print("1. Athlete Analysis - Simone Biles:")
    athlete_analysis = analyzer.analyze_athlete("Simone Biles")
    print(f"Overall Rating: {athlete_analysis['analysis']['overall_rating']:.2f}")
    print(f"Olympic Appearances: {athlete_analysis['athlete']['olympic_appearances']}")
    print(f"Total Medals: {athlete_analysis['athlete']['medals_won']}")
    print(f"Gold Medals: {athlete_analysis['athlete']['gold_medals']}")
    print()
    
    # Country analysis
    print("2. Country Analysis - United States:")
    country_analysis = analyzer.get_country_analysis("United States")
    print(f"Total Historical Medals: {country_analysis['analysis']['total_medals']}")
    print(f"Best Sport: {country_analysis['analysis']['best_sport']}")
    print(f"Athlete Count: {country_analysis['analysis']['athlete_count']}")
    print()
    
    # Event simulation
    print("3. Event Simulation - Men's 100m Freestyle:")
    event = analyzer.get_event_by_name("100m Freestyle", "Men")
    if event:
        event.participants = [a for a in analyzer.athletes 
                            if a.sport == "Swimming" and a.gender == "Men"]
        result = OlympicSimulator.simulate_event(event)
        if result:
            print(f"Gold: {result.gold_medalist}")
            print(f"Silver: {result.silver_medalist}")
            print(f"Bronze: {result.bronze_medalist}")
    print()
    
    # Medal prediction
    print("4. Medal Prediction - China:")
    prediction = analyzer.predict_medals("China")
    print(f"Predicted Gold: {prediction['prediction']['gold']}")
    print(f"Predicted Silver: {prediction['prediction']['silver']}")
    print(f"Predicted Bronze: {prediction['prediction']['bronze']}")
    print(f"Predicted Total: {prediction['prediction']['total']}")
    print()
    
    # Sport analysis
    print("5. Sport Analysis - Swimming:")
    sport_analysis = analyzer.get_sport_analysis("Swimming")
    print(f"Total Athletes: {sport_analysis['total_athletes']}")
    print("Top Countries:")
    for i, (country, stats) in enumerate(list(sport_analysis['country_analysis'].items())[:3], 1):
        print(f"{i}. {country} - {stats['athletes']} athletes, {stats['avg_rating']:.2f} avg rating")
    
    print("\n=== Analysis Complete ===")


if __name__ == "__main__":
    main() 