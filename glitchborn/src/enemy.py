import pygame

# --- Constants ---
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_COLOR = (255, 0, 0) # Red
PATROL_SPEED = 2

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy in the game.
    """
    def __init__(self, x, y, patrol_range=100):
        """
        Initialize the enemy.
        """
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xp_reward = (20, 30) # Range of XP granted when defeated
        self.health = 100

        # --- Patrolling AI ---
        self.start_x = x
        self.patrol_range = patrol_range
        self.direction = 1 # 1 for right, -1 for left

    def update(self):
        """
        Update the enemy's behavior (e.g., patrolling).
        """
        self.rect.x += PATROL_SPEED * self.direction

        # Check if we've reached the edge of the patrol range
        if self.rect.x > self.start_x + self.patrol_range:
            self.direction = -1
            # To prevent overshooting, snap back to the edge
            self.rect.x = self.start_x + self.patrol_range
        elif self.rect.x < self.start_x:
            self.direction = 1
            # Snap back to the edge
            self.rect.x = self.start_x

    def take_damage(self, amount):
        """
        Reduces health by the given amount. Returns True if the enemy is killed.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False
