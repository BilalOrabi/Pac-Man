"""Audio management for the Pac-Man presentation layer."""

from dataclasses import dataclass, field


@dataclass
class AudioManager:
    """Manage game music and sound effects."""

    is_initialized: bool = False
    current_music: str | None = None
    played_sounds: list[str] = field(default_factory=list)

    def initialize(self) -> None:
        """Initialize the audio manager."""
        self.is_initialized = True

    def play_music(self, music_asset: str, loop: bool = True) -> None:
        """Start playing a music asset."""
        self._require_initialization()

        if not music_asset:
            raise ValueError("music_asset cannot be empty.")

        self.current_music = music_asset

    def stop_music(self) -> None:
        """Stop the currently playing music."""
        self._require_initialization()

        self.current_music = None

    def play_sound(self, sound_asset: str) -> None:
        """Play a sound-effect asset."""
        self._require_initialization()

        if not sound_asset:
            raise ValueError("sound_asset cannot be empty.")

        self.played_sounds.append(sound_asset)

    def clear_played_sounds(self) -> None:
        """Clear the record of played sound effects."""
        self.played_sounds.clear()

    def shutdown(self) -> None:
        """Shut down the audio manager."""
        self.current_music = None
        self.played_sounds.clear()
        self.is_initialized = False

    def _require_initialization(self) -> None:
        """Ensure the audio manager has been initialized."""
        if not self.is_initialized:
            raise RuntimeError(
                "AudioManager must be initialized before use."
            )
