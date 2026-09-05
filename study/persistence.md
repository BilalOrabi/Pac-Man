# Persistence Module (`src/persistence/`)

## 1. Module Overview
The `persistence` module provides robust filesystem I/O operations for serializing and deserializing application data (such as high-score records) to and from JSON files. It abstracts directory creation, file existence verification, safe deletion, and structured JSON parsing.

---

## 2. File & Class Breakdown

### `persistence_manager.py`
Implements `PersistenceManager`, providing resilient JSON disk persistence.

| Function / Method | Signature | Purpose & Job |
| :--- | :--- | :--- |
| `PersistenceManager.__init__` | `(self, file_path: str \| Path) -> None` | Stores and converts target storage location into a `pathlib.Path`. |
| `PersistenceManager._ensure_parent_directory` | `(self) -> None` | *(Internal helper)* Creates missing parent folder trees (`mkdir(parents=True, exist_ok=True)`). |
| `PersistenceManager.save_data` | `(self, data: dict[str, Any]) -> None` | Enforces dictionary type, ensures directory structure, and dumps formatted JSON with 4-space indent. |
| `PersistenceManager._validate_loaded_dict` | `(data: Any) -> dict[str, Any]` | *(Internal helper)* Asserts deserialized content is a valid JSON dictionary structure. |
| `PersistenceManager.load_data` | `(self) -> dict[str, Any]` | Reads persistence file, returning empty dictionary `{}` if file does not exist. |
| `PersistenceManager.delete_data` | `(self) -> None` | Unlinks and removes persistent data file from the filesystem if present. |
| `PersistenceManager.has_data` | `(self) -> bool` | Checks whether the target file currently exists on disk. |

