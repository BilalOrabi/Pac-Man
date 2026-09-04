"""Animation support for the Pac-Man presentation layer."""

from dataclasses import dataclass


@dataclass
class Animation:
    """Represent a time-based presentation animation."""

    duration: float
    elapsed_time: float = 0.0
    is_finished: bool = False

    def __post_init__(self) -> None:
        """Validate animation configuration."""
        if self.duration <= 0:
            raise ValueError(
                "Animation duration must be greater than zero."
            )

    @property
    def progress(self) -> float:
        """Return animation progress between zero and one."""
        if self.is_finished:
            return 1.0

        return min(
            self.elapsed_time / self.duration,
            1.0,
        )

    def update(self, elapsed_seconds: float) -> None:
        """Advance the animation by the elapsed time."""
        if elapsed_seconds < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        if self.is_finished:
            return

        self.elapsed_time += elapsed_seconds

        if self.elapsed_time >= self.duration:
            self.elapsed_time = self.duration
            self.is_finished = True

    def reset(self) -> None:
        """Reset the animation to its initial state."""
        self.elapsed_time = 0.0
        self.is_finished = False
