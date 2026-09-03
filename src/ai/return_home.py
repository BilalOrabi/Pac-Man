"""Return-home behavior for Pac-Man ghosts."""

from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


class ReturnHomeBehavior:
    """Calculate movement directions that move a ghost toward home."""

    @staticmethod
    def get_direction_toward_home(
        maze: Maze,
        ghost_position: Coordinate,
        home_position: Coordinate,
    ) -> Direction:
        """Return a direction that moves the ghost toward its home.

        Args:
            maze: Maze used to determine whether movement is possible.
            ghost_position: Current ghost position.
            home_position: Ghost's home position.

        Returns:
            The best available movement direction toward home.

        Raises:
            ValueError: If the ghost position is outside the maze.
        """
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        if not maze.is_inside(*home_position):
            raise ValueError(
                "Home position must be inside the maze."
            )

        possible_directions = (
            (Direction.LEFT, (-1, 0)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, 1)),
            (Direction.UP, (0, -1)),
        )

        preferred_direction = Direction.NONE

        if home_position[0] < ghost_position[0]:

            preferred_direction = Direction.LEFT
        elif home_position[0] > ghost_position[0]:
            preferred_direction = Direction.RIGHT
        elif home_position[1] < ghost_position[1]:
            preferred_direction = Direction.UP
        elif home_position[1] > ghost_position[1]:
            preferred_direction = Direction.DOWN

        best_direction = Direction.NONE
        shortest_distance = float("inf")
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
                abs(candidate_position[0] - home_position[0])
                + abs(candidate_position[1] - home_position[1])
            )

            is_preferred = direction is preferred_direction

            if distance < shortest_distance or (
                distance == shortest_distance
                and is_preferred
                and not preferred_distance
            ):
                shortest_distance = distance
                best_direction = direction
                preferred_distance = is_preferred

        return best_direction
