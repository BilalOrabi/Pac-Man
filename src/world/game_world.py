"""Runtime world containing the active Pac-Man level."""

from dataclasses import dataclass

from src.config.game_config import GameConfig
from src.world.level import Level
from src.world.level_factory import LevelFactory


@dataclass
class GameWorld:
    """Manage the currently active Pac-Man level."""

    game_configuration: GameConfig
    level_factory: LevelFactory
    current_level_index: int = 0
    current_level: Level | None = None
    start_called: bool = False

    @property
    def current_level_number(self) -> int:
        """Expose the 1-based level number for runtime callers."""
        return self.current_level_index + 1

    @current_level_number.setter
    def current_level_number(self, value: int) -> None:
        """Keep the 1-based alias synchronized with the zero-based index."""
        self.current_level_index = value - 1

    def start(self) -> Level:
        """Start the game by creating the first configured level."""
        self.current_level_index = 0
        self.current_level = self._create_level(
            self.current_level_index
        )
        self.start_called = True

        return self.current_level

    def advance_to_next_level(self) -> Level | None:
        """Create and activate the next configured level."""
        preserved_score = 0
        preserved_lives = self.game_configuration.lives
        if (
            self.current_level is not None
            and self.current_level.player is not None
        ):
            preserved_score = self.current_level.player.score
            preserved_lives = self.current_level.player.lives

        next_level_index = self.current_level_index + 1

        if next_level_index >= len(self.game_configuration.levels):
            self.current_level = None
            return None

        self.current_level_index = next_level_index
        self.current_level = self._create_level(
            next_level_index
        )
        if self.current_level.player is not None:
            self.current_level.player.score = preserved_score
            self.current_level.player.lives = preserved_lives

        return self.current_level

    def has_completed_all_levels(self) -> bool:
        """Return whether the final configured level is complete."""
        if self.current_level is None:
            return False

        return (
            self.current_level_index
            >= len(self.game_configuration.levels) - 1
            and self.current_level.completed
        )

    def update(self, elapsed_seconds: float) -> None:
        """Update the active level."""
        if elapsed_seconds < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        if self.current_level is None:
            return

        self.current_level.update_time(elapsed_seconds)

    def _create_level(self, level_index: int) -> Level:
        """Create a level using the configured level settings."""
        level_configuration = self.game_configuration.levels[
            level_index
        ]

        maze_seed = self.game_configuration.seed + level_index

        return self.level_factory.create_level(
            level_number=level_index + 1,
            level_configuration=level_configuration,
            maze_seed=maze_seed,
            pacgum_count=self.game_configuration.pacgum,
        )
