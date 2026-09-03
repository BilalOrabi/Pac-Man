"""Tests for Pac-Man ghost chase behavior."""

import pytest

from src.ai.chase import ChaseBehavior
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


def test_chase_moves_right_toward_target() -> None:
    """Chase should move right when the target is directly right."""
    maze = create_open_maze()

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(1, 2),
        target_position=(4, 2),
    )

    assert direction is Direction.RIGHT


def test_chase_moves_left_toward_target() -> None:
    """Chase should move left when the target is directly left."""
    maze = create_open_maze()

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(4, 2),
        target_position=(1, 2),
    )

    assert direction is Direction.LEFT


def test_chase_moves_up_toward_target() -> None:
    """Chase should move up when the target is directly above."""
    maze = create_open_maze()

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(2, 4),
        target_position=(2, 1),
    )

    assert direction is Direction.UP


def test_chase_moves_down_toward_target() -> None:
    """Chase should move down when the target is directly below."""
    maze = create_open_maze()

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(2, 1),
        target_position=(2, 4),
    )

    assert direction is Direction.DOWN


def test_chase_avoids_solid_cell() -> None:
    """Chase should avoid a solid cell blocking the direct route."""
    cells = []

    for y in range(3):
        row = []

        for x in range(3):
            is_solid_block = (x, y) == (1, 1)

            row.append(
                MazeCell(
                    position=(x, y),
                    walls=(
                        Wall.ALL
                        if is_solid_block
                        else Wall.NONE
                    ),
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

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(1, 0),
        target_position=(1, 2),
    )

    assert direction is Direction.RIGHT


def test_chase_returns_none_when_surrounded() -> None:
    """Chase should return NONE when no neighboring cell is walkable."""
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

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(0, 0),
    )

    assert direction is Direction.NONE


def test_chase_rejects_position_outside_maze() -> None:
    """Chase should reject a ghost position outside the maze."""
    maze = create_open_maze()

    with pytest.raises(ValueError):
        ChaseBehavior.get_direction_toward_target(
            maze=maze,
            ghost_position=(10, 10),
            target_position=(1, 1),
        )


def test_chase_uses_deterministic_tie_breaking() -> None:
    """Chase should use the defined priority when distances are equal."""
    maze = create_open_maze()

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(3, 3),
    )

    assert direction is Direction.RIGHT
