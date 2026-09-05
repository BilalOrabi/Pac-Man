"""Tests for the Pac-Man configuration loader."""

import json

import pytest

from src.config.config_loader import ConfigError, ConfigLoader
from src.utils.error_logger import ErrorLogger


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

    assert configuration.player_speed == ConfigLoader.DEFAULT_PLAYER_SPEED
    assert configuration.ghost_speed == ConfigLoader.DEFAULT_GHOST_SPEED
    assert (
        configuration.frightened_ghost_speed
        == ConfigLoader.DEFAULT_FRIGHTENED_GHOST_SPEED
    )
    assert (
        configuration.returning_ghost_speed
        == ConfigLoader.DEFAULT_RETURNING_GHOST_SPEED
    )
    assert configuration.power_mode_duration == 7.0


@pytest.mark.parametrize(
    "speed_key",
    [
        "player_speed",
        "ghost_speed",
        "frightened_ghost_speed",
        "returning_ghost_speed",
    ],
)
def test_loader_allows_missing_speed_keys(tmp_path, speed_key: str) -> None:
    """The loader should allow omitting speed keys and use defaults."""
    configuration_data = create_valid_configuration()
    del configuration_data[speed_key]

    configuration_path = tmp_path / "config.json"
    configuration_path.write_text(
        json.dumps(configuration_data),
        encoding="utf-8",
    )

    configuration = ConfigLoader.load(configuration_path)
    assert configuration.player_speed == ConfigLoader.DEFAULT_PLAYER_SPEED
    assert configuration.ghost_speed == ConfigLoader.DEFAULT_GHOST_SPEED


@pytest.mark.parametrize(
    "field_name",
    [
        "power_mode_duration",
        "level_max_time",
        "lives",
    ],
)
def test_loader_rejects_missing_gameplay_value(
    tmp_path,
    field_name: str,
) -> None:
    """The loader should reject missing required gameplay values."""
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
        "power_mode_duration",
        "level_max_time",
        "lives",
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
    configuration_data["power_mode_duration"] = "long"

    configuration_path = tmp_path / "config.json"

    configuration_path.write_text(
        json.dumps(configuration_data),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        ConfigLoader.load(configuration_path)


def test_loader_ignores_comments_in_json(tmp_path) -> None:
    """The loader should ignore lines starting with # or //."""
    content = """
    # This is a comment at top
    {
        // Inline comment style
        "highscore_filename": "scores.json",
        "lives": 5,
        "pacgum": 30,
        "points_per_pacgum": 15,
        "points_per_super_pacgum": 60,
        "points_per_ghost": 300,
        "seed": 99,
        "level_max_time": 100,
        "player_speed": 4.5,
        "ghost_speed": 3.5,
        "frightened_ghost_speed": 2.0,
        "returning_ghost_speed": 5.0,
        "power_mode_duration": 6.0,
        "levels": [{"width": 10, "height": 10}]
    }
    # End comment
    """
    config_path = tmp_path / "config_with_comments.json"
    config_path.write_text(content, encoding="utf-8")

    config = ConfigLoader.load(config_path)
    assert config.lives == 5
    assert config.points_per_pacgum == 15


def test_loader_safe_defaults_clamping(tmp_path) -> None:
    """The safe loader should clamp missing or invalid values to defaults."""
    content = """
    {
        "unknown_key_ignored": 12345,
        "lives": -5
    }
    """
    config_path = tmp_path / "broken_config.json"
    config_path.write_text(content, encoding="utf-8")

    config = ConfigLoader.load(config_path, fallback_to_defaults=True)
    assert config.lives == ConfigLoader.DEFAULT_LIVES
    assert config.player_speed == ConfigLoader.DEFAULT_PLAYER_SPEED
    def_hs = ConfigLoader.DEFAULT_HIGHSCORE_FILENAME
    assert def_hs == config.highscore_filename
    assert len(config.levels) == 10


def test_loader_faulty_small_dimensions_default_to_19x21(
    tmp_path,
) -> None:
    """Dimensions smaller than 5x5 should warn and default to 19x21."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.install(str(log_file))
    try:
        config_data = create_valid_configuration()
        config_data["levels"] = [{"width": 2, "height": 2}]
        config_path = tmp_path / "config_2x2.json"
        config_path.write_text(json.dumps(config_data), encoding="utf-8")

        config = ConfigLoader.load(config_path)

        assert config.levels[0].width == 19
        assert config.levels[0].height == 21
        assert log_file.exists()
        assert "Faulty level 1 dimensions (2x2)" in log_file.read_text(
            encoding="utf-8"
        )
    finally:
        ErrorLogger.uninstall()


def test_loader_exceeding_max_dimensions_default_to_19x21(
    tmp_path,
) -> None:
    """Dimensions exceeding 35x24 should warn and default to 19x21."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.install(str(log_file))
    try:
        config_data = create_valid_configuration()
        config_data["levels"] = [{"width": 40, "height": 30}]
        config_path = tmp_path / "config_large.json"
        config_path.write_text(json.dumps(config_data), encoding="utf-8")

        config = ConfigLoader.load(config_path)

        assert config.levels[0].width == 19
        assert config.levels[0].height == 21
        assert log_file.exists()
        assert "Faulty level 1 dimensions (40x30)" in log_file.read_text(
            encoding="utf-8"
        )
    finally:
        ErrorLogger.uninstall()


def test_loader_safe_fallback_dimensions_clamping(
    tmp_path,
) -> None:
    """Safe fallback should also clamp faulty dimensions to 19x21."""
    log_file = tmp_path / "errors.log"
    ErrorLogger.install(str(log_file))
    try:
        content = json.dumps({
            "levels": [{"width": 2, "height": 2}, {"width": 50, "height": 50}]
        })
        config_path = tmp_path / "config_safe_bounds.json"
        config_path.write_text(content, encoding="utf-8")

        config = ConfigLoader.load(config_path, fallback_to_defaults=True)

        assert config.levels[0].width == 19
        assert config.levels[0].height == 21
        assert config.levels[1].width == 19
        assert config.levels[1].height == 21
        assert log_file.exists()
        log_content = log_file.read_text(encoding="utf-8")
        assert "Faulty level 1 dimensions (2x2)" in log_content
        assert "Faulty level 2 dimensions (50x50)" in log_content
    finally:
        ErrorLogger.uninstall()
