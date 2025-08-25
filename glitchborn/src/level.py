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
        self.world_shift = 0
        self.background_x = 0

        # Load background
        try:
            self.background_image = pygame.image.load("glitchborn/assets/bg1.png").convert()
        except (pygame.error, FileNotFoundError):
            self.background_image = pygame.Surface([800, 600])
            self.background_image.fill((100, 100, 100)) # Gray placeholder

        # Load ground tile
        try:
            ground_tile_image = pygame.image.load("glitchborn/assets/groundtile.png").convert()
        except (pygame.error, FileNotFoundError):
            ground_tile_image = pygame.Surface([64, 64])
            ground_tile_image.fill((0, 255, 0)) # Green placeholder

        # Ground platform
        ground = Platform(2000, 64, tile_image=ground_tile_image)
        ground.rect.x = 0
        ground.rect.y = 536 # Place ground at the bottom of the screen (600 - 64)
        self.platform_list.add(ground)


        # Array of platform data: [width, height, x, y]
        level_data = [
            [500, 30, 100, 500],
            [300, 30, 300, 400],
            [200, 30, 550, 300],
        ]

        for data in level_data:
            platform = Platform(data[0], data[1])
            platform.rect.x = data[2]
            platform.rect.y = data[3]
            self.platform_list.add(platform)

        # Array of enemy data: [x, y]
        enemy_data = [
            [400, 504], # Adjusted for new ground height
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
        self.background_x += shift_x * 0.5

        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def draw(self, screen):
        """
        Draw all the sprites in the level.
        """
        # Draw the background
        bg_width = self.background_image.get_width()
        # Calculate the position of the first background image
        bg1_x = self.background_x % bg_width
        # Calculate the position of the second background image
        bg2_x = bg1_x - bg_width
        # Draw the two background images
        screen.blit(self.background_image, (bg1_x, 0))
        screen.blit(self.background_image, (bg2_x, 0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def update(self):
        """
        Update everything in this level.
        """
        self.platform_list.update()
        self.enemy_list.update()
