"""Tests for the level progression system."""

import pytest

from src.config.game_config import GameConfig, LevelConfig
from src.maze.maze import Maze, MazeCell, Wall
from src.systems.level_progression import (
    LevelProgressionResult,
    LevelProgressionSystem,
)
from src.world.game_world import GameWorld
from src.world.level import Level


class FakeLevelFactory:
    """Create predictable levels for progression tests."""

    def create_level(
        self,
        level_number: int,
        level_configuration: LevelConfig,
        maze_seed: int,
        pacgum_count: int,
    ) -> Level:
        """Create a simple test level."""
        cell = MazeCell(
            position=(0, 0),
            walls=Wall.ALL,
            is_solid_block=False,
        )

        maze = Maze(
            width=1,
            height=1,
            cells=((cell,),),
            entry=(0, 0),
            exit=(0, 0),
            shortest_path="",
        )

        return Level(
            number=level_number,
            configuration=level_configuration,
            maze=maze,
            remaining_pacgums=pacgum_count,
        )


def create_game_world(number_of_levels: int = 2) -> GameWorld:
    """Create a game world containing predictable test levels."""
    levels = tuple(
        LevelConfig(width=19, height=21)
        for _ in range(number_of_levels)
    )

    game_configuration = GameConfig(
        highscore_filename="highscores.json",
        lives=3,
        pacgum=1,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=42,
        level_max_time=90,
        player_speed=5.0,
        ghost_speed=4.0,
        frightened_ghost_speed=2.0,
        returning_ghost_speed=6.0,
        power_mode_duration=7.0,
        levels=levels,
    )

    return GameWorld(
        game_configuration=game_configuration,
        level_factory=FakeLevelFactory(),
    )


def test_progress_returns_level_not_completed_when_level_is_active() -> None:
    """Progression should not advance an incomplete level."""
    game_world = create_game_world()
    game_world.start()

    progression_system = LevelProgressionSystem()

    result = progression_system.progress(game_world)

    assert result == LevelProgressionResult.LEVEL_NOT_COMPLETED
    assert game_world.current_level_index == 0


def test_progress_advances_to_next_level_when_current_level_is_completed() -> None:
    """Progression should create the next level after completion."""
    game_world = create_game_world()
    current_level = game_world.start()
    current_level.completed = True

    progression_system = LevelProgressionSystem()

    result = progression_system.progress(game_world)

    assert result == LevelProgressionResult.NEXT_LEVEL
    assert game_world.current_level_index == 1
    assert game_world.current_level is not None
    assert game_world.current_level.number == 2


def test_progress_returns_victory_after_final_level() -> None:
    """Progression should report victory after the final level."""
    game_world = create_game_world(number_of_levels=1)
    current_level = game_world.start()
    current_level.completed = True

    progression_system = LevelProgressionSystem()

    result = progression_system.progress(game_world)

    assert result == LevelProgressionResult.VICTORY


def test_progress_rejects_world_that_has_not_started() -> None:
    """Progression should reject a world without a current level."""
    game_world = create_game_world()

    progression_system = LevelProgressionSystem()

    with pytest.raises(ValueError, match="game world is started"):
        progression_system.progress(game_world)


def test_is_level_completed_returns_correct_status() -> None:
    """is_level_completed should reflect the level completion state."""
    game_world = create_game_world()
    level = game_world.start()

    progression_system = LevelProgressionSystem()

    assert not progression_system.is_level_completed(level)

    level.completed = True

    assert progression_system.is_level_completed(level)
