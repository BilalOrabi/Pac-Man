# Application Module (`src/application/`)

## 1. Module Overview
The `application` module serves as the primary compositional layer bringing together domain systems, state machines, hardware inputs, and presentation rendering. It encapsulates the top-level orchestration in `GameCoordinator` (managing level lifecycles, level progression transitions, loss condition checks, and action routing) and `MainGameLoop` (providing frame-by-frame simulation clock ticking and rendering dispatch).

---

## 2. File & Class Breakdown

### `game_coordinator.py`
Implements `GameCoordinator`, mediating between `GameWorld`, `InputSystem`, `GameStateMachine`, `GameplayController`, and `GameRenderer`.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameCoordinator._bind_active_level` | `(self, level: Any) -> None` | *(Internal helper)* Binds active level to presentation renderer and resets gameplay controllers. |
| `GameCoordinator.start_game` | `(self) -> None` | Starts level 1, initializes display renderer, binds actors, and transitions to `PLAYING`. |
| `GameCoordinator._handle_level_completion` | `(self, level: Any) -> None` | *(Internal helper)* Advances to the next maze or transitions to `VICTORY` if all levels are cleared. |
| `GameCoordinator._check_game_over_conditions` | `(self, level: Any) -> None` | *(Internal helper)* Transitions to `GAME_OVER` if Pac-Man runs out of lives or level timer expires. |
| `GameCoordinator.update` | `(self, elapsed_seconds: float) -> None` | Drives simulation frame if in `PLAYING` state and evaluates progression/loss conditions. |
| `GameCoordinator.render` | `(self) -> None` | Dispatches render call to the active graphical presentation layer. |
| `GameCoordinator.shutdown` | `(self) -> None` | Safely releases presentation and Pygame display resources on exit. |
| `GameCoordinator._handle_menu_action` | `(self, action: InputAction) -> bool` | *(Internal helper)* Handles `START_GAME` input when browsing the main menu. |
| `GameCoordinator._handle_playing_action` | `(self, action: InputAction) -> bool` | *(Internal helper)* Handles `PAUSE_GAME` or forwards directional controls to `PlayerController`. |
| `GameCoordinator._handle_paused_action` | `(self, action: InputAction) -> bool` | *(Internal helper)* Handles `PAUSE_GAME` toggle to resume active gameplay. |
| `GameCoordinator._handle_navigation_action` | `(self, current_state: GameStateType, action: InputAction) -> bool` | *(Internal helper)* Routes `RETURN_TO_MENU` and enter-name navigation from game over and victory screens. |
| `GameCoordinator.handle_action` | `(self, action: InputAction) -> None` | Context-aware router directing user inputs to the appropriate state-specific action handler. |

---

### `main_loop.py`
Implements `MainGameLoop`, managing the continuous execution lifecycle.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MainGameLoop.start` | `(self) -> None` | Activates running flag (`is_running = True`). |
| `MainGameLoop.stop` | `(self) -> None` | Deactivates running flag (`is_running = False`). |
| `MainGameLoop.process_action` | `(self, action: InputAction) -> None` | Validates input action and passes it to coordinator, stopping the loop on `QUIT_GAME`. |
| `MainGameLoop.update` | `(self, elapsed_seconds: float) -> None` | Ticks game coordinator simulation by delta time while running. |
| `MainGameLoop.render` | `(self) -> None` | Dispatches frame render request to coordinator while running. |
| `MainGameLoop._execute_frame` | `(self, elapsed_seconds: float) -> None` | *(Internal helper)* Executes simulation update followed immediately by presentation render. |
| `MainGameLoop.run_once` | `(self, elapsed_seconds: float, action: InputAction \| None = None) -> None` | Executes a single discrete loop iteration (action ingestion -> update -> render). |

