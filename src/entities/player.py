"""Player entity for the Pac-Man game."""

from dataclasses import dataclass

from src.entities.direction import Direction
from src.entities.entity import Entity
from src.maze import Coordinate


@dataclass
class Player(Entity):
    """Represent Pac-Man and its gameplay-related state."""

    lives: int = 3
    score: int = 0
    is_powered_up: bool = False

    @staticmethod
    def _validate_points(points: int) -> None:
        """Ensure points being added to the player score are non-negative."""
        if points < 0:
            raise ValueError("Score points cannot be negative.")

    @staticmethod
    def _validate_remaining_lives(lives: int) -> None:
        """Ensure the player has at least one remaining life to deduct."""
        if lives <= 0:
            raise ValueError("Player has no remaining lives.")

    def add_score(self, points: int) -> None:
        """Increase the player's score by the specified number of points."""
        self._validate_points(points)
        self.score += points

    def lose_life(self) -> None:
        """Remove one life from the player."""
        self._validate_remaining_lives(self.lives)
        self.lives -= 1

    def activate_power_mode(self) -> None:
        """Activate the player's power mode."""
        self.is_powered_up = True

    def deactivate_power_mode(self) -> None:
        """Deactivate the player's power mode."""
        self.is_powered_up = False

    def reset_position(self, position: Coordinate) -> None:
        """Move the player back to a specified position."""
        self.position = position
        self.direction = Direction.NONE
        self.target_position = None
        self.movement_progress = 0.0
