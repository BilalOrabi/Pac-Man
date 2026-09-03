"""Playing state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class PlayingState:
    """Handle the active gameplay state."""

    state_machine: GameStateMachine

    def pause_game(self) -> None:
        """Pause the current game."""
        self.state_machine.transition_to(GameStateType.PAUSED)

    def end_game(self) -> None:
        """End the current game and enter the game-over state."""
        self.state_machine.transition_to(GameStateType.GAME_OVER)

    def complete_game(self) -> None:
        """Complete the game and enter the victory state."""
        self.state_machine.transition_to(GameStateType.VICTORY)

    def is_active(self) -> bool:
        """Return whether gameplay is currently active."""
        return self.state_machine.is_in_state(GameStateType.PLAYING)
