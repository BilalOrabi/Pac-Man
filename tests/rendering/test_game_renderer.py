"""Tests for the central Pac-Man game renderer."""

from unittest.mock import Mock

import pytest

from src.rendering.game_renderer import GameRenderer
from src.rendering.ghost_renderer import GhostRenderer
from src.rendering.maze_renderer import MazeRenderer
from src.rendering.player_renderer import PlayerRenderer
from src.rendering.ui_renderer import UIRenderer


def create_game_renderer() -> GameRenderer:
    """Create a game renderer with mocked child renderers."""
    return GameRenderer(
        maze_renderer=Mock(spec=MazeRenderer),
        player_renderer=Mock(spec=PlayerRenderer),
        ghost_renderers=[
            Mock(spec=GhostRenderer),
            Mock(spec=GhostRenderer),
            Mock(spec=GhostRenderer),
            Mock(spec=GhostRenderer),
        ],
        ui_renderer=Mock(spec=UIRenderer),
    )


def test_renderer_starts_uninitialized() -> None:
    """The game renderer should start uninitialized."""
    game_renderer = create_game_renderer()

    assert game_renderer.is_initialized is False


def test_initialize_initializes_all_renderers() -> None:
    """Initialization should initialize every child renderer."""
    game_renderer = create_game_renderer()

    game_renderer.initialize()

    game_renderer.maze_renderer.initialize.assert_called_once()
    game_renderer.player_renderer.initialize.assert_called_once()

    for ghost_renderer in game_renderer.ghost_renderers:
        ghost_renderer.initialize.assert_called_once()

    game_renderer.ui_renderer.initialize.assert_called_once()

    assert game_renderer.is_initialized is True


def test_render_requires_initialization() -> None:
    """Rendering should fail before initialization."""
    game_renderer = create_game_renderer()

    with pytest.raises(RuntimeError, match="must be initialized"):
        game_renderer.render()


def test_render_calls_all_renderers() -> None:
    """Rendering should render every presentation component."""
    game_renderer = create_game_renderer()

    game_renderer.initialize()
    game_renderer.render()

    game_renderer.maze_renderer.render.assert_called_once()
    game_renderer.player_renderer.render.assert_called_once()

    for ghost_renderer in game_renderer.ghost_renderers:
        ghost_renderer.render.assert_called_once()

    game_renderer.ui_renderer.render.assert_called_once()


def test_shutdown_shuts_down_all_renderers() -> None:
    """Shutdown should shut down every child renderer."""
    game_renderer = create_game_renderer()

    game_renderer.initialize()
    game_renderer.shutdown()

    game_renderer.maze_renderer.shutdown.assert_called_once()
    game_renderer.player_renderer.shutdown.assert_called_once()

    for ghost_renderer in game_renderer.ghost_renderers:
        ghost_renderer.shutdown.assert_called_once()

    game_renderer.ui_renderer.shutdown.assert_called_once()

    assert game_renderer.is_initialized is False


def test_shutdown_does_not_require_initialization() -> None:
    """Shutdown should be safe even when the renderer is uninitialized."""
    game_renderer = create_game_renderer()

    game_renderer.shutdown()

    game_renderer.maze_renderer.shutdown.assert_called_once()
    game_renderer.player_renderer.shutdown.assert_called_once()

    for ghost_renderer in game_renderer.ghost_renderers:
        ghost_renderer.shutdown.assert_called_once()

    game_renderer.ui_renderer.shutdown.assert_called_once()

    assert game_renderer.is_initialized is False
