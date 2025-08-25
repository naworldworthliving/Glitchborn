import pygame
from player import Player
from level import Level
from enemy import Enemy

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Glitchborn"
BLACK = (0, 0, 0)
FPS = 60

class Game:
    """
    Main game class.
    """
    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.level = Level()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player.level = self.level
        self.all_sprites.add(self.player)


    def run(self):
        """
        The main game loop.
        """
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.quit()

    def events(self):
        """
        Handle all events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_f:
                    self.player.attack()

    def update(self):
        """
        Update the game state.
        """
        self.all_sprites.update()
        self.level.update()

        # --- Side-scrolling logic ---
        # If the player gets near the right side, shift the world left (-x)
        if self.player.rect.right > SCREEN_WIDTH - 200:
            shift = self.player.rect.right - (SCREEN_WIDTH - 200)
            self.player.rect.right = SCREEN_WIDTH - 200
            self.level.shift_world(-shift)

        # If the player gets near the left side, shift the world right (+x)
        if self.player.rect.left < 200:
            shift = 200 - self.player.rect.left
            self.player.rect.left = 200
            self.level.shift_world(shift)

        # --- Attack collision ---
        if self.player.attacking:
            # The attack_rect is in screen coordinates. The enemy rects are in world coordinates.
            # We need to check for collision in the same coordinate system.
            # We can check by creating a temporary rect for the enemy in screen coordinates.
            for enemy in self.level.enemy_list:
                # The world_shift is the offset of the world relative to the screen.
                # A positive world_shift means the world has moved right (player went left).
                # So, screen_x = world_x + world_shift
                enemy_screen_rect = enemy.rect.move(self.level.world_shift, 0)
                if self.player.attack_rect.colliderect(enemy_screen_rect):
                    enemy.kill()

        # --- Player-enemy collision ---
        # Only check for player-enemy collision if the player is not attacking.
        if not self.player.attacking:
            enemy_hit_list = pygame.sprite.spritecollide(self.player, self.level.enemy_list, False)
            if enemy_hit_list:
                # For now, just print a message
                print("Player hit an enemy!")
                # We could end the game here, or reduce player health, etc.

    def draw(self):
        """
        Draw everything to the screen.
        """
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """
        Quit the game.
        """
        pygame.quit()

def main():
    """
    Main function to run the game.
    """
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
