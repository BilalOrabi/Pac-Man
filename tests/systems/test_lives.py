"""Tests for the lives system."""

import pytest

from src.systems.lives import LivesSystem


def test_lives_system_starts_with_configured_lives() -> None:
    """Lives system should use the configured starting lives."""
    lives_system = LivesSystem(starting_lives=3)

    assert lives_system.remaining_lives == 3
    assert lives_system.is_alive


def test_lose_life_removes_one_life() -> None:
    """Losing a life should decrease the remaining lives by one."""
    lives_system = LivesSystem(starting_lives=3)

    lives_system.lose_life()

    assert lives_system.remaining_lives == 2
    assert lives_system.is_alive


def test_lose_last_life_makes_player_dead() -> None:
    """Losing the final life should make the player no longer alive."""
    lives_system = LivesSystem(starting_lives=1)

    result = lives_system.lose_life()

    assert result is False
    assert lives_system.remaining_lives == 0
    assert not lives_system.is_alive


def test_losing_life_when_already_dead_does_not_go_negative() -> None:
    """Remaining lives should never become negative."""
    lives_system = LivesSystem(starting_lives=1)

    lives_system.lose_life()
    lives_system.lose_life()

    assert lives_system.remaining_lives == 0


def test_add_life_increases_remaining_lives() -> None:
    """Adding a life should increase the remaining lives by one."""
    lives_system = LivesSystem(starting_lives=2)

    lives_system.add_life()

    assert lives_system.remaining_lives == 3


def test_reset_restores_configured_lives() -> None:
    """Reset should restore the requested number of lives."""
    lives_system = LivesSystem(starting_lives=3)

    lives_system.lose_life()
    lives_system.reset(starting_lives=3)

    assert lives_system.remaining_lives == 3
    assert lives_system.is_alive


def test_starting_lives_must_be_positive() -> None:
    """Lives system should reject zero or negative starting lives."""
    with pytest.raises(ValueError):
        LivesSystem(starting_lives=0)

    with pytest.raises(ValueError):
        LivesSystem(starting_lives=-1)


def test_reset_lives_must_be_positive() -> None:
    """Reset should reject zero or negative life counts."""
    lives_system = LivesSystem(starting_lives=3)

    with pytest.raises(ValueError):
        lives_system.reset(starting_lives=0)

    with pytest.raises(ValueError):
        lives_system.reset(starting_lives=-1)
