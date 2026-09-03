"""Movement system for Pac-Man entities."""

from src.entities.direction import Direction
from src.entities.entity import Entity
from src.maze.maze import Coordinate, Maze


class MovementSystem:
    """Handle movement calculations for game entities."""

    @staticmethod
    def calculate_next_position(
        entity: Entity,
        maze: Maze,
    ) -> Coordinate:
        """Calculate the next grid position for an entity.

        The movement system only calculates movement. Collision rules and
        movement restrictions are handled by the appropriate collision system.
        """
        current_x, current_y = entity.position

        movement_offsets: dict[Direction, Coordinate] = {
            Direction.NONE: (0, 0),
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
        }

        offset_x, offset_y = movement_offsets[entity.direction]

        next_x = current_x + offset_x
        next_y = current_y + offset_y

        if not maze.is_inside(next_x, next_y):
            return entity.position

        return (next_x, next_y)

    @staticmethod
    def move_entity(entity: Entity, maze: Maze) -> None:
        """Move an entity to its next valid position."""
        entity.position = MovementSystem.calculate_next_position(
            entity,
            maze,
        )
