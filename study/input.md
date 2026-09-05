# Input Module (`src/input/`)

## 1. Module Overview
The `input` module abstracts presentation-layer input events away from domain gameplay systems. It captures raw hardware input events from Pygame, normalizes them into typed, platform-agnostic actions (`InputAction`), maps directional keys (WASD, Arrows) to spatial `Direction` enums, and maintains the current player input buffer (`InputState`). This ensures the core game logic never depends directly on Pygame keyboard codes.

---

## 2. File & Class Breakdown

### `input_event.py`
Defines typed actions and event containers representing user intent.

| Function / Method / Class | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputAction` | `Enum` | Enumeration of all discrete game actions (`MOVE_UP`, `MOVE_DOWN`, `MOVE_LEFT`, `MOVE_RIGHT`, `PAUSE_GAME`, `START_GAME`, `RESTART_GAME`, `RETURN_TO_MENU`, `QUIT_GAME`). |
| `InputEvent` | `@dataclass(frozen=True)` | Immutable container holding the dispatched `action`. |

---

### `input_handler.py`
Implements `InputHandler`, converting raw Pygame events into typed `InputEvent` instances.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputHandler._is_quit_event` | `(pygame_event: pygame.event.Event) -> bool` | *(Internal helper)* Identifies whether the Pygame event is a window close / quit request (`pygame.QUIT`). |
| `InputHandler.process_event` | `(self, pygame_event: pygame.event.Event) -> InputEvent \| None` | Converts raw Pygame event into typed `InputEvent`, or returns `None` for unhandled events. |
| `InputHandler._process_keydown_event` | `(self, pygame_event: pygame.event.Event) -> InputEvent \| None` | *(Internal helper)* Converts a keyboard key-down event into the corresponding game input action. |
| `InputHandler._get_keyboard_action` | `(key_code: int) -> InputAction \| None` | *(Internal helper)* Maps hardware key codes (Arrows, WASD, ESC, Space, Enter, R, M) to `InputAction`. |

---

### `input_mapper.py`
Implements `InputMapper`, bridging input actions to spatial navigation.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputMapper.get_direction` | `(input_action: InputAction) -> Direction \| None` | Converts movement actions (`MOVE_UP`, `MOVE_DOWN`, etc.) to spatial `Direction` enums, returning `None` for non-movement actions. |

---

### `input_state.py`
Implements `InputState`, storing the player's active movement heading request.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputState.set_direction` | `(self, direction: Direction) -> None` | Stores the newly requested heading from the user. |
| `InputState.clear_direction` | `(self) -> None` | Resets the requested direction back to `Direction.NONE`. |
| `InputState.has_requested_direction` | `(self) -> bool` | Checks whether an active movement direction has been registered. |

---

### `input_manager.py`
Implements `InputManager`, maintaining the active input state across game ticks.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputManager.__init__` | `(self) -> None` | Initializes the manager with a clean `InputState`. |
| `InputManager._apply_action` | `(self, action: InputAction) -> None` | *(Internal helper)* Maps action to movement direction to update state, or clears direction on restart. |
| `InputManager.process_event` | `(self, input_event: InputEvent) -> None` | Ingests a typed event and updates the managed `InputState`. |
| `InputManager.get_requested_direction` | `(self) -> Direction` | Returns the player's currently requested movement heading. |
| `InputManager.clear_direction` | `(self) -> None` | Clears any pending movement requests from the buffer. |

---

### `input_system.py`
Implements `InputSystem`, coordinating Pygame event pumping into the input manager.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `InputSystem.__init__` | `(self, input_handler=None, input_manager=None) -> None` | Initializes the system with handler and manager instances. |
| `InputSystem._dispatch_single_event` | `(self, pygame_event: pygame.event.Event) -> None` | *(Internal helper)* Processes an individual Pygame event and routes it to `InputManager` if valid. |
| `InputSystem.process_events` | `(self) -> None` | Polls Pygame's event queue and dispatches all events for the current frame. |

