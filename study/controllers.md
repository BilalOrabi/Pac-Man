# Controllers Module (`src/controllers/`)

## 1. Module Overview
The `controllers` module orchestrates gameplay interactions, actor movement pacing, and decision cycles. It acts as the bridge between input/AI intentions and domain system executions. It houses `PlayerController` (handling player turning, corner buffering, and reversals), `GhostController` (driving individual ghost pathfinding steps and respawn cooldowns), and `GameplayController` (the central game loop coordinator managing sub-tick physics pacing, pellet eating, scatter/chase waves, entity collisions, lives deductions, and audio events).

---

## 2. File & Class Breakdown

### `player_controller.py`
Implements `PlayerController`, managing directional input handling, corner buffering, and instantaneous direction reversals.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PlayerController._reverse_movement` | `(self, direction: Direction) -> None` | *(Internal helper)* Instantly reverses player heading and inverts sub-tile interpolation progress. |
| `PlayerController._is_opposite_direction` | `(current: Direction, target: Direction) -> bool` | *(Internal helper)* Checks whether the desired direction directly opposes the active heading. |
| `PlayerController.handle_action` | `(self, action: InputAction, maze: Maze \| None = None) -> None` | Ingests an input action, performing an instant 180° turnaround or buffering upcoming perpendicular turns. |
| `PlayerController._apply_buffered_direction` | `(self, maze: Maze) -> None` | *(Internal helper)* Applies queued turn direction as soon as the corridor opening becomes walkable. |
| `PlayerController.update` | `(self, maze: Maze) -> None` | Calculates next grid tile and executes discrete tile step if walkable. |
| `PlayerController._can_move_in_direction` | `(self, direction: Direction, maze: Maze, from_position: tuple[int, int] \| None = None) -> bool` | *(Internal helper)* Checks collision clearance for a prospective step in the specified direction. |
| `PlayerController._get_direction_for_action` | `(action: InputAction) -> Direction \| None` | *(Internal helper)* Maps user input actions (`MOVE_UP`, `MOVE_LEFT`, etc.) to spatial `Direction` enums. |

---

### `ghost_controller.py`
Implements `GhostController`, directing individual ghost movement decisions and respawn cycles.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GhostController._is_on_respawn_cooldown` | `(self) -> bool` | *(Internal helper)* Checks if ghost is resting on its home tile during its 5-second respawn penalty. |
| `GhostController._map_ghost_state_to_mode` | `(state: GhostState) -> GhostMode` | *(Internal helper)* Translates entity state (`CHASE`, `FLEE`, `RETURN_HOME`) to AI mode representation. |
| `GhostController._get_valid_target_position` | `(self) -> Coordinate \| None` | *(Internal helper)* Safely accesses and validates the ghost's prepared target grid coordinate. |
| `GhostController._update_ai_direction` | `(self, maze: Maze, target_position: Coordinate \| None) -> None` | *(Internal helper)* Invokes `GhostAI` to resolve the optimal next corridor heading towards its target. |
| `GhostController._check_home_arrival` | `(self) -> None` | *(Internal helper)* Detects when an eaten ghost successfully reaches home and activates its 5-second cooldown. |
| `GhostController.prepare_next_step` | `(self, maze: Maze, target_position: Coordinate \| None = None) -> None` | Precomputes next valid target tile in advance for sub-tile smooth visual interpolation. |
| `GhostController.update` | `(self, maze: Maze, target_position: Coordinate \| None = None) -> None` | Steps ghost into its prepared target tile and schedules the subsequent pathfinding evaluation. |

---

