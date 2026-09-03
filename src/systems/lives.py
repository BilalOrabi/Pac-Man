"""Lives management system for the Pac-Man game."""


class LivesSystem:
    """Manage the player's remaining lives."""

    def __init__(self, starting_lives: int) -> None:
        """Initialize the lives system."""
        if starting_lives <= 0:
            raise ValueError("Starting lives must be greater than zero.")

        self._remaining_lives = starting_lives

    @property
    def remaining_lives(self) -> int:
        """Return the number of lives currently remaining."""
        return self._remaining_lives

    @property
    def is_alive(self) -> bool:
        """Return whether the player still has at least one life."""
        return self._remaining_lives > 0

    def lose_life(self) -> bool:
        """Remove one life and return whether any lives remain.

        Returns:
            True if the player still has lives remaining, otherwise False.
        """
        if self._remaining_lives > 0:
            self._remaining_lives -= 1

        return self.is_alive

    def add_life(self) -> None:
        """Add one life."""
        self._remaining_lives += 1

    def reset(self, starting_lives: int) -> None:
        """Reset the number of lives.

        Args:
            starting_lives: Number of lives after the reset.

        Raises:
            ValueError: If starting_lives is not positive.
        """
        if starting_lives <= 0:
            raise ValueError("Starting lives must be greater than zero.")

        self._remaining_lives = starting_lives
