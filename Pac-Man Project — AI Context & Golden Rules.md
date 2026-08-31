# Pac-Man Project — AI Context & Golden Rules

## 1. Project Overview

This project is a complete Pac-Man-style game written in **Python 3.10+** as part of the 42 curriculum.

The project must provide a playable game with:

- Multiple levels
- Player movement
- Four ghosts
- Ghost AI
- Pacgums
- Super-pacgums / power mode
- Collision handling
- Scoring
- Lives
- Level timers
- Pause/resume
- Main menu
- Highscores
- Game-over handling
- Victory handling
- Name entry for highscores
- Cheat mode
- Configurable game parameters
- External maze generation through the assigned A-Maze-ing package
- A polished graphical presentation
- Packaging for a public gaming platform

The architecture should be **modular, maintainable, easy to walk through during peer review, and easy to explain**.

The project should favor **clear separation of responsibilities over cleverness**.

---

# 2. Golden Rule

## Pygame is a presentation and input dependency — NOT the game engine.

Pygame may be used for:

- Window creation
- Reading keyboard/user events
- Drawing shapes
- Rendering images
- Rendering text
- Audio playback where permitted
- Presenting frames

Pygame must NOT be responsible for the game's core systems.

The following must be implemented by the project itself:

- Player movement
- Ghost movement
- Collision detection
- Collision resolution
- Ghost AI
- Game state management
- Level progression
- Scoring
- Lives
- Timers
- Power mode
- Animations
- Entity behavior
- Game rules
- Cheat behavior
- Highscore logic
- Game architecture

Do not use Pygame's functionality as a replacement for these systems.

---

# 3. Architecture Principle

The most important architectural boundary is:

```text
                GAME LOGIC
                    │
                    │
                    ▼
        ┌─────────────────────┐
        │ Player              │
        │ Ghosts              │
        │ Maze                │
        │ Collision           │
        │ AI                  │
        │ Score               │
        │ Levels              │
        │ Game State          │
        │ Timers              │
        └─────────────────────┘
                    │
                    ▼
              PRESENTATION
        ┌─────────────────────┐
        │ Rendering           │
        │ Themes              │
        │ UI                  │
        │ Audio               │
        │ Pygame              │
        └─────────────────────┘
```

Game logic should not depend on Pygame-specific rendering code.

A domain object should not be drawing itself.

Bad:

```python
class Player:
    def update(self):
        pygame.key.get_pressed()
        pygame.draw.circle(...)
        check_collision(...)
```

Preferred:

```text
Input
  ↓
Player Movement
  ↓
Player
  ↓
Collision System
  ↓
Game State
  ↓
Renderer
  ↓
Pygame
```

---

# 4. Separation of Concerns

Every module should have a clear responsibility.

Examples:

```text
entities/
    Represent game objects and their state.

systems/
    Implement gameplay systems and rules.

ai/
    Implement ghost decision-making.

states/
    Manage high-level game modes.

rendering/
    Convert game state into visual output.

themes/
    Define the visual identity of the game.

input/
    Convert user input into game actions.

config/
    Load, validate, and provide configuration.

maze/
    Integrate the external A-Maze-ing package.

highscore/
    Manage highscore behavior.

persistence/
    Handle generic file/data persistence.

audio/
    Handle music and sound playback.

cheat/
    Implement review/debug cheat functionality.

world/
    Represent the game world and levels.
```

Do not move responsibilities between these modules merely because it is convenient.

---

# 5. Do Not Over-Engineer

The project should use architecture that provides real value.

Do NOT introduce patterns merely to demonstrate patterns.

Avoid unnecessary:

- Dependency injection frameworks
- CQRS
- Domain-driven design
- Hexagonal architecture
- Event buses everywhere
- ECS
- Large interface hierarchies
- Abstract factories without a real need
- Repositories for simple in-memory data
- Managers for every tiny operation

Prefer concrete classes first.

Introduce an abstraction only when it solves an actual problem.

---

# 6. File Granularity

Small files are acceptable and encouraged when they represent a meaningful responsibility.

A file containing one small class is valid if that class represents a clear concept.

However:

> Split by responsibility, not by line count.

Good:

```text
player.py
player_direction.py
player_status.py
```

Bad:

```text
add_score.py
remove_score.py
get_score.py
reset_score.py
```

Four tiny files for operations belonging to one coherent responsibility would make the project harder to navigate rather than easier.

---

# 7. Game State Architecture

The game naturally follows a state-machine model.

Expected high-level states include:

