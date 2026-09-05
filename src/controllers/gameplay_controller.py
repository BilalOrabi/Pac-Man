"""Controller responsible for coordinating Pac-Man gameplay systems."""

from dataclasses import dataclass, field
from typing import Any, cast

from src.ai.ghost_targeting import GhostTargeting
from src.cheat.cheat_system import CheatSystem
from src.controllers.ghost_controller import GhostController
from src.controllers.player_controller import PlayerController
from src.entities.direction import Direction
from src.entities.ghost import GhostState
from src.systems.collision import CollisionSystem
from src.systems.lives import LivesSystem
from src.systems.movement import MovementSystem
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
    cheat_system: CheatSystem | None = None
    player_timer: float = 0.0
    ghost_timers: list[float] = field(default_factory=list)
    wave_timer: float = 0.0
    is_scatter_wave: bool = False

    def _check_level_skip(self, level: Level) -> bool:
        """Process cheat level skip request if active."""
        if self.cheat_system and self.cheat_system.level_skip_requested:
            level.completed = True
            self.cheat_system.level_skip_requested = False
            return True
        return False

    def _sync_power_mode(self, player: Any) -> None:
        """Synchronize player power mode state with systems and cheats."""
        if player is not None:
            if self.cheat_system and self.cheat_system.is_power_mode_enabled:
                player.activate_power_mode()
            elif not self.power_mode_system.is_active:
                player.deactivate_power_mode()

    def _sync_player_turnaround(
        self, player: Any, step_interval: float
    ) -> None:
        """Synchronize player movement timer if direction reversal occurred."""
        curr_prog = getattr(player, "movement_progress", 0.0)
        expected_timer = curr_prog * step_interval
        if abs(self.player_timer - expected_timer) > 0.05 * step_interval:
            self.player_timer = expected_timer

    def _prepare_player_target(
        self, player: Any, level: Level, cur_dir: Direction
    ) -> tuple[bool, Direction]:
        """Verify path ahead or apply buffered turn if available."""
        can_move = self.player_controller._can_move_in_direction(
            cur_dir, level.maze
        )
        buf_dir = self.player_controller.buffered_direction
        if not can_move and buf_dir is not None:
            if self.player_controller._can_move_in_direction(
                buf_dir, level.maze
            ):
                player.direction = buf_dir
                self.player_controller.buffered_direction = None
                cur_dir = buf_dir
                can_move = True

        if not can_move:
            self.player_timer = 0.0
            if hasattr(player, "movement_progress"):
                player.movement_progress = 0.0
            if hasattr(player, "target_position"):
                player.target_position = None
            return False, cur_dir

        cand = MovementSystem.calculate_next_position(player, level.maze)
        cs = self.player_controller.collision_system
        if (
            cand != player.position
            and cs.can_move_to(player, cand, level.maze)
        ):
            player.target_position = cand
        else:
            player.target_position = None
            player.direction = Direction.NONE
            self.player_timer = 0.0
            if hasattr(player, "movement_progress"):
                player.movement_progress = 0.0
            return False, cur_dir

        return True, cur_dir

    def _step_player_pacing(
        self, player: Any, level: Level, elapsed: float
    ) -> tuple[bool, float]:
        """Compute movement pacing returning (should_step, step_interval)."""
        player_speed = getattr(player, "speed", 0.0)
        if not (
            player is not None
            and isinstance(player_speed, (int, float))
            and player_speed > 0
        ):
            return True, 0.0

        player_speed = 2.1429
        speed_mult = (
            2.2
            if (self.cheat_system and self.cheat_system.is_speed_boosted)
            else 1.0
        )
        step_interval = 1.0 / (player_speed * speed_mult)

        self._sync_player_turnaround(player, step_interval)

        cur_dir = getattr(player, "direction", Direction.NONE)
        if cur_dir is Direction.NONE:
            self.player_timer = 0.0
            if hasattr(player, "movement_progress"):
                player.movement_progress = 0.0
            if hasattr(player, "target_position"):
                player.target_position = None
            return False, step_interval

        if getattr(player, "target_position", None) is None:
            can_step, _ = self._prepare_player_target(player, level, cur_dir)
            if not can_step:
                return False, step_interval

        if getattr(player, "target_position", None) is not None:
            self.player_timer += elapsed
            if self.player_timer >= step_interval:
                self.player_timer %= step_interval
                return True, step_interval
            if hasattr(player, "movement_progress"):
                player.movement_progress = min(
                    1.0, self.player_timer / step_interval
                )
            return False, step_interval

        return True, step_interval

    def _execute_player_step(
        self, player: Any, level: Level, step_interval: float
    ) -> None:
        """Execute discrete player step and prepare next cell target."""
        self.player_controller.update(level.maze)
        if player is not None and step_interval > 0:
            cur_dir = getattr(player, "direction", Direction.NONE)
            if cur_dir is not Direction.NONE:
                cand = MovementSystem.calculate_next_position(
                    player, level.maze
                )
                cs = self.player_controller.collision_system
                if cand != player.position and cs.can_move_to(
                    player, cand, level.maze
                ):
                    player.target_position = cand
                    if hasattr(player, "movement_progress"):
                        player.movement_progress = min(
                            1.0, self.player_timer / step_interval
                        )
                else:
                    player.target_position = None
                    player.direction = Direction.NONE
                    if hasattr(player, "movement_progress"):
                        player.movement_progress = 0.0
                    self.player_timer = 0.0

    def _consume_pellets(self, level: Level, player: Any) -> None:
        """Consume pellets at player's current logical tile position."""
        if player is None or not hasattr(level, "consume_pacgum_at"):
            return

        if hasattr(player, "get_visual_position"):
            vx, vy = player.get_visual_position()
            logical_pos = (round(vx), round(vy))
        else:
            logical_pos = player.position

        pellet_type = level.consume_pacgum_at(logical_pos)
        if pellet_type == "pacgum":
            player.add_score(self.scoring_system.calculate_pacgum_score())
        elif pellet_type == "super_pacgum":
            player.add_score(
                self.scoring_system.calculate_super_pacgum_score()
            )
            self.power_mode_system.activate()
            player.activate_power_mode()

    def _update_wave_timer(self, player: Any, elapsed: float) -> None:
        """Advance Chase (20s) and Scatter (6s) wave cycles."""
        is_powered_wave = (
            player.is_powered_up if player is not None else False
        ) or self.power_mode_system.is_active

        if not is_powered_wave:
            self.wave_timer += elapsed
            if self.is_scatter_wave:
                if self.wave_timer >= 6.0:
                    self.is_scatter_wave = False
                    self.wave_timer = 0.0
            else:
                if self.wave_timer >= 20.0:
                    self.is_scatter_wave = True
                    self.wave_timer = 0.0

    def _resolve_ghost_target(
        self, ghost: Any, state: Any, player: Any, level: Level
    ) -> tuple[int, int] | None:
        """Determine target tile for ghost based on personality and wave."""
        player_pos: tuple[int, int] | None = (
            player.position if player is not None else None
        )
        if self.is_scatter_wave or state is GhostState.RETURN_HOME:
            return cast(
                tuple[int, int] | None, getattr(ghost, "home_position", None)
            )
        if state is GhostState.FLEE:
            return player_pos
        if player is not None and player_pos is not None:
            return GhostTargeting.get_chase_target(
                ghost,
                player,
                getattr(level, "ghosts", None),
                level.maze,
            )
        return player_pos

    def _update_single_ghost(
        self,
        idx: int,
        gc: GhostController,
        level: Level,
        player: Any,
        elapsed: float,
    ) -> None:
        """Update movement pacing and step for an individual ghost."""
        ghost = getattr(gc, "ghost", None)
        cd = getattr(ghost, "respawn_cooldown", 0.0) if ghost else 0.0
        if ghost is not None and isinstance(cd, (int, float)) and cd > 0.0:
            ghost.respawn_cooldown = max(0.0, ghost.respawn_cooldown - elapsed)
            ghost.direction = Direction.NONE
            ghost.target_position = None
            ghost.movement_progress = 0.0
            self.ghost_timers[idx] = 0.0
            if ghost.respawn_cooldown == 0.0:
                ghost.state = GhostState.CHASE
            return

        ghost_speed = getattr(ghost, "speed", 0.0) if ghost else 0.0
        should_step = True
        target: tuple[int, int] | None = None

        if (
            ghost is not None
            and isinstance(ghost_speed, (int, float))
            and ghost_speed > 0
        ):
            ghost_speed = 1.8214
            state = getattr(ghost, "state", GhostState.CHASE)
            speed_factor = 0.50 if state is GhostState.FLEE else (
                1.8667 if state is GhostState.RETURN_HOME else 1.0
            )
            step_interval = 1.0 / (ghost_speed * speed_factor)

            target = self._resolve_ghost_target(ghost, state, player, level)

            if (
                getattr(ghost, "target_position", None) is None
                or ghost.direction is Direction.NONE
            ):
                if hasattr(gc, "prepare_next_step"):
                    gc.prepare_next_step(level.maze, target)

            self.ghost_timers[idx] += elapsed
            if self.ghost_timers[idx] >= step_interval:
                self.ghost_timers[idx] %= step_interval
                should_step = True
            else:
                if hasattr(ghost, "movement_progress"):
                    ghost.movement_progress = min(
                        1.0, self.ghost_timers[idx] / step_interval
                    )
                should_step = False

        if should_step:
            player_pos = player.position if player is not None else None
            if player_pos is not None or self.is_scatter_wave:
                gc.update(level.maze, target)
            else:
                gc.update(level.maze)
            if (
                ghost is not None
                and isinstance(ghost_speed, (int, float))
                and ghost_speed > 0
                and hasattr(ghost, "movement_progress")
            ):
                ghost.movement_progress = min(
                    1.0, self.ghost_timers[idx] / step_interval
                )

    def _update_ghosts(
        self, level: Level, player: Any, elapsed: float
    ) -> None:
        """Update all ghosts if not frozen by cheats."""
        if self.cheat_system and self.cheat_system.is_ghosts_frozen:
            return

        if len(self.ghost_timers) != len(self.ghost_controllers):
            self.ghost_timers = [0.0] * len(self.ghost_controllers)

        for idx, gc in enumerate(self.ghost_controllers):
            self._update_single_ghost(idx, gc, level, player, elapsed)

    def _sync_ghost_flee_states(
        self, ghosts: list[Any], is_powered: bool
    ) -> None:
        """Transition ghosts between CHASE and FLEE based on power state."""
        for idx, ghost in enumerate(ghosts):
            if is_powered and ghost.state is GhostState.CHASE:
                ghost.state = GhostState.FLEE
                rev_dir = ghost.direction.opposite()
                if rev_dir is not Direction.NONE:
                    if (
                        ghost.target_position is not None
                        and ghost.target_position != ghost.position
                        and getattr(ghost, "movement_progress", 0.0) > 0.0
                    ):
                        old_pos = ghost.position
                        ghost.position = ghost.target_position
                        ghost.target_position = old_pos
                        ghost.movement_progress = max(
                            0.0,
                            min(1.0, 1.0 - ghost.movement_progress),
                        )
                    else:
                        ghost.target_position = None
                        ghost.movement_progress = 0.0
                    ghost.direction = rev_dir
                    if idx < len(self.ghost_timers):
                        self.ghost_timers[idx] = 0.0
            elif not is_powered and ghost.state is GhostState.FLEE:
                ghost.state = GhostState.CHASE

    def _process_ghost_collision(
        self, player: Any, ghost: Any, level: Level, is_powered: bool
    ) -> None:
        """Resolve impact when player touches a ghost."""
        can_eat = (
            ghost.state is GhostState.FLEE
            or (is_powered and ghost.state is not GhostState.RETURN_HOME)
        )
        if can_eat:
            player.add_score(self.scoring_system.calculate_ghost_score())
            ghost.state = GhostState.RETURN_HOME
        elif ghost.state is GhostState.CHASE:
            invincible = (
                self.cheat_system is not None
                and (
                    self.cheat_system.is_invincible
                    or self.cheat_system.is_infinite_lives
                )
            )
            if not invincible:
                if self.lives_system.remaining_lives > 0:
                    self.lives_system.lose_life()
                if player.lives > 0:
                    player.lose_life()
                player.reset_position(level.maze.entry)
                self.player_timer = 0.0
                if hasattr(player, "movement_progress"):
                    player.movement_progress = 0.0
                if hasattr(player, "target_position"):
                    player.target_position = None

    def _handle_entity_collisions(
        self, level: Level, player: Any
    ) -> None:
        """Check and process collisions between player and ghosts."""
        ghosts = getattr(level, "ghosts", [])
        if player is None or not ghosts:
            return

        is_powered = (
            player.is_powered_up
            or self.power_mode_system.is_active
            or (
                self.cheat_system.is_power_mode_enabled
                if self.cheat_system is not None
                else False
            )
        )
        self._sync_ghost_flee_states(ghosts, is_powered)

        for ghost in ghosts:
            if CollisionSystem.check_entity_collision(player, ghost):
                self._process_ghost_collision(player, ghost, level, is_powered)

            if (
                ghost.state is GhostState.RETURN_HOME
                and ghost.position == ghost.home_position
            ):
                if getattr(ghost, "respawn_cooldown", 0.0) <= 0.0:
                    ghost.respawn_cooldown = 5.0
                    ghost.direction = Direction.NONE
                    ghost.target_position = None
                    ghost.movement_progress = 0.0

    def update(
        self,
        level: Level,
        elapsed_seconds: float,
    ) -> None:
        """Update all active gameplay systems for the current level."""
        if elapsed_seconds < 0:
            raise ValueError("Elapsed time cannot be negative.")

        if self._check_level_skip(level):
            return

        self.timer_system.update(level, elapsed_seconds)
        self.power_mode_system.update(elapsed_seconds)

        player = getattr(self.player_controller, "player", None)
        if player is None:
            player = getattr(level, "player", None)

        self._sync_power_mode(player)

        should_step, step_interval = self._step_player_pacing(
            player, level, elapsed_seconds
        )
        if should_step:
            self._execute_player_step(player, level, step_interval)

        self._consume_pellets(level, player)
        self._update_wave_timer(player, elapsed_seconds)
        self._update_ghosts(level, player, elapsed_seconds)
        self._handle_entity_collisions(level, player)

    def reset_level(self, level: Level) -> None:
        """Reset gameplay timing and entity bindings for a new level."""
        self.timer_system.reset(level)
        self.power_mode_system.deactivate()
        self.player_timer = 0.0
        self.ghost_timers = [0.0] * len(self.ghost_controllers)
        self.wave_timer = 0.0
        self.is_scatter_wave = False
        if hasattr(level, "player") and level.player is not None:
            self.player_controller.player = level.player
            self.player_controller.buffered_direction = None
            if hasattr(level.player, "movement_progress"):
                level.player.movement_progress = 0.0
            if hasattr(level.player, "target_position"):
                level.player.target_position = None
            if hasattr(self.lives_system, "reset"):
                self.lives_system.reset(level.player.lives)
        if hasattr(level, "ghosts") and level.ghosts:
            for gc, ghost in zip(self.ghost_controllers, level.ghosts):
                gc.ghost = ghost
                ghost.respawn_cooldown = 0.0
                if hasattr(ghost, "movement_progress"):
                    ghost.movement_progress = 0.0
                if hasattr(ghost, "target_position"):
                    ghost.target_position = None
