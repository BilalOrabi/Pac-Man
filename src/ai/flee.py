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
            (Direction.LEFT, (-1, 0)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, 1)),
            (Direction.UP, (0, -1)),
        )

        preferred_direction = Direction.NONE

        if target_position[0] < ghost_position[0]:
            preferred_direction = Direction.RIGHT
        elif target_position[0] > ghost_position[0]:
            preferred_direction = Direction.LEFT
        elif target_position[1] < ghost_position[1]:
            preferred_direction = Direction.DOWN
        elif target_position[1] > ghost_position[1]:
            preferred_direction = Direction.UP

        best_direction = Direction.NONE
        greatest_distance = float("-inf")
        preferred_distance = False

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

            is_preferred = direction is preferred_direction

            if distance > greatest_distance or (
                distance == greatest_distance
                and is_preferred
                and not preferred_distance
            ):
                greatest_distance = distance
                best_direction = direction
                preferred_distance = is_preferred

        return best_direction
