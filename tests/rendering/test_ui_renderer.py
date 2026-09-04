"""Tests for the Pac-Man user-interface renderer."""

from unittest.mock import Mock

import pytest

from src.rendering.ui_renderer import UIRenderer
from src.theme.asset_manager import AssetManager


def create_renderer() -> UIRenderer:
    """Create a UI renderer for testing."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = True
    asset_manager.get_font.side_effect = {
        "menu": "assets/fonts/menu.ttf",
        "game": "assets/fonts/game.ttf",
    }.__getitem__

    return UIRenderer(
        asset_manager=asset_manager,
    )


def test_renderer_starts_uninitialized() -> None:
    """UI renderer should start uninitialized."""
    renderer = create_renderer()

    assert renderer.is_initialized is False
    assert renderer.score == 0
    assert renderer.lives == 0
    assert renderer.level_number == 1
    assert renderer.message == ""


def test_initialize_loads_ui_fonts() -> None:
    """Initialization should configure both UI fonts."""
    renderer = create_renderer()

    renderer.initialize()

    assert renderer.is_initialized is True
    assert renderer.menu_font_asset == "assets/fonts/menu.ttf"
    assert renderer.game_font_asset == "assets/fonts/game.ttf"

    renderer.asset_manager.get_font.assert_any_call("menu")
    renderer.asset_manager.get_font.assert_any_call("game")


def test_initialize_initializes_asset_manager_when_needed() -> None:
    """Renderer should initialize an uninitialized asset manager."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = False
    asset_manager.get_font.side_effect = {
        "menu": "assets/fonts/menu.ttf",
        "game": "assets/fonts/game.ttf",
    }.__getitem__

    renderer = UIRenderer(
        asset_manager=asset_manager,
    )

    renderer.initialize()

    asset_manager.initialize.assert_called_once()


def test_set_score() -> None:
    """Renderer should update the displayed score."""
    renderer = create_renderer()

    renderer.set_score(500)

    assert renderer.score == 500


def test_negative_score_is_rejected() -> None:
    """Negative scores should be rejected."""
    renderer = create_renderer()

    with pytest.raises(ValueError):
        renderer.set_score(-1)


def test_set_lives() -> None:
    """Renderer should update the displayed lives."""
    renderer = create_renderer()

    renderer.set_lives(3)

    assert renderer.lives == 3


def test_negative_lives_are_rejected() -> None:
    """Negative lives should be rejected."""
    renderer = create_renderer()

    with pytest.raises(ValueError):
        renderer.set_lives(-1)


def test_set_level_number() -> None:
    """Renderer should update the displayed level number."""
    renderer = create_renderer()

    renderer.set_level_number(4)

    assert renderer.level_number == 4


def test_invalid_level_number_is_rejected() -> None:
    """Non-positive level numbers should be rejected."""
    renderer = create_renderer()

    with pytest.raises(ValueError):
        renderer.set_level_number(0)


def test_set_message() -> None:
    """Renderer should update the displayed message."""
    renderer = create_renderer()

    renderer.set_message("READY!")

    assert renderer.message == "READY!"


def test_non_string_message_is_rejected() -> None:
    """Messages must be strings."""
    renderer = create_renderer()

    with pytest.raises(TypeError):
        renderer.set_message(123)  # type: ignore[arg-type]


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = create_renderer()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_menu_font() -> None:
    """Rendering should fail without the menu font."""
    renderer = create_renderer()
    renderer.initialize()
    renderer.menu_font_asset = None

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_game_font() -> None:
    """Rendering should fail without the game font."""
    renderer = create_renderer()
    renderer.initialize()
    renderer.game_font_asset = None

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_with_valid_state() -> None:
    """Rendering should succeed after initialization."""
    renderer = create_renderer()

    renderer.initialize()
    renderer.set_score(100)
    renderer.set_lives(3)
    renderer.set_level_number(1)
    renderer.set_message("READY!")

    renderer.render()


def test_shutdown_resets_renderer() -> None:
    """Shutdown should clear renderer presentation assets."""
    renderer = create_renderer()
    renderer.initialize()

    renderer.shutdown()

    assert renderer.is_initialized is False
    assert renderer.menu_font_asset is None
    assert renderer.game_font_asset is None
