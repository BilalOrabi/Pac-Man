"""Tests for the collision system."""

from src.entities.direction import Direction
from src.entities.entity import Entity
from src.maze.maze import Maze, MazeCell, Wall
from src.systems.collision import CollisionSystem


def create_test_maze() -> Maze:
    """Create a small maze containing one solid block."""
    cells = (
        (
            MazeCell((0, 0), Wall.NONE, False),
            MazeCell((1, 0), Wall.ALL, True),
            MazeCell((2, 0), Wall.NONE, False),
        ),
        (
            MazeCell((0, 1), Wall.NONE, False),
            MazeCell((1, 1), Wall.NONE, False),
            MazeCell((2, 1), Wall.NONE, False),
        ),
        (
            MazeCell((0, 2), Wall.NONE, False),
            MazeCell((1, 2), Wall.NONE, False),
            MazeCell((2, 2), Wall.NONE, False),
        ),
    )

    return Maze(
        width=3,
        height=3,
        cells=cells,
        entry=(0, 0),
        exit=(2, 2),
        shortest_path="",
    )


def create_test_entity(position: tuple[int, int]) -> Entity:
    """Create an entity for collision tests."""
    return Entity(
        position=position,
        direction=Direction.NONE,
        speed=1.0,
    )


def test_can_move_to_walkable_cell() -> None:
    """An entity should be able to move to a walkable cell."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    assert CollisionSystem.can_move_to(entity, (0, 1), maze)


def test_cannot_move_to_solid_block() -> None:
    """An entity should not be able to enter a solid block."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    assert not CollisionSystem.can_move_to(entity, (1, 0), maze)


def test_cannot_move_outside_maze() -> None:
    """An entity should not be able to leave the maze."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    assert not CollisionSystem.can_move_to(entity, (-1, 0), maze)


def test_move_if_valid_moves_entity() -> None:
    """A valid target position should update the entity position."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    moved = CollisionSystem.move_if_valid(
        entity,
        (0, 1),
        maze,
    )

    assert moved
    assert entity.position == (0, 1)


def test_move_if_valid_rejects_solid_block() -> None:
    """A solid block should prevent the entity from moving."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    moved = CollisionSystem.move_if_valid(
        entity,
        (1, 0),
        maze,
    )

    assert not moved
    assert entity.position == (0, 0)


def test_move_if_valid_rejects_out_of_bounds_position() -> None:
    """An out-of-bounds position should prevent movement."""
    maze = create_test_maze()
    entity = create_test_entity((0, 0))

    moved = CollisionSystem.move_if_valid(
        entity,
        (-1, 0),
        maze,
    )

    assert not moved
    assert entity.position == (0, 0)
