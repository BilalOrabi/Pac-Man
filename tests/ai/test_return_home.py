"""Tests for Pac-Man ghost return-home behavior."""

from src.ai.return_home import ReturnHomeBehavior
from src.entities.direction import Direction
from src.maze.maze import Maze, MazeCell, Wall


def create_open_maze(
    width: int = 5,
    height: int = 5,
) -> Maze:
    """Create a small maze with walkable cells."""
    cells = tuple(
        tuple(
            MazeCell(
                position=(x, y),
                walls=Wall.NONE,
                is_solid_block=False,
            )
            for x in range(width)
        )
        for y in range(height)
    )

    return Maze(
        width=width,
        height=height,
        cells=cells,
        entry=(0, 0),
        exit=(width - 1, height - 1),
        shortest_path="",
    )


def test_return_home_moves_right_toward_home() -> None:
    """Return-home should choose RIGHT when home is to the right."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(1, 2),
        home_position=(4, 2),
    )

    assert direction is Direction.RIGHT


def test_return_home_moves_left_toward_home() -> None:
    """Return-home should choose LEFT when home is to the left."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(4, 2),
        home_position=(1, 2),
    )

    assert direction is Direction.LEFT


def test_return_home_moves_up_toward_home() -> None:
    """Return-home should choose UP when home is above."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(2, 4),
        home_position=(2, 1),
    )

    assert direction is Direction.UP


def test_return_home_moves_down_toward_home() -> None:
    """Return-home should choose DOWN when home is below."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(2, 1),
        home_position=(2, 4),
    )

    assert direction is Direction.DOWN


def test_return_home_avoids_solid_cells() -> None:
    """Return-home should not move into a solid cell."""
    cells = []

    for y in range(3):
        row = []

        for x in range(3):
            is_solid_block = (x, y) == (1, 0)

            row.append(
                MazeCell(
                    position=(x, y),
                    walls=Wall.ALL if is_solid_block else Wall.NONE,
                    is_solid_block=is_solid_block,
                )
            )

        cells.append(tuple(row))

    maze = Maze(
        width=3,
        height=3,
        cells=tuple(cells),
        entry=(0, 0),
        exit=(2, 2),
        shortest_path="",
    )

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(1, 1),
        home_position=(1, 0),
    )

    assert direction is Direction.LEFT


def test_return_home_returns_none_when_blocked() -> None:
    """Return-home should return NONE when no movement is possible."""
    cells = []

    for y in range(3):
        row = []

        for x in range(3):
            is_center_cell = (x, y) == (1, 1)

            row.append(
                MazeCell(
                    position=(x, y),
                    walls=Wall.ALL,
                    is_solid_block=not is_center_cell,
                )
            )

        cells.append(tuple(row))

    maze = Maze(
        width=3,
        height=3,
        cells=tuple(cells),
        entry=(1, 1),
        exit=(1, 1),
        shortest_path="",
    )

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(1, 1),
        home_position=(0, 0),
    )

    assert direction is Direction.NONE


def test_return_home_rejects_invalid_ghost_position() -> None:
    """Return-home should reject a ghost outside the maze."""
    maze = create_open_maze()

    try:
        ReturnHomeBehavior.get_direction_toward_home(
            maze=maze,
            ghost_position=(10, 10),
            home_position=(1, 1),
        )
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for an invalid ghost position."
    )


def test_return_home_rejects_invalid_home_position() -> None:
    """Return-home should reject a home position outside the maze."""
    maze = create_open_maze()

    try:
        ReturnHomeBehavior.get_direction_toward_home(
            maze=maze,
            ghost_position=(1, 1),
            home_position=(10, 10),
        )
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for an invalid home position."
    )
