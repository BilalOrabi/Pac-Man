"""Scoring system for the Pac-Man game."""


class ScoringSystem:
    """Manage score calculations for Pac-Man gameplay."""

    def __init__(
        self,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int,
    ) -> None:
        """Initialize the scoring rules."""
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost

    def calculate_pacgum_score(self) -> int:
        """Return the points awarded for eating a regular pacgum."""
        return self.points_per_pacgum

    def calculate_super_pacgum_score(self) -> int:
        """Return the points awarded for eating a super pacgum."""
        return self.points_per_super_pacgum

    def calculate_ghost_score(self) -> int:
        """Return the points awarded for defeating a ghost."""
        return self.points_per_ghost
