"""Ghost behavior modes used by the Pac-Man AI."""

from enum import Enum


class GhostMode(Enum):
    """Represent the possible behavioral modes of a ghost."""

    CHASE = "chase"
    FLEE = "flee"
    RETURN_HOME = "return_home"
