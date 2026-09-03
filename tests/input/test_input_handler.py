"""Tests for the Pac-Man input handler."""

import pygame

from src.input.input_event import InputAction
from src.input.input_handler import InputHandler


def create_keydown_event(key_code: int) -> pygame.event.Event:
    """Create a pygame keyboard event for testing."""
    return pygame.event.Event(
        pygame.KEYDOWN,
        {"key": key_code},
    )


def test_arrow_up_maps_to_move_up() -> None:
    """Up arrow should generate a MOVE_UP action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_UP)
    )

    assert input_event is not None
    assert input_event.action is InputAction.MOVE_UP


def test_w_key_maps_to_move_up() -> None:
    """W should generate a MOVE_UP action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_w)
    )

    assert input_event is not None
    assert input_event.action is InputAction.MOVE_UP


def test_arrow_down_maps_to_move_down() -> None:
    """Down arrow should generate a MOVE_DOWN action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_DOWN)
    )

    assert input_event is not None
    assert input_event.action is InputAction.MOVE_DOWN


def test_arrow_left_maps_to_move_left() -> None:
    """Left arrow should generate a MOVE_LEFT action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_LEFT)
    )

    assert input_event is not None
    assert input_event.action is InputAction.MOVE_LEFT


def test_arrow_right_maps_to_move_right() -> None:
    """Right arrow should generate a MOVE_RIGHT action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_RIGHT)
    )

    assert input_event is not None
    assert input_event.action is InputAction.MOVE_RIGHT


def test_escape_maps_to_pause() -> None:
    """Escape should generate a PAUSE_GAME action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_ESCAPE)
    )

    assert input_event is not None
    assert input_event.action is InputAction.PAUSE_GAME


def test_enter_maps_to_start_game() -> None:
    """Enter should generate a START_GAME action."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_RETURN)
    )

    assert input_event is not None
    assert input_event.action is InputAction.START_GAME


def test_quit_event_maps_to_quit_game() -> None:
    """A pygame QUIT event should generate QUIT_GAME."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        pygame.event.Event(pygame.QUIT)
    )

    assert input_event is not None
    assert input_event.action is InputAction.QUIT_GAME


def test_unrecognized_key_returns_none() -> None:
    """Unsupported keyboard keys should be ignored."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        create_keydown_event(pygame.K_F1)
    )

    assert input_event is None


def test_unrelated_pygame_event_returns_none() -> None:
    """Non-input pygame events should be ignored."""
    input_handler = InputHandler()

    input_event = input_handler.process_event(
        pygame.event.Event(pygame.MOUSEMOTION)
    )

    assert input_event is None
