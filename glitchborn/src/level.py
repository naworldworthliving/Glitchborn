import pygame
import random
from platform import Platform
from enemy import Enemy
from treasure import TreasureChest
from portal import Portal

class Level:
    """
    This class handles the creation and management of a single level.
    """
    def __init__(self):
        """
        Initialize the level.
        """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.world_objects = pygame.sprite.Group() # For chest, portal, etc.
        self.dropped_items = pygame.sprite.Group()
        self.portal = None # To be created when chest is opened
        self.world_shift = 0
        self.generate_level()


    def generate_level(self):
        """
        Generate a new procedural level.
        """
        # Clear existing sprites
        self.platform_list.empty()
        self.enemy_list.empty()
        self.world_objects.empty()
        self.dropped_items.empty()

        # --- Level generation parameters ---
        level_length = 50 # Number of platforms
        platform_width_range = (100, 250)
        platform_height = 30
        x_gap_range = (80, 150)
        y_gap_range = (-100, 100)

        # --- Start with a ground platform ---
        last_x = 0
        last_y = 570
        ground = Platform(1000, platform_height)
        ground.rect.x = -200
        ground.rect.y = last_y
        self.platform_list.add(ground)

        # --- Generate platforms ---
        for i in range(level_length):
            width = random.randint(*platform_width_range)
            x_gap = random.randint(*x_gap_range)
            y_gap = random.randint(*y_gap_range)

            x = last_x + x_gap + width
            y = last_y + y_gap

            # Clamp y to be within screen bounds (with some margin)
            y = max(100, min(y, 570))

            platform = Platform(width, platform_height)
            platform.rect.x = x
            platform.rect.y = y
            self.platform_list.add(platform)

            last_x = x
            last_y = y

            # --- Spawn enemies ---
            if random.random() < 0.2: # 20% chance to spawn an enemy on a platform
                enemy = Enemy(x + width / 2, y - 32)
                self.enemy_list.add(enemy)

        # --- Add treasure chest at the end ---
        chest_x = last_x + 100
        chest_y = last_y - 40
        self.treasure_chest = TreasureChest(chest_x, chest_y)
        self.world_objects.add(self.treasure_chest)

    def shift_world(self, shift_x):
        """
        Shift the world left or right.
        """
        self.world_shift += shift_x
        self.platform_list.update(shift_x)
        self.enemy_list.update(shift_x)
        self.world_objects.update(shift_x)
        self.dropped_items.update(shift_x)

    def draw(self, screen):
        """
        Draw all the sprites in the level.
        """
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.world_objects.draw(screen)
        self.dropped_items.draw(screen)

    def update(self):
        """
        Update everything in this level.
        """
        self.platform_list.update()
        self.enemy_list.update()
        self.world_objects.update()
        self.dropped_items.update()
