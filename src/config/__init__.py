"""Configuration package for the Pac-Man game."""

from src.config.config_loader import ConfigError, ConfigLoader
from src.config.game_config import GameConfig, LevelConfig

__all__ = [
    "ConfigError",
    "ConfigLoader",
    "GameConfig",
    "LevelConfig",
]
