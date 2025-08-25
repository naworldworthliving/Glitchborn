import pygame

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

        # --- Player Stats ---
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.xp = 0
        self.next_level_xp = 100

    def update(self):
        """
        Update the player's position and handle physics.
        """
        # --- Gravity ---
        self.calc_grav()

        # --- Move left/right ---
        self.rect.x += self.change_x

        # Check for horizontal collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # --- Move up/down ---
        self.rect.y += self.change_y

        # Check for vertical collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.jump_count = 0
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0

        # --- Handle keyboard input for horizontal movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.go_left()
        elif keys[pygame.K_d]:
            self.go_right()
        else:
            self.stop()

    def calc_grav(self):
        """
        Calculate the effect of gravity.
        """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

    def jump(self):
        """
        Called when the user hits the jump button.
        """
        # Check if we are on the ground
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.jump_count < 2:
            self.change_y = JUMP_HEIGHT
            self.jump_count += 1


    def go_left(self):
        """
        Called when the user hits the 'a' key.
        """
        self.change_x = -PLAYER_SPEED

    def go_right(self):
        """
        Called when the user hits the 'd' key.
        """
        self.change_x = PLAYER_SPEED

    def stop(self):
        """
        Called when the user lets off the keyboard for horizontal movement.
        """
        self.change_x = 0
