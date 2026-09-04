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

    assert assets.menu_music == "assets/audio/menu_music.ogg"
    assert assets.game_music == "assets/audio/game_music.ogg"
    assert assets.pacgum_sound == "assets/audio/pacgum.wav"
    assert assets.super_pacgum_sound == (
        "assets/audio/super_pacgum.wav"
    )
    assert assets.ghost_eaten_sound == (
        "assets/audio/ghost_eaten.wav"
    )
    assert assets.death_sound == "assets/audio/death.wav"


def test_effect_assets_are_defined() -> None:
    """Visual effect assets should be available."""
    assets = AssetPaths()

    assert assets.power_mode_effect == (
        "assets/effects/power_mode.effect"
    )
    assert assets.death_effect == "assets/effects/death.effect"


def test_default_assets_is_asset_paths_instance() -> None:
    """The shared default asset registry should use AssetPaths."""
    assert isinstance(DEFAULT_ASSETS, AssetPaths)


def test_asset_paths_are_immutable() -> None:
    """Asset configuration should not be modified accidentally."""
    assets = AssetPaths()

    with pytest.raises(FrozenInstanceError):
        assets.background = "different_background.png"
