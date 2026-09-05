# Audio Module (`src/audio/`)

## 1. Module Overview
The `audio` module abstracts sound effect playback and background music scheduling. It defines `AudioManager`, which enforces an explicit initialization lifecycle, validates non-empty asset identifiers, tracks currently looping music tracks, buffers sound effects, and guarantees clean teardown on application shutdown.

---

## 2. File & Class Breakdown

### `audio_manager.py`
Implements `AudioManager`, managing presentation music tracks and sound-effect playback.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `AudioManager.initialize` | `(self) -> None` | Sets `is_initialized = True`, enabling audio operations. |
| `AudioManager._validate_asset_identifier` | `(asset: str, param_name: str) -> None` | *(Internal helper)* Asserts that the provided audio resource string is non-empty. |
| `AudioManager.play_music` | `(self, music_asset: str, loop: bool = True) -> None` | Commences playback of a background music track after validation. |
| `AudioManager.stop_music` | `(self) -> None` | Halts currently playing background music and clears track state. |
| `AudioManager.play_sound` | `(self, sound_asset: str) -> None` | Triggers a one-shot sound effect (e.g. pellet eat, ghost eaten, death). |
| `AudioManager.clear_played_sounds` | `(self) -> None` | Flushes the internal record of played sound effects. |
| `AudioManager._reset_state` | `(self) -> None` | *(Internal helper)* Clears music and sound buffers and resets initialization flag. |
| `AudioManager.shutdown` | `(self) -> None` | Releases audio channels and resets manager state. |
| `AudioManager._require_initialization` | `(self) -> None` | *(Internal helper)* Raises `RuntimeError` if operations are attempted before `initialize()`. |

