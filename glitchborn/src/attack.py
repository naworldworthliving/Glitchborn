import pygame

class Attack(pygame.sprite.Sprite):
    """
    Represents the hitbox for a player's attack.
    It's a short-lived sprite that damages enemies on collision.
    """
    def __init__(self, x, y, direction):
        """
        Initializes the attack sprite.
        'x' and 'y' are the coordinates for positioning the attack.
        'direction' should be 'left' or 'right'.
        """
        super().__init__()
        self.image = pygame.Surface([40, 30])
        self.image.fill((255, 255, 0))  # Yellow for high visibility during testing
        self.rect = self.image.get_rect()

        # Position the hitbox based on player's direction
        if direction == 'right':
            self.rect.left = x
        else:  # 'left'
            self.rect.right = x
        self.rect.centery = y

        self.spawn_time = pygame.time.get_ticks()
        self.duration = 150  # milliseconds

    def update(self):
        """
        The attack sprite destroys itself after its duration expires.
        """
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()
