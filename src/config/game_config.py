"""Typed configuration models for the Pac-Man game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    """Configuration for a single game level."""

    width: int
    height: int


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
    levels: tuple[LevelConfig, ...]
