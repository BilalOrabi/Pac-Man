"""Ghost entity types used by the Pac-Man game."""

from dataclasses import dataclass
from enum import Enum

from src.entities.entity import Entity
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
class Ghost(Entity):
    """Represent the state of a single ghost."""

    ghost_type: GhostType
    home_position: Coordinate
    state: GhostState = GhostState.CHASE
    respawn_cooldown: float = 0.0
