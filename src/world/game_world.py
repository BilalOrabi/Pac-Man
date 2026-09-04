"""Runtime world containing the game's levels and current level."""

from dataclasses import dataclass

from src.config.game_config import GameConfig
from src.world.level import Level
from src.world.level_factory import LevelFactory


@dataclass
class GameWorld:
    """Manage the levels that make up a Pac-Man game session."""

    game_configuration: GameConfig
    level_factory: LevelFactory
    current_level_index: int = 0
    current_level: Level | None = None
    start_called: bool = False

    def start(self) -> Level:
        """Create and start the first level."""
        self.current_level_index = 0
        self.current_level = self._create_level(
            self.current_level_index
        )
        self.start_called = True

        return self.current_level

    def advance_to_next_level(self) -> Level | None:
        """Advance to the next configured level.

        Returns:
            The newly created level, or None when all levels are complete.
        """
        next_level_index = self.current_level_index + 1

        if next_level_index >= len(self.game_configuration.levels):
            self.current_level = None
            return None

        self.current_level_index = next_level_index
        self.current_level = self._create_level(
            self.current_level_index
        )

        return self.current_level

    def has_completed_all_levels(self) -> bool:
        """Return whether every configured level has been completed."""
        return (
            self.current_level_index
            >= len(self.game_configuration.levels) - 1
            and self.current_level is not None
            and self.current_level.completed
        )

    def _create_level(self, level_index: int) -> Level:
        """Create a level from the configured level index."""
        level_configuration = self.game_configuration.levels[
            level_index
        ]

        return self.level_factory.create_level(
            level_number=level_index + 1,
            level_configuration=level_configuration,
            maze_seed=self.game_configuration.seed + level_index,
            pacgum_count=self.game_configuration.pacgum,
        )
