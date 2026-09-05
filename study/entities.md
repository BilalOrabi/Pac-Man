# Entities Module (`src/entities/`)


## 1. Module Overview
The `entities` module defines the foundational domain objects representing active game participants (Pac-Man and the four Ghosts), along with their spatial representations and movement directions. It encapsulates core entity attributes like grid positions, movement progress, lives, score, and state machines, keeping domain logic strictly decoupled from Pygame rendering.

---


## 2. File & Class Breakdown


### `direction.py`
Defines the `Direction` enumeration representing cardinal 2D movement on the maze grid.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Direction.opposite` | `(self) -> Direction` | Returns the reverse movement vector (e.g., `UP` -> `DOWN`, `LEFT` -> `RIGHT`). Used by ghosts during fleeing reversals and player input changes. |

---

### `entity.py`
Defines `Entity`, the abstract base domain model for movable objects on the tile grid.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Entity.set_direction` | `(self, direction: Direction) -> None` | Updates the entity's desired heading. |
| `Entity.stop` | `(self) -> None` | Halts movement, resets target tile, and clears interpolation progress to zero. |
| `Entity._clamp_progress` | `(progress: float) -> float` | *(Internal helper)* Clamps movement progress between `0.0` and `1.0` to prevent overshooting between grid tiles. |
| `Entity._interpolate_target` | `(origin: Coordinate, target: Coordinate, progress: float) -> tuple[float, float]` | *(Internal helper)* Computes smooth linear interpolation `(x, y)` in grid tiles. |
| `Entity._interpolate_direction` | `(origin: Coordinate, direction: Direction, progress: float) -> tuple[float, float]` | *(Internal helper)* Computes smooth floating `(x, y)` position along the movement direction vector. |
| `Entity._compute_visual_coords` | `(self, progress: float) -> tuple[float, float]` | *(Internal helper)* Selects target interpolation or directional projection based on target availability. |
| `Entity.get_visual_position` | `(self) -> tuple[float, float]` | Returns the precise sub-tile floating position used by renderers to draw smooth 60 FPS motion. |

---

### `ghost.py`
Defines `GhostState`, `GhostType`, and `Ghost` models representing the four enemy ghosts.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Ghost.__init__` | `(self, ghost_type, home_position, ...)` | Instantiates a ghost entity with its personality type (Red, Pink, Blue, Orange), spawn corner, and state. |

---

### `player.py`
Defines `Player`, representing Pac-Man and tracking lives, score, and power-up state.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `Player._validate_points` | `(points: int) -> None` | *(Internal helper)* Ensures score points added are non-negative, raising `ValueError` otherwise. |
| `Player._validate_remaining_lives` | `(lives: int) -> None` | *(Internal helper)* Asserts that lives remain before deduction to prevent negative life counters. |
| `Player.add_score` | `(self, points: int) -> None` | Safely validates and increments the player's cumulative score. |
| `Player.lose_life` | `(self) -> None` | Safely validates and decrements remaining lives by 1 when caught by a ghost. |
| `Player.activate_power_mode` | `(self) -> None` | Enables power-pellet mode (`is_powered_up = True`). |
| `Player.deactivate_power_mode` | `(self) -> None` | Disables power-pellet mode (`is_powered_up = False`). |
| `Player.reset_position` | `(self, position: Coordinate) -> None` | Teleports player back to spawn and halts movement after death or level reset. |
