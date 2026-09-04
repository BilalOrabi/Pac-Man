"""Flee behavior for Pac-Man ghosts."""

from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


class FleeBehavior:
    """Calculate movement directions that move a ghost away from a target."""

    POSSIBLE_DIRECTIONS = (
        (Direction.RIGHT, (1, 0)),
        (Direction.LEFT, (-1, 0)),
        (Direction.DOWN, (0, 1)),
        (Direction.UP, (0, -1)),
    )

    @staticmethod
    def get_direction_away_from_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
    ) -> Direction:
        """Return the walkable direction farthest from the target."""
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        best_direction = Direction.NONE
        greatest_distance = float("-inf")

        for direction, (horizontal_change, vertical_change) in (
            FleeBehavior.POSSIBLE_DIRECTIONS
        ):
            candidate_position = (
                ghost_position[0] + horizontal_change,
                ghost_position[1] + vertical_change,
            )

            if not maze.is_walkable(candidate_position):
                continue

            distance_from_target = (
                abs(candidate_position[0] - target_position[0])
                + abs(candidate_position[1] - target_position[1])
            )

            if distance_from_target > greatest_distance:
                greatest_distance = distance_from_target
                best_direction = direction

        return best_direction
