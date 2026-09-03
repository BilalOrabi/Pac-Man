"""Tests for the movement system."""

from src.entities.direction import Direction
from src.entities.entity import Entity
from src.maze.maze import Maze, MazeCell, Wall
from src.systems.movement import MovementSystem


def create_open_maze(width: int = 5, height: int = 5) -> Maze:
    """Create a simple open maze for movement tests."""
    open_cell = MazeCell(
        position=(0, 0),
        walls=Wall.NONE,
        is_solid_block=False,
    )

    cells = tuple(
        tuple(
            MazeCell(
                position=(x, y),
                walls=open_cell.walls,
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


def create_entity(
    position: tuple[int, int],
    direction: Direction,
) -> Entity:
    """Create an entity for movement tests."""
    return Entity(
        position=position,
        direction=direction,
        speed=1.0,
    )


def test_move_up() -> None:
    """Entity should move one cell upward."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.UP)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (2, 1)


def test_move_right() -> None:
    """Entity should move one cell to the right."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.RIGHT)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (3, 2)


def test_move_down() -> None:
    """Entity should move one cell downward."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.DOWN)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (2, 3)


def test_move_left() -> None:
    """Entity should move one cell to the left."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.LEFT)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (1, 2)


def test_none_direction_does_not_move_entity() -> None:
    """Entity should remain stationary with no direction."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.NONE)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (2, 2)


def test_entity_cannot_leave_maze_bounds() -> None:
    """Entity should remain in place when movement leaves the maze."""
    maze = create_open_maze()
    entity = create_entity((0, 0), Direction.LEFT)

    MovementSystem.move_entity(entity, maze)

    assert entity.position == (0, 0)


def test_calculate_next_position_does_not_modify_entity() -> None:
    """Calculating movement should not modify the entity position."""
    maze = create_open_maze()
    entity = create_entity((2, 2), Direction.UP)

    next_position = MovementSystem.calculate_next_position(entity, maze)

    assert next_position == (2, 1)
    assert entity.position == (2, 2)
