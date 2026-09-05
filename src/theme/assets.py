"""Centralized asset configuration for the Pac-Man presentation layer."""

import os
from dataclasses import dataclass


def _resolve_menu_music() -> str:
    """Return the available menu music track path."""
    mp3_path = "assets/audio/menu music.mp3"
    if os.path.isfile(mp3_path):
        return mp3_path
    return "assets/audio/main menu music.ogg"


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

    menu_music: str = _resolve_menu_music()
    game_music: str = "assets/audio/start of game music.ogg"
    game_start_music: str = "assets/audio/start of game music.ogg"
    invincibility_music: str = (
        "assets/audio/Invincibility cheat ON music.mp3"
    )
    game_over_music: str = "assets/audio/gameover screen music.mp3"
    victory_music: str = "assets/audio/victory music.mp3"

    super_pacgum_sound: str = "assets/audio/supergum eating sound.mp3"
    death_sound: str = "assets/audio/death music.mp3"
    ghost_eaten_1_sound: str = "assets/audio/kill ghost 1.ogg"
    ghost_eaten_2_sound: str = "assets/audio/kill ghost 2.ogg"
    ghost_eaten_3_sound: str = "assets/audio/kill ghost 3.ogg"
    ghost_eaten_4_sound: str = "assets/audio/kill ghost 4.ogg"

    cheat_freeze_sound: str = "assets/audio/freeze cheat ON sound.ogg"
    cheat_speed_sound: str = "assets/audio/speed.ogg"
    cheat_extra_life_sound: str = "assets/audio/Lives inscress sound.mp3"


DEFAULT_ASSETS = AssetPaths()
