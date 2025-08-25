import pygame

# --- Enemy Constants ---
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 48
ENEMY_COLOR = (200, 0, 0)  # Dark Red

class Enemy(pygame.sprite.Sprite):
    """
    Base class for all enemies in the game.
    """
    def __init__(self, x, y, patrol_range=100, difficulty_modifier=1.0):
        """
        Initialize the enemy.
        'x' and 'y' are the starting coordinates.
        'patrol_range' is the horizontal distance the enemy will patrol from its start point.
        'difficulty_modifier' scales the enemy's stats.
        """
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # --- Movement ---
        self.patrol_start = x
        self.patrol_end = x + patrol_range
        self.change_x = 2  # Patrolling speed

        # --- Stats ---
        self.difficulty_modifier = difficulty_modifier
        self.max_health = int(50 * difficulty_modifier)
        self.health = self.max_health
        self.damage = int(10 * difficulty_modifier)

    def update(self):
        """
        Update the enemy's position and behavior.
        """
        # --- Patrol AI ---
        self.rect.x += self.change_x
        if self.rect.right > self.patrol_end or self.rect.left < self.patrol_start:
            self.change_x *= -1  # Reverse direction

    def take_damage(self, amount):
        """
        Reduces the enemy's health by a given amount.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Removes the sprite from all groups it's in
