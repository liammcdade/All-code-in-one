import tkinter as tk
from tkinter import ttk, scrolledtext
import difflib

item_database = {
    # === Basic/Core Items ===
    "wood planks": {
        "uses": "Basic crafting material, building blocks, crafting tables, sticks.",
        "how_to_get": "Crafted from logs (any type of wood)."
    },
    "crafting table": {
        "uses": "Used to craft most items in the game. Provides a 3x3 crafting grid.",
        "how_to_get": "Crafted from 4 wood planks in a 2x2 grid."
    },
    "stick": {
        "uses": "Crafting tool handles (pickaxes, axes, shovels, swords), torches, ladders, fences.",
        "how_to_get": "Crafted from 2 wood planks (stacked vertically)."
    },
    "coal": {
        "uses": "Fuel for furnaces, crafting torches, crafting fire charges (with gunpowder and blaze powder).",
        "how_to_get": "Mined from coal ore (found commonly underground)."
    },
    "torch": {
        "uses": "Provides light to prevent mob spawns, helps with visibility in dark areas.",
        "how_to_get": "Crafted from 1 coal (or charcoal) and 1 stick."
    },
    "furnace": {
        "uses": "Smelts raw ores into ingots, cooks raw food, converts sand into glass, wood into charcoal, etc.",
        "how_to_get": "Crafted from 8 cobblestone (leaving the center empty)."
    },
    "bed": {
        "uses": "Allows players to skip to daytime, set their spawn point, and sleep through the night (except in The End).",
        "how_to_get": "Crafted from 3 wool (same color) and 3 wood planks."
    },
    "flint and steel": {
        "uses": "Used to light fires, activate Nether Portals, and ignite TNT.",
        "how_to_get": "Crafted from 1 iron ingot and 1 flint."
    },
    "book": {
        "uses": "Crafting bookshelves, enchanting tables, written books, and spell books.",
        "how_to_get": "Crafted from 3 paper and 1 leather."
    },
    "paper": {
        "uses": "Crafting books, maps, and fireworks rockets.",
        "how_to_get": "Crafted from 3 sugar canes."
    },
    "leather": {
        "uses": "Crafting armor, item frames, and books.",
        "how_to_get": "Dropped by cows, mooshrooms, horses, donkeys, mules, and hoglins. Also found in chests."
    },
    "apple": {
        "uses": "Restores hunger. Can be crafted into a Golden Apple for powerful temporary buffs.",
        "how_to_get": "Dropped by oak or dark oak leaves when broken or decayed."
    },
    "golden apple": {
        "uses": "Provides Absorption and Regeneration effects. Can cure zombie villagers.",
        "how_to_get": "Crafted from 1 apple and 8 gold ingots."
    },
    "water bucket": {
        "uses": "Places water blocks, can be used to extinguish fires, create obsidian, farm crops, clear mob spawns.",
        "how_to_get": "Crafted from 3 iron ingots. Fill the empty bucket by right-clicking on a water source block."
    },
    "lava bucket": {
        "uses": "Places lava blocks. Can be used as a strong fuel source in furnaces.",
        "how_to_get": "Crafted from 3 iron ingots. Fill the empty bucket by right-clicking on a lava source block."
    },
    "empty bucket": {
        "uses": "Used to pick up water, lava, or milk.",
        "how_to_get": "Crafted from 3 iron ingots."
    },
    "shears": {
        "uses": "Harvests wool from sheep without harming them. Breaks leaves, ferns, and tall grass instantly.",
        "how_to_get": "Crafted from 2 iron ingots (diagonally)."
    },

    # === Ores, Ingots & Gems ===
    "iron ore": {
        "uses": "Raw material for iron ingots. Can be decorative.",
        "how_to_get": "Mined from iron ore blocks (found commonly underground)."
    },
    "iron ingot": {
        "uses": "Crafting iron tools, armor, buckets, shears, iron blocks, rails, iron doors.",
        "how_to_get": "Smelted from iron ore in a furnace. Also found in treasure chests."
    },
    "gold ore": {
        "uses": "Raw material for gold ingots. Can be decorative.",
        "how_to_get": "Mined from gold ore blocks (found uncommonly underground, more in Badlands biomes)."
    },
    "gold ingot": {
        "uses": "Crafting gold tools, armor, apples, golden carrots, powered rails, and clocks.",
        "how_to_get": "Smelted from gold ore in a furnace. Also found in treasure chests or dropped by Zombified Piglins."
    },
    "diamond ore": {
        "uses": "Raw material for diamonds.",
        "how_to_get": "Mined from diamond ore (found rarely deep underground, usually at Y-level 16 or below)."
    },
    "diamond": {
        "uses": "Crafting the strongest tools, armor, and weapons. Also used for enchanting tables and jukeboxes.",
        "how_to_get": "Mined from diamond ore (found rarely deep underground, usually at Y-level 16 or below)."
    },
    "emerald ore": {
        "uses": "Raw material for emeralds.",
        "how_to_get": "Mined from emerald ore (found rarely in mountain biomes)."
    },
    "emerald": {
        "uses": "Currency for trading with villagers.",
        "how_to_get": "Mined from emerald ore, found in village chests, or dropped by Vexes."
    },
    "lapis lazuli": {
        "uses": "Used for enchanting, dyeing wool/leather, and crafting lapis blocks.",
        "how_to_get": "Mined from Lapis Lazuli ore (found underground)."
    },
    "redstone dust": {
        "uses": "Used for redstone circuitry (powering components, transmitting signals), crafting redstone components, and brewing.",
        "how_to_get": "Mined from Redstone ore (found deep underground)."
    },
    "quartz": {
        "uses": "Crafting polished quartz blocks, daylight detectors, and comparators.",
        "how_to_get": "Mined from Nether Quartz ore in the Nether."
    },
    "ancient debris": {
        "uses": "Smelted into Netherite Scraps. Highly blast resistant.",
        "how_to_get": "Found rarely deep in the Nether (Y-level 15-20 is common)."
    },
    "netherite scrap": {
        "uses": "Crafting Netherite Ingot.",
        "how_to_get": "Smelted from Ancient Debris."
    },
    "netherite ingot": {
        "uses": "Upgrading diamond tools and armor to netherite gear via a smithing table.",
        "how_to_get": "Crafted from 4 Netherite Scraps and 4 Gold Ingots (shapeless)."
    },
    "raw copper": {
        "uses": "Smelted into copper ingots.",
        "how_to_get": "Mined from copper ore."
    },
    "copper ingot": {
        "uses": "Crafting copper blocks, lightning rods, spyglasses, and the brush.",
        "how_to_get": "Smelted from raw copper in a furnace."
    },

    # === Tools, Weapons & Armor ===
    "stone pickaxe": {
        "uses": "Mines stone, coal, iron ore, lapis lazuli, nether quartz, redstone. Breaks faster on other blocks.",
        "how_to_get": "Crafted from 3 cobblestone and 2 sticks (in a pickaxe shape)."
    },
    "iron pickaxe": {
        "uses": "Mines stone, coal, iron ore, lapis lazuli, nether quartz, redstone, gold ore, diamond ore, emerald ore, obsidian.",
        "how_to_get": "Crafted from 3 iron ingots and 2 sticks."
    },
    "diamond pickaxe": {
        "uses": "Mines all mineable blocks, including obsidian, crying obsidian, ancient debris, and netherite blocks.",
        "how_to_get": "Crafted from 3 diamonds and 2 sticks."
    },
    "netherite pickaxe": {
        "uses": "The fastest and most durable pickaxe. Mines all mineable blocks. Also floats in lava.",
        "how_to_get": "Upgraded from a Diamond Pickaxe and 1 Netherite Ingot on a Smithing Table with a Netherite Upgrade Smithing Template."
    },
    "wooden axe": {
        "uses": "Chops wood. Slowest axe.",
        "how_to_get": "Crafted from 3 wood planks and 2 sticks."
    },
    "iron axe": {
        "uses": "Efficiently chops wood.",
        "how_to_get": "Crafted from 3 iron ingots and 2 sticks."
    },
    "diamond sword": {
        "uses": "A powerful weapon for melee combat.",
        "how_to_get": "Crafted from 2 diamonds and 1 stick."
    },
    "bow": {
        "uses": "Ranged weapon that shoots arrows.",
        "how_to_get": "Crafted from 3 sticks and 3 string."
    },
    "arrow": {
        "uses": "Ammunition for bows and crossbows.",
        "how_to_get": "Crafted from 1 flint, 1 stick, and 1 feather. Dropped by Skeletons."
    },
    "shield": {
        "uses": "Blocks incoming attacks, reducing damage. Can be customized with banners.",
        "how_to_get": "Crafted from 6 wood planks and 1 iron ingot."
    },
    "leather helmet": {
        "uses": "Provides basic armor protection.",
        "how_to_get": "Crafted from 5 leather."
    },
    "iron chestplate": {
        "uses": "Provides good armor protection.",
        "how_to_get": "Crafted from 8 iron ingots."
    },
    "diamond leggings": {
        "uses": "Provides strong armor protection.",
        "how_to_get": "Crafted from 7 diamonds."
    },
    "netherite boots": {
        "uses": "Provides the strongest armor protection. Also floats in lava.",
        "how_to_get": "Upgraded from Diamond Boots and 1 Netherite Ingot on a Smithing Table with a Netherite Upgrade Smithing Template."
    },
    "elytra": {
        "uses": "Allows players to glide through the air, consuming fireworks rockets for propulsion.",
        "how_to_get": "Found in End Cities, typically in the treasure room of an End Ship."
    },
    "fishing rod": {
        "uses": "Used to catch fish, treasure, and junk from water.",
        "how_to_get": "Crafted from 3 sticks and 2 string."
    },
    "compass": {
        "uses": "Points to your world spawn point.",
        "how_to_get": "Crafted from 4 iron ingots and 1 redstone dust."
    },
    "clock": {
        "uses": "Indicates the time of day.",
        "how_to_get": "Crafted from 4 gold ingots and 1 redstone dust."
    },
    "spyglass": {
        "uses": "Allows players to zoom in on distant objects.",
        "how_to_get": "Crafted from 2 copper ingots and 1 amethyst shard."
    },

    # === Food & Farming ===
    "wheat seeds": {
        "uses": "Plantable on farmland to grow wheat.",
        "how_to_get": "Obtained by breaking grass or tall grass."
    },
    "wheat": {
        "uses": "Crafting bread, cookies, and breeding cows, sheep, and mooshrooms.",
        "how_to_get": "Harvested from fully grown wheat crops."
    },
    "bread": {
        "uses": "Restores hunger points.",
        "how_to_get": "Crafted from 3 wheat (in a row)."
    },
    "carrot": {
        "uses": "Restores hunger. Can be crafted into golden carrots or used to breed pigs and rabbits.",
        "how_to_get": "Harvested from carrot crops, found in village farms, or dropped by zombies."
    },
    "potato": {
        "uses": "Restores hunger. Can be baked into baked potatoes. Used to breed pigs.",
        "how_to_get": "Harvested from potato crops, found in village farms, or dropped by zombies."
    },
    "baked potato": {
        "uses": "Restores more hunger than raw potatoes.",
        "how_to_get": "Smelted from potatoes in a furnace."
    },
    "cooked beef": {
        "uses": "Restores a large amount of hunger.",
        "how_to_get": "Cooked from raw beef in a furnace or campfire. Raw beef is dropped by cows."
    },
    "cooked chicken": {
        "uses": "Restores hunger.",
        "how_to_get": "Cooked from raw chicken in a furnace or campfire. Raw chicken is dropped by chickens."
    },
    "porkchop": {
        "uses": "Restores hunger.",
        "how_to_get": "Dropped by pigs."
    },
    "cooked porkchop": {
        "uses": "Restores a good amount of hunger.",
        "how_to_get": "Cooked from porkchop in a furnace or campfire."
    },
    "pumpkin": {
        "uses": "Decorative block, crafting pumpkin pie, pumpkin seeds, and carved pumpkins (for Golems).",
        "how_to_get": "Found naturally in most biomes. Can be grown from pumpkin seeds."
    },
    "melon slice": {
        "uses": "Restores a small amount of hunger. Can be crafted into glistering melon slices.",
        "how_to_get": "Harvested from melon blocks. Melon blocks grow from melon seeds."
    },
    "cookie": {
        "uses": "Small hunger restoration. Stackable.",
        "how_to_get": "Crafted from 2 wheat and 1 cocoa beans."
    },
    "sugar cane": {
        "uses": "Crafting sugar, paper, and rockets.",
        "how_to_get": "Grows naturally near water in most biomes."
    },
    "sugar": {
        "uses": "Crafting cake, cookies, pumpkin pie, and brewing potions.",
        "how_to_get": "Crafted from sugar cane."
    },
    "cake": {
        "uses": "A multi-use food block that can be eaten by multiple players.",
        "how_to_get": "Crafted from 3 milk, 2 sugar, 1 egg, and 3 wheat."
    },
    "egg": {
        "uses": "Throwing to spawn chickens (small chance). Used in crafting cake and pumpkin pie.",
        "how_to_get": "Dropped by chickens."
    },
    "milk bucket": {
        "uses": "Removes all status effects. Used in crafting cake.",
        "how_to_get": "Right-click a cow or mooshroom with an empty bucket."
    },

    # === Redstone Components ===
    "redstone dust": {
        "uses": "Used for redstone circuitry (powering components, transmitting signals), crafting redstone components, and brewing.",
        "how_to_get": "Mined from Redstone ore (found deep underground)."
    },
    "redstone torch": {
        "uses": "Provides a constant redstone signal. Can be used as a power source or inverter.",
        "how_to_get": "Crafted from 1 redstone dust and 1 stick."
    },
    "lever": {
        "uses": "Provides a toggleable redstone signal.",
        "how_to_get": "Crafted from 1 cobblestone and 1 stick."
    },
    "button (stone)": {
        "uses": "Provides a temporary redstone pulse when pressed.",
        "how_to_get": "Crafted from 1 stone."
    },
    "pressure plate (stone)": {
        "uses": "Provides a redstone signal when an entity (player, mob, item) steps on it.",
        "how_to_get": "Crafted from 2 stone blocks (side-by-side)."
    },
    "repeater": {
        "uses": "Repeats, delays, and locks redstone signals.",
        "how_to_get": "Crafted from 3 stone, 2 redstone torch, and 1 redstone dust."
    },
    "comparator": {
        "uses": "Compares, subtracts, or measures redstone signal strength. Used for advanced redstone logic.",
        "how_to_get": "Crafted from 3 stone, 1 nether quartz, and 3 redstone torch."
    },
    "piston": {
        "uses": "Pushes blocks. Can be extended with a redstone signal.",
        "how_to_get": "Crafted from 3 wood planks, 4 cobblestone, 1 iron ingot, and 1 redstone dust."
    },
    "sticky piston": {
        "uses": "Pushes and pulls blocks. Can be extended with a redstone signal.",
        "how_to_get": "Crafted from 1 piston and 1 slimeball."
    },
    "hopper": {
        "uses": "Collects items dropped above it or from containers, and moves them into connected inventories.",
        "how_to_get": "Crafted from 5 iron ingots and 1 chest."
    },
    "dropper": {
        "uses": "Dispenses items one at a time when powered by redstone.",
        "how_to_get": "Crafted from 7 cobblestone and 1 Redstone dust."
    },
    "dispenser": {
        "uses": "Dispenses items or activates certain items (e.g., shooting arrows, placing water/lava).",
        "how_to_get": "Crafted from 7 cobblestone, 1 Redstone dust, and 1 bow."
    },
    "observer": {
        "uses": "Detects block updates and emits a redstone pulse.",
        "how_to_get": "Crafted from 6 cobblestone, 2 redstone dust, and 1 nether quartz."
    },
    "daylight detector": {
        "uses": "Emits a redstone signal based on the time of day.",
        "how_to_get": "Crafted from 3 glass, 3 nether quartz, and 3 wood slabs."
    },
    "target block": {
        "uses": "Emits a redstone signal proportional to how close an arrow (or other projectile) hits its center.",
        "how_to_get": "Crafted from 1 hay bale and 4 redstone dust."
    },

    # === Brewing & Potions ===
    "brewing stand": {
        "uses": "Used to brew potions.",
        "how_to_get": "Crafted from 1 blaze rod and 3 cobblestone."
    },
    "glass bottle": {
        "uses": "Holds potions. Can be filled with water from a water source or cauldron.",
        "how_to_get": "Crafted from 3 glass blocks."
    },
    "nether wart": {
        "uses": "Primary ingredient for brewing Awkward Potions, the base for most other potions.",
        "how_to_get": "Found in Nether Fortresses."
    },
    "blaze rod": {
        "uses": "Crafting blaze powder and brewing stands. Also used for the Mace and Wind Charges.",
        "how_to_get": "Dropped by Blazes in Nether Fortresses."
    },
    "blaze powder": {
        "uses": "Fuel for brewing stands. Used to craft Blaze Rods, Fire Charges, and Eyes of Ender.",
        "how_to_get": "Crafted from 1 Blaze Rod."
    },
    "ghast tear": {
        "uses": "Brewing Potions of Regeneration.",
        "how_to_get": "Dropped by Ghasts."
    },
    "fermented spider eye": {
        "uses": "Used to corrupt potions (e.g., from Healing to Harming, Night Vision to Invisibility).",
        "how_to_get": "Crafted from 1 spider eye, 1 mushroom (brown), and 1 sugar."
    },
    "sugar (brewing)": { # Distinction for brewing use
        "uses": "Brewing Potions of Swiftness.",
        "how_to_get": "Crafted from sugar cane."
    },
    "magma cream": {
        "uses": "Brewing Potions of Fire Resistance.",
        "how_to_get": "Crafted from 1 Slimeball and 1 Blaze Powder. Dropped by Magma Cubes."
    },
    "glistering melon slice": {
        "uses": "Brewing Potions of Healing.",
        "how_to_get": "Crafted from 1 melon slice and 1 gold nugget."
    },
    "golden carrot": {
        "uses": "Brewing Potions of Night Vision.",
        "how_to_get": "Crafted from 1 carrot and 8 gold nuggets."
    },
    "rabbit's foot": {
        "uses": "Brewing Potions of Leaping.",
        "how_to_get": "Dropped by Rabbits (low chance)."
    },
    "phantom membrane": {
        "uses": "Brewing Potions of Slow Falling. Repairing Elytra in an anvil.",
        "how_to_get": "Dropped by Phantoms."
    },
    "turtle shell": {
        "uses": "Brewing Potions of the Turtle Master.",
        "how_to_get": "Crafted from 5 Scutes (dropped by baby turtles)."
    },
    "awkward potion": {
        "uses": "Base potion for most other potions.",
        "how_to_get": "Brewed from 1 Nether Wart and 1 Water Bottle."
    },
    "potion of healing": {
        "uses": "Instantly restores health.",
        "how_to_get": "Brewed from 1 Glistering Melon Slice and 1 Awkward Potion."
    },
    "splash potion": {
        "uses": "A throwable potion that applies effects in an area.",
        "how_to_get": "Crafted by adding gunpowder to any potion in a brewing stand."
    },
    "lingering potion": {
        "uses": "A throwable potion that leaves a cloud of effect for a short duration.",
        "how_to_get": "Crafted by adding dragon's breath to a splash potion in a brewing stand."
    },
    "dragon's breath": {
        "uses": "Crafting lingering potions.",
        "how_to_get": "Collected from the Ender Dragon's breath attack with empty glass bottles."
    },

    # === Enchanting ===
    "enchanting table": {
        "uses": "Allows players to enchant tools, armor, and weapons with special abilities using experience levels and Lapis Lazuli.",
        "how_to_get": "Crafted from 1 book, 2 diamonds, and 4 obsidian."
    },
    "bookshelf": {
        "uses": "Increases the enchantment level available from an enchanting table when placed nearby.",
        "how_to_get": "Crafted from 3 books and 6 wood planks."
    },
    "experience bottle": {
        "uses": "Smashes to release experience orbs.",
        "how_to_get": "Found in End City chests, Shipwrecks, or purchased from cleric villagers."
    },
    "anvil": {
        "uses": "Combines enchantments, repairs items using materials or other items, and renames items.",
        "how_to_get": "Crafted from 3 iron blocks and 4 iron ingots."
    },
    "grindstone": {
        "uses": "Removes enchantments from items (returning some XP) and repairs tools/weapons without losing enchantments.",
        "how_to_get": "Crafted from 2 sticks, 1 stone slab, and 2 wood planks."
    },
    "smithing table": {
        "uses": "Upgrades diamond gear to netherite and applies armor trims using smithing templates.",
        "how_to_get": "Crafted from 2 iron ingots and 4 wood planks."
    },
    "fletching table": {
        "uses": "Villagers can claim it as a job site block to become fletchers.",
        "how_to_get": "Crafted from 2 flint and 4 wood planks."
    },
    "cartography table": {
        "uses": "Used to clone, enlarge, lock, or combine maps.",
        "how_to_get": "Crafted from 2 paper and 4 wood planks."
    },
    "lectern": {
        "uses": "Holds books for multiple players to read. Emits redstone signal when pages are turned.",
        "how_to_get": "Crafted from 4 wood slabs and 1 bookshelf."
    },

    # === Building Blocks & Decorative ===
    "cobblestone": {
        "uses": "Basic building block. Smelts into stone.",
        "how_to_get": "Mined from stone blocks."
    },
    "stone": {
        "uses": "Building block. Can be crafted into stone bricks, polished stone, etc.",
        "how_to_get": "Smelted from cobblestone in a furnace."
    },
    "dirt": {
        "uses": "Common block for terrain. Can be turned into farmland. Grows grass and trees.",
        "how_to_get": "Found abundantly on the surface."
    },
    "grass block": {
        "uses": "The standard surface block, used for building and where animals spawn.",
        "how_to_get": "Dirt blocks exposed to light will turn to grass. Can be obtained with Silk Touch."
    },
    "sand": {
        "uses": "Falls due to gravity. Smelts into glass. Used in crafting sandstone.",
        "how_to_get": "Found in deserts and beaches."
    },
    "gravel": {
        "uses": "Falls due to gravity. Drops flint when broken (sometimes). Used in crafting concrete powder.",
        "how_to_get": "Found commonly underground, in beaches, and riverbeds."
    },
    "clay": {
        "uses": "Crafting clay balls, which can be smelted into bricks.",
        "how_to_get": "Found in shallow water areas."
    },
    "brick": {
        "uses": "Crafting brick blocks, decorative items.",
        "how_to_get": "Smelted from clay balls in a furnace."
    },
    "netherrack": {
        "uses": "Main block of the Nether. Burns indefinitely when lit.",
        "how_to_get": "Found abundantly in the Nether."
    },
    "end stone": {
        "uses": "Main block of The End.",
        "how_to_get": "Found abundantly in The End dimension."
    },
    "purpur block": {
        "uses": "Decorative building block found in End Cities.",
        "how_to_get": "Crafted from 4 Popped Chorus Fruit."
    },
    "shulker box": {
        "uses": "A portable storage block that retains its contents when broken. Comes in 16 colors.",
        "how_to_get": "Crafted from 2 Shulker Shells and 1 Chest."
    },
    "concrete powder": {
        "uses": "Falls due to gravity. Turns into solid concrete when it comes into contact with water.",
        "how_to_get": "Crafted from 4 gravel, 4 sand, and 1 dye."
    },
    "concrete": {
        "uses": "Solid and vibrant building block. Comes in 16 colors.",
        "how_to_get": "Created when concrete powder comes into contact with water."
    },
    "terracotta": {
        "uses": "Decorative block, can be dyed into 16 colors. Glazed terracotta has patterns.",
        "how_to_get": "Smelted from clay blocks."
    },
    "glazed terracotta": {
        "uses": "Decorative block with unique patterns based on its color and orientation.",
        "how_to_get": "Smelted from dyed terracotta."
    },
    "blackstone": {
        "uses": "Similar to cobblestone, found in the Nether. Can be polished, chiseled, and used for tools.",
        "how_to_get": "Found abundantly in Basalt Deltas and other Nether biomes."
    },
    "basalt": {
        "uses": "Decorative block, found in Basalt Deltas and large basalt pillars in the Nether.",
        "how_to_get": "Found naturally in Basalt Deltas and large basalt pillars in the Nether."
    },
    "crying obsidian": {
        "uses": "Emits purple particles and light. Used to craft Respawn Anchors.",
        "how_to_get": "Found in Ruined Portals, Bastion Remnants, or Piglin bartering."
    },
    "respawn anchor": {
        "uses": "Allows players to set a spawn point in the Nether (requires Glowstone to charge).",
        "how_to_get": "Crafted from 6 Crying Obsidian and 3 Glowstone blocks."
    },
    "amethyst shard": {
        "uses": "Used to craft spyglasses, tinted glass, and blocks of amethyst.",
        "how_to_get": "Mined from amethyst geodes, specifically from budding amethyst blocks."
    },
    "tinted glass": {
        "uses": "A block that blocks all light, unlike normal glass. Can be broken and re-collected.",
        "how_to_get": "Crafted from 4 amethyst shards and 1 glass block."
    },
    "sculk sensor": {
        "uses": "Detects vibrations (player actions, mob movement, etc.) and emits a redstone signal.",
        "how_to_get": "Found in Ancient Cities or Deep Dark biomes."
    },
    "sculk catalyst": {
        "uses": "Spreads sculk blocks when mobs die near it, dropping experience.",
        "how_to_get": "Found in Ancient Cities."
    },
    "sculk shrieker": {
        "uses": "Emits a shrieking sound and can summon a Warden if triggered multiple times.",
        "how_to_get": "Found in Ancient Cities."
    },

    # === Nether & End Items ===
    "nether star": {
        "uses": "Crafting beacons.",
        "how_to_get": "Dropped by the Wither boss."
    },
    "beacon": {
        "uses": "Emits a beam of light into the sky and provides status effects (Haste, Speed, Jump Boost, Regeneration, Strength) to nearby players.",
        "how_to_get": "Crafted from 1 Nether Star, 3 Obsidian, and 5 Glass."
    },
    "end crystal": {
        "uses": "Used to re-summon the Ender Dragon. Also found on top of obsidian pillars in The End.",
        "how_to_get": "Crafted from 7 Glass, 1 Eye of Ender, and 1 Ghast Tear."
    },
    "ender pearl": {
        "uses": "Teleports the player to where it lands. Used to craft Eyes of Ender.",
        "how_to_get": "Dropped by Endermen."
    },
    "eye of ender": {
        "uses": "Used to locate strongholds. Activates End Portals. Crafted from Ender Pearls and Blaze Powder.",
        "how_to_get": "Crafted from 1 Ender Pearl and 1 Blaze Powder."
    },
    "chorus fruit": {
        "uses": "Teleports the player a short distance when eaten. Can be cooked into Popped Chorus Fruit.",
        "how_to_get": "Harvested from Chorus Plants in The End."
    },
    "popped chorus fruit": {
        "uses": "Used to craft Purpur Blocks.",
        "how_to_get": "Smelted from Chorus Fruit."
    },
    "shulker shell": {
        "uses": "Crafting Shulker Boxes.",
        "how_to_get": "Dropped by Shulkers in End Cities."
    },
    "warped fungus on a stick": {
        "uses": "Used to ride and steer Strider mobs in the Nether.",
        "how_to_get": "Crafted from 1 fishing rod and 1 Warped Fungus."
    },
    "crimson fungus": {
        "uses": "Plantable on Nylium to grow Crimson trees. Used to breed Hoglins.",
        "how_to_get": "Found in Crimson Forests in the Nether."
    },
    "warped fungus": {
        "uses": "Plantable on Nylium to grow Warped trees. Used to breed Striders.",
        "how_to_get": "Found in Warped Forests in the Nether."
    },
    "ghast tear": {
        "uses": "Brewing Potions of Regeneration.",
        "how_to_get": "Dropped by Ghasts."
    },
    "wither skull": {
        "uses": "Used to summon the Wither boss (requires 3 Wither Skulls and 4 Soul Sand/Soil).",
        "how_to_get": "Dropped by Wither Skeletons in Nether Fortresses."
    },
    "nether star": {
        "uses": "Used to craft beacons.",
        "how_to_get": "Dropped by the Wither boss."
    },

    # === Miscellaneous ===
    "string": {
        "uses": "Crafting wool, bows, fishing rods, crossbows, leads, tripwire hooks.",
        "how_to_get": "Dropped by spiders, found in chests, or obtained by breaking cobwebs."
    },
    "slimeball": {
        "uses": "Crafting slime blocks, magma cream, and sticky pistons.",
        "how_to_get": "Dropped by Slimes, found in jungle temple chests."
    },
    "ender chest": {
        "uses": "A unique chest that allows players to access their personal inventory from any Ender Chest in the world.",
        "how_to_get": "Crafted from 8 obsidian and 1 Eye of Ender."
    },
    "flower pot": {
        "uses": "Decorative block for holding flowers, saplings, mushrooms, cacti, and ferns.",
        "how_to_get": "Crafted from 3 bricks."
    },
    "banner": {
        "uses": "Decorative block that can be customized with various patterns and colors.",
        "how_to_get": "Crafted from 6 wool (same color) and 1 stick."
    },
    "map": {
        "uses": "Shows a top-down view of explored terrain. Can be enlarged and cloned.",
        "how_to_get": "Crafted from 8 paper and 1 compass."
    },
    "item frame": {
        "uses": "Displays an item or block on a wall. Can be rotated.",
        "how_to_get": "Crafted from 8 sticks and 1 leather."
    },
    "glow item frame": {
        "uses": "Displays an item or block on a wall and makes it glow, even in darkness.",
        "how_to_get": "Crafted from 1 Item Frame and 1 Glow Ink Sac."
    },
    "glow ink sac": {
        "uses": "Used to craft Glow Item Frames and make text on signs glow.",
        "how_to_get": "Dropped by Glow Squids."
    },
    "name tag": {
        "uses": "Allows players to rename mobs.",
        "how_to_get": "Found in dungeon chests, abandoned mineshafts, or traded with librarian villagers."
    },
    "saddle": {
        "uses": "Required to ride pigs and horses. Cannot be crafted.",
        "how_to_get": "Found in chests (dungeons, temples, villages), fished, or traded with leatherworker villagers."
    },
    "totem of undying": {
        "uses": "Saves the player from death once, restoring health and granting temporary buffs.",
        "how_to_get": "Dropped by Evokers (found in Woodland Mansions and Raids)."
    },

    # === 1.20 Trails & Tales Update Items ===
    "suspicious sand": {
        "uses": "Brushable block found in desert temples and desert wells, revealing hidden items like pottery sherds, sniffer eggs, or diamonds.",
        "how_to_get": "Found naturally in desert temples and desert wells. Requires a brush to excavate."
    },
    "suspicious gravel": {
        "uses": "Brushable block found in cold ocean ruins, trail ruins, and warm ocean ruins, revealing items like pottery sherds, emeralds, or tools.",
        "how_to_get": "Found naturally in ocean ruins and trail ruins. Requires a brush to excavate."
    },
    "brush": {
        "uses": "Used for archeology, specifically to brush suspicious sand and suspicious gravel to reveal hidden items.",
        "how_to_get": "Crafted from 1 feather, 1 copper ingot, and 1 stick (vertically)."
    },
    "sniffer egg": {
        "uses": "Hatches into a Sniffer, a passive mob that can dig up unique seeds.",
        "how_to_get": "Found by brushing suspicious sand in desert temples or suspicious gravel in ocean ruins."
    },
    "torchflower seeds": {
        "uses": "Plantable on dirt or grass to grow a Torchflower, a unique flower. Can be used to breed sniffers.",
        "how_to_get": "Dug up by a Sniffer mob."
    },
    "pitcher pod": {
        "uses": "Plantable on dirt or grass to grow a Pitcher Plant, a large unique decorative plant. Can be used to breed sniffers.",
        "how_to_get": "Dug up by a Sniffer mob."
    },
    "decorated pot": {
        "uses": "Decorative block that can display up to 4 items inside. Can be made with or without pottery sherds.",
        "how_to_get": "Crafted from 4 pottery sherds, or 4 bricks (in a diamond shape). Can be broken with a tool to drop its contents."
    },
    "chiseled bookshelf": {
        "uses": "Functional storage for up to 6 books (normal books, enchanted books, or written books). Can be interacted with via Redstone.",
        "how_to_get": "Crafted from 6 wood planks and 3 wood slabs (any type of wood)."
    },
    "smithing template": { # Generic entry, as there are many variants
        "uses": "Used in a smithing table to apply armor trims or upgrade diamond gear to netherite.",
        "how_to_get": "Armor trim smithing templates are found in various structures (e.g., Bastion Remnants, Shipwrecks, Trail Ruins). Netherite Upgrade templates are found in Bastion Remnants."
    },
    "netherite upgrade smithing template": {
        "uses": "Specifically used to upgrade diamond gear to netherite gear on a smithing table.",
        "how_to_get": "Found in Bastion Remnants (guaranteed in treasure room)."
    },
    "sentry armor trim smithing template": {
        "uses": "Applies the Sentry armor trim pattern to armor pieces using a smithing table.",
        "how_to_get": "Found in Pillager Outposts."
    },
    "wayfinder armor trim smithing template": {
        "uses": "Applies the Wayfinder armor trim pattern to armor pieces using a smithing table.",
        "how_to_get": "Found in Trail Ruins."
    },
    "recovery compass": {
        "uses": "Points to the location of your last death, helping you recover lost items.",
        "how_to_get": "Crafted from 1 compass and 4 Echo Shards."
    },
    "echo shard": {
        "uses": "Used to craft a Recovery Compass.",
        "how_to_get": "Found in Ancient City chests."
    },
    "music disc 5": {
        "uses": "Plays a unique, eerie music track when placed in a Jukebox.",
        "how_to_get": "Crafted from 9 Disc Fragments."
    },
    "disc fragment": {
        "uses": "Used to craft Music Disc 5.",
        "how_to_get": "Found in Ancient City chests."
    },
    "cherry wood": { # General entry for the new wood type
        "uses": "Used for building and crafting all standard wood-based items (planks, doors, fences, etc.). Unique pink color.",
        "how_to_get": "Obtained from Cherry Grove biomes by cutting down cherry trees."
    },
    "bamboo block": { # Representative of new bamboo wood set
        "uses": "Crafted into bamboo planks, bamboo mosaic, and used in building. Can also be crafted into rafts.",
        "how_to_get": "Crafted from 9 bamboo, or found in jungle biomes."
    },
    "raft": {
        "uses": "A variant of the boat, made from bamboo, for traversing water.",
        "how_to_get": "Crafted from 5 bamboo planks."
    },
    "bamboo mosaic": {
        "uses": "A decorative building block, similar to wood planks, with a unique pattern.",
        "how_to_get": "Crafted from 2 bamboo slabs."
    },

    # === 1.21 Tricky Trials Update Items ===
    "trial key": {
        "uses": "Used to unlock the Trial Vaults found within Trial Chambers.",
        "how_to_get": "Dropped by Trial Spawners after defeating all mobs."
    },
    "ominous bottle": {
        "uses": "Drinking it gives you the Ominous Omen effect, triggering Ominous Trials at Trial Spawners or Bad Omen at villages.",
        "how_to_get": "Found in Ominous Vaults or dropped by Raid Captains (Illagers with banners)."
    },
    "heavy core": {
        "uses": "A crafting ingredient used to create the Mace.",
        "how_to_get": "Found in Ominous Vaults within Trial Chambers."
    },
    "mace": {
        "uses": "A powerful melee weapon that deals more damage the further you fall before hitting an enemy.",
        "how_to_get": "Crafted from 1 Heavy Core and 1 Breeze Rod."
    },
    "breeze rod": {
        "uses": "A crafting ingredient used to create the Mace and Wind Charges.",
        "how_to_get": "Dropped by the Breeze mob in Trial Chambers."
    },
    "crafter": {
        "uses": "An automated crafting block that can craft items when powered by Redstone. Items are placed into its inventory via hoppers.",
        "how_to_get": "Crafted from 5 iron ingots, 2 Redstone dust, 1 dropper, and 1 crafting table."
    },
    "copper bulb": {
        "uses": "A unique light source that can be toggled on/off with Redstone. Its light level decreases as it oxidizes.",
        "how_to_get": "Crafted from 3 copper blocks, 1 blaze rod, and 1 Redstone dust."
    },
    "copper grate": {
        "uses": "A decorative and functional block that allows light and water to pass through. Can be oxidized.",
        "how_to_get": "Crafted from 4 copper blocks."
    },
    "copper door": {
        "uses": "A unique door type that oxidizes over time, changing its appearance. Can be opened/closed by hand or Redstone.",
        "how_to_get": "Crafted from 6 copper blocks."
    },
    "tuff blocks": { # General entry for new tuff variants
        "uses": "Decorative building blocks with various textures: Polished Tuff, Tuff Bricks, Chiseled Tuff. Slabs, stairs, and walls also exist.",
        "how_to_get": "Tuff is found deep underground. Polished and brick variants are crafted from tuff blocks."
    },
    "polished tuff": {
        "uses": "A decorative building block derived from tuff.",
        "how_to_get": "Crafted from 4 tuff blocks (2x2)."
    },
    "tuff bricks": {
        "uses": "A decorative building block with a brick pattern, derived from tuff.",
        "how_to_get": "Crafted from 4 polished tuff blocks (2x2)."
    },
    "chiseled tuff": {
        "uses": "A decorative building block with a chiseled pattern, derived from tuff.",
        "how_to_get": "Crafted from 2 tuff slabs (vertically)."
    },
    "pottery sherd": { # General entry for various sherds
        "uses": "Decorative items used to add patterns to Decorated Pots.",
        "how_to_get": "Found by brushing suspicious sand/gravel in various archeological sites (e.g., Trail Ruins, Ocean Ruins, Desert Temples)."
    },
    "arms up pottery sherd": {
        "uses": "A specific pottery sherd used for decorating pots with an 'arms up' pattern.",
        "how_to_get": "Found by brushing suspicious sand in Desert Temples."
    },
    "archer pottery sherd": {
        "uses": "A specific pottery sherd used for decorating pots with an 'archer' pattern.",
        "how_to_get": "Found by brushing suspicious gravel in Trail Ruins."
    },
    "wind charge": {
        "uses": "A throwable item that creates a powerful gust of wind, pushing entities and activating certain blocks. Acts similarly to a Breeze's attack.",
        "how_to_get": "Dropped by the Breeze mob."
    },
    "flow armortrim smithing template": {
        "uses": "Applies the Flow armor trim pattern to armor pieces using a smithing table.",
        "how_to_get": "Found in Trial Chambers."
    },
    "guster armortrim smithing template": {
        "uses": "Applies the Guster armor trim pattern to armor pieces using a smithing table.",
        "how_to_get": "Found in Ominous Vaults in Trial Chambers."
    },
    "ominous trial key": {
        "uses": "Used to unlock Ominous Vaults found within Trial Chambers, which contain rarer loot.",
        "how_to_get": "Dropped by Ominous Trial Spawners during Ominous Trials."
    },
    "vault": { # Note: This is the block, not the key
        "uses": "A new block found in Trial Chambers that requires a Trial Key to open and dispense loot once per player.",
        "how_to_get": "Found naturally in Trial Chambers."
    },
    "ominous vault": {
        "uses": "A rarer vault found during Ominous Trials, requiring an Ominous Trial Key and containing better loot.",
        "how_to_get": "Found naturally in Trial Chambers during Ominous Trials."
    },
    "infested block": { # For completeness, as it's a "hidden" item/block
        "uses": "Looks like a normal stone-type block but spawns Silverfish when broken.",
        "how_to_get": "Found naturally in Strongholds, Extreme Hills biomes, or Igloos."
    },
    "slime block": {
        "uses": "Bouncy block that launches entities. Can be used in redstone contraptions to move multiple blocks.",
        "how_to_get": "Crafted from 9 slimeballs."
    },
    "honey block": {
        "uses": "Slows down entities, reduces fall damage, and allows players to slide down walls. Can be moved by pistons.",
        "how_to_get": "Crafted from 4 honey bottles."
    },
    "honey bottle": {
        "uses": "Restores hunger and removes poison status effect.",
        "how_to_get": "Right-click a filled beehive or bee nest with an empty glass bottle."
    },
    "bone meal": {
        "uses": "Acts as fertilizer to instantly grow crops, trees, and flowers. Can be used to dye white wool.",
        "how_to_get": "Crafted from 1 bone. Bones are dropped by Skeletons or found in desert temples/dungeons."
    },
    "nether star": {
        "uses": "Used to craft beacons.",
        "how_to_get": "Dropped by the Wither boss."
    },
    "heart of the sea": {
        "uses": "Used to craft Conduits.",
        "how_to_get": "Found in Buried Treasure chests."
    },
    "conduit": {
        "uses": "Grants Conduit Power status effect (underwater breathing, night vision, and fast mining) to nearby players while submerged.",
        "how_to_get": "Crafted from 1 Heart of the Sea and 8 Nautilus Shells."
    },
    "nautilus shell": {
        "uses": "Used to craft Conduits.",
        "how_to_get": "Dropped by Drowned (rarely), fished, or traded with wandering traders."
    },
    "phantom membrane": {
        "uses": "Brewing Potions of Slow Falling. Repairing Elytra in an anvil.",
        "how_to_get": "Dropped by Phantoms."
    },
    "scute": {
        "uses": "Used to craft Turtle Shells.",
        "how_to_get": "Dropped by baby turtles when they grow into adults."
    },
    "tube coral": {
        "uses": "Decorative block found in warm ocean biomes. Dies if not in water.",
        "how_to_get": "Found naturally in warm oceans."
    },
    "brain coral": {
        "uses": "Decorative block found in warm ocean biomes. Dies if not in water.",
        "how_to_get": "Found naturally in warm oceans."
    },
    "bubble coral": {
        "uses": "Decorative block found in warm ocean biomes. Dies if not in water.",
        "how_to_get": "Found naturally in warm oceans."
    },
    "fire coral": {
        "uses": "Decorative block found in warm ocean biomes. Dies if not in water.",
        "how_to_get": "Found naturally in warm oceans."
    },
    "horn coral": {
        "uses": "Decorative block found in warm ocean biomes. Dies if not in water.",
        "how_to_get": "Found naturally in warm oceans."
    },
    "dead coral block": {
        "uses": "Decorative block, the 'dead' version of coral, not requiring water.",
        "how_to_get": "When living coral is removed from water or placed outside water, it dies and becomes this."
    },
    "sea pickle": {
        "uses": "Decorative light source. Can be placed in clusters. Can be smelted into green dye.",
        "how_to_get": "Found in warm ocean biomes. Dropped by Turtles."
    },
    "kelp": {
        "uses": "Food source (raw or dried). Can be smelted into dried kelp blocks for fuel.",
        "how_to_get": "Found abundantly in ocean biomes."
    },
    "dried kelp": {
        "uses": "Food source. Can be crafted into dried kelp blocks.",
        "how_to_get": "Smelted from kelp."
    },
    "dried kelp block": {
        "uses": "Compact storage for dried kelp. Can be used as a fuel source.",
        "how_to_get": "Crafted from 9 dried kelp."
    },
    "scaffolding": {
        "uses": "Temporary building block that can be quickly placed and removed. Players can climb it easily.",
        "how_to_get": "Crafted from 6 bamboo and 1 string."
    },
    "campfire": {
        "uses": "Cooks food slowly. Produces smoke. Can be used as a light source. Emits a redstone signal.",
        "how_to_get": "Crafted from 3 sticks, 3 wood logs/wood, and 1 coal/charcoal."
    },
    "soul campfire": {
        "uses": "Cooks food slowly. Produces higher smoke than regular campfire. Emits a redstone signal.",
        "how_to_get": "Crafted from 3 sticks, 3 wood logs/wood, and 1 Soul Sand/Soul Soil."
    },
    "sweet berries": {
        "uses": "Food source. Used to breed foxes.",
        "how_to_get": "Found growing on sweet berry bushes in Taiga biomes."
    },
    "glowstone dust": {
        "uses": "Crafting glowstone blocks and redstone lamps. Used in brewing to strengthen potion effects.",
        "how_to_get": "Dropped by Glowstone blocks in the Nether."
    },
    "ender chest": {
        "uses": "A unique chest that allows players to access their personal inventory from any Ender Chest in the world.",
        "how_to_get": "Crafted from 8 obsidian and 1 Eye of Ender."
    },
    "totem of undying": {
        "uses": "Saves the player from death once, restoring health and granting temporary buffs.",
        "how_to_get": "Dropped by Evokers (found in Woodland Mansions and Raids)."
    },
    "heart of the sea": {
        "uses": "Used to craft Conduits.",
        "how_to_get": "Found in Buried Treasure chests."
    },
    "conduit": {
        "uses": "Grants Conduit Power status effect (underwater breathing, night vision, and fast mining) to nearby players while submerged.",
        "how_to_get": "Crafted from 1 Heart of the Sea and 8 Nautilus Shells."
    },
    "nether star": {
        "uses": "Used to craft beacons.",
        "how_to_get": "Dropped by the Wither boss."
    },
    "firework rocket": {
        "uses": "Propels players using Elytra. Can also be launched from a crossbow for ranged explosions.",
        "how_to_get": "Crafted from 1 paper, 1 gunpowder, and optional firework stars for effects."
    },
    "firework star": {
        "uses": "Adds a colored explosion and optional effects to firework rockets.",
        "how_to_get": "Crafted from 1 gunpowder, 1 dye, and optional ingredients for shape/effect."
    },
    "gunpowder": {
        "uses": "Crafting TNT, firework rockets, and fire charges. Used in brewing to make splash potions.",
        "how_to_get": "Dropped by Creepers, Ghasts, and gained from breaking certain blocks in dungeons."
    },
    "tnt": {
        "uses": "Explosive block that can be ignited with flint and steel, fire, or redstone.",
        "how_to_get": "Crafted from 5 gunpowder and 4 sand/gravel."
    },
    "name tag": {
        "uses": "Allows players to rename mobs.",
        "how_to_get": "Found in dungeon chests, abandoned mineshafts, or traded with librarian villagers."
    },
    "saddle": {
        "uses": "Required to ride pigs and horses. Cannot be crafted.",
        "how_to_get": "Found in chests (dungeons, temples, villages), fished, or traded with leatherworker villagers."
    },
    "music disc": { # Generic entry for music discs
        "uses": "Plays music when placed in a Jukebox.",
        "how_to_get": "Various methods including dropped by Creepers when killed by a Skeleton's arrow, found in chests, or traded."
    },
    "music disc (otherside)": {
        "uses": "Plays a unique upbeat music track when placed in a Jukebox.",
        "how_to_get": "Found in Stronghold or Dungeon chests."
    },
    "jukebox": {
        "uses": "Plays music discs.",
        "how_to_get": "Crafted from 8 wood planks and 1 diamond."
    },
    "painting": {
        "uses": "Decorative block that displays various pixel art images.",
        "how_to_get": "Crafted from 8 sticks and 1 wool (any color)."
    },
    "flower pot": {
        "uses": "Decorative block for holding flowers, saplings, mushrooms, cacti, and ferns.",
        "how_to_get": "Crafted from 3 bricks."
    },
    "tripwire hook": {
        "uses": "Used to create tripwire traps with string, activating redstone signals.",
        "how_to_get": "Crafted from 1 iron ingot, 1 stick, and 1 wood plank."
    },
    "string (redstone)": { # Distinction for redstone use
        "uses": "Connects two tripwire hooks to form a tripwire, triggering redstone.",
        "how_to_get": "Dropped by spiders, found in chests, or obtained by breaking cobwebs."
    },
    "slime block": {
        "uses": "Bouncy block that launches entities. Can be used in redstone contraptions to move multiple blocks.",
        "how_to_get": "Crafted from 9 slimeballs."
    },
    "honey block": {
        "uses": "Slows down entities, reduces fall damage, and allows players to slide down walls. Can be moved by pistons.",
        "how_to_get": "Crafted from 4 honey bottles."
    },
    "bell": {
        "uses": "Rings to alert villagers of danger (raid imminent) or can be used with redstone.",
        "how_to_get": "Found in villages or crafted from 3 wood and 1 gold ingot."
    },
    "lodestone": {
        "uses": "Allows a compass to point to it, even in other dimensions.",
        "how_to_get": "Crafted from 1 netherite ingot and 8 chiseled stone bricks."
    },
    "netherite block": {
        "uses": "A compact storage block for Netherite Ingots. Can be used as a base for a beacon.",
        "how_to_get": "Crafted from 9 netherite ingots."
    },
    "ancient city": { # This is a structure, not an item, but I'll add a placeholder to explain
        "uses": "A structure found in the Deep Dark, containing valuable loot, Echo Shards, and Sculk blocks. Home of the Warden.",
        "how_to_get": "Explored in the Deep Dark biome, typically far underground."
    },
    "warden": { # This is a mob, not an item, but I'll add a placeholder to explain
        "uses": "A powerful, blind, hostile mob that hunts based on sound and vibrations in the Deep Dark.",
        "how_to_get": "Summoned by repeatedly triggering Sculk Shriekers in Ancient Cities."
    }
}

