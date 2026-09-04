"""Renderer responsible for drawing the Pac-Man maze."""

from dataclasses import dataclass

from src.maze.maze import Maze
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class MazeRenderer(Renderer):
    """Render the maze using configured presentation assets."""

    asset_manager: AssetManager
    maze: Maze | None = None
    is_initialized: bool = False
    background_asset: str | None = None

    def set_maze(self, maze: Maze) -> None:
        """Set the maze that should be rendered."""
        self.maze = maze

    def initialize(self) -> None:
        """Initialize the maze renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.background_asset = self.asset_manager.get_background()
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

        if self.background_asset is None:
            raise RuntimeError(
                "Background asset must be configured before rendering."
            )

    def shutdown(self) -> None:
        """Shut down the maze renderer."""
        self.background_asset = None
        self.is_initialized = False
