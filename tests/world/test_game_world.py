"""Tests for the GameWorld."""

from src.config.game_config import GameConfig, LevelConfig
from src.maze.maze import Maze, MazeCell, Wall
from src.world.game_world import GameWorld
from src.world.level import Level
from src.world.level_factory import LevelFactory
import pytest

class FakeMazeAdapter:
    """Provide predictable maze generation for world tests."""

    def generate_level(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Return a simple predictable maze."""
        cells = tuple(
            tuple(
                MazeCell(
                    position=(x, y),
                    walls=Wall.ALL,
                    is_solid_block=True,
                )
                for x in range(width)
            )
            for y in range(height)
        )

        return Maze(
            width=width,
            height=height,
            cells=cells,
            entry=(0, 0),
            exit=(width - 1, height - 1),
            shortest_path="",
        )


def create_game_configuration() -> GameConfig:
    """Create a predictable multi-level configuration."""
    return GameConfig(
        highscore_filename="highscores.json",
        lives=3,
        pacgum=42,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=42,
        level_max_time=90,
        levels=(
            LevelConfig(width=19, height=21),
            LevelConfig(width=21, height=23),
            LevelConfig(width=25, height=27),
        ),
    )


def create_game_world() -> GameWorld:
    """Create a GameWorld with predictable dependencies."""
    maze_adapter = FakeMazeAdapter()
    level_factory = LevelFactory(maze_adapter)

    return GameWorld(
        game_configuration=create_game_configuration(),
        level_factory=level_factory,
    )


def test_world_starts_at_first_level_index() -> None:
    """World should begin with the first level index."""
    game_world = create_game_world()

    assert game_world.current_level_index == 0
    assert game_world.current_level is None


def test_start_creates_first_level() -> None:
    """Starting the world should create the first level."""
    game_world = create_game_world()

    current_level = game_world.start()

    assert isinstance(current_level, Level)
    assert current_level.number == 1
    assert game_world.current_level is current_level
    assert game_world.current_level_index == 0


def test_start_uses_first_level_configuration() -> None:
    """First level should use the first configured dimensions."""
    game_world = create_game_world()

    current_level = game_world.start()

    assert current_level.configuration.width == 19
    assert current_level.configuration.height == 21


def test_advance_to_next_level_creates_next_level() -> None:
    """World should create the next configured level."""
    game_world = create_game_world()

    game_world.start()
    next_level = game_world.advance_to_next_level()

    assert next_level is not None
    assert next_level.number == 2
    assert game_world.current_level is next_level
    assert game_world.current_level_index == 1


def test_advance_to_next_level_uses_correct_configuration() -> None:
    """Next level should use its configured dimensions."""
    game_world = create_game_world()

    game_world.start()
    next_level = game_world.advance_to_next_level()

    assert next_level is not None
    assert next_level.configuration.width == 21
    assert next_level.configuration.height == 23


def test_advance_to_last_level() -> None:
    """World should be able to advance to the final configured level."""
    game_world = create_game_world()

    game_world.start()
    game_world.advance_to_next_level()
    final_level = game_world.advance_to_next_level()

    assert final_level is not None
    assert final_level.number == 3
    assert game_world.current_level_index == 2


def test_advance_after_final_level_returns_none() -> None:
    """World should return None when no levels remain."""
    game_world = create_game_world()

    game_world.start()
    game_world.advance_to_next_level()
    game_world.advance_to_next_level()

    next_level = game_world.advance_to_next_level()

    assert next_level is None
    assert game_world.current_level is None


def test_world_is_not_complete_when_first_level_is_active() -> None:
    """World should not be complete while the first level is active."""
    game_world = create_game_world()

    game_world.start()

    assert not game_world.has_completed_all_levels()


def test_world_is_not_complete_when_middle_level_is_completed() -> None:
    """Completing a non-final level should not complete the world."""
    game_world = create_game_world()

    game_world.start()
    assert game_world.current_level is not None

    game_world.current_level.completed = True
    game_world.advance_to_next_level()

    assert not game_world.has_completed_all_levels()


def test_world_is_complete_when_final_level_is_completed() -> None:
    """World should be complete after completing its final level."""
    game_world = create_game_world()

    game_world.start()
    game_world.advance_to_next_level()
    game_world.advance_to_next_level()

    assert game_world.current_level is not None
    game_world.current_level.completed = True

    assert game_world.has_completed_all_levels()
