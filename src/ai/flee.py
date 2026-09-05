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
    def _get_opposite_direction(direction: Direction) -> Direction:
        """Return the opposite direction for a given movement direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposites.get(direction, Direction.NONE)

    @staticmethod
    def _collect_candidates(
        maze: Maze,
        ghost_pos: Coordinate,
        target_pos: Coordinate,
        distance_map: dict[Coordinate, int],
    ) -> list[tuple[Direction, float]]:
        """Collect all walkable neighbor directions and target distances."""
        candidates: list[tuple[Direction, float]] = []
        for direction, (dx, dy) in FleeBehavior.POSSIBLE_DIRECTIONS:
            cand = (ghost_pos[0] + dx, ghost_pos[1] + dy)
            if not maze.is_walkable(cand, from_position=ghost_pos):
                continue

            if cand in distance_map:
                dist = float(distance_map[cand])
            else:
                dist = float(
                    abs(cand[0] - target_pos[0]) + abs(cand[1] - target_pos[1])
                )
            candidates.append((direction, dist))
        return candidates

    @staticmethod
    def _select_best_flee_direction(
        candidates: list[tuple[Direction, float]],
        forbidden: Direction,
        current_dist: float,
    ) -> Direction:
        """Choose safest direction preferring moves that maintain distance."""
        fleeing: list[tuple[Direction, float]] = []
        approaching: list[tuple[Direction, float]] = []
        reverse_candidate: tuple[Direction, float] | None = None

        for direction, dist in candidates:
            if forbidden is not Direction.NONE and direction == forbidden:
                reverse_candidate = (direction, dist)
                continue
            if dist >= current_dist:
                fleeing.append((direction, dist))
            else:
                approaching.append((direction, dist))

        # Priority 1: Move away or maintain distance without reversing
        if fleeing:
            return max(fleeing, key=lambda item: item[1])[0]

        # Priority 2: Reverse if it leads away from danger
        if (
            reverse_candidate is not None
            and reverse_candidate[1] > current_dist
        ):
            return reverse_candidate[0]

        # Priority 3: If cornered, take farthest non-forbidden option
        if approaching:
            return max(approaching, key=lambda item: item[1])[0]

        # Fallback: reverse if only walkable option
        if reverse_candidate is not None:
            return reverse_candidate[0]

        return Direction.NONE

    @staticmethod
    def get_direction_away_from_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
        current_direction: Direction = Direction.NONE,
    ) -> Direction:
        """Return the walkable direction farthest from the target."""
        if not maze.is_inside(*ghost_position):
            raise ValueError("Ghost position must be inside the maze.")

        forbidden = FleeBehavior._get_opposite_direction(current_direction)
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

        candidates = FleeBehavior._collect_candidates(
            maze, ghost_position, target_position, distance_map
        )
        if not candidates:
            return Direction.NONE

        return FleeBehavior._select_best_flee_direction(
            candidates, forbidden, current_dist
        )
