"""Tests for Pac-Man configuration domain models."""

import pytest

from src.config.game_config import GameConfig, LevelConfig


def test_level_config_stores_dimensions() -> None:
    """LevelConfig should store the configured dimensions."""
    level = LevelConfig(width=19, height=21)

    assert level.width == 19
    assert level.height == 21


def test_level_config_rejects_zero_width() -> None:
    """LevelConfig should reject a zero width."""
    with pytest.raises(ValueError):
        LevelConfig(width=0, height=21)


def test_level_config_rejects_zero_height() -> None:
    """LevelConfig should reject a zero height."""
    with pytest.raises(ValueError):
        LevelConfig(width=19, height=0)


def test_game_config_stores_values() -> None:
    """GameConfig should store the configured game values."""
    level = LevelConfig(width=19, height=21)

    config = GameConfig(
        highscore_filename="highscores.json",
        lives=3,
        pacgum=42,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=42,
        level_max_time=90,
        levels=(level,),
    )

    assert config.lives == 3
    assert config.pacgum == 42
    assert config.points_per_pacgum == 10
    assert config.points_per_super_pacgum == 50
    assert config.points_per_ghost == 200
    assert config.seed == 42
    assert config.level_max_time == 90
    assert config.levels == (level,)


def test_game_config_rejects_invalid_lives() -> None:
    """GameConfig should reject a non-positive number of lives."""
    level = LevelConfig(width=19, height=21)

    with pytest.raises(ValueError):
        GameConfig(
            highscore_filename="highscores.json",
            lives=0,
            pacgum=42,
            points_per_pacgum=10,
            points_per_super_pacgum=50,
            points_per_ghost=200,
            seed=42,
            level_max_time=90,
            levels=(level,),
        )
