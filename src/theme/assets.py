"""Centralized asset configuration for the Pac-Man presentation layer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AssetPaths:
    """Store paths to presentation assets."""

    background: str = "assets/images/background.png"

    player_sprite: str = "assets/images/player.png"

    ghost_red_sprite: str = "assets/images/ghost_red.png"
    ghost_pink_sprite: str = "assets/images/ghost_pink.png"
    ghost_blue_sprite: str = "assets/images/ghost_blue.png"
    ghost_orange_sprite: str = "assets/images/ghost_orange.png"

    menu_font: str = "assets/fonts/menu.ttf"
    game_font: str = "assets/fonts/game.ttf"

    menu_music: str = "assets/audio/menu_music.ogg"
    game_music: str = "assets/audio/game_music.ogg"

    pacgum_sound: str = "assets/audio/pacgum.wav"
    super_pacgum_sound: str = "assets/audio/super_pacgum.wav"
    ghost_eaten_sound: str = "assets/audio/ghost_eaten.wav"
    death_sound: str = "assets/audio/death.wav"

    power_mode_effect: str = "assets/effects/power_mode.effect"
    death_effect: str = "assets/effects/death.effect"


DEFAULT_ASSETS = AssetPaths()
