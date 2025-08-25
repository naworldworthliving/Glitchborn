import pygame

# --- Constants ---
CHEST_WIDTH = 40
CHEST_HEIGHT = 40
CHEST_COLOR_CLOSED = (255, 255, 0) # Yellow
CHEST_COLOR_OPEN = (255, 200, 0) # Darker Yellow

class TreasureChest(pygame.sprite.Sprite):
    """
    Represents a treasure chest in the game.
    """
    def __init__(self, x, y):
        """
        Initialize the treasure chest.
        """
        super().__init__()
        self.image = pygame.Surface([CHEST_WIDTH, CHEST_HEIGHT])
        self.image.fill(CHEST_COLOR_CLOSED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.opened = False

    def open(self):
        """
        Open the chest.
        """
        if not self.opened:
            self.opened = True
            self.image.fill(CHEST_COLOR_OPEN)

    def update(self, shift_x=0):
        """
        Update the chest's position.
        """
        self.rect.x += shift_x
