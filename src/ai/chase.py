"""Chase behavior for Pac-Man ghosts."""

from collections import deque

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
    def _find_walkable_target(maze: Maze, target: Coordinate) -> Coordinate:
        """Find the nearest walkable coordinate in the maze to target."""
        if (
            maze.is_inside(*target)
            and not maze.get_cell(target).is_solid_block
        ):
            return target

        best_cell = target
        min_dist = float("inf")
        for y in range(maze.height):
            for x in range(maze.width):
                c = (x, y)
                if not maze.get_cell(c).is_solid_block:
                    d = abs(x - target[0]) + abs(y - target[1])
                    if d < min_dist:
                        min_dist = d
                        best_cell = c
        return best_cell

    @staticmethod
    def _compute_distance_map(
        maze: Maze,
        target_position: Coordinate,
    ) -> dict[Coordinate, int]:
        """Compute shortest path corridor distances from target to cells."""
        effective_target = ChaseBehavior._find_walkable_target(
            maze, target_position
        )
        distance_map: dict[Coordinate, int] = {effective_target: 0}
        queue: deque[Coordinate] = deque([effective_target])

        while queue:
            curr = queue.popleft()
            curr_dist = distance_map[curr]
            for _, (dx, dy) in ChaseBehavior.POSSIBLE_DIRECTIONS:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in distance_map and maze.is_inside(*nxt):
                    if maze.is_walkable(curr, from_position=nxt):
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
    def _evaluate_candidate_distance(
        candidate: Coordinate,
        target: Coordinate,
        distance_map: dict[Coordinate, int],
    ) -> float:
        """Calculate the distance from a candidate position to target."""
        if candidate in distance_map:
            return float(distance_map[candidate])
        manhattan = abs(candidate[0] - target[0]) + abs(
            candidate[1] - target[1]
        )
        return 1000.0 + float(manhattan)

    @staticmethod
    def get_direction_toward_target(
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
        current_direction: Direction = Direction.NONE,
    ) -> Direction:
        """Return the walkable direction closest to the target."""
        if not maze.is_inside(*ghost_position):
            raise ValueError("Ghost position must be inside the maze.")

        forbidden = ChaseBehavior._get_opposite_direction(current_direction)
        distance_map = ChaseBehavior._compute_distance_map(
            maze, target_position
        )

        best_direction = Direction.NONE
        shortest_distance = float("inf")
        reverse_fallback = Direction.NONE

        for direction, (dx, dy) in ChaseBehavior.POSSIBLE_DIRECTIONS:
            candidate = (ghost_position[0] + dx, ghost_position[1] + dy)
            if not maze.is_walkable(candidate, from_position=ghost_position):
                continue

            if forbidden is not Direction.NONE and direction == forbidden:
                reverse_fallback = direction
                continue

            dist = ChaseBehavior._evaluate_candidate_distance(
                candidate, target_position, distance_map
            )
            if dist < shortest_distance:
                shortest_distance = dist
                best_direction = direction

        if best_direction is not Direction.NONE:
            return best_direction

        return reverse_fallback
