"""Factory for constructing playable Pac-Man levels."""

import random

from src.config.game_config import GameConfig, LevelConfig
from src.entities.ghost import Ghost, GhostType
from src.entities.player import Player
from src.maze.adapter import MazeAdapter
from src.maze.maze import Coordinate, Maze
from src.world.level import Level


class LevelFactory:
    """Create Level objects and their runtime entities."""

    def __init__(
        self,
        maze_adapter: MazeAdapter,
        game_configuration: GameConfig,
    ) -> None:
        """Initialize the factory with maze and game configuration."""
        self.maze_adapter = maze_adapter
        self.game_configuration = game_configuration

    @staticmethod
    def _place_super_pacgums(maze: Maze) -> set[Coordinate]:
        """Place super-pacgums in open corners of the maze."""
        corners = {
            (0, 0),
            (maze.width - 1, 0),
            (0, maze.height - 1),
            (maze.width - 1, maze.height - 1),
        }
        return {
            c for c in corners
            if maze.is_inside(*c) and not maze.get_cell(c).is_solid_block
        }

    @staticmethod
    def _distribute_pacgums(
        maze: Maze,
        player_pos: Coordinate,
        super_pacgums: set[Coordinate],
        pacgum_count: int,
        maze_seed: int,
    ) -> set[Coordinate]:
        """Sample and distribute regular pacgums across open corridors."""
        walkable = [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if not maze.get_cell((x, y)).is_solid_block
            and (x, y) not in super_pacgums
            and (x, y) != player_pos
        ]
        target_regular = max(0, pacgum_count - len(super_pacgums))
        rng = random.Random(maze_seed)
        if 0 < target_regular < len(walkable):
            return set(rng.sample(walkable, target_regular))
        if target_regular >= len(walkable):
            return set(walkable)
        return set()

    def create_level(
        self,
        level_number: int,
        level_configuration: LevelConfig,
        maze_seed: int,
        pacgum_count: int,
    ) -> Level:
        """Create a complete playable level."""
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

        player = self._create_player(maze)
        ghosts = self._create_ghosts(maze)

        super_pacgums = self._place_super_pacgums(maze)
        pacgums = self._distribute_pacgums(
            maze, player.position, super_pacgums, pacgum_count, maze_seed
        )

        total_pacgums = (
            len(pacgums) + len(super_pacgums)
            if (pacgums or super_pacgums)
            else pacgum_count
        )

        return Level(
            number=level_number,
            configuration=level_configuration,
            maze=maze,
            remaining_pacgums=total_pacgums,
            player=player,
            ghosts=ghosts,
            pacgums=pacgums,
            super_pacgums=super_pacgums,
        )

    def _create_player(self, maze: Maze) -> Player:
        """Create the player at the maze entry."""
        return Player(
            position=maze.entry,
            speed=self.game_configuration.player_speed,
            lives=self.game_configuration.lives,
        )

    def _create_ghosts(self, maze: Maze) -> list[Ghost]:
        """Create the four standard ghosts in the 4 corners of the maze."""
        corners = (
            (0, 0),
            (maze.width - 1, 0),
            (0, maze.height - 1),
            (maze.width - 1, maze.height - 1),
        )

        ghost_types = (
            GhostType.RED,
            GhostType.PINK,
            GhostType.BLUE,
            GhostType.ORANGE,
        )

        return [
            Ghost(
                position=corner,
                ghost_type=ghost_type,
                home_position=corner,
                speed=self.game_configuration.ghost_speed,
            )
            for corner, ghost_type in zip(corners, ghost_types)
        ]
