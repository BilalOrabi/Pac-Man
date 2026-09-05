"""Presentation-layer audio manager for Pac-Man music and sound effects."""

import os
from dataclasses import dataclass, field
import pygame

from src.theme.asset_manager import AssetManager
from src.utils.error_logger import ErrorLogger


@dataclass
class AudioPresenter:
    """Manage Pygame presentation audio playback and sound effects."""

    asset_manager: AssetManager
    is_initialized: bool = False
    is_audio_available: bool = False
    current_music_track: str | None = None
    _ghost_kill_index: int = 1
    _last_game_state: str | None = None
    _sounds: dict[str, pygame.mixer.Sound] = field(default_factory=dict)

    def initialize(self) -> None:
        """Initialize the Pygame audio mixer safely."""
        self.is_initialized = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.is_audio_available = True
            self._preload_all_audio()
        except Exception as exc:
            self.is_audio_available = False
            ErrorLogger.log(
                f"Audio hardware initialization failed: {exc}"
            )

    def _preload_all_audio(self) -> None:
        """Preload all music and sound assets into Pygame Sound instances."""
        sound_keys = [
            "super_pacgum",
            "death",
            "ghost_eaten_1",
            "ghost_eaten_2",
            "ghost_eaten_3",
            "ghost_eaten_4",
            "cheat_freeze",
            "cheat_speed",
            "cheat_extra_life",
        ]
        for key in sound_keys:
            self._load_sound_asset(key)

        music_keys = [
            "menu",
            "game_start",
            "game",
            "invincibility",
            "game_over",
            "victory",
        ]
        for key in music_keys:
            self._load_music_asset(key)

    def _load_sound_asset(self, key: str) -> None:
        """Load a single sound asset safely into the sound cache."""
        try:
            path = self.asset_manager.get_sound(key)
            if os.path.isfile(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.8)
                self._sounds[key] = sound
        except Exception as exc:
            ErrorLogger.log(f"Could not preload sound '{key}': {exc}")

    def _load_music_asset(self, key: str) -> None:
        """Load a music asset safely as a Pygame Sound for codec support."""
        try:
            path = self.asset_manager.get_music(key)
            if os.path.isfile(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.7)
                self._sounds[key] = sound
        except Exception as exc:
            ErrorLogger.log(f"Could not preload music '{key}': {exc}")

    def _stop_all_audio(self) -> None:
        """Stop all active audio playback across all channels immediately."""
        if not self.is_audio_available:
            return
        try:
            pygame.mixer.stop()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception as exc:
            ErrorLogger.log(f"Failed to stop audio: {exc}")
        self.current_music_track = None

    def play_music(self, track_key: str, loops: int = -1) -> None:
        """Play a music track exclusively, stopping any running audio."""
        if not self.is_audio_available:
            return

        if self.current_music_track == track_key:
            return

        sound = self._sounds.get(track_key)
        if sound is not None:
            self._stop_all_audio()
            try:
                sound.play(loops=loops)
                self.current_music_track = track_key
            except Exception as exc:
                ErrorLogger.log(
                    f"Failed to play music track '{track_key}': {exc}"
                )
        else:
            # Fallback to streaming music player if not preloaded as Sound
            try:
                track_path = self.asset_manager.get_music(track_key)
                if os.path.isfile(track_path):
                    self._stop_all_audio()
                    pygame.mixer.music.load(track_path)
                    pygame.mixer.music.play(loops=loops)
                    self.current_music_track = track_key
            except Exception as exc:
                ErrorLogger.log(
                    f"Failed streaming music '{track_key}': {exc}"
                )

    def stop_music(self) -> None:
        """Stop any currently playing audio."""
        self._stop_all_audio()

    def play_sound(self, sound_key: str) -> None:
        """Play a sound effect exclusively, cutting off any playing sound."""
        if not self.is_audio_available:
            return

        sound = self._sounds.get(sound_key)
        if sound is not None:
            self._stop_all_audio()
            try:
                sound.play(loops=0)
                self.current_music_track = sound_key
            except Exception as exc:
                ErrorLogger.log(
                    f"Failed to play sound '{sound_key}': {exc}"
                )

    def play_ghost_eaten(self) -> None:
        """Play next ghost kill sound in round-robin sequence (1..4)."""
        sound_key = f"ghost_eaten_{self._ghost_kill_index}"
        self.play_sound(sound_key)
        self._ghost_kill_index = (self._ghost_kill_index % 4) + 1

    def play_super_pacgum(self) -> None:
        """Play the super pacgum eating sound effect."""
        self.play_sound("super_pacgum")

    def play_death(self) -> None:
        """Play the player death sound effect."""
        self.play_sound("death")

    def play_cheat_freeze(self) -> None:
        """Play freeze cheat activated sound."""
        self.play_sound("cheat_freeze")

    def play_cheat_speed(self) -> None:
        """Play speed cheat activated sound."""
        self.play_sound("cheat_speed")

    def play_cheat_extra_life(self) -> None:
        """Play extra life cheat sound."""
        self.play_sound("cheat_extra_life")

    def sync_music_state(
        self,
        game_state_name: str,
        invincibility_active: bool,
    ) -> None:
        """Synchronize audio playback with active game state and cheats."""
        if not self.is_audio_available:
            return

        state_changed = game_state_name != self._last_game_state
        self._last_game_state = game_state_name

        if game_state_name == "MENU":
            if self.current_music_track != "menu":
                self.play_music("menu", loops=-1)
        elif game_state_name in ("ENTER_NAME", "GAME_OVER"):
            if self.current_music_track not in ("game_over", "victory"):
                self.play_music("game_over", loops=-1)
        elif game_state_name == "VICTORY":
            if self.current_music_track != "victory":
                self.play_music("victory", loops=-1)
        elif game_state_name == "PLAYING":
            if state_changed:
                self.play_music("game_start", loops=0)
            elif invincibility_active:
                if self.current_music_track != "invincibility":
                    self.play_music("invincibility", loops=-1)
            elif self.current_music_track == "invincibility":
                self.stop_music()

    def shutdown(self) -> None:
        """Shut down presentation audio cleanly."""
        if self.is_audio_available:
            self._stop_all_audio()
            try:
                pygame.mixer.quit()
            except Exception:
                pass
        self._sounds.clear()
        self.current_music_track = None
        self._last_game_state = None
        self.is_audio_available = False
        self.is_initialized = False
