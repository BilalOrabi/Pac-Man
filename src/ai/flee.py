"""Flee behavior for Pac-Man ghosts."""

from collections import deque

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
    def _compute_distance_map(
        maze: Maze,
        target_position: Coordinate,
    ) -> dict[Coordinate, int]:
        """Compute shortest path corridor distances from target to cells."""
        distance_map: dict[Coordinate, int] = {target_position: 0}
        queue: deque[Coordinate] = deque([target_position])
        while queue:
            curr = queue.popleft()
            curr_dist = distance_map[curr]
            for _, (dx, dy) in FleeBehavior.POSSIBLE_DIRECTIONS:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in distance_map and maze.is_inside(*nxt):
                    if maze.is_walkable(nxt, from_position=curr):
                        distance_map[nxt] = curr_dist + 1
                        queue.append(nxt)
        return distance_map

    @staticmethod
    def get_direction_away_from_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
        current_direction: Direction = Direction.NONE,
    ) -> Direction:
        """Return the walkable direction farthest from the target."""
        if not maze.is_inside(*ghost_position):
            raise ValueError(
                "Ghost position must be inside the maze."
            )

        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        forbidden = opposites.get(current_direction, Direction.NONE)

        distance_map = FleeBehavior._compute_distance_map(
            maze, target_position
        )
        if ghost_position in distance_map:
            current_dist = float(distance_map[ghost_position])
        else:
            current_dist = float(
                abs(ghost_position[0] - target_position[0])
                + abs(ghost_position[1] - target_position[1])
            )

        candidates: list[tuple[Direction, float]] = []
        for direction, (horizontal_change, vertical_change) in (
            FleeBehavior.POSSIBLE_DIRECTIONS
        ):
            candidate_position = (
                ghost_position[0] + horizontal_change,
                ghost_position[1] + vertical_change,
            )

            if not maze.is_walkable(
                candidate_position,
                from_position=ghost_position,
            ):
                continue

            if candidate_position in distance_map:
                dist = float(distance_map[candidate_position])
            else:
                dist = float(
                    abs(candidate_position[0] - target_position[0])
                    + abs(candidate_position[1] - target_position[1])
                )
            candidates.append((direction, dist))

        if not candidates:
            return Direction.NONE

        fleeing_non_forbidden: list[tuple[Direction, float]] = []
        approaching_non_forbidden: list[tuple[Direction, float]] = []
        reverse_candidate: tuple[Direction, float] | None = None

        for direction, dist in candidates:
            if forbidden is not Direction.NONE and direction == forbidden:
                reverse_candidate = (direction, dist)
                continue
            if dist >= current_dist:
                fleeing_non_forbidden.append((direction, dist))
            else:
                approaching_non_forbidden.append((direction, dist))

        # Priority 1: Move away or maintain distance without reversing
        if fleeing_non_forbidden:
            best_dir = Direction.NONE
            greatest_distance = float("-inf")
            for d, dist in fleeing_non_forbidden:
                if dist > greatest_distance:
                    greatest_distance = dist
                    best_dir = d
            return best_dir

        # Priority 2: If no forward/side path moves away, reverse to flee
        if (
            reverse_candidate is not None
            and reverse_candidate[1] > current_dist
        ):
            return reverse_candidate[0]

        # Priority 3: If cornered, take the best non-forbidden option
        if approaching_non_forbidden:
            best_dir = Direction.NONE
            greatest_distance = float("-inf")
            for d, dist in approaching_non_forbidden:
                if dist > greatest_distance:
                    greatest_distance = dist
                    best_dir = d
            return best_dir

        # Fallback: reverse if it was the only walkable direction
        if reverse_candidate is not None:
            return reverse_candidate[0]

        return Direction.NONE
