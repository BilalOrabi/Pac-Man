"""Return-home behavior for Pac-Man ghosts."""

from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


class ReturnHomeBehavior:
    """Calculate movement directions that move a ghost toward home."""

    POSSIBLE_DIRECTIONS = (
        (Direction.RIGHT, (1, 0)),
        (Direction.LEFT, (-1, 0)),
        (Direction.DOWN, (0, 1)),
        (Direction.UP, (0, -1)),
    )

    @staticmethod
    def get_direction_toward_home(
        maze: Maze,
        ghost_position: Coordinate,
        home_position: Coordinate,
    ) -> Direction:
        """Return the walkable direction closest to the ghost's home."""
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        best_direction = Direction.NONE
        shortest_distance = float("inf")

        for direction, (horizontal_change, vertical_change) in (
            ReturnHomeBehavior.POSSIBLE_DIRECTIONS
        ):
            candidate_position = (
                ghost_position[0] + horizontal_change,
                ghost_position[1] + vertical_change,
            )

            if not maze.is_walkable(candidate_position):
                continue

            distance_to_home = (
                abs(candidate_position[0] - home_position[0])
                + abs(candidate_position[1] - home_position[1])
            )

            if distance_to_home < shortest_distance:
                shortest_distance = distance_to_home
                best_direction = direction

        return best_direction
