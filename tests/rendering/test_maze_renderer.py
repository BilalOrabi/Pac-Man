"""Tests for the Pac-Man maze renderer."""

from unittest.mock import Mock

import pytest

from src.maze.maze import Maze
from src.rendering.maze_renderer import MazeRenderer
from src.theme.asset_manager import AssetManager


def create_renderer() -> MazeRenderer:
    """Create an initialized maze renderer for testing."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = True
    asset_manager.get_background.return_value = (
        "assets/images/background.png"
    )

    return MazeRenderer(
        asset_manager=asset_manager,
    )


def test_renderer_starts_uninitialized() -> None:
    """Maze renderer should start uninitialized."""
    renderer = create_renderer()

    assert renderer.is_initialized is False
    assert renderer.maze is None
    assert renderer.background_asset is None


def test_initialize_loads_background_asset() -> None:
    """Initialization should configure the background asset."""
    renderer = create_renderer()

    renderer.initialize()

    assert renderer.is_initialized is True
    assert (
        renderer.background_asset
        == "assets/images/background.png"
    )


def test_initialize_initializes_asset_manager_when_needed() -> None:
    """Renderer should initialize an uninitialized asset manager."""
    asset_manager = Mock(spec=AssetManager)
    asset_manager.is_initialized = False
    asset_manager.get_background.return_value = (
        "assets/images/background.png"
    )

    renderer = MazeRenderer(
        asset_manager=asset_manager,
    )

    renderer.initialize()

    asset_manager.initialize.assert_called_once()
    asset_manager.get_background.assert_called_once()
    assert renderer.is_initialized is True


def test_set_maze_assigns_maze() -> None:
    """Renderer should store the maze to be rendered."""
    renderer = create_renderer()
    maze = Mock(spec=Maze)

    renderer.set_maze(maze)

    assert renderer.maze is maze


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = create_renderer()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_maze() -> None:
    """Rendering without a maze should fail."""
    renderer = create_renderer()

    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_background_asset() -> None:
    """Rendering should fail when no background asset is configured."""
    renderer = create_renderer()
    renderer.initialize()

    renderer.background_asset = None
    renderer.maze = Mock(spec=Maze)

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_with_initialized_renderer_and_maze() -> None:
    """Rendering should succeed with valid renderer state."""
    renderer = create_renderer()
    renderer.initialize()
    renderer.set_maze(Mock(spec=Maze))

    renderer.render()


def test_shutdown_resets_renderer() -> None:
    """Shutdown should clear renderer state."""
    renderer = create_renderer()
    renderer.initialize()
    renderer.set_maze(Mock(spec=Maze))

    renderer.shutdown()

    assert renderer.is_initialized is False
    assert renderer.background_asset is None
