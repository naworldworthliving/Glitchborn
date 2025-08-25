import pygame

# --- Constants ---
BAR_HEIGHT = 20
HP_BAR_WIDTH = 200
STAMINA_BAR_WIDTH = 150
XP_BAR_WIDTH = 250

HP_COLOR = (255, 0, 0) # Red
STAMINA_COLOR = (0, 255, 0) # Green
XP_COLOR = (0, 0, 255) # Blue
BAR_BACKGROUND_COLOR = (50, 50, 50) # Dark Grey
BORDER_COLOR = (255, 255, 255) # White

class UI:
    """
    Handles the user interface, including stat bars.
    """
    def __init__(self, player):
        """
        Initialize the UI.
        """
        self.player = player
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 24)

    def _draw_bar(self, x, y, width, height, fill_pct, color, label):
        """
        Draw a single stat bar.
        """
        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, BAR_BACKGROUND_COLOR, bg_rect)
        # Fill
        fill_width = width * fill_pct
        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, color, fill_rect)
        # Border
        pygame.draw.rect(self.screen, BORDER_COLOR, bg_rect, 2)
        # Label
        text_surface = self.font.render(label, True, BORDER_COLOR)
        self.screen.blit(text_surface, (x + 5, y + height))


    def draw(self):
        """
        Draw all UI elements.
        """
        # --- HP Bar ---
        hp_pct = self.player.hp / self.player.max_hp
        hp_label = f"HP: {self.player.hp}/{self.player.max_hp}"
        self._draw_bar(10, 10, HP_BAR_WIDTH, BAR_HEIGHT, hp_pct, HP_COLOR, hp_label)

        # --- Stamina Bar ---
        stamina_pct = self.player.stamina / self.player.max_stamina
        stamina_label = f"Stamina: {int(self.player.stamina)}/{self.player.max_stamina}"
        self._draw_bar(10, 50, STAMINA_BAR_WIDTH, BAR_HEIGHT, stamina_pct, STAMINA_COLOR, stamina_label)

        # --- XP Bar ---
        xp_pct = self.player.xp / self.player.xp_to_next_level
        xp_label = f"XP: {self.player.xp}/{self.player.xp_to_next_level}"
        self._draw_bar(10, 90, XP_BAR_WIDTH, BAR_HEIGHT, xp_pct, XP_COLOR, xp_label)

        # --- Level Text ---
        level_text = f"Level: {self.player.level}"
        level_surface = self.font.render(level_text, True, BORDER_COLOR)
        self.screen.blit(level_surface, (10, 130))
