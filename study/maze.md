# Maze Module (`src/maze/`)

## 1. Module Overview
The `maze` module encapsulates the discrete grid environment of the game. It models walls using 4-bit bitmasks (`NORTH`, `EAST`, `SOUTH`, `WEST`), provides geometric collision and corridor traversability queries, and adapts the external `mazegenerator` wheel into project-owned domain models (`Maze`, `MazeCell`) with automatic '42' logo pattern collision avoidance.

---

## 2. File & Class Breakdown

### `maze.py`
Defines the `Wall` bitmask enum, immutable `MazeCell`, and the top-level `Maze` container.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MazeCell.has_wall` | `(self, wall: Wall) -> bool` | Performs bitwise AND (`walls & wall`) to test whether a cell boundary is blocked. |
| `Maze.get_cell` | `(self, position: Coordinate) -> MazeCell` | Retrieves cell at `(x, y)` coordinate, throwing `IndexError` if out of bounds. |
| `Maze.is_inside` | `(self, x: int, y: int) -> bool` | Bounds check confirming whether `0 <= x < width` and `0 <= y < height`. |
| `Maze._is_passage_open` | `(from_cell, to_cell, delta_x, delta_y) -> bool` | *(Internal helper)* Verifies that neither the origin cell nor destination cell has a blocking wall across their shared border. |
| `Maze._are_positions_valid` | `(self, from_pos, to_pos) -> bool` | *(Internal helper)* Validates that both origin and destination tiles reside within maze boundaries. |
| `Maze._are_cells_clear` | `(from_cell, to_cell) -> bool` | *(Internal helper)* Verifies that neither tile is an impassable solid obstacle block (e.g. logo or outer border). |
| `Maze.can_move` | `(self, from_position, to_position) -> bool` | Top-level movement validation: bounds check -> obstacle check -> shared wall check. |
| `Maze.is_walkable` | `(self, position, from_position=None) -> bool` | Determines whether an entity can occupy a target cell, checking walls if origin is provided. |

---

### `adapter.py`
Implements `MazeAdapter`, which converts the external generator's raw numeric matrix into immutable `Maze` models.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MazeAdapter._is_42_solid_cell` | `(cls, x, y, width, height) -> bool` | *(Internal helper)* Maps `(x, y)` to the centered '42' logo pattern matrix to detect solid logo blocks. |
| `MazeAdapter._find_safe_entry` | `(cls, width, height, preferred_entry) -> Coordinate` | *(Internal helper)* Automatically relocates player spawn to the nearest open corridor if the center cell overlaps the '42' logo. |
| `MazeAdapter._validate_dimensions` | `(width: int, height: int) -> None` | *(Internal helper)* Ensures dimensions are positive non-zero integers before invoking generator. |
| `MazeAdapter._validate_coordinate` | `(coordinate, width, height, name) -> None` | *(Internal helper)* Validates that entry/exit coordinates reside inside maze dimensions. |
| `MazeAdapter._create_generator` | `(width, height, seed, entry_cell, exit_cell) -> MazeGenerator` | *(Internal helper)* Configures external generator with `perfect=False` and intercepts console warnings into `errors.log`. |
| `MazeAdapter._parse_bitmask_grid` | `(raw_grid, width, height) -> MazeGrid` | *(Internal helper)* Converts raw integers into 2D tuples of immutable `MazeCell` instances with bitwise `Wall` flags. |
| `MazeAdapter.generate_level` | `(self, width, height, seed, ...) -> Maze` | Orchestrates the entire level maze generation and model transformation pipeline. |