"""Renderer responsible for Pac-Man user-interface information."""

import os
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
    background_asset: str | None = None
    surface: Any = None
    game_state_name: str = "PLAYING"
    time_remaining: float = 0.0
    active_cheats: list[str] = field(default_factory=list)
    name_input: str = ""
    highscores: list[dict[str, Any]] = field(default_factory=list)
    menu_selection: int = 0
    menu_view: str = "main"
    last_outcome: str = "game_over"
    _bg_cache: dict[tuple[str, int, int], pygame.Surface] = field(
        default_factory=dict, init=False, repr=False
    )

    def initialize(self) -> None:
        """Initialize the user-interface renderer."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.menu_font_asset = self.asset_manager.get_font("menu")
        self.game_font_asset = self.asset_manager.get_font("game")
        if hasattr(self.asset_manager, "get_background"):
            bg = self.asset_manager.get_background()
            if isinstance(bg, str):
                self.background_asset = bg

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

    def _load_scaled_image(
        self, file_path: str, width: int, height: int
    ) -> pygame.Surface | None:
        """Load and cache a scaled image by file path with fallback."""
        try:
            target_path = file_path
            if not os.path.exists(target_path):
                if target_path.endswith(".png"):
                    alt_path = target_path[:-4] + ".jpg"
                    if os.path.exists(alt_path):
                        target_path = alt_path
                elif target_path.endswith(".jpg"):
                    alt_path = target_path[:-4] + ".png"
                    if os.path.exists(alt_path):
                        target_path = alt_path

            if not os.path.exists(target_path):
                return None

            cache_key = (target_path, width, height)
            if hasattr(self, "_bg_cache") and cache_key in self._bg_cache:
                return self._bg_cache[cache_key]

            raw_img = pygame.image.load(target_path)
            if pygame.display.get_surface() is not None:
                img = raw_img.convert()
            else:
                img = raw_img
            scaled = pygame.transform.scale(img, (width, height))
            if not hasattr(self, "_bg_cache"):
                self._bg_cache = {}
            self._bg_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _get_background_image(
        self, width: int, height: int
    ) -> pygame.Surface | None:
        """Load and cache the scaled menu background image."""
        try:
            bg_path = (
                self.background_asset
                if self.background_asset is not None
                else self.asset_manager.get_background()
            )
            if not isinstance(bg_path, str) or not bg_path:
                return None
            return self._load_scaled_image(bg_path, width, height)
        except Exception:
            return None

    def _get_victory_background(
        self, width: int, height: int
    ) -> pygame.Surface | None:
        """Load and cache the scaled victory background image."""
        return self._load_scaled_image(
            "assets/images/victory_background.jpg", width, height
        )

    def _get_game_over_background(
        self, width: int, height: int
    ) -> pygame.Surface | None:
        """Load and cache the scaled game over background image."""
        return self._load_scaled_image(
            "assets/images/game_over_background.jpg", width, height
        )

    @staticmethod
    def _draw_text_with_shadow(
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int],
        pos: tuple[int, int],
        shadow_color: tuple[int, int, int] = (0, 0, 0),
        offset: tuple[int, int] = (2, 2),
        center_x: bool = False,
    ) -> None:
        """Draw text with a drop shadow for high contrast."""
        t_surf = font.render(text, True, color)
        s_surf = font.render(text, True, shadow_color)
        x, y = pos
        if center_x:
            x = x - t_surf.get_width() // 2
        surface.blit(s_surf, (x + offset[0], y + offset[1]))
        surface.blit(t_surf, (x, y))

    def _render_menu_background(self, w: int, h: int) -> None:
        """Render the background image or fallback solid color."""
        bg_surf = self._get_background_image(w, h)
        if bg_surf is not None:
            self.surface.blit(bg_surf, (0, 0))
        else:
            self.surface.fill((10, 10, 25))

    def _draw_menu_options(
        self,
        card_x: int,
        card_y: int,
        opt_font: pygame.font.Font,
        options: list[str],
    ) -> None:
        """Render selectable menu items inside the menu card."""
        for i, opt in enumerate(options):
            is_selected = i == self.menu_selection
            color = (255, 255, 60) if is_selected else (210, 210, 210)
            prefix = "> " if is_selected else "  "
            self._draw_text_with_shadow(
                self.surface,
                opt_font,
                f"{prefix}{opt}",
                color,
                (card_x + 60, card_y + 25 + i * 48),
            )

    def _draw_menu_footer(
        self, w: int, h: int, footer_font: pygame.font.Font
    ) -> None:
        """Render navigation hints footer at bottom of menu."""
        foot_w = 420
        foot_box = pygame.Surface((foot_w, 36), pygame.SRCALPHA)
        foot_box.fill((10, 10, 25, 180))
        pygame.draw.rect(
            foot_box, (80, 80, 120), (0, 0, foot_w, 36), 1, border_radius=8
        )
        self.surface.blit(foot_box, ((w - foot_w) // 2, h - 55))

        foot = "UP/DOWN: Navigate | ENTER: Select"
        self._draw_text_with_shadow(
            self.surface,
            footer_font,
            foot,
            (200, 200, 220),
            (w // 2, h - 47),
            center_x=True,
        )

    def _render_menu(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render main menu with navigable options and background image."""
        w = self.surface.get_width()
        h = self.surface.get_height()
        self._render_menu_background(w, h)

        title_font = self._get_font(52) or header_font or font
        sub_font = self._get_font(22) or font
        opt_font = self._get_font(26) or font
        footer_font = self._get_font(18) or font

        self._draw_text_with_shadow(
            self.surface,
            title_font,
            "P A C - M A N",
            (255, 220, 0),
            (w // 2, 45),
            center_x=True,
        )
        self._draw_text_with_shadow(
            self.surface,
            sub_font,
            "42 School Project",
            (240, 240, 255),
            (w // 2, 115),
            center_x=True,
        )

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

        card_w, card_h = 480, 230
        card_x = (w - card_w) // 2
        card_y = 155

        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card.fill((10, 10, 25, 205))
        pygame.draw.rect(
            card, (255, 180, 0), (0, 0, card_w, card_h), 2, border_radius=12
        )
        self.surface.blit(card, (card_x, card_y))

        self._draw_menu_options(card_x, card_y, opt_font, options)
        self._draw_menu_footer(w, h, footer_font)

    def _render_highscores_view(
        self, font: pygame.font.Font, w: int, h: int
    ) -> None:
        """Render leaderboard view on top of menu background."""
        card_w, card_h = 600, 480
        card_x = (w - card_w) // 2
        card_y = 150

        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card.fill((10, 10, 25, 215))
        pygame.draw.rect(
            card, (0, 255, 255), (0, 0, card_w, card_h), 2, border_radius=12
        )
        self.surface.blit(card, (card_x, card_y))

        title_f = self._get_font(22) or font
        row_f = self._get_font(20) or font

        self._draw_text_with_shadow(
            self.surface,
            title_f,
            "=== HALL OF FAME (TOP 10) ===",
            (0, 255, 255),
            (w // 2, card_y + 20),
            center_x=True,
        )

        start_y = card_y + 65
        if not self.highscores:
            self._draw_text_with_shadow(
                self.surface,
                row_f,
                "No highscores yet!",
                (180, 180, 180),
                (w // 2, start_y + 20),
                center_x=True,
            )
        else:
            for idx, entry in enumerate(self.highscores[:10]):
                name = entry.get("name", "PLAYER")
                score = entry.get("score", 0)
                row_str = f"#{idx + 1:2d}  {name:<10}  {score:>6d}"
                self._draw_text_with_shadow(
                    self.surface,
                    row_f,
                    row_str,
                    (255, 255, 255),
                    (card_x + 100, start_y + idx * 32),
                )

        self._draw_text_with_shadow(
            self.surface,
            row_f,
            "Press ESC or ENTER to return",
            (160, 160, 200),
            (w // 2, card_y + card_h - 40),
            center_x=True,
        )

    def _render_instructions_view(
        self, font: pygame.font.Font, w: int, h: int
    ) -> None:
        """Render instructions view on top of menu background."""
        card_w, card_h = 680, 490
        card_x = (w - card_w) // 2
        card_y = 150

        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card.fill((10, 10, 25, 215))
        pygame.draw.rect(
            card, (0, 255, 255), (0, 0, card_w, card_h), 2, border_radius=12
        )
        self.surface.blit(card, (card_x, card_y))

        title_f = self._get_font(22) or font
        text_f = self._get_font(18) or font

        self._draw_text_with_shadow(
            self.surface,
            title_f,
            "=== HOW TO PLAY ===",
            (0, 255, 255),
            (w // 2, card_y + 18),
            center_x=True,
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
            self._draw_text_with_shadow(
                self.surface,
                text_f,
                line,
                color,
                (card_x + 40, card_y + 55 + idx * 26),
            )

        self._draw_text_with_shadow(
            self.surface,
            text_f,
            "Press ESC or ENTER to return",
            (160, 160, 200),
            (w // 2, card_y + card_h - 35),
            center_x=True,
        )

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

    def _draw_outcome_card(
        self,
        w: int,
        h: int,
        fill: tuple[int, int, int, int],
        border: tuple[int, int, int],
        inner: tuple[int, int, int],
    ) -> int:
        """Render frosted glass card at bottom and return its top-left Y."""
        card_w = min(640, w - 40)
        card_h = 135
        card_x = (w - card_w) // 2
        card_y = max(10, h - card_h - 25)

        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card.fill(fill)
        pygame.draw.rect(
            card, border, (0, 0, card_w, card_h), 2, border_radius=14
        )
        pygame.draw.rect(
            card,
            inner,
            (2, 2, card_w - 4, card_h - 4),
            1,
            border_radius=12,
        )
        self.surface.blit(card, (card_x, card_y))
        return card_y

    def _render_game_over(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Game Over screen with themed artwork and UI card."""
        self.last_outcome = "game_over"
        w = self.surface.get_width()
        h = self.surface.get_height()

        bg_surf = self._get_game_over_background(w, h)
        if bg_surf is not None:
            self.surface.blit(bg_surf, (0, 0))
        else:
            self.surface.fill((25, 10, 10))

        card_y = self._draw_outcome_card(
            w, h, (26, 12, 16, 225), (255, 70, 70), (200, 40, 40)
        )

        title_font = self._get_font(26) or header_font or font
        info_font = self._get_font(19) or font
        action_font = self._get_font(17) or font

        self._draw_text_with_shadow(
            self.surface,
            title_font,
            "G A M E   O V E R",
            (255, 70, 70),
            (w // 2, card_y + 14),
            center_x=True,
        )

        sub_str = (
            f"Level Reached: {self.level_number}   |   "
            f"FINAL SCORE: {self.score}"
        )
        self._draw_text_with_shadow(
            self.surface,
            info_font,
            sub_str,
            (255, 200, 200),
            (w // 2, card_y + 54),
            center_x=True,
        )

        prompt_str = (
            "[ ENTER: Enter Name & Save Score ]       [ ESC: Main Menu ]"
        )
        self._draw_text_with_shadow(
            self.surface,
            action_font,
            prompt_str,
            (255, 255, 255),
            (w // 2, card_y + 94),
            center_x=True,
        )

    def _render_victory(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Victory screen with themed artwork and UI card."""
        self.last_outcome = "victory"
        w = self.surface.get_width()
        h = self.surface.get_height()

        bg_surf = self._get_victory_background(w, h)
        if bg_surf is not None:
            self.surface.blit(bg_surf, (0, 0))
        else:
            self.surface.fill((10, 25, 15))

        card_y = self._draw_outcome_card(
            w, h, (10, 22, 28, 225), (50, 255, 120), (255, 215, 0)
        )

        title_font = self._get_font(26) or header_font or font
        info_font = self._get_font(19) or font
        action_font = self._get_font(17) or font

        self._draw_text_with_shadow(
            self.surface,
            title_font,
            "* * *   V I C T O R Y !   * * *",
            (255, 215, 0),
            (w // 2, card_y + 14),
            center_x=True,
        )

        sub_str = (
            f"All Maze Levels Conquered!   |   "
            f"FINAL SCORE: {self.score}"
        )
        self._draw_text_with_shadow(
            self.surface,
            info_font,
            sub_str,
            (180, 255, 200),
            (w // 2, card_y + 54),
            center_x=True,
        )

        prompt_str = (
            "[ ENTER: Enter Name & Save Score ]       [ ESC: Main Menu ]"
        )
        self._draw_text_with_shadow(
            self.surface,
            action_font,
            prompt_str,
            (255, 255, 255),
            (w // 2, card_y + 94),
            center_x=True,
        )

    def _draw_name_input_box(
        self, card_w: int, card_y: int, w: int, font: pygame.font.Font
    ) -> None:
        """Render text entry box for player name input."""
        box_w, box_h = min(320, card_w - 60), 44
        box_x = (w - box_w) // 2
        box_y = card_y + 144
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        input_bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        input_bg.fill((25, 30, 50, 220))
        self.surface.blit(input_bg, (box_x, box_y))
        pygame.draw.rect(
            self.surface, (0, 255, 255), box_rect, 2, border_radius=6
        )

        input_text = f"{self.name_input}_"
        self._draw_text_with_shadow(
            self.surface,
            font,
            input_text,
            (255, 255, 255),
            (box_x + 16, box_y + 11),
        )

    def _render_enter_name(
        self, font: pygame.font.Font, header_font: pygame.font.Font | None
    ) -> None:
        """Render Name Entry screen with themed backdrop and frosted card."""
        w = self.surface.get_width()
        h = self.surface.get_height()

        bg_surf = (
            self._get_victory_background(w, h)
            if self.last_outcome == "victory"
            else self._get_game_over_background(w, h)
        )
        if bg_surf is not None:
            self.surface.blit(bg_surf, (0, 0))
        else:
            self.surface.fill((15, 15, 30))

        # Centered frosted glass card
        card_w = min(560, w - 40)
        card_h = 280
        card_x = (w - card_w) // 2
        card_y = (h - card_h) // 2

        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card.fill((16, 18, 32, 235))
        pygame.draw.rect(
            card, (0, 255, 255), (0, 0, card_w, card_h), 2, border_radius=14
        )
        pygame.draw.rect(
            card,
            (255, 215, 0),
            (2, 2, card_w - 4, card_h - 4),
            1,
            border_radius=12,
        )
        self.surface.blit(card, (card_x, card_y))

        title_font = self._get_font(26) or header_font or font
        info_font = self._get_font(20) or font
        label_font = self._get_font(18) or font
        footer_font = self._get_font(16) or font

        self._draw_text_with_shadow(
            self.surface,
            title_font,
            "RECORD HIGH SCORE",
            (255, 215, 0),
            (w // 2, card_y + 20),
            center_x=True,
        )

        sc_str = f"FINAL SCORE: {self.score}"
        self._draw_text_with_shadow(
            self.surface,
            info_font,
            sc_str,
            (255, 255, 255),
            (w // 2, card_y + 62),
            center_x=True,
        )

        prompt_str = "Enter Name (max 10 chars):"
        self._draw_text_with_shadow(
            self.surface,
            label_font,
            prompt_str,
            (200, 240, 255),
            (w // 2, card_y + 102),
            center_x=True,
        )

        self._draw_name_input_box(card_w, card_y, w, label_font)

        footer_str = "[ ENTER: Submit & Save ]       [ ESC: Skip ]"
        self._draw_text_with_shadow(
            self.surface,
            footer_font,
            footer_str,
            (170, 190, 225),
            (w // 2, card_y + 228),
            center_x=True,
        )

    def shutdown(self) -> None:
        """Shut down the user-interface renderer."""
        self.menu_font_asset = None
        self.game_font_asset = None
        self.background_asset = None
        if hasattr(self, "_bg_cache"):
            self._bg_cache.clear()
        self.is_initialized = False
