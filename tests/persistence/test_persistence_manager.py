"""Tests for the Pac-Man persistence manager."""

import json

import pytest

from src.persistence.persistence_manager import PersistenceManager


def test_persistence_manager_starts_without_data(
    tmp_path,
) -> None:
    """A new persistence manager should have no saved data."""
    file_path = tmp_path / "game_data.json"

    persistence_manager = PersistenceManager(file_path)

    assert persistence_manager.has_data() is False
    assert persistence_manager.load_data() == {}


def test_save_data_creates_persistence_file(
    tmp_path,
) -> None:
    """Saving data should create the persistence file."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    persistence_manager.save_data(
        {
            "score": 1000,
            "lives": 2,
        }
    )

    assert file_path.exists()
    assert persistence_manager.has_data() is True


def test_save_data_can_be_loaded(
    tmp_path,
) -> None:
    """Saved data should be recoverable."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    game_data = {
        "score": 2500,
        "lives": 3,
        "level": 2,
    }

    persistence_manager.save_data(game_data)

    assert persistence_manager.load_data() == game_data


def test_save_data_overwrites_previous_data(
    tmp_path,
) -> None:
    """Saving new data should replace the previous data."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    persistence_manager.save_data({"score": 100})
    persistence_manager.save_data({"score": 500})

    assert persistence_manager.load_data() == {
        "score": 500,
    }


def test_save_data_creates_parent_directories(
    tmp_path,
) -> None:
    """Saving should create missing parent directories."""
    file_path = (
        tmp_path
        / "data"
        / "saves"
        / "game_data.json"
    )

    persistence_manager = PersistenceManager(file_path)

    persistence_manager.save_data({"score": 100})

    assert file_path.exists()
    assert persistence_manager.load_data() == {
        "score": 100,
    }


def test_load_data_returns_empty_dictionary_for_missing_file(
    tmp_path,
) -> None:
    """Loading a missing file should return an empty dictionary."""
    file_path = tmp_path / "missing.json"
    persistence_manager = PersistenceManager(file_path)

    assert persistence_manager.load_data() == {}


def test_delete_data_removes_existing_file(
    tmp_path,
) -> None:
    """Deleting data should remove the persistence file."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    persistence_manager.save_data({"score": 100})

    persistence_manager.delete_data()

    assert file_path.exists() is False
    assert persistence_manager.has_data() is False


def test_delete_data_is_safe_when_file_does_not_exist(
    tmp_path,
) -> None:
    """Deleting missing data should not raise an error."""
    file_path = tmp_path / "missing.json"
    persistence_manager = PersistenceManager(file_path)

    persistence_manager.delete_data()

    assert persistence_manager.has_data() is False


def test_save_data_rejects_non_dictionary_data(
    tmp_path,
) -> None:
    """Persistence should only accept dictionaries."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    with pytest.raises(TypeError):
        persistence_manager.save_data(
            ["invalid", "data"]  # type: ignore[arg-type]
        )


def test_load_data_rejects_non_object_json(
    tmp_path,
) -> None:
    """A JSON array should not be accepted as game data."""
    file_path = tmp_path / "game_data.json"

    file_path.write_text(
        json.dumps(["invalid", "data"]),
        encoding="utf-8",
    )

    persistence_manager = PersistenceManager(file_path)

    with pytest.raises(ValueError):
        persistence_manager.load_data()


def test_nested_game_data_is_preserved(
    tmp_path,
) -> None:
    """Nested JSON-compatible game data should be preserved."""
    file_path = tmp_path / "game_data.json"
    persistence_manager = PersistenceManager(file_path)

    game_data = {
        "player": {
            "score": 5000,
            "lives": 2,
        },
        "level": {
            "number": 3,
            "completed": False,
        },
    }

    persistence_manager.save_data(game_data)

    assert persistence_manager.load_data() == game_data
