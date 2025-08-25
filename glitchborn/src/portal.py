import pygame

# --- Constants ---
PORTAL_WIDTH = 40
PORTAL_HEIGHT = 60
PORTAL_COLOR = (128, 0, 128) # Purple

class Portal(pygame.sprite.Sprite):
    """
    Represents a portal to the next level.
    """
    def __init__(self, x, y):
        """
        Initialize the portal.
        """
        super().__init__()
        self.image = pygame.Surface([PORTAL_WIDTH, PORTAL_HEIGHT])
        self.image.fill(PORTAL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, shift_x=0):
        """
        Update the portal's position.
        """
        self.rect.x += shift_x
