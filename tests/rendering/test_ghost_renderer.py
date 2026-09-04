"""Tests for the Pac-Man ghost renderer."""

import pytest

from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.rendering.ghost_renderer import GhostRenderer


def create_test_ghost() -> Ghost:
    """Create a ghost for renderer tests."""
    return Ghost(
        ghost_type=GhostType.RED,
        position=(2, 2),
        home_position=(2, 2),
        direction=Direction.LEFT,
    )


def test_ghost_renderer_starts_uninitialized() -> None:
    """GhostRenderer should initially be uninitialized."""
    renderer = GhostRenderer()

    assert renderer.is_initialized is False
    assert renderer.ghost is None


def test_initialize_initializes_renderer() -> None:
    """Initialize should activate the renderer."""
    renderer = GhostRenderer()

    renderer.initialize()

    assert renderer.is_initialized is True


def test_set_ghost_assigns_ghost() -> None:
    """The renderer should store the ghost to be rendered."""
    renderer = GhostRenderer()
    ghost = create_test_ghost()

    renderer.set_ghost(ghost)

    assert renderer.ghost is ghost


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = GhostRenderer()
    renderer.set_ghost(create_test_ghost())

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_ghost() -> None:
    """Rendering without a ghost should fail."""
    renderer = GhostRenderer()
    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_when_initialized_with_ghost() -> None:
    """Rendering should succeed with a valid initialized renderer."""
    renderer = GhostRenderer()
    renderer.initialize()
    renderer.set_ghost(create_test_ghost())

    renderer.render()


def test_shutdown_deactivates_renderer() -> None:
    """Shutdown should deactivate the renderer."""
    renderer = GhostRenderer()
    renderer.initialize()

    renderer.shutdown()

    assert renderer.is_initialized is False
