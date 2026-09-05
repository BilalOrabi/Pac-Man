# World Module (`src/world/`)

## 1. Module Overview
The `world` module manages the game's level instances, spatial composition, and progression life-cycle. It unites the maze geometry, the player, the four ghosts, and pellet distribution into a coherent `Level` runtime state, while `GameWorld` tracks the active level index, preserves player score/lives across transitions, and coordinates overall level progression.

---

## 2. File & Class Breakdown

### `level.py`
Defines `Level`, which encapsulates the runtime state, pellet sets, and timers for a single level.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Level.__post_init__` | `(self) -> None` | Synchronizes total `remaining_pacgums` counter with the initial count of pellets and super-pacgums. |
| `Level.update_time` | `(self, elapsed_time: float) -> None` | Accumulates active gameplay time if the level is not yet completed; rejects negative deltas. |
| `Level.consume_pacgum` | `(self) -> None` | Decrements `remaining_pacgums` counter by 1 and marks `completed = True` when all pellets are eaten. |
| `Level._process_pellet_consumption` | `(self, position, pellet_set) -> None` | *(Internal helper)* Removes eaten pellet from set, invokes counter decrement, and checks level completion. |
| `Level.consume_pacgum_at` | `(self, position: Coordinate) -> str \| None` | Consumes pellet at tile coordinate and returns pellet type (`"super_pacgum"`, `"pacgum"`, or `None`). |
| `Level.is_time_expired` | `(self, maximum_level_time: float) -> bool` | Checks whether elapsed level time has reached or exceeded the configured limit. |
| `Level.reset_timer` | `(self) -> None` | Resets the elapsed level timer back to zero (e.g. after level restart). |

---

### `game_world.py`
Defines `GameWorld`, managing progression across the game's sequence of levels.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameWorld.start` | `(self) -> Level` | Boots level 0, creates entities and maze, and sets `start_called = True`. |
| `GameWorld._get_preserved_player_stats` | `(self) -> tuple[int, int]` | *(Internal helper)* Extracts current player score and remaining lives to carry over to the next level. |
| `GameWorld.advance_to_next_level` | `(self) -> Level \| None` | Instantiates next level index and transfers preserved score and lives into the new player entity. |
| `GameWorld.has_completed_all_levels` | `(self) -> bool` | Evaluates if the player finished the final configured level, triggering overall victory. |
| `GameWorld.update` | `(self, elapsed_seconds: float) -> None` | Forwards tick delta-time to the active level timer. |
| `GameWorld._create_level` | `(self, level_index: int) -> Level` | *(Internal helper)* Delegates level creation to `LevelFactory` with level-specific configuration and seed. |

---

### `level_factory.py`
Implements `LevelFactory`, responsible for procedurally generating and wiring all level components.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `LevelFactory._place_super_pacgums` | `(maze: Maze) -> set[Coordinate]` | *(Internal helper)* Identifies open maze corners to place the 4 super-pacgums. |
| `LevelFactory._distribute_pacgums` | `(maze, player_pos, super_pacgums, ...) -> set[Coordinate]` | *(Internal helper)* Randomly distributes regular pacgums across open corridors (excluding player spawn and corners). |
| `LevelFactory._create_player` | `(self, maze: Maze) -> Player` | *(Internal helper)* Instantiates the player entity positioned at `maze.entry`. |
| `LevelFactory._create_ghosts` | `(self, maze: Maze) -> list[Ghost]` | *(Internal helper)* Instantiates the 4 ghosts (Red, Pink, Blue, Orange) in the 4 corners of the maze. |
| `LevelFactory.create_level` | `(self, level_number, level_configuration, ...) -> Level` | High-level builder that generates the maze, entities, and pellets into a ready-to-play `Level`. |
