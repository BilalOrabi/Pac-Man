# Project Management: Acceptance Test Plan & Quality Matrix

## 1. Quality & Verification Strategy

The acceptance test plan verifies every functional, non-functional, and architectural requirement defined in **`Pacman.pdf`** (v1.5) and the project memory guidelines.

Testing comprises three rigorous levels:
1. **Automated Unit & Integration Testing**: 525 automated tests run via `pytest`.
2. **Static Code Analysis**: Strict compliance with `flake8` (0 warnings) and `mypy` (strict types).
3. **Manual Functional Verification**: In-game interactive testing across all game states, levels, and cheats.

---

## 2. Requirements Traceability Matrix

| Subject Chapter | Requirement Description | Test Case Reference | Automated / Manual | Verification Result |
| :--- | :--- | :--- | :---: | :---: |
| **Ch. 4** | Decoupled Architecture & State Machine | `tests/states/`, `tests/application/` | Automated + Manual | **PASS** |
| **Ch. 5.1** | JSON Configuration File Structure | `tests/config/test_game_config.py` | Automated | **PASS** |
| **Ch. 5.2** | Comment Filtering (`#` and `//`) | `tests/config/test_config_loader.py` | Automated | **PASS** |
| **Ch. 5.3** | Fault-Tolerance & Safe Clamping | `tests/config/test_config_loader.py` | Automated + Manual | **PASS** |
| **Ch. 5.4** | Maze Generator Wheel Integration | `tests/maze/test_adapter.py` | Automated | **PASS** |
| **Ch. 5.4 (Add.)**| Safe Entry Resolution ('42' Logo Collisions) | `tests/maze/test_adapter.py` | Automated | **PASS** |
| **Ch. 5.5** | High-Score Validation (Mixed-Case, 10 chars, disk I/O) | `tests/highscore/`, `tests/persistence/` | Automated + Manual | **PASS** |
| **Ch. 6.1** | Corridor Wall Collisions & BFS Pathfinding | `tests/systems/test_collision.py`, `tests/ai/` | Automated + Manual | **PASS** |
| **Ch. 6.2** | Player Movement (WASD / Arrows) | `tests/controllers/test_player_controller.py` | Automated + Manual | **PASS** |
| **Ch. 6.3** | Ghost AI (Chase, Flee, Return Home) | `tests/ai/`, `tests/controllers/test_ghost_controller.py` | Automated + Manual | **PASS** |
| **Ch. 6.4** | Pacgums & Super-Pacgums Consumption | `tests/world/test_level.py`, `tests/systems/test_scoring.py` | Automated + Manual | **PASS** |
| **Ch. 6.5** | Power Mode Duration & Edible Ghosts | `tests/systems/test_power_mode.py` | Automated + Manual | **PASS** |
| **Ch. 6.6** | Lives Deduction & Center Respawn | `tests/systems/test_lives.py` | Automated + Manual | **PASS** |
| **Ch. 6.7** | Cheat Mode (Keys 1-5) | `tests/cheat/test_cheat_system.py` | Automated + Manual | **PASS** |
| **Ch. 6.8** | 60 FPS Presentation, HUD & Menus | `tests/rendering/`, `pac-man.py` | Automated + Manual | **PASS** |
| **Ch. 6.8 (Add.)**| Native Fixed 1600x900 Display & Centering | `tests/rendering/`, `pac-man.py` | Automated + Manual | **PASS** |
| **Quality (Add.)**| Centralized Silent Logging (`errors.log`) | `tests/utils/test_error_logger.py` | Automated + Manual | **PASS** |
| **Ch. 7** | Packaging for itch.io / Steam | `package.py`, `pacman.spec` | Automated + Manual | **PASS** |
| **Ch. 8** | Project Management Artifacts | `docs/project_management/` | Manual Audit | **PASS** |
| **Ch. 9** | Comprehensive README Documentation | `README.md` | Manual Audit | **PASS** |

---

## 3. Manual Functional Test Scenarios

### Scenario 1: Game Launch & Fault-Tolerant Config
- **Action**: Run `python pac-man.py config.json` where `config.json` contains `#` comments and missing keys.
- **Expected**: Application opens a window with Main Menu; logs informational warnings for clamped values; no unhandled tracebacks.
- **Result**: **PASS**.

### Scenario 2: Main Menu Navigation & Sub-views
- **Action**: Use UP/DOWN to navigate menu options (Start Game, Highscores, Instructions, Exit). Press ENTER on Highscores and Instructions, then ESC.
- **Expected**: Views transition cleanly; leaderboard displays top 10 scores; instructions explain all rules.
- **Result**: **PASS**.

