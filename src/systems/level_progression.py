"""System responsible for progressing between Pac-Man levels."""

from enum import Enum

from src.world.game_world import GameWorld
from src.world.level import Level


class LevelProgressionResult(Enum):
    """Represent the result of attempting to progress the game."""

    NEXT_LEVEL = "next_level"
    VICTORY = "victory"
    LEVEL_NOT_COMPLETED = "level_not_completed"


class LevelProgressionSystem:
    """Handle progression from completed levels to the next level."""

    def progress(self, game_world: GameWorld) -> LevelProgressionResult:
        """Progress the game when the current level is completed.

        Args:
            game_world: Runtime world containing the current level.

        Returns:
            The result describing what happened.

        Raises:
            ValueError: If the game world has not been started.
        """
        current_level = game_world.current_level

        if current_level is None:
            raise ValueError(
                "Cannot progress levels before the game world is started."
            )

        if not current_level.completed:
            return LevelProgressionResult.LEVEL_NOT_COMPLETED

        if game_world.has_completed_all_levels():
            return LevelProgressionResult.VICTORY

        next_level = game_world.advance_to_next_level()

        if next_level is None:
            return LevelProgressionResult.VICTORY

        return LevelProgressionResult.NEXT_LEVEL

    @staticmethod
    def is_level_completed(level: Level) -> bool:
        """Return whether the specified level has been completed."""
        return level.completed
