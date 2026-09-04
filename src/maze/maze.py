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

    def can_move(
        self,
        from_position: Coordinate,
        to_position: Coordinate,
    ) -> bool:
        """Return whether movement between adjacent cells is permitted."""
        if (
            not self.is_inside(*from_position)
            or not self.is_inside(*to_position)
        ):
            return False

        from_cell = self.get_cell(from_position)
        to_cell = self.get_cell(to_position)

        if from_cell.is_solid_block or to_cell.is_solid_block:
            return False

        delta_x = to_position[0] - from_position[0]
        delta_y = to_position[1] - from_position[1]

        if delta_x == 1 and delta_y == 0:
            east_blocked = from_cell.has_wall(Wall.EAST)
            west_blocked = to_cell.has_wall(Wall.WEST)
            return not (east_blocked or west_blocked)
        if delta_x == -1 and delta_y == 0:
            west_blocked = from_cell.has_wall(Wall.WEST)
            east_blocked = to_cell.has_wall(Wall.EAST)
            return not (west_blocked or east_blocked)
        if delta_x == 0 and delta_y == 1:
            south_blocked = from_cell.has_wall(Wall.SOUTH)
            north_blocked = to_cell.has_wall(Wall.NORTH)
            return not (south_blocked or north_blocked)
        if delta_x == 0 and delta_y == -1:
            north_blocked = from_cell.has_wall(Wall.NORTH)
            south_blocked = to_cell.has_wall(Wall.SOUTH)
            return not (north_blocked or south_blocked)

        return True

    def is_walkable(
        self,
        position: Coordinate,
        from_position: Coordinate | None = None,
    ) -> bool:
        """Return whether a position can be occupied by an entity."""
        if not self.is_inside(*position):
            return False

        if from_position is not None:
            return self.can_move(from_position, position)

        return not self.get_cell(position).is_solid_block
