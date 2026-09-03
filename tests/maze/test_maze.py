"""Tests for the maze domain model."""

import pytest

from src.maze.maze import Maze, MazeCell, Wall


def _create_maze() -> Maze:
    """Create a small maze for testing."""
    cells = (
        (
            MazeCell(
                position=(0, 0),
                walls=Wall.NORTH | Wall.WEST,
                is_solid_block=False,
            ),
            MazeCell(
                position=(1, 0),
                walls=Wall.NORTH | Wall.EAST,
                is_solid_block=False,
            ),
        ),
        (
            MazeCell(
                position=(0, 1),
                walls=Wall.SOUTH | Wall.WEST,
                is_solid_block=False,
            ),
            MazeCell(
                position=(1, 1),
                walls=Wall.ALL,
                is_solid_block=True,
            ),
        ),
    )

    return Maze(
        width=2,
        height=2,
        cells=cells,
        entry=(0, 0),
        exit=(1, 0),
        shortest_path="E",
    )


def test_cell_has_wall() -> None:
    """MazeCell should correctly report walls."""
    cell = MazeCell(
        position=(0, 0),
        walls=Wall.NORTH | Wall.WEST,
        is_solid_block=False,
    )

    assert cell.has_wall(Wall.NORTH)
    assert cell.has_wall(Wall.WEST)
    assert not cell.has_wall(Wall.SOUTH)
    assert not cell.has_wall(Wall.EAST)


def test_maze_get_cell() -> None:
    """Maze should return the cell at the requested position."""
    maze = _create_maze()

    cell = maze.get_cell((1, 0))

    assert cell.position == (1, 0)
    assert cell.x == 1
    assert cell.y == 0


def test_maze_get_cell_out_of_bounds() -> None:
    """Maze should reject positions outside its bounds."""
    maze = _create_maze()

    with pytest.raises(IndexError):
        maze.get_cell((2, 0))


def test_maze_is_inside() -> None:
    """Maze should correctly identify valid positions."""
    maze = _create_maze()

    assert maze.is_inside(0, 0)
    assert maze.is_inside(1, 1)
    assert not maze.is_inside(2, 0)
    assert not maze.is_inside(0, 2)


def test_maze_is_walkable() -> None:
    """Maze should identify walkable and solid cells."""
    maze = _create_maze()

    assert maze.is_walkable((0, 0))
    assert maze.is_walkable((1, 0))
    assert not maze.is_walkable((1, 1))


def test_maze_outside_is_not_walkable() -> None:
    """Positions outside the maze should not be walkable."""
    maze = _create_maze()

    assert not maze.is_walkable((-1, 0))
    assert not maze.is_walkable((2, 0))
