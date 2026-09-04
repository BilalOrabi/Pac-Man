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

    @classmethod
    def get_chase_target(
        cls,
        ghost: Ghost,
        player: Player,
        ghosts: Sequence[Ghost] | None = None,
        maze: Maze | None = None,
    ) -> Coordinate:
        """Compute the chase target tile for a given ghost.

        - RED (Blinky): Targets Pac-Man's current grid position directly.
        - PINK (Pinky): Ambush predictor targeting 4 tiles ahead of
          Pac-Man's orientation.
        - BLUE (Inky): Flanker using a pivot 2 tiles ahead of Pac-Man,
          reflected across Blinky's position.
        - ORANGE (Clyde): Chases Pac-Man when farther than 8 tiles away,
          retreating to home corner when within 8 tiles.
        """
        px, py = player.position
        p_dir = getattr(player, "direction", Direction.NONE)
        dir_offsets = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.NONE: (0, 0),
        }
        dx, dy = dir_offsets.get(p_dir, (0, 0))

        gtype = getattr(ghost, "ghost_type", GhostType.RED)

        if gtype is GhostType.RED:
            return cls._clamp((px, py), maze)

        if gtype is GhostType.PINK:
            target = (px + 4 * dx, py + 4 * dy)
            return cls._clamp(target, maze)

        if gtype is GhostType.BLUE:
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
                target_x = 2 * pivot_x - bx
                target_y = 2 * pivot_y - by
                return cls._clamp((target_x, target_y), maze)
            return cls._clamp((pivot_x, pivot_y), maze)

        if gtype is GhostType.ORANGE:
            gx, gy = ghost.position
            dist = abs(gx - px) + abs(gy - py)
            if dist > 8:
                return cls._clamp((px, py), maze)
            return cls._clamp(ghost.home_position, maze)

        return cls._clamp((px, py), maze)
