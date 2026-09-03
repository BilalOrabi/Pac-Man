"""Manage the current input state of the Pac-Man game."""

from src.entities.direction import Direction
from src.input.input_event import InputAction, InputEvent
from src.input.input_state import InputState
from src.input.input_mapper import InputMapper


class InputManager:
    """Process input events and maintain the current input state."""

    def __init__(self) -> None:
        """Initialize the input manager with an empty input state."""
        self.input_state = InputState()

    def process_event(self, input_event: InputEvent) -> None:
        """Process an input event and update the input state.

        Args:
            input_event: Event produced by the input handler.
        """
        movement_direction = InputMapper.get_direction(
            input_event.action
        )

        if movement_direction is not None:
            self.input_state.set_direction(movement_direction)
            return

        if input_event.action is InputAction.RESTART_GAME:
            self.input_state.clear_direction()

    def get_requested_direction(self) -> Direction:
        """Return the direction currently requested by the player."""
        return self.input_state.requested_direction

    def clear_direction(self) -> None:
        """Clear the current movement request."""
        self.input_state.clear_direction()
