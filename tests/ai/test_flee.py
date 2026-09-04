"""Tests for Pac-Man ghost flee behavior."""

import pytest

from src.ai.flee import FleeBehavior
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


def test_flee_moves_right_when_right_is_farthest() -> None:
    """Flee should choose RIGHT when it provides the greatest distance."""
    maze = create_open_maze()

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 2),
        target_position=(0, 2),
    )

    assert direction is Direction.RIGHT


def test_flee_moves_left_when_left_is_farthest() -> None:
    """Flee should choose LEFT when it provides the greatest distance."""
    maze = create_open_maze()

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(3, 2),
        target_position=(4, 2),
    )

    assert direction is Direction.LEFT


def test_flee_moves_down_when_down_is_farthest() -> None:
    """Flee should choose DOWN when DOWN is the farthest option."""
    maze = create_maze_with_solid_cells(
        solid_positions={(0, 1), (2, 1)},
    )

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(1, 0),
    )

    assert direction is Direction.DOWN


def test_flee_moves_up_when_up_is_farthest() -> None:
    """Flee should choose UP when UP is the farthest option."""
    maze = create_maze_with_solid_cells(
        solid_positions={(0, 2), (2, 2), (1, 3)},
    )

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 2),
        target_position=(1, 4),
    )

    assert direction is Direction.UP


def test_flee_avoids_solid_cell() -> None:
    """Flee should not choose a direction leading into a solid cell."""
    maze = create_maze_with_solid_cells(
        solid_positions={(2, 1)},
        width=3,
        height=3,
    )

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(1, 0),
    )

    assert direction is Direction.LEFT


def test_flee_returns_none_when_no_direction_is_walkable() -> None:
    """Flee should return NONE when the ghost is completely blocked."""
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

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(0, 0),
    )

    assert direction is Direction.NONE


def test_flee_rejects_position_outside_maze() -> None:
    """Flee should reject a ghost position outside the maze."""
    maze = create_open_maze()

    with pytest.raises(ValueError):
        FleeBehavior.get_direction_away_from_target(
            maze=maze,
            ghost_position=(10, 10),
            target_position=(1, 1),
        )


def test_flee_uses_deterministic_tie_breaking() -> None:
    """Flee should use the defined priority when distances are equal."""
    maze = create_open_maze()

    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(3, 3),
    )

    assert direction is Direction.LEFT


def test_flee_obeys_no_reverse_rule_at_junction() -> None:
    """Flee should not reverse direction if an alternative is open."""
    maze = create_open_maze()

    # Target is to the RIGHT (3, 2). Moving LEFT maximizes distance.
    # But if ghost is already moving RIGHT, LEFT is forbidden at this junction.
    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(3, 2),
        current_direction=Direction.RIGHT,
    )

    assert direction != Direction.LEFT
    assert direction in (Direction.UP, Direction.DOWN, Direction.RIGHT)


def test_flee_reverses_at_dead_end() -> None:
    """Flee should reverse if all other directions are blocked."""
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
    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(0, 1),
        current_direction=Direction.RIGHT,
    )

    assert direction is Direction.LEFT


def test_flee_reverses_in_corridor_when_facing_target() -> None:
    """Fleeing ghost facing target in a corridor must turn around to escape."""
    # Horizontal corridor: y=1 is open for x=0..4, y=0 and y=2 are solid walls
    cells = []
    for y in range(3):
        row = []
        for x in range(5):
            is_wall = (y != 1)
            row.append(
                MazeCell(
                    (x, y),
                    Wall.ALL if is_wall else Wall.NONE,
                    is_wall,
                )
            )
        cells.append(tuple(row))
    maze = Maze(5, 3, tuple(cells), (0, 1), (4, 1), "")

    # Ghost is at (2, 1) heading RIGHT towards target at (4, 1).
    # Moving RIGHT approaches target. LEFT flees away.
    direction = FleeBehavior.get_direction_away_from_target(
        maze=maze,
        ghost_position=(2, 1),
        target_position=(4, 1),
        current_direction=Direction.RIGHT,
    )

    assert direction is Direction.LEFT
