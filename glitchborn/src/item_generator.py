import random
from item import Item, ITEM_QUALITIES

# --- Base Item Data ---
BASE_ITEMS = {
    "weapon": [
        {"name": "Sword", "stats": {"damage": 10}},
        {"name": "Axe", "stats": {"damage": 12}},
        {"name": "Dagger", "stats": {"damage": 8, "speed": 1.2}},
    ],
    "armor": [
        {"name": "Leather Tunic", "stats": {"armor": 5}},
        {"name": "Iron Plate", "stats": {"armor": 10}},
    ]
}

def generate_random_item():
    """
    Generates a random item with a random quality and stats.
    """
    # --- Choose a random item type and base item ---
    item_type = random.choice(list(BASE_ITEMS.keys()))
    base_item_data = random.choice(BASE_ITEMS[item_type])

    # --- Determine quality ---
    # This is a simple quality distribution, can be made more complex
    quality_roll = random.random()
    if quality_roll < 0.05: # 5%
        quality = "unique"
    elif quality_roll < 0.15: # 10%
        quality = "super_rare"
    elif quality_roll < 0.35: # 20%
        quality = "rare"
    elif quality_roll < 0.75: # 40%
        quality = "normal"
    else: # 25%
        quality = "poor"

    # --- Create the item ---
    item_name = base_item_data["name"]
    item_stats = base_item_data["stats"].copy()

    # --- Modify stats based on quality ---
    modifier = ITEM_QUALITIES[quality]["modifier"]
    for stat, value in item_stats.items():
        item_stats[stat] = int(value * modifier)

    return Item(item_name, quality, item_stats)
