# States Module (`src/states/`)

## 1. Module Overview
The `states` module manages the high-level finite state machine governing the Pac-Man application lifecycle. It encapsulates screen transitions and execution contexts across Menu, Active Gameplay, Paused, Game Over, Victory, and Name Entry screens. By enforcing state boundaries through `GameStateMachine`, the application prevents illegal actions (e.g. moving actors while paused or receiving keyboard gameplay input in menus).

---

## 2. File & Class Breakdown

### `game_state.py`
Defines the enumeration of all supported application modes.

| Class / Enum | Values | Purpose & Job |
| :--- | :--- | :--- |
| `GameStateType` | `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`, `VICTORY`, `ENTER_NAME` | Distinct states representing the entire user flow and screen hierarchy. |

---

### `state_machine.py`
Implements `GameStateMachine`, the deterministic state transition controller.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameStateMachine._validate_state` | `(state: object, param_name: str) -> None` | *(Internal helper)* Validates that candidate state is a genuine `GameStateType` instance. |
| `GameStateMachine.transition_to` | `(self, next_state: GameStateType) -> None` | Atomically transitions active application state to `next_state`. |
| `GameStateMachine.is_in_state` | `(self, game_state: GameStateType) -> bool` | Checks whether the machine is currently executing within the specified state. |

---

### `menu_state.py`
Implements `MenuState`, governing main menu interactions.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `MenuState.start_game` | `(self) -> None` | Initiates fresh game session by transitioning to `PLAYING`. |
| `MenuState.is_active` | `(self) -> bool` | Queries whether the main menu screen is currently active. |

---

### `playing_state.py`
Implements `PlayingState`, representing active maze exploration and combat.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PlayingState.pause_game` | `(self) -> None` | Suspends active gameplay by transitioning to `PAUSED`. |
| `PlayingState.end_game` | `(self) -> None` | Concludes match upon zero lives, transitioning to `GAME_OVER`. |
| `PlayingState.complete_game` | `(self) -> None` | Triggers game win sequence by transitioning to `VICTORY`. |
| `PlayingState.is_active` | `(self) -> bool` | Queries whether active gameplay is currently running. |

---

### `paused_state.py`
Implements `PausedState`, halting world updates while retaining full game state.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PausedState.resume_game` | `(self) -> None` | Restores gameplay loop by transitioning to `PLAYING`. |
| `PausedState.return_to_menu` | `(self) -> None` | Aborts paused session and returns to `MENU`. |
| `PausedState.is_active` | `(self) -> bool` | Queries whether gameplay is currently suspended. |

---

### `game_over_state.py`
Implements `GameOverState`, handling post-loss user decisions.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `GameOverState.restart_game` | `(self) -> None` | Restarts game immediately from Level 1 (`PLAYING`). |
| `GameOverState.return_to_menu` | `(self) -> None` | Leaves game-over screen to return to `MENU`. |
| `GameOverState.is_active` | `(self) -> bool` | Queries whether the game-over screen is displayed. |

---

### `victory_state.py`
Implements `VictoryState`, celebrating successful maze completion.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `VictoryState.return_to_menu` | `(self) -> None` | Returns to `MENU` after viewing victory screen. |
| `VictoryState.start_new_game` | `(self) -> None` | Launches brand new campaign (`PLAYING`). |
| `VictoryState.is_active` | `(self) -> bool` | Queries whether the victory celebration screen is active. |

---

### `enter_name_state.py`
Implements `EnterNameState`, managing interactive arcade name entry for the leaderboard.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `EnterNameState._validate_character` | `(character: object) -> None` | *(Internal helper)* Asserts character input is a single string character. |
| `EnterNameState.add_character` | `(self, character: str) -> None` | Appends a typed alphanumeric character (max 10 chars). |
| `EnterNameState.remove_character` | `(self) -> None` | Deletes the trailing character (backspace behavior). |
| `EnterNameState.confirm_name` | `(self) -> str` | Commits and returns the completed player name string. |
| `EnterNameState.is_active` | `(self) -> bool` | Queries whether name input dialog is active. |
| `EnterNameState.reset` | `(self) -> None` | Clears current input buffer back to empty string. |

