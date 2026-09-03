"""Tests for the Pac-Man menu state."""

from src.states.game_state import GameStateType
from src.states.menu_state import MenuState
from src.states.state_machine import GameStateMachine


def test_menu_state_is_active_when_state_machine_is_in_menu() -> None:
    """Menu state should be active while the game is in the menu."""
    state_machine = GameStateMachine(
        current_state=GameStateType.MENU
    )
    menu_state = MenuState(state_machine)

    assert menu_state.is_active()


def test_menu_state_is_not_active_when_game_is_playing() -> None:
    """Menu state should not be active during gameplay."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    menu_state = MenuState(state_machine)

    assert not menu_state.is_active()


def test_start_game_transitions_to_playing_state() -> None:
    """Starting the game should transition from menu to playing."""
    state_machine = GameStateMachine(
        current_state=GameStateType.MENU
    )
    menu_state = MenuState(state_machine)

    menu_state.start_game()

    assert state_machine.current_state is GameStateType.PLAYING
