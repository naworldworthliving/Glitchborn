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
    def __init__(self, name, quality="normal"):
        """
        Initialize the item.
        """
        self.name = name
        if quality in ITEM_QUALITIES:
            self.quality = quality
        else:
            self.quality = "normal"

# --- Predefined items ---
# In a real game, this would likely come from a database or JSON file.
POSSIBLE_ITEMS = [
    {"name": "Rusty Sword", "quality": "uncommon"},
    {"name": "Iron Sword", "quality": "normal"},
    {"name": "Steel Sword", "quality": "normal"},
    {"name": "Sword of the Blue Sky", "quality": "rare"},
    {"name": "Boots of Speed", "quality": "rare"},
    {"name": "Helmet of Strength", "quality": "super_rare"},
    {"name": "Glitched Amulet", "quality": "super_rare"},
    {"name": "The One Ring", "quality": "unique"},
]

def generate_random_item():
    """
    Generates a random item from the POSSIBLE_ITEMS list.
    """
    item_data = random.choice(POSSIBLE_ITEMS)
    return Item(item_data["name"], item_data["quality"])
