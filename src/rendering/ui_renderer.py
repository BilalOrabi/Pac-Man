"""Renderer responsible for Pac-Man user-interface information."""

from dataclasses import dataclass


@dataclass
class UIRenderer:
    """Render score, lives, level, and other game information."""

    is_initialized: bool = False
    score: int = 0
    lives: int = 0
    level_number: int = 1
    message: str = ""

    def initialize(self) -> None:
        """Initialize the user-interface renderer."""
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

    def shutdown(self) -> None:
        """Shut down the user-interface renderer."""
        self.is_initialized = False
