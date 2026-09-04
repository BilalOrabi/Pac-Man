"""Base renderer interface for the Pac-Man application."""

from abc import ABC, abstractmethod


class Renderer(ABC):
    """Define the interface for rendering the Pac-Man game."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the rendering system."""
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        """Render the current game frame."""
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """Shut down the rendering system."""
        raise NotImplementedError
