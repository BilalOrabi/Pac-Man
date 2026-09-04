"""Renderer responsible for drawing Pac-Man ghosts."""

from dataclasses import dataclass

from src.entities.ghost import Ghost
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class GhostRenderer(Renderer):
    """Render a Pac-Man ghost using configured presentation assets."""

    asset_manager: AssetManager
    ghost: Ghost | None = None
    is_initialized: bool = False
    ghost_sprite_asset: str | None = None

    def set_ghost(self, ghost: Ghost) -> None:
        """Set the ghost that should be rendered."""
        self.ghost = ghost

        if self.is_initialized:
            self.ghost_sprite_asset = (
                self.asset_manager.get_ghost_sprite(
                    ghost.ghost_type.value
                )
            )

    def initialize(self) -> None:
        """Initialize the ghost renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.is_initialized = True

        if self.ghost is not None:
            self.ghost_sprite_asset = (
                self.asset_manager.get_ghost_sprite(
                    self.ghost.ghost_type.value
                )
            )

    def render(self) -> None:
        """Render the currently assigned ghost."""
        if not self.is_initialized:
            raise RuntimeError(
                "GhostRenderer must be initialized before rendering."
            )

        if self.ghost is None:
            raise RuntimeError(
                "Ghost must be assigned before rendering."
            )

        if self.ghost_sprite_asset is None:
            raise RuntimeError(
                "Ghost sprite asset must be configured before rendering."
            )

    def shutdown(self) -> None:
        """Shut down the ghost renderer."""
        self.ghost_sprite_asset = None
        self.is_initialized = False
