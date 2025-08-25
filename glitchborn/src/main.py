import pygame
from player import Player
from level import Level

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
                if event.key == pygame.K_w:
                    self.player.jump()

    def update(self):
        """
        Update the game state.
        """
        self.all_sprites.update()
        self.level.update()

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
