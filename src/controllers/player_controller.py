"""Controller responsible for Pac-Man player movement."""

from dataclasses import dataclass

from src.entities.direction import Direction
from src.entities.player import Player
from src.input.input_event import InputAction
from src.maze.maze import Maze
from src.systems.collision import CollisionSystem
from src.systems.movement import MovementSystem


@dataclass
class PlayerController:
    """Handle player input and movement."""

    player: Player
    collision_system: CollisionSystem

    def handle_action(self, action: InputAction) -> None:
        """Update the player's direction from a movement action."""
        direction = self._get_direction_for_action(action)

        if direction is not None:
            self.player.direction = direction

    def update(self, maze: Maze) -> None:
        """Calculate and apply the player's next valid position."""
        target_position = MovementSystem.calculate_next_position(
            self.player,
            maze,
        )

        self.collision_system.move_if_valid(
            self.player,
            target_position,
            maze,
        )

    @staticmethod
    def _get_direction_for_action(
        action: InputAction,
    ) -> Direction | None:
        """Convert an input action into a movement direction."""
        direction_by_action: dict[InputAction, Direction] = {
            InputAction.MOVE_UP: Direction.UP,
            InputAction.MOVE_RIGHT: Direction.RIGHT,
            InputAction.MOVE_DOWN: Direction.DOWN,
            InputAction.MOVE_LEFT: Direction.LEFT,
        }

        return direction_by_action.get(action)
