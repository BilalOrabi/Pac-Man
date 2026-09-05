# Theme Module (`src/theme/`)

## 1. Module Overview
The `theme` module isolates visual styling, color palettes, fonts, music, and sprite assets from domain logic in strict compliance with Chapter 2 of the project memory. It establishes the single centralized access point `AssetManager`, ensuring renderers never construct raw asset file paths and gameplay code never loads graphical resources. This architecture enables effortless swapping of themes (e.g., Classic 80s arcade vs. modern variants) without editing gameplay mechanics.

---

## 2. File & Class Breakdown

### `assets.py`
Defines default relative filesystem paths for game assets.

| Function / Method / Class | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `_resolve_menu_music` | `() -> str` | *(Internal helper)* Verifies filesystem presence of `"menu music.mp3"` or falls back to `".ogg"`. |
| `AssetPaths` | `@dataclass(frozen=True)` | Immutable structure storing relative filepaths for images, fonts, music, and sounds. |
| `DEFAULT_ASSETS` | `AssetPaths` | Default constant instance of `AssetPaths` pointing to project assets. |

---

### `theme.py`
Defines visual configurations, palette themes, and categorized resource collections.

| Class | Attributes | Purpose & Job |
| :--- | :--- | :--- |
| `ColorTheme` | RGB tuples | Centralizes color palette definitions (background, maze walls, Pac-Man, ghosts, HUD). |
| `FontTheme` | File paths | Maps font categories (game font, UI font, score font) to TTF assets. |
| `ImageAssets` | File paths | References image textures (background, Pac-Man sprite, 4 ghost sprites). |
| `AudioAssets` | File paths | References audio tracks (menu music, gameplay, cheats, deaths, eating sfx). |
| `EffectAssets` | File paths | Defines particle/animation effects for power mode and death. |
| `Theme` | Composite container | Root theme aggregating colors, fonts, images, audio, and visual effects. |

---

### `asset_manager.py`
Implements `AssetManager`, the centralized presentation gateway.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `AssetManager.initialize` | `(self) -> None` | Marks the asset manager initialized and ready for service. |
| `AssetManager.get_background` | `(self) -> str` | Returns the resolved background image filepath. |
| `AssetManager.get_player_sprite` | `(self) -> str` | Returns the player sprite image filepath. |
| `AssetManager._lookup_asset` | `(self, mapping: dict, key: str, type_name: str) -> str` | *(Internal helper)* Resolves key in asset lookup dictionary or raises descriptive `ValueError`. |
| `AssetManager.get_ghost_sprite` | `(self, ghost_color: str) -> str` | Retrieves ghost sprite path by color name (`red`, `pink`, `blue`, `orange`). |
| `AssetManager.get_font` | `(self, font_type: str) -> str` | Retrieves font path by category (`menu`, `game`). |
| `AssetManager.get_music` | `(self, music_type: str) -> str` | Retrieves soundtrack path (`menu`, `game`, `game_start`, `invincibility`, `game_over`, `victory`). |
| `AssetManager.get_sound` | `(self, sound_type: str) -> str` | Retrieves sound effect path (`super_pacgum`, `ghost_eaten`, `death`, cheat sfx). |
| `AssetManager._validate_effect_type` | `(effect_type: str) -> None` | *(Internal helper)* Asserts effect type is valid (`power_mode`, `death`). |
| `AssetManager.get_effect` | `(self, effect_type: str) -> str` | Retrieves visual effect path. |
| `AssetManager.shutdown` | `(self) -> None` | Resets initialization status. |
| `AssetManager._require_initialization` | `(self) -> None` | *(Internal helper)* Enforces `initialize()` lifecycle contract before asset retrieval. |