```text
MAIN_MENU
    ↓
PLAYING
    ├── PAUSED
    │      ↓
    │   PLAYING
    │
    ├── GAME_OVER
    │      ↓
    │  ENTER_NAME
    │      ↓
    │  MAIN_MENU
    │
    └── VICTORY
           ↓
       ENTER_NAME
           ↓
       MAIN_MENU
```

Game states should be explicit and easy to understand.

A state should generally handle:

```text
Input/Event handling
Update
Rendering
State transitions
```

Do not turn the main `Game` class into one enormous collection of conditionals.

Avoid:

```python
if state == MAIN_MENU:
    # hundreds of lines
elif state == PLAYING:
    # hundreds of lines
elif state == GAME_OVER:
    # hundreds of lines
```

Prefer separate state objects/classes.

---

# 8. Entities vs Systems

Entities represent things.

Systems implement behavior across things.

Example:

```text
Player
    owns player state:
    position
    direction
    speed
    status
    lives-related state where appropriate

PlayerMovement
    determines how the player moves

CollisionDetector
    determines what collided

WallCollision
    determines whether movement is allowed

PlayerRenderer
    determines how the player is displayed
```

Do not put every behavior inside the entity class.

A `Player` should not become responsible for:

- Rendering itself
- Managing global score
- Loading configuration
- Saving highscores
- Managing levels
- Processing all keyboard input
- Running ghost AI

---

# 9. Rendering Rules

Rendering must consume game state.

Rendering should not define game rules.

For example:

```python
renderer.draw_player(player)
```

is good.

The renderer may inspect:

```text
player.position
player.direction
player.status
```

to determine what to display.

The renderer must not decide:

```text
whether the player can move
whether the player collided with a ghost
whether the player gains score
whether a level is complete
```

Those belong to game logic.

---

# 10. Theme System

The visual design must be separated from the gameplay.

The game should support themes such as:

```text
Classic
Runeterra-inspired
Cyberpunk
```

or future themes without changing the core gameplay implementation.

The core game should NOT contain logic such as:

```python
if theme == "runeterra":
    ...
elif theme == "cyberpunk":
    ...
```

Instead:

```text
Game Logic
    ↓
Renderer
    ↓
Theme
    ↓
Assets / Colors / Fonts / Effects
```

A theme may define:

- Colors
- Fonts
- Sprites
- Animations
- Backgrounds
- UI appearance
- Sounds
- Visual effects
- Maze style
- Entity appearance

Changing a theme should not require modifying the Player, Ghost AI, Collision, Scoring, or Level logic.

---

# 11. Intellectual Property / Assets

The project may be inspired by existing games and visual styles.

Do not assume that existing commercial assets can simply be copied into the project.

Use:

- Original assets
- Self-created assets
- Properly licensed assets
- Assets whose licenses permit project use

The implementation should reproduce a visual style without depending on unlicensed proprietary assets.

---

# 12. Ghost AI

Ghost AI is an explicit gameplay subsystem.

Ghosts should have clear behavioral states/strategies such as:

```text
CHASE
FLEE
RETURN_HOME
```

The AI should determine decisions.

The movement system should execute movement.

Do not combine the entire AI, movement, collision, rendering, and game-state system into `ghost.py`.

A useful separation is:

```text
Ghost
   ↓
Ghost AI
   ↓
Strategy
   ├── Chase
   ├── Flee
   └── Return Home
   ↓
Direction Selection
   ↓
Ghost Movement
```

---

# 13. Maze Integration

The assigned **A-Maze-ing** package is an external dependency.

Do not modify the assigned package.

Our project adapts to its interface.

Preferred boundary:

```text
A-Maze-ing Package
        ↓
   Maze Adapter
        ↓
  Project Maze Model
        ↓
      Game
```

The rest of the project should not need to know the details of the external package's API.

Do not rewrite the external generator inside this project.

---

# 14. Configuration

Configuration is external data.

The configuration layer is responsible for:

- Loading the configuration file
- Removing/handling comments
- Validating values
- Applying safe defaults
- Handling missing values
- Handling invalid values
- Reporting errors clearly

Game systems should consume validated configuration rather than repeatedly parsing raw configuration files.

---

# 15. Highscore System

The highscore system should be isolated from gameplay.

It is responsible for:

- Loading highscores
- Validating entries
- Validating player names
- Sorting scores
- Keeping the top 10
- Saving highscores
- Handling corrupted/missing files gracefully

Gameplay should interact with the highscore system through a clear API rather than manually reading and writing JSON everywhere.

