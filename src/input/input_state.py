"""Runtime state for user input in the Pac-Man game."""

from dataclasses import dataclass

from src.entities.direction import Direction


@dataclass
class InputState:
    """Store the current movement input state."""

    requested_direction: Direction = Direction.NONE

    def set_direction(self, direction: Direction) -> None:
        """Set the direction currently requested by the player."""
        self.requested_direction = direction

    def clear_direction(self) -> None:
        """Clear the current movement request."""
        self.requested_direction = Direction.NONE

    def has_requested_direction(self) -> bool:
        """Return whether a movement direction has been requested."""
        return self.requested_direction is not Direction.NONE
