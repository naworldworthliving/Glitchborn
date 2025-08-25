import pygame
import random
import loot_generator

# --- Colors ---
CHEST_COLOR_CLOSED = (139, 69, 19)  # Brown
CHEST_COLOR_OPEN = (255, 215, 0)   # Gold

class TreasureChest(pygame.sprite.Sprite):
    """
    A chest that contains loot. Can be opened by the player.
    """
    def __init__(self, x, y):
        """
        Initializes the treasure chest.
        """
        super().__init__()
        self.image_closed = pygame.Surface([50, 40])
        self.image_closed.fill(CHEST_COLOR_CLOSED)
        self.image_open = pygame.Surface([50, 40])
        self.image_open.fill(CHEST_COLOR_OPEN)

        self.image = self.image_closed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_opened = False

    def open_chest(self, game_level):
        """
        Opens the chest, changes its appearance, and generates loot.
        Returns a list of items.
        """
        if not self.is_opened:
            self.is_opened = True
            self.image = self.image_open

            # Generate 3-5 items
            num_items = random.randint(3, 5)
            loot = []
            for _ in range(num_items):
                # We use the game_level as the difficulty modifier for better loot
                item = loot_generator.generate_random_item(difficulty_modifier=game_level)
                loot.append(item)
            return loot
        return [] # Return empty list if already opened
