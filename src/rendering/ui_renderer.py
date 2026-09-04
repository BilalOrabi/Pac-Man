"""Renderer responsible for Pac-Man user-interface information."""

from dataclasses import dataclass, field
from typing import Any

import pygame

from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class UIRenderer(Renderer):
    """Render score, lives, level, and other game information."""

    asset_manager: AssetManager
    is_initialized: bool = False
    score: int = 0
    lives: int = 0
    level_number: int = 1
    message: str = ""
    menu_font_asset: str | None = None
    game_font_asset: str | None = None
    surface: Any = None
    game_state_name: str = "PLAYING"
    time_remaining: float = 0.0
    active_cheats: list[str] = field(default_factory=list)
    name_input: str = ""
    highscores: list[dict[str, Any]] = field(default_factory=list)
    menu_selection: int = 0
    menu_view: str = "main"

    def initialize(self) -> None:
        """Initialize the user-interface renderer."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.menu_font_asset = self.asset_manager.get_font("menu")
        self.game_font_asset = self.asset_manager.get_font("game")

        self.is_initialized = True

    def set_score(self, score: int) -> None:
        """Set the score displayed by the user interface."""
        if score < 0:
            raise ValueError("Score cannot be negative.")

        self.score = score

    def set_lives(self, lives: int) -> None:
        """Set the number of lives displayed by the user interface."""
        if lives < 0:
            raise ValueError("Lives cannot be negative.")

        self.lives = lives

    def set_level_number(self, level_number: int) -> None:
        """Set the level number displayed by the user interface."""
        if level_number <= 0:
            raise ValueError(
                "Level number must be greater than zero."
            )

        self.level_number = level_number

    def set_message(self, message: str) -> None:
        """Set a message displayed by the user interface."""
        if not isinstance(message, str):
            raise TypeError("message must be a string.")

        self.message = message

    def render(self) -> None:
        """Render the current user-interface information."""
        if not self.is_initialized:
            raise RuntimeError(
                "UIRenderer must be initialized before rendering."
            )

        if self.menu_font_asset is None:
            raise RuntimeError(
                "Menu font asset must be configured before rendering."
            )

        if self.game_font_asset is None:
            raise RuntimeError(
                "Game font asset must be configured before rendering."
            )

        if self.surface is not None:
            self._render_to_surface()

    def _get_font(self, size: int) -> pygame.font.Font | None:
        """Create or return a font of the requested size."""
        try:
            if not pygame.font.get_init():
                pygame.font.init()
            return pygame.font.SysFont(
                "consolas,courier,arial", size, bold=True
            )
        except Exception:
            return None

    def _render_to_surface(self) -> None:
        """Draw UI elements onto the Pygame display surface."""
        if self.surface is None:
            return

        font = self._get_font(18)
        header_font = self._get_font(32)
        if font is None:
            return

        state = self.game_state_name.upper()

        if state == "MENU":
            self._render_menu(font, header_font)
        elif state == "PAUSED":
            self._render_hud(font)
            self._render_pause_overlay(font, header_font)
        elif state == "GAME_OVER":
            self._render_game_over(font, header_font)
        elif state == "VICTORY":
            self._render_victory(font, header_font)
        elif state == "ENTER_NAME":
            self._render_enter_name(font, header_font)
        else:
            self._render_hud(font)

    def _render_hud(self, font: pygame.font.Font) -> None:
        """Render top in-game HUD banner and cheat bar."""
        surf_w = self.surface.get_width()

        # Top HUD strip background
        pygame.draw.rect(self.surface, (15, 15, 30), (0, 0, surf_w, 40))
        pygame.draw.line(
            self.surface, (50, 50, 100), (0, 40), (surf_w, 40), 2
        )

        # HUD text items
        score_text = font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"LIVES: {self.lives}", True, (255, 255, 0))
        level_str = f"LEVEL: {self.level_number}"
        level_text = font.render(level_str, True, (0, 255, 255))
        time_sec = max(0, int(self.time_remaining))
        time_text = font.render(f"TIME: {time_sec}s", True, (255, 180, 0))

        self.surface.blit(score_text, (20, 10))
        self.surface.blit(lives_text, (220, 10))
        self.surface.blit(level_text, (380, 10))
        self.surface.blit(time_text, (540, 10))

        # Bottom banner for message or active cheats
        surf_h = self.surface.get_height()
        if self.active_cheats:
            cheats_str = "CHEATS: " + " | ".join(self.active_cheats)
            cheats_surf = font.render(cheats_str, True, (255, 80, 80))
            self.surface.blit(cheats_surf, (20, surf_h - 28))
        elif self.message:
            msg_surf = font.render(self.message, True, (255, 220, 100))
            self.surface.blit(msg_surf, (20, surf_h - 28))

    def _render_menu(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render main menu with navigable options."""
        self.surface.fill((10, 10, 25))
        w = self.surface.get_width()
        h = self.surface.get_height()

        title_font = header_font or font
        title = title_font.render("P A C - M A N", True, (255, 255, 0))
        sub = font.render("42 School Project", True, (160, 160, 200))

        self.surface.blit(title, (w // 2 - title.get_width() // 2, 70))
        self.surface.blit(sub, (w // 2 - sub.get_width() // 2, 115))

        if self.menu_view == "highscores":
            self._render_highscores_view(font, w, h)
            return

        if self.menu_view == "instructions":
            self._render_instructions_view(font, w, h)
            return

        options = [
            "1. Start Game",
            "2. Highscores",
            "3. Instructions",
            "4. Exit",
        ]

        start_y = 190
        for i, opt in enumerate(options):
            is_selected = i == self.menu_selection
            color = (255, 255, 50) if is_selected else (200, 200, 200)
            prefix = "> " if is_selected else "  "
            text_surf = font.render(f"{prefix}{opt}", True, color)
            self.surface.blit(text_surf, (w // 2 - 120, start_y + i * 45))

        foot = "UP/DOWN: Navigate | ENTER: Select"
        footer = font.render(foot, True, (120, 120, 160))
        self.surface.blit(footer, (w // 2 - footer.get_width() // 2, h - 50))

    def _render_highscores_view(
        self, font: pygame.font.Font, w: int, h: int
    ) -> None:
        """Render leaderboard view."""
        hs_title = font.render(
            "=== HALL OF FAME (TOP 10) ===", True, (0, 255, 255)
        )
        self.surface.blit(hs_title, (w // 2 - hs_title.get_width() // 2, 170))

        start_y = 220
        if not self.highscores:
            no_hs = font.render("No highscores yet!", True, (180, 180, 180))
            no_hs_x = w // 2 - no_hs.get_width() // 2
            self.surface.blit(no_hs, (no_hs_x, start_y))
        else:
            for idx, entry in enumerate(self.highscores[:10]):
                name = entry.get("name", "PLAYER")
                score = entry.get("score", 0)
                row_str = f"#{idx + 1:2d}  {name:<10}  {score:>6d}"
                row_surf = font.render(row_str, True, (255, 255, 255))
                pos = (w // 2 - 140, start_y + idx * 28)
                self.surface.blit(row_surf, pos)

        back = font.render(
            "Press ESC or ENTER to return", True, (120, 120, 160)
        )
        self.surface.blit(back, (w // 2 - back.get_width() // 2, h - 50))

    def _render_instructions_view(
        self, font: pygame.font.Font, w: int, h: int
    ) -> None:
        """Render instructions view."""
        inst_title = font.render("=== HOW TO PLAY ===", True, (0, 255, 255))
        self.surface.blit(
            inst_title, (w // 2 - inst_title.get_width() // 2, 160)
        )

        lines = [
            "CONTROLS:",
            "  Arrow Keys / WASD  : Move Pac-Man",
            "  P / ESC            : Pause Game",
            "",
            "CHEATS (Numeric Keys):",
            "  1 : Invincibility Toggle",
            "  2 : Freeze Ghosts Toggle",
            "  3 : Speed Boost Toggle",
            "  4 : Extra Life (+1)",
            "  5 : Skip Level",
            "",
            "SCORING:",
            "  Pacgum: +10 pts | Super: +50 pts | Ghost: +200 pts",
        ]
        for idx, line in enumerate(lines):
            color = (255, 220, 100) if line.endswith(":") else (200, 200, 200)
            line_surf = font.render(line, True, color)
            self.surface.blit(line_surf, (w // 2 - 240, 200 + idx * 24))

        back = font.render(
            "Press ESC or ENTER to return", True, (120, 120, 160)
        )
        self.surface.blit(back, (w // 2 - back.get_width() // 2, h - 50))

    def _render_pause_overlay(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render pause message overlay."""
        w = self.surface.get_width()
        h = self.surface.get_height()

        title_font = header_font or font
        p_text = title_font.render("P A U S E D", True, (255, 255, 0))
        msg = "Press ESC or P to Resume | M for Menu"
        sub_text = font.render(msg, True, (220, 220, 220))

        self.surface.blit(
            p_text, (w // 2 - p_text.get_width() // 2, h // 2 - 30)
        )
        self.surface.blit(
            sub_text, (w // 2 - sub_text.get_width() // 2, h // 2 + 20)
        )

    def _render_game_over(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Game Over screen."""
        self.surface.fill((25, 10, 10))
        w = self.surface.get_width()
        h = self.surface.get_height()

        title_font = header_font or font
        go_text = title_font.render("G A M E   O V E R", True, (255, 50, 50))
        sc_str = f"Final Score: {self.score}"
        score_text = font.render(sc_str, True, (255, 255, 255))
        prompt_str = "Press ENTER to continue | ESC for Menu"
        prompt = font.render(prompt_str, True, (200, 200, 200))

        self.surface.blit(
            go_text, (w // 2 - go_text.get_width() // 2, h // 2 - 60)
        )
        self.surface.blit(
            score_text, (w // 2 - score_text.get_width() // 2, h // 2 - 10)
        )
        self.surface.blit(
            prompt, (w // 2 - prompt.get_width() // 2, h // 2 + 40)
        )

    def _render_victory(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Victory screen."""
        self.surface.fill((10, 25, 15))
        w = self.surface.get_width()
        h = self.surface.get_height()

        title_font = header_font or font
        vic_text = title_font.render("V I C T O R Y !", True, (50, 255, 50))
        cong_str = "You completed all maze levels!"
        cong_text = font.render(cong_str, True, (220, 255, 220))
        score_text = font.render(
            f"Final Score: {self.score}", True, (255, 255, 255)
        )
        prompt_str = "Press ENTER to save score | ESC for Menu"
        prompt = font.render(prompt_str, True, (200, 200, 200))

        self.surface.blit(
            vic_text, (w // 2 - vic_text.get_width() // 2, h // 2 - 70)
        )
        self.surface.blit(
            cong_text, (w // 2 - cong_text.get_width() // 2, h // 2 - 25)
        )
        self.surface.blit(
            score_text, (w // 2 - score_text.get_width() // 2, h // 2 + 15)
        )
        self.surface.blit(
            prompt, (w // 2 - prompt.get_width() // 2, h // 2 + 60)
        )

    def _render_enter_name(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Name Entry screen."""
        self.surface.fill((15, 15, 30))
        w = self.surface.get_width()
        h = self.surface.get_height()

        title_font = header_font or font
        rec_text = title_font.render("RECORD HIGH SCORE", True, (255, 215, 0))
        sc_str = f"Your Score: {self.score}"
        score_text = font.render(sc_str, True, (255, 255, 255))
        prompt_str = "Enter Name (max 10 chars):"
        prompt = font.render(prompt_str, True, (200, 200, 255))

        # Input box
        box_rect = pygame.Rect(w // 2 - 150, h // 2 + 10, 300, 40)
        pygame.draw.rect(self.surface, (30, 30, 60), box_rect)
        pygame.draw.rect(self.surface, (0, 255, 255), box_rect, 2)

        input_text = font.render(f"{self.name_input}_", True, (255, 255, 255))
        self.surface.blit(input_text, (box_rect.x + 15, box_rect.y + 10))

        footer_str = "ENTER: Submit | ESC: Skip"
        footer = font.render(footer_str, True, (140, 140, 180))

        self.surface.blit(
            rec_text, (w // 2 - rec_text.get_width() // 2, h // 2 - 80)
        )
        self.surface.blit(
            score_text, (w // 2 - score_text.get_width() // 2, h // 2 - 40)
        )
        self.surface.blit(
            prompt, (w // 2 - prompt.get_width() // 2, h // 2 - 15)
        )
        self.surface.blit(
            footer, (w // 2 - footer.get_width() // 2, h // 2 + 70)
        )

    def shutdown(self) -> None:
        """Shut down the user-interface renderer."""
        self.menu_font_asset = None
        self.game_font_asset = None
        self.is_initialized = False
