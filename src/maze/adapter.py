"""Adapter between the external A-Maze-ing package and the game domain."""

import io
import sys

from mazegenerator import MazeGenerator

from src.maze.maze import Coordinate, Maze, MazeGrid, MazeCell, Wall
from src.utils.error_logger import ErrorLogger


class MazeGenerationError(Exception):
    """Raised when the external maze generator cannot create a valid maze."""


class MazeAdapter:
    """Convert A-Maze-ing output into project-owned domain models."""

    FT_SMALL_PATTERN = (
        (1, 0, 0, 0, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 0, 1, 1, 1),
        (0, 0, 1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1, 1, 1),
    )

    @classmethod
    def _is_42_solid_cell(
        cls,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> bool:
        """Check if (x, y) overlaps with the generator's '42' logo."""
        pattern_h = len(cls.FT_SMALL_PATTERN)
        pattern_w = len(cls.FT_SMALL_PATTERN[0])
        if pattern_h * 2 > height or pattern_w * 2 > width:
            return False

        pos_y = int((height - pattern_h) / 2)
        pos_x = int((width - pattern_w) / 2)
        rel_x = x - pos_x
        rel_y = y - pos_y

        if 0 <= rel_y < pattern_h and 0 <= rel_x < pattern_w:
            return cls.FT_SMALL_PATTERN[rel_y][rel_x] == 1
        return False

    @classmethod
    def _find_safe_entry(
        cls,
        width: int,
        height: int,
        preferred_entry: Coordinate,
    ) -> Coordinate:
        """Find the closest corridor cell to preferred entry avoiding '42'."""
        px, py = preferred_entry
        if not cls._is_42_solid_cell(px, py, width, height):
            return preferred_entry

        best_cell = preferred_entry
        min_dist = float("inf")
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if not cls._is_42_solid_cell(x, y, width, height):
                    dist = abs(x - px) + abs(y - py)
                    if dist < min_dist:
                        min_dist = dist
                        best_cell = (x, y)
        return best_cell

    def generate_level(
        self,
        width: int,
        height: int,
        seed: int,
        entry_cell: Coordinate | None = None,
        exit_cell: Coordinate | None = None,
    ) -> Maze:
        """Generate a maze and convert it into a project domain model.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            seed: Seed used by the external generator.
            entry_cell: Starting cell coordinates.
            exit_cell: Exit cell coordinates. If omitted, the generator
                chooses the appropriate exit.

        Returns:
            A project-owned immutable Maze.

        Raises:
            MazeGenerationError: If maze generation or conversion fails.
            ValueError: If the requested dimensions or coordinates are invalid.
        """
        self._validate_dimensions(width, height)
        preferred_entry = (
            entry_cell
            if entry_cell is not None
            else (width // 2, height // 2)
        )
        self._validate_coordinate(
            preferred_entry,
            width,
            height,
            "entry",
        )

        actual_entry = self._find_safe_entry(width, height, preferred_entry)

        if exit_cell is not None:
            self._validate_coordinate(
                exit_cell,
                width,
                height,
                "exit",
            )

        try:
            generator = self._create_generator(
                width=width,
                height=height,
                seed=seed,
                entry_cell=actual_entry,
                exit_cell=exit_cell,
            )

            raw_grid = generator.maze

            cells = self._parse_bitmask_grid(
                raw_grid=raw_grid,
                width=width,
                height=height,
            )

            shortest_path = (
                generator.shortest_path
                if isinstance(generator.shortest_path, str)
                else ""
            )

            return Maze(
                width=width,
                height=height,
                cells=cells,
                entry=generator.maze_entry,
                exit=generator.maze_exit,
                shortest_path=shortest_path,
            )

        except MazeGenerationError:
            raise
        except Exception as exc:
            raise MazeGenerationError(
                f"Failed to generate maze with seed {seed}"
            ) from exc

    @staticmethod
    def _create_generator(
        width: int,
        height: int,
        seed: int,
        entry_cell: Coordinate,
        exit_cell: Coordinate | None,
    ) -> MazeGenerator:
        """Create the external maze generator with project settings."""
        kwargs: dict[str, object] = {
            "size": (width, height),
            "perfect": False,
            "entry_cell": entry_cell,
            "seed": seed,
        }

        if exit_cell is not None:
            kwargs["exit_cell"] = exit_cell

        old_stdout = sys.stdout
        buf = io.StringIO()
        try:
            sys.stdout = buf
            generator = MazeGenerator(**kwargs)
        finally:
            sys.stdout = old_stdout

        warning_text = buf.getvalue().strip()
        if warning_text:
            ErrorLogger.log(warning_text)

        return generator

    @staticmethod
    def _parse_bitmask_grid(
        raw_grid: list[list[int]],
        width: int,
        height: int,
    ) -> MazeGrid:
        """Convert external bitmasks into immutable domain cells."""
        if len(raw_grid) != height:
            raise MazeGenerationError(
                "Generated maze height does not match requested height."
            )

        rows: list[tuple[MazeCell, ...]] = []

        for y, raw_row in enumerate(raw_grid):
            if len(raw_row) != width:
                raise MazeGenerationError(
                    "Generated maze width does not match requested width."
                )

            row: list[MazeCell] = []

            for x, value in enumerate(raw_row):
                try:
                    walls = Wall(value)
                except ValueError as exc:
                    raise MazeGenerationError(
                        f"Invalid wall bitmask {value} at ({x}, {y})."
                    ) from exc

                row.append(
                    MazeCell(
                        position=(x, y),
                        walls=walls,
                        is_solid_block=walls == Wall.ALL,
                    )
                )

            rows.append(tuple(row))

        return tuple(rows)

    @staticmethod
    def _validate_dimensions(width: int, height: int) -> None:
        """Validate maze dimensions."""
        if width <= 0 or height <= 0:
            raise ValueError(
                "Maze width and height must both be greater than zero."
            )

    @staticmethod
    def _validate_coordinate(
        coordinate: Coordinate,
        width: int,
        height: int,
        name: str,
    ) -> None:
        """Validate that a coordinate belongs to the requested maze."""
        x, y = coordinate

        if not 0 <= x < width or not 0 <= y < height:
            raise ValueError(
                f"{name.capitalize()} coordinate ({x}, {y}) "
                f"is outside the maze bounds."
            )
