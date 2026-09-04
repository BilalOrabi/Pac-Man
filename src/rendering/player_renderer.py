"""Renderer responsible for drawing Pac-Man."""

from dataclasses import dataclass

from src.entities.player import Player
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class PlayerRenderer(Renderer):
    """Render the Pac-Man player using configured presentation assets."""

    asset_manager: AssetManager
    player: Player | None = None
    is_initialized: bool = False
    player_sprite_asset: str | None = None

    def set_player(self, player: Player) -> None:
        """Set the player that should be rendered."""
        self.player = player

    def initialize(self) -> None:
        """Initialize the player renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.player_sprite_asset = (
            self.asset_manager.get_player_sprite()
        )
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

        if self.player_sprite_asset is None:
            raise RuntimeError(
                "Player sprite asset must be configured before rendering."
            )

    def shutdown(self) -> None:
        """Shut down the player renderer."""
        self.player_sprite_asset = None
        self.is_initialized = False
