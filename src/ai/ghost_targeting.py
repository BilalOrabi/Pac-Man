"""Targeting logic for individual ghost personalities in chase mode."""

from typing import Sequence

from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.entities.player import Player
from src.maze.maze import Coordinate, Maze


class GhostTargeting:
    """Compute chase targets for ghosts based on their personality."""

    @staticmethod
    def _clamp(coord: Coordinate, maze: Maze | None) -> Coordinate:
        """Clamp coordinates within maze bounds if maze is available."""
        if (
            maze is None
            or not isinstance(getattr(maze, "width", None), int)
            or not isinstance(getattr(maze, "height", None), int)
        ):
            return coord
        x = max(0, min(maze.width - 1, coord[0]))
        y = max(0, min(maze.height - 1, coord[1]))
        return (x, y)

    @staticmethod
    def _get_direction_offset(direction: Direction) -> tuple[int, int]:
        """Return horizontal and vertical deltas for player direction."""
        dir_offsets = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.NONE: (0, 0),
        }
        return dir_offsets.get(direction, (0, 0))

    @staticmethod
    def _target_pink(px: int, py: int, dx: int, dy: int) -> Coordinate:
        """Target 4 tiles ahead in the direction Pac-Man is facing."""
        return (px + 4 * dx, py + 4 * dy)

    @staticmethod
    def _target_blue(
        px: int,
        py: int,
        dx: int,
        dy: int,
        ghost: Ghost,
        ghosts: Sequence[Ghost] | None,
    ) -> Coordinate:
        """Target double the vector from Blinky to pivot 2 tiles ahead."""
        pivot_x = px + 2 * dx
        pivot_y = py + 2 * dy

        blinky_pos: Coordinate | None = None
        if ghosts:
            for g in ghosts:
                if (
                    getattr(g, "ghost_type", None) is GhostType.RED
                    and g is not ghost
                ):
                    blinky_pos = g.position
                    break

        if blinky_pos is not None:
            bx, by = blinky_pos
            return (2 * pivot_x - bx, 2 * pivot_y - by)
        return (pivot_x, pivot_y)

    @staticmethod
    def _target_orange(ghost: Ghost, px: int, py: int) -> Coordinate:
        """Target Pac-Man when far, retreat to home when within 8 tiles."""
        gx, gy = ghost.position
        dist = abs(gx - px) + abs(gy - py)
        if dist > 8:
            return (px, py)
        return ghost.home_position

    @classmethod
    def get_chase_target(
        cls,
        ghost: Ghost,
        player: Player,
        ghosts: Sequence[Ghost] | None = None,
        maze: Maze | None = None,
    ) -> Coordinate:
        """Compute the chase target tile for a given ghost."""
        px, py = player.position
        p_dir = getattr(player, "direction", Direction.NONE)
        dx, dy = cls._get_direction_offset(p_dir)
        gtype = getattr(ghost, "ghost_type", GhostType.RED)

        if gtype is GhostType.RED:
            target = (px, py)
        elif gtype is GhostType.PINK:
            target = cls._target_pink(px, py, dx, dy)
        elif gtype is GhostType.BLUE:
            target = cls._target_blue(px, py, dx, dy, ghost, ghosts)
        elif gtype is GhostType.ORANGE:
            target = cls._target_orange(ghost, px, py)
        else:
            target = (px, py)

        return cls._clamp(target, maze)
