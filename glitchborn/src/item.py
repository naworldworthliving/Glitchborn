import random

# Item qualities and colors
ITEM_QUALITIES = {
    "uncommon": (128, 128, 128),  # Grey
    "normal": (255, 255, 255),  # White
    "rare": (0, 0, 255),        # Blue
    "super_rare": (128, 0, 128), # Purple
    "unique": (255, 215, 0)      # Gold
}

class Item:
    """
    Represents an item in the game.
    """
    def __init__(self, name, quality="normal", item_type="weapon", stats=None):
        """
        Initialize the item.
        """
        self.name = name
        self.item_type = item_type
        self.stats = stats if stats is not None else {}
        if quality in ITEM_QUALITIES:
            self.quality = quality
        else:
            self.quality = "normal"

# --- Predefined items ---
# In a real game, this would likely come from a database or JSON file.
POSSIBLE_ITEMS = [
    {"name": "Rusty Sword", "quality": "uncommon", "type": "weapon"},
    {"name": "Iron Sword", "quality": "normal", "type": "weapon"},
    {"name": "Steel Sword", "quality": "normal", "type": "weapon"},
    {"name": "Sword of the Blue Sky", "quality": "rare", "type": "weapon"},
    {"name": "Boots of Speed", "quality": "rare", "type": "feet"},
    {"name": "Leather Helmet", "quality": "normal", "type": "head"},
    {"name": "Iron Helmet", "quality": "rare", "type": "head"},
    {"name": "Helmet of Strength", "quality": "super_rare", "type": "head"},
    {"name": "Glitched Amulet", "quality": "super_rare", "type": "shield"},
    {"name": "The One Ring", "quality": "unique", "type": "shield"},
]

def generate_random_item():
    """
    Generates a random item from the POSSIBLE_ITEMS list, with randomized stats.
    """
    item_data = random.choice(POSSIBLE_ITEMS)
    quality = item_data["quality"]

    # Define stat budgets for each quality
    quality_stat_budgets = {
        "uncommon": 5,
        "normal": 10,
        "rare": 20,
        "super_rare": 40,
        "unique": 80,
    }

    # Define which stats are possible
    possible_stats = ["strength", "dexterity", "intelligence", "wisdom", "magic", "charisma", "health"]

    # Generate stats
    item_stats = {}
    budget = quality_stat_budgets.get(quality, 0)

    # Number of stats an item can have
    num_stats = random.randint(1, 3)

    # Distribute budget among a few random stats
    for _ in range(num_stats):
        if budget <= 0:
            break
        stat_to_buff = random.choice(possible_stats)
        if stat_to_buff not in item_stats:
            item_stats[stat_to_buff] = 0

        # Allocate a portion of the budget
        value = random.randint(1, budget)
        item_stats[stat_to_buff] += value
        budget -= value

    return Item(item_data["name"], quality, item_data["type"], item_stats)
