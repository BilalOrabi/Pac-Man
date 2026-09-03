"""Translate raw keyboard input into typed Pac-Man input events."""

from dataclasses import dataclass

import pygame

from src.input.input_event import InputAction, InputEvent


@dataclass
class InputHandler:
    """Convert pygame keyboard events into game input events."""

    def process_event(
            self, pygame_event: pygame.event.Event) -> InputEvent | None:
        """Convert one pygame event into a typed input event.

        Args:
            pygame_event: Raw event received from pygame.

        Returns:
            The corresponding InputEvent, or None if the event is irrelevant.
        """
        if pygame_event.type == pygame.KEYDOWN:
            return self._process_keydown_event(pygame_event)

        if pygame_event.type == pygame.QUIT:
            return InputEvent(action=InputAction.QUIT_GAME)

        return None

    def _process_keydown_event(
        self,
        pygame_event: pygame.event.Event,
    ) -> InputEvent | None:
        """Convert a keyboard press into a game input event."""
        keyboard_action = self._get_keyboard_action(pygame_event.key)

        if keyboard_action is None:
            return None

        return InputEvent(action=keyboard_action)

    @staticmethod
    def _get_keyboard_action(key_code: int) -> InputAction | None:
        """Map a pygame keyboard key to a game action."""
        keyboard_action_mapping = {
            pygame.K_UP: InputAction.MOVE_UP,
            pygame.K_w: InputAction.MOVE_UP,
            pygame.K_DOWN: InputAction.MOVE_DOWN,
            pygame.K_s: InputAction.MOVE_DOWN,
            pygame.K_LEFT: InputAction.MOVE_LEFT,
            pygame.K_a: InputAction.MOVE_LEFT,
            pygame.K_RIGHT: InputAction.MOVE_RIGHT,
            pygame.K_d: InputAction.MOVE_RIGHT,
            pygame.K_ESCAPE: InputAction.PAUSE_GAME,
            pygame.K_p: InputAction.PAUSE_GAME,
            pygame.K_RETURN: InputAction.START_GAME,
            pygame.K_SPACE: InputAction.START_GAME,
            pygame.K_r: InputAction.RESTART_GAME,
            pygame.K_m: InputAction.RETURN_TO_MENU,
        }

        return keyboard_action_mapping.get(key_code)
