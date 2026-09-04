"""Decision-making controller for Pac-Man ghosts."""

from dataclasses import dataclass

from src.ai.chase import ChaseBehavior
from src.ai.flee import FleeBehavior
from src.ai.ghost_mode import GhostMode
from src.ai.return_home import ReturnHomeBehavior
from src.entities.direction import Direction
from src.maze.maze import Coordinate, Maze


@dataclass
class GhostAI:
    """Control ghost behavior according to its current mode."""

    current_mode: GhostMode = GhostMode.CHASE
    current_direction: Direction = Direction.NONE

    def set_mode(self, ghost_mode: GhostMode) -> None:
        """Change the ghost's current behavioral mode."""
        self.current_mode = ghost_mode

    def set_direction(self, direction: Direction) -> None:
        """Set the ghost's current movement direction."""
        self.current_direction = direction

    def get_next_direction(
        self,
        maze: Maze,
        ghost_position: Coordinate,
        target_position: Coordinate,
        home_position: Coordinate,
        current_direction: Direction = Direction.NONE,
    ) -> Direction:
        """Calculate the next direction according to the current mode."""
        cur_dir = (
            current_direction
            if current_direction is not Direction.NONE
            else self.current_direction
        )

        if self.current_mode is GhostMode.CHASE:
            return ChaseBehavior.get_direction_toward_target(
                maze=maze,
                ghost_position=ghost_position,
                target_position=target_position,
                current_direction=cur_dir,
            )

        if self.current_mode is GhostMode.FLEE:
            return FleeBehavior.get_direction_away_from_target(
                maze=maze,
                ghost_position=ghost_position,
                target_position=target_position,
                current_direction=cur_dir,
            )

        if self.current_mode is GhostMode.RETURN_HOME:
            return ReturnHomeBehavior.get_direction_toward_home(
                maze=maze,
                ghost_position=ghost_position,
                home_position=home_position,
            )

        return Direction.NONE

    def get_current_mode(self) -> GhostMode:
        """Return the ghost's current behavioral mode."""
        return self.current_mode

    def get_current_direction(self) -> Direction:
        """Return the ghost's current movement direction."""
        return self.current_direction

    def reset(self) -> None:
        """Reset the ghost AI to its initial state."""
        self.current_mode = GhostMode.CHASE
        self.current_direction = Direction.NONE
