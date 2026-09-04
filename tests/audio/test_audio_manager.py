"""Tests for the Pac-Man audio manager."""

import pytest

from src.audio.audio_manager import AudioManager


def test_audio_manager_starts_uninitialized() -> None:
    """AudioManager should initially be uninitialized."""
    audio_manager = AudioManager()

    assert audio_manager.is_initialized is False
    assert audio_manager.current_music is None
    assert audio_manager.played_sounds == []


def test_initialize_initializes_audio_manager() -> None:
    """Initialize should activate the audio manager."""
    audio_manager = AudioManager()

    audio_manager.initialize()

    assert audio_manager.is_initialized is True


def test_play_music_sets_current_music() -> None:
    """Playing music should store the current music asset."""
    audio_manager = AudioManager()
    audio_manager.initialize()

    audio_manager.play_music("assets/sounds/game_start.wav")

    assert (
        audio_manager.current_music
        == "assets/sounds/game_start.wav"
    )


def test_stop_music_clears_current_music() -> None:
    """Stopping music should clear the current music asset."""
    audio_manager = AudioManager()
    audio_manager.initialize()
    audio_manager.play_music("assets/sounds/game_start.wav")

    audio_manager.stop_music()

    assert audio_manager.current_music is None


def test_play_sound_records_sound_asset() -> None:
    """Playing a sound should record its asset."""
    audio_manager = AudioManager()
    audio_manager.initialize()

    audio_manager.play_sound("assets/sounds/waka.wav")

    assert audio_manager.played_sounds == [
        "assets/sounds/waka.wav"
    ]


def test_multiple_sounds_are_recorded_in_order() -> None:
    """Sound effects should be recorded in playback order."""
    audio_manager = AudioManager()
    audio_manager.initialize()

    audio_manager.play_sound("assets/sounds/waka.wav")
    audio_manager.play_sound("assets/sounds/power_mode.wav")

    assert audio_manager.played_sounds == [
        "assets/sounds/waka.wav",
        "assets/sounds/power_mode.wav",
    ]


def test_clear_played_sounds_removes_recorded_sounds() -> None:
    """Clearing sounds should remove the playback history."""
    audio_manager = AudioManager()
    audio_manager.initialize()
    audio_manager.play_sound("assets/sounds/waka.wav")

    audio_manager.clear_played_sounds()

    assert audio_manager.played_sounds == []


def test_play_music_requires_initialization() -> None:
    """Music should not play before initialization."""
    audio_manager = AudioManager()

    with pytest.raises(RuntimeError):
        audio_manager.play_music("assets/sounds/game_start.wav")


def test_stop_music_requires_initialization() -> None:
    """Stopping music should require initialization."""
    audio_manager = AudioManager()

    with pytest.raises(RuntimeError):
        audio_manager.stop_music()


def test_play_sound_requires_initialization() -> None:
    """Sound effects should not play before initialization."""
    audio_manager = AudioManager()

    with pytest.raises(RuntimeError):
        audio_manager.play_sound("assets/sounds/waka.wav")


def test_empty_music_asset_is_rejected() -> None:
    """An empty music asset should be rejected."""
    audio_manager = AudioManager()
    audio_manager.initialize()

    with pytest.raises(ValueError):
        audio_manager.play_music("")


def test_empty_sound_asset_is_rejected() -> None:
    """An empty sound asset should be rejected."""
    audio_manager = AudioManager()
    audio_manager.initialize()

    with pytest.raises(ValueError):
        audio_manager.play_sound("")


def test_shutdown_resets_audio_manager() -> None:
    """Shutdown should reset the audio manager."""
    audio_manager = AudioManager()
    audio_manager.initialize()
    audio_manager.play_music("assets/sounds/game_start.wav")
    audio_manager.play_sound("assets/sounds/waka.wav")

    audio_manager.shutdown()

    assert audio_manager.is_initialized is False
    assert audio_manager.current_music is None
    assert audio_manager.played_sounds == []
