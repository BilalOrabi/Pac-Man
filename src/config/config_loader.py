"""Load and validate Pac-Man game configuration from JSON."""

import json
from pathlib import Path
import sys
from typing import Any

from src.config.game_config import GameConfig, LevelConfig


class ConfigError(Exception):
    """Raised when the game configuration is invalid."""


class ConfigLoader:
    """Load and validate configuration files for the Pac-Man game."""

    DEFAULT_HIGHSCORE_FILENAME = "highscores.json"
    DEFAULT_LIVES = 3
    DEFAULT_PACGUM = 42
    DEFAULT_POINTS_PER_PACGUM = 10
    DEFAULT_POINTS_PER_SUPER_PACGUM = 50
    DEFAULT_POINTS_PER_GHOST = 200
    DEFAULT_SEED = 42
    DEFAULT_LEVEL_MAX_TIME = 90
    DEFAULT_PLAYER_SPEED = 2.1429
    DEFAULT_GHOST_SPEED = 1.8214
    DEFAULT_FRIGHTENED_GHOST_SPEED = 1.0714
    DEFAULT_RETURNING_GHOST_SPEED = 3.5
    DEFAULT_POWER_MODE_DURATION = 7.0
    DEFAULT_LEVELS = tuple(
        LevelConfig(width=19, height=21) for _ in range(10)
    )

    @staticmethod
    def load(
        path: str | Path,
        fallback_to_defaults: bool = False,
    ) -> GameConfig:
        """Load a configuration file and return a validated GameConfig."""
        config_path = Path(path)

        data = ConfigLoader._read_json(config_path)

        if fallback_to_defaults:
            return ConfigLoader._build_config_safe(data)

        return ConfigLoader._build_config(data)

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        """Read and decode a JSON configuration file, ignoring comments."""
        if not path.is_file():
            raise ConfigError(f"Configuration file not found: {path}")

        try:
            with path.open("r", encoding="utf-8-sig") as file:
                lines: list[str] = []
                for line in file:
                    stripped = line.strip()
                    if stripped.startswith("#") or stripped.startswith("//"):
                        continue
                    lines.append(line)
                clean_json_str = "".join(lines)
                data: Any = json.loads(clean_json_str)
        except OSError as exc:
            raise ConfigError(
                f"Unable to read configuration file: {path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ConfigError(
                f"Invalid JSON in configuration file: {path}"
            ) from exc

        if not isinstance(data, dict):
            raise ConfigError(
                "Configuration root must be a JSON object."
            )

        return data

    @staticmethod
    def _build_config_safe(data: dict[str, Any]) -> GameConfig:
        """Build GameConfig with safe defaults for missing/invalid keys."""
        highscore_filename = data.get("highscore_filename")
        if (
            not isinstance(highscore_filename, str)
            or not highscore_filename.strip()
        ):
            print(
                f"Warning: Invalid or missing 'highscore_filename'. "
                f"Using default: '{ConfigLoader.DEFAULT_HIGHSCORE_FILENAME}'.",
                file=sys.stderr,
            )
            highscore_filename = ConfigLoader.DEFAULT_HIGHSCORE_FILENAME

        def safe_int(key: str, default: int, min_val: int = 0) -> int:
            val = data.get(key)
            if (
                not isinstance(val, int)
                or isinstance(val, bool)
                or val < min_val
            ):
                print(
                    f"Warning: Invalid or missing '{key}' ({val}). "
                    f"Clamping to default: {default}.",
                    file=sys.stderr,
                )
                return default
            return val

        def safe_float(key: str, default: float) -> float:
            val = data.get(key)
            if (
                not isinstance(val, (int, float))
                or isinstance(val, bool)
                or val <= 0
            ):
                print(
                    f"Warning: Invalid or missing '{key}' ({val}). "
                    f"Clamping to default: {default}.",
                    file=sys.stderr,
                )
                return default
            return float(val)

        lives = safe_int("lives", ConfigLoader.DEFAULT_LIVES, min_val=1)
        pacgum = safe_int("pacgum", ConfigLoader.DEFAULT_PACGUM, min_val=0)
        points_per_pacgum = safe_int(
            "points_per_pacgum",
            ConfigLoader.DEFAULT_POINTS_PER_PACGUM,
            min_val=0,
        )
        points_per_super_pacgum = safe_int(
            "points_per_super_pacgum",
            ConfigLoader.DEFAULT_POINTS_PER_SUPER_PACGUM,
            min_val=0,
        )
        points_per_ghost = safe_int(
            "points_per_ghost",
            ConfigLoader.DEFAULT_POINTS_PER_GHOST,
            min_val=0,
        )
        seed_val = data.get("seed")
        seed = (
            seed_val
            if isinstance(seed_val, int) and not isinstance(seed_val, bool)
            else ConfigLoader.DEFAULT_SEED
        )
        level_max_time = safe_int(
            "level_max_time", ConfigLoader.DEFAULT_LEVEL_MAX_TIME, min_val=1
        )

        # Speeds are permanently locked to engine constants
        # to ensure stable 60 FPS movement and physics.
        player_speed = ConfigLoader.DEFAULT_PLAYER_SPEED
        ghost_speed = ConfigLoader.DEFAULT_GHOST_SPEED
        frightened_ghost_speed = ConfigLoader.DEFAULT_FRIGHTENED_GHOST_SPEED
        returning_ghost_speed = ConfigLoader.DEFAULT_RETURNING_GHOST_SPEED
        power_mode_duration = safe_float(
            "power_mode_duration",
            ConfigLoader.DEFAULT_POWER_MODE_DURATION,
        )

        levels_data = data.get("levels")
        levels: list[LevelConfig] = []
        if isinstance(levels_data, list) and levels_data:
            for idx, lvl in enumerate(levels_data):
                if isinstance(lvl, dict):
                    w = lvl.get("width")
                    h = lvl.get("height")
                    if (
                        isinstance(w, int)
                        and isinstance(h, int)
                        and w > 0
                        and h > 0
                    ):
                        levels.append(LevelConfig(width=w, height=h))
        if not levels:
            msg = (
                "Warning: No valid levels found. "
                "Using standard 10 default levels."
            )
            print(msg, file=sys.stderr)
            levels = list(ConfigLoader.DEFAULT_LEVELS)

        return GameConfig(
            highscore_filename=highscore_filename,
            lives=lives,
            pacgum=pacgum,
            points_per_pacgum=points_per_pacgum,
            points_per_super_pacgum=points_per_super_pacgum,
            points_per_ghost=points_per_ghost,
            seed=seed,
            level_max_time=level_max_time,
            player_speed=player_speed,
            ghost_speed=ghost_speed,
            frightened_ghost_speed=frightened_ghost_speed,
            returning_ghost_speed=returning_ghost_speed,
            power_mode_duration=power_mode_duration,
            levels=tuple(levels),
        )

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
            player_speed=ConfigLoader._get_positive_float(
                data,
                "player_speed",
            ),
            ghost_speed=ConfigLoader._get_positive_float(
                data,
                "ghost_speed",
            ),
            frightened_ghost_speed=ConfigLoader._get_positive_float(
                data,
                "frightened_ghost_speed",
            ),
            returning_ghost_speed=ConfigLoader._get_positive_float(
                data,
                "returning_ghost_speed",
            ),
            power_mode_duration=ConfigLoader._get_positive_float(
                data,
                "power_mode_duration",
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
    def _get_positive_int(
        data: dict[str, Any],
        key: str,
    ) -> int:
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
    def _get_positive_float(
        data: dict[str, Any],
        key: str,
    ) -> float:
        """Get a required positive floating-point configuration value."""
        value = data.get(key)

        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise ConfigError(
                f"Configuration '{key}' must be a number."
            )

        numeric_value = float(value)

        if numeric_value <= 0:
            raise ConfigError(
                f"Configuration '{key}' must be greater than zero."
            )

        return numeric_value

    @staticmethod
    def _get_levels(
        data: dict[str, Any],
    ) -> tuple[LevelConfig, ...]:
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
