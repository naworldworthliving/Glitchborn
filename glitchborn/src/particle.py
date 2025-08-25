import pygame
import random

class Particle(pygame.sprite.Sprite):
    """
    A particle effect for enemy deaths.
    """
    def __init__(self, x, y):
        """
        Initialize the particle.
        """
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill((255, 255, 255)) # White
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Set a random velocity
        self.change_x = random.randrange(-5, 6)
        self.change_y = random.randrange(-5, 6)

        # Set a lifetime for the particle
        self.lifetime = 20 # Number of frames
        self.life_timer = 0

    def update(self):
        """
        Update the particle's position and lifetime.
        """
        # Move the particle
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # "Fade" the particle by making it smaller
        self.life_timer += 1
        if self.life_timer > self.lifetime:
            self.kill()
