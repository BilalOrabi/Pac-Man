"""Central renderer coordinating the Pac-Man presentation layer."""

from dataclasses import dataclass

from src.entities.ghost import Ghost
from src.entities.player import Player
from src.rendering.ghost_renderer import GhostRenderer
from src.rendering.maze_renderer import MazeRenderer
from src.rendering.player_renderer import PlayerRenderer
from src.rendering.ui_renderer import UIRenderer
from src.world.level import Level


@dataclass
class GameRenderer:
    """Coordinate all renderers used by the Pac-Man application."""

    maze_renderer: MazeRenderer
    player_renderer: PlayerRenderer
    ghost_renderers: list[GhostRenderer]
    ui_renderer: UIRenderer
    is_initialized: bool = False

    def initialize(self) -> None:
        """Initialize every presentation renderer."""
        self.maze_renderer.initialize()
        self.player_renderer.initialize()

        for ghost_renderer in self.ghost_renderers:
            ghost_renderer.initialize()

        self.ui_renderer.initialize()

        self.is_initialized = True

    def _recompute_layout(self, surface: object, maze: object) -> None:
        """Calculate and apply scaled cell size and centering offsets."""
        if hasattr(surface, "get_width") and maze is not None:
            w = getattr(surface, "get_width")()
            h = getattr(surface, "get_height")()
            mw = getattr(maze, "width", 19)
            mh = getattr(maze, "height", 21)
            cell_size = min((w - 100) // mw, (h - 120) // mh, 36)
            offset_x = (w - mw * cell_size) // 2
            offset_y = 50 + (h - 50 - mh * cell_size) // 2
            self.configure_layout(cell_size, offset_x, offset_y)

    def set_surface(self, surface: object) -> None:
        """Propagate the presentation surface to child renderers."""
        self.maze_renderer.surface = surface
        self.player_renderer.surface = surface
        for ghost_renderer in self.ghost_renderers:
            ghost_renderer.surface = surface
        self.ui_renderer.surface = surface

        maze = getattr(self.maze_renderer, "maze", None)
        self._recompute_layout(surface, maze)

    def configure_layout(
        self,
        cell_size: int,
        offset_x: int,
        offset_y: int,
    ) -> None:
        """Propagate cell size and positioning to spatial renderers."""
        self.maze_renderer.cell_size = cell_size
        self.maze_renderer.offset_x = offset_x
        self.maze_renderer.offset_y = offset_y

        self.player_renderer.cell_size = cell_size
        self.player_renderer.offset_x = offset_x
        self.player_renderer.offset_y = offset_y

        for ghost_renderer in self.ghost_renderers:
            ghost_renderer.cell_size = cell_size
            ghost_renderer.offset_x = offset_x
            ghost_renderer.offset_y = offset_y

    def set_level(self, level: Level) -> None:
        """Provide the current level to the maze renderer."""
        self.maze_renderer.set_maze(level.maze)
        self.maze_renderer.level = level
        self.set_player(level.player)
        self.set_ghosts(level.ghosts)

        surface = getattr(self.maze_renderer, "surface", None)
        self._recompute_layout(surface, level.maze)

    def set_player(self, player: Player) -> None:
        """Provide the current player to the player renderer."""
        self.player_renderer.set_player(player)

    def set_ghosts(self, ghosts: list[Ghost]) -> None:
        """Provide the current ghosts to their renderers."""
        if len(ghosts) != len(self.ghost_renderers):
            raise ValueError(
                "Number of ghosts must match the number of ghost renderers."
            )

        for ghost_renderer, ghost in zip(
            self.ghost_renderers,
            ghosts,
        ):
            ghost_renderer.set_ghost(ghost)

    def render(self) -> None:
        """Render one complete game frame."""
        if not self.is_initialized:
            raise RuntimeError(
                "GameRenderer must be initialized before rendering."
            )

        self.maze_renderer.render()
        self.player_renderer.render()

        for ghost_renderer in self.ghost_renderers:
            ghost_renderer.render()

        self.ui_renderer.render()

    def shutdown(self) -> None:
        """Shut down every presentation renderer."""
        self.maze_renderer.shutdown()
        self.player_renderer.shutdown()

        for ghost_renderer in self.ghost_renderers:
            ghost_renderer.shutdown()

        self.ui_renderer.shutdown()

        self.is_initialized = False