### `gameplay_controller.py`
Implements `GameplayController`, the central coordinator uniting all actors, timers, rules, and collision events.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameplayController.pop_audio_events` | `(self) -> list[str]` | Drains and returns queued audio event triggers (`"pacgum"`, `"super_pacgum"`, `"ghost_eaten"`, `"death"`). |
| `GameplayController._check_level_skip` | `(self, level: Level) -> bool` | *(Internal helper)* Evaluates cheat key requests to immediately mark current level completed. |
| `GameplayController._sync_power_mode` | `(self, player: Any) -> None` | *(Internal helper)* Synchronizes player invulnerability state with active cheat toggles and power mode timers. |
| `GameplayController._sync_player_turnaround` | `(self, player: Any, step_interval: float) -> None` | *(Internal helper)* Resynchronizes movement accumulator when player reverses direction mid-tile. |
| `GameplayController._prepare_player_target` | `(self, player: Any, level: Level, cur_dir: Direction) -> tuple[bool, Direction]` | *(Internal helper)* Resolves corridor clearance or buffered turns to assign upcoming target position. |
| `GameplayController._step_player_pacing` | `(self, player: Any, level: Level, elapsed: float) -> tuple[bool, float]` | *(Internal helper)* Accumulates elapsed time against calibrated step intervals for 60 FPS sub-tile pacing. |
| `GameplayController._execute_player_step` | `(self, player: Any, level: Level, step_interval: float) -> None` | *(Internal helper)* Executes physical tile arrival and prepares subsequent target cell. |
| `GameplayController._consume_pellets` | `(self, level: Level, player: Any) -> None` | *(Internal helper)* Tests Pac-Man's tile for pellets, awards points, triggers power mode, and queues audio. |
| `GameplayController._update_wave_timer` | `(self, player: Any, elapsed: float) -> None` | *(Internal helper)* Alternates global ghost behavior between 20-second Chase and 6-second Scatter waves. |
| `GameplayController._resolve_ghost_target` | `(self, ghost: Any, state: Any, player: Any, level: Level) -> tuple[int, int] \| None` | *(Internal helper)* Selects target tile based on ghost personality (Blinky, Pinky, Inky, Clyde) and active wave. |
| `GameplayController._update_single_ghost` | `(self, idx: int, gc: GhostController, level: Level, player: Any, elapsed: float) -> None` | *(Internal helper)* Advances step timer, calculates sub-tile progress, and updates individual ghost. |
| `GameplayController._update_ghosts` | `(self, level: Level, player: Any, elapsed: float) -> None` | *(Internal helper)* Iterates all ghosts if ghost freeze cheat is inactive. |
| `GameplayController._sync_ghost_flee_states` | `(self, ghosts: list[Any], is_powered: bool) -> None` | *(Internal helper)* Flips ghosts to `FLEE` mode and 180° reversals upon super-pacgum activation, or restores `CHASE`. |
| `GameplayController._apply_player_death` | `(self, player: Any, entry_pos: tuple[int, int]) -> None` | *(Internal helper)* Deducts 1 life, plays death sound, and resets player position to maze entry. |
| `GameplayController._process_ghost_collision` | `(self, player: Any, ghost: Any, level: Level, is_powered: bool) -> None` | *(Internal helper)* Handles ghost eaten (+200 pts, return home) or Pac-Man death penalty. |
| `GameplayController._trigger_ghost_home_cooldown` | `(ghost: Any) -> None` | *(Internal helper)* Sets 5.0s respawn cooldown once returning ghost reaches its home corner. |
| `GameplayController._handle_entity_collisions` | `(self, level: Level, player: Any) -> None` | *(Internal helper)* Detects entity-to-entity overlaps and dispatches collision outcomes. |
| `GameplayController.update` | `(self, level: Level, elapsed_seconds: float) -> None` | Master tick updating level timer, power timer, player pacing, pellet eating, ghost AI, and collisions. |
| `GameplayController._reset_player_binding` | `(self, player: Any) -> None` | *(Internal helper)* Rebinds and clears movement buffers for player entity on level reset. |
| `GameplayController._reset_ghost_bindings` | `(self, ghosts: list[Any]) -> None` | *(Internal helper)* Rebinds and resets ghosts and controllers on level reset. |
| `GameplayController.reset_level` | `(self, level: Level) -> None` | Resets all sub-tick timers, waves, and entity states for entering a new level. |

