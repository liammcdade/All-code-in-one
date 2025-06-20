import random

# Array of 150 diverse games with categories
games = [
    {"title": "The Witcher 3: Wild Hunt", "category": "RPG"},
    {"title": "Grand Theft Auto V", "category": "Action-Adventure"},
    {"title": "The Legend of Zelda: Breath of the Wild", "category": "Action-Adventure"},
    {"title": "Red Dead Redemption 2", "category": "Action-Adventure"},
    {"title": "Cyberpunk 2077", "category": "RPG"},
    {"title": "Elden Ring", "category": "RPG"},
    {"title": "God of War (2018)", "category": "Action-Adventure"},
    {"title": "Uncharted 4: A Thief's End", "category": "Action-Adventure"},
    {"title": "Horizon Zero Dawn", "category": "Action RPG"},
    {"title": "Marvel's Spider-Man", "category": "Action-Adventure"},
    {"title": "Assassin's Creed Valhalla", "category": "Action RPG"},
    {"title": "Minecraft", "category": "Sandbox"},
    {"title": "Fortnite", "category": "Battle Royale"},
    {"title": "Apex Legends", "category": "Battle Royale"},
    {"title": "Counter-Strike 2", "category": "FPS"},
    {"title": "Valorant", "category": "FPS"},
    {"title": "Overwatch 2", "category": "FPS"},
    {"title": "DOOM Eternal", "category": "FPS"},
    {"title": "Resident Evil Village", "category": "Survival Horror"},
    {"title": "Dying Light 2 Stay Human", "category": "Action RPG"},
    {"title": "Stardew Valley", "category": "Simulation"},
    {"title": "Animal Crossing: New Horizons", "category": "Simulation"},
    {"title": "Fall Guys", "category": "Party"},
    {"title": "Among Us", "category": "Social Deduction"},
    {"title": "Rocket League", "category": "Sports"},
    {"title": "FIFA 25", "category": "Sports"},
    {"title": "NBA 2K25", "category": "Sports"},
    {"title": "Forza Horizon 5", "category": "Racing"},
    {"title": "Gran Turismo 7", "category": "Racing"},
    {"title": "Slay the Spire", "category": "Card Battler"},
    {"title": "Hades", "category": "Roguelike"},
    {"title": "Dead Cells", "category": "Roguelike"},
    {"title": "Celeste", "category": "Platformer"},
    {"title": "Hollow Knight", "category": "Metroidvania"},
    {"title": "Ori and the Blind Forest", "category": "Metroidvania"},
    {"title": "Cuphead", "category": "Run and Gun"},
    {"title": "Disco Elysium", "category": "RPG"},
    {"title": "Divinity: Original Sin II", "category": "RPG"},
    {"title": "Baldur's Gate 3", "category": "RPG"},
    {"title": "Pillars of Eternity", "category": "RPG"},
    {"title": "Control", "category": "Action-Adventure"},
    {"title": "Death Stranding", "category": "Action-Adventure"},
    {"title": "Prey (2017)", "category": "FPS"},
    {"title": "Dishonored 2", "category": "Stealth"},
    {"title": "Hitman 3", "category": "Stealth"},
    {"title": "Persona 5 Royal", "category": "JRPG"},
    {"title": "Final Fantasy VII Remake", "category": "JRPG"},
    {"title": "Dragon Quest XI S", "category": "JRPG"},
    {"title": "Genshin Impact", "category": "Action RPG"},
    {"title": "Monster Hunter: World", "category": "Action RPG"},
    {"title": "Nioh 2", "category": "Action RPG"},
    {"title": "Dark Souls III", "category": "Action RPG"},
    {"title": "Sekiro: Shadows Die Twice", "category": "Action-Adventure"},
    {"title": "Bloodborne", "category": "Action RPG"},
    {"title": "Ghost of Tsushima", "category": "Action-Adventure"},
    {"title": "Immortals Fenyx Rising", "category": "Action-Adventure"},
    {"title": "Watch Dogs: Legion", "category": "Action-Adventure"},
    {"title": "Far Cry 6", "category": "FPS"},
    {"title": "Borderlands 3", "category": "FPS"},
    {"title": "Destiny 2", "category": "FPS"},
    {"title": "Call of Duty: Modern Warfare III", "category": "FPS"},
    {"title": "Battlefield 2042", "category": "FPS"},
    {"title": "Rainbow Six Siege", "category": "Tactical FPS"},
    {"title": "Escape from Tarkov", "category": "Tactical FPS"},
    {"title": "Sea of Thieves", "category": "Adventure"},
    {"title": "No Man's Sky", "category": "Exploration"},
    {"title": "Elite Dangerous", "category": "Simulation"},
    {"title": "Kerbal Space Program", "category": "Simulation"},
    {"title": "Cities: Skylines", "category": "City-Building"},
    {"title": "Civilization VI", "category": "Strategy"},
    {"title": "Total War: Warhammer III", "category": "Strategy"},
    {"title": "Age of Empires IV", "category": "RTS"},
    {"title": "StarCraft II", "category": "RTS"},
    {"title": "Dota 2", "category": "MOBA"},
    {"title": "League of Legends", "category": "MOBA"},
    {"title": "Teamfight Tactics", "category": "Auto Battler"},
    {"title": "Hearthstone", "category": "Card Game"},
    {"title": "Magic: The Gathering Arena", "category": "Card Game"},
    {"title": "Legends of Runeterra", "category": "Card Game"},
    {"title": "Phasmophobia", "category": "Horror"},
    {"title": "Outlast", "category": "Horror"},
    {"title": "Amnesia: The Dark Descent", "category": "Horror"},
    {"title": "Subnautica", "category": "Survival"},
    {"title": "Rust", "category": "Survival"},
    {"title": "DayZ", "category": "Survival"},
    {"title": "ARK: Survival Evolved", "category": "Survival"},
    {"title": "The Forest", "category": "Survival Horror"},
    {"title": "Valheim", "category": "Survival"},
    {"title": "Project Zomboid", "category": "Survival"},
    {"title": "Satisfactory", "category": "Factory Building"},
    {"title": "Factorio", "category": "Factory Building"},
    {"title": "Oxygen Not Included", "category": "Simulation"},
    {"title": "RimWorld", "category": "Simulation"},
    {"title": "Crusader Kings III", "category": "Grand Strategy"},
    {"title": "Europa Universalis IV", "category": "Grand Strategy"},
    {"title": "Hearts of Iron IV", "category": "Grand Strategy"},
    {"title": "Stellaris", "category": "Grand Strategy"},
    {"title": "Disco Elysium", "category": "RPG"},
    {"title": "Omori", "category": "RPG"},
    {"title": "Undertale", "category": "RPG"},
    {"title": "Braid", "category": "Puzzle-Platformer"},
    {"title": "Portal 2", "category": "Puzzle"},
    {"title": "The Witness", "category": "Puzzle"},
    {"title": "Baba Is You", "category": "Puzzle"},
    {"title": "Return of the Obra Dinn", "category": "Puzzle"},
    {"title": "Outer Wilds", "category": "Exploration"},
    {"title": "What Remains of Edith Finch", "category": "Walking Simulator"},
    {"title": "Firewatch", "category": "Walking Simulator"},
    {"title": "Gone Home", "category": "Walking Simulator"},
    {"title": "Life is Strange", "category": "Adventure"},
    {"title": "Detroit: Become Human", "category": "Interactive Drama"},
    {"title": "Heavy Rain", "category": "Interactive Drama"},
    {"title": "Beyond: Two Souls", "category": "Interactive Drama"},
    {"title": "Ori and the Will of the Wisps", "category": "Metroidvania"},
    {"title": "Grindstone", "category": "Puzzle"},
    {"title": "The Binding of Isaac: Rebirth", "category": "Roguelike"},
    {"title": "Enter the Gungeon", "category": "Roguelike"},
    {"title": "Risk of Rain 2", "category": "Roguelike"},
    {"title": "Deep Rock Galactic", "category": "FPS"},
    {"title": "Warframe", "category": "Looter Shooter"},
    {"title": "Path of Exile", "category": "ARPG"},
    {"title": "Diablo IV", "category": "ARPG"},
    {"title": "EVE Online", "category": "MMORPG"},
    {"title": "World of Warcraft", "category": "MMORPG"},
    {"title": "Final Fantasy XIV", "category": "MMORPG"},
    {"title": "Guild Wars 2", "category": "MMORPG"},
    {"title": "The Elder Scrolls Online", "category": "MMORPG"},
    {"title": "Black Desert Online", "category": "MMORPG"},
    {"title": "Runescape", "category": "MMORPG"},
    {"title": "Terraria", "category": "Sandbox"},
    {"title": "Starbound", "category": "Sandbox"},
    {"title": "Don't Starve Together", "category": "Survival"},
    {"title": "Oxygen Not Included", "category": "Simulation"},
    {"title": "Two Point Hospital", "category": "Simulation"},
    {"title": "Planet Coaster", "category": "Simulation"},
    {"title": "Zoo Tycoon", "category": "Simulation"},
    {"title": "The Sims 4", "category": "Life Simulation"},
    {"title": "Fallout 4", "category": "RPG"},
    {"title": "The Elder Scrolls V: Skyrim", "category": "RPG"},
    {"title": "Mass Effect Legendary Edition", "category": "RPG"},
    {"title": "Dragon Age: Inquisition", "category": "RPG"},
    {"title": "Starfield", "category": "RPG"},
    {"title": "Zelda: Tears of the Kingdom", "category": "Action-Adventure"},
    {"title": "Super Mario Bros. Wonder", "category": "Platformer"},
    {"title": "Alan Wake 2", "category": "Survival Horror"},
    {"title": "Lies of P", "category": "Action RPG"},
    {"title": "Cyberpunk 2077: Phantom Liberty", "category": "RPG"},
    {"title": "Armored Core VI: Fires of Rubicon", "category": "Action"},
    {"title": "Street Fighter 6", "category": "Fighting"},
    {"title": "Final Fantasy XVI", "category": "Action RPG"},
    {"title": "Star Wars Jedi: Survivor", "category": "Action-Adventure"},
    {"title": "Hogwarts Legacy", "category": "Action RPG"},
    {"title": "Dead Space Remake", "category": "Survival Horror"},
    {"title": "Resident Evil 4 Remake", "category": "Survival Horror"},
    {"title": "Octopath Traveler II", "category": "JRPG"},
    {"title": "Persona 3 Reload", "category": "JRPG"},
    {"title": "Tekken 8", "category": "Fighting"},
    {"title": "Helldivers 2", "category": "Co-op Shooter"},
    {"title": "Palworld", "category": "Survival Crafting"},
    {"title": "Enshrouded", "category": "Survival Crafting"},
    {"title": "Final Fantasy VII Rebirth", "category": "JRPG"},
    {"title": "Prince of Persia: The Lost Crown", "category": "Metroidvania"},
    {"title": "Alone in the Dark (2024)", "category": "Survival Horror"},
    {"title": "Black Myth: Wukong", "category": "Action RPG"},
    {"title": "Avowed", "category": "RPG"},
    {"title": "Fable", "category": "RPG"},
    {"title": "The Outer Worlds 2", "category": "RPG"},
    {"title": "Everwild", "category": "Adventure"},
    {"title": "State of Decay 3", "category": "Survival Horror"},
    {"title": "Indiana Jones and the Great Circle", "category": "Action-Adventure"},
    {"title": "Perfect Dark", "category": "FPS"},
    {"title": "Contraband", "category": "Co-op Action"}
]