### Scenario 3: Maze Traversal & Corridor Collisions
- **Action**: Start game and move Pac-Man using Arrow keys or WASD into walls.
- **Expected**: Pac-Man stops against cell boundary walls and cannot walk through corridors.
- **Result**: **PASS**.

### Scenario 4: Pellet Eating & Power Mode
- **Action**: Guide Pac-Man over regular pacgums and super-pacgums in the corners.
- **Expected**:
  - Regular pacgums vanish, score increases by +10 pts.
  - Super-pacgum vanishes, score increases by +50 pts, power mode activates, ghosts turn blue.
  - Devouring a blue ghost awards +200 pts and ghost eyes return home.
- **Result**: **PASS**.

### Scenario 5: Ghost Collision & Lives System
- **Action**: Walk into a normal (chasing) ghost.
- **Expected**: Pac-Man loses 1 life, respawns in center; HUD reflects reduced lives count.
- **Result**: **PASS**.

### Scenario 6: Cheat Mode Hotkeys
- **Action**:
  - Press `1`: Invincibility activates; ghost touch does not reduce life.
  - Press `2`: Ghosts freeze in position.
  - Press `3`: Pac-Man speed boosts.
  - Press `4`: Extra life added to player and HUD.
  - Press `5`: Current level skips immediately to next level.
- **Expected**: Active cheats banner displayed on HUD; gameplay modifies immediately.
- **Result**: **PASS**.

### Scenario 7: Game Over / Victory & High-score Persistence
- **Action**: Lose all lives or complete level 10. Enter a 10-character player name and press ENTER.
- **Expected**: Score is saved to `highscores.json`. Viewing Highscores from Main Menu displays newly recorded entry in correct sorted position.
- **Result**: **PASS**.

---

## 4. Bug Tracking & Resolution Log

| Bug ID | Component | Severity | Description | Resolution Applied |
| :--- | :--- | :---: | :--- | :--- |
| **BUG-01** | `config_loader.py` | High | `json.loads` failed when `#` comments existed in `config.json`. | Added regex preprocessing to strip comment lines prior to JSON parsing. |
| **BUG-02** | `collision.py` | Critical | Pac-Man walked through walls because only `is_solid_block` was verified. | Enhanced `Maze.can_move` to check bitmask walls (`NORTH`, `EAST`, `SOUTH`, `WEST`) between adjacent cells. |
| **BUG-03** | `level_factory.py` | Medium | All ghosts and player spawned at `maze.entry`. | Repositioned player to center and 4 ghosts to the 4 corners of the maze. |
| **BUG-04** | `level.py` | High | Pellets were not tracked as physical grid tiles. | Added `pacgums: set[Coordinate]` and `super_pacgums: set[Coordinate]` with `consume_pacgum_at()`. |
| **BUG-05** | `gameplay_controller.py` | High | Player-ghost collisions had no gameplay effect. | Wired collision response: ghost eaten in power mode, or player loses life and respawns. |
| **BUG-06** | `ui_renderer.py` | High | UI renderer lacked graphical implementation for menus and HUD. | Implemented Pygame drawing for HUD, Main Menu, Highscores, Instructions, Pause, Game Over, and Name Entry. |
| **BUG-07** | `pac-man.py` | Critical | Main executable printed config summary and immediately exited. | Built full 60 FPS Pygame loop with input event polling, state synchronization, and clean persistence shutdown. |
| **BUG-08** | `adapter.py` | Critical | Center spawn at width 14 landed on solid block of '42' pattern, trapping player and deleting interior walls. | Added `_find_safe_entry()` to resolve spawn to nearest open corridor cell `(6, 5)` between digits. |
| **BUG-09** | `pac-man.py` | Medium | Highscore name input rejected lowercase characters. | Allowed mixed-case letters `a-z`, `A-Z`, numbers, and spaces up to 10 characters. |
| **BUG-10** | `error_logger.py` | Medium | External wheel notices and config warnings printed to console terminal. | Created centralized `ErrorLogger` capturing stderr and wheel notices into `errors.log`. |
| **BUG-11** | `pac-man.py` | Medium | Dynamic window resizing caused artwork distortion, letterboxing, and screen flickering. | Fixed display permanently to $1600 \times 900$, centering auto-scaled mazes via `GameRenderer`. |
