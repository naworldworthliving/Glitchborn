import pygame
from attack import Attack

# --- Constants ---
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_COLOR = (255, 0, 0) # Red
PLAYER_SPEED = 5
GRAVITY = 0.35
JUMP_HEIGHT = -10

class Player(pygame.sprite.Sprite):
    """
    The player character.
    """
    def __init__(self, start_x, start_y):
        """
        Initialize the player.
        """
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.change_x = 0
        self.change_y = 0
        self.jump_count = 0
        self.level = None
        self.direction = 'right'

        # --- Player Stats ---
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.xp = 0
        self.next_level_xp = 100
        self.damage = 15

        # --- Damage Cooldown ---
        self.invincible = False
        self.invincibility_duration = 1000  # in milliseconds
        self.last_hit_time = 0

        # --- Inventory ---
        self.inventory = []

    def update(self):
        """
        Update the player's position and handle physics.
        """
        # --- Invincibility Timer ---
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time > self.invincibility_duration:
                self.invincible = False
                self.image.set_alpha(255) # Return to normal opacity
            else:
                self.image.set_alpha(128) # Become semi-transparent

        # --- Gravity ---
        self.calc_grav()

        # --- Handle keyboard input for horizontal movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.go_left()
        elif keys[pygame.K_d]:
            self.go_right()
        else:
            self.stop()

        # --- Move left/right and check for platform collisions ---
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # --- Move up/down and check for platform collisions ---
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.jump_count = 0
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0

        # --- Check for enemy collisions ---
        if not self.invincible:
            enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            if enemy_hit_list:
                self.take_damage(enemy_hit_list[0].damage)

    def calc_grav(self):
        """ Calculate the effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

    def jump(self):
        """ Called when the user hits the jump button. """
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.jump_count < 2:
            self.change_y = JUMP_HEIGHT
            self.jump_count += 1

    def attack(self):
        """Creates an attack sprite."""
        if self.direction == 'right':
            attack_x = self.rect.right
        else: # left
            attack_x = self.rect.left
        return Attack(attack_x, self.rect.centery, self.direction)

    def go_left(self):
        self.change_x = -PLAYER_SPEED
        self.direction = 'left'

    def go_right(self):
        self.change_x = PLAYER_SPEED
        self.direction = 'right'

    def stop(self):
        self.change_x = 0

    def take_damage(self, amount):
        """Reduces player health and makes them invincible for a short time."""
        if not self.invincible:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            self.invincible = True
            self.last_hit_time = pygame.time.get_ticks()

    def add_to_inventory(self, item):
        """Adds an item to the player's inventory."""
        self.inventory.append(item)
