"""Tests for the Pac-Man main game loop."""

from unittest.mock import Mock

import pytest

from src.application.game_coordinator import GameCoordinator
from src.application.main_loop import MainGameLoop
from src.input.input_event import InputAction


def create_main_game_loop() -> MainGameLoop:
    """Create a main game loop with a mocked coordinator."""
    game_coordinator = Mock(spec=GameCoordinator)

    return MainGameLoop(
        game_coordinator=game_coordinator
    )


def test_main_game_loop_starts_stopped() -> None:
    """The main loop should initially be stopped."""
    main_loop = create_main_game_loop()

    assert main_loop.is_running is False


def test_start_starts_main_game_loop() -> None:
    """Starting the loop should mark it as running."""
    main_loop = create_main_game_loop()

    main_loop.start()

    assert main_loop.is_running is True


def test_stop_stops_main_game_loop() -> None:
    """Stopping the loop should mark it as not running."""
    main_loop = create_main_game_loop()

    main_loop.start()
    main_loop.stop()

    assert main_loop.is_running is False


def test_process_action_sends_action_to_coordinator() -> None:
    """Running the loop should forward actions to the coordinator."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.process_action(InputAction.START_GAME)

    main_loop.game_coordinator.handle_action.assert_called_once_with(
        InputAction.START_GAME
    )


def test_process_action_quit_stops_loop() -> None:
    """QUIT_GAME should stop the main loop."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.process_action(InputAction.QUIT_GAME)

    assert main_loop.is_running is False
    main_loop.game_coordinator.handle_action.assert_not_called()


def test_process_action_does_nothing_when_stopped() -> None:
    """Actions should be ignored while the loop is stopped."""
    main_loop = create_main_game_loop()

    main_loop.process_action(InputAction.START_GAME)

    main_loop.game_coordinator.handle_action.assert_not_called()


def test_update_forwards_elapsed_time_to_coordinator() -> None:
    """Running the loop should update the game coordinator."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.update(0.016)

    main_loop.game_coordinator.update.assert_called_once_with(
        0.016
    )


def test_update_does_nothing_when_stopped() -> None:
    """The coordinator should not update while the loop is stopped."""
    main_loop = create_main_game_loop()

    main_loop.update(0.016)

    main_loop.game_coordinator.update.assert_not_called()


def test_update_rejects_negative_elapsed_time() -> None:
    """The main loop should reject negative elapsed time."""
    main_loop = create_main_game_loop()
    main_loop.start()

    with pytest.raises(ValueError):
        main_loop.update(-0.016)


def test_run_once_processes_action_and_updates() -> None:
    """One loop iteration should process input and update the game."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.run_once(
        elapsed_seconds=0.016,
        action=InputAction.START_GAME,
    )

    main_loop.game_coordinator.handle_action.assert_called_once_with(
        InputAction.START_GAME
    )
    main_loop.game_coordinator.update.assert_called_once_with(
        0.016
    )


def test_run_once_without_action_still_updates() -> None:
    """A loop iteration without input should still update the game."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.run_once(elapsed_seconds=0.016)

    main_loop.game_coordinator.handle_action.assert_not_called()
    main_loop.game_coordinator.update.assert_called_once_with(
        0.016
    )


def test_run_once_quit_does_not_update_after_stopping() -> None:
    """QUIT_GAME should stop the loop before the update occurs."""
    main_loop = create_main_game_loop()
    main_loop.start()

    main_loop.run_once(
        elapsed_seconds=0.016,
        action=InputAction.QUIT_GAME,
    )

    assert main_loop.is_running is False
    main_loop.game_coordinator.update.assert_not_called()


def test_process_action_rejects_invalid_action() -> None:
    """The loop should reject values that are not InputAction."""
    main_loop = create_main_game_loop()
    main_loop.start()

    with pytest.raises(TypeError):
        main_loop.process_action("START_GAME")  # type: ignore[arg-type]


def test_render_does_nothing_when_loop_is_stopped() -> None:
    """Rendering should do nothing when the loop is stopped."""
    coordinator = Mock(spec=GameCoordinator)
    main_loop = MainGameLoop(
        game_coordinator=coordinator,
    )

    main_loop.render()

    coordinator.render.assert_not_called()


def test_render_renders_when_loop_is_running() -> None:
    """Rendering should render through the game coordinator."""
    coordinator = Mock(spec=GameCoordinator)
    main_loop = MainGameLoop(
        game_coordinator=coordinator,
    )

    main_loop.start()
    main_loop.render()

    coordinator.render.assert_called_once()


def test_run_once_updates_and_renders() -> None:
    """One running loop iteration should update and render."""
    coordinator = Mock(spec=GameCoordinator)
    main_loop = MainGameLoop(
        game_coordinator=coordinator,
    )

    main_loop.start()
    main_loop.run_once(1.0)

    coordinator.update.assert_called_once_with(1.0)
    coordinator.render.assert_called_once()