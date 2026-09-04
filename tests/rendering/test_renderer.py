"""Tests for the Pac-Man renderer interface."""

import pytest

from src.rendering.renderer import Renderer


class ConcreteRenderer(Renderer):
    """Concrete renderer used for testing the abstract interface."""

    def __init__(self) -> None:
        self.initialize_called = False
        self.render_called = False
        self.shutdown_called = False

    def initialize(self) -> None:
        """Record renderer initialization."""
        self.initialize_called = True

    def render(self) -> None:
        """Record a render call."""
        self.render_called = True

    def shutdown(self) -> None:
        """Record renderer shutdown."""
        self.shutdown_called = True


def test_renderer_is_abstract() -> None:
    """Renderer should not be directly instantiable."""
    with pytest.raises(TypeError):
        Renderer()  # type: ignore[abstract]


def test_renderer_initialize() -> None:
    """A renderer should support initialization."""
    renderer = ConcreteRenderer()

    renderer.initialize()

    assert renderer.initialize_called is True


def test_renderer_render() -> None:
    """A renderer should support rendering."""
    renderer = ConcreteRenderer()

    renderer.render()

    assert renderer.render_called is True


def test_renderer_shutdown() -> None:
    """A renderer should support shutdown."""
    renderer = ConcreteRenderer()

    renderer.shutdown()

    assert renderer.shutdown_called is True
