"""Tests for the Pac-Man playing state."""

from src.states.game_state import GameStateType
from src.states.playing_state import PlayingState
from src.states.state_machine import GameStateMachine


def test_playing_state_is_active_when_game_is_playing() -> None:
    """Playing state should be active during gameplay."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    playing_state = PlayingState(state_machine)

    assert playing_state.is_active()


def test_playing_state_is_not_active_when_game_is_paused() -> None:
    """Playing state should not be active while paused."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PAUSED
    )
    playing_state = PlayingState(state_machine)

    assert not playing_state.is_active()


def test_pause_game_transitions_to_paused_state() -> None:
    """Pausing the game should transition to the paused state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    playing_state = PlayingState(state_machine)

    playing_state.pause_game()

    assert state_machine.current_state is GameStateType.PAUSED


def test_end_game_transitions_to_game_over_state() -> None:
    """Ending the game should transition to game-over."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    playing_state = PlayingState(state_machine)

    playing_state.end_game()

    assert state_machine.current_state is GameStateType.GAME_OVER


def test_complete_game_transitions_to_victory_state() -> None:
    """Completing the game should transition to victory."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )
    playing_state = PlayingState(state_machine)

    playing_state.complete_game()

    assert state_machine.current_state is GameStateType.VICTORY
