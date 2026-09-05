# Highscore Module (`src/highscore/`)

## 1. Module Overview
The `highscore` module manages in-memory ranking and validation for the top 10 arcade high scores. It enforces strict player name sanitization (1 to 10 characters, restricted to alphanumeric characters and spaces) and deterministic descending order sorting, determining whether completed matches qualify for persistent leaderboard preservation.

---

## 2. File & Class Breakdown

### `highscore_manager.py`
Implements `HighscoreEntry` and `HighscoreManager`.

| Function / Method / Class | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `HighscoreEntry` | `@dataclass(frozen=True)` | Immutable pair binding `player_name: str` and `score: int`. |
| `HighscoreManager.__post_init__` | `(self) -> None` | Asserts positive maximum capacity (`> 0`) and sorts starting entries. |
| `HighscoreManager.validate_player_name` | `(player_name: str) -> bool` | Enforces 1-10 alphanumeric characters and non-blank spaces. |
| `HighscoreManager._validate_score_input` | `(self, player_name: str, score: int) -> None` | *(Internal helper)* Validates candidate player name and asserts non-negative score. |
| `HighscoreManager._sort_and_truncate` | `(self) -> None` | *(Internal helper)* Sorts records descending by score and clamps list to `maximum_entries`. |
| `HighscoreManager.add_score` | `(self, player_name: str, score: int) -> None` | Validates input, inserts score, and retains top entries in sorted order. |
| `HighscoreManager.get_entries` | `(self) -> list[HighscoreEntry]` | Returns a protective defensive copy of all active leaderboard records. |
| `HighscoreManager.get_highest_score` | `(self) -> int` | Retrieves top record score (rank 1), or returns 0 if table is empty. |
| `HighscoreManager.qualifies_for_highscore` | `(self, score: int) -> bool` | Checks if candidate score beats lowest leaderboard entry or if slots remain open. |
| `HighscoreManager.clear` | `(self) -> None` | Purges all leaderboard records from memory. |
| `HighscoreManager._sort_entries` | `(self) -> None` | *(Internal helper)* Sorts internal list in-place descending by score value. |

