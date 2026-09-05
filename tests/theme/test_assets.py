"""Tests for the Pac-Man presentation asset configuration."""

from dataclasses import FrozenInstanceError

import pytest

from src.theme.assets import AssetPaths, DEFAULT_ASSETS


def test_asset_paths_use_expected_default_values() -> None:
    """Default asset paths should point to the expected asset locations."""
    assets = AssetPaths()

    assert assets.background == "assets/images/background.png"
    assert assets.player_sprite == "assets/images/player.png"
    assert assets.menu_font == "assets/fonts/menu.ttf"
    assert assets.game_font == "assets/fonts/game.ttf"


def test_ghost_assets_are_defined() -> None:
    """All ghost sprite assets should be available."""
    assets = AssetPaths()

    assert assets.ghost_red_sprite == "assets/images/ghost_red.png"
    assert assets.ghost_pink_sprite == "assets/images/ghost_pink.png"
    assert assets.ghost_blue_sprite == "assets/images/ghost_blue.png"
    assert assets.ghost_orange_sprite == "assets/images/ghost_orange.png"


def test_audio_assets_are_defined() -> None:
    """Required audio assets should be available."""
    assets = AssetPaths()

    assert assets.menu_music in (
        "assets/audio/main menu music.ogg",
        "assets/audio/menu music.mp3",
    )
    assert assets.game_music == "assets/audio/start of game music.ogg"
    assert assets.game_start_music == "assets/audio/start of game music.ogg"
    assert assets.invincibility_music == (
        "assets/audio/Invincibility cheat ON music.mp3"
    )
    assert assets.super_pacgum_sound == (
        "assets/audio/supergum eating sound.mp3"
    )
    assert assets.ghost_eaten_1_sound == "assets/audio/kill ghost 1.ogg"
    assert assets.death_sound == "assets/audio/death music.mp3"


def test_cheat_sound_assets_are_defined() -> None:
    """Cheat audio assets should be available."""
    assets = AssetPaths()

    assert assets.cheat_freeze_sound == (
        "assets/audio/freeze cheat ON sound.ogg"
    )
    assert assets.cheat_speed_sound == "assets/audio/speed.ogg"
    assert assets.cheat_extra_life_sound == (
        "assets/audio/Lives inscress sound.mp3"
    )


def test_default_assets_is_asset_paths_instance() -> None:
    """The shared default asset registry should use AssetPaths."""
    assert isinstance(DEFAULT_ASSETS, AssetPaths)


def test_asset_paths_are_immutable() -> None:
    """Asset configuration should not be modified accidentally."""
    assets = AssetPaths()

    with pytest.raises(FrozenInstanceError):
        assets.background = "different_background.png"
