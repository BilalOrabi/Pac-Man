"""Unit tests for the presentation-layer AudioPresenter."""

from unittest.mock import patch
import pytest

from src.rendering.audio_presenter import AudioPresenter
from src.theme.asset_manager import AssetManager
from src.theme.assets import AssetPaths


@pytest.fixture
def asset_manager() -> AssetManager:
    """Provide an initialized AssetManager instance."""
    manager = AssetManager(assets=AssetPaths())
    manager.initialize()
    return manager


@pytest.fixture
def presenter(asset_manager: AssetManager) -> AudioPresenter:
    """Provide an uninitialized AudioPresenter instance."""
    return AudioPresenter(asset_manager=asset_manager)


def test_audio_presenter_initialization_failure(
    presenter: AudioPresenter,
) -> None:
    """Presenter should gracefully degrade when mixer init fails."""
    err = RuntimeError("No audio device")
    with patch("pygame.mixer.init", side_effect=err):
        with patch("pygame.mixer.get_init", return_value=False):
            presenter.initialize()
            assert presenter.is_initialized is True
            assert presenter.is_audio_available is False


def test_audio_presenter_successful_initialization(
    presenter: AudioPresenter,
) -> None:
    """Presenter should mark audio available upon successful mixer init."""
    with patch("pygame.mixer.init") as mock_init:
        with patch("pygame.mixer.get_init", return_value=False):
            with patch.object(presenter, "_preload_all_audio") as mock_preload:
                presenter.initialize()
                assert presenter.is_initialized is True
                assert presenter.is_audio_available is True
                mock_init.assert_called_once()
                mock_preload.assert_called_once()


def test_ghost_eaten_round_robin_sequence(
    presenter: AudioPresenter,
) -> None:
    """Eating ghosts should cycle sounds 1 -> 2 -> 3 -> 4 -> 1."""
    presenter.is_audio_available = True
    played_keys: list[str] = []

    def mock_play(key: str) -> None:
        played_keys.append(key)

    presenter.play_sound = mock_play  # type: ignore

    for _ in range(5):
        presenter.play_ghost_eaten()

    assert played_keys == [
        "ghost_eaten_1",
        "ghost_eaten_2",
        "ghost_eaten_3",
        "ghost_eaten_4",
        "ghost_eaten_1",
    ]


def test_sfx_playback_methods(presenter: AudioPresenter) -> None:
    """Convenience methods should dispatch correct sound keys."""
    presenter.is_audio_available = True
    dispatched: list[str] = []
    presenter.play_sound = lambda k: dispatched.append(k)  # type: ignore

    presenter.play_super_pacgum()
    presenter.play_death()
    presenter.play_cheat_freeze()
    presenter.play_cheat_speed()
    presenter.play_cheat_extra_life()

    assert dispatched == [
        "super_pacgum",
        "death",
        "cheat_freeze",
        "cheat_speed",
        "cheat_extra_life",
    ]


def test_exclusive_sound_playback(presenter: AudioPresenter) -> None:
    """Invoking a sound or music must stop all running audio channels."""
    presenter.is_audio_available = True
    stopped: list[bool] = []

    def mock_stop() -> None:
        stopped.append(True)

    presenter._stop_all_audio = mock_stop  # type: ignore

    mock_sound = patch("pygame.mixer.Sound").start()
    presenter._sounds["super_pacgum"] = mock_sound
    presenter.play_sound("super_pacgum")

    assert len(stopped) == 1


def test_sync_music_state_transitions(presenter: AudioPresenter) -> None:
    """sync_music_state should trigger expected music tracks per state."""
    presenter.is_audio_available = True
    tracks_played: list[tuple[str, int]] = []
    stopped: list[bool] = []

    def mock_play_music(t: str, loops: int = -1) -> None:
        tracks_played.append((t, loops))

    presenter.play_music = mock_play_music  # type: ignore
    presenter.stop_music = lambda: stopped.append(True)  # type: ignore

    # MENU state -> menu BGM looping
    presenter.sync_music_state("MENU", False)
    assert tracks_played[-1] == ("menu", -1)

    # Transition to PLAYING state -> game_start music plays once
    presenter.sync_music_state("PLAYING", False)
    assert tracks_played[-1] == ("game_start", 0)

    # PLAYING state with invincibility cheat ON -> invincibility BGM
    presenter.sync_music_state("PLAYING", True)
    assert tracks_played[-1] == ("invincibility", -1)

    # PLAYING state invincibility cheat OFF
    presenter.current_music_track = "invincibility"
    presenter.sync_music_state("PLAYING", False)
    assert len(stopped) == 1

    # GAME_OVER state -> game_over BGM
    presenter.sync_music_state("GAME_OVER", False)
    assert tracks_played[-1] == ("game_over", -1)

    # VICTORY state -> victory BGM
    presenter.sync_music_state("VICTORY", False)
    assert tracks_played[-1] == ("victory", -1)


def test_shutdown_resets_presenter(presenter: AudioPresenter) -> None:
    """Shutdown should clear internal state and quit mixer."""
    presenter.is_initialized = True
    presenter.is_audio_available = True
    presenter.current_music_track = "menu"

    with patch("pygame.mixer.stop") as mock_stop:
        with patch("pygame.mixer.quit") as mock_quit:
            presenter.shutdown()
            assert presenter.is_initialized is False
            assert presenter.is_audio_available is False
            assert presenter.current_music_track is None
            mock_stop.assert_called_once()
            mock_quit.assert_called_once()


def test_asset_manager_extended_audio_lookups(
    asset_manager: AssetManager,
) -> None:
    """AssetManager should resolve all sound and music asset keys."""
    assert (
        asset_manager.get_music("game_start")
        == "assets/audio/start of game music.ogg"
    )
    assert asset_manager.get_music("invincibility") == (
        "assets/audio/Invincibility cheat ON music.mp3"
    )
    assert asset_manager.get_music("game_over") == (
        "assets/audio/gameover screen music.mp3"
    )
    assert asset_manager.get_music("victory") == (
        "assets/audio/victory music.mp3"
    )

    assert asset_manager.get_sound("ghost_eaten_1") == (
        "assets/audio/kill ghost 1.ogg"
    )
    assert asset_manager.get_sound("ghost_eaten_2") == (
        "assets/audio/kill ghost 2.ogg"
    )
    assert asset_manager.get_sound("ghost_eaten_3") == (
        "assets/audio/kill ghost 3.ogg"
    )
    assert asset_manager.get_sound("ghost_eaten_4") == (
        "assets/audio/kill ghost 4.ogg"
    )
    assert asset_manager.get_sound("cheat_freeze") == (
        "assets/audio/freeze cheat ON sound.ogg"
    )
    assert asset_manager.get_sound("cheat_speed") == "assets/audio/speed.ogg"
    assert asset_manager.get_sound("cheat_extra_life") == (
        "assets/audio/Lives inscress sound.mp3"
    )
