"""Map game input actions to entity movement directions."""

from src.entities.direction import Direction
from src.input.input_event import InputAction


class InputMapper:
    """Convert movement input actions into movement directions."""

    @staticmethod
    def get_direction(input_action: InputAction) -> Direction | None:
        """Return the movement direction represented by an input action.

        Args:
            input_action: Action received from the input handler.

        Returns:
            The corresponding Direction for movement actions,
            or None for non-movement actions.
        """
        input_direction_mapping = {
            InputAction.MOVE_UP: Direction.UP,
            InputAction.MOVE_DOWN: Direction.DOWN,
            InputAction.MOVE_LEFT: Direction.LEFT,
            InputAction.MOVE_RIGHT: Direction.RIGHT,
        }

        return input_direction_mapping.get(input_action)
