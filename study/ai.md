# AI Module (`src/ai/`)

## 1. Module Overview
The `ai` module implements the autonomous intelligence and pathfinding algorithms for the four enemy ghosts. It features distinct individual targeting personalities in `CHASE` mode powered by corridor-aware BFS shortest path graph search, evasive distance maximization in `FLEE` mode, and homing corridor routing in `RETURN_HOME` mode, ensuring ghosts navigate maze geometry intelligently without getting trapped behind walls.

---

## 2. File & Class Breakdown

### `ghost_mode.py`
Defines the `GhostMode` enum representing the ghost behavioral state machine.

| Function / Enum Value | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GhostMode.CHASE` | `"chase"` | Normal aggressive pursuit of Pac-Man based on ghost personality targeting. |
| `GhostMode.FLEE` | `"flee"` | Frightened state (blue/vulnerable) retreating away from Pac-Man following power-pellet consumption. |
| `GhostMode.RETURN_HOME` | `"return_home"` | Defeated state returning to home corner at high speed after being eaten. |

---

### `ghost_targeting.py`
Implements `GhostTargeting`, defining the authentic Pac-Man arcade targeting personalities.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GhostTargeting._clamp` | `(coord, maze) -> Coordinate` | *(Internal helper)* Clamps target coordinate inside maze dimensions `0 <= x < width` and `0 <= y < height`. |
| `GhostTargeting._get_direction_offset` | `(direction) -> tuple[int, int]` | *(Internal helper)* Maps `Direction` to `(dx, dy)` orientation vectors. |
| `GhostTargeting._target_pink` | `(px, py, dx, dy) -> Coordinate` | *(Internal helper)* Projects Pinky's ambush target 4 tiles ahead of Pac-Man's orientation vector. |
| `GhostTargeting._target_blue` | `(px, py, dx, dy, ghost, ghosts) -> Coordinate` | *(Internal helper)* Calculates Inky's flanking pivot (2 tiles ahead of Pac-Man reflected across Blinky). |
| `GhostTargeting._target_orange` | `(ghost, px, py) -> Coordinate` | *(Internal helper)* Clyde pursues when > 8 tiles from Pac-Man, but retreats to home corner when closer. |
| `GhostTargeting.get_chase_target` | `(cls, ghost, player, ghosts, maze) -> Coordinate` | Master dispatcher computing the clamped target tile for the specified ghost personality. |

---

### `chase.py`
Implements `ChaseBehavior`, finding the corridor step that minimizes shortest-path distance to target.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `ChaseBehavior._find_walkable_target` | `(maze, target) -> Coordinate` | *(Internal helper)* Resolves target to closest open corridor cell if target tile overlaps a solid wall. |
| `ChaseBehavior._compute_distance_map` | `(maze, target_position) -> dict` | *(Internal helper)* Runs backward BFS flood-fill from target across open corridors to compute exact distances. |
| `ChaseBehavior._get_opposite_direction` | `(direction) -> Direction` | *(Internal helper)* Returns opposite direction to enforce the Pac-Man rule forbidding immediate 180° reversals. |
| `ChaseBehavior._evaluate_candidate_distance` | `(candidate, target, distance_map) -> float` | *(Internal helper)* Retrieves BFS corridor distance with Manhattan fallback if unreached. |
| `ChaseBehavior.get_direction_toward_target` | `(maze, ghost_pos, target_pos, cur_dir) -> Direction` | Selects the non-reversing walkable direction with the shortest corridor distance to target. |

---

### `flee.py`
Implements `FleeBehavior`, directing vulnerable ghosts away from Pac-Man during power mode.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `FleeBehavior._compute_distance_map` | `(maze, target_position) -> dict` | *(Internal helper)* Runs BFS from Pac-Man to evaluate how corridor distances radiate outward. |
| `FleeBehavior._get_opposite_direction` | `(direction) -> Direction` | *(Internal helper)* Identifies reverse direction to prevent backtracking unless cornered. |
| `FleeBehavior._collect_candidates` | `(maze, ghost_pos, target_pos, map) -> list` | *(Internal helper)* Collects all walkable neighbors and their distances from Pac-Man. |
| `FleeBehavior._select_best_flee_direction` | `(candidates, forbidden, cur_dist) -> Direction` | *(Internal helper)* Prioritizes moves that increase or maintain distance from Pac-Man, reversing only when trapped. |
| `FleeBehavior.get_direction_away_from_target` | `(maze, ghost_pos, target_pos, cur_dir) -> Direction` | Determines the safest escape corridor heading away from Pac-Man. |

---

### `return_home.py`
Implements `ReturnHomeBehavior`, routing eaten ghosts back to their spawn corners.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `ReturnHomeBehavior._bfs_search_home` | `(maze, ghost_pos, home_pos) -> Direction \| None` | *(Internal helper)* Performs forward BFS to find the first step along the shortest corridor path home. |
| `ReturnHomeBehavior._greedy_fallback` | `(maze, ghost_pos, home_pos) -> Direction` | *(Internal helper)* Greedy Manhattan distance fallback if path is momentarily unreachable. |
| `ReturnHomeBehavior.get_direction_toward_home` | `(maze, ghost_pos, home_pos) -> Direction` | Returns the next movement direction to return to corner spawn. |

---

### `ghost_ai.py`
Implements `GhostAI`, the high-level decision coordinator switching behaviors based on active `GhostMode`.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GhostAI.set_mode` | `(self, ghost_mode: GhostMode) -> None` | Transitions ghost behavioral state between `CHASE`, `FLEE`, and `RETURN_HOME`. |
| `GhostAI.set_direction` | `(self, direction: Direction) -> None` | Updates the ghost's current facing direction. |
| `GhostAI._resolve_effective_direction` | `(self, current_direction) -> Direction` | *(Internal helper)* Resolves argument direction with fallback to cached instance direction. |
| `GhostAI._dispatch_mode_direction` | `(self, maze, ghost_pos, target_pos, ...) -> Direction` | *(Internal helper)* Routes directional query to the appropriate strategy (`Chase`, `Flee`, `ReturnHome`). |
| `GhostAI.get_next_direction` | `(self, maze, ghost_pos, target_pos, ...) -> Direction` | Computes the ghost's next move by resolving direction and dispatching to mode strategy. |
| `GhostAI.get_current_mode` | `(self) -> GhostMode` | Returns current behavioral mode. |
| `GhostAI.get_current_direction` | `(self) -> Direction` | Returns current movement heading. |
| `GhostAI.reset` | `(self) -> None` | Resets AI state to `GhostMode.CHASE` and `Direction.NONE`. |
