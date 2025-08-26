import pygame
import random
from player import Player
from level import Level
from enemy import Enemy

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Glitchborn"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
FPS = 60
FONT_NAME = 'sans-serif'

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
        self.game_state = 'playing' # Can be 'playing', 'character_screen', 'inventory_screen'
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.all_sprites = pygame.sprite.Group()
        self.level = Level()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.stat_buttons = {}
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
                if event.key == pygame.K_LSHIFT:
                    self.player.dash()
                if event.key == pygame.K_i:
                    if self.game_state == 'playing':
                        self.game_state = 'character_screen'
                    elif self.game_state == 'character_screen':
                        self.game_state = 'playing'
            if event.type == pygame.MOUSEBUTTONUP:
                if self.game_state == 'character_screen':
                    pos = pygame.mouse.get_pos()
                    for stat_name, button_rect in self.stat_buttons.items():
                        if button_rect.collidepoint(pos):
                            if self.player.available_stat_points > 0:
                                self.player.available_stat_points -= 1
                                current_value = getattr(self.player, stat_name.lower())
                                setattr(self.player, stat_name.lower(), current_value + 1)
                                self.player.update_derived_stats()
                                print(f"Increased {stat_name} to {getattr(self.player, stat_name.lower())}")
                                break # Process one click at a time

    def update(self):
        """
        Update the game state.
        """
        if self.game_state == 'playing':
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
                for enemy in self.level.enemy_list:
                    # Skip enemies already hit in this attack swing
                    if enemy in self.player.hit_enemies_this_attack:
                        continue

                    enemy_screen_rect = enemy.rect.move(self.level.world_shift, 0)
                    if self.player.attack_rect.colliderect(enemy_screen_rect):
                        self.player.hit_enemies_this_attack.append(enemy)

                        damage = self.player.calculate_damage()
                        killed = enemy.take_damage(damage)

                        if killed:
                            xp = random.randint(enemy.xp_reward[0], enemy.xp_reward[1])
                            self.player.add_xp(xp)
                            # Item drop logic
                            if random.random() < 0.5: # 50% drop chance
                                print("Enemy dropped an item!")

            # --- Player-enemy collision ---
            # Only check for player-enemy collision if the player is not attacking or invincible.
            if not self.player.attacking and not self.player.invincible:
                enemy_hit_list = pygame.sprite.spritecollide(self.player, self.level.enemy_list, False)
                if enemy_hit_list:
                    # For now, just print a message
                    print("Player hit an enemy!")
                    # We could end the game here, or reduce player health, etc.

    def draw_text(self, text, size, color, x, y):
        """
        Helper function to draw text on the screen.
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_character_screen(self):
        """
        Draws the character statistics screen.
        """
        # Draw a semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Black with 180/255 alpha
        self.screen.blit(overlay, (0, 0))

        # --- Draw the stats ---
        y_pos = 100
        self.draw_text("Character Stats", 48, WHITE, 100, y_pos)
        y_pos += 60
        self.draw_text(f"Level: {self.player.character_level}", 30, WHITE, 100, y_pos)
        y_pos += 40
        self.draw_text(f"XP: {self.player.xp} / {self.player.xp_to_next_level}", 30, WHITE, 100, y_pos)
        y_pos += 60
        self.draw_text(f"Points to Spend: {self.player.available_stat_points}", 30, GREEN, 100, y_pos)
        y_pos += 60

        stats = {
            "Strength": self.player.strength,
            "Dexterity": self.player.dexterity,
            "Intelligence": self.player.intelligence,
            "Wisdom": self.player.wisdom,
            "Charisma": self.player.charisma,
        }

        button_size = 20
        for stat_name, stat_value in stats.items():
            self.draw_text(f"{stat_name}: {stat_value}", 24, WHITE, 100, y_pos)

            # Draw the '+' button
            button_rect = pygame.Rect(350, y_pos, button_size, button_size)
            pygame.draw.rect(self.screen, WHITE, button_rect)
            self.draw_text("+", 20, BLACK, 355, y_pos - 2) # Adjust text position slightly

            # Store the button rect for click detection later
            self.stat_buttons[stat_name] = button_rect

            y_pos += 40

    def draw(self):
        """
        Draw everything to the screen.
        """
        # Always draw the game world
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # Draw attack hitbox for debugging/feedback
        if self.player.attacking:
            pygame.draw.rect(self.screen, (255, 255, 255), self.player.attack_rect)

        # If in a menu state, draw it on top
        if self.game_state == 'character_screen':
            self.draw_character_screen()

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
