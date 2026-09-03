"""Menu state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class MenuState:
    """Handle the behavior of the Pac-Man main menu."""

    state_machine: GameStateMachine

    def start_game(self) -> None:
        """Start a new game from the main menu."""
        self.state_machine.transition_to(GameStateType.PLAYING)

    def is_active(self) -> bool:
        """Return whether the menu is currently active."""
        return self.state_machine.is_in_state(GameStateType.MENU)
