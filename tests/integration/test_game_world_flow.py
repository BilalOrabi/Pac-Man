"""Integration tests for the GameWorld level creation flow."""

from src.application.game_coordinator import GameCoordinator

from src.config.game_config import GameConfig, LevelConfig

from src.input.input_system import InputSystem
from src.input.input_event import InputAction

from src.maze.adapter import MazeAdapter

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine

from src.world.game_world import GameWorld
from src.world.level_factory import LevelFactory


def create_game_coordinator() -> GameCoordinator:
    """Create a coordinator using the real world and level components."""
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

    game_world = GameWorld(
        game_configuration=game_configuration,
        level_factory=level_factory,
    )

    return GameCoordinator(
        game_world=game_world,
        input_system=InputSystem(),
        state_machine=GameStateMachine(),
    )


def test_start_game_creates_real_level_and_enters_playing() -> None:
    """Starting the game should create a real level and enter PLAYING."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(
    InputAction.START_GAME
)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )

    current_level = coordinator.game_world.current_level

    assert current_level is not None
    assert current_level.number == 1
    assert current_level.configuration.width == 5
    assert current_level.configuration.height == 5
    assert current_level.remaining_pacgums == 10


def test_game_world_can_advance_to_real_second_level() -> None:
    """The world should create the next configured level."""
    coordinator = create_game_coordinator()

    first_level = coordinator.game_world.start()

    assert first_level is not None
    assert first_level.number == 1

    second_level = coordinator.game_world.advance_to_next_level()

    assert second_level is not None
    assert second_level.number == 2
    assert second_level.configuration.width == 6
    assert second_level.configuration.height == 6
    assert second_level.remaining_pacgums == 10
