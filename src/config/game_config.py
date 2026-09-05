"""Typed configuration models for the Pac-Man game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    """Configuration for a single game level."""

    width: int
    height: int

    def __post_init__(self) -> None:
        """Validate level dimensions."""
        if self.width <= 0:
            raise ValueError(
                "Level width must be greater than zero."
            )

        if self.height <= 0:
            raise ValueError(
                "Level height must be greater than zero."
            )


@dataclass(frozen=True)
class GameConfig:
    """Validated configuration for the Pac-Man game."""

    highscore_filename: str
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int

    player_speed: float
    ghost_speed: float
    frightened_ghost_speed: float
    returning_ghost_speed: float
    power_mode_duration: float

    levels: tuple[LevelConfig, ...]

    def _validate_score_and_lives(self) -> None:
        """Validate highscore filename, lives, pellets, and points."""
        if not self.highscore_filename.strip():
            raise ValueError("Highscore filename cannot be empty.")
        if self.lives <= 0:
            raise ValueError("Lives must be greater than zero.")
        if self.pacgum < 0:
            raise ValueError("Pacgum count cannot be negative.")
        if self.points_per_pacgum < 0:
            raise ValueError("Pacgum points cannot be negative.")
        if self.points_per_super_pacgum < 0:
            raise ValueError("Super pacgum points cannot be negative.")
        if self.points_per_ghost < 0:
            raise ValueError("Ghost points cannot be negative.")
        if self.level_max_time <= 0:
            raise ValueError("Level maximum time must be greater than zero.")

    def _validate_speeds(self) -> None:
        """Validate player, ghost speeds, and power mode duration."""
        if self.player_speed <= 0:
            raise ValueError("Player speed must be greater than zero.")
        if self.ghost_speed <= 0:
            raise ValueError("Ghost speed must be greater than zero.")
        if self.frightened_ghost_speed <= 0:
            raise ValueError(
                "Frightened ghost speed must be greater than zero."
            )
        if self.returning_ghost_speed <= 0:
            raise ValueError(
                "Returning ghost speed must be greater than zero."
            )
        if self.power_mode_duration <= 0:
            raise ValueError("Power mode duration must be greater than zero.")

    def _validate_levels(self) -> None:
        """Validate level configuration collection."""
        if not self.levels:
            raise ValueError("At least one level must be configured.")

    def __post_init__(self) -> None:
        """Validate game configuration values."""
        self._validate_score_and_lives()
        self._validate_speeds()
        self._validate_levels()