---

# 16. Cheat Mode

Cheat mode exists primarily to make peer review easier.

Useful cheats include:

```text
Invincibility
Level Skip
Ghost Freeze
Extra Lives
Speed Boost
```

Cheat behavior should be isolated inside `cheat/`.

Do not spread cheat-specific conditions throughout every gameplay class.

Avoid:

```python
if cheat_mode:
    ...
```

appearing in dozens of unrelated files.

Prefer centralizing cheat state and exposing the necessary effects to the systems that legitimately need them.

---

# 17. Input

Input handling should translate Pygame events into project-level actions.

Preferred direction:

```text
Pygame Event
      ↓
Keyboard Input
      ↓
Input Action
      ↓
Game / State
```

Avoid making the entire game directly depend on:

```python
pygame.key.get_pressed()
```

everywhere.

Input is an external concern and should have a clear boundary.

---

# 18. Game Loop

The game should have a clear loop conceptually similar to:

```text
while running:

    events = read_input()

    current_state.handle_input(events)

    current_state.update(dt)

    current_state.render()

    present_frame()
```

The game loop coordinates the process.

It should not contain all game logic.

---

# 19. Dependency Direction

Prefer dependencies to flow toward stable project logic.

Conceptually:

```text
External Dependencies
        ↓
     Adapters
        ↓
   Project Logic
        ↓
   Presentation
```

Examples:

```text
A-Maze-ing → MazeAdapter → Maze
Pygame → Input Layer → Game
Pygame → Renderer → Game State
Config File → Config Layer → Game
JSON File → Persistence → Highscore
```

Do not allow every class to import and directly manipulate everything else.

---

# 20. Testing Philosophy

Gameplay logic should be testable without requiring the complete graphical application.

Prioritize tests for:

- Movement
- Wall collision
- Entity collision
- Ghost behavior
- Scoring
- Power mode
- Lives
- Level progression
- Timer behavior
- Highscore validation
- Configuration validation

Avoid writing tests that merely verify that Pygame can draw a rectangle.

Test project behavior, not third-party functionality.

---

# 21. Code Quality

Follow the project requirements:

- Python 3.10+
- Type hints
- `mypy`
- `flake8`
- PEP 257 docstrings
- Graceful exception handling
- Proper resource management
- Context managers where appropriate
- Clean project structure
- `.gitignore`
- `Makefile`

The code should be understandable during peer review.

Do not sacrifice readability to make code shorter.

---

# 22. AI Assistance Rules

When an AI assistant is helping with this project:

1. Understand the existing architecture before suggesting changes.
2. Do not introduce a framework or pattern unless it solves a real project problem.
3. Respect the Pygame boundary.
4. Do not move gameplay logic into Pygame.
5. Do not modify the A-Maze-ing package.
6. Prefer incremental changes.
7. Explain architectural consequences of proposed changes.
8. Identify trade-offs.
9. Flag anti-patterns and unnecessary complexity.
10. Do not generate huge amounts of code blindly.
11. Keep solutions understandable enough for the developer to explain during peer review.
12. Prefer teaching the reasoning behind a solution over blindly producing finished code.

When reviewing code, actively look for:

- God classes
- Circular dependencies
- Pygame leaking into domain logic
- Duplicated logic
- Tight coupling
- Global state
- Hidden side effects
- Over-abstraction
- Inappropriate inheritance
- Long functions
- Poor naming
- Responsibilities in the wrong module
- Unnecessary framework usage

---

# 23. Decision-Making Rule

When choosing between two designs:

Prefer the design that:

```text
1. Is easier to understand
2. Has clearer responsibilities
3. Has fewer unnecessary dependencies
4. Is easier to test
5. Is easier to explain during peer review
6. Can be changed without affecting unrelated systems
```

Do not choose a design merely because it uses more patterns.

---

# 24. The Ultimate Boundary

Always preserve this distinction:

```text
                    PYGAME
                      │
             ┌────────┴────────┐
             │                 │
           INPUT           RENDERING
             │                 ▲
             ▼                 │
        GAME ACTIONS      VISUAL OUTPUT
             │                 │
             └──────┬──────────┘
                    │
                    ▼
              GAME SYSTEMS
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    Player        Ghosts       Maze
       │            │            │
       ▼            ▼            ▼
   Movement        AI       Level System
       │            │            │
       └────────────┼────────────┘
                    ▼
              Game Rules
```

**Pygame displays the game.  
Pygame does not define the game.**

That is the project's primary architectural rule.