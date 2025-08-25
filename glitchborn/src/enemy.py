import pygame

# --- Constants ---
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = (255, 0, 0) # Red

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy in the game.
    """
    def __init__(self, x, y):
        """
        Initialize the enemy.
        """
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 30

        # AI attributes
        self.start_x = x
        self.speed = 2
        self.direction = 1 # 1 for right, -1 for left
        self.patrol_range = 100

    def take_damage(self, amount):
        """
        Take damage and check for death. Returns True if the enemy died.
        """
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def update(self, shift_x=0):
        """
        Update the enemy's position and AI.
        """
        # --- Patrol AI ---
        self.rect.x += self.direction * self.speed
        if self.rect.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.patrol_range:
            self.direction = 1

        # Adjust for world shift
        self.rect.x += shift_x
        self.start_x += shift_x # The patrol center needs to shift with the world
