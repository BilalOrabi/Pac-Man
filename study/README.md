# Pac-Man Codebase Defense & Study Guide

*Curriculum: 42 School — Python Presentation & Domain Architecture*

---

## 1. Architectural Overview & Separation of Concerns

The Pac-Man codebase is engineered around strict domain-driven hexagonal boundaries:

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION & INPUT LAYER                  │
│   src/rendering/   src/input/   src/audio/   src/theme/     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Dispatches Actions / Read Snapshots
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION ORCHESTRATION                 │
│      src/application/ (GameCoordinator, MainGameLoop)       │
│      src/states/      (Finite State Machine & Screens)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Ticks Simulation
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      CONTROLLERS LAYER                      │
│   src/controllers/ (GameplayController, Player, Ghosts)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Invokes Rules & Algorithms
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     PURE DOMAIN ENGINE                      │
│   src/entities/   src/maze/      src/world/   src/systems/  │
│   src/ai/         src/cheat/     src/config/  src/highscore/│
│   src/persistence/               src/utils/                 │
└─────────────────────────────────────────────────────────────┘
```

### Core Golden Rules
1. **Pygame Presentation Boundary**: *Pygame displays the game; Pygame does not define the game.* Core game logic (grid movements, BFS pathfinding, collision detection, scoring, lives, timers) contains zero Pygame dependencies.
2. **AssetManager Centralization**: Renderers never construct raw asset file paths; they query `AssetManager`. Gameplay classes never touch assets.
3. **Silent Terminal**: Console output is kept clean and quiet. All non-fatal warnings (such as JSON parsing clamps or small-maze notices) are routed to `errors.log`.
4. **Fault Tolerance**: Malformed dimensions clamp to valid limits (`5 <= width <= 35`, `5 <= height <= 24`) and missing JSON keys safely default.

---

## 2. Directory Defense Guides Index

Each folder inside `src/` has a dedicated study guide explaining every class, function, and internal helper method for 42 School peer evaluations:

| Guide Link | Directory | Core Responsibility |
| :--- | :--- | :--- |
| **[AI Guide](file:///d:/pacman/study/ai.md)** | `src/ai/` | BFS corridor shortest pathfinding, ghost modes (`CHASE`, `FLEE`, `RETURN_HOME`), and unique ghost targeting personalities (Blinky, Pinky, Inky, Clyde). |
| **[Application Guide](file:///d:/pacman/study/application.md)** | `src/application/` | Central orchestration (`GameCoordinator`) and 60 FPS clock cycle management (`MainGameLoop`). |
| **[Audio Guide](file:///d:/pacman/study/audio.md)** | `src/audio/` | Abstract audio tracking, music lifecycle, and sound-effect record buffering. |
| **[Cheat Guide](file:///d:/pacman/study/cheat.md)** | `src/cheat/` | Debug and evaluation cheats (Keys 1-5: Invincibility, Freeze, Speed Boost, Extra Life, Skip Level). |
| **[Config Guide](file:///d:/pacman/study/config.md)** | `src/config/` | Strict and fault-tolerant JSON configuration parsing, comment stripping (`#` and `//`), and bounds clamping. |
| **[Controllers Guide](file:///d:/pacman/study/controllers.md)** | `src/controllers/` | Actor movement pacing, turn buffering, 180° reversals, scatter/chase wave cycles, pellet eating, and death penalties. |
| **[Entities Guide](file:///d:/pacman/study/entities.md)** | `src/entities/` | Actor data models: `Player`, `Ghost`, `Entity` base class, and 4-directional spatial orientations. |
| **[Highscore Guide](file:///d:/pacman/study/highscore.md)** | `src/highscore/` | Top 10 leaderboard ranking, player name validation (1-10 alphanumeric characters), and score sorting. |
| **[Input Guide](file:///d:/pacman/study/input.md)** | `src/input/` | Translating raw hardware keyboard events into typed domain actions (`InputAction`) and maintaining `InputState`. |
| **[Maze Guide](file:///d:/pacman/study/maze.md)** | `src/maze/` | Maze representation, bitmask wall flags (N, E, S, W), corridor passage validation, and `mazegenerator` wheel adapter. |
| **[Persistence Guide](file:///d:/pacman/study/persistence.md)** | `src/persistence/` | Resilient JSON file operations on disk with automatic parent directory creation. |
| **[Rendering Guide](file:///d:/pacman/study/rendering.md)** | `src/rendering/` | Pygame graphical presentation: animated Pac-Man mouth chomping, ghost sprites/eyes, wall rendering, HUD, and audio playback. |
| **[States Guide](file:///d:/pacman/study/states.md)** | `src/states/` | Finite state machine managing screen contexts (`MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`, `VICTORY`, `ENTER_NAME`). |
| **[Systems Guide](file:///d:/pacman/study/systems.md)** | `src/systems/` | Discrete domain rule engines: collision, movement steps, power mode timer, scoring, lives, level progression, and level timer. |
| **[Theme Guide](file:///d:/pacman/study/theme.md)** | `src/theme/` | Centralized `AssetManager` access point, color palettes, fonts, music paths, and sprite definitions. |
| **[Utils Guide](file:///d:/pacman/study/utils.md)** | `src/utils/` | Centralized `ErrorLogger` and `ErrorLogStream` redirecting `sys.stderr` to `errors.log` with timestamps. |
| **[World Guide](file:///d:/pacman/study/world.md)** | `src/world/` | Campaign management: `Level` state, procedural `LevelFactory` generation, and `GameWorld` campaign lifecycle. |

---

## 3. Key Peer Review Defense Topics

### Q1: How does ghost AI ensure ghosts never cut through walls?
> **Defense Answer**: The `GhostAI` class runs Breadth-First Search (BFS) exclusively across adjacent cells where `Maze.can_move(current, neighbor)` returns `True`. Bitmask wall clearance (NORTH, SOUTH, EAST, WEST) is strictly checked before any cell is enqueued. Additionally, ghosts cannot make 180° turns during normal chase navigation unless reversing into Frightened mode.

### Q2: What happens if `config.json` has missing keys or invalid dimensions?
> **Defense Answer**: In fallback mode, `ConfigLoader` inspects every key safely:
> - Maze dimensions outside `5x5` to `35x24` are automatically clamped with a warning logged to `errors.log` (defaulting to standard `19x21`), preventing engine crashes.
> - Comment lines beginning with `#` and `//` are stripped before JSON decoding.
> - Speeds are calibrated to stable 60 FPS constants.

### Q3: How are cheats enabled and displayed?
> **Defense Answer**: Handled by `CheatSystem` and keyboard keys:
> - `1`: Invincibility (ghost collisions do not deduct lives)
> - `2`: Freeze Ghosts (ghost movement ticks are skipped)
> - `3`: Speed Boost (2.2x player speed multiplier)
> - `4`: Extra Life (+1 life awarded)
> - `5`: Skip Level (instantly marks level completed)
> Active cheats are rendered as badges on the in-game HUD.

### Q4: How is audio handled across screens?
> **Defense Answer**: `AudioPresenter` centralizes sound playback:
> - Screen states dynamically switch tracks (`MENU` plays menu music, `PLAYING` plays start sound then normal ambiance, `VICTORY` and `GAME_OVER` trigger thematic soundtracks).
> - One-shot sound effects (pellets, ghost kills, death) cut off conflicting sounds immediately to avoid audio cacophony.

