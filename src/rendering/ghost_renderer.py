"""Renderer responsible for drawing Pac-Man ghosts."""

from dataclasses import dataclass

from src.entities.ghost import Ghost
from src.rendering.renderer import Renderer


@dataclass
class GhostRenderer(Renderer):
    """Render a Pac-Man ghost."""

    ghost: Ghost | None = None
    is_initialized: bool = False

    def set_ghost(self, ghost: Ghost) -> None:
        """Set the ghost that should be rendered."""
        self.ghost = ghost

    def initialize(self) -> None:
        """Initialize the ghost renderer."""
        self.is_initialized = True

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

    def shutdown(self) -> None:
        """Shut down the ghost renderer."""
        self.is_initialized = False
