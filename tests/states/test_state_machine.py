"""Tests for the Pac-Man game state machine."""

import pytest

from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


def test_state_machine_starts_in_menu_state() -> None:
    """State machine should start in the menu state."""
    state_machine = GameStateMachine()

    assert state_machine.current_state is GameStateType.MENU


def test_state_machine_can_transition_to_playing_state() -> None:
    """State machine should transition to the playing state."""
    state_machine = GameStateMachine()

    state_machine.transition_to(GameStateType.PLAYING)

    assert state_machine.current_state is GameStateType.PLAYING


def test_state_machine_can_transition_between_all_states() -> None:
    """State machine should support every defined game state."""
    state_machine = GameStateMachine()

    for game_state in GameStateType:
        state_machine.transition_to(game_state)

        assert state_machine.current_state is game_state


def test_is_in_state_returns_true_for_current_state() -> None:
    """is_in_state should identify the current state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PAUSED
    )

    assert state_machine.is_in_state(GameStateType.PAUSED)


def test_is_in_state_returns_false_for_different_state() -> None:
    """is_in_state should reject a different state."""
    state_machine = GameStateMachine(
        current_state=GameStateType.PLAYING
    )

    assert not state_machine.is_in_state(GameStateType.PAUSED)


def test_transition_rejects_invalid_state() -> None:
    """transition_to should require a GameStateType."""
    state_machine = GameStateMachine()

    with pytest.raises(TypeError, match="GameStateType"):
        state_machine.transition_to("playing")  # type: ignore[arg-type]


def test_is_in_state_rejects_invalid_state() -> None:
    """is_in_state should require a GameStateType."""
    state_machine = GameStateMachine()

    with pytest.raises(TypeError, match="GameStateType"):
        state_machine.is_in_state("menu")  # type: ignore[arg-type]
