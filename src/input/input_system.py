"""Coordinate Pygame input processing for the Pac-Man game."""

import pygame

from src.input.input_handler import InputHandler
from src.input.input_manager import InputManager


class InputSystem:
    """Process Pygame events and update the game input state."""

    def __init__(
        self,
        input_handler: InputHandler | None = None,
        input_manager: InputManager | None = None,
    ) -> None:
        """Initialize the input system."""
        self.input_handler = input_handler or InputHandler()
        self.input_manager = input_manager or InputManager()

    def process_events(self) -> None:
        """Process all currently queued Pygame events."""
        for pygame_event in pygame.event.get():
            input_event = self.input_handler.process_event(
                pygame_event
            )

            if input_event is not None:
                self.input_manager.process_event(input_event)
