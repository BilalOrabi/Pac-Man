"""Power mode system for the Pac-Man game."""

from enum import Enum


class PowerModeState(Enum):
    """Represent the current power mode state."""

    INACTIVE = "inactive"
    ACTIVE = "active"


class PowerModeSystem:
    """Manage Pac-Man's temporary power mode."""

    def __init__(self, duration: float) -> None:
        """Initialize the power mode system.

        Args:
            duration: Duration of power mode in seconds.

        Raises:
            ValueError: If the duration is not positive.
        """
        if duration <= 0:
            raise ValueError("Power mode duration must be greater than zero.")

        self._duration = duration
        self._remaining_time = 0.0
        self._state = PowerModeState.INACTIVE

    @property
    def state(self) -> PowerModeState:
        """Return the current power mode state."""
        return self._state

    @property
    def remaining_time(self) -> float:
        """Return the remaining power mode duration."""
        return self._remaining_time

    @property
    def is_active(self) -> bool:
        """Return whether power mode is currently active."""
        return self._state == PowerModeState.ACTIVE

    def activate(self) -> None:
        """Activate or restart power mode."""
        self._remaining_time = self._duration
        self._state = PowerModeState.ACTIVE

    def update(self, elapsed_seconds: float) -> None:
        """Advance the power mode timer.

        Args:
            elapsed_seconds: Time elapsed since the previous update.

        Raises:
            ValueError: If elapsed_seconds is negative.
        """
        if elapsed_seconds < 0:
            raise ValueError("Elapsed time cannot be negative.")

        if not self.is_active:
            return

        self._remaining_time = max(
            0.0,
            self._remaining_time - elapsed_seconds,
        )

        if self._remaining_time == 0.0:
            self._state = PowerModeState.INACTIVE

    def deactivate(self) -> None:
        """Deactivate power mode immediately."""
        self._remaining_time = 0.0
        self._state = PowerModeState.INACTIVE
