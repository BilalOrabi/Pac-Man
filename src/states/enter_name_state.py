"""Enter-name state for the Pac-Man game."""

from dataclasses import dataclass

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


@dataclass
class EnterNameState:
    """Handle entering the player's name for the high-score table."""

    state_machine: GameStateMachine
    player_name: str = ""
    maximum_name_length: int = 10

    def add_character(self, character: str) -> None:
        """Add one character to the player's name."""
        if not isinstance(character, str):
            raise TypeError("character must be a string.")

        if len(character) != 1:
            raise ValueError(
                "character must contain exactly one character."
            )

        if len(self.player_name) >= self.maximum_name_length:
            return

        self.player_name += character

    def remove_character(self) -> None:
        """Remove the last character from the player's name."""
        self.player_name = self.player_name[:-1]

    def confirm_name(self) -> str:
        """Confirm and return the player's entered name."""
        return self.player_name

    def is_active(self) -> bool:
        """Return whether the enter-name state is currently active."""
        return self.state_machine.is_in_state(
            GameStateType.ENTER_NAME
        )

    def reset(self) -> None:
        """Clear the currently entered player name."""
        self.player_name = ""
