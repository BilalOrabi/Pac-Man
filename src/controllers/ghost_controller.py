"""Controller responsible for Pac-Man ghost movement."""

from dataclasses import dataclass

from src.entities.ghost import Ghost
from src.maze.maze import Maze
from src.systems.collision import CollisionSystem
from src.systems.movement import MovementSystem


@dataclass
class GhostController:
    """Handle movement of one Pac-Man ghost."""

    ghost: Ghost
    collision_system: CollisionSystem

    def update(self, maze: Maze) -> None:
        """Move the ghost according to its current direction."""
        target_position = MovementSystem.calculate_next_position(
            self.ghost,
            maze,
        )

        self.collision_system.move_if_valid(
            self.ghost,
            target_position,
            maze,
        )
