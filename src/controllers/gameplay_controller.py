"""Controller responsible for coordinating Pac-Man gameplay systems."""

from dataclasses import dataclass

from src.controllers.ghost_controller import GhostController
from src.controllers.player_controller import PlayerController
from src.systems.lives import LivesSystem
from src.systems.power_mode import PowerModeSystem
from src.systems.scoring import ScoringSystem
from src.systems.timer_system import TimerSystem
from src.world.level import Level


@dataclass
class GameplayController:
    """Coordinate player, ghosts, scoring, power mode, and level timing."""

    player_controller: PlayerController
    ghost_controllers: list[GhostController]
    lives_system: LivesSystem
    scoring_system: ScoringSystem
    power_mode_system: PowerModeSystem
    timer_system: TimerSystem

    def update(
        self,
        level: Level,
        elapsed_seconds: float,
    ) -> None:
        """Update all active gameplay systems for the current level."""
        if elapsed_seconds < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        self.timer_system.update(
            level,
            elapsed_seconds,
        )

        self.power_mode_system.update(
            elapsed_seconds,
        )

        self.player_controller.update(
            level.maze,
        )

        for ghost_controller in self.ghost_controllers:
            ghost_controller.update(
                level.maze,
            )

    def reset_level(self, level: Level) -> None:
        """Reset gameplay timing for a new level."""
        self.timer_system.reset(level)
        self.power_mode_system.deactivate()
