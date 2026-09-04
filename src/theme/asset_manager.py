"""Asset management for the Pac-Man presentation layer."""

from dataclasses import dataclass, field

from src.theme.assets import AssetPaths, DEFAULT_ASSETS


@dataclass
class AssetManager:
    """Provide centralized access to presentation assets."""

    assets: AssetPaths = field(
        default_factory=lambda: DEFAULT_ASSETS
    )
    is_initialized: bool = False

    def initialize(self) -> None:
        """Initialize the asset manager."""
        self.is_initialized = True

    def get_background(self) -> str:
        """Return the main background asset path."""
        self._require_initialization()
        return self.assets.background

    def get_player_sprite(self) -> str:
        """Return the player sprite asset path."""
        self._require_initialization()
        return self.assets.player_sprite

    def get_ghost_sprite(self, ghost_color: str) -> str:
        """Return the sprite path for a ghost color."""
        self._require_initialization()

        ghost_sprite_paths = {
            "red": self.assets.ghost_red_sprite,
            "pink": self.assets.ghost_pink_sprite,
            "blue": self.assets.ghost_blue_sprite,
            "orange": self.assets.ghost_orange_sprite,
        }

        try:
            return ghost_sprite_paths[ghost_color.lower()]
        except KeyError as error:
            raise ValueError(
                f"Unknown ghost color: {ghost_color}"
            ) from error

    def get_font(self, font_type: str) -> str:
        """Return a configured font asset path."""
        self._require_initialization()

        font_paths = {
            "menu": self.assets.menu_font,
            "game": self.assets.game_font,
        }

        try:
            return font_paths[font_type.lower()]
        except KeyError as error:
            raise ValueError(
                f"Unknown font type: {font_type}"
            ) from error

    def get_music(self, music_type: str) -> str:
        """Return a configured music asset path."""
        self._require_initialization()

        music_paths = {
            "menu": self.assets.menu_music,
            "game": self.assets.game_music,
        }

        try:
            return music_paths[music_type.lower()]
        except KeyError as error:
            raise ValueError(
                f"Unknown music type: {music_type}"
            ) from error

    def get_sound(self, sound_type: str) -> str:
        """Return a configured sound-effect asset path."""
        self._require_initialization()

        sound_paths = {
            "pacgum": self.assets.pacgum_sound,
            "super_pacgum": self.assets.super_pacgum_sound,
            "ghost_eaten": self.assets.ghost_eaten_sound,
            "death": self.assets.death_sound,
        }

        try:
            return sound_paths[sound_type.lower()]
        except KeyError as error:
            raise ValueError(
                f"Unknown sound type: {sound_type}"
            ) from error

    def get_effect(self, effect_type: str) -> str:
        """Return a configured visual-effect asset path."""
        self._require_initialization()

        effect_paths = {
            "power_mode": self.assets.power_mode_effect,
            "death": self.assets.death_effect,
        }

        try:
            return effect_paths[effect_type.lower()]
        except KeyError as error:
            raise ValueError(
                f"Unknown effect type: {effect_type}"
            ) from error

    def shutdown(self) -> None:
        """Shut down the asset manager."""
        self.is_initialized = False

    def _require_initialization(self) -> None:
        """Ensure the asset manager has been initialized."""
        if not self.is_initialized:
            raise RuntimeError(
                "AssetManager must be initialized before use."
            )
