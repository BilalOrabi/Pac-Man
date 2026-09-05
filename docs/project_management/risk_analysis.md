# Project Management: Risk Analysis & Mitigation Matrix

## 1. Risk Assessment Framework

Risks were identified, evaluated, and mitigated based on two primary dimensions:
- **Likelihood**: Low (1), Medium (2), High (3)
- **Impact**: Minor (1), Moderate (2), Critical (3)
- **Risk Priority Number (RPN)**: $Likelihood \times Impact$ (Scale 1 to 9).

---

## 2. Risk Evaluation Matrix

| Risk ID | Category | Risk Description | Likelihood (1-3) | Impact (1-3) | RPN (1-9) | Severity Level |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **R-01** | Technical | Pygame coupling leaks into domain models / gameplay logic | 2 | 3 | **6** | High |
| **R-02** | Technical | Maze corridors pass-through bug due to bitmask wall misinterpretation | 3 | 3 | **9** | Critical |
| **R-03** | Dependency | External wheel dependency (`mazegenerator-2.1.0`) compatibility failure | 1 | 3 | **3** | Moderate |
| **R-04** | Robustness | JSON configuration parser crashes on user comments or missing parameters | 3 | 2 | **6** | High |
| **R-05** | Schedule | Presentation layer complexity delays complete playable loop | 2 | 3 | **6** | High |
| **R-06** | Quality | Mock incompatibility in test suite when enhancing real domain methods | 2 | 2 | **4** | Moderate |
| **R-07** | Compliance | Non-compliance with 42 code style (flake8 line limits, untyped mypy signatures) | 2 | 2 | **4** | Moderate |
| **R-08** | Packaging | Standalone bundle fails to package required assets and dependencies | 2 | 2 | **4** | Moderate |
| **R-09** | Technical | Center spawn collision with '42' solid logo block at width 14 | 3 | 3 | **9** | Critical |
| **R-10** | Presentation | Dynamic window resizing causes aspect ratio distortion and screen flicker | 2 | 2 | **4** | Moderate |
| **R-11** | Compliance | Stderr stream pollution and external library notices violate silent console requirement | 2 | 2 | **4** | Moderate |

---

## 3. Detailed Risk Mitigation Strategies & Outcomes

### R-01: Architectural Coupling (Pygame Leaks)
- **Description**: If Pygame dependencies (`pygame.Surface`, `pygame.Rect`, event polling) are referenced inside gameplay classes (`Player`, `Ghost`, `GameplayController`, `CollisionSystem`), visual theme swappability and testability are compromised.
- **Mitigation Strategy**: Strict architectural boundary enforcement:
  - `AssetManager` is the single centralized gateway for visual/audio assets.
  - Gameplay entities only reference pure domain types (`Coordinate = tuple[int, int]`, pure dataclasses).
  - Renderers in `src/rendering/` consume domain state and blit to Pygame surfaces.
- **Outcome**: **Mitigated**. Zero Pygame imports exist in domain code, verified by automated imports inspection and headless unit tests.

### R-02: Maze Bitmask Wall Collision Failure
- **Description**: The external `mazegenerator` wheel generates non-solid grid cells with bitmask boundary walls (`NORTH`, `EAST`, `SOUTH`, `WEST`). If collision systems only check `cell.is_solid_block`, entities can walk through any corridor wall.
- **Mitigation Strategy**:
  - Implemented `can_move(from_pos, to_pos)` in `Maze` to calculate direction and inspect wall bitmasks on the origin cell (and complementary walls on the destination cell).
  - Updated `CollisionSystem.can_move_to` and `GhostAI` to validate corridor walls.
- **Outcome**: **Mitigated**. Pac-Man and ghosts respect all interior walls cleanly.

