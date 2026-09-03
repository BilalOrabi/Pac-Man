"""Domain model representing one playable Pac-Man level."""

from dataclasses import dataclass

from src.config.game_config import LevelConfig
from src.maze.maze import Maze


@dataclass
class Level:
    """Represent the runtime state of one game level."""

    number: int
    configuration: LevelConfig
    maze: Maze
    remaining_pacgums: int
    elapsed_level_time: float = 0.0
    completed: bool = False

    def update_time(self, elapsed_time: float) -> None:
        """Advance the level timer."""
        if elapsed_time < 0:
            raise ValueError("Elapsed time cannot be negative.")

        if not self.completed:
            self.elapsed_level_time += elapsed_time

    def consume_pacgum(self) -> None:
        """Register one consumed pacgum."""
        if self.remaining_pacgums <= 0:
            return

        self.remaining_pacgums -= 1

        if self.remaining_pacgums == 0:
            self.completed = True

    def is_time_expired(self, maximum_level_time: float) -> bool:
        """Return whether the level time limit has been reached."""
        if maximum_level_time <= 0:
            raise ValueError(
                "Maximum level time must be greater than zero."
            )

        return self.elapsed_level_time >= maximum_level_time

    def reset_timer(self) -> None:
        """Reset the level timer to zero."""
        self.elapsed_level_time = 0.0
