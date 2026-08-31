"""Adapter module converting external MazeGenerator
bitmasks into game domain data structures."""

from dataclasses import dataclass
from mazegenerator import MazeGenerator


@dataclass(frozen=True)
class MazeCell:
    """Domain representation of a single grid cell."""

    x: int
    y: int
    wall_north: bool
    wall_east: bool
    wall_south: bool
    wall_west: bool
    is_solid_block: bool


@dataclass(frozen=True)
class MazeResult:
    """Decoupled container for generated level layouts."""

    width: int
    height: int
    cells: list[list[MazeCell]]
    raw_bitmask_grid: list[list[int]]
    entry: tuple[int, int]
    exit: tuple[int, int]
    shortest_path: str


class MazeAdapter:
    """Adapts third-party MazeGenerator bitmask output
    for internal game engine consumption."""

    NORTH_BIT = 1
    EAST_BIT = 2
    SOUTH_BIT = 4
    WEST_BIT = 8

    def generate_level(
        self,
        width: int,
        height: int,
        seed: int,
        entry_cell: tuple[int, int] = (0, 0),
        exit_cell: tuple[int, int] = (-1, -1),
    ) -> MazeResult | None:
        """Generate a level using the external package
        and return domain models.

        Args:
            width: Grid width in cells.
            height: Grid height in cells.
            seed: Seed for random generation.
            entry_cell: (x, y) starting coordinates.
            exit_cell: (x, y) exit coordinates.

        Returns:
            MazeResult domain model, or None if generation failed.
        """
        try:
            # Force perfect=False
            generator = MazeGenerator(
                size=(width, height),
                perfect=False,
                entry_cell=entry_cell,
                exit_cell=exit_cell,
                seed=seed,
            )

            raw_grid = generator.maze
            path_str = (
                str(generator.shortest_path)
                if isinstance(generator.shortest_path, str)
                else ""
            )

            parsed_cells = self._parse_bitmask_grid(raw_grid, width, height)

            return MazeResult(
                width=width,
                height=height,
                cells=parsed_cells,
                raw_bitmask_grid=raw_grid,
                entry=generator.maze_entry,
                exit=generator.maze_exit,
                shortest_path=path_str,
            )
        except Exception as err:
            print(f"Maze generation error [Seed {seed}]: {err}")
            return None

    def _parse_bitmask_grid(
        self, raw_grid: list[list[int]], width: int, height: int
    ) -> list[list[MazeCell]]:
        """Translate bitmask integers into strongly-typed MazeCell objects."""
        grid: list[list[MazeCell]] = []
        for y in range(height):
            row: list[MazeCell] = []
            for x in range(width):
                val = raw_grid[y][x]
                cell = MazeCell(
                    x=x,
                    y=y,
                    wall_north=bool(val & self.NORTH_BIT),
                    wall_east=bool(val & self.EAST_BIT),
                    wall_south=bool(val & self.SOUTH_BIT),
                    wall_west=bool(val & self.WEST_BIT),
                    is_solid_block=(val == 15),
                )
                row.append(cell)
            grid.append(row)
        grid
        return grid
