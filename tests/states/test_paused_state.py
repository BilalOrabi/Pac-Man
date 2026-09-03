"""Tests for the Pac-Man paused state."""

from src.states.game_state import GameStateType
from src.states.paused_state import PausedState
from src.states.state_machine import GameStateMachine


def test_paused_state_is_active_when_game_is_paused() -> None:
    """Paused state should be active when the game is paused."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PAUSED
    )
    paused_state = PausedState(state_machine)

    assert paused_state.is_active()


def test_paused_state_is_not_active_during_gameplay() -> None:
    """Paused state should not be active during gameplay."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    paused_state = PausedState(state_machine)

    assert not paused_state.is_active()


def test_resume_game_transitions_to_playing_state() -> None:
    """Resuming should return the game to the playing state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PAUSED
    )
    paused_state = PausedState(state_machine)

    paused_state.resume_game()

    assert state_machine.current_state is GameStateType.PLAYING


def test_return_to_menu_transitions_to_menu_state() -> None:
    """Returning to menu should transition to the menu state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PAUSED
    )
    paused_state = PausedState(state_machine)

    paused_state.return_to_menu()

    assert state_machine.current_state is GameStateType.MENU
