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

    def set_level(self, level: Level) -> None:
        """Provide the current level to the maze renderer."""
        self.maze_renderer.set_maze(level.maze)

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
