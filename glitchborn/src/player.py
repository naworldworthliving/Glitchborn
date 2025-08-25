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
        # -- Load images for animations ---
        # -- Load images for animations ---
        self.idle_image = pygame.image.load("glitchborn/assets/player_s.png").convert()
        self.idle_image.set_colorkey((255, 255, 255))
        self.walk_frames = [
            pygame.image.load("glitchborn/assets/player_walk1.png").convert(),
            pygame.image.load("glitchborn/assets/player_walk2.png").convert(),
            pygame.image.load("glitchborn/assets/player_walk3.png").convert(),
            pygame.image.load("glitchborn/assets/player_walk4.png").convert()
        ]
        self.attack_frames = [
            pygame.image.load("glitchborn/assets/player_w1.png").convert(),
            pygame.image.load("glitchborn/assets/player_w2.png").convert()
        ]
        for frame in self.walk_frames:
            frame.set_colorkey((255, 255, 255))
        for frame in self.attack_frames:
            frame.set_colorkey((255, 255, 255))

        # Create flipped images for moving left
        self.idle_image_left = pygame.transform.flip(self.idle_image, True, False)
        self.walk_frames_left = [pygame.transform.flip(img, True, False) for img in self.walk_frames]
        self.attack_frames_left = [pygame.transform.flip(img, True, False) for img in self.attack_frames]

        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # --- Animation attributes ---
        self.walking = False
        self.facing_right = True
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100 # ms per frame

        # --- Attack attributes ---
        self.attacking = False
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.attack_duration = 200 # ms
        self.attack_time = 0


        self.change_x = 0
        self.change_y = 0
        self.jump_count = 0
        self.level = None
        self.inventory = []

        # --- Player Stats ---
        self.health = 100
        self.strength = 10
        self.defense = 5

    def update(self):
        """
        Update the player's position and handle physics.
        """
        self._animate()
        self._handle_attack_timer()

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
        self.walking = True
        self.facing_right = False

    def go_right(self):
        """
        Called when the user hits the 'd' key.
        """
        self.change_x = PLAYER_SPEED
        self.walking = True
        self.facing_right = True

    def stop(self):
        """
        Called when the user lets off the keyboard for horizontal movement.
        """
        self.change_x = 0
        self.walking = False

    def _animate(self):
        """
        Handles player animation.
        """
        now = pygame.time.get_ticks()

        # Attack animation
        if self.attacking:
            # roughly corresponds to attack_duration
            time_since_attack = now - self.attack_time
            # Each attack frame is shown for half the attack duration
            frame_duration = self.attack_duration / len(self.attack_frames)
            # Determine which frame to show
            frame_index = int(time_since_attack / frame_duration)
            if frame_index >= len(self.attack_frames):
                frame_index = len(self.attack_frames) -1 # hold last frame

            if self.facing_right:
                self.image = self.attack_frames[frame_index]
            else:
                self.image = self.attack_frames_left[frame_index]

            # Reset walking animation frame index
            self.frame_index = 0
            return

        # Idle animation
        if not self.walking:
            if self.facing_right:
                self.image = self.idle_image
            else:
                self.image = self.idle_image_left
            return

        # Walking animation
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
            if self.facing_right:
                self.image = self.walk_frames[self.frame_index]
            else:
                self.image = self.walk_frames_left[self.frame_index]

        # Store the old center position
        old_center = self.rect.center
        # Update the rect with the new image
        self.rect = self.image.get_rect()
        # Set the new rect's center to the old center
        self.rect.center = old_center

    def attack(self):
        """
        Perform an attack.
        """
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            # Create a hitbox in front of the player
            if self.facing_right:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y, 40, self.rect.height)
            else:
                self.attack_rect = pygame.Rect(self.rect.left - 40, self.rect.y, 40, self.rect.height)

    def _handle_attack_timer(self):
        """
        Handles the timer for the attack duration.
        """
        if self.attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_time > self.attack_duration:
                self.attacking = False
                self.attack_rect = pygame.Rect(0, 0, 0, 0)
