"""Tests for the Pac-Man input state."""

from src.entities.direction import Direction
from src.input.input_state import InputState


def test_input_state_starts_with_no_direction() -> None:
    """InputState should start without a requested direction."""
    input_state = InputState()

    assert input_state.requested_direction is Direction.NONE
    assert not input_state.has_requested_direction()


def test_set_direction_stores_requested_direction() -> None:
    """InputState should store the requested movement direction."""
    input_state = InputState()

    input_state.set_direction(Direction.UP)

    assert input_state.requested_direction is Direction.UP
    assert input_state.has_requested_direction()


def test_set_direction_can_change_direction() -> None:
    """InputState should allow the requested direction to change."""
    input_state = InputState()

    input_state.set_direction(Direction.LEFT)
    input_state.set_direction(Direction.RIGHT)

    assert input_state.requested_direction is Direction.RIGHT


def test_clear_direction_removes_requested_direction() -> None:
    """Clearing the input should restore Direction.NONE."""
    input_state = InputState()

    input_state.set_direction(Direction.DOWN)
    input_state.clear_direction()

    assert input_state.requested_direction is Direction.NONE
    assert not input_state.has_requested_direction()
