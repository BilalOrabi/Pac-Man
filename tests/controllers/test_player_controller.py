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
    """Update should move player through collision checks."""
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


def test_update_keeps_player_in_place_when_direction_is_none() -> None:
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


def test_instant_turnaround_inverts_progress_and_swaps_positions() -> None:
    """Reversing direction mid-corridor should immediately invert progress."""
    player = Player(
        position=(5, 5),
        direction=Direction.RIGHT,
        target_position=(6, 5),
        movement_progress=0.4,
    )
    collision_system = Mock(spec=CollisionSystem)
    controller = PlayerController(
        player=player,
        collision_system=collision_system,
    )

    controller.handle_action(InputAction.MOVE_LEFT)

    assert player.direction is Direction.LEFT
    assert player.position == (6, 5)
    assert player.target_position == (5, 5)
    assert abs(player.movement_progress - 0.6) < 1e-6


def test_edge_wall_turnaround_resets_progress_cleanly() -> None:
    """Reversing when stopped against an edge wall starts a clean step."""
    player = Player(
        position=(0, 5),
        direction=Direction.LEFT,
        target_position=None,
        movement_progress=0.0,
    )
    collision_system = Mock(spec=CollisionSystem)
    controller = PlayerController(
        player=player,
        collision_system=collision_system,
    )

    controller.handle_action(InputAction.MOVE_RIGHT)

    assert player.direction is Direction.RIGHT
    assert player.target_position is None
    assert player.movement_progress == 0.0