def get_minecraft_item_info(query):
    key = query.strip().lower()
    if key in item_database:
        # Return the item name + newline + description
        return f"{key.title()}\n{item_database[key]}"
    return None

class MinecraftItemLookupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Item Lookup")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search section
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_label = ttk.Label(self.search_frame, text="Search for Minecraft item:")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda e: self.search_item())
        
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_item)
        self.search_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Results section
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item info display
        self.item_info = scrolledtext.ScrolledText(
            self.results_frame, 
            wrap=tk.WORD, 
            font=('Arial', 10),
            padx=10,
            pady=10
        )
        self.item_info.pack(fill=tk.BOTH, expand=True)
        self.item_info.config(state=tk.DISABLED)
        
        # Suggestions listbox
        self.suggestions_label = ttk.Label(self.results_frame, text="Did you mean:")
        self.suggestions_label.pack(fill=tk.X)
        
        self.suggestions_listbox = tk.Listbox(
            self.results_frame,
            height=5,
            font=('Arial', 10),
            selectbackground='#4a6984',
            selectforeground='#ffffff'
        )
        self.suggestions_listbox.pack(fill=tk.X)
        self.suggestions_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)
        
        # Initially hide suggestions
        self.hide_suggestions()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X)
        
        # Set focus to search entry
        self.search_entry.focus()
        
    def search_item(self):
        query = self.search_var.get().strip()
        if not query:
            self.show_status("Please enter an item name to search")
            return
            
        self.show_status(f"Searching for '{query}'...")
        
        # Clear previous results
        self.item_info.config(state=tk.NORMAL)
        self.item_info.delete(1.0, tk.END)
        
        # Try exact match first
        info = get_minecraft_item_info(query)
        
        if info:
            self.display_item_info(info)
            self.hide_suggestions()
            self.show_status(f"Found information for '{query}'")
        else:
            self.show_suggestions(query)
            
    def display_item_info(self, info):
        self.item_info.config(state=tk.NORMAL)
        self.item_info.delete(1.0, tk.END)
        
        # Configure tags for formatting
        self.item_info.tag_configure('title', font=('Arial', 12, 'bold'))
        self.item_info.tag_configure('subtitle', font=('Arial', 10, 'bold'))
        
        # Split the info into lines
        lines = info.split('\n')
        
        # Insert title
        self.item_info.insert(tk.END, lines[0] + '\n', 'title')
        
        # Insert uses and how to get
        for line in lines[1:]:
            self.item_info.insert(tk.END, line + '\n')
        
        self.item_info.config(state=tk.DISABLED)
        
    def show_suggestions(self, query):
        all_item_names = list(item_database.keys())
        normalized_user_input = query.strip().lower()
        
        # Step 1: Use difflib to find close matches
        suggestions_from_difflib = difflib.get_close_matches(normalized_user_input, all_item_names, n=10, cutoff=0.6)
        
        # Step 2: Add substring matches as a fallback/enhancement
        substring_suggestions = set()
        if len(normalized_user_input) > 1:  # Only do substring for inputs longer than 1 character
            for item in all_item_names:
                if normalized_user_input in item:
                    substring_suggestions.add(item)

        # Combine and de-duplicate suggestions, keeping order from difflib first
        combined_suggestions = list(
            dict.fromkeys(suggestions_from_difflib + sorted(list(substring_suggestions))))
        
        if combined_suggestions:
            self.suggestions_listbox.delete(0, tk.END)
            for item in combined_suggestions[:10]:  # Limit to 10 suggestions
                self.suggestions_listbox.insert(tk.END, item.title())
            
            self.show_status(f"No exact match for '{query}'. Select a suggestion or try another search.")
            self.show_suggestions_widgets()
        else:
            self.hide_suggestions()
            self.show_status(f"Sorry, no matches found for '{query}'. Try another item.")
            self.item_info.config(state=tk.NORMAL)
            self.item_info.delete(1.0, tk.END)
            self.item_info.insert(tk.END, f"No information found for '{query}'.\n\nTry searching for another item.")
            self.item_info.config(state=tk.DISABLED)
            
    def on_suggestion_select(self, event):
        selection = self.suggestions_listbox.curselection()
        if selection:
            selected_item = self.suggestions_listbox.get(selection[0])
            self.search_var.set(selected_item)
            self.search_item()
            
    def show_suggestions_widgets(self):
        self.suggestions_label.pack(fill=tk.X)
        self.suggestions_listbox.pack(fill=tk.X)
        
    def hide_suggestions(self):
        self.suggestions_label.pack_forget()
        self.suggestions_listbox.pack_forget()
        
    def show_status(self, message):
        self.status_var.set(message)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftItemLookupApp(root)
    app.run()