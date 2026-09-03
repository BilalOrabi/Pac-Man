"""Domain model for Pac-Man maze data."""

from dataclasses import dataclass
from enum import IntFlag
from typing import TypeAlias


Coordinate: TypeAlias = tuple[int, int]


class Wall(IntFlag):
    """Bit flags representing walls around a maze cell."""

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST


@dataclass(frozen=True)
class MazeCell:
    """Immutable representation of one maze cell."""

    position: Coordinate
    walls: Wall
    is_solid_block: bool

    def has_wall(self, wall: Wall) -> bool:
        """Return whether this cell contains the specified wall."""
        return bool(self.walls & wall)

    @property
    def x(self) -> int:
        """Return the horizontal coordinate of the cell."""
        return self.position[0]

    @property
    def y(self) -> int:
        """Return the vertical coordinate of the cell."""
        return self.position[1]


MazeGrid: TypeAlias = tuple[tuple[MazeCell, ...], ...]


@dataclass(frozen=True)
class Maze:
    """Immutable maze representation used by the game."""

    width: int
    height: int
    cells: MazeGrid
    entry: Coordinate
    exit: Coordinate
    shortest_path: str

    def get_cell(self, position: Coordinate) -> MazeCell:
        """Return the maze cell at the specified position."""
        x, y = position

        if not self.is_inside(x, y):
            raise IndexError(
                f"Cell position ({x}, {y}) is outside the maze."
            )

        return self.cells[y][x]

    def is_inside(self, x: int, y: int) -> bool:
        """Return whether the coordinates are inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, position: Coordinate) -> bool:
        """Return whether a position can be occupied by an entity."""
        if not self.is_inside(*position):
            return False

        return not self.get_cell(position).is_solid_block
