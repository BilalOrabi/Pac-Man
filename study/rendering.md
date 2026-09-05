# Rendering Module (`src/rendering/`)

## 1. Module Overview
The `rendering` module houses the Pygame presentation layer, strictly decoupled from game rules and domain state. Guided by the golden rule that *"Pygame displays the game; Pygame does not define the game"*, this module consumes read-only snapshots from entities and levels to paint 60 FPS graphics. It includes discrete sub-renderers for the maze, player chomping animations, ghost sprites/eyes, in-game HUD, menu overlays, screen state transitions, and presentation audio synthesis.

---

## 2. File & Class Breakdown

### `renderer.py`
Defines abstract presentation contract `Renderer`.

| Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Renderer.initialize` | `(self) -> None` | Sets up presentation surfaces, font caches, and assets. |
| `Renderer.render` | `(self) -> None` | Paints graphics to the target display surface. |
| `Renderer.shutdown` | `(self) -> None` | Releases display textures and resets state. |

---

### `animation.py`
Implements `Animation`, providing time-based progress interpolation.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Animation.__post_init__` | `(self) -> None` | Asserts animation duration is strictly positive (`> 0`). |
| `Animation.progress` | `property -> float` | Returns clamped interpolation progress `[0.0, 1.0]`. |
| `Animation._complete_animation` | `(self) -> None` | *(Internal helper)* Marks animation as fully elapsed and sets `is_finished = True`. |
| `Animation.update` | `(self, elapsed_seconds: float) -> None` | Advances animation timer by delta time. |
| `Animation.reset` | `(self) -> None` | Resets elapsed timer to zero and clears finished flag. |

---

### `effect.py`
Implements `VisualEffect`, encapsulating stateful presentation effects.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `VisualEffect.__post_init__` | `(self) -> None` | Asserts non-empty effect name string. |
| `VisualEffect.is_finished` | `property -> bool` | Queries whether the underlying animation has concluded. |
| `VisualEffect.progress` | `property -> float` | Retrieves normalized completion fraction `[0.0, 1.0]`. |
| `VisualEffect.update` | `(self, elapsed_seconds: float) -> None` | Ticks animation timer if effect is active. |
| `VisualEffect.enable` | `(self) -> None` | Activates effect rendering. |
| `VisualEffect.disable` | `(self) -> None` | Suspends effect updates. |
| `VisualEffect.reset` | `(self) -> None` | Clears animation progress back to starting state. |
| `VisualEffect.restart` | `(self) -> None` | Enables effect and resets animation progress to 0. |

---

### `audio_presenter.py`
Implements `AudioPresenter`, managing Pygame mixer sound channels and soundtrack transitions.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `AudioPresenter.initialize` | `(self) -> None` | Initializes Pygame mixer safely and preloads audio files into memory cache. |
| `AudioPresenter._preload_all_audio` | `(self) -> None` | *(Internal helper)* Preloads all sound effects and music tracks into Pygame `Sound` buffers. |
| `AudioPresenter._load_sound_asset` | `(self, key: str) -> None` | *(Internal helper)* Safely loads and caches individual SFX file with volume 0.8. |
| `AudioPresenter._load_music_asset` | `(self, key: str) -> None` | *(Internal helper)* Safely loads and caches music file with volume 0.7. |
| `AudioPresenter._stop_all_audio` | `(self) -> None` | *(Internal helper)* Halts all active mixer channels and streaming playback immediately. |
| `AudioPresenter.play_music` | `(self, track_key: str, loops: int = -1) -> None` | Exclusively plays music track, stopping conflicting playback. |
| `AudioPresenter.stop_music` | `(self) -> None` | Halts any currently active background music. |
| `AudioPresenter.play_sound` | `(self, sound_key: str) -> None` | Triggers a sound effect exclusively, cutting off any competing sound. |
| `AudioPresenter.play_ghost_eaten` | `(self) -> None` | Plays next ghost kill sound in round-robin sequence (1..4). |
| `AudioPresenter.play_super_pacgum` | `(self) -> None` | Plays super-pacgum ingestion sound. |
| `AudioPresenter.play_death` | `(self) -> None` | Plays player death sound effect. |
| `AudioPresenter.play_cheat_freeze` | `(self) -> None` | Plays ghost freeze cheat activation chime. |
| `AudioPresenter.play_cheat_speed` | `(self) -> None` | Plays speed boost cheat activation sound. |
| `AudioPresenter.play_cheat_extra_life` | `(self) -> None` | Plays extra life cheat awarded chime. |
| `AudioPresenter._sync_playing_audio` | `(self, state_changed: bool, invincibility_active: bool) -> None` | *(Internal helper)* Coordinates game start and invincibility music during active play. |
| `AudioPresenter.sync_music_state` | `(self, game_state_name: str, invincibility_active: bool) -> None` | Switches music automatically based on screen state (`MENU`, `PLAYING`, `GAME_OVER`, etc.). |
| `AudioPresenter.shutdown` | `(self) -> None` | Stops playback, releases audio mixer channels, and purges cache. |

