"""Game state definitions for the Pac-Man application."""

from enum import Enum


class GameStateType(Enum):
    """Represent the possible states of the Pac-Man game."""

    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"
