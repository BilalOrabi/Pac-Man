"""High-score management for the Pac-Man game."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HighscoreEntry:
    """Represent one high-score entry."""

    player_name: str
    score: int


@dataclass
class HighscoreManager:
    """Manage and rank Pac-Man high scores."""

    maximum_entries: int = 10
    entries: list[HighscoreEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the high-score configuration."""
        if self.maximum_entries <= 0:
            raise ValueError(
                "maximum_entries must be greater than zero."
            )

        self._sort_entries()

    @staticmethod
    def validate_player_name(player_name: str) -> bool:
        """Validate player name is 1-10 chars, alphanumeric and spaces."""
        if not isinstance(player_name, str):
            return False
        if not player_name or len(player_name) > 10:
            return False
        if not player_name.strip():
            return False
        return all(c.isalnum() or c == " " for c in player_name)

    def add_score(self, player_name: str, score: int) -> None:
        """Add a score and keep the leaderboard ordered."""
        if not self.validate_player_name(player_name):
            raise ValueError(
                "player_name must be 1 to 10 alphanumeric/space chars."
            )

        if score < 0:
            raise ValueError("score cannot be negative.")

        self.entries.append(
            HighscoreEntry(
                player_name=player_name,
                score=score,
            )
        )

        self._sort_entries()
        self.entries = self.entries[: self.maximum_entries]

    def get_entries(self) -> list[HighscoreEntry]:
        """Return the current high-score entries."""
        return list(self.entries)

    def get_highest_score(self) -> int:
        """Return the highest recorded score."""
        if not self.entries:
            return 0

        return self.entries[0].score

    def qualifies_for_highscore(self, score: int) -> bool:
        """Return whether a score belongs on the leaderboard."""
        if score < 0:
            raise ValueError("score cannot be negative.")

        if len(self.entries) < self.maximum_entries:
            return True

        return score > self.entries[-1].score

    def clear(self) -> None:
        """Remove all high-score entries."""
        self.entries.clear()

    def _sort_entries(self) -> None:
        """Sort entries from highest score to lowest score."""
        self.entries.sort(
            key=lambda entry: entry.score,
            reverse=True,
        )
