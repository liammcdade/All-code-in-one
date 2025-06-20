# This script provides information about items that can be cooked/smelted
# and items that can be used as fuel in a Minecraft furnace.


def get_smeltable_items_data():
    """
    Returns a dictionary of items that can be smelted/cooked in a Minecraft furnace
    and the time it takes (in seconds) for ONE item.
    Standard smelting time is 10 seconds (200 game ticks) per item.
    """
    return {
        "iron ore": {
            "output": "Iron Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining in caves/mountains (common).",
        },
        "gold ore": {
            "output": "Gold Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining in caves/badlands (less common).",
        },
        "copper ore": {
            "output": "Copper Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining in caves (common).",
        },
        "raw iron": {
            "output": "Iron Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining deepslate iron ore in caves.",
        },
        "raw gold": {
            "output": "Gold Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining deepslate gold ore in caves/badlands.",
        },
        "raw copper": {
            "output": "Copper Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining deepslate copper ore in caves.",
        },
        "ancient debris": {
            "output": "Netherite Scrap",
            "time_per_item_seconds": 10,
            "source": "Mining in the Nether (Y-level 15-22, very rare).",
        },
        "nether gold ore": {
            "output": "Gold Ingot",
            "time_per_item_seconds": 10,
            "source": "Mining in the Nether (common).",
        },
        "coal ore": {
            "output": "Coal",
            "time_per_item_seconds": 10,
            "source": "Mining in caves/mountains (common).",
        },
        "lapis lazuli ore": {
            "output": "Lapis Lazuli",
            "time_per_item_seconds": 10,
            "source": "Mining in caves (Y-level -64 to 64).",
        },
        "redstone ore": {
            "output": "Redstone Dust",
            "time_per_item_seconds": 10,
            "source": "Mining in caves (Y-level -64 to 15).",
        },
        "diamond ore": {
            "output": "Diamond",
            "time_per_item_seconds": 10,
            "source": "Mining in caves (Y-level -64 to -50, rare).",
        },
        "emerald ore": {
            "output": "Emerald",
            "time_per_item_seconds": 10,
            "source": "Mining in mountains (extreme hills biomes, rare).",
        },
        "nether quartz ore": {
            "output": "Nether Quartz",
            "time_per_item_seconds": 10,
            "source": "Mining in the Nether (common).",
        },
        "raw beef": {
            "output": "Steak",
            "time_per_item_seconds": 10,
            "source": "Killing Cows, Mooshrooms.",
        },
        "raw porkchop": {
            "output": "Cooked Porkchop",
            "time_per_item_seconds": 10,
            "source": "Killing Pigs.",
        },
        "raw chicken": {
            "output": "Cooked Chicken",
            "time_per_item_seconds": 10,
            "source": "Killing Chickens.",
        },
        "raw mutton": {
            "output": "Cooked Mutton",
            "time_per_item_seconds": 10,
            "source": "Killing Sheep.",
        },
        "raw rabbit": {
            "output": "Cooked Rabbit",
            "time_per_item_seconds": 10,
            "source": "Killing Rabbits.",
        },
        "raw cod": {
            "output": "Cooked Cod",
            "time_per_item_seconds": 10,
            "source": "Fishing or killing Cod.",
        },
        "raw salmon": {
            "output": "Cooked Salmon",
            "time_per_item_seconds": 10,
            "source": "Fishing or killing Salmon.",
        },
        "potato": {
            "output": "Baked Potato",
            "time_per_item_seconds": 10,
            "source": "Farming, zombie drops.",
        },
        "kelp": {
            "output": "Dried Kelp",
            "time_per_item_seconds": 10,
            "source": "Underwater in oceans (abundant).",
        },
        "chorus fruit": {
            "output": "Popped Chorus Fruit",
            "time_per_item_seconds": 10,
            "source": "Breaking Chorus Plants in The End.",
        },
        "cobblestone": {
            "output": "Stone",
            "time_per_item_seconds": 10,
            "source": "Mining Stone blocks (very common).",
        },
        "stone": {
            "output": "Smooth Stone",
            "time_per_item_seconds": 10,
            "source": "Smelting Cobblestone, found in some structures.",
        },
        "sand": {
            "output": "Glass",
            "time_per_item_seconds": 10,
            "source": "Deserts, beaches, riverbeds (very common).",
        },
        "red sand": {
            "output": "Red Glass",
            "time_per_item_seconds": 10,
            "source": "Badlands biomes (common).",
        },
        "netherrack": {
            "output": "Nether Brick",
            "time_per_item_seconds": 10,
            "source": "Mining in the Nether (very common).",
        },
        "clay ball": {
            "output": "Brick",
            "time_per_item_seconds": 10,
            "source": "Breaking Clay blocks in rivers/swamps/oceans.",
        },
        "wet sponge": {
            "output": "Dry Sponge",
            "time_per_item_seconds": 10,
            "source": "Defeating Elder Guardians in Ocean Monuments.",
        },
        "cactus": {
            "output": "Green Dye",
            "time_per_item_seconds": 10,
            "source": "Deserts (common).",
        },
        "basalt": {
            "output": "Smooth Basalt",
            "time_per_item_seconds": 10,
            "source": "Mining in Basalt Deltas (Nether).",
        },
        "cobbled deepslate": {
            "output": "Deepslate",
            "time_per_item_seconds": 10,
            "source": "Mining Deepslate (very common at Y-level 0 and below).",
        },
        "deepslate": {
            "output": "Smooth Deepslate",
            "time_per_item_seconds": 10,
            "source": "Smelting Cobbled Deepslate.",
        },
        "terracotta": {
            "output": "Glazed Terracotta",
            "time_per_item_seconds": 10,
            "source": "Mining Clay (to get Clay blocks), then craft and smelt.",
        },  # Assumes uncolored terracotta for simplicity
        "stone bricks": {
            "output": "Cracked Stone Bricks",
            "time_per_item_seconds": 10,
            "source": "Crafting from Stone, found in structures like strongholds/dungeons.",
        },
        "deepslate bricks": {
            "output": "Cracked Deepslate Bricks",
            "time_per_item_seconds": 10,
            "source": "Crafting from Deepslate, then smelt.",
        },
        "log": {
            "output": "Charcoal",
            "time_per_item_seconds": 10,
            "source": "Chopping down trees (any type).",
        },  # Any log type
        "stripped log": {
            "output": "Charcoal",
            "time_per_item_seconds": 10,
            "source": "Stripping logs with an axe.",
        },  # Any stripped log type
        "wood": {
            "output": "Charcoal",
            "time_per_item_seconds": 10,
            "source": "Crafting logs into wood blocks.",
        },  # Any wood (block) type
        "stripped wood": {
            "output": "Charcoal",
            "time_per_item_seconds": 10,
            "source": "Stripping wood blocks with an axe.",
        },  # Any stripped wood type
        "iron helmet": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron helmets.",
        },
        "iron chestplate": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron chestplates.",
        },
        "iron leggings": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron leggings.",
        },
        "iron boots": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron boots.",
        },
        "iron sword": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron swords.",
        },
        "iron pickaxe": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron pickaxes.",
        },
        "iron axe": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron axes.",
        },
        "iron shovel": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron shovels.",
        },
        "iron hoe": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding iron hoes.",
        },
        "gold helmet": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold helmets.",
        },
        "gold chestplate": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold chestplates.",
        },
        "gold leggings": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold leggings.",
        },
        "gold boots": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold boots.",
        },
        "gold sword": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold swords.",
        },
        "gold pickaxe": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold pickaxes.",
        },
        "gold axe": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold axes.",
        },
        "gold shovel": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold shovels.",
        },
        "gold hoe": {
            "output": "Gold Nugget",
            "time_per_item_seconds": 10,
            "source": "Crafting or finding gold hoes.",
        },
        "chainmail helmet": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Killing zombies/skeletons, trading with villagers.",
        },
        "chainmail chestplate": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Killing zombies/skeletons, trading with villagers.",
        },
        "chainmail leggings": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Killing zombies/skeletons, trading with villagers.",
        },
        "chainmail boots": {
            "output": "Iron Nugget",
            "time_per_item_seconds": 10,
            "source": "Killing zombies/skeletons, trading with villagers.",
        },
    }


