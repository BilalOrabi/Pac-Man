"""Tests for Pac-Man ghost entities."""

import pytest

from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostState, GhostType


def test_ghost_has_expected_default_state() -> None:
    """A newly created ghost should start in chase mode."""
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(5, 5),
        home_position=(9, 10),
    )

    assert ghost.state == GhostState.CHASE
    assert ghost.direction == Direction.NONE
    assert ghost.speed == 1.0


def test_ghost_stores_identity() -> None:
    """A ghost should retain its assigned ghost type."""
    ghost = Ghost(
        ghost_type=GhostType.PINK,
        position=(3, 4),
        home_position=(9, 10),
    )

    assert ghost.ghost_type == GhostType.PINK


def test_ghost_stores_position() -> None:
    """A ghost should store its current position."""
    ghost = Ghost(
        ghost_type=GhostType.BLUE,
        position=(7, 8),
        home_position=(9, 10),
    )

    assert ghost.position == (7, 8)


def test_ghost_stores_home_position() -> None:
    """A ghost should store its home position."""
    ghost = Ghost(
        ghost_type=GhostType.ORANGE,
        position=(2, 3),
        home_position=(9, 10),
    )

    assert ghost.home_position == (9, 10)


def test_ghost_accepts_custom_direction() -> None:
    """A ghost should accept a specific movement direction."""
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(5, 5),
        home_position=(9, 10),
        direction=Direction.LEFT,
    )

    assert ghost.direction == Direction.LEFT


def test_ghost_accepts_custom_state() -> None:
    """A ghost should accept a specific behavioral state."""
    ghost = Ghost(
        ghost_type=GhostType.BLUE,
        position=(5, 5),
        home_position=(9, 10),
        state=GhostState.FLEE,
    )

    assert ghost.state == GhostState.FLEE


def test_ghost_accepts_custom_speed() -> None:
    """A ghost should accept a custom movement speed."""
    ghost = Ghost(
        ghost_type=GhostType.ORANGE,
        position=(5, 5),
        home_position=(9, 10),
        speed=2.5,
    )

    assert ghost.speed == 2.5


def test_ghost_type_is_enum() -> None:
    """Ghost types should be represented by a type-safe enum."""
    assert isinstance(GhostType.RED, GhostType)
    assert isinstance(GhostType.PINK, GhostType)
    assert isinstance(GhostType.BLUE, GhostType)
    assert isinstance(GhostType.ORANGE, GhostType)


def test_ghost_state_is_enum() -> None:
    """Ghost states should be represented by a type-safe enum."""
    assert isinstance(GhostState.CHASE, GhostState)
    assert isinstance(GhostState.FLEE, GhostState)
    assert isinstance(GhostState.RETURN_HOME, GhostState)


def test_ghost_type_values_are_unique() -> None:
    """Each ghost type should have a unique value."""
    ghost_type_values = {ghost_type.value for ghost_type in GhostType}

    assert len(ghost_type_values) == len(GhostType)


def test_ghost_state_values_are_unique() -> None:
    """Each ghost state should have a unique value."""
    ghost_state_values = {ghost_state.value for ghost_state in GhostState}

    assert len(ghost_state_values) == len(GhostState)


def test_ghost_rejects_invalid_type() -> None:
    """GhostType should reject invalid values."""
    with pytest.raises(ValueError):
        GhostType("invalid")


def test_ghost_rejects_invalid_state() -> None:
    """GhostState should reject invalid values."""
    with pytest.raises(ValueError):
        GhostState("invalid")
