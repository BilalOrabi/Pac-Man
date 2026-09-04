"""Tests for the Pac-Man animation system."""

import pytest

from src.rendering.animation import Animation


def test_animation_starts_at_zero_progress() -> None:
    """A new animation should have zero progress."""
    animation = Animation(duration=2.0)

    assert animation.elapsed_time == 0.0
    assert animation.progress == 0.0
    assert animation.is_finished is False


def test_animation_rejects_non_positive_duration() -> None:
    """Animation duration must be greater than zero."""
    with pytest.raises(ValueError):
        Animation(duration=0.0)

    with pytest.raises(ValueError):
        Animation(duration=-1.0)


def test_update_advances_animation() -> None:
    """Updating should advance the animation progress."""
    animation = Animation(duration=4.0)

    animation.update(1.0)

    assert animation.elapsed_time == 1.0
    assert animation.progress == 0.25
    assert animation.is_finished is False


def test_animation_finishes_at_duration() -> None:
    """An animation should finish when its duration is reached."""
    animation = Animation(duration=2.0)

    animation.update(2.0)

    assert animation.elapsed_time == 2.0
    assert animation.progress == 1.0
    assert animation.is_finished is True


def test_animation_clamps_progress_after_duration() -> None:
    """Progress should never exceed one."""
    animation = Animation(duration=2.0)

    animation.update(5.0)

    assert animation.elapsed_time == 2.0
    assert animation.progress == 1.0
    assert animation.is_finished is True


def test_negative_elapsed_time_is_rejected() -> None:
    """Negative elapsed time should be rejected."""
    animation = Animation(duration=2.0)

    with pytest.raises(ValueError):
        animation.update(-1.0)


def test_finished_animation_does_not_continue_updating() -> None:
    """A finished animation should remain finished."""
    animation = Animation(duration=2.0)

    animation.update(2.0)
    animation.update(1.0)

    assert animation.elapsed_time == 2.0
    assert animation.progress == 1.0
    assert animation.is_finished is True


def test_reset_returns_animation_to_initial_state() -> None:
    """Reset should return the animation to its initial state."""
    animation = Animation(duration=2.0)

    animation.update(2.0)
    animation.reset()

    assert animation.elapsed_time == 0.0
    assert animation.progress == 0.0
    assert animation.is_finished is False