### R-03: External Wheel Dependency Integrity
- **Description**: The subject strictly mandates using `libs/mazegenerator-2.1.0-py3-none-any.whl` with `perfect=False` and forbids modifying the wheel.
- **Mitigation Strategy**:
  - Built an adapter (`MazeAdapter`) wrapping `mazegenerator.generate_maze(width, height, perfect=False)`.
  - Converted raw bitmask outputs into typed domain cells (`src/maze/maze.py`).
- **Outcome**: **Mitigated**. Wheel utilized as-is without any external modifications.

### R-04: Configuration Parser Fragility
- **Description**: Subject Chapter 5 requires fault tolerance: missing or invalid values must clamp to safe defaults without tracebacks, and comments (`#`, `//`) must be supported.
- **Mitigation Strategy**:
  - Preprocessed JSON text using regex line stripping before JSON decoding.
  - Added safe default clamping across all numeric and level settings.
- **Outcome**: **Mitigated**. System boots reliably even when given empty or corrupt configs, logging clean warnings.

### R-05: Presentation Layer Scope Creep
- **Description**: Pygame rendering (procedural graphics, HUD, menus, sound, 60 FPS loop) could bottleneck delivery.
- **Mitigation Strategy**:
  - Built a modular presentation architecture with distinct renderers (`MazeRenderer`, `PlayerRenderer`, `GhostRenderer`, `UIRenderer`).
  - Implemented procedural fallback drawing ensuring immediate out-of-the-box operation.
- **Outcome**: **Mitigated**. Clean 60 FPS presentation loop running smoothly.

### R-06: Test Suite Regression via Mock Types
- **Description**: Existing unit tests mock certain objects (`player.lives`, `game_renderer`), which could raise `TypeError` when tested against numeric operators (e.g., `lives <= 0`).
- **Mitigation Strategy**:
  - Added safe type-checking guards (`isinstance(lives, (int, float))`) in state coordination checks.
  - Maintained complete backward compatibility across all 525 test cases.
- **Outcome**: **Mitigated**. 525/525 tests pass without failures.

### R-09: Center Spawn Collision with '42' Solid Logo Blocks (Width 14)
- **Description**: In mazes of width 14 and height $\ge 10$, the mandatory '42' logo places an impenetrable solid block directly at `(width // 2, height // 2) = (7, 5)`. Spawning Pac-Man here trapped the player and prevented DFS corridor carving, causing interior walls to vanish.
- **Mitigation Strategy**:
  - Implemented `_is_42_solid_cell` in `MazeAdapter` to map the logo pattern footprint.
  - Implemented `_find_safe_entry` to automatically shift the spawn inward to the nearest open corridor cell `(6, 5)` between the '4' and '2'.
- **Outcome**: **Mitigated**. Complete maze carving and walkable player spawns for all valid dimension combinations.

### R-10: Display Resizing Jitter & Background Distortion
- **Description**: Recalculating OS window dimensions per level based on maze cell counts caused menu artwork distortion, letterboxing, and window flickering between state changes.
- **Mitigation Strategy**:
  - Locked display permanently to native $1600 \times 900$ native widescreen resolution across all game states.
  - MazeRenderer dynamically downscales cells (`cell_size = min((1500 // w), (780 // h), 36)`) and centers the maze arena inside the screen.
- **Outcome**: **Mitigated**. Stable 60 FPS presentation with crisp anti-aliased scaling and zero window distortion.

### R-11: Console Output Leaks & External Wheel Stderr Pollution
- **Description**: External `mazegenerator` wheel notices ("too small to add '42'") and configuration validation warnings printed directly to `stdout`/`stderr`, violating clean silent terminal requirements.
- **Mitigation Strategy**:
  - Created centralized `ErrorLogger` and `ErrorLogStream` in `src/utils/error_logger.py`.
  - Redirected `sys.stderr` and captured library stdout notices during maze generation, routing all entries exclusively to `errors.log` formatted with `[YYYY-MM-DD HH:MM:SS] <message>`.
- **Outcome**: **Mitigated**. 100% silent console execution with full diagnostic traceability in root `errors.log`.
