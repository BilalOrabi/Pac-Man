"""Return-home behavior for Pac-Man ghosts."""

from collections import deque

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
    def _bfs_search_home(
        maze: Maze,
        ghost_position: Coordinate,
        home_position: Coordinate,
    ) -> Direction | None:
        """Find the initial step along shortest corridor path using BFS."""
        queue: deque[tuple[Coordinate, Direction]] = deque()
        visited: set[Coordinate] = {ghost_position}

        for direction, (dx, dy) in ReturnHomeBehavior.POSSIBLE_DIRECTIONS:
            cand = (ghost_position[0] + dx, ghost_position[1] + dy)
            if maze.is_walkable(cand, from_position=ghost_position):
                if cand == home_position:
                    return direction
                visited.add(cand)
                queue.append((cand, direction))

        while queue:
            curr, first_dir = queue.popleft()
            if curr == home_position:
                return first_dir

            for _, (dx, dy) in ReturnHomeBehavior.POSSIBLE_DIRECTIONS:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in visited and maze.is_walkable(
                    nxt, from_position=curr
                ):
                    if nxt == home_position:
                        return first_dir
                    visited.add(nxt)
                    queue.append((nxt, first_dir))

        return None

    @staticmethod
    def _greedy_fallback(
        maze: Maze,
        ghost_position: Coordinate,
        home_position: Coordinate,
    ) -> Direction:
        """Greedy Manhattan direction fallback if home is unreachable."""
        best_direction = Direction.NONE
        shortest_distance = float("inf")

        for direction, (dx, dy) in ReturnHomeBehavior.POSSIBLE_DIRECTIONS:
            cand = (ghost_position[0] + dx, ghost_position[1] + dy)
            if not maze.is_walkable(cand, from_position=ghost_position):
                continue

            dist = abs(cand[0] - home_position[0]) + abs(
                cand[1] - home_position[1]
            )
            if dist < shortest_distance:
                shortest_distance = dist
                best_direction = direction

        return best_direction

    @staticmethod
    def get_direction_toward_home(
        maze: Maze,
        ghost_position: Coordinate,
        home_position: Coordinate,
    ) -> Direction:
        """Return the walkable direction closest to the ghost's home."""
        if not maze.is_inside(*ghost_position):
            raise ValueError("Ghost position must be inside the maze.")

        if ghost_position == home_position:
            return Direction.NONE

        bfs_direction = ReturnHomeBehavior._bfs_search_home(
            maze, ghost_position, home_position
        )
        if bfs_direction is not None:
            return bfs_direction

        return ReturnHomeBehavior._greedy_fallback(
            maze, ghost_position, home_position
        )
