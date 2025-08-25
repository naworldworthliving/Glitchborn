import pygame
import random
from player import Player
from level import Level
from enemy import Enemy
from treasure import TreasureChest
from portal import Portal
from ui import UI
from item import DroppedItem
from item_generator import generate_random_item

# --- Constants ---
DROP_CHANCE = 0.5 # 50%
PLAYER_REACH = 50 # pixels
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
        self.ui = UI(self.player)


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
                if event.key == pygame.K_e:
                    self.check_interaction()

    def update(self):
        """
        Update the game state.
        """
        self.all_sprites.update()
        self.level.update()

        # --- Side-scrolling logic ---
        if self.player.rect.right > SCREEN_WIDTH - 200:
            shift = self.player.rect.right - (SCREEN_WIDTH - 200)
            self.player.rect.right = SCREEN_WIDTH - 200
            self.level.shift_world(-shift)
        if self.player.rect.left < 200:
            shift = 200 - self.player.rect.left
            self.player.rect.left = 200
            self.level.shift_world(shift)

        # --- Collision detection ---
        # Attack collision
        if self.player.attacking:
            # We need to make sure we only hit each enemy once per attack
            if not hasattr(self.player, 'hit_enemies_this_attack'):
                self.player.hit_enemies_this_attack = []

            for enemy in self.level.enemy_list:
                if enemy not in self.player.hit_enemies_this_attack:
                    enemy_screen_rect = enemy.rect.move(self.level.world_shift, 0)
                    if self.player.attack_rect.colliderect(enemy_screen_rect):
                        self.player.hit_enemies_this_attack.append(enemy)
                        if enemy.take_damage(self.player.attack_damage):
                            # Enemy died, roll for drop
                            if random.random() < DROP_CHANCE:
                                item = generate_random_item()
                                dropped_item_sprite = DroppedItem(enemy.rect.x, enemy.rect.y, item)
                                self.level.dropped_items.add(dropped_item_sprite)
        else:
            # Reset the hit list when not attacking
            self.player.hit_enemies_this_attack = []

        # Player-enemy collision
        if not self.player.attacking:
            if pygame.sprite.spritecollide(self.player, self.level.enemy_list, False):
                print("Player hit an enemy!")


        # Player-portal collision
        if self.level.portal:
            portal_screen_rect = self.level.portal.rect.move(self.level.world_shift, 0)
            if self.player.rect.colliderect(portal_screen_rect):
                self.next_level()

        # Player-item collision (pickup)
        for item_sprite in self.level.dropped_items:
            item_screen_rect = item_sprite.rect.move(self.level.world_shift, 0)
            if self.player.rect.colliderect(item_screen_rect):
                if self.player.inventory.add_item(item_sprite.item):
                    item_sprite.kill()

    def next_level(self):
        """
        Go to the next level.
        """
        print("Moving to the next level!")
        # Reset player position
        self.player.rect.x = SCREEN_WIDTH / 2
        self.player.rect.y = SCREEN_HEIGHT / 2
        self.player.change_x = 0
        self.player.change_y = 0
        # Generate new level
        self.level.world_shift = 0
        self.level.generate_level()

    def check_interaction(self):
        """
        Check if the player is close enough to interact with an object.
        """
        # Check for chest interaction
        if self.level.treasure_chest and not self.level.treasure_chest.opened:
            chest_screen_rect = self.level.treasure_chest.rect.move(self.level.world_shift, 0)
            if self.player.rect.colliderect(chest_screen_rect.inflate(PLAYER_REACH, PLAYER_REACH)):
                self.level.treasure_chest.open()
                # Spawn portal
                portal_x = self.level.treasure_chest.rect.x
                portal_y = self.level.treasure_chest.rect.y - 60
                self.level.portal = Portal(portal_x, portal_y)
                self.level.world_objects.add(self.level.portal)
                return # Interact with one thing at a time

        # Check for campfire interaction
        if self.level.campfire and not self.level.campfire.used:
            campfire_screen_rect = self.level.campfire.rect.move(self.level.world_shift, 0)
            if self.player.rect.colliderect(campfire_screen_rect.inflate(PLAYER_REACH, PLAYER_REACH)):
                self.level.campfire.activate(self.player)
                return # Interact with one thing at a time


    def draw(self):
        """
        Draw everything to the screen.
        """
        self.screen.fill(BLACK)
        self.level.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # Draw attack visual
        if self.player.attacking:
            self.screen.blit(self.player.attack_image, self.player.attack_rect)

        # Draw UI
        self.ui.draw()

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
