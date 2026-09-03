"""Base domain entity for Pac-Man game objects."""

from dataclasses import dataclass

from src.maze import Coordinate
from src.entities.direction import Direction


@dataclass
class Entity:
    """Represent the common state shared by movable game entities."""

    position: Coordinate
    direction: Direction = Direction.NONE
    speed: float = 0.0

    def set_direction(self, direction: Direction) -> None:
        """Set the entity's current movement direction."""
        self.direction = direction

    def stop(self) -> None:
        """Stop the entity from moving."""
        self.direction = Direction.NONE
