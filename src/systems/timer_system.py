"""System responsible for managing Pac-Man level timers."""

from dataclasses import dataclass

from src.world.level import Level


@dataclass
class TimerSystem:
    """Manage elapsed time for the current game level."""

    maximum_level_time: float

    def __post_init__(self) -> None:
        """Validate the configured maximum level time."""
        if self.maximum_level_time <= 0:
            raise ValueError(
                "Maximum level time must be greater than zero."
            )

    def update(self, level: Level, elapsed_time: float) -> None:
        """Advance the level timer by the elapsed frame time.

        Args:
            level: Current game level.
            elapsed_time: Time elapsed since the previous update.

        Raises:
            ValueError: If elapsed_time is negative.
        """
        if elapsed_time < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        level.update_time(elapsed_time)

    def is_expired(self, level: Level) -> bool:
        """Return whether the level has reached its time limit."""
        return level.is_time_expired(self.maximum_level_time)

    def reset(self, level: Level) -> None:
        """Reset the level timer."""
        level.reset_timer()
