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

        # Ground platform - we can make this longer for a longer level
        ground = Platform(5000, 64, tile_image=ground_tile_image)
        ground.rect.x = 0
        ground.rect.y = 536 # Place ground at the bottom of the screen (600 - 64)
        self.platform_list.add(ground)

        # Generate the rest of the level
        self._generate_level()

    def _generate_level(self):
        """
        Procedurally generates the platforms and enemies for the level.
        """
        # --- Generation Parameters ---
        PLATFORM_COUNT = 100
        MIN_WIDTH, MAX_WIDTH = 150, 300
        MIN_GAP, MAX_GAP = 80, 200
        MIN_Y, MAX_Y = 250, 500
        MAX_Y_CHANGE = 80

        last_x = 200
        last_y = 500

        for _ in range(PLATFORM_COUNT):
            width = random.randint(MIN_WIDTH, MAX_WIDTH)
            height = 30 # Standard platform height

            # Calculate new position
            gap = random.randint(MIN_GAP, MAX_GAP)
            x = last_x + gap

            y_change = random.randint(-MAX_Y_CHANGE, MAX_Y_CHANGE)
            y = last_y + y_change

            # Clamp y-position to ensure level is traversable
            y = max(MIN_Y, min(y, MAX_Y))

            # Create and add the platform
            platform = Platform(width, height)
            platform.rect.x = x
            platform.rect.y = y
            self.platform_list.add(platform)

            # Update for next iteration
            last_x = platform.rect.right
            last_y = platform.rect.y

            # --- Optional: Spawn an enemy on this platform ---
            ENEMY_SPAWN_CHANCE = 0.3
            if random.random() < ENEMY_SPAWN_CHANCE:
                enemy = Enemy(platform.rect.x + 20, platform.rect.y - 32) # 32 is ENEMY_HEIGHT
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
