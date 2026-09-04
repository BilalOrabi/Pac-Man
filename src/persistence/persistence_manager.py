"""Persistence management for the Pac-Man game."""

import json
from pathlib import Path
from typing import Any


class PersistenceManager:
    """Save and load Pac-Man game data from a JSON file."""

    def __init__(self, file_path: str | Path) -> None:
        """Create a persistence manager for the specified file."""
        self.file_path = Path(file_path)

    def save_data(self, data: dict[str, Any]) -> None:
        """Save game data to the persistence file."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.file_path.open(
            mode="w",
            encoding="utf-8",
        ) as persistence_file:
            json.dump(
                data,
                persistence_file,
                indent=4,
            )

    def load_data(self) -> dict[str, Any]:
        """Load game data from the persistence file."""
        if not self.file_path.exists():
            return {}

        with self.file_path.open(
            mode="r",
            encoding="utf-8",
        ) as persistence_file:
            loaded_data = json.load(persistence_file)

        if not isinstance(loaded_data, dict):
            raise ValueError(
                "Persistence file must contain a JSON object."
            )

        return loaded_data

    def delete_data(self) -> None:
        """Delete the persistence file if it exists."""
        if self.file_path.exists():
            self.file_path.unlink()

    def has_data(self) -> bool:
        """Return whether a persistence file exists."""
        return self.file_path.exists()
