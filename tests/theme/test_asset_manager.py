"""Tests for the Pac-Man asset manager."""

import pytest

from src.theme.asset_manager import AssetManager
from src.theme.assets import AssetPaths


def create_asset_manager() -> AssetManager:
    """Create an initialized asset manager for testing."""
    asset_manager = AssetManager()
    asset_manager.initialize()
    return asset_manager


def test_asset_manager_starts_uninitialized() -> None:
    """Asset manager should start uninitialized."""
    asset_manager = AssetManager()

    assert asset_manager.is_initialized is False


def test_initialize_enables_asset_manager() -> None:
    """Initialization should enable asset access."""
    asset_manager = AssetManager()

    asset_manager.initialize()

    assert asset_manager.is_initialized is True


def test_get_background_returns_configured_asset() -> None:
    """Background lookup should return the configured path."""
    asset_manager = create_asset_manager()

    assert (
        asset_manager.get_background()
        == "assets/images/background.png"
    )


def test_get_player_sprite_returns_configured_asset() -> None:
    """Player sprite lookup should return the configured path."""
    asset_manager = create_asset_manager()

    assert (
        asset_manager.get_player_sprite()
        == "assets/images/player.png"
    )


@pytest.mark.parametrize(
    ("ghost_color", "expected_path"),
    [
        ("red", "assets/images/ghost_red.png"),
        ("pink", "assets/images/ghost_pink.png"),
        ("blue", "assets/images/ghost_blue.png"),
        ("orange", "assets/images/ghost_orange.png"),
    ],
)
def test_get_ghost_sprite_returns_correct_asset(
    ghost_color: str,
    expected_path: str,
) -> None:
    """Ghost lookup should return the correct sprite."""
    asset_manager = create_asset_manager()

    assert (
        asset_manager.get_ghost_sprite(ghost_color)
        == expected_path
    )


def test_get_ghost_sprite_is_case_insensitive() -> None:
    """Ghost color lookup should ignore letter casing."""
    asset_manager = create_asset_manager()

    assert (
        asset_manager.get_ghost_sprite("RED")
        == "assets/images/ghost_red.png"
    )


def test_unknown_ghost_color_is_rejected() -> None:
    """Unknown ghost colors should raise ValueError."""
    asset_manager = create_asset_manager()

    with pytest.raises(ValueError):
        asset_manager.get_ghost_sprite("green")


@pytest.mark.parametrize(
    ("font_type", "expected_path"),
    [
        ("menu", "assets/fonts/menu.ttf"),
        ("game", "assets/fonts/game.ttf"),
    ],
)
def test_get_font_returns_correct_asset(
    font_type: str,
    expected_path: str,
) -> None:
    """Font lookup should return the configured font."""
    asset_manager = create_asset_manager()

    assert asset_manager.get_font(font_type) == expected_path


def test_unknown_font_type_is_rejected() -> None:
    """Unknown font types should raise ValueError."""
    asset_manager = create_asset_manager()

    with pytest.raises(ValueError):
        asset_manager.get_font("unknown")


@pytest.mark.parametrize(
    ("music_type", "expected_path"),
    [
        ("menu", "assets/audio/menu_music.ogg"),
        ("game", "assets/audio/game_music.ogg"),
    ],
)
def test_get_music_returns_correct_asset(
    music_type: str,
    expected_path: str,
) -> None:
    """Music lookup should return the configured music asset."""
    asset_manager = create_asset_manager()

    assert asset_manager.get_music(music_type) == expected_path


def test_unknown_music_type_is_rejected() -> None:
    """Unknown music types should raise ValueError."""
    asset_manager = create_asset_manager()

    with pytest.raises(ValueError):
        asset_manager.get_music("unknown")


@pytest.mark.parametrize(
    ("sound_type", "expected_path"),
    [
        ("pacgum", "assets/audio/pacgum.wav"),
        ("super_pacgum", "assets/audio/super_pacgum.wav"),
        ("ghost_eaten", "assets/audio/ghost_eaten.wav"),
        ("death", "assets/audio/death.wav"),
    ],
)
def test_get_sound_returns_correct_asset(
    sound_type: str,
    expected_path: str,
) -> None:
    """Sound lookup should return the configured sound asset."""
    asset_manager = create_asset_manager()

    assert asset_manager.get_sound(sound_type) == expected_path


def test_unknown_sound_type_is_rejected() -> None:
    """Unknown sound types should raise ValueError."""
    asset_manager = create_asset_manager()

    with pytest.raises(ValueError):
        asset_manager.get_sound("unknown")


@pytest.mark.parametrize(
    ("effect_type", "expected_path"),
    [
        ("power_mode", "assets/effects/power_mode.effect"),
        ("death", "assets/effects/death.effect"),
    ],
)
def test_get_effect_returns_correct_asset(
    effect_type: str,
    expected_path: str,
) -> None:
    """Effect lookup should return the configured effect asset."""
    asset_manager = create_asset_manager()

    assert asset_manager.get_effect(effect_type) == expected_path


def test_unknown_effect_type_is_rejected() -> None:
    """Unknown effects should raise ValueError."""
    asset_manager = create_asset_manager()

    with pytest.raises(ValueError):
        asset_manager.get_effect("unknown")


def test_asset_access_requires_initialization() -> None:
    """Asset access should require initialization."""
    asset_manager = AssetManager()

    with pytest.raises(RuntimeError):
        asset_manager.get_background()


def test_custom_asset_configuration_is_supported() -> None:
    """Asset manager should support custom asset configurations."""
    custom_assets = AssetPaths(
        background="custom/menu_background.png",
        player_sprite="custom/pacman.png",
    )

    asset_manager = AssetManager(assets=custom_assets)
    asset_manager.initialize()

    assert (
        asset_manager.get_background()
        == "custom/menu_background.png"
    )
    assert (
        asset_manager.get_player_sprite()
        == "custom/pacman.png"
    )


def test_shutdown_disables_asset_manager() -> None:
    """Shutdown should disable future asset access."""
    asset_manager = create_asset_manager()

    asset_manager.shutdown()

    assert asset_manager.is_initialized is False

    with pytest.raises(RuntimeError):
        asset_manager.get_background()
