# Config Module (`src/config/`)

## 1. Module Overview
The `config` module loads, sanitizes, and validates game parameters from `config.json` in accordance with Chapters 5.1–5.3 of the 42 School subject. It supports both strict schema validation and fault-tolerant safe fallback parsing. Features include stripping full-line and inline `#` and `//` comments, clamping out-of-bounds maze dimensions (`5 <= width <= 35`, `5 <= height <= 24`) with warnings logged to `errors.log`, and locking speeds to stable 60 FPS physics constants.

---

## 2. File & Class Breakdown

### `game_config.py`
Defines typed immutable domain configuration data models.

| Function / Method / Class | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `LevelConfig._validate_dimension` | `(value: int, axis: str) -> None` | *(Internal helper)* Asserts a grid dimension (width or height) is strictly positive (`> 0`). |
| `LevelConfig.__post_init__` | `(self) -> None` | Validates width and height during dataclass instantiation. |
| `GameConfig._validate_score_and_lives` | `(self) -> None` | *(Internal helper)* Validates non-empty filename, lives `> 0`, non-negative score values, and positive level max time. |
| `GameConfig._validate_speeds` | `(self) -> None` | *(Internal helper)* Asserts player speed, ghost speeds, and power mode duration are strictly positive. |
| `GameConfig._validate_levels` | `(self) -> None` | *(Internal helper)* Asserts at least one valid level configuration is provided. |
| `GameConfig.__post_init__` | `(self) -> None` | Orchestrates complete domain integrity validation on loaded configuration. |

---

### `config_loader.py`
Implements `ConfigLoader`, handling JSON disk I/O, comment stripping, bounds clamping, and default fallbacks.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `ConfigError` | `Exception` | Custom domain exception raised when configuration fails strict validation. |
| `ConfigLoader.load` | `(path: str \| Path, fallback_to_defaults: bool = False) -> GameConfig` | Loads JSON configuration file in either strict or fault-tolerant fallback mode. |
| `ConfigLoader._read_json` | `(path: Path) -> dict[str, Any]` | *(Internal helper)* Reads disk file, discards `#` and `//` comments, and parses JSON object. |
| `ConfigLoader._safe_int` | `(data: dict, key: str, default: int, min_val: int = 0) -> int` | *(Internal helper)* Safely reads integer or logs warning and returns calibrated default. |
| `ConfigLoader._safe_float` | `(data: dict, key: str, default: float) -> float` | *(Internal helper)* Safely reads positive float or logs warning and returns calibrated default. |
| `ConfigLoader._safe_highscore_filename` | `(data: dict[str, Any]) -> str` | *(Internal helper)* Validates non-empty highscore filename or falls back to `"highscores.json"`. |
| `ConfigLoader._safe_level_dimension` | `(w: int, h: int, idx: int) -> tuple[int, int]` | *(Internal helper)* Clamps level dimensions to 5..35 width and 5..24 height bounds with `errors.log` notice. |
| `ConfigLoader._parse_safe_single_level` | `(idx: int, lvl: Any) -> LevelConfig \| None` | *(Internal helper)* Parses and bounds a single level dictionary entry. |
| `ConfigLoader._safe_levels` | `(data: dict[str, Any]) -> tuple[LevelConfig, ...]` | *(Internal helper)* Constructs level collection with clamping or defaults to 10 standard 19x21 levels. |
| `ConfigLoader._build_config_safe` | `(data: dict[str, Any]) -> GameConfig` | *(Internal helper)* Constructs a fault-tolerant configuration, guaranteeing zero crashes from faulty JSON. |
| `ConfigLoader._build_config` | `(data: dict[str, Any]) -> GameConfig` | *(Internal helper)* Constructs configuration enforcing strict type and positive-value constraints. |
| `ConfigLoader._get_string` | `(data: dict[str, Any], key: str) -> str` | *(Internal helper)* Strict reader asserting key exists and is a non-empty string. |
| `ConfigLoader._get_int` | `(data: dict[str, Any], key: str) -> int` | *(Internal helper)* Strict reader asserting key exists and is an integer. |
| `ConfigLoader._get_positive_int` | `(data: dict[str, Any], key: str) -> int` | *(Internal helper)* Strict reader asserting key exists and is an integer `> 0`. |
| `ConfigLoader._get_non_negative_int` | `(data: dict[str, Any], key: str) -> int` | *(Internal helper)* Strict reader asserting key exists and is an integer `>= 0`. |
| `ConfigLoader._get_positive_float` | `(data: dict[str, Any], key: str) -> float` | *(Internal helper)* Strict reader asserting key exists and is a number `> 0`. |
| `ConfigLoader._parse_single_level` | `(index: int, raw_level: Any) -> LevelConfig` | *(Internal helper)* Strict level parser asserting dimensions and clamping bounds. |
| `ConfigLoader._get_levels` | `(data: dict[str, Any]) -> tuple[LevelConfig, ...]` | *(Internal helper)* Strict reader parsing non-empty list of level configurations. |

