"""Tests for the Pac-Man player renderer."""

from unittest.mock import Mock

import pytest

from src.entities.player import Player
from src.rendering.player_renderer import PlayerRenderer
from src.theme.asset_manager import AssetManager


def create_renderer() -> PlayerRenderer:
    """Create a player renderer for testing."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = True
    asset_manager.get_player_sprite.return_value = (
        "assets/images/player.png"
    )

    return PlayerRenderer(
        asset_manager=asset_manager,
    )


def test_renderer_starts_uninitialized() -> None:
    """Player renderer should start uninitialized."""
    renderer = create_renderer()

    assert renderer.is_initialized is False
    assert renderer.player is None
    assert renderer.player_sprite_asset is None


def test_initialize_loads_player_sprite() -> None:
    """Initialization should configure the player sprite."""
    renderer = create_renderer()

    renderer.initialize()

    assert renderer.is_initialized is True
    assert (
        renderer.player_sprite_asset
        == "assets/images/player.png"
    )


def test_initialize_initializes_asset_manager_when_needed() -> None:
    """Renderer should initialize an uninitialized asset manager."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = False
    asset_manager.get_player_sprite.return_value = (
        "assets/images/player.png"
    )

    renderer = PlayerRenderer(
        asset_manager=asset_manager,
    )

    renderer.initialize()

    asset_manager.initialize.assert_called_once()
    asset_manager.get_player_sprite.assert_called_once()


def test_set_player_assigns_player() -> None:
    """Renderer should store the player to be rendered."""
    renderer = create_renderer()
    player = Mock(spec=Player)

    renderer.set_player(player)

    assert renderer.player is player


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = create_renderer()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_player() -> None:
    """Rendering without a player should fail."""
    renderer = create_renderer()

    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_player_sprite() -> None:
    """Rendering should fail without a player sprite."""
    renderer = create_renderer()
    renderer.initialize()

    renderer.player = Mock(spec=Player)
    renderer.player_sprite_asset = None

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_with_valid_state() -> None:
    """Rendering should succeed with valid renderer state."""
    renderer = create_renderer()

    renderer.initialize()
    renderer.set_player(Mock(spec=Player))

    renderer.render()


def test_shutdown_resets_renderer() -> None:
    """Shutdown should clear renderer presentation state."""
    renderer = create_renderer()
    renderer.initialize()
    renderer.set_player(Mock(spec=Player))

    renderer.shutdown()

    assert renderer.is_initialized is False
    assert renderer.player_sprite_asset is None
