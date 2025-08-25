import pygame
from platform import Platform
from enemy import Enemy
from world_objects import TreasureChest

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
        self.treasure_chests = pygame.sprite.Group()

        # --- Platform Data ---
        platform_data = [
            # Ground
            [4000, 30, 0, 570],
            # Floating platforms
            [300, 30, 200, 450],
            [250, 30, 550, 350],
            [200, 30, 850, 250],
            [300, 30, 1100, 350],
            [150, 30, 1450, 450],
            [200, 30, 1700, 350],
            [400, 30, 2000, 400],
            [150, 30, 2500, 300],
            [250, 30, 2800, 450],
            [300, 30, 3200, 350],
            [200, 30, 3600, 250],
        ]

        # --- Enemy Data ---
        enemy_data = [
            [300, 402, 100, 1.0],
            [600, 302, 150, 1.2],
            [1200, 302, 100, 1.5],
            [1750, 302, 100, 1.8],
            [2200, 352, 100, 2.0],
            [2850, 402, 100, 2.2],
            [3300, 302, 150, 2.5],
        ]

        # --- Treasure Chest Data ---
        # [x, y]
        chest_data = [
            [3900, 530] # At the end of the 4000px ground platform
        ]

        # --- Process Platforms ---
        max_x = 0
        max_y = 0
        for data in platform_data:
            if data[2] + data[0] > max_x: max_x = data[2] + data[0]
            if data[3] + data[1] > max_y: max_y = data[3] + data[1]
            platform = Platform(data[0], data[1])
            platform.rect.x = data[2]
            platform.rect.y = data[3]
            self.platform_list.add(platform)

        self.level_width = max_x
        self.level_height = max_y

        # --- Process Enemies ---
        for data in enemy_data:
            enemy = Enemy(data[0], data[1], patrol_range=data[2], difficulty_modifier=data[3])
            self.enemy_list.add(enemy)

        # --- Process Treasure Chests ---
        for data in chest_data:
            chest = TreasureChest(data[0], data[1])
            self.treasure_chests.add(chest)

    def draw(self, screen):
        """
        Draw all the sprites in the level.
        """
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.treasure_chests.draw(screen)

    def update(self):
        """
        Update everything in this level.
        """
        self.platform_list.update()
        self.enemy_list.update()
        self.treasure_chests.update()
