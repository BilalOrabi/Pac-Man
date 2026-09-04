"""Tests for the LevelFactory."""

from src.config.game_config import GameConfig, LevelConfig
from src.entities.ghost import GhostType
from src.maze.maze import Maze, MazeCell, Wall
from src.world.level import Level
from src.world.level_factory import LevelFactory
import pytest


class FakeMazeAdapter:
    """Provide predictable maze generation for factory tests."""

    def __init__(self) -> None:
        """Initialize the fake adapter."""
        self.received_width: int | None = None
        self.received_height: int | None = None
        self.received_seed: int | None = None

    def generate_level(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Return a predictable maze and record the arguments."""
        self.received_width = width
        self.received_height = height
        self.received_seed = seed

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
    """Create a valid game configuration for level factory tests."""
    return GameConfig(
        highscore_filename="highscores.txt",
        lives=3,
        pacgum=10,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=100,
        level_max_time=120,
        player_speed=5.0,
        ghost_speed=4.0,
        frightened_ghost_speed=2.0,
        returning_ghost_speed=6.0,
        power_mode_duration=7.0,
        levels=(LevelConfig(width=19, height=21),),
    )


def create_level_factory() -> tuple[LevelFactory, FakeMazeAdapter]:
    """Create a LevelFactory with a controllable maze adapter."""
    fake_maze_adapter = FakeMazeAdapter()

    return (
        LevelFactory(
            fake_maze_adapter,
            game_configuration=create_game_configuration(),
        ),
        fake_maze_adapter,
    )


def test_create_level_returns_level() -> None:
    """Factory should create a Level instance."""
    level_factory, _ = create_level_factory()

    level = level_factory.create_level(
        level_number=1,
        level_configuration=LevelConfig(width=19, height=21),
        maze_seed=42,
        pacgum_count=42,
    )

    assert isinstance(level, Level)


def test_create_level_assigns_level_number() -> None:
    """Factory should assign the requested level number."""
    level_factory, _ = create_level_factory()

    level = level_factory.create_level(
        level_number=3,
        level_configuration=LevelConfig(width=19, height=21),
        maze_seed=42,
        pacgum_count=42,
    )

    assert level.number == 3


def test_create_level_preserves_configuration() -> None:
    """Factory should preserve the supplied level configuration."""
    level_factory, _ = create_level_factory()

    level_configuration = LevelConfig(
        width=19,
        height=21,
    )

    level = level_factory.create_level(
        level_number=1,
        level_configuration=level_configuration,
        maze_seed=42,
        pacgum_count=42,
    )

    assert level.configuration == level_configuration


def test_create_level_assigns_pacgum_count() -> None:
    """Factory should assign the configured pacgum count."""
    level_factory, _ = create_level_factory()

    level = level_factory.create_level(
        level_number=1,
        level_configuration=LevelConfig(width=19, height=21),
        maze_seed=42,
        pacgum_count=100,
    )

    assert level.remaining_pacgums == 100


def test_create_level_passes_configuration_to_maze_adapter() -> None:
    """Factory should pass dimensions and seed to the maze adapter."""
    level_factory, fake_maze_adapter = create_level_factory()

    level_factory.create_level(
        level_number=1,
        level_configuration=LevelConfig(width=19, height=21),
        maze_seed=123,
        pacgum_count=42,
    )

    assert fake_maze_adapter.received_width == 19
    assert fake_maze_adapter.received_height == 21
    assert fake_maze_adapter.received_seed == 123


def test_create_level_rejects_invalid_level_number() -> None:
    """Factory should reject non-positive level numbers."""
    level_factory, _ = create_level_factory()

    with pytest.raises(ValueError):
        level_factory.create_level(
            level_number=0,
            level_configuration=LevelConfig(width=19, height=21),
            maze_seed=42,
            pacgum_count=42,
        )


def test_create_level_rejects_negative_pacgum_count() -> None:
    """Factory should reject negative pacgum counts."""
    level_factory, _ = create_level_factory()

    with pytest.raises(ValueError):
        level_factory.create_level(
            level_number=1,
            level_configuration=LevelConfig(width=19, height=21),
            maze_seed=42,
            pacgum_count=-1,
        )


def create_level() -> Level:
    """Create a ready-to-use level for factory assertions."""
    level_factory, _ = create_level_factory()

    return level_factory.create_level(
        level_number=1,
        level_configuration=LevelConfig(width=19, height=21),
        maze_seed=42,
        pacgum_count=42,
    )


def test_factory_creates_player_at_maze_entry() -> None:
    """The player should start at the maze entry."""
    level = create_level()

    assert level.player.position == level.maze.entry


def test_factory_creates_four_ghosts() -> None:
    """A level should contain the four standard ghosts."""
    level = create_level()

    assert len(level.ghosts) == 4


def test_factory_creates_all_ghost_types() -> None:
    """The level should contain one ghost of each standard type."""
    level = create_level()

    ghost_types = {
        ghost.ghost_type
        for ghost in level.ghosts
    }

    assert ghost_types == {
        GhostType.RED,
        GhostType.PINK,
        GhostType.BLUE,
        GhostType.ORANGE,
    }


def test_factory_applies_player_speed() -> None:
    """Configured player speed should be applied."""
    level = create_level()

    assert level.player.speed == 5.0


def test_factory_applies_ghost_speed() -> None:
    """Configured ghost speed should be applied."""
    level = create_level()

    assert all(
        ghost.speed == 4.0
        for ghost in level.ghosts
    )
