import pygame
from player import Player
from level import Level
from ui import draw_player_hud
from camera import Camera
from attack import Attack
import loot_generator

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Glitchborn"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
INTERACTION_RANGE = 50 # pixels

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
        self.game_level = 1

        # --- Font for placeholder screens ---
        self.font = pygame.font.Font(None, 50)

        # --- Game Objects ---
        self.all_sprites = pygame.sprite.Group()
        self.attacks = pygame.sprite.Group()
        self.level = Level()
        self.player = Player(100, SCREEN_HEIGHT - 100)
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
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_f:
                        new_attack = self.player.attack()
                        self.attacks.add(new_attack)
                    if event.key == pygame.K_e:
                        self.handle_interaction()
                if event.key == pygame.K_i:
                    if self.game_state == 'playing': self.game_state = 'inventory'
                    elif self.game_state == 'inventory': self.game_state = 'playing'
                if event.key == pygame.K_c:
                    if self.game_state == 'playing': self.game_state = 'character'
                    elif self.game_state == 'character': self.game_state = 'playing'

    def update(self):
        """
        Update the game state. Only updates the world if playing.
        """
        if self.game_state == 'playing':
            self.all_sprites.update()
            self.level.update()
            self.attacks.update()
            self.camera.update(self.player)
            self.handle_combat()

    def handle_interaction(self):
        """Handles player interaction with world objects like chests."""
        for chest in self.level.treasure_chests:
            # Check distance between player and chest
            dist_x = abs(self.player.rect.centerx - chest.rect.centerx)
            dist_y = abs(self.player.rect.centery - chest.rect.centery)
            if dist_x < INTERACTION_RANGE and dist_y < INTERACTION_RANGE:
                loot = chest.open_chest(self.game_level)
                if loot:
                    print(f"Chest opened! Player received {len(loot)} items.")
                    for item in loot:
                        self.player.add_to_inventory(item)
                        print(f"  - {item}")


    def handle_combat(self):
        """Checks and processes collisions between attacks and enemies."""
        hits = pygame.sprite.groupcollide(self.level.enemy_list, self.attacks, False, True)
        for enemy in hits:
            is_defeated = (enemy.health - self.player.damage) <= 0
            enemy.take_damage(self.player.damage)
            if is_defeated:
                loot = loot_generator.generate_random_item(enemy.difficulty_modifier)
                self.player.add_to_inventory(loot)
                print(f"Player received loot: {loot}")

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
        for sprite in self.level.enemy_list:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.level.treasure_chests:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_sprites: # Player
             self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.attacks:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_hud(self.screen, self.player)

    def draw_inventory_screen(self):
        """Draws the placeholder inventory screen."""
        self.screen.fill(BLACK)
        text = self.font.render("INVENTORY", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 50))
        self.screen.blit(text, text_rect)
        for i, item in enumerate(self.player.inventory):
            item_text = self.font.render(str(item), True, item.quality_color)
            self.screen.blit(item_text, (50, 100 + i * 40))

    def draw_character_screen(self):
        """Draws the placeholder character screen."""
        self.screen.fill(BLACK)
        text = self.font.render("CHARACTER SCREEN", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)

    def quit(self):
        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
