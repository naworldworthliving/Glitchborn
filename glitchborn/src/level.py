import pygame
import random
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

        # Level dimensions
        level_width = 10000

        # Ground platform
        ground = Platform(level_width, 30)
        ground.rect.x = 0
        ground.rect.y = 570
        self.platform_list.add(ground)

        # Procedurally generate platforms
        last_x = 0
        for x in range(0, level_width, 200):
            if x - last_x > 400: # Ensure platforms are not too far apart
                x = last_x + random.randint(200, 400)

            if x >= level_width:
                break

            width = random.randint(150, 300)
            height = 30

            # Ensure platforms are reachable
            y = random.randint(300, 540)

            platform = Platform(width, height)
            platform.rect.x = x
            platform.rect.y = y
            self.platform_list.add(platform)

            # Add an enemy on some platforms
            if random.random() < 0.3: # 30% chance of an enemy
                enemy = Enemy(x + width / 2, y - 32)
                self.enemy_list.add(enemy)

            last_x = x + width

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
