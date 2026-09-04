"""Integration tests for Pac-Man gameplay systems."""

from src.config.game_config import LevelConfig
from src.entities.direction import Direction
from src.entities.entity import Entity
from src.systems.collision import CollisionSystem
from src.systems.level_progression import (
    LevelProgressionResult,
    LevelProgressionSystem,
)
from src.systems.lives import LivesSystem
from src.systems.movement import MovementSystem
from src.systems.power_mode import (
    PowerModeState,
    PowerModeSystem,
)
from src.systems.scoring import ScoringSystem
from src.systems.timer_system import TimerSystem
from src.world.game_world import GameWorld
from src.world.level import Level
from src.world.level_factory import LevelFactory
from src.config.game_config import GameConfig
from src.maze.adapter import MazeAdapter


def create_game_world() -> GameWorld:
    """Create a real game world for integration testing."""
    game_configuration = GameConfig(
        highscore_filename="highscores.txt",
        lives=3,
        pacgum=10,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=100,
        level_max_time=120,
        levels=(
            LevelConfig(width=5, height=5),
            LevelConfig(width=6, height=6),
        ),
    )

    maze_adapter = MazeAdapter()
    level_factory = LevelFactory(
        maze_adapter=maze_adapter,
    )

    return GameWorld(
        game_configuration=game_configuration,
        level_factory=level_factory,
    )


def test_movement_and_collision_work_together() -> None:
    """An entity should move only when its calculated position is walkable."""
    game_world = create_game_world()

    level = game_world.start()

    assert level is not None

    entity = Entity(
        position=(0, 0),
        direction=Direction.RIGHT,
    )

    next_position = MovementSystem.calculate_next_position(
        entity=entity,
        maze=level.maze,
    )

    moved = CollisionSystem.move_if_valid(
        entity=entity,
        target_position=next_position,
        maze=level.maze,
    )

    assert moved is True
    assert entity.position == next_position


def test_collision_prevents_entity_from_entering_solid_cell() -> None:
    """Collision should prevent an entity from entering an invalid cell."""
    game_world = create_game_world()

    level = game_world.start()

    assert level is not None

    entity = Entity(
        position=(0, 0),
        direction=Direction.RIGHT,
    )

    original_position = entity.position

    invalid_position = (
        level.maze.width + 1,
        level.maze.height + 1,
    )

    moved = CollisionSystem.move_if_valid(
        entity=entity,
        target_position=invalid_position,
        maze=level.maze,
    )

    assert moved is False
    assert entity.position == original_position


def test_power_mode_activation_and_expiration() -> None:
    """Power mode should activate and expire after its duration."""
    power_mode = PowerModeSystem(duration=5.0)

    power_mode.activate()

    assert power_mode.state is PowerModeState.ACTIVE
    assert power_mode.is_active is True
    assert power_mode.remaining_time == 5.0

    power_mode.update(5.0)

    assert power_mode.state is PowerModeState.INACTIVE
    assert power_mode.is_active is False
    assert power_mode.remaining_time == 0.0


def test_lives_and_scoring_work_independently_during_gameplay() -> None:
    """Lives and scoring systems should apply their configured rules."""
    game_world = create_game_world()

    level = game_world.start()

    assert level is not None

    lives_system = LivesSystem(
        starting_lives=game_world.game_configuration.lives
    )

    scoring_system = ScoringSystem(
        points_per_pacgum=game_world.game_configuration.points_per_pacgum,
        points_per_super_pacgum=(
            game_world.game_configuration.points_per_super_pacgum
        ),
        points_per_ghost=game_world.game_configuration.points_per_ghost,
    )

    assert lives_system.remaining_lives == 3

    assert scoring_system.calculate_pacgum_score() == 10
    assert scoring_system.calculate_super_pacgum_score() == 50
    assert scoring_system.calculate_ghost_score() == 200

    assert lives_system.lose_life() is True
    assert lives_system.remaining_lives == 2


def test_timer_updates_level_and_detects_expiration() -> None:
    """The timer should update the level and detect when time expires."""
    game_world = create_game_world()

    level = game_world.start()

    assert level is not None

    timer_system = TimerSystem(
        maximum_level_time=120,
    )

    timer_system.update(
        level=level,
        elapsed_time=10.0,
    )

    assert level.elapsed_level_time == 10.0
    assert timer_system.is_expired(level) is False


def test_completed_level_progresses_to_next_level() -> None:
    """A completed level should cause the world to create the next level."""
    game_world = create_game_world()

    first_level = game_world.start()

    assert first_level is not None

    first_level.completed = True

    progression_system = LevelProgressionSystem()

    result = progression_system.progress(game_world)

    assert result is LevelProgressionResult.NEXT_LEVEL

    assert game_world.current_level is not None
    assert game_world.current_level.number == 2
