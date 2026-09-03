"""State machine responsible for managing the current Pac-Man game state."""

from dataclasses import dataclass

from src.states.game_state import GameStateType


@dataclass
class GameStateMachine:
    """Manage transitions between Pac-Man game states."""

    current_state: GameStateType = GameStateType.MENU

    def transition_to(self, next_state: GameStateType) -> None:
        """Change the current game state."""
        if not isinstance(next_state, GameStateType):
            raise TypeError(
                "next_state must be a GameStateType."
            )

        self.current_state = next_state

    def is_in_state(self, game_state: GameStateType) -> bool:
        """Return whether the game is currently in the given state."""
        if not isinstance(game_state, GameStateType):
            raise TypeError(
                "game_state must be a GameStateType."
            )

        return self.current_state is game_state
