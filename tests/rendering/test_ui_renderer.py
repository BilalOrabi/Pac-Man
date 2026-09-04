"""Tests for the Pac-Man user-interface renderer."""

import pytest

from src.rendering.ui_renderer import UIRenderer


def test_ui_renderer_starts_with_default_values() -> None:
    """UIRenderer should start with sensible default values."""
    renderer = UIRenderer()

    assert renderer.is_initialized is False
    assert renderer.score == 0
    assert renderer.lives == 0
    assert renderer.level_number == 1
    assert renderer.message == ""


def test_initialize_initializes_renderer() -> None:
    """Initialize should activate the renderer."""
    renderer = UIRenderer()

    renderer.initialize()

    assert renderer.is_initialized is True


def test_set_score_updates_score() -> None:
    """The displayed score should be updated."""
    renderer = UIRenderer()

    renderer.set_score(500)

    assert renderer.score == 500


def test_set_score_rejects_negative_score() -> None:
    """Negative scores should be rejected."""
    renderer = UIRenderer()

    with pytest.raises(ValueError):
        renderer.set_score(-1)


def test_set_lives_updates_lives() -> None:
    """The displayed lives should be updated."""
    renderer = UIRenderer()

    renderer.set_lives(3)

    assert renderer.lives == 3


def test_set_lives_rejects_negative_lives() -> None:
    """Negative lives should be rejected."""
    renderer = UIRenderer()

    with pytest.raises(ValueError):
        renderer.set_lives(-1)


def test_set_level_number_updates_level() -> None:
    """The displayed level number should be updated."""
    renderer = UIRenderer()

    renderer.set_level_number(4)

    assert renderer.level_number == 4


def test_set_level_number_rejects_zero() -> None:
    """A level number of zero should be rejected."""
    renderer = UIRenderer()

    with pytest.raises(ValueError):
        renderer.set_level_number(0)


def test_set_level_number_rejects_negative_number() -> None:
    """Negative level numbers should be rejected."""
    renderer = UIRenderer()

    with pytest.raises(ValueError):
        renderer.set_level_number(-1)


def test_set_message_updates_message() -> None:
    """The displayed message should be updated."""
    renderer = UIRenderer()

    renderer.set_message("READY!")

    assert renderer.message == "READY!"


def test_set_message_rejects_non_string_message() -> None:
    """Messages must be strings."""
    renderer = UIRenderer()

    with pytest.raises(TypeError):
        renderer.set_message(123)  # type: ignore[arg-type]


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = UIRenderer()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_when_initialized() -> None:
    """Rendering should succeed after initialization."""
    renderer = UIRenderer()

    renderer.initialize()
    renderer.render()


def test_shutdown_deactivates_renderer() -> None:
    """Shutdown should deactivate the renderer."""
    renderer = UIRenderer()

    renderer.initialize()
    renderer.shutdown()

    assert renderer.is_initialized is False
