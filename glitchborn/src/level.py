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
            # Ground
            [2000, 30, 0, 570],
            # Floating platforms
            [300, 30, 200, 450],
            [250, 30, 550, 350],
            [200, 30, 850, 250],
            [300, 30, 1100, 350],
            [150, 30, 1450, 450],
            [200, 30, 1700, 350],
        ]

        # Calculate level dimensions
        max_x = 0
        max_y = 0
        for data in level_data:
            # data[2] is x, data[0] is width
            if data[2] + data[0] > max_x:
                max_x = data[2] + data[0]
            # data[3] is y, data[1] is height
            if data[3] + data[1] > max_y:
                max_y = data[3] + data[1]

        self.level_width = max_x
        self.level_height = max_y

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
