"""Tests for Pac-Man ghost behavior modes."""

from src.ai.ghost_mode import GhostMode


def test_ghost_mode_contains_all_required_modes() -> None:
    """GhostMode should contain all required AI modes."""
    expected_modes = {
        "chase",
        "flee",
        "return_home",
    }

    actual_modes = {
        ghost_mode.value
        for ghost_mode in GhostMode
    }

    assert actual_modes == expected_modes


def test_ghost_mode_values_are_unique() -> None:
    """Every ghost mode should have a unique value."""
    mode_values = [
        ghost_mode.value
        for ghost_mode in GhostMode
    ]

    assert len(mode_values) == len(set(mode_values))


def test_chase_mode_exists() -> None:
    """CHASE mode should be available."""
    assert GhostMode.CHASE.value == "chase"


def test_flee_mode_exists() -> None:
    """FLEE mode should be available."""
    assert GhostMode.FLEE.value == "flee"


def test_return_home_mode_exists() -> None:
    """RETURN_HOME mode should be available."""
    assert GhostMode.RETURN_HOME.value == "return_home"
