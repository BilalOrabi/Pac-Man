"""Load and validate Pac-Man game configuration from JSON."""

import json
from pathlib import Path
from typing import Any

from src.config.game_config import GameConfig, LevelConfig
from src.utils.error_logger import ErrorLogger


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
    MIN_LEVEL_WIDTH = 5
    MAX_LEVEL_WIDTH = 35
    MIN_LEVEL_HEIGHT = 5
    MAX_LEVEL_HEIGHT = 24
    DEFAULT_LEVEL_WIDTH = 19
    DEFAULT_LEVEL_HEIGHT = 21
    DEFAULT_LEVELS = tuple(
        LevelConfig(width=19, height=21)
        for _ in range(10)
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
    @staticmethod
    def _safe_int(
        data: dict[str, Any],
        key: str,
        default: int,
        min_val: int = 0,
    ) -> int:
        """Extract an integer or fall back to default with warning."""
        val = data.get(key)
        if not isinstance(val, int) or isinstance(val, bool) or val < min_val:
            ErrorLogger.log(
                f"Warning: Invalid or missing '{key}' ({val}). "
                f"Clamping to default: {default}."
            )
            return default
        return val

    @staticmethod
    def _safe_float(
        data: dict[str, Any],
        key: str,
        default: float,
    ) -> float:
        """Extract a float or fall back to default with warning."""
        val = data.get(key)
        if (
            not isinstance(val, (int, float))
            or isinstance(val, bool)
            or val <= 0
        ):
            ErrorLogger.log(
                f"Warning: Invalid or missing '{key}' ({val}). "
                f"Clamping to default: {default}."
            )
            return default
        return float(val)

    @staticmethod
    def _safe_highscore_filename(data: dict[str, Any]) -> str:
        """Extract valid highscore filename or fall back to default."""
        highscore_filename = data.get("highscore_filename")
        if (
            not isinstance(highscore_filename, str)
            or not highscore_filename.strip()
        ):
            ErrorLogger.log(
                f"Warning: Invalid or missing 'highscore_filename'. "
                f"Using default: '{ConfigLoader.DEFAULT_HIGHSCORE_FILENAME}'."
            )
            return ConfigLoader.DEFAULT_HIGHSCORE_FILENAME
        return highscore_filename

    @staticmethod
    def _safe_level_dimension(w: int, h: int, idx: int) -> tuple[int, int]:
        """Clamp level dimensions to allowed bounds with warning."""
        if (
            w < ConfigLoader.MIN_LEVEL_WIDTH
            or w > ConfigLoader.MAX_LEVEL_WIDTH
            or h < ConfigLoader.MIN_LEVEL_HEIGHT
            or h > ConfigLoader.MAX_LEVEL_HEIGHT
        ):
            ErrorLogger.log(
                f"Warning: Faulty level {idx + 1} dimensions "
                f"({w}x{h}). Width must be between "
                f"({ConfigLoader.MIN_LEVEL_WIDTH} - "
                f"{ConfigLoader.MAX_LEVEL_WIDTH}) and height "
                f"({ConfigLoader.MIN_LEVEL_HEIGHT} - "
                f"{ConfigLoader.MAX_LEVEL_HEIGHT}). "
                f"Defaulting to "
                f"{ConfigLoader.DEFAULT_LEVEL_WIDTH}x"
                f"{ConfigLoader.DEFAULT_LEVEL_HEIGHT}."
            )
            return (
                ConfigLoader.DEFAULT_LEVEL_WIDTH,
                ConfigLoader.DEFAULT_LEVEL_HEIGHT,
            )
        return (w, h)

    @staticmethod
    def _safe_levels(data: dict[str, Any]) -> tuple[LevelConfig, ...]:
        """Parse levels with dimension clamping and default fallback."""
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
                        and not isinstance(w, bool)
                        and not isinstance(h, bool)
                        and w > 0
                        and h > 0
                    ):
                        w, h = ConfigLoader._safe_level_dimension(w, h, idx)
                        levels.append(LevelConfig(width=w, height=h))

        if not levels:
            ErrorLogger.log(
                "Warning: No valid levels found. "
                "Using standard 10 default levels."
            )
            return ConfigLoader.DEFAULT_LEVELS

        return tuple(levels)

    @staticmethod
    def _build_config_safe(data: dict[str, Any]) -> GameConfig:
        """Build GameConfig with safe defaults for missing/invalid keys."""
        seed_val = data.get("seed")
        seed = (
            seed_val
            if isinstance(seed_val, int) and not isinstance(seed_val, bool)
            else ConfigLoader.DEFAULT_SEED
        )

        return GameConfig(
            highscore_filename=ConfigLoader._safe_highscore_filename(data),
            lives=ConfigLoader._safe_int(
                data, "lives", ConfigLoader.DEFAULT_LIVES, min_val=1
            ),
            pacgum=ConfigLoader._safe_int(
                data, "pacgum", ConfigLoader.DEFAULT_PACGUM, min_val=0
            ),
            points_per_pacgum=ConfigLoader._safe_int(
                data,
                "points_per_pacgum",
                ConfigLoader.DEFAULT_POINTS_PER_PACGUM,
                min_val=0,
            ),
            points_per_super_pacgum=ConfigLoader._safe_int(
                data,
                "points_per_super_pacgum",
                ConfigLoader.DEFAULT_POINTS_PER_SUPER_PACGUM,
                min_val=0,
            ),
            points_per_ghost=ConfigLoader._safe_int(
                data,
                "points_per_ghost",
                ConfigLoader.DEFAULT_POINTS_PER_GHOST,
                min_val=0,
            ),
            seed=seed,
            level_max_time=ConfigLoader._safe_int(
                data,
                "level_max_time",
                ConfigLoader.DEFAULT_LEVEL_MAX_TIME,
                min_val=1,
            ),
            player_speed=ConfigLoader.DEFAULT_PLAYER_SPEED,
            ghost_speed=ConfigLoader.DEFAULT_GHOST_SPEED,
            frightened_ghost_speed=ConfigLoader.DEFAULT_FRIGHTENED_GHOST_SPEED,
            returning_ghost_speed=ConfigLoader.DEFAULT_RETURNING_GHOST_SPEED,
            power_mode_duration=ConfigLoader._safe_float(
                data,
                "power_mode_duration",
                ConfigLoader.DEFAULT_POWER_MODE_DURATION,
            ),
            levels=ConfigLoader._safe_levels(data),
        )

    @staticmethod
    def _build_config(data: dict[str, Any]) -> GameConfig:
        """Validate raw configuration and build the domain model."""
        player_speed = ConfigLoader.DEFAULT_PLAYER_SPEED
        ghost_speed = ConfigLoader.DEFAULT_GHOST_SPEED
        frightened_ghost_speed = ConfigLoader.DEFAULT_FRIGHTENED_GHOST_SPEED
        returning_ghost_speed = ConfigLoader.DEFAULT_RETURNING_GHOST_SPEED

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
            player_speed=player_speed,
            ghost_speed=ghost_speed,
            frightened_ghost_speed=frightened_ghost_speed,
            returning_ghost_speed=returning_ghost_speed,
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
    def _parse_single_level(index: int, raw_level: Any) -> LevelConfig:
        """Validate and construct a LevelConfig from raw JSON."""
        if not isinstance(raw_level, dict):
            raise ConfigError(f"Level {index} must be a JSON object.")

        width = ConfigLoader._get_positive_int(raw_level, "width")
        height = ConfigLoader._get_positive_int(raw_level, "height")

        if (
            width < ConfigLoader.MIN_LEVEL_WIDTH
            or width > ConfigLoader.MAX_LEVEL_WIDTH
            or height < ConfigLoader.MIN_LEVEL_HEIGHT
            or height > ConfigLoader.MAX_LEVEL_HEIGHT
        ):
            ErrorLogger.log(
                f"Warning: Faulty level {index + 1} dimensions "
                f"({width}x{height}). Width must be "
                f"{ConfigLoader.MIN_LEVEL_WIDTH}.."
                f"{ConfigLoader.MAX_LEVEL_WIDTH} and height "
                f"{ConfigLoader.MIN_LEVEL_HEIGHT}.."
                f"{ConfigLoader.MAX_LEVEL_HEIGHT}. "
                f"Defaulting to "
                f"{ConfigLoader.DEFAULT_LEVEL_WIDTH}x"
                f"{ConfigLoader.DEFAULT_LEVEL_HEIGHT}."
            )
            width = ConfigLoader.DEFAULT_LEVEL_WIDTH
            height = ConfigLoader.DEFAULT_LEVEL_HEIGHT

        return LevelConfig(width=width, height=height)

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

        return tuple(
            ConfigLoader._parse_single_level(idx, raw)
            for idx, raw in enumerate(raw_levels)
        )
