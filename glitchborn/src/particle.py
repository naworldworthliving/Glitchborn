import pygame
import random

class Particle(pygame.sprite.Sprite):
    """
    A single particle for an effect.
    """
    def __init__(self, x, y):
        """
        Initialize the particle.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.speed = random.uniform(1, 4)
        self.angle = random.uniform(0, 2 * 3.14159)
        self.vx = self.speed * pygame.math.Vector2(1, 0).rotate(self.angle * 180 / 3.14159).x
        self.vy = self.speed * pygame.math.Vector2(1, 0).rotate(self.angle * 180 / 3.14159).y

        self.lifespan = random.uniform(20, 40)
        self.age = 0

        self.color = (random.randint(200, 255), random.randint(0, 50), 0)
        self.radius = random.randint(3, 7)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, shift_x=0):
        """
        Update the particle's position, size, and lifespan.
        """
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x) + shift_x
        self.rect.y = int(self.y)

        self.age += 1
        if self.age >= self.lifespan:
            self.kill()
        else:
            # Fade out
            alpha = max(0, 255 * (1 - self.age / self.lifespan))
            self.image.set_alpha(alpha)


def create_explosion(x, y, particle_group):
    """
    Create a burst of particles.
    """
    particle_count = 20
    for _ in range(particle_count):
        particle = Particle(x, y)
        particle_group.add(particle)
