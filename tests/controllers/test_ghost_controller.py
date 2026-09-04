"""Tests for the Pac-Man ghost controller."""

from unittest.mock import Mock

from src.controllers.ghost_controller import GhostController
from src.entities.direction import Direction
from src.entities.ghost import Ghost
from src.maze.maze import Maze
from src.systems.collision import CollisionSystem


def test_update_moves_ghost_through_collision_system() -> None:
    """Updating the controller should validate the ghost's next position."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.RIGHT
    ghost.position = (1, 1)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (2, 1),
        maze,
    )


def test_update_with_no_direction_keeps_ghost_in_place() -> None:
    """A ghost with no direction should remain in its current position."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.NONE
    ghost.position = (2, 3)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (2, 3),
        maze,
    )


def test_update_does_not_move_ghost_outside_maze() -> None:
    """The movement system should keep an out-of-bounds ghost in place."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.LEFT
    ghost.position = (0, 1)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = False

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (0, 1),
        maze,
    )
