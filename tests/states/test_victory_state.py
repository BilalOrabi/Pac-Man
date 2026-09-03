"""Tests for the Pac-Man victory state."""

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.states.victory_state import VictoryState


def test_victory_state_is_active_when_game_is_completed() -> None:
    """Victory state should be active after completing the game."""
    state_machine = GameStateMachine(
        current_state=GameStateType.VICTORY
    )
    victory_state = VictoryState(state_machine)

    assert victory_state.is_active()


def test_victory_state_is_not_active_during_gameplay() -> None:
    """Victory state should not be active during gameplay."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    victory_state = VictoryState(state_machine)

    assert not victory_state.is_active()


def test_return_to_menu_transitions_to_menu_state() -> None:
    """Returning to menu should transition to the menu state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.VICTORY
    )
    victory_state = VictoryState(state_machine)

    victory_state.return_to_menu()

    assert state_machine.current_state is GameStateType.MENU


def test_start_new_game_transitions_to_playing_state() -> None:
    """Starting a new game should transition to playing."""
    state_machine = GameStateMachine(
        current_state=GameStateType.VICTORY
    )
    victory_state = VictoryState(state_machine)

    victory_state.start_new_game()

    assert state_machine.current_state is GameStateType.PLAYING
