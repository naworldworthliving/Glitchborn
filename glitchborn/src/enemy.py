import pygame

# --- Constants ---
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = (255, 0, 0) # Red

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy in the game.
    """
    def __init__(self, x, y):
        """
        Initialize the enemy.
        """
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
