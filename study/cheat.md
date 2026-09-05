# Cheat Module (`src/cheat/`)

## 1. Module Overview
The `cheat` module implements developer debug aids and grading evaluation cheats required by Chapter 6.7 of the 42 School curriculum. Controlled via keyboard number keys (1-5) during gameplay, these features allow peer evaluators to verify later levels, test entity collision outcomes without dying, freeze ghost pathfinding, and inspect speed multipliers without modifying configuration files.

---

## 2. File & Class Breakdown

### `cheat_system.py`
Implements `CheatSystem`, holding reactive telemetry toggles and level skip flags.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `CheatSystem._toggle_flag` | `(self, attr_name: str) -> bool` | *(Internal helper)* Inverts a designated boolean cheat flag attribute and returns the updated state. |
| `CheatSystem.toggle_invincibility` | `(self) -> bool` | Toggles player immunity from ghost collisions (Key `1`). |
| `CheatSystem.toggle_infinite_lives` | `(self) -> bool` | Toggles infinite lives prevention from game-over triggers. |
| `CheatSystem.toggle_power_mode` | `(self) -> bool` | Toggles persistent frightened / edible ghost mode. |
| `CheatSystem.toggle_ghost_freeze` | `(self) -> bool` | Toggles freezing all ghost pathfinding updates (Key `2`). |
| `CheatSystem.toggle_speed_boost` | `(self) -> bool` | Toggles 2.2x player locomotion speed multiplier (Key `3`). |
| `CheatSystem.trigger_level_skip` | `(self) -> None` | Sets a one-shot request flag to advance immediately to the next maze (Key `5`). |
| `CheatSystem._clear_all_flags` | `(self) -> None` | *(Internal helper)* Resets every boolean cheat toggle back to inactive `False`. |
| `CheatSystem.reset` | `(self) -> None` | Disables all cheats simultaneously. |

