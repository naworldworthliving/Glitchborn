import pygame

# --- Constants ---
CAMPFIRE_WIDTH = 50
CAMPFIRE_HEIGHT = 50
CAMPFIRE_COLOR_UNLIT = (100, 100, 100) # Grey
CAMPFIRE_COLOR_LIT = (255, 100, 0) # Orange

class Campfire(pygame.sprite.Sprite):
    """
    A campfire that restores player stats.
    """
    def __init__(self, x, y):
        """
        Initialize the campfire.
        """
        super().__init__()
        self.image = pygame.Surface([CAMPFIRE_WIDTH, CAMPFIRE_HEIGHT])
        self.image.fill(CAMPFIRE_COLOR_LIT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.used = False

    def activate(self, player):
        """
        Activate the campfire to restore player stats.
        """
        if not self.used:
            self.used = True
            player.hp = player.max_hp
            player.stamina = player.max_stamina
            self.image.fill(CAMPFIRE_COLOR_UNLIT)
            print("Campfire activated! Stats restored.")

    def update(self, shift_x=0):
        """
        Update the campfire's position.
        """
        self.rect.x += shift_x
