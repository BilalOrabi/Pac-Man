"""Renderer responsible for drawing the Pac-Man maze."""

from dataclasses import dataclass

from src.maze.maze import Maze
from src.rendering.renderer import Renderer


@dataclass
class MazeRenderer(Renderer):
    """Render the maze using a rendering backend."""

    maze: Maze | None = None
    is_initialized: bool = False

    def set_maze(self, maze: Maze) -> None:
        """Set the maze that should be rendered."""
        self.maze = maze

    def initialize(self) -> None:
        """Initialize the maze renderer."""
        self.is_initialized = True

    def render(self) -> None:
        """Render the currently assigned maze."""
        if not self.is_initialized:
            raise RuntimeError(
                "MazeRenderer must be initialized before rendering."
            )

        if self.maze is None:
            raise RuntimeError(
                "Maze must be assigned before rendering."
            )

    def shutdown(self) -> None:
        """Shut down the maze renderer."""
        self.is_initialized = False
