"""Tests for the Pac-Man visual effect system."""

import pytest

from src.rendering.animation import Animation
from src.rendering.effect import VisualEffect


def create_effect() -> VisualEffect:
    """Create a visual effect for testing."""
    return VisualEffect(
        name="power_mode",
        animation=Animation(duration=2.0),
    )


def test_effect_starts_enabled() -> None:
    """A new visual effect should be enabled."""
    effect = create_effect()

    assert effect.is_enabled is True
    assert effect.is_finished is False
    assert effect.progress == 0.0


def test_effect_rejects_empty_name() -> None:
    """An effect name cannot be empty."""
    with pytest.raises(ValueError):
        VisualEffect(
            name="",
            animation=Animation(duration=1.0),
        )


def test_effect_rejects_whitespace_name() -> None:
    """An effect name cannot contain only whitespace."""
    with pytest.raises(ValueError):
        VisualEffect(
            name="   ",
            animation=Animation(duration=1.0),
        )


def test_effect_updates_animation() -> None:
    """Updating an enabled effect should advance its animation."""
    effect = create_effect()

    effect.update(1.0)

    assert effect.progress == 0.5
    assert effect.is_finished is False


def test_effect_finishes_when_animation_finishes() -> None:
    """The effect should finish when its animation finishes."""
    effect = create_effect()

    effect.update(2.0)

    assert effect.progress == 1.0
    assert effect.is_finished is True


def test_disabled_effect_does_not_update() -> None:
    """A disabled effect should not advance."""
    effect = create_effect()

    effect.disable()
    effect.update(1.0)

    assert effect.progress == 0.0
    assert effect.is_finished is False


def test_enable_allows_effect_to_update_again() -> None:
    """An enabled effect should resume updating."""
    effect = create_effect()

    effect.disable()
    effect.update(1.0)

    effect.enable()
    effect.update(1.0)

    assert effect.progress == 0.5


def test_reset_resets_effect_animation() -> None:
    """Reset should return the effect to its initial state."""
    effect = create_effect()

    effect.update(2.0)
    effect.reset()

    assert effect.progress == 0.0
    assert effect.is_finished is False


def test_restart_enables_and_resets_effect() -> None:
    """Restart should enable and reset the effect."""
    effect = create_effect()

    effect.update(2.0)
    effect.disable()
    effect.restart()

    assert effect.is_enabled is True
    assert effect.progress == 0.0
    assert effect.is_finished is False
