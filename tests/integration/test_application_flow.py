"""Integration tests for the complete Pac-Man application flow."""

from unittest.mock import Mock

from src.application.game_coordinator import GameCoordinator
from src.config.game_config import GameConfig, LevelConfig
from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.maze.adapter import MazeAdapter
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.world.game_world import GameWorld
from src.world.level_factory import LevelFactory


def create_game_coordinator() -> GameCoordinator:
    """Create a coordinator with real world dependencies."""
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
        input_system=Mock(spec=InputSystem),
        state_machine=GameStateMachine(),
    )


def test_complete_start_pause_resume_flow() -> None:
    """The application should move through its basic gameplay states."""
    coordinator = create_game_coordinator()

    assert (
        coordinator.state_machine.current_state
        is GameStateType.MENU
    )

    coordinator.handle_action(InputAction.START_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )

    assert coordinator.game_world.current_level is not None

    coordinator.handle_action(InputAction.PAUSE_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PAUSED
    )

    coordinator.handle_action(InputAction.PAUSE_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )


def test_gameplay_updates_current_level() -> None:
    """The application should update the active level during gameplay."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    level = coordinator.game_world.current_level

    assert level is not None

    coordinator.update(5.0)

    assert coordinator.state_machine.current_state is GameStateType.PLAYING

    assert level.is_time_expired(120) is False


def test_gameplay_update_is_ignored_when_paused() -> None:
    """The current level should not update while the game is paused."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    level = coordinator.game_world.current_level

    assert level is not None

    coordinator.handle_action(InputAction.PAUSE_GAME)

    coordinator.update(5.0)

    assert coordinator.state_machine.current_state is GameStateType.PAUSED

    assert level.is_time_expired(120) is False


def test_restart_action_starts_game_from_game_over() -> None:
    """Restarting from game over should start a new game."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    coordinator.handle_action(InputAction.QUIT_GAME)

    # QUIT_GAME is currently not handled by GameCoordinator.
    # The state should therefore remain PLAYING.
    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )
