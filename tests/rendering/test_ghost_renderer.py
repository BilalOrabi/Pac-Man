"""Tests for the Pac-Man ghost renderer."""

from unittest.mock import Mock

import pytest

from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.rendering.ghost_renderer import GhostRenderer
from src.theme.asset_manager import AssetManager


def create_ghost_renderer() -> GhostRenderer:
    """Create a ghost renderer for testing."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = True
    asset_manager.get_ghost_sprite.return_value = (
        "assets/images/ghost_red.png"
    )

    return GhostRenderer(
        asset_manager=asset_manager,
    )


def create_ghost(ghost_type: GhostType = GhostType.RED) -> Ghost:
    """Create a ghost for testing."""
    return Ghost(
        ghost_type=ghost_type,
        position=(1, 1),
        home_position=(2, 2),
        direction=Direction.NONE,
    )


def test_renderer_starts_uninitialized() -> None:
    """Ghost renderer should start uninitialized."""
    renderer = create_ghost_renderer()

    assert renderer.is_initialized is False
    assert renderer.ghost is None
    assert renderer.ghost_sprite_asset is None


def test_initialize_without_ghost() -> None:
    """Renderer should initialize without requiring a ghost."""
    renderer = create_ghost_renderer()

    renderer.initialize()

    assert renderer.is_initialized is True
    assert renderer.ghost_sprite_asset is None


def test_set_ghost_assigns_ghost() -> None:
    """Renderer should store the ghost."""
    renderer = create_ghost_renderer()
    ghost = create_ghost()

    renderer.set_ghost(ghost)

    assert renderer.ghost is ghost


def test_set_ghost_loads_sprite_when_initialized() -> None:
    """Setting a ghost after initialization should configure its sprite."""
    renderer = create_ghost_renderer()
    renderer.initialize()

    ghost = create_ghost(GhostType.RED)
    renderer.set_ghost(ghost)

    renderer.asset_manager.get_ghost_sprite.assert_called_once_with(
        GhostType.RED.value
    )

    assert (
        renderer.ghost_sprite_asset
        == "assets/images/ghost_red.png"
    )


def test_initialize_loads_sprite_for_assigned_ghost() -> None:
    """Initialization should configure the assigned ghost sprite."""
    renderer = create_ghost_renderer()
    ghost = create_ghost(GhostType.PINK)

    renderer.set_ghost(ghost)
    renderer.initialize()

    renderer.asset_manager.get_ghost_sprite.assert_called_once_with(
        GhostType.PINK.value
    )


def test_initialize_initializes_asset_manager_when_needed() -> None:
    """Renderer should initialize an uninitialized asset manager."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = False
    asset_manager.get_ghost_sprite.return_value = (
        "assets/images/ghost_blue.png"
    )

    renderer = GhostRenderer(
        asset_manager=asset_manager,
    )

    renderer.initialize()

    asset_manager.initialize.assert_called_once()
    assert renderer.is_initialized is True


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = create_ghost_renderer()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_ghost() -> None:
    """Rendering without a ghost should fail."""
    renderer = create_ghost_renderer()
    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_ghost_sprite() -> None:
    """Rendering should fail without a ghost sprite."""
    renderer = create_ghost_renderer()
    renderer.initialize()

    renderer.ghost = create_ghost()
    renderer.ghost_sprite_asset = None

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_with_valid_state() -> None:
    """Rendering should succeed with a valid ghost."""
    renderer = create_ghost_renderer()
    renderer.initialize()
    renderer.set_ghost(create_ghost())

    renderer.render()


def test_shutdown_resets_renderer() -> None:
    """Shutdown should clear renderer presentation state."""
    renderer = create_ghost_renderer()
    renderer.initialize()
    renderer.set_ghost(create_ghost())

    renderer.shutdown()

    assert renderer.is_initialized is False
    assert renderer.ghost_sprite_asset is None
