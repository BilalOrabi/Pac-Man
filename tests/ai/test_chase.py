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


def test_chase_obeys_no_reverse_rule_at_junction() -> None:
    """Chase should not reverse direction if an alternative is open."""
    maze = create_open_maze()

    # Target is directly behind the ghost (LEFT).
    # Since ghost is moving RIGHT, LEFT is forbidden at this junction.
    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(0, 2),
        current_direction=Direction.RIGHT,
    )

    assert direction != Direction.LEFT
    assert direction in (Direction.UP, Direction.DOWN, Direction.RIGHT)


def test_chase_reverses_at_dead_end() -> None:
    """Chase should reverse if all other directions are blocked."""
    cells = [
        [
            MazeCell(
                position=(x, y),
                walls=Wall.ALL,
                is_solid_block=True,
            )
            for x in range(3)
        ]
        for y in range(3)
    ]
    # Make a dead-end corridor: (0, 1) <-> (1, 1), blocked everywhere else
    cells[1][0] = MazeCell((0, 1), Wall.NONE, False)
    cells[1][1] = MazeCell((1, 1), Wall.NONE, False)

    maze = Maze(
        width=3,
        height=3,
        cells=tuple(tuple(row) for row in cells),
        entry=(0, 1),
        exit=(1, 1),
        shortest_path="",
    )

    # Ghost is at (1, 1) after moving RIGHT from (0, 1). Only LEFT is open.
    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(2, 1),
        current_direction=Direction.RIGHT,
    )

    assert direction is Direction.LEFT


def test_chase_navigates_corridor_around_wall() -> None:
    """Chase should navigate open corridor bends to reach target."""
    cells = [
        [
            MazeCell(position=(x, y), walls=Wall.NONE, is_solid_block=False)
            for x in range(3)
        ]
        for y in range(3)
    ]
    # Wall between (0, 0) and (2, 0) at (1, 0)
    cells[0][1] = MazeCell(
        position=(1, 0), walls=Wall.ALL, is_solid_block=True
    )

    maze = Maze(
        width=3,
        height=3,
        cells=tuple(tuple(row) for row in cells),
        entry=(0, 0),
        exit=(2, 0),
        shortest_path="",
    )

    # From (0, 0), RIGHT is blocked by wall at (1, 0).
    # BFS should navigate DOWN to (0, 1) to follow corridor around wall.
    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(0, 0),
        target_position=(2, 0),
    )
    assert direction is Direction.DOWN


def test_chase_resolves_solid_wall_target() -> None:
    """Chase should navigate toward nearest walkable cell if target in wall."""
    cells = [
        [
            MazeCell(position=(x, y), walls=Wall.NONE, is_solid_block=False)
            for x in range(3)
        ]
        for y in range(3)
    ]
    # (1, 1) is a solid wall
    cells[1][1] = MazeCell(
        position=(1, 1), walls=Wall.ALL, is_solid_block=True
    )

    maze = Maze(
        width=3,
        height=3,
        cells=tuple(tuple(row) for row in cells),
        entry=(0, 0),
        exit=(2, 2),
        shortest_path="",
    )

    direction = ChaseBehavior.get_direction_toward_target(
        maze=maze,
        ghost_position=(0, 0),
        target_position=(1, 1),
    )
    assert direction in (Direction.RIGHT, Direction.DOWN)
