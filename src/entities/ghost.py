"""Ghost entity types used by the Pac-Man game."""

from dataclasses import dataclass
from enum import Enum

from src.entities.direction import Direction
from src.maze.maze import Coordinate


class GhostState(Enum):
    """Represent the current behavioral state of a ghost."""

    CHASE = "chase"
    FLEE = "flee"
    RETURN_HOME = "return_home"


class GhostType(Enum):
    """Represent the identity of a Pac-Man ghost."""

    RED = "red"
    PINK = "pink"
    BLUE = "blue"
    ORANGE = "orange"


@dataclass
class Ghost:
    """Represent the state of a single ghost."""

    ghost_type: GhostType
    position: Coordinate
    home_position: Coordinate
    direction: Direction = Direction.NONE
    state: GhostState = GhostState.CHASE
    speed: float = 1.0
