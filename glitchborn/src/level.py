import pygame
from platform import Platform
from enemy import Enemy

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
        self.enemy_list = pygame.sprite.Group()
        self.floating_text_group = pygame.sprite.Group()
        self.world_shift = 0

        # Array of platform data: [width, height, x, y]
        level_data = [
            [500, 30, 100, 500],
            [300, 30, 300, 400],
            [200, 30, 550, 300],
            # Ground platform
            [2000, 30, 0, 570],
        ]

        for data in level_data:
            platform = Platform(data[0], data[1])
            platform.rect.x = data[2]
            platform.rect.y = data[3]
            self.platform_list.add(platform)

        # Array of enemy data: [x, y]
        enemy_data = [
            [400, 540],
            [800, 370],
        ]

        for data in enemy_data:
            enemy = Enemy(data[0], data[1])
            self.enemy_list.add(enemy)

    def shift_world(self, shift_x):
        """
        Shift the world left or right.
        """
        self.world_shift += shift_x
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for text in self.floating_text_group:
            text.rect.x += shift_x

    def draw(self, screen):
        """
        Draw all the sprites in the level.
        """
        # We will draw the background here later
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.floating_text_group.draw(screen)

    def update(self):
        """
        Update everything in this level.
        """
        self.platform_list.update()
        self.enemy_list.update()
        self.floating_text_group.update()
