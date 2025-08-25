import pygame
from platform import Platform

class Level:
    """
    This class represents a single level. It creates all the platforms and other
    objects for the level.
    """
    def __init__(self):
        """
        Initialize the level.
        """
        self.platform_list = pygame.sprite.Group()

        # Array of platform data: [width, height, x, y]
        level_data = [
            [500, 30, 100, 500],
            [300, 30, 300, 400],
            [200, 30, 550, 300],
            # Ground platform
            [800, 30, 0, 570],
        ]

        for data in level_data:
            platform = Platform(data[0], data[1])
            platform.rect.x = data[2]
            platform.rect.y = data[3]
            self.platform_list.add(platform)

    def draw(self, screen):
        """
        Draw all the sprites in the level.
        """
        # We will draw the background here later
        self.platform_list.draw(screen)

    def update(self):
        """
        Update everything in this level.
        """
        self.platform_list.update()
