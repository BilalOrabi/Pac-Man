"""Tests for Pac-Man input event definitions."""

from src.input.input_event import InputAction, InputEvent


def test_input_action_contains_all_required_actions() -> None:
    """InputAction should contain all supported game actions."""
    expected_actions = {
        "move_up",
        "move_down",
        "move_left",
        "move_right",
        "pause_game",
        "start_game",
        "restart_game",
        "return_to_menu",
        "quit_game",
    }

    actual_actions = {
        action.value
        for action in InputAction
    }

    assert actual_actions == expected_actions


def test_input_action_values_are_unique() -> None:
    """Every input action should have a unique value."""
    action_values = [action.value for action in InputAction]

    assert len(action_values) == len(set(action_values))


def test_input_event_stores_input_action() -> None:
    """InputEvent should store its action as an InputAction."""
    input_event = InputEvent(
        action=InputAction.MOVE_UP
    )

    assert input_event.action is InputAction.MOVE_UP


def test_input_event_is_immutable() -> None:
    """InputEvent should be immutable."""
    input_event = InputEvent(
        action=InputAction.PAUSE_GAME
    )

    try:
        input_event.action = InputAction.START_GAME
        assert False, "InputEvent should be immutable."
    except AttributeError:
        pass
