"""Tests for the Pac-Man configuration loader."""

import json

import pytest

from src.config.config_loader import ConfigError, ConfigLoader


def create_valid_configuration() -> dict:
    """Create a valid JSON configuration dictionary."""
    return {
        "highscore_filename": "highscores.txt",
        "lives": 3,
        "pacgum": 10,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 100,
        "level_max_time": 120,
        "player_speed": 5.0,
        "ghost_speed": 4.0,
        "frightened_ghost_speed": 2.0,
        "returning_ghost_speed": 6.0,
        "power_mode_duration": 7.0,
        "levels": [
            {
                "width": 5,
                "height": 5,
            },
            {
                "width": 6,
                "height": 6,
            },
        ],
    }


def test_loader_reads_gameplay_configuration(tmp_path) -> None:
    """The loader should read gameplay values from JSON."""
    configuration_path = tmp_path / "config.json"

    configuration_path.write_text(
        json.dumps(create_valid_configuration()),
        encoding="utf-8",
    )

    configuration = ConfigLoader.load(configuration_path)

    assert configuration.player_speed == 5.0
    assert configuration.ghost_speed == 4.0
    assert configuration.frightened_ghost_speed == 2.0
    assert configuration.returning_ghost_speed == 6.0
    assert configuration.power_mode_duration == 7.0


@pytest.mark.parametrize(
    "field_name",
    [
        "player_speed",
        "ghost_speed",
        "frightened_ghost_speed",
        "returning_ghost_speed",
        "power_mode_duration",
    ],
)
def test_loader_rejects_missing_gameplay_value(
    tmp_path,
    field_name: str,
) -> None:
    """The loader should reject missing gameplay values."""
    configuration_data = create_valid_configuration()
    del configuration_data[field_name]

    configuration_path = tmp_path / "config.json"

    configuration_path.write_text(
        json.dumps(configuration_data),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        ConfigLoader.load(configuration_path)


@pytest.mark.parametrize(
    "field_name",
    [
        "player_speed",
        "ghost_speed",
        "frightened_ghost_speed",
        "returning_ghost_speed",
        "power_mode_duration",
    ],
)
def test_loader_rejects_non_positive_gameplay_value(
    tmp_path,
    field_name: str,
) -> None:
    """The loader should reject non-positive gameplay values."""
    configuration_data = create_valid_configuration()
    configuration_data[field_name] = 0

    configuration_path = tmp_path / "config.json"

    configuration_path.write_text(
        json.dumps(configuration_data),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        ConfigLoader.load(configuration_path)


def test_loader_rejects_non_numeric_gameplay_value(tmp_path) -> None:
    """The loader should reject non-numeric gameplay values."""
    configuration_data = create_valid_configuration()
    configuration_data["player_speed"] = "fast"

    configuration_path = tmp_path / "config.json"

    configuration_path.write_text(
        json.dumps(configuration_data),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        ConfigLoader.load(configuration_path)
