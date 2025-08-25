from enum import Enum

# --- Item Quality Colors ---
POOR_COLOR = (150, 150, 150)  # Grey
NORMAL_COLOR = (255, 255, 255) # White
RARE_COLOR = (0, 100, 255)   # Blue
SUPER_RARE_COLOR = (163, 53, 238) # Purple
UNIQUE_COLOR = (255, 128, 0)  # Orange

class ItemQuality(Enum):
    """Enumeration for item quality tiers."""
    POOR = POOR_COLOR
    NORMAL = NORMAL_COLOR
    RARE = RARE_COLOR
    SUPER_RARE = SUPER_RARE_COLOR
    UNIQUE = UNIQUE_COLOR

class Item:
    """Base class for all items in the game."""
    def __init__(self, name, description, quality):
        if not isinstance(quality, ItemQuality):
            raise TypeError("quality must be an instance of ItemQuality Enum")
        self.name = name
        self.description = description
        self.quality = quality
        self.quality_color = quality.value
        self.image = None # Placeholder for item icon

    def __str__(self):
        return f"{self.name} ({self.quality.name})"

class Equipment(Item):
    """
    Represents an item that can be equipped by the player to gain stats.
    e.g., weapons, armor.
    """
    def __init__(self, name, description, quality, slot, stats_bonus=None):
        super().__init__(name, description, quality)
        self.slot = slot  # e.g., 'weapon', 'head', 'chest', 'legs'
        self.stats_bonus = stats_bonus if stats_bonus else {} # e.g., {'max_health': 10, 'damage': 5}

class Consumable(Item):
    """
    Represents an item that can be consumed for a one-time effect.
    e.g., health potions.
    """
    def __init__(self, name, description, quality, effect):
        super().__init__(name, description, quality)
        # e.g., {'type': 'heal', 'amount': 25}
        self.effect = effect
