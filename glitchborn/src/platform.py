import pygame

# --- Constants ---
PLATFORM_COLOR = (0, 255, 0) # Green

class Platform(pygame.sprite.Sprite):
    """
    Represents a platform in the game.
    """
    def __init__(self, width, height, tile_image=None):
        """
        Initialize the platform.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        if tile_image:
            tile_w, tile_h = tile_image.get_size()
            for x in range(0, int(width), tile_w):
                for y in range(0, int(height), tile_h):
                    self.image.blit(tile_image, (x, y))
        else:
            self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
