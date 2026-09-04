"""Integration tests for the Pac-Man application flow."""

from unittest.mock import Mock

import pytest

from src.application.game_coordinator import GameCoordinator
from src.config.game_config import GameConfig
from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.rendering.game_renderer import GameRenderer
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.world.game_world import GameWorld
from src.world.level_factory import LevelFactory


def create_game_coordinator() -> GameCoordinator:
    """Create a coordinator with its application dependencies."""
    game_configuration = Mock(spec=GameConfig)
    game_configuration.levels = [Mock()]
    game_configuration.seed = 100
    game_configuration.pacgum = 20

    level_factory = Mock(spec=LevelFactory)

    level = Mock()
    level.completed = False

    level_factory.create_level.return_value = level

    game_world = GameWorld(
        game_configuration=game_configuration,
        level_factory=level_factory,
    )

    game_renderer = Mock(spec=GameRenderer)
    game_renderer.is_initialized = False

    return GameCoordinator(
        game_world=game_world,
        input_system=Mock(spec=InputSystem),
        state_machine=GameStateMachine(),
        game_renderer=game_renderer,
    )


def test_start_game_connects_menu_to_playing_and_world() -> None:
    """Starting the game should initialize the world and enter PLAYING."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )

    assert coordinator.game_world.current_level is not None
    assert coordinator.game_world.start_called is True


def test_pause_and_resume_flow() -> None:
    """The game should move between PLAYING and PAUSED."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )

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


def test_update_only_updates_world_while_playing() -> None:
    """World updates should happen only during active gameplay."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    level = coordinator.game_world.current_level

    assert level is not None

    coordinator.update(1.5)

    level.update_time.assert_called_once_with(1.5)


def test_update_does_not_update_world_while_in_menu() -> None:
    """The world should not update while the game is in the menu."""
    coordinator = create_game_coordinator()

    coordinator.update(1.5)

    assert coordinator.game_world.current_level is None


def test_negative_elapsed_time_is_rejected() -> None:
    """Negative elapsed time should be rejected."""
    coordinator = create_game_coordinator()

    with pytest.raises(ValueError):
        coordinator.update(-1.0)


def test_render_initializes_renderer_when_needed() -> None:
    """Rendering should initialize an uninitialized renderer."""
    coordinator = create_game_coordinator()

    coordinator.render()

    coordinator.game_renderer.initialize.assert_called_once()
    coordinator.game_renderer.render.assert_called_once()


def test_render_does_not_reinitialize_renderer() -> None:
    """Rendering should not initialize an already initialized renderer."""
    coordinator = create_game_coordinator()

    coordinator.game_renderer.is_initialized = True

    coordinator.render()

    coordinator.game_renderer.initialize.assert_not_called()
    coordinator.game_renderer.render.assert_called_once()


def test_shutdown_shuts_down_initialized_renderer() -> None:
    """Shutdown should shut down an initialized renderer."""
    coordinator = create_game_coordinator()

    coordinator.game_renderer.is_initialized = True

    coordinator.shutdown()

    coordinator.game_renderer.shutdown.assert_called_once()


def test_shutdown_does_not_shutdown_uninitialized_renderer() -> None:
    """Shutdown should ignore an uninitialized renderer."""
    coordinator = create_game_coordinator()

    coordinator.shutdown()

    coordinator.game_renderer.shutdown.assert_not_called()
