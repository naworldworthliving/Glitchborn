import pygame

# --- Constants ---
PLATFORM_COLOR = (0, 255, 0) # Green

class Platform(pygame.sprite.Sprite):
    """
    Represents a platform in the game.
    """
    def __init__(self, width, height):
        """
        Initialize the platform.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
