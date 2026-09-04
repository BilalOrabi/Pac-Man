"""Tests for the Pac-Man enter-name state."""

import pytest

from src.states.enter_name_state import EnterNameState
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine


def create_enter_name_state() -> EnterNameState:
    """Create an enter-name state for testing."""
    state_machine = GameStateMachine(
        current_state=GameStateType.ENTER_NAME
    )

    return EnterNameState(
        state_machine=state_machine
    )


def test_enter_name_state_starts_with_empty_name() -> None:
    """The player's name should initially be empty."""
    state = create_enter_name_state()

    assert state.player_name == ""


def test_enter_name_state_can_add_characters() -> None:
    """Characters should be appended to the player's name."""
    state = create_enter_name_state()

    state.add_character("H")
    state.add_character("a")
    state.add_character("m")
    state.add_character("z")
    state.add_character("a")

    assert state.player_name == "Hamza"


def test_enter_name_state_can_remove_character() -> None:
    """The last character should be removed from the name."""
    state = create_enter_name_state()

    state.add_character("H")
    state.add_character("a")
    state.add_character("m")

    state.remove_character()

    assert state.player_name == "Ha"


def test_enter_name_state_remove_from_empty_name() -> None:
    """Removing from an empty name should remain safe."""
    state = create_enter_name_state()

    state.remove_character()

    assert state.player_name == ""


def test_enter_name_state_confirms_name() -> None:
    """Confirming the name should return the entered name."""
    state = create_enter_name_state()

    state.add_character("H")
    state.add_character("a")
    state.add_character("m")
    state.add_character("z")
    state.add_character("a")

    assert state.confirm_name() == "Hamza"


def test_enter_name_state_respects_maximum_name_length() -> None:
    """The name should not exceed the configured maximum length."""
    state = EnterNameState(
        state_machine=GameStateMachine(
            current_state=GameStateType.ENTER_NAME
        ),
        maximum_name_length=3,
    )

    state.add_character("A")
    state.add_character("B")
    state.add_character("C")
    state.add_character("D")

    assert state.player_name == "ABC"


def test_enter_name_state_rejects_multiple_characters() -> None:
    """Adding more than one character at a time should fail."""
    state = create_enter_name_state()

    with pytest.raises(ValueError):
        state.add_character("AB")


def test_enter_name_state_rejects_non_string_character() -> None:
    """Adding a non-string character should fail."""
    state = create_enter_name_state()

    with pytest.raises(TypeError):
        state.add_character(1)  # type: ignore[arg-type]


def test_enter_name_state_reports_active_state() -> None:
    """The state should report whether it is currently active."""
    state = create_enter_name_state()

    assert state.is_active() is True

    state.state_machine.transition_to(GameStateType.MENU)

    assert state.is_active() is False


def test_enter_name_state_can_reset_name() -> None:
    """Reset should clear the player's entered name."""
    state = create_enter_name_state()

    state.add_character("H")
    state.add_character("a")
    state.add_character("m")

    state.reset()

    assert state.player_name == ""
