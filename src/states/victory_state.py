"""Victory state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class VictoryState:
    """Handle the state reached when the player completes the game."""

    state_machine: GameStateMachine

    def return_to_menu(self) -> None:
        """Return to the main menu after completing the game."""
        self.state_machine.transition_to(GameStateType.MENU)

    def start_new_game(self) -> None:
        """Start a new game after completing the previous game."""
        self.state_machine.transition_to(GameStateType.PLAYING)

    def is_active(self) -> bool:
        """Return whether the victory state is currently active."""
        return self.state_machine.is_in_state(GameStateType.VICTORY)
