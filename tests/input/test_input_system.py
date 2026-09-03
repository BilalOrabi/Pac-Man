"""Tests for the Pac-Man input system."""

from unittest.mock import patch

import pygame

from src.entities.direction import Direction
from src.input.input_manager import InputManager
from src.input.input_system import InputSystem


def create_keydown_event(key_code: int) -> pygame.event.Event:
    """Create a keyboard event for testing."""
    return pygame.event.Event(
        pygame.KEYDOWN,
        {"key": key_code},
    )


def test_process_events_updates_input_manager() -> None:
    """Keyboard events should update the input manager."""
    input_manager = InputManager()
    input_system = InputSystem(
        input_manager=input_manager
    )

    pygame_events = [
        create_keydown_event(pygame.K_UP),
    ]

    with patch(
        "src.input.input_system.pygame.event.get",
        return_value=pygame_events,
    ):
        input_system.process_events()

    assert (
        input_manager.get_requested_direction()
        is Direction.UP
    )


def test_process_events_handles_multiple_events() -> None:
    """The input system should process all queued events."""
    input_manager = InputManager()
    input_system = InputSystem(
        input_manager=input_manager
    )

    pygame_events = [
        create_keydown_event(pygame.K_LEFT),
        create_keydown_event(pygame.K_RIGHT),
    ]

    with patch(
        "src.input.input_system.pygame.event.get",
        return_value=pygame_events,
    ):
        input_system.process_events()

    assert (
        input_manager.get_requested_direction()
        is Direction.RIGHT
    )


def test_process_events_ignores_unrecognized_events() -> None:
    """Unsupported events should not modify the input state."""
    input_manager = InputManager()
    input_system = InputSystem(
        input_manager=input_manager
    )

    pygame_events = [
        pygame.event.Event(pygame.MOUSEMOTION),
    ]

    with patch(
        "src.input.input_system.pygame.event.get",
        return_value=pygame_events,
    ):
        input_system.process_events()

    assert (
        input_manager.get_requested_direction()
        is Direction.NONE
    )


def test_process_events_can_process_quit_event() -> None:
    """Quit events should be passed through the input pipeline."""
    input_system = InputSystem()

    with patch(
        "src.input.input_system.pygame.event.get",
        return_value=[
            pygame.event.Event(pygame.QUIT),
        ],
    ):
        input_system.process_events()
