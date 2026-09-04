"""Tests for Pac-Man configuration models."""

import pytest

from src.config.game_config import GameConfig, LevelConfig


def create_game_config() -> GameConfig:
    """Create a valid game configuration for testing."""
    return GameConfig(
        highscore_filename="highscores.txt",
        lives=3,
        pacgum=10,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=100,
        level_max_time=120,
        player_speed=5.0,
        ghost_speed=4.0,
        frightened_ghost_speed=2.0,
        returning_ghost_speed=6.0,
        power_mode_duration=7.0,
        levels=(
            LevelConfig(width=5, height=5),
        ),
    )


def test_level_config_accepts_valid_dimensions() -> None:
    """LevelConfig should accept positive dimensions."""
    configuration = LevelConfig(
        width=10,
        height=15,
    )

    assert configuration.width == 10
    assert configuration.height == 15


@pytest.mark.parametrize(
    "width,height",
    [
        (0, 5),
        (-1, 5),
        (5, 0),
        (5, -1),
    ],
)
def test_level_config_rejects_invalid_dimensions(
    width: int,
    height: int,
) -> None:
    """LevelConfig should reject non-positive dimensions."""
    with pytest.raises(ValueError):
        LevelConfig(width=width, height=height)


def test_game_config_accepts_valid_values() -> None:
    """GameConfig should accept a complete valid configuration."""
    configuration = create_game_config()

    assert configuration.lives == 3
    assert configuration.player_speed == 5.0
    assert configuration.ghost_speed == 4.0
    assert configuration.frightened_ghost_speed == 2.0
    assert configuration.returning_ghost_speed == 6.0
    assert configuration.power_mode_duration == 7.0
    assert len(configuration.levels) == 1


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
def test_game_config_rejects_non_positive_gameplay_values(
    field_name: str,
) -> None:
    """GameConfig should reject non-positive gameplay values."""
    configuration_values = {
        "player_speed": 5.0,
        "ghost_speed": 4.0,
        "frightened_ghost_speed": 2.0,
        "returning_ghost_speed": 6.0,
        "power_mode_duration": 7.0,
    }

    configuration_values[field_name] = 0.0

    with pytest.raises(ValueError):
        GameConfig(
            **{
                **create_game_config().__dict__,
                **configuration_values,
            }
        )


def test_game_config_rejects_empty_levels() -> None:
    """GameConfig should require at least one level."""
    with pytest.raises(ValueError):
        GameConfig(
            **{
                **create_game_config().__dict__,
                "levels": (),
            }
        )


def test_game_config_is_immutable() -> None:
    """GameConfig should be immutable."""
    configuration = create_game_config()

    with pytest.raises(AttributeError):
        configuration.player_speed = 10.0
