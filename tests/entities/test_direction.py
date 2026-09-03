"""Tests for the Direction enum."""

from src.entities.direction import Direction
import pytest


def test_direction_contains_all_cardinal_directions() -> None:
    """Direction should contain the four cardinal movement directions."""
    assert Direction.UP
    assert Direction.RIGHT
    assert Direction.DOWN
    assert Direction.LEFT


def test_direction_values_are_unique() -> None:
    """Each direction should have a unique value."""
    direction_values = {
        Direction.UP,
        Direction.RIGHT,
        Direction.DOWN,
        Direction.LEFT,
    }

    assert len(direction_values) == 4


def test_direction_is_an_enum() -> None:
    """Direction should behave as a proper enum."""
    assert isinstance(Direction.UP, Direction)


def test_direction_opposite_returns_expected_direction() -> None:
    """Each direction should return its correct opposite."""
    assert Direction.UP.opposite() == Direction.DOWN
    assert Direction.RIGHT.opposite() == Direction.LEFT
    assert Direction.DOWN.opposite() == Direction.UP
    assert Direction.LEFT.opposite() == Direction.RIGHT


def test_direction_opposite_is_involutive() -> None:
    """Applying opposite twice should return the original direction."""
    for direction in Direction:
        assert direction.opposite().opposite() == direction


def test_direction_rejects_invalid_value() -> None:
    """Direction should reject values that are not valid directions."""
    with pytest.raises(ValueError):
        Direction("invalid")
