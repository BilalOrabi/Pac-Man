"""Tests for the Pac-Man player renderer."""

import pytest

from src.entities.player import Player
from src.entities.direction import Direction
from src.rendering.player_renderer import PlayerRenderer


def create_test_player() -> Player:
    """Create a player for renderer tests."""
    return Player(
        position=(1, 1),
        direction=Direction.RIGHT,
    )


def test_player_renderer_starts_uninitialized() -> None:
    """PlayerRenderer should initially be uninitialized."""
    renderer = PlayerRenderer()

    assert renderer.is_initialized is False
    assert renderer.player is None


def test_initialize_initializes_renderer() -> None:
    """Initialize should activate the renderer."""
    renderer = PlayerRenderer()

    renderer.initialize()

    assert renderer.is_initialized is True


def test_set_player_assigns_player() -> None:
    """The renderer should store the player to be rendered."""
    renderer = PlayerRenderer()
    player = create_test_player()

    renderer.set_player(player)

    assert renderer.player is player


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = PlayerRenderer()
    renderer.set_player(create_test_player())

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_player() -> None:
    """Rendering without a player should fail."""
    renderer = PlayerRenderer()
    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_when_initialized_with_player() -> None:
    """Rendering should succeed with a valid initialized renderer."""
    renderer = PlayerRenderer()
    renderer.initialize()
    renderer.set_player(create_test_player())

    renderer.render()


def test_shutdown_deactivates_renderer() -> None:
    """Shutdown should deactivate the renderer."""
    renderer = PlayerRenderer()
    renderer.initialize()

    renderer.shutdown()

    assert renderer.is_initialized is False
