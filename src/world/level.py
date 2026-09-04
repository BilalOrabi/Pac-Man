"""Domain model representing one playable Pac-Man level."""

from dataclasses import dataclass, field

from src.config.game_config import LevelConfig
from src.entities.ghost import Ghost
from src.entities.player import Player
from src.maze.maze import Coordinate, Maze


@dataclass
class Level:
    """Represent the runtime state of one game level."""

    number: int
    configuration: LevelConfig
    maze: Maze
    remaining_pacgums: int
    player: Player
    ghosts: list[Ghost]
    elapsed_level_time: float = 0.0
    completed: bool = False
    pacgums: set[Coordinate] = field(default_factory=set)
    super_pacgums: set[Coordinate] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Synchronize remaining_pacgums with pellet sets if provided."""
        if self.pacgums or self.super_pacgums:
            total_pellets = len(self.pacgums) + len(self.super_pacgums)
            self.remaining_pacgums = total_pellets

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

    def consume_pacgum_at(self, position: Coordinate) -> str | None:
        """Consume pellet at the specified coordinate and return its type."""
        if position in self.super_pacgums:
            self.super_pacgums.remove(position)
            self.consume_pacgum()
            if len(self.pacgums) == 0:
                self.completed = True
            return "super_pacgum"

        if position in self.pacgums:
            self.pacgums.remove(position)
            self.consume_pacgum()
            if len(self.pacgums) == 0:
                self.completed = True
            return "pacgum"

        return None

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
