"""Tests for the A-Maze-ing maze adapter."""

from pathlib import Path

import pytest

from src.maze.adapter import MazeAdapter
from src.maze.maze import Wall
from src.utils.error_logger import ErrorLogger


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


def test_generate_level_avoids_42_solid_block_at_width_14() -> None:
    """Dimensions like 14x10 should not spawn entry inside '42' solid block."""
    adapter = MazeAdapter()
    maze = adapter.generate_level(
        width=14,
        height=10,
        seed=42,
    )

    entry_cell = maze.get_cell(maze.entry)
    assert not entry_cell.is_solid_block
    assert maze.shortest_path != ""
    assert any(
        not cell.is_solid_block and cell.walls != Wall.ALL
        for row in maze.cells
        for cell in row
    )


def test_generate_level_captures_small_maze_warning_to_error_logger(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Small mazes trigger MazeGenerator warning, captured to ErrorLogger."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.install(str(log_file))
    try:
        adapter = MazeAdapter()
        maze = adapter.generate_level(
            width=8,
            height=8,
            seed=42,
        )
        assert maze is not None
        captured = capsys.readouterr()
        assert "maze is too small" not in captured.out
        assert log_file.exists()
        log_content = log_file.read_text(encoding="utf-8")
        assert (
            "MazeGenerator Warning: maze is too small to add '42' in it"
            in log_content
        )
    finally:
        ErrorLogger.uninstall()