def get_categories():
    """Extracts and returns a sorted list of unique categories from the games data."""
    categories = sorted(list(set(game["category"] for game in games)))
    return ["All Categories"] + categories

def suggest_game(category=None):
    """
    Suggests a game based on a specified category or completely randomly.

    Args:
        category (str, optional): The category to filter games by.
                                  If None or "All Categories", a random game from all categories is suggested.

    Returns:
        dict: A dictionary containing the suggested game's title and category,
              or None if no games match the category.
    """
    if category and category != "All Categories":
        filtered_games = [game for game in games if game["category"] == category]
    else:
        filtered_games = games

    if filtered_games:
        return random.choice(filtered_games)
    else:
        return None

def main():
    """Main function to run the game suggester CLI."""
    print("🎮 Welcome to the Game Suggester! 🎲")

    categories = get_categories()

    while True:
        print("\n--- Choose an Option ---")
        for i, cat in enumerate(categories):
            print(f"{i + 1}. {cat}")
        print(f"{len(categories) + 1}. Get a Completely Random Game")

        try:
            choice = int(input(f"Enter your choice (1-{len(categories) + 1}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        suggested_game = None # Initialize to None

        if 1 <= choice <= len(categories):
            selected_category = categories[choice - 1]
            if selected_category == "All Categories":
                suggested_game = suggest_game(None) # Pass None for completely random
            else:
                suggested_game = suggest_game(selected_category)
        elif choice == len(categories) + 1:
            suggested_game = suggest_game(None) # Pass None for completely random
        else:
            print("Invalid choice. Please try again.")
            continue

        if suggested_game:
            print(f"\n✨ Suggested Game: {suggested_game['title']}")
            print(f"✨ Category: {suggested_game['category']}")
        else:
            print("\nNo games found for the selected category.")

        # Ask if the user wants another suggestion
        while True:
            play_again = input("\nWould you like another game suggestion? (yes/no): ").lower().strip()
            if play_again in ["yes", "y"]:
                break # Break out of inner loop to continue to main loop
            elif play_again in ["no", "n"]:
                print("Exiting Game Suggester. Happy gaming!")
                return # Exit the main function, ending the program
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
