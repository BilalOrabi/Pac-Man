"""Visual effect abstractions for the Pac-Man presentation layer."""

from dataclasses import dataclass

from src.rendering.animation import Animation


@dataclass
class VisualEffect:
    """Represent a time-based visual effect."""

    name: str
    animation: Animation
    is_enabled: bool = True

    def __post_init__(self) -> None:
        """Validate the visual effect configuration."""
        if not self.name.strip():
            raise ValueError(
                "Effect name cannot be empty."
            )

    @property
    def is_finished(self) -> bool:
        """Return whether the effect has completed."""
        return self.animation.is_finished

    @property
    def progress(self) -> float:
        """Return the current effect progress."""
        return self.animation.progress

    def update(self, elapsed_seconds: float) -> None:
        """Update the effect animation."""
        if not self.is_enabled:
            return

        self.animation.update(elapsed_seconds)

    def enable(self) -> None:
        """Enable the visual effect."""
        self.is_enabled = True

    def disable(self) -> None:
        """Disable the visual effect."""
        self.is_enabled = False

    def reset(self) -> None:
        """Reset the effect animation."""
        self.animation.reset()

    def restart(self) -> None:
        """Enable and restart the effect."""
        self.is_enabled = True
        self.animation.reset()
