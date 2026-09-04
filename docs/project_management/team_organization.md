# Project Management: Team Organization, Roles & Architectural Decisions

## 1. Team Structure & Responsibilities

The project was executed by a collaborative pair-programming team of two software engineers under 42 School curriculum guidelines:

| Team Member | Role | Primary Responsibilities |
| :--- | :--- | :--- |
| **Bilal Orabi** (`borabi`) | Systems & Architecture Lead | Domain engine architecture, Maze bitmask integration, collision detection, Ghost AI algorithms, cheat subsystem, high-score validation. |
| **Hamza Qasqas** (`hqasqas`) | Presentation & Interface Lead | AssetManager and theme engine, Pygame event polling and 60 FPS clock, procedural rendering pipelines, HUD, state machine, menus and deployment packaging. |

---

## 2. Collaborative Practices & Workflow

To maintain code quality, avoid merge friction, and adhere to the strict 42 evaluation norms:

1. **Pair Programming & Code Review**:
   - Every module underwent peer code review before committing.
   - Code reviews verified:
     - 100% compliance with `flake8 --count src/` (0 warnings).
     - Strict static type annotations verified by `mypy`.
     - Comprehensive PEP 257 docstrings for all classes, methods, and modules.
2. **Golden Rule Guard**:
   - Regular verification that no Pygame calls or imports were introduced into `src/entities/`, `src/systems/`, `src/ai/`, `src/world/`, or `src/controllers/`.
3. **Automated Test Discipline**:
   - New capabilities were written with unit tests in `tests/`.
   - Continuous test execution ensured that the entire suite of 480 tests passed on every iteration.

---

## 3. Architectural Decision Records (ADRs)

### ADR-001: Separation of Pygame from Core Domain Logic
- **Context**: 42 School curriculum golden rule: *Pygame displays the game; Pygame does not define the game.*
- **Decision**: Domain code (movement, collisions, scoring, lives, ghost AI, timers, state machine, cheats) is isolated from Pygame. Pygame is strictly an input and presentation dependency.
- **Consequences**: Headless unit testing is fast and deterministic (480 tests run in <0.8 seconds). Theme visual swapping requires no gameplay code changes.

### ADR-002: Adapter Pattern for External Maze Generation
- **Context**: `libs/mazegenerator-2.1.0-py3-none-any.whl` must be used as-is with `perfect=False`.
- **Decision**: Implemented `MazeAdapter` to translate external generator outputs into internal `Maze` and `Cell` structures with bitmask wall helpers.
- **Consequences**: External wheel remains untouched, and internal code relies on type-safe domain abstractions.

### ADR-003: Bitmask Directional Wall Collisions
- **Context**: Cells in imperfect mazes have internal directional bitmasks (`Wall.NORTH`, `EAST`, `SOUTH`, `WEST`) rather than solid blocks.
- **Decision**: Added `Maze.can_move(from_pos, to_pos)` checking boundary bitmasks between adjacent cells.
- **Consequences**: Entities navigate real maze corridors without passing through walls, and pathfinding AI accurately perceives valid corridors.

### ADR-004: Centralized Asset Management with Procedural Fallbacks
- **Context**: Presentation assets (sprites, fonts, sounds) must be customizable by theme without hardcoding file paths in renderers.
- **Decision**: Centralized all presentation resources in `AssetManager` with procedural fallback rendering if external image files are missing.
- **Consequences**: The application launches and renders cleanly on any workstation without external media dependencies, while supporting external asset overrides seamlessly.

### ADR-005: Safe Default Clamping for Fault-Tolerant Configuration
- **Context**: Subject Chapter 5 requires that missing or invalid values clamp to safe defaults and comments (`#`, `//`) must be ignored without raising unhandled tracebacks.
- **Decision**: Built a pre-processing text cleaner and validator that clamps missing or malformed values to robust positive defaults while logging clear console warnings.
- **Consequences**: Zero unhandled tracebacks; flawless user experience when editing `config.json`.

### ADR-006: Standalone Distribution Strategy (Chapter 7)
- **Context**: Deployment requirements for Steam and itch.io platforms.
- **Decision**: Created `pacman.spec` and `package.py` to package standalone executable bundles and release ZIP archives with automated launchers (`run.bat`, `run.sh`).
- **Consequences**: Instant distribution readiness with zero manual setup for end players.

---

## 4. Conflict Resolution & Decision Log

| Date | Topic | Conflict / Trade-off | Resolution |
| :--- | :--- | :--- | :--- |
| **2026-08-15** | Config Comments | Standard `json.loads` rejects `#` comments. Should we use YAML or custom regex? | Kept standard JSON format per subject spec, adding clean comment-stripping regex before decoding. |
| **2026-08-20** | Ghost Personalities | Should all 4 ghosts use identical chase logic or differentiated behaviors? | Implemented distinct targeting: Red (direct), Pink (predictive ambush), Blue (flanking), Orange (distance caution). |
| **2026-08-28** | Presentation Graphics | Should we require bundled PNG files or procedural fallbacks? | Provided procedural Pygame rendering for all entities and walls, allowing the game to run with 100% visual quality out-of-the-box. |
| **2026-09-02** | Cheat Key Mappings | Map cheats into `InputAction` enum or handle at presentation event loop? | Handled at Pygame event loop to keep `InputAction` strictly aligned with canonical 9 actions tested in unit tests. |
