"""Tests for the A-Maze-ing maze adapter."""

import pytest

from src.maze.adapter import MazeAdapter, MazeGenerationError
from src.maze.maze import Wall


def test_generate_level_returns_maze() -> None:
    """Adapter should convert generated data into a Maze."""
    adapter = MazeAdapter()

    maze = adapter.generate_level(
        width=19,
        height=21,
        seed=42,
    )

    assert maze.width == 19
    assert maze.height == 21
    assert len(maze.cells) == 21
    assert all(len(row) == 19 for row in maze.cells)


def test_generated_cells_have_valid_coordinates() -> None:
    """Generated cells should contain their grid coordinates."""
    adapter = MazeAdapter()

    maze = adapter.generate_level(
        width=19,
        height=21,
        seed=42,
    )

    for y, row in enumerate(maze.cells):
        for x, cell in enumerate(row):
            assert cell.x == x
            assert cell.y == y


def test_invalid_dimensions_are_rejected() -> None:
    """Adapter should reject invalid maze dimensions."""
    adapter = MazeAdapter()

    with pytest.raises(ValueError):
        adapter.generate_level(
            width=0,
            height=21,
            seed=42,
        )


def test_invalid_entry_is_rejected() -> None:
    """Adapter should reject an entry outside the maze."""
    adapter = MazeAdapter()

    with pytest.raises(ValueError):
        adapter.generate_level(
            width=19,
            height=21,
            seed=42,
            entry_cell=(19, 0),
        )


def test_invalid_exit_is_rejected() -> None:
    """Adapter should reject an exit outside the maze."""
    adapter = MazeAdapter()

    with pytest.raises(ValueError):
        adapter.generate_level(
            width=19,
            height=21,
            seed=42,
            exit_cell=(19, 0),
        )


def test_maze_cells_use_wall_flags() -> None:
    """Generated cells should expose walls through Wall flags."""
    adapter = MazeAdapter()

    maze = adapter.generate_level(
        width=19,
        height=21,
        seed=42,
    )

    for row in maze.cells:
        for cell in row:
            assert isinstance(cell.walls, Wall)