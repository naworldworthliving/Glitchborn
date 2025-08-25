import pygame

class Camera:
    def __init__(self, level_width, level_height):
        self.camera = pygame.Rect(0, 0, level_width, level_height)
        self.width = level_width
        self.height = level_height

    def apply(self, entity):
        """
        Applies the camera offset to an entity's rect.
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """
        Updates the camera's position to follow the target.
        """
        # Center the target in the middle of the screen
        x = -target.rect.centerx + int(pygame.display.get_surface().get_width() / 2)
        y = -target.rect.centery + int(pygame.display.get_surface().get_height() / 2)

        # Limit scrolling to the level's boundaries
        x = min(0, x)  # Don't scroll past the left edge
        y = min(0, y)  # Don't scroll past the top edge
        x = max(-(self.width - pygame.display.get_surface().get_width()), x)  # Don't scroll past the right edge
        y = max(-(self.height - pygame.display.get_surface().get_height()), y) # Don't scroll past the bottom edge

        self.camera = pygame.Rect(x, y, self.width, self.height)
