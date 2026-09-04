"""Tests for the Pac-Man maze renderer."""

import pytest

from src.maze.maze import Maze, MazeCell, Wall
from src.rendering.maze_renderer import MazeRenderer


def create_test_maze() -> Maze:
    """Create a small maze for renderer tests."""
    cells = tuple(
        tuple(
            MazeCell(
                position=(x, y),
                walls=Wall.NONE,
                is_solid_block=False,
            )
            for x in range(2)
        )
        for y in range(2)
    )

    return Maze(
        width=2,
        height=2,
        cells=cells,
        entry=(0, 0),
        exit=(1, 1),
        shortest_path="",
    )


def test_maze_renderer_starts_uninitialized() -> None:
    """MazeRenderer should initially be uninitialized."""
    renderer = MazeRenderer()

    assert renderer.is_initialized is False
    assert renderer.maze is None


def test_initialize_initializes_renderer() -> None:
    """Initialize should activate the renderer."""
    renderer = MazeRenderer()

    renderer.initialize()

    assert renderer.is_initialized is True


def test_set_maze_assigns_maze() -> None:
    """The renderer should store the maze to be rendered."""
    renderer = MazeRenderer()
    maze = create_test_maze()

    renderer.set_maze(maze)

    assert renderer.maze is maze


def test_render_requires_initialization() -> None:
    """Rendering before initialization should fail."""
    renderer = MazeRenderer()
    renderer.set_maze(create_test_maze())

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_requires_maze() -> None:
    """Rendering without a maze should fail."""
    renderer = MazeRenderer()
    renderer.initialize()

    with pytest.raises(RuntimeError):
        renderer.render()


def test_render_succeeds_when_initialized_with_maze() -> None:
    """Rendering should succeed with a valid initialized renderer."""
    renderer = MazeRenderer()
    renderer.initialize()
    renderer.set_maze(create_test_maze())

    renderer.render()


def test_shutdown_deactivates_renderer() -> None:
    """Shutdown should deactivate the renderer."""
    renderer = MazeRenderer()
    renderer.initialize()

    renderer.shutdown()

    assert renderer.is_initialized is False
