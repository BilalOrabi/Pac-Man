"""Chase behavior for Pac-Man ghosts."""

from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


class ChaseBehavior:
    """Calculate movement directions that approach a target."""

    POSSIBLE_DIRECTIONS = (
        (Direction.RIGHT, (1, 0)),
        (Direction.LEFT, (-1, 0)),
        (Direction.DOWN, (0, 1)),
        (Direction.UP, (0, -1)),
    )

    @staticmethod
    def get_direction_toward_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
    ) -> Direction:
        """Return the walkable direction closest to the target.

        When multiple directions have the same distance to the target,
        directions are evaluated using the defined priority order.
        """
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        best_direction = Direction.NONE
        shortest_distance = float("inf")

        for direction, (horizontal_change, vertical_change) in (
            ChaseBehavior.POSSIBLE_DIRECTIONS
        ):
            candidate_position = (
                ghost_position[0] + horizontal_change,
                ghost_position[1] + vertical_change,
            )

            if not maze.is_walkable(candidate_position):
                continue

            distance_to_target = (
                abs(candidate_position[0] - target_position[0])
                + abs(candidate_position[1] - target_position[1])
            )

            if distance_to_target < shortest_distance:
                shortest_distance = distance_to_target
                best_direction = direction

        return best_direction
