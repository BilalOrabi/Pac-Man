"""Paused state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class PausedState:
    """Handle the paused gameplay state."""

    state_machine: GameStateMachine

    def resume_game(self) -> None:
        """Resume the game from the paused state."""
        self.state_machine.transition_to(GameStateType.PLAYING)

    def return_to_menu(self) -> None:
        """Return to the main menu from the paused state."""
        self.state_machine.transition_to(GameStateType.MENU)

    def is_active(self) -> bool:
        """Return whether the game is currently paused."""
        return self.state_machine.is_in_state(GameStateType.PAUSED)
