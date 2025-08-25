import pygame
from player import Player
from level import Level
from ui import draw_player_hud
from camera import Camera

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Glitchborn"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        self.game_state = 'playing'

        # --- Font for placeholder screens ---
        self.font = pygame.font.Font(None, 50)

        # --- Game Objects ---
        self.all_sprites = pygame.sprite.Group()
        self.level = Level()
        self.player = Player(100, SCREEN_HEIGHT - 100) # Start player near the beginning
        self.player.level = self.level
        self.all_sprites.add(self.player)

        # --- Camera ---
        self.camera = Camera(self.level.level_width, self.level.level_height)


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
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_state == 'playing':
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                if event.key == pygame.K_i:
                    if self.game_state == 'playing':
                        self.game_state = 'inventory'
                    elif self.game_state == 'inventory':
                        self.game_state = 'playing'
                if event.key == pygame.K_c:
                    if self.game_state == 'playing':
                        self.game_state = 'character'
                    elif self.game_state == 'character':
                        self.game_state = 'playing'

    def update(self):
        """
        Update the game state. Only updates the world if playing.
        """
        if self.game_state == 'playing':
            self.all_sprites.update()
            self.level.update()
            self.camera.update(self.player)

    def draw(self):
        """
        Draws the correct screen based on the current game state.
        """
        if self.game_state == 'playing':
            self.draw_game()
        elif self.game_state == 'inventory':
            self.draw_inventory_screen()
        elif self.game_state == 'character':
            self.draw_character_screen()

        pygame.display.flip()

    def draw_game(self):
        """Draws the main game world."""
        self.screen.fill(BLACK)
        for sprite in self.level.platform_list:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_sprites:
             self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_hud(self.screen, self.player)

    def draw_inventory_screen(self):
        """Draws the placeholder inventory screen."""
        self.screen.fill(BLACK)
        text = self.font.render("INVENTORY", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)

    def draw_character_screen(self):
        """Draws the placeholder character screen."""
        self.screen.fill(BLACK)
        text = self.font.render("CHARACTER SCREEN", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)

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
