"""Input event definitions for the Pac-Man game."""

from dataclasses import dataclass
from enum import Enum


class InputAction(Enum):
    """Represent actions that can be triggered by user input."""

    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE_GAME = "pause_game"
    START_GAME = "start_game"
    RESTART_GAME = "restart_game"
    RETURN_TO_MENU = "return_to_menu"
    QUIT_GAME = "quit_game"


@dataclass(frozen=True)
class InputEvent:
    """Represent one processed user input event."""

    action: InputAction
