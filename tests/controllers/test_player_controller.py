"""Tests for the Pac-Man player controller."""

from unittest.mock import Mock

import pytest

from src.controllers.player_controller import PlayerController
from src.entities.direction import Direction
from src.entities.player import Player
from src.input.input_event import InputAction
from src.maze.maze import Maze
from src.systems.collision import CollisionSystem


def create_player_controller() -> PlayerController:
    """Create a player controller with mocked dependencies."""
    player = Mock(spec=Player)
    player.direction = Direction.NONE

    collision_system = Mock(spec=CollisionSystem)

    return PlayerController(
        player=player,
        collision_system=collision_system,
    )


@pytest.mark.parametrize(
    ("input_action", "expected_direction"),
    [
        (InputAction.MOVE_UP, Direction.UP),
        (InputAction.MOVE_RIGHT, Direction.RIGHT),
        (InputAction.MOVE_DOWN, Direction.DOWN),
        (InputAction.MOVE_LEFT, Direction.LEFT),
    ],
)
def test_movement_action_sets_player_direction(
    input_action: InputAction,
    expected_direction: Direction,
) -> None:
    """Movement input should set the player's requested direction."""
    controller = create_player_controller()

    controller.handle_action(input_action)

    assert controller.player.direction is expected_direction


def test_non_movement_action_does_not_change_direction() -> None:
    """Non-movement input should not change the player's direction."""
    controller = create_player_controller()
    controller.player.direction = Direction.LEFT

    controller.handle_action(InputAction.PAUSE_GAME)

    assert controller.player.direction is Direction.LEFT


def test_update_moves_player_through_collision_system() -> None:
    """Updating the controller should move the player through collision checks."""
    player = Mock(spec=Player)
    player.direction = Direction.RIGHT
    player.position = (1, 1)

    collision_system = Mock(spec=CollisionSystem)
    collision_system.move_if_valid.return_value = True

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = PlayerController(
        player=player,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        player,
        (2, 1),
        maze,
    )


def test_update_does_not_require_player_to_move_when_direction_is_none() -> None:
    """A player with no movement direction should remain in place."""
    player = Mock(spec=Player)
    player.direction = Direction.NONE
    player.position = (1, 1)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = PlayerController(
        player=player,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        player,
        (1, 1),
        maze,
    )
