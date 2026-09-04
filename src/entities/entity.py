"""Base domain entity for Pac-Man game objects."""

from dataclasses import dataclass

from src.entities.direction import Direction
from src.maze import Coordinate


@dataclass(kw_only=True)
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
