"""Tests for the Pac-Man game-over state."""

from src.states.game_over_state import GameOverState
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


def test_game_over_state_is_active_when_game_is_over() -> None:
    """Game-over state should be active when the game has ended."""
    state_machine = GameStateMachine(
        current_state=GameStateType.GAME_OVER
    )
    game_over_state = GameOverState(state_machine)

    assert game_over_state.is_active()


def test_game_over_state_is_not_active_during_gameplay() -> None:
    """Game-over state should not be active during gameplay."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    game_over_state = GameOverState(state_machine)

    assert not game_over_state.is_active()


def test_restart_game_transitions_to_playing_state() -> None:
    """Restarting should transition back to the playing state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.GAME_OVER
    )
    game_over_state = GameOverState(state_machine)

    game_over_state.restart_game()

    assert state_machine.current_state is GameStateType.PLAYING


def test_return_to_menu_transitions_to_menu_state() -> None:
    """Returning to menu should transition to the menu state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.GAME_OVER
    )
    game_over_state = GameOverState(state_machine)

    game_over_state.return_to_menu()

    assert state_machine.current_state is GameStateType.MENU
