"""State machine responsible for managing the current Pac-Man game state."""

from dataclasses import dataclass

from src.states.game_state import GameStateType


@dataclass
class GameStateMachine:
    """Manage transitions between Pac-Man game states."""

    current_state: GameStateType = GameStateType.MENU

    @staticmethod
    def _validate_state(state: object, param_name: str) -> None:
        """Validate that argument is a valid GameStateType instance."""
        if not isinstance(state, GameStateType):
            raise TypeError(f"{param_name} must be a GameStateType.")

    def transition_to(self, next_state: GameStateType) -> None:
        """Change the current game state."""
        self._validate_state(next_state, "next_state")
        self.current_state = next_state

    def is_in_state(self, game_state: GameStateType) -> bool:
        """Return whether the game is currently in the given state."""
        self._validate_state(game_state, "game_state")
        return self.current_state is game_state
