"""Tests for the Pac-Man game coordinator."""

from unittest.mock import Mock

import pytest

from src.application.game_coordinator import GameCoordinator
from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.world.game_world import GameWorld


def create_game_coordinator() -> GameCoordinator:
    """Create a coordinator with mocked game-world dependencies."""
    game_world = Mock(spec=GameWorld)
    input_system = InputSystem()
    state_machine = GameStateMachine()

    return GameCoordinator(
        game_world=game_world,
        input_system=input_system,
        state_machine=state_machine,
    )


def test_coordinator_starts_in_menu() -> None:
    """The coordinator should initially be in the menu."""
    coordinator = create_game_coordinator()

    assert (
        coordinator.state_machine.current_state
        is GameStateType.MENU
    )


def test_start_game_starts_world_and_enters_playing_state() -> None:
    """Starting the game should start the world and enter PLAYING."""
    coordinator = create_game_coordinator()

    coordinator.start_game()

    coordinator.game_world.start.assert_called_once()
    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )


def test_start_game_action_starts_game_from_menu() -> None:
    """START_GAME should begin the game when the menu is active."""
    coordinator = create_game_coordinator()

    coordinator.handle_action(InputAction.START_GAME)

    coordinator.game_world.start.assert_called_once()
    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )


def test_pause_game_action_enters_paused_state() -> None:
    """PAUSE_GAME should move the game from PLAYING to PAUSED."""
    coordinator = create_game_coordinator()

    coordinator.start_game()
    coordinator.handle_action(InputAction.PAUSE_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PAUSED
    )


def test_pause_game_action_resumes_game() -> None:
    """PAUSE_GAME should resume the game from the paused state."""
    coordinator = create_game_coordinator()

    coordinator.start_game()
    coordinator.handle_action(InputAction.PAUSE_GAME)
    coordinator.handle_action(InputAction.PAUSE_GAME)

    assert (
        coordinator.state_machine.current_state
        is GameStateType.PLAYING
    )


def test_update_rejects_negative_elapsed_time() -> None:
    """Update should reject negative elapsed time."""
    coordinator = create_game_coordinator()

    with pytest.raises(ValueError):
        coordinator.update(-1.0)


def test_update_does_nothing_when_not_playing() -> None:
    """Update should not update the world outside PLAYING."""
    coordinator = create_game_coordinator()

    coordinator.update(1.0)

    coordinator.game_world.start.assert_not_called()


def test_handle_action_rejects_invalid_action() -> None:
    """The coordinator should reject values that are not InputAction."""
    coordinator = create_game_coordinator()

    with pytest.raises(TypeError):
        coordinator.handle_action("START_GAME")  # type: ignore[arg-type]
