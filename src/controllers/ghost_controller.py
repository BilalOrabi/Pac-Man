"""Controller responsible for Pac-Man ghost movement."""

from dataclasses import dataclass

from src.ai.ghost_ai import GhostAI
from src.ai.ghost_mode import GhostMode
from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostState
from src.maze.maze import Coordinate, Maze
from src.systems.collision import CollisionSystem
from src.systems.movement import MovementSystem


@dataclass
class GhostController:
    """Handle movement and decision-making for one Pac-Man ghost."""

    ghost: Ghost
    collision_system: CollisionSystem
    ai: GhostAI | None = None

    def prepare_next_step(
        self,
        maze: Maze,
        target_position: Coordinate | None = None,
    ) -> None:
        """Evaluate AI and prepare target_position for the upcoming step."""
        cd = getattr(self.ghost, "respawn_cooldown", 0.0)
        if isinstance(cd, (int, float)) and cd > 0.0:
            self.ghost.target_position = None
            self.ghost.direction = Direction.NONE
            self.ghost.movement_progress = 0.0
            return

        if self.ai is not None:
            mode_mapping = {
                GhostState.CHASE: GhostMode.CHASE,
                GhostState.FLEE: GhostMode.FLEE,
                GhostState.RETURN_HOME: GhostMode.RETURN_HOME,
            }
            self.ai.set_mode(
                mode_mapping.get(self.ghost.state, GhostMode.CHASE)
            )
            target = (
                target_position
                if target_position is not None
                else self.ghost.home_position
            )
            next_direction = self.ai.get_next_direction(
                maze=maze,
                ghost_position=self.ghost.position,
                target_position=target,
                home_position=self.ghost.home_position,
                current_direction=self.ghost.direction,
            )
            if next_direction is not Direction.NONE:
                self.ghost.direction = next_direction

        cand = MovementSystem.calculate_next_position(self.ghost, maze)
        if (
            cand != self.ghost.position
            and self.collision_system.can_move_to(self.ghost, cand, maze)
        ):
            self.ghost.target_position = cand
        else:
            self.ghost.target_position = None
        self.ghost.movement_progress = 0.0

    def update(
        self,
        maze: Maze,
        target_position: Coordinate | None = None,
    ) -> None:
        """Calculate next direction via AI if configured and move the ghost."""
        cd = getattr(self.ghost, "respawn_cooldown", 0.0)
        if isinstance(cd, (int, float)) and cd > 0.0:
            self.ghost.target_position = None
            self.ghost.direction = Direction.NONE
            self.ghost.movement_progress = 0.0
            return

        dest = (
            self.ghost.target_position
            if isinstance(getattr(self.ghost, "target_position", None), tuple)
            else None
        )

        if dest is not None:
            self.collision_system.move_if_valid(
                self.ghost,
                dest,
                maze,
            )
            if (
                self.ghost.state is GhostState.RETURN_HOME
                and self.ghost.position == self.ghost.home_position
            ):
                rc = getattr(self.ghost, "respawn_cooldown", 0.0)
                if isinstance(rc, (int, float)) and rc <= 0.0:
                    self.ghost.respawn_cooldown = 5.0
                    self.ghost.direction = Direction.NONE
                    self.ghost.target_position = None
                    self.ghost.movement_progress = 0.0
        else:
            if self.ai is not None:
                mode_mapping = {
                    GhostState.CHASE: GhostMode.CHASE,
                    GhostState.FLEE: GhostMode.FLEE,
                    GhostState.RETURN_HOME: GhostMode.RETURN_HOME,
                }
                self.ai.set_mode(
                    mode_mapping.get(self.ghost.state, GhostMode.CHASE)
                )
                target = (
                    target_position
                    if target_position is not None
                    else self.ghost.home_position
                )
                next_direction = self.ai.get_next_direction(
                    maze=maze,
                    ghost_position=self.ghost.position,
                    target_position=target,
                    home_position=self.ghost.home_position,
                    current_direction=self.ghost.direction,
                )
                if next_direction is not Direction.NONE:
                    self.ghost.direction = next_direction

            calculated_target = MovementSystem.calculate_next_position(
                self.ghost,
                maze,
            )

            self.collision_system.move_if_valid(
                self.ghost,
                calculated_target,
                maze,
            )

        self.prepare_next_step(maze, target_position)
