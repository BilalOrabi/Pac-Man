"""Tests for configuration file loading."""

import json
from pathlib import Path

import pytest

from src.config.config_loader import ConfigError, ConfigLoader


def _write_config(
    tmp_path: Path,
    data: dict[str, object],
) -> Path:
    """Write a temporary JSON configuration file."""
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )
    return path


def _valid_config() -> dict[str, object]:
    """Return a minimal valid Pac-Man configuration."""
    return {
        "highscore_filename": "highscores.json",
        "lives": 3,
        "pacgum": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
        "levels": [
            {
                "width": 19,
                "height": 21,
            }
        ],
    }


def test_load_valid_config(tmp_path: Path) -> None:
    """ConfigLoader should load a valid configuration."""
    path = _write_config(tmp_path, _valid_config())

    config = ConfigLoader.load(path)

    assert config.lives == 3
    assert config.pacgum == 42
    assert len(config.levels) == 1
    assert config.levels[0].width == 19
    assert config.levels[0].height == 21


def test_missing_config_file(tmp_path: Path) -> None:
    """ConfigLoader should reject a missing configuration file."""
    path = tmp_path / "missing.json"

    with pytest.raises(ConfigError):
        ConfigLoader.load(path)


def test_invalid_json(tmp_path: Path) -> None:
    """ConfigLoader should reject malformed JSON."""
    path = tmp_path / "invalid.json"
    path.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        ConfigLoader.load(path)


def test_missing_required_field(tmp_path: Path) -> None:
    """ConfigLoader should reject missing required configuration."""
    data = _valid_config()
    del data["lives"]

    path = _write_config(tmp_path, data)

    with pytest.raises(ConfigError):
        ConfigLoader.load(path)


def test_invalid_level_dimensions(tmp_path: Path) -> None:
    """ConfigLoader should reject invalid level dimensions."""
    data = _valid_config()
    data["levels"] = [{"width": 0, "height": 21}]

    path = _write_config(tmp_path, data)

    with pytest.raises(ConfigError):
        ConfigLoader.load(path)
