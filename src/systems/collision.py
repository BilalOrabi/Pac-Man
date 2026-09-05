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

        if entity.position == target_position:
            return False

        if maze.is_inside(*entity.position):
            return maze.can_move(entity.position, target_position)

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

    @staticmethod
    def _check_visual_collision(entity_a: Entity, entity_b: Entity) -> bool:
        """Check collision based on sub-tile interpolated positions."""
        pos_fn_a = getattr(entity_a, "get_visual_position", None)
        pos_fn_b = getattr(entity_b, "get_visual_position", None)
        if callable(pos_fn_a) and callable(pos_fn_b):
            va = pos_fn_a()
            vb = pos_fn_b()
            if (round(va[0]), round(va[1])) == (round(vb[0]), round(vb[1])):
                return True
            dx = va[0] - vb[0]
            dy = va[1] - vb[1]
            return bool((dx * dx + dy * dy) < 0.36)
        return False

    @staticmethod
    def check_entity_collision(
        entity_a: Entity,
        entity_b: Entity,
    ) -> bool:
        """Return whether two entities collide."""
        if entity_a.position == entity_b.position:
            return True

        return CollisionSystem._check_visual_collision(entity_a, entity_b)
