"""Direction types used by Pac-Man entities."""

from enum import Enum


class Direction(Enum):
    """Represent the possible movement directions."""

    NONE = "none"
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

    def opposite(self) -> "Direction":
        """Return the opposite movement direction."""
        opposite_directions = {
            Direction.NONE: Direction.NONE,
            Direction.UP: Direction.DOWN,
            Direction.RIGHT: Direction.LEFT,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
        }

        return opposite_directions[self]
