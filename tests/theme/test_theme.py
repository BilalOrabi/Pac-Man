"""Tests for the Pac-Man visual theme configuration."""

from src.theme.theme import (
    AudioAssets,
    ColorTheme,
    EffectAssets,
    FontTheme,
    ImageAssets,
    Theme,
)


def test_theme_has_default_visual_configuration() -> None:
    """Theme should provide usable default visual configuration."""
    theme = Theme()

    assert theme.colors.background == (0, 0, 0)
    assert theme.colors.player == (255, 255, 0)


def test_theme_contains_default_image_assets() -> None:
    """Theme should define placeholder image asset paths."""
    theme = Theme()

    assert theme.images.background_path == (
        "assets/images/background.png"
    )

    assert theme.images.player_path == (
        "assets/images/pacman.png"
    )


def test_theme_contains_default_font_assets() -> None:
    """Theme should define placeholder font asset paths."""
    theme = Theme()

    assert theme.fonts.game_font_path == (
        "assets/fonts/game_font.ttf"
    )

    assert theme.fonts.ui_font_path == (
        "assets/fonts/ui_font.ttf"
    )


def test_theme_contains_default_audio_assets() -> None:
    """Theme should define default audio asset paths."""
    theme = Theme()

    assert theme.audio.menu_music_path == (
        "assets/audio/main menu music.ogg"
    )
    assert theme.audio.super_pacgum_sound_path == (
        "assets/audio/supergum eating sound.mp3"
    )


def test_theme_contains_default_effect_assets() -> None:
    """Theme should provide default effect configuration."""
    theme = Theme()

    assert theme.effects.power_mode_effect_path == ""
    assert theme.effects.death_effect_path == ""


def test_theme_allows_custom_assets() -> None:
    """Theme should allow custom assets without changing renderers."""
    custom_images = ImageAssets(
        background_path="custom/background.png",
        player_path="custom/player.png",
    )

    custom_fonts = FontTheme(
        game_font_path="custom/game.ttf",
        ui_font_path="custom/ui.ttf",
        score_font_path="custom/score.ttf",
    )

    custom_audio = AudioAssets(
        menu_music_path="custom/menu.ogg",
        game_music_path="custom/game.ogg",
        super_pacgum_sound_path="custom/super.mp3",
        death_sound_path="custom/death.mp3",
    )

    custom_effects = EffectAssets(
        power_mode_effect_path="custom/power.png",
        death_effect_path="custom/death.png",
    )

    theme = Theme(
        images=custom_images,
        fonts=custom_fonts,
        audio=custom_audio,
        effects=custom_effects,
    )

    assert theme.images.player_path == "custom/player.png"
    assert theme.fonts.game_font_path == "custom/game.ttf"
    assert theme.audio.menu_music_path == "custom/menu.ogg"
    assert theme.effects.death_effect_path == "custom/death.png"


def test_theme_is_immutable() -> None:
    """Theme configuration should be immutable after creation."""
    theme = Theme()

    try:
        theme.colors = ColorTheme(
            background=(255, 255, 255),
        )
    except AttributeError:
        return

    raise AssertionError("Theme should be immutable.")
