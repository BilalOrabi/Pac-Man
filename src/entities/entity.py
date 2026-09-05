"""Base domain entity for Pac-Man game objects."""

from dataclasses import dataclass

from src.entities.direction import Direction
from src.maze import Coordinate


@dataclass(kw_only=True)
class Entity:
    """Represent the common state shared by movable game entities."""

    position: Coordinate
    direction: Direction = Direction.NONE
    speed: float = 0.0
    movement_progress: float = 0.0
    target_position: Coordinate | None = None

    def set_direction(self, direction: Direction) -> None:
        """Set the entity's current movement direction."""
        self.direction = direction

    def stop(self) -> None:
        """Stop the entity from moving."""
        self.direction = Direction.NONE
        self.target_position = None
        self.movement_progress = 0.0

    @staticmethod
    def _interpolate_target(
        origin: Coordinate, target: Coordinate, progress: float
    ) -> tuple[float, float]:
        """Interpolate between origin and target coordinates."""
        x, y = origin
        tx, ty = target
        return (x + (tx - x) * progress, y + (ty - y) * progress)

    @staticmethod
    def _interpolate_direction(
        origin: Coordinate, direction: Direction, progress: float
    ) -> tuple[float, float]:
        """Interpolate from origin along movement direction."""
        x, y = origin
        offsets = {
            Direction.UP: (0.0, -1.0),
            Direction.RIGHT: (1.0, 0.0),
            Direction.DOWN: (0.0, 1.0),
            Direction.LEFT: (-1.0, 0.0),
        }
        dx, dy = offsets.get(direction, (0.0, 0.0))
        return (x + dx * progress, y + dy * progress)

    def get_visual_position(self) -> tuple[float, float]:
        """Return the sub-tile interpolated floating position."""
        x, y = self.position
        if self.movement_progress <= 0.0:
            return (float(x), float(y))

        t = max(0.0, min(1.0, self.movement_progress))
        if self.target_position is not None:
            return self._interpolate_target(
                self.position, self.target_position, t
            )

        if self.direction is Direction.NONE:
            return (float(x), float(y))

        return self._interpolate_direction(
            self.position, self.direction, t
        )
