"""Collision detection and movement validation for the Pac-Man game."""

from src.entities.entity import Entity
from src.maze.maze import Coordinate, Maze


class CollisionSystem:
    """Handle collision checks between entities and the maze."""

    @staticmethod
    def can_move_to(
        entity: Entity,
        target_position: Coordinate,
        maze: Maze,
    ) -> bool:
        """Return whether an entity can occupy the target position."""
        if not maze.is_inside(*target_position):
            return False

        target_cell = maze.get_cell(target_position)

        return not target_cell.is_solid_block

    @staticmethod
    def move_if_valid(
        entity: Entity,
        target_position: Coordinate,
        maze: Maze,
    ) -> bool:
        """Move an entity if the target position is valid.

        Returns:
            True if the entity was moved, otherwise False.
        """
        if not CollisionSystem.can_move_to(
            entity,
            target_position,
            maze,
        ):
            return False

        entity.position = target_position
        return True
