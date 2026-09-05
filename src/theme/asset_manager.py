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

    def _lookup_asset(
        self, mapping: dict[str, str], key: str, type_name: str
    ) -> str:
        """Lookup an asset path in a mapping or raise a ValueError."""
        self._require_initialization()
        try:
            return mapping[key.lower()]
        except KeyError as error:
            raise ValueError(f"Unknown {type_name}: {key}") from error

    def get_ghost_sprite(self, ghost_color: str) -> str:
        """Return the sprite path for a ghost color."""
        ghost_sprite_paths = {
            "red": self.assets.ghost_red_sprite,
            "pink": self.assets.ghost_pink_sprite,
            "blue": self.assets.ghost_blue_sprite,
            "orange": self.assets.ghost_orange_sprite,
        }
        return self._lookup_asset(
            ghost_sprite_paths, ghost_color, "ghost color"
        )

    def get_font(self, font_type: str) -> str:
        """Return a configured font asset path."""
        font_paths = {
            "menu": self.assets.menu_font,
            "game": self.assets.game_font,
        }
        return self._lookup_asset(font_paths, font_type, "font type")

    def get_music(self, music_type: str) -> str:
        """Return a configured music asset path."""
        music_paths = {
            "menu": self.assets.menu_music,
            "game": self.assets.game_music,
        }
        return self._lookup_asset(music_paths, music_type, "music type")

    def get_sound(self, sound_type: str) -> str:
        """Return a configured sound-effect asset path."""
        sound_paths = {
            "pacgum": self.assets.pacgum_sound,
            "super_pacgum": self.assets.super_pacgum_sound,
            "ghost_eaten": self.assets.ghost_eaten_sound,
            "death": self.assets.death_sound,
        }
        return self._lookup_asset(sound_paths, sound_type, "sound type")

    def get_effect(self, effect_type: str) -> str:
        """Return a configured visual-effect asset path."""
        effect_paths = {
            "power_mode": self.assets.power_mode_effect,
            "death": self.assets.death_effect,
        }
        return self._lookup_asset(effect_paths, effect_type, "effect type")

    def shutdown(self) -> None:
        """Shut down the asset manager."""
        self.is_initialized = False

    def _require_initialization(self) -> None:
        """Ensure the asset manager has been initialized."""
        if not self.is_initialized:
            raise RuntimeError(
                "AssetManager must be initialized before use."
            )
