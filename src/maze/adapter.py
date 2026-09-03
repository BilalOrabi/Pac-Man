"""Adapter between the external A-Maze-ing package and the game domain."""

from mazegenerator import MazeGenerator

from src.maze.maze import Coordinate, Maze, MazeGrid, MazeCell, Wall


class MazeGenerationError(Exception):
    """Raised when the external maze generator cannot create a valid maze."""


class MazeAdapter:
    """Convert A-Maze-ing output into project-owned domain models."""

    def generate_level(
        self,
        width: int,
        height: int,
        seed: int,
        entry_cell: Coordinate = (0, 0),
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
        self._validate_coordinate(
            entry_cell,
            width,
            height,
            "entry",
        )

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
                entry_cell=entry_cell,
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

        return MazeGenerator(**kwargs)

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
