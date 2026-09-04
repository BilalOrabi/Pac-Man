"""Tests for Pac-Man ghost return-home behavior."""

import pytest

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


def create_maze_with_solid_cells(
    solid_positions: set[tuple[int, int]],
    width: int = 5,
    height: int = 5,
) -> Maze:
    """Create a maze with specific solid cells."""
    cells = tuple(
        tuple(
            MazeCell(
                position=(x, y),
                walls=(
                    Wall.ALL
                    if (x, y) in solid_positions
                    else Wall.NONE
                ),
                is_solid_block=(x, y) in solid_positions,
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
    """Return-home should move RIGHT when home is directly right."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(1, 2),
        home_position=(4, 2),
    )

    assert direction is Direction.RIGHT


def test_return_home_moves_left_toward_home() -> None:
    """Return-home should move LEFT when home is directly left."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(3, 2),
        home_position=(0, 2),
    )

    assert direction is Direction.LEFT


def test_return_home_moves_down_toward_home() -> None:
    """Return-home should move DOWN when home is below."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(2, 1),
        home_position=(2, 4),
    )

    assert direction is Direction.DOWN


def test_return_home_moves_up_toward_home() -> None:
    """Return-home should move UP when home is above."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(2, 3),
        home_position=(2, 0),
    )

    assert direction is Direction.UP


def test_return_home_avoids_solid_cell() -> None:
    """Return-home should avoid a solid cell blocking the direct route."""
    maze = create_maze_with_solid_cells(
        solid_positions={(1, 0)},
        width=3,
        height=3,
    )

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(1, 1),
        home_position=(1, 0),
    )

    assert direction is Direction.RIGHT


def test_return_home_returns_none_when_surrounded() -> None:
    """Return-home should return NONE when no direction is walkable."""
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


def test_return_home_rejects_position_outside_maze() -> None:
    """Return-home should reject a ghost position outside the maze."""
    maze = create_open_maze()

    with pytest.raises(ValueError):
        ReturnHomeBehavior.get_direction_toward_home(
            maze=maze,
            ghost_position=(10, 10),
            home_position=(1, 1),
        )


def test_return_home_uses_deterministic_tie_breaking() -> None:
    """Return-home should use the defined priority when distances tie."""
    maze = create_open_maze()

    direction = ReturnHomeBehavior.get_direction_toward_home(
        maze=maze,
        ghost_position=(2, 2),
        home_position=(3, 3),
    )

    assert direction is Direction.RIGHT

