"""Flee behavior for Pac-Man ghosts."""

from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


class FleeBehavior:
    """Calculate movement directions that move a ghost away from a target."""

    @staticmethod
    def get_direction_away_from_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
    ) -> Direction:
        """Return a direction that increases distance from the target.

        Args:
            maze: Maze used to determine whether movement is possible.
            ghost_position: Current ghost position.
            target_position: Position the ghost wants to avoid.

        Returns:
            The best available movement direction away from the target.

        Raises:
            ValueError: If the ghost position is outside the maze.
        """
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        possible_directions = (
            (Direction.UP, (0, -1)),
            (Direction.DOWN, (0, 1)),
            (Direction.LEFT, (-1, 0)),
            (Direction.RIGHT, (1, 0)),
        )

        best_direction = Direction.NONE
        greatest_distance = float("-inf")

        for direction, (horizontal_change, vertical_change) in (
            possible_directions
        ):
            candidate_position = (
                ghost_position[0] + horizontal_change,
                ghost_position[1] + vertical_change,
            )

            if not maze.is_walkable(candidate_position):
                continue

            distance = (
                abs(candidate_position[0] - target_position[0])
                + abs(candidate_position[1] - target_position[1])
            )

            if distance > greatest_distance:
                greatest_distance = distance
                best_direction = direction

        return best_direction
