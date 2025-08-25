import pygame

# --- Item Quality ---
ITEM_QUALITIES = {
    "poor": {"color": (150, 150, 150), "modifier": 0.7}, # Grey
    "normal": {"color": (255, 255, 255), "modifier": 1.0}, # White
    "rare": {"color": (0, 100, 255), "modifier": 1.5}, # Blue
    "super_rare": {"color": (128, 0, 128), "modifier": 2.0}, # Purple
    "unique": {"color": (255, 165, 0), "modifier": 2.5} # Orange
}

class Item:
    """
    Represents an item with stats and a quality.
    """
    def __init__(self, name, quality="normal", stats=None):
        self.name = name
        self.quality = quality
        self.stats = stats if stats is not None else {}
        self.color = ITEM_QUALITIES[self.quality]["color"]

    def __str__(self):
        return f"{self.quality.capitalize()} {self.name}"

class DroppedItem(pygame.sprite.Sprite):
    """
    Represents an item that has been dropped on the ground.
    """
    def __init__(self, x, y, item):
        """
        Initialize the dropped item sprite.
        """
        super().__init__()
        self.item = item

        # Create a simple visual for the dropped item (e.g., a small colored square)
        self.image = pygame.Surface([15, 15])
        self.image.fill(self.item.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, shift_x=0):
        """
        Update the item's position.
        """
        self.rect.x += shift_x
