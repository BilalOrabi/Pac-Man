"""Factory for constructing playable Pac-Man levels."""

from src.config.game_config import LevelConfig
from src.maze.adapter import MazeAdapter
from src.world.level import Level


class LevelFactory:
    """Create Level objects from validated level configuration."""

    def __init__(self, maze_adapter: MazeAdapter) -> None:
        """Initialize the level factory with a maze adapter."""
        self.maze_adapter = maze_adapter

    def create_level(
        self,
        level_number: int,
        level_configuration: LevelConfig,
        maze_seed: int,
        pacgum_count: int,
    ) -> Level:
        """Create a playable level from its configuration.

        Args:
            level_number: One-based number identifying the level.
            level_configuration: Dimensions and settings for the level.
            maze_seed: Seed used to generate the maze.
            pacgum_count: Number of pacgums placed in the level.

        Returns:
            A newly constructed Level.

        Raises:
            ValueError: If the level number or pacgum count is invalid.
            MazeGenerationError: If maze generation fails.
        """
        if level_number <= 0:
            raise ValueError(
                "Level number must be greater than zero."
            )

        if pacgum_count < 0:
            raise ValueError(
                "Pacgum count cannot be negative."
            )

        maze = self.maze_adapter.generate_level(
            width=level_configuration.width,
            height=level_configuration.height,
            seed=maze_seed,
        )

        return Level(
            number=level_number,
            configuration=level_configuration,
            maze=maze,
            remaining_pacgums=pacgum_count,
        )
