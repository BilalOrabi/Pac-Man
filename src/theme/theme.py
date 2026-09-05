"""Centralized visual theme configuration for the Pac-Man game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorTheme:
    """Define the colors used throughout the Pac-Man interface."""

    background: tuple[int, int, int] = (0, 0, 0)
    maze: tuple[int, int, int] = (0, 0, 255)
    player: tuple[int, int, int] = (255, 255, 0)
    ghost_red: tuple[int, int, int] = (255, 0, 0)
    ghost_pink: tuple[int, int, int] = (255, 184, 255)
    ghost_blue: tuple[int, int, int] = (0, 255, 255)
    ghost_orange: tuple[int, int, int] = (255, 184, 82)
    text: tuple[int, int, int] = (255, 255, 255)
    accent: tuple[int, int, int] = (255, 255, 0)


@dataclass(frozen=True)
class FontTheme:
    """Define font assets used by the game's interface."""

    game_font_path: str = "assets/fonts/game_font.ttf"
    ui_font_path: str = "assets/fonts/ui_font.ttf"
    score_font_path: str = "assets/fonts/score_font.ttf"


@dataclass(frozen=True)
class ImageAssets:
    """Define image assets used by the game's presentation."""

    background_path: str = "assets/images/background.png"
    player_path: str = "assets/images/pacman.png"
    ghost_red_path: str = "assets/images/ghost_red.png"
    ghost_pink_path: str = "assets/images/ghost_pink.png"
    ghost_blue_path: str = "assets/images/ghost_blue.png"
    ghost_orange_path: str = "assets/images/ghost_orange.png"


@dataclass(frozen=True)
class AudioAssets:
    """Define audio assets used by the game."""

    menu_music_path: str = "assets/audio/main menu music.ogg"
    game_music_path: str = "assets/audio/start of game music.ogg"
    invincibility_music_path: str = (
        "assets/audio/Invincibility cheat ON music.mp3"
    )
    game_over_music_path: str = "assets/audio/gameover screen music.mp3"
    victory_music_path: str = "assets/audio/victory music.mp3"
    super_pacgum_sound_path: str = "assets/audio/supergum eating sound.mp3"
    death_sound_path: str = "assets/audio/death music.mp3"
    ghost_eaten_1_sound_path: str = "assets/audio/kill ghost 1.ogg"
    ghost_eaten_2_sound_path: str = "assets/audio/kill ghost 2.ogg"
    ghost_eaten_3_sound_path: str = "assets/audio/kill ghost 3.ogg"
    ghost_eaten_4_sound_path: str = "assets/audio/kill ghost 4.ogg"
    cheat_freeze_sound_path: str = "assets/audio/freeze cheat ON sound.ogg"
    cheat_speed_sound_path: str = "assets/audio/speed.ogg"
    cheat_extra_life_sound_path: str = "assets/audio/Lives inscress sound.mp3"


@dataclass(frozen=True)
class EffectAssets:
    """Define visual-effect assets used by the game."""

    power_mode_effect_path: str = ""
    death_effect_path: str = ""


@dataclass(frozen=True)
class Theme:
    """Centralize all configurable presentation assets and visual values."""

    colors: ColorTheme = ColorTheme()
    fonts: FontTheme = FontTheme()
    images: ImageAssets = ImageAssets()
    audio: AudioAssets = AudioAssets()
    effects: EffectAssets = EffectAssets()
