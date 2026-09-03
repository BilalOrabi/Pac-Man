"""Tests for the Player entity."""

import pytest

from src.entities.direction import Direction
from src.entities.player import Player


def test_player_has_expected_default_state() -> None:
    """Player should initialize with the expected default state."""
    player = Player(position=(1, 2))

    assert player.position == (1, 2)
    assert player.direction is Direction.NONE
    assert player.speed == 0.0
    assert player.lives == 3
    assert player.score == 0
    assert player.is_powered_up is False


def test_player_can_add_score() -> None:
    """Player should increase its score by the requested amount."""
    player = Player(position=(1, 2))

    player.add_score(100)

    assert player.score == 100


def test_player_can_add_score_multiple_times() -> None:
    """Player score should accumulate across multiple score events."""
    player = Player(position=(1, 2))

    player.add_score(10)
    player.add_score(50)

    assert player.score == 60


def test_player_rejects_negative_score() -> None:
    """Player should reject negative score additions."""
    player = Player(position=(1, 2))

    with pytest.raises(ValueError):
        player.add_score(-10)


def test_player_can_lose_life() -> None:
    """Player should lose exactly one life."""
    player = Player(position=(1, 2), lives=3)

    player.lose_life()

    assert player.lives == 2


def test_player_cannot_lose_life_when_no_lives_remain() -> None:
    """Player should reject losing a life when already at zero."""
    player = Player(position=(1, 2), lives=0)

    with pytest.raises(ValueError):
        player.lose_life()


def test_player_can_activate_power_mode() -> None:
    """Player should enter power mode when activated."""
    player = Player(position=(1, 2))

    player.activate_power_mode()

    assert player.is_powered_up is True


def test_player_can_deactivate_power_mode() -> None:
    """Player should leave power mode when deactivated."""
    player = Player(position=(1, 2), is_powered_up=True)

    player.deactivate_power_mode()

    assert player.is_powered_up is False


def test_player_can_reset_position() -> None:
    """Player should move to the new position and stop."""
    player = Player(
        position=(1, 2),
        direction=Direction.RIGHT,
        speed=2.0,
    )

    player.reset_position((10, 15))

    assert player.position == (10, 15)
    assert player.direction is Direction.NONE
