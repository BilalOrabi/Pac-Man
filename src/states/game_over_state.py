"""Game-over state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class GameOverState:
    """Handle the state reached when the player loses the game."""

    state_machine: GameStateMachine

    def restart_game(self) -> None:
        """Start a new game from the game-over state."""
        self.state_machine.transition_to(GameStateType.PLAYING)

    def return_to_menu(self) -> None:
        """Return to the main menu."""
        self.state_machine.transition_to(GameStateType.MENU)

    def is_active(self) -> bool:
        """Return whether the game-over state is currently active."""
        return self.state_machine.is_in_state(GameStateType.GAME_OVER)
