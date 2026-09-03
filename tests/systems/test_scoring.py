"""Tests for the scoring system."""

from src.systems.scoring import ScoringSystem


def create_scoring_system() -> ScoringSystem:
    """Create a scoring system with the project's default values."""
    return ScoringSystem(
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
    )


def test_pacgum_score() -> None:
    """Eating a regular pacgum should award the configured points."""
    scoring_system = create_scoring_system()

    assert scoring_system.calculate_pacgum_score() == 10


def test_super_pacgum_score() -> None:
    """Eating a super pacgum should award the configured points."""
    scoring_system = create_scoring_system()

    assert scoring_system.calculate_super_pacgum_score() == 50


def test_ghost_score() -> None:
    """Defeating a ghost should award the configured points."""
    scoring_system = create_scoring_system()

    assert scoring_system.calculate_ghost_score() == 200


def test_scoring_system_uses_custom_values() -> None:
    """Scoring should use the values supplied during initialization."""
    scoring_system = ScoringSystem(
        points_per_pacgum=15,
        points_per_super_pacgum=75,
        points_per_ghost=300,
    )

    assert scoring_system.calculate_pacgum_score() == 15
    assert scoring_system.calculate_super_pacgum_score() == 75
    assert scoring_system.calculate_ghost_score() == 300