def get_fuel_data():
    """
    Returns a dictionary of items that can be used as fuel in a Minecraft furnace
    and the number of items they can smelt (burn duration / 200 game ticks).
    Includes common sources for fuel.
    """
    return {
        "lava bucket": {
            "efficiency": 100,
            "source": "Lava lakes (Overworld/Nether), volcanic areas.",
        },  # Burns for 1000 seconds
        "block of coal": {
            "efficiency": 80,
            "source": "Crafted from 9 Coal.",
        },  # Burns for 800 seconds
        "block of dried kelp": {
            "efficiency": 20,
            "source": "Crafted from 9 Dried Kelp.",
        },  # Burns for 200 seconds
        "blaze rod": {
            "efficiency": 12,
            "source": "Killing Blazes in Nether Fortresses.",
        },  # Burns for 120 seconds
        "coal": {
            "efficiency": 8,
            "source": "Mining Coal Ore in caves/mountains.",
        },  # Burns for 80 seconds
        "charcoal": {
            "efficiency": 8,
            "source": "Smelting Wood/Logs in a furnace.",
        },  # Burns for 80 seconds
        "wooden plank": {
            "efficiency": 1.5,
            "source": "Crafted from Wood/Logs (any type).",
        },  # Any wood plank type, burns for 15 seconds
        "wooden log": {
            "efficiency": 1.5,
            "source": "Chopping down trees (any type).",
        },  # Any wood log type, burns for 15 seconds
        "wooden wood": {
            "efficiency": 1.5,
            "source": "Crafted from Logs (all 6 sides textured as bark).",
        },  # Any wood (block) type, burns for 15 seconds
        "wooden slab": {
            "efficiency": 0.75,
            "source": "Crafted from Wooden Planks (any type).",
        },  # Any wood slab type, burns for 7.5 seconds (Java)
        "stick": {
            "efficiency": 0.5,
            "source": "Crafted from Wooden Planks, breaking leaves.",
        },  # Burns for 5 seconds
        "wooden tool": {
            "efficiency": 1,
            "source": "Crafting wooden tools (e.g., Wooden Pickaxe).",
        },  # e.g., Wooden Pickaxe, burns for 10 seconds
        "wooden weapon": {
            "efficiency": 1,
            "source": "Crafting wooden weapons (e.g., Wooden Sword).",
        },  # e.g., Wooden Sword, burns for 10 seconds
        "sapling": {
            "efficiency": 0.5,
            "source": "Breaking tree leaves (any type).",
        },  # Any sapling type, burns for 5 seconds
        "dead bush": {
            "efficiency": 0.5,
            "source": "Found in deserts/badlands.",
        },  # Burns for 5 seconds
        "bamboo": {
            "efficiency": 0.25,
            "source": "Found in jungles, bamboo forests.",
        },  # Burns for 2.5 seconds
        "wool": {
            "efficiency": 0.5,
            "source": "Shearing sheep.",
        },  # Any wool block, burns for 5 seconds
        "carpet": {
            "efficiency": 0.335,
            "source": "Crafted from Wool (any type).",
        },  # Any carpet type, burns for 3.35 seconds
        "banner": {
            "efficiency": 0.5,
            "source": "Crafted from Wool and Sticks (any type).",
        },  # Any banner type, burns for 5 seconds
        "bookshelf": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Books.",
        },  # Burns for 15 seconds
        "crafting table": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks.",
        },  # Burns for 15 seconds
        "chest": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks.",
        },  # Burns for 15 seconds
        "trapped chest": {
            "efficiency": 1.5,
            "source": "Crafted from a Chest and Tripwire Hook.",
        },  # Burns for 15 seconds
        "jukebox": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and a Diamond.",
        },  # Burns for 15 seconds
        "note block": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Redstone Dust.",
        },  # Burns for 15 seconds
        "boat": {
            "efficiency": 6,
            "source": "Crafted from Wooden Planks (any type).",
        },  # Any boat type, burns for 60 seconds
        "sign": {
            "efficiency": 1,
            "source": "Crafted from Wooden Planks and Sticks (any type).",
        },  # Any sign type, burns for 10 seconds
        "door": {
            "efficiency": 1,
            "source": "Crafted from Wooden Planks (any type).",
        },  # Any wooden door type, burns for 10 seconds
        "fence": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Sticks (any type).",
        },  # Any wooden fence type, burns for 15 seconds
        "fence gate": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Sticks (any type).",
        },  # Any wooden fence gate type, burns for 15 seconds
        "ladder": {
            "efficiency": 0.5,
            "source": "Crafted from Sticks.",
        },  # Burns for 5 seconds
        "bow": {
            "efficiency": 1,
            "source": "Crafting from Sticks and String.",
        },  # Burns for 10 seconds
        "crossbow": {
            "efficiency": 1,
            "source": "Crafting from Sticks, Iron Ingot, String, and Tripwire Hook.",
        },  # Burns for 10 seconds
        "bowl": {
            "efficiency": 0.5,
            "source": "Crafted from Wooden Planks.",
        },  # Burns for 5 seconds
        "lectern": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Slabs and a Bookshelf.",
        },  # Burns for 15 seconds
        "barrel": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Slabs and Sticks.",
        },  # Burns for 15 seconds
        "loom": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and String.",
        },  # Burns for 15 seconds
        "cartography table": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Paper.",
        },  # Burns for 15 seconds
        "fletching table": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Flint.",
        },  # Burns for 15 seconds
        "smithing table": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Iron Ingots.",
        },  # Burns for 15 seconds
        "composter": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Slabs.",
        },  # Burns for 15 seconds
        "beehive": {
            "efficiency": 1.5,
            "source": "Crafted from Wooden Planks and Honeycomb.",
        },  # Burns for 15 seconds
        "campfire": {
            "efficiency": 1.5,
            "source": "Crafted from Logs, Sticks, and Coal/Charcoal.",
        },  # Burns for 15 seconds
        "soul campfire": {
            "efficiency": 1.5,
            "source": "Crafted from Logs, Sticks, and Soul Soil/Sand.",
        },  # Burns for 15 seconds
        "scaffolding": {
            "efficiency": 0.25,
            "source": "Crafted from Bamboo and String.",
        },  # Burns for 2.5 seconds
    }