---

### `player_renderer.py`
Implements `PlayerRenderer`, drawing animated 4-directional Pac-Man sprites.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PlayerRenderer.set_player` | `(self, player: Player) -> None` | Binds the player domain entity for rendering. |
| `PlayerRenderer.initialize` | `(self) -> None` | Resolves player sprite asset path via `AssetManager`. |
| `PlayerRenderer._resolve_frame_path` | `(self, dir_folder: str, frame_idx: int) -> str \| None` | *(Internal helper)* Resolves filesystem image path for animated mouth chomp frame. |
| `PlayerRenderer._get_player_frame` | `(self) -> Any` | *(Internal helper)* Computes tick-based frame index (0..3) and retrieves scaled texture from cache. |
| `PlayerRenderer._render_fallback_circle` | `(self, px: int, py: int) -> None` | *(Internal helper)* Draws classic yellow circle if PNG assets are unavailable. |
| `PlayerRenderer._compute_draw_coordinates` | `(self, vx: float, vy: float, margin: int) -> tuple[int, int]` | *(Internal helper)* Converts continuous float coordinates to pixel screen positions. |
| `PlayerRenderer._render_to_surface` | `(self) -> None` | Blits active directional sprite or fallback circle onto target surface. |
| `PlayerRenderer.render` | `(self) -> None` | Validates initialization and assigned player, then renders frame. |
| `PlayerRenderer.shutdown` | `(self) -> None` | Clears frame cache and unbinds player entity. |

---

### `ghost_renderer.py`
Implements `GhostRenderer`, rendering ghost sprites, frightened states, and returning eyes.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GhostRenderer.set_ghost` | `(self, ghost: Ghost) -> None` | Binds ghost entity and retrieves colored sprite asset. |
| `GhostRenderer.initialize` | `(self) -> None` | Initializes asset bindings for the assigned ghost type. |
| `GhostRenderer._resolve_ghost_sprite_path` | `(self, state: GhostState) -> str \| None` | *(Internal helper)* Selects normal color, blue frightened, or returning eyes path. |
| `GhostRenderer._get_ghost_image` | `(self) -> Any` | *(Internal helper)* Loads and caches scaled ghost texture. |
| `GhostRenderer._render_home_eyes` | `(self, center_x: int, center_y: int, radius: int) -> None` | *(Internal helper)* Draws returning ghost eyes traveling back to home corner. |
| `GhostRenderer._render_fallback_body` | `(self, center_x: int, center_y: int, radius: int, state: GhostState) -> None` | *(Internal helper)* Draws procedural ghost body and eyes if sprite images are missing. |
| `GhostRenderer._compute_draw_coordinates` | `(self, vx: float, vy: float, margin: int) -> tuple[int, int]` | *(Internal helper)* Converts continuous sub-tile coordinates into pixel screen positions. |
| `GhostRenderer._render_to_surface` | `(self) -> None` | Renders ghost sprite, eyes, or procedural fallback to target surface. |
| `GhostRenderer.render` | `(self) -> None` | Validates initialization and assigned ghost, then paints frame. |
| `GhostRenderer.shutdown` | `(self) -> None` | Clears sprite texture cache and unbinds ghost. |

---

