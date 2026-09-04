"""Tests for the Pac-Man high-score manager."""

import pytest

from src.highscore.highscore_manager import (
    HighscoreEntry,
    HighscoreManager,
)


def test_highscore_manager_starts_empty() -> None:
    """The leaderboard should initially be empty."""
    manager = HighscoreManager()

    assert manager.get_entries() == []
    assert manager.get_highest_score() == 0


def test_add_score_creates_entry() -> None:
    """Adding a score should create a leaderboard entry."""
    manager = HighscoreManager()

    manager.add_score("HAMZA", 1000)

    assert manager.get_entries() == [
        HighscoreEntry(
            player_name="HAMZA",
            score=1000,
        )
    ]


def test_scores_are_sorted_highest_first() -> None:
    """Scores should be ordered from highest to lowest."""
    manager = HighscoreManager()

    manager.add_score("PLAYER1", 500)
    manager.add_score("PLAYER2", 2000)
    manager.add_score("PLAYER3", 1000)

    assert manager.get_entries() == [
        HighscoreEntry("PLAYER2", 2000),
        HighscoreEntry("PLAYER3", 1000),
        HighscoreEntry("PLAYER1", 500),
    ]


def test_highest_score_returns_top_score() -> None:
    """The highest score should be returned."""
    manager = HighscoreManager()

    manager.add_score("PLAYER1", 500)
    manager.add_score("PLAYER2", 2500)

    assert manager.get_highest_score() == 2500


def test_highest_score_is_zero_when_empty() -> None:
    """An empty leaderboard should have a highest score of zero."""
    manager = HighscoreManager()

    assert manager.get_highest_score() == 0


def test_manager_limits_number_of_entries() -> None:
    """The leaderboard should keep only the configured number of entries."""
    manager = HighscoreManager(maximum_entries=3)

    manager.add_score("PLAYER1", 100)
    manager.add_score("PLAYER2", 300)
    manager.add_score("PLAYER3", 200)
    manager.add_score("PLAYER4", 400)

    assert manager.get_entries() == [
        HighscoreEntry("PLAYER4", 400),
        HighscoreEntry("PLAYER2", 300),
        HighscoreEntry("PLAYER3", 200),
    ]


def test_low_score_is_removed_when_leaderboard_is_full() -> None:
    """A new higher score should replace the lowest score."""
    manager = HighscoreManager(maximum_entries=2)

    manager.add_score("PLAYER1", 100)
    manager.add_score("PLAYER2", 200)
    manager.add_score("PLAYER3", 300)

    assert manager.get_entries() == [
        HighscoreEntry("PLAYER3", 300),
        HighscoreEntry("PLAYER2", 200),
    ]


def test_get_entries_returns_copy() -> None:
    """Getting entries should not expose the internal list."""
    manager = HighscoreManager()
    manager.add_score("PLAYER1", 100)

    entries = manager.get_entries()
    entries.clear()

    assert manager.get_entries() == [
        HighscoreEntry("PLAYER1", 100)
    ]


def test_score_qualifies_when_leaderboard_has_space() -> None:
    """Any valid score should qualify when the leaderboard has space."""
    manager = HighscoreManager(maximum_entries=3)

    assert manager.qualifies_for_highscore(100) is True


def test_score_qualifies_when_higher_than_lowest_score() -> None:
    """A score above the lowest score should qualify."""
    manager = HighscoreManager(maximum_entries=2)

    manager.add_score("PLAYER1", 100)
    manager.add_score("PLAYER2", 200)

    assert manager.qualifies_for_highscore(300) is True


def test_score_does_not_qualify_when_lower_than_lowest_score() -> None:
    """A low score should not qualify when the leaderboard is full."""
    manager = HighscoreManager(maximum_entries=2)

    manager.add_score("PLAYER1", 100)
    manager.add_score("PLAYER2", 200)

    assert manager.qualifies_for_highscore(50) is False


def test_clear_removes_all_entries() -> None:
    """Clearing should remove every high-score entry."""
    manager = HighscoreManager()

    manager.add_score("PLAYER1", 100)
    manager.add_score("PLAYER2", 200)

    manager.clear()

    assert manager.get_entries() == []


def test_empty_player_name_is_rejected() -> None:
    """An empty player name should be rejected."""
    manager = HighscoreManager()

    with pytest.raises(ValueError):
        manager.add_score("", 100)


def test_whitespace_player_name_is_rejected() -> None:
    """A whitespace-only player name should be rejected."""
    manager = HighscoreManager()

    with pytest.raises(ValueError):
        manager.add_score("   ", 100)


def test_negative_score_is_rejected() -> None:
    """Negative scores should be rejected."""
    manager = HighscoreManager()

    with pytest.raises(ValueError):
        manager.add_score("PLAYER", -1)


def test_negative_qualification_score_is_rejected() -> None:
    """Negative qualification scores should be rejected."""
    manager = HighscoreManager()

    with pytest.raises(ValueError):
        manager.qualifies_for_highscore(-1)


def test_invalid_maximum_entries_is_rejected() -> None:
    """The leaderboard size must be positive."""
    with pytest.raises(ValueError):
        HighscoreManager(maximum_entries=0)
