"""Tests for the Pac-Man input manager."""

from src.entities.direction import Direction
from src.input.input_event import InputAction, InputEvent
from src.input.input_manager import InputManager


def test_input_manager_starts_with_no_direction() -> None:
    """InputManager should start without a requested direction."""
    input_manager = InputManager()

    assert (
        input_manager.get_requested_direction()
        is Direction.NONE
    )


def test_movement_event_updates_requested_direction() -> None:
    """A movement event should update the requested direction."""
    input_manager = InputManager()

    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_UP)
    )

    assert (
        input_manager.get_requested_direction()
        is Direction.UP
    )


def test_new_movement_event_replaces_previous_direction() -> None:
    """The newest movement event should replace the previous direction."""
    input_manager = InputManager()

    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_LEFT)
    )
    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_RIGHT)
    )

    assert (
        input_manager.get_requested_direction()
        is Direction.RIGHT
    )


def test_non_movement_event_does_not_change_direction() -> None:
    """Non-movement events should not alter the requested direction."""
    input_manager = InputManager()

    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_DOWN)
    )

    input_manager.process_event(
        InputEvent(action=InputAction.PAUSE_GAME)
    )

    assert (
        input_manager.get_requested_direction()
        is Direction.DOWN
    )


def test_restart_event_clears_direction() -> None:
    """Restarting the game should clear the movement request."""
    input_manager = InputManager()

    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_RIGHT)
    )
    input_manager.process_event(
        InputEvent(action=InputAction.RESTART_GAME)
    )

    assert (
        input_manager.get_requested_direction()
        is Direction.NONE
    )


def test_clear_direction_resets_input_state() -> None:
    """clear_direction should remove the current movement request."""
    input_manager = InputManager()

    input_manager.process_event(
        InputEvent(action=InputAction.MOVE_DOWN)
    )

    input_manager.clear_direction()

    assert (
        input_manager.get_requested_direction()
        is Direction.NONE
    )
