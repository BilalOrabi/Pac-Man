"""Renderer responsible for Pac-Man user-interface information."""

from dataclasses import dataclass

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

    def shutdown(self) -> None:
        """Shut down the user-interface renderer."""
        self.menu_font_asset = None
        self.game_font_asset = None
        self.is_initialized = False
