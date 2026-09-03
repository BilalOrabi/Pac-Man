"""Load and validate Pac-Man game configuration from JSON."""

import json
from pathlib import Path
from typing import Any

from src.config.game_config import GameConfig, LevelConfig


class ConfigError(Exception):
    """Raised when the game configuration is invalid."""


class ConfigLoader:
    """Load and validate configuration files for the Pac-Man game."""

    @staticmethod
    def load(path: str | Path) -> GameConfig:
        """Load a configuration file and return a validated GameConfig.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            A validated GameConfig instance.

        Raises:
            ConfigError: If the file cannot be read or contains
                invalid configuration.
        """
        config_path = Path(path)

        data = ConfigLoader._read_json(config_path)

        return ConfigLoader._build_config(data)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        """Read and decode a JSON configuration file."""
        if not path.is_file():
            raise ConfigError(f"Configuration file not found: {path}")

        try:
            with path.open("r", encoding="utf-8") as file:
                data: Any = json.load(file)
        except OSError as exc:
            raise ConfigError(
                f"Unable to read configuration file: {path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Invalid JSON in configuration file: {path}"
            ) from exc

        if not isinstance(data, dict):
            raise ConfigError("Configuration root must be a JSON object.")

        return data

    @staticmethod
    def _build_config(data: dict[str, Any]) -> GameConfig:
        """Validate raw configuration and build the domain model."""
        return GameConfig(
            highscore_filename=ConfigLoader._get_string(
                data,
                "highscore_filename",
            ),
            lives=ConfigLoader._get_positive_int(data, "lives"),
            pacgum=ConfigLoader._get_non_negative_int(data, "pacgum"),
            points_per_pacgum=ConfigLoader._get_non_negative_int(
                data,
                "points_per_pacgum",
            ),
            points_per_super_pacgum=ConfigLoader._get_non_negative_int(
                data,
                "points_per_super_pacgum",
            ),
            points_per_ghost=ConfigLoader._get_non_negative_int(
                data,
                "points_per_ghost",
            ),
            seed=ConfigLoader._get_int(data, "seed"),
            level_max_time=ConfigLoader._get_positive_int(
                data,
                "level_max_time",
            ),
            levels=ConfigLoader._get_levels(data),
        )

    @staticmethod
    def _get_string(data: dict[str, Any], key: str) -> str:
        """Get a required string configuration value."""
        value = data.get(key)

        if not isinstance(value, str) or not value.strip():
            raise ConfigError(
                f"Configuration '{key}' must be a non-empty string."
            )

        return value

    @staticmethod
    def _get_int(data: dict[str, Any], key: str) -> int:
        """Get a required integer configuration value."""
        value = data.get(key)

        if isinstance(value, bool) or not isinstance(value, int):
            raise ConfigError(
                f"Configuration '{key}' must be an integer."
            )

        return value

    @staticmethod
    def _get_positive_int(data: dict[str, Any], key: str) -> int:
        """Get a required positive integer configuration value."""
        value = ConfigLoader._get_int(data, key)

        if value <= 0:
            raise ConfigError(
                f"Configuration '{key}' must be greater than zero."
            )

        return value

    @staticmethod
    def _get_non_negative_int(
        data: dict[str, Any],
        key: str,
    ) -> int:
        """Get a required non-negative integer configuration value."""
        value = ConfigLoader._get_int(data, key)

        if value < 0:
            raise ConfigError(
                f"Configuration '{key}' cannot be negative."
            )

        return value

    @staticmethod
    def _get_levels(data: dict[str, Any]) -> tuple[LevelConfig, ...]:
        """Validate and build all configured levels."""
        raw_levels = data.get("levels")

        if not isinstance(raw_levels, list):
            raise ConfigError(
                "Configuration 'levels' must be a list."
            )

        if not raw_levels:
            raise ConfigError(
                "Configuration 'levels' must contain at least one level."
            )

        levels: list[LevelConfig] = []

        for index, raw_level in enumerate(raw_levels):
            if not isinstance(raw_level, dict):
                raise ConfigError(
                    f"Level {index} must be a JSON object."
                )

            width = ConfigLoader._get_positive_int(
                raw_level,
                "width",
            )
            height = ConfigLoader._get_positive_int(
                raw_level,
                "height",
            )

            levels.append(
                LevelConfig(
                    width=width,
                    height=height,
                )
            )

        return tuple(levels)
