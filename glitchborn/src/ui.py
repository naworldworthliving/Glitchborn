import pygame

# --- UI Constants ---
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
STAMINA_BAR_WIDTH = 200
XP_BAR_WIDTH = 200

# --- Colors ---
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
DARK_GREY = (50, 50, 50)

def draw_player_hud(screen, player):
    """
    Draws the player's Heads-Up Display (HUD), including health, stamina, and XP.
    """
    # --- Font Setup ---
    try:
        font = pygame.font.Font(None, 22)  # Use a default font
    except pygame.error:
        # Fallback to a guaranteed font if the default is not found
        font = pygame.font.Font(pygame.font.get_default_font(), 22)

    # --- Health Bar ---
    # Label
    health_label = font.render(f"HP: {int(player.health)} / {player.max_health}", True, WHITE)
    screen.blit(health_label, (10, 10))
    # Bar
    health_ratio = player.health / player.max_health
    health_bar_rect = pygame.Rect(10, 35, HEALTH_BAR_WIDTH, BAR_HEIGHT)
    pygame.draw.rect(screen, DARK_GREY, health_bar_rect)
    pygame.draw.rect(screen, GREEN, (health_bar_rect.x, health_bar_rect.y, HEALTH_BAR_WIDTH * health_ratio, BAR_HEIGHT))

    # --- Stamina Bar ---
    # Label
    stamina_label = font.render(f"SP: {int(player.stamina)} / {player.max_stamina}", True, WHITE)
    screen.blit(stamina_label, (10, 65))
    # Bar
    stamina_ratio = player.stamina / player.max_stamina
    stamina_bar_rect = pygame.Rect(10, 90, STAMINA_BAR_WIDTH, BAR_HEIGHT)
    pygame.draw.rect(screen, DARK_GREY, stamina_bar_rect)
    pygame.draw.rect(screen, BLUE, (stamina_bar_rect.x, stamina_bar_rect.y, STAMINA_BAR_WIDTH * stamina_ratio, BAR_HEIGHT))

    # --- XP Bar ---
    # Label
    xp_label = font.render(f"XP: {int(player.xp)} / {player.next_level_xp}", True, WHITE)
    screen.blit(xp_label, (10, 120))
    # Bar
    if player.next_level_xp > 0:
        xp_ratio = player.xp / player.next_level_xp
    else:
        xp_ratio = 0
    xp_bar_rect = pygame.Rect(10, 145, XP_BAR_WIDTH, BAR_HEIGHT)
    pygame.draw.rect(screen, DARK_GREY, xp_bar_rect)
    pygame.draw.rect(screen, YELLOW, (xp_bar_rect.x, xp_bar_rect.y, XP_BAR_WIDTH * xp_ratio, BAR_HEIGHT))
