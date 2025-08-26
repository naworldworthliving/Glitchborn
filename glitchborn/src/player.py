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
        for frame in self.walk_frames:
            frame.set_colorkey((255, 255, 255))

        # Create flipped images for moving left
        self.idle_image_left = pygame.transform.flip(self.idle_image, True, False)
        self.walk_frames_left = [pygame.transform.flip(img, True, False) for img in self.walk_frames]

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
        self.attack_duration = 300 # ms
        self.attack_time = 0
        self.hit_enemies_this_attack = []

        # --- Movement State ---
        self.crouching = False
        self.original_height = PLAYER_HEIGHT

        # --- Dash State ---
        self.dashing = False
        self.invincible = False
        self.dash_speed = 15
        self.dash_duration = 200 # ms
        self.dash_cooldown = 1000 # ms
        self.last_dash_time = -self.dash_cooldown # Allow dashing immediately
        self.dash_start_time = 0

        # --- Stats ---
        self.character_level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.strength = 5
        self.dexterity = 5
        self.intelligence = 5
        self.wisdom = 5
        self.charisma = 5
        self.available_stat_points = 0


        self.change_x = 0
        self.change_y = 0
        self.jump_count = 0
        self.level = None

        self.update_derived_stats()

    def update_derived_stats(self):
        """
        Updates player attributes that are derived from base stats.
        Call this whenever a stat is changed.
        """
        # Dexterity affects dash speed and cooldown
        base_dash_speed = 15
        self.dash_speed = base_dash_speed + (self.dexterity * 0.5)

        base_dash_cooldown = 1000 # ms
        self.dash_cooldown = base_dash_cooldown - (self.dexterity * 40)
        if self.dash_cooldown < 200: # Set a minimum cooldown
            self.dash_cooldown = 200

    def calculate_damage(self):
        """
        Calculates melee damage based on strength.
        """
        base_damage = 10
        return base_damage + (self.strength * 2)

    def update(self):
        """
        Update the player's position and handle physics.
        """
        # --- Handle Input and State Updates ---
        self._handle_dash() # Manage dash state first

        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            self.crouch()
        else:
            self.uncrouch()

        # Process movement input if not dashing or crouching
        if not self.dashing and not self.crouching:
            if keys[pygame.K_a]:
                self.go_left()
            elif keys[pygame.K_d]:
                self.go_right()
            else:
                self.stop()
        elif self.crouching:
            self.stop()

        # --- Update animations ---
        self._animate()
        self._handle_attack_timer()

        # --- Physics and Collisions ---
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

    def calc_grav(self):
        """
        Calculate the effect of gravity.
        """
        if self.dashing:
            self.change_y = 0
            return

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

    def jump(self):
        """
        Called when the user hits the jump button.
        """
        if self.crouching:
            return

        # Check if we are on the ground
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.jump_count < 2:
            self.change_y = JUMP_HEIGHT
            self.jump_count += 1

    def dash(self):
        """Initiate a dash if cooldown is over."""
        now = pygame.time.get_ticks()
        if now - self.last_dash_time > self.dash_cooldown:
            if not self.crouching and not self.dashing:
                self.dashing = True
                self.invincible = True
                self.dash_start_time = now

                if self.facing_right:
                    self.change_x = self.dash_speed
                else:
                    self.change_x = -self.dash_speed

    def _handle_dash(self):
        """Manage dash state, duration, and cooldown."""
        if self.dashing:
            now = pygame.time.get_ticks()
            if now - self.dash_start_time > self.dash_duration:
                self.dashing = False
                self.invincible = False
                self.last_dash_time = now # Cooldown starts when dash ends
                self.stop()

    def crouch(self):
        """Enter crouching state."""
        if not self.crouching:
            self.crouching = True
            bottom = self.rect.bottom
            self.rect.height = self.original_height // 2
            self.rect.bottom = bottom

    def uncrouch(self):
        """Exit crouching state if possible."""
        if self.crouching:
            # Check for space above before standing up
            bottom = self.rect.bottom
            self.rect.height = self.original_height
            self.rect.bottom = bottom

            # Check for collision with platforms above
            self.rect.y -= 1 # Move up slightly to detect ceiling
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y += 1 # Move back down

            if block_hit_list:
                # Obstacle above, cannot uncrouch, revert height change
                self.rect.height = self.original_height // 2
                self.rect.bottom = bottom
            else:
                self.crouching = False

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
        Handles player animation, including scaling for crouching.
        """
        now = pygame.time.get_ticks()

        # Determine base image based on state
        base_image = None
        if not self.walking:
            base_image = self.idle_image if self.facing_right else self.idle_image_left
        else: # Walking
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
            base_image = self.walk_frames[self.frame_index] if self.facing_right else self.walk_frames_left[self.frame_index]

        # Preserve position and dimensions
        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        # Scale image to current rect height
        current_height = self.rect.height
        new_width = base_image.get_rect().width
        self.image = pygame.transform.scale(base_image, (new_width, current_height))

        # Reset rect based on new image and restore position
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = old_centerx

    def attack(self):
        """
        Perform an attack.
        """
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.hit_enemies_this_attack.clear() # Clear list for new attack
            # Create a hitbox in front of the player
            if self.facing_right:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y, 60, self.rect.height)
            else:
                self.attack_rect = pygame.Rect(self.rect.left - 60, self.rect.y, 60, self.rect.height)

    def _handle_attack_timer(self):
        """
        Handles the timer for the attack duration.
        """
        if self.attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_time > self.attack_duration:
                self.attacking = False
                self.attack_rect = pygame.Rect(0, 0, 0, 0)
                self.hit_enemies_this_attack.clear()

    def add_xp(self, amount):
        """
        Add XP to the player and check for level up.
        """
        self.xp += amount
        print(f"Player gained {amount} XP! Total XP: {self.xp}/{self.xp_to_next_level}")
        self._check_level_up()

    def _check_level_up(self):
        """
        Check if the player has enough XP to level up.
        """
        while self.xp >= self.xp_to_next_level:
            self.character_level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = 100 * self.character_level
            self.available_stat_points += 5
            print(f"Ding! You reached level {self.character_level}!")
            print(f"You have {self.available_stat_points} stat points to spend.")