### `maze_renderer.py`
Implements `MazeRenderer`, displaying walls, background wallpaper, and pellets.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MazeRenderer.set_maze` | `(self, maze: Maze) -> None` | Binds maze model for wall and corridor layout. |
| `MazeRenderer.initialize` | `(self) -> None` | Resolves background image asset path via `AssetManager`. |
| `MazeRenderer._get_scaled_image` | `(self, rel_path: str, size: int) -> Any` | *(Internal helper)* Loads, smoothscales, and caches image texture. |
| `MazeRenderer._resolve_background_path` | `(self) -> str` | *(Internal helper)* Locates wallpaper image file on disk. |
| `MazeRenderer._get_background_surface` | `(self, width: int, height: int) -> Any` | *(Internal helper)* Caches screen-sized wallpaper surface. |
| `MazeRenderer._render_background` | `(self, surf_w: int, surf_h: int) -> None` | *(Internal helper)* Blits background image or fills deep space color. |
| `MazeRenderer._render_maze_backdrop` | `(self) -> None` | *(Internal helper)* Draws translucent dark backing under maze grid. |
| `MazeRenderer._render_cell_walls` | `(self, cell: Any, px: int, py: int, wall_block_img: Any, wall_color: tuple, line_width: int) -> None` | *(Internal helper)* Draws bitmask walls (N, E, S, W) or solid block texture for one cell. |
| `MazeRenderer._render_maze_cells` | `(self, wall_block_img: Any, wall_color: tuple, line_width: int) -> None` | *(Internal helper)* Iterates all cells in maze grid to render walls. |
| `MazeRenderer._render_regular_pacgums` | `(self, pacgums: set, half: int, dot_size: int, dot_img: Any) -> None` | *(Internal helper)* Blits or draws regular pacgums across open corridors. |
| `MazeRenderer._render_super_pacgums` | `(self, super_pacgums: set, half: int, super_dot_size: int, super_dot_img: Any) -> None` | *(Internal helper)* Blits or draws super-pacgums in maze corners. |
| `MazeRenderer._render_pellets` | `(self) -> None` | *(Internal helper)* Orchestrates pellet rendering across the maze. |
| `MazeRenderer._render_to_surface` | `(self) -> None` | Combines background, backdrop, walls, and pellets onto surface. |
| `MazeRenderer.render` | `(self) -> None` | Validates initialization and assigned maze, then paints frame. |
| `MazeRenderer.shutdown` | `(self) -> None` | Clears image and background caches. |

---

### `game_renderer.py`
Implements `GameRenderer`, coordinating all sub-renderers.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameRenderer.initialize` | `(self) -> None` | Initializes maze, player, ghost, and UI renderers. |
| `GameRenderer._recompute_layout` | `(self, surface: object, maze: object) -> None` | *(Internal helper)* Computes optimal cell scaling and center offsets for maze dimensions. |
| `GameRenderer._propagate_surface` | `(self, surface: object) -> None` | *(Internal helper)* Distributes display surface to all child sub-renderers. |
| `GameRenderer.set_surface` | `(self, surface: object) -> None` | Assigns display surface and recalculates screen layout. |
| `GameRenderer.configure_layout` | `(self, cell_size: int, offset_x: int, offset_y: int) -> None` | Propagates grid scaling and offset to spatial sub-renderers. |
| `GameRenderer.set_level` | `(self, level: Level) -> None` | Binds level maze, player, and ghosts, triggering layout recomputation. |
| `GameRenderer.set_player` | `(self, player: Player) -> None` | Forwards player entity to `PlayerRenderer`. |
| `GameRenderer.set_ghosts` | `(self, ghosts: list[Ghost]) -> None` | Binds 4 ghost entities to corresponding `GhostRenderer` instances. |
| `GameRenderer.render` | `(self) -> None` | Sequentially renders maze, player, ghosts, and UI overlays. |
| `GameRenderer.shutdown` | `(self) -> None` | Shuts down all child renderers cleanly. |

---

### `ui_renderer.py`
Implements `UIRenderer`, displaying HUD, menus, pause, victory, and leaderboard screens.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `UIRenderer.initialize` | `(self) -> None` | Resolves menu font, game font, and background assets. |
| `UIRenderer._validate_non_negative_int` | `(value: int, name: str) -> None` | *(Internal helper)* Asserts HUD telemetry value is non-negative. |
| `UIRenderer.set_score` | `(self, score: int) -> None` | Updates current match score display value. |
| `UIRenderer.set_lives` | `(self, lives: int) -> None` | Updates remaining lives display count. |
| `UIRenderer.set_level_number` | `(self, level_number: int) -> None` | Updates current level number display (`> 0`). |
| `UIRenderer.set_message` | `(self, message: str) -> None` | Sets status message banner string. |
| `UIRenderer._get_font` | `(self, size: int) -> pygame.font.Font \| None` | *(Internal helper)* Creates or returns cached bold SysFont. |
| `UIRenderer._dispatch_screen_render` | `(self, state: str, font: pygame.font.Font, header_font: pygame.font.Font \| None) -> None` | *(Internal helper)* Dispatches UI painting based on active application state name. |
| `UIRenderer._render_to_surface` | `(self) -> None` | Obtains fonts and dispatches rendering for the active screen. |
| `UIRenderer._render_hud` | `(self, font: pygame.font.Font) -> None` | *(Internal helper)* Draws top HUD strip (Score, Lives, Level, Timer, Active Cheats). |
| `UIRenderer._render_menu` | `(self, font: pygame.font.Font, header_font: pygame.font.Font) -> None` | *(Internal helper)* Draws main menu buttons or leaderboard highscore table. |
| `UIRenderer._render_pause_overlay` | `(self, font: pygame.font.Font, header_font: pygame.font.Font) -> None` | *(Internal helper)* Draws translucent paused dialog with resume instructions. |
| `UIRenderer._render_game_over` | `(self, font: pygame.font.Font, header_font: pygame.font.Font) -> None` | *(Internal helper)* Draws game over banner, final score, and restart options. |
| `UIRenderer._render_victory` | `(self, font: pygame.font.Font, header_font: pygame.font.Font) -> None` | *(Internal helper)* Draws victory celebration screen with final campaign score. |
| `UIRenderer._render_enter_name` | `(self, font: pygame.font.Font, header_font: pygame.font.Font) -> None` | *(Internal helper)* Draws arcade name input boxes for high-score submission. |
| `UIRenderer.render` | `(self) -> None` | Validates initialization and renders current UI frame. |
| `UIRenderer.shutdown` | `(self) -> None` | Clears background cache and unbinds surface. |