def convert_seconds_to_display(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return (
        f"{minutes} minute(s) and {remaining_seconds} second(s)"
        if minutes
        else f"{remaining_seconds} second(s)"
    )


def lookup_item_info(item_name, smeltable_data, fuel_data):
    normalized = item_name.lower().strip()
    smelting_key = next((k for k in smeltable_data if normalized in k), None)
    fuel_key = next((k for k in fuel_data if normalized in k), None)

    is_smeltable = smelting_key is not None
    is_fuel = fuel_key is not None

    if is_smeltable and is_fuel:
        print(f"\n'{item_name.title()}' can be both smelted/cooked AND used as fuel:")
        smelting = smeltable_data[smelting_key]
        fuel = fuel_data[fuel_key]
        print(
            f"  - Smelting: Produces '{smelting['output']}' in {convert_seconds_to_display(smelting['time_per_item_seconds'])}. Source: {smelting['source']}"
        )
        print(
            f"  - Fuel: Can smelt {fuel['efficiency']} item(s). Source: {fuel['source']}"
        )
    elif is_smeltable:
        smelting = smeltable_data[smelting_key]
        print(
            f"\n'{item_name.title()}' can be smelted/cooked into '{smelting['output']}' in {convert_seconds_to_display(smelting['time_per_item_seconds'])}. Source: {smelting['source']}"
        )
    elif is_fuel:
        fuel = fuel_data[fuel_key]
        print(
            f"\n'{item_name.title()}' can be used as fuel to smelt {fuel['efficiency']} item(s). Source: {fuel['source']}"
        )
    else:
        print(f"\n'{item_name.title()}' is not a recognized smeltable or fuel item.")


def display_all_smeltable_items(data):
    print("\n--- Minecraft Furnace Smeltable/Cookable Items ---")
    print(
        "{:<25} {:<20} {:<20} {:<30}".format(
            "Input Item", "Output Item", "Time Per Item", "Primary Source"
        )
    )
    print("-" * 95)
    for item_name, info in sorted(data.items()):
        print(
            "{:<25} {:<20} {:<20} {:<30}".format(
                item_name.title(),
                info["output"],
                convert_seconds_to_display(info["time_per_item_seconds"]),
                info["source"],
            )
        )
    print("-" * 95)


def display_all_fuel_items(data):
    print("\n--- Minecraft Furnace Fuel Items ---")
    print("{:<25} {:<20} {:<30}".format("Fuel Item", "Items Smelted", "Primary Source"))
    print("-" * 77)
    for item_name, info in sorted(
        data.items(), key=lambda i: i[1]["efficiency"], reverse=True
    ):
        print(
            "{:<25} {:<20} {:<30}".format(
                item_name.title(), info["efficiency"], info["source"]
            )
        )
    print("-" * 77)


def calculate_cooking_potential():
    smeltable_data = get_smeltable_items_data()
    fuel_data = get_fuel_data()

    print("\n--- Calculate Your Minecraft Cooking Potential ---")
    fuel_type = (
        input("What type of fuel do you want to use (e.g., 'coal', 'lava bucket')? ")
        .lower()
        .strip()
    )
    try:
        fuel_quantity = int(
            input(f"How many '{fuel_type.title()}' do you have? ").strip()
        )
        if fuel_quantity < 0:
            print("Fuel quantity must be non-negative.")
            return
    except ValueError:
        print("Invalid quantity. Must be a number.")
        return

    fuel_key = next((k for k in fuel_data if fuel_type in k), None)
    if not fuel_key:
        print(f"'{fuel_type.title()}' is not a recognized fuel.")
        return

    fuel_info = fuel_data[fuel_key]
    capacity = fuel_info["efficiency"] * fuel_quantity
    print(
        f"\nYou can smelt {capacity} item(s) using {fuel_quantity} {fuel_type.title()}(s). Source: {fuel_info['source']}"
    )

    print(
        "\nEnter smeltable items and quantities (e.g., 'raw beef 10'). Type 'done' to finish."
    )
    user_materials = {}
    while True:
        line = input("Item and quantity: ").lower().strip()
        if line == "done":
            break
        try:
            name, qty = line.rsplit(" ", 1)
            qty = int(qty)
            if qty < 0:
                raise ValueError
        except ValueError:
            print("Invalid format. Use 'item_name quantity' with a positive number.")
            continue

        match_key = next((k for k in smeltable_data if name in k), None)
        if not match_key:
            print(f"'{name.title()}' is not a valid smeltable item.")
            continue
        user_materials[match_key] = user_materials.get(match_key, 0) + qty

    if not user_materials:
        print("No items entered. Returning.")
        return

    print("\n--- Cooking Results ---")
    cooked_total = 0
    leftover = {}

    for item, qty in user_materials.items():
        cook = min(qty, capacity)
        cooked_total += cook
        capacity -= cook
        if cook > 0:
            print(
                f"Cooked {cook} of {item.title()} into {smeltable_data[item]['output']}."
            )
        if qty > cook:
            remaining = qty - cook
            leftover[item] = remaining
            print(
                f"Could not cook {remaining} of {item.title()}. Need approx. {remaining / fuel_info['efficiency']:.2f} more {fuel_type.title()}(s)."
            )

    print(f"\nTotal cooked: {cooked_total} item(s). Remaining capacity: {capacity}")
    if not leftover:
        print("All items successfully cooked.")


def main():
    smeltable_data = get_smeltable_items_data()
    fuel_data = get_fuel_data()
    print("Welcome to the Minecraft Furnace Information Tool!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Look up information for a specific item (smeltable/fuel)")
        print("2. List all smeltable/cookable items")
        print("3. List all fuel items (by efficiency)")
        print("4. Calculate cooking potential from your materials")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            item = input("Enter item name: ")
            lookup_item_info(item, smeltable_data, fuel_data)
        elif choice == "2":
            display_all_smeltable_items(smeltable_data)
        elif choice == "3":
            display_all_fuel_items(fuel_data)
        elif choice == "4":
            calculate_cooking_potential()
        elif choice == "5":
            print("Exiting. Happy crafting!")
            break
        else:
            print("Invalid input. Enter a number 1–5.")


if __name__ == "__main__":
    main()
