# Systems Module (`src/systems/`)

## 1. Module Overview
The `systems` module houses the decoupled rule engines and physics calculations of the Pac-Man domain. It operates strictly on domain entities and maze models without depending on presentation or graphics, implementing spatial collision detection, grid movement steps, power-pellet countdown timers, score calculation, lives tracking, level transitions, and elapsed level timers.

---

## 2. File & Class Breakdown

### `collision.py`
Implements `CollisionSystem`, evaluating tile-to-tile movement clearance and entity-to-entity contact.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `CollisionSystem.can_move_to` | `(entity, target_pos, maze) -> bool` | Checks whether an entity can legally step from current tile to target tile. |
| `CollisionSystem.move_if_valid` | `(entity, target_pos, maze) -> bool` | Updates entity position if target cell is open and walkable; returns boolean success. |
| `CollisionSystem._check_visual_collision` | `(entity_a, entity_b) -> bool` | *(Internal helper)* Computes Euclidean distance between sub-tile visual coordinates `< 0.36` tile radius. |
| `CollisionSystem.check_entity_collision` | `(entity_a, entity_b) -> bool` | True if entities share the exact grid cell OR are within visual collision range. |

---

### `movement.py`
Implements `MovementSystem`, calculating directional target grid positions.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MovementSystem._get_direction_offset` | `(direction: Direction) -> Coordinate` | *(Internal helper)* Maps `Direction` to integer `(dx, dy)` grid offsets. |
| `MovementSystem.calculate_next_position` | `(entity, maze) -> Coordinate` | Calculates the adjacent grid coordinate in the entity's current heading. |
| `MovementSystem.move_entity` | `(entity, maze) -> None` | Steps entity to the calculated next grid coordinate. |

---

### `power_mode.py`
Implements `PowerModeSystem`, managing the vulnerability window triggered by super-pacgums.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PowerModeSystem.__init__` | `(self, duration: float) -> None` | Initializes system with maximum duration; rejects non-positive durations. |
| `PowerModeSystem.activate` | `(self) -> None` | Sets power mode state to `ACTIVE` and resets remaining timer to full duration. |
| `PowerModeSystem.update` | `(self, elapsed_seconds: float) -> None` | Counts down remaining time; deactivates to `INACTIVE` when reaching 0. |
| `PowerModeSystem.deactivate` | `(self) -> None` | Instantly resets timer to 0 and marks state as `INACTIVE`. |

---

### `scoring.py`
Implements `ScoringSystem`, defining points awarded for gameplay achievements.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `ScoringSystem.calculate_pacgum_score` | `(self) -> int` | Returns points for standard pacgum consumption (default: 10). |
| `ScoringSystem.calculate_super_pacgum_score` | `(self) -> int` | Returns points for super-pacgum consumption (default: 50). |
| `ScoringSystem.calculate_ghost_score` | `(self) -> int` | Returns points for eating a vulnerable ghost in flee mode (default: 200). |

---

### `lives.py`
Implements `LivesSystem`, tracking Pac-Man's life pool.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `LivesSystem.lose_life` | `(self) -> bool` | Deducts 1 life and returns boolean indicating if player is still alive (`> 0`). |
| `LivesSystem.add_life` | `(self) -> None` | Increments lives by 1 (e.g. from extra life cheat). |
| `LivesSystem.reset` | `(self, starting_lives: int) -> None` | Resets life pool back to configured starting value. |

---

### `level_progression.py`
Implements `LevelProgressionSystem`, deciding when to advance levels or trigger victory.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `LevelProgressionSystem.progress` | `(self, game_world: GameWorld) -> LevelProgressionResult` | Evaluates level completion and triggers advancement to next level or declares overall victory. |
| `LevelProgressionSystem.is_level_completed` | `(level: Level) -> bool` | Queries whether the active level has been flagged complete. |

---

### `timer_system.py`
Implements `TimerSystem`, enforcing level time limits.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `TimerSystem.update` | `(self, level, elapsed_time) -> None` | Advances the level's elapsed active gameplay timer. |
| `TimerSystem.is_expired` | `(self, level: Level) -> bool` | Checks whether elapsed level time has reached the maximum permitted time limit. |
| `TimerSystem.reset` | `(self, level: Level) -> None` | Clears level timer back to zero. |
