"""Renderer responsible for drawing Pac-Man."""

from dataclasses import dataclass

from src.entities.player import Player
from src.rendering.renderer import Renderer


@dataclass
class PlayerRenderer(Renderer):
    """Render the Pac-Man player."""

    player: Player | None = None
    is_initialized: bool = False

    def set_player(self, player: Player) -> None:
        """Set the player that should be rendered."""
        self.player = player

    def initialize(self) -> None:
        """Initialize the player renderer."""
        self.is_initialized = True

    def render(self) -> None:
        """Render the currently assigned player."""
        if not self.is_initialized:
            raise RuntimeError(
                "PlayerRenderer must be initialized before rendering."
            )

        if self.player is None:
            raise RuntimeError(
                "Player must be assigned before rendering."
            )

    def shutdown(self) -> None:
        """Shut down the player renderer."""
        self.is_initialized = False
