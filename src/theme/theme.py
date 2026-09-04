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

    background_music_path: str = "assets/audio/background_music.ogg"
    pacgum_sound_path: str = "assets/audio/pacgum.wav"
    super_pacgum_sound_path: str = "assets/audio/super_pacgum.wav"
    ghost_eaten_sound_path: str = "assets/audio/ghost_eaten.wav"
    game_over_sound_path: str = "assets/audio/game_over.wav"
    victory_sound_path: str = "assets/audio/victory.wav"


@dataclass(frozen=True)
class EffectAssets:
    """Define visual-effect assets used by the game."""

    power_mode_effect_path: str = (
        "assets/effects/power_mode_effect.png"
    )
    death_effect_path: str = (
        "assets/effects/death_effect.png"
    )


@dataclass(frozen=True)
class Theme:
    """Centralize all configurable presentation assets and visual values."""

    colors: ColorTheme = ColorTheme()
    fonts: FontTheme = FontTheme()
    images: ImageAssets = ImageAssets()
    audio: AudioAssets = AudioAssets()
    effects: EffectAssets = EffectAssets()
