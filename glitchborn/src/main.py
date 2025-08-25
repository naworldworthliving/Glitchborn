import pygame
from player import Player
from level import Level
from enemy import Enemy
from item import Item, generate_random_item, ITEM_QUALITIES

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Glitchborn"
BLACK = (0, 0, 0)
FPS = 60
FONT_NAME = "arial"

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, size=20):
        super().__init__()
        self.font = pygame.font.SysFont(FONT_NAME, size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alpha = 255
        self.fade_speed = 5
        self.lift_speed = 1

    def update(self):
        self.rect.y -= self.lift_speed
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

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
        self.font = pygame.font.SysFont(FONT_NAME, 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.level = Level()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player.level = self.level
        self.all_sprites.add(self.player)
        self.character_screen_open = False
        self.inventory_screen_open = False


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
                if event.key == pygame.K_c:
                    self.character_screen_open = not self.character_screen_open
                    self.inventory_screen_open = False
                if event.key == pygame.K_i:
                    self.inventory_screen_open = not self.inventory_screen_open
                    self.character_screen_open = False

    def update(self):
        """
        Update the game state.
        """
        if self.character_screen_open or self.inventory_screen_open:
            return

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
            # Attack collision logic
            for enemy in self.level.enemy_list:
                if self.player.attack_rect.colliderect(enemy.rect):
                    # Kill the enemy
                    enemy.kill()
                    # Drop an item
                    item = generate_random_item()
                    self.player.inventory.append(item)
                    # Show item name
                    text = FloatingText(enemy.rect.centerx, enemy.rect.top,
                                        item.name, ITEM_QUALITIES[item.quality])
                    self.level.floating_text_group.add(text)

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

        if self.character_screen_open:
            self.draw_character_screen()
        elif self.inventory_screen_open:
            self.draw_inventory_screen()

        pygame.display.flip()

    def draw_inventory_screen(self):
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        self.draw_text("Inventory", 50, 50)
        y_offset = 100
        for item in self.player.inventory:
            color = ITEM_QUALITIES.get(item.quality, (255, 255, 255))
            self.draw_text(item.name, 50, y_offset, color)
            y_offset += 30

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_character_screen(self):
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Stats
        self.draw_text("Character Stats", 50, 50)
        self.draw_text(f"Health: {self.player.health}", 50, 100)
        self.draw_text(f"Strength: {self.player.strength}", 50, 130)
        self.draw_text(f"Defense: {self.player.defense}", 50, 160)

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
