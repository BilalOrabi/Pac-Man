"""Tests for Pac-Man game state definitions."""

from src.states.game_state import GameStateType


def test_game_state_type_contains_all_required_states() -> None:
    """GameStateType should contain every required game state."""
    assert GameStateType.MENU.value == "menu"
    assert GameStateType.PLAYING.value == "playing"
    assert GameStateType.PAUSED.value == "paused"
    assert GameStateType.GAME_OVER.value == "game_over"
    assert GameStateType.VICTORY.value == "victory"


def test_game_state_type_values_are_unique() -> None:
    """Every game state should have a unique value."""
    state_values = [state.value for state in GameStateType]

    assert len(state_values) == len(set(state_values))


def test_game_state_type_is_an_enum() -> None:
    """Game states should be represented by Enum members."""
    assert isinstance(GameStateType.PLAYING, GameStateType)
