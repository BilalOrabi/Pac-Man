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
    buffered_direction: Direction | None = None

    CORNERING_TOLERANCE: float = 0.35

    def handle_action(
        self, action: InputAction, maze: Maze | None = None
    ) -> None:
        """Update the player's direction from a movement action."""
        direction = self._get_direction_for_action(action)
        if direction is None:
            return

        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if (
            self.player.direction is not Direction.NONE
            and opposites.get(self.player.direction) == direction
        ):
            if (
                self.player.target_position is not None
                and self.player.target_position != self.player.position
                and self.player.movement_progress > 0.0
            ):
                old_pos = self.player.position
                self.player.position = self.player.target_position
                self.player.target_position = old_pos
                self.player.movement_progress = max(
                    0.0, min(1.0, 1.0 - self.player.movement_progress)
                )
            else:
                self.player.target_position = None
                self.player.movement_progress = 0.0
            self.player.direction = direction
            self.buffered_direction = None
            return

        if self.player.direction is Direction.NONE:
            self.player.direction = direction
            self.buffered_direction = None
        else:
            self.buffered_direction = direction

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

        if self.buffered_direction is not None:
            if self._can_move_in_direction(self.buffered_direction, maze):
                self.player.direction = self.buffered_direction
                self.buffered_direction = None

        self.player.target_position = None
        self.player.movement_progress = 0.0

    def _can_move_in_direction(
        self,
        direction: Direction,
        maze: Maze,
        from_position: tuple[int, int] | None = None,
    ) -> bool:
        """Check whether the player can move in the given direction."""
        if direction is Direction.NONE:
            return False

        offsets = {
            Direction.UP: (0, -1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
        }
        offset = offsets.get(direction, (0, 0))
        origin = (
            from_position
            if from_position is not None
            else self.player.position
        )
        target_pos = (
            origin[0] + offset[0],
            origin[1] + offset[1],
        )
        return self.collision_system.can_move_to(
            self.player,
            target_pos,
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
