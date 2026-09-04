"""Controller responsible for coordinating Pac-Man gameplay systems."""

from dataclasses import dataclass, field

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

        if self.cheat_system and self.cheat_system.level_skip_requested:
            level.completed = True
            self.cheat_system.level_skip_requested = False
            return

        self.timer_system.update(
            level,
            elapsed_seconds,
        )

        self.power_mode_system.update(
            elapsed_seconds,
        )

        player = getattr(self.player_controller, "player", None)
        if player is None:
            player = getattr(level, "player", None)
        if player is not None:
            if self.cheat_system and self.cheat_system.is_power_mode_enabled:
                player.activate_power_mode()
            elif not self.power_mode_system.is_active:
                player.deactivate_power_mode()

        # Delta-time based smooth movement pacing for player
        player_speed = getattr(player, "speed", 0.0)
        should_step_player = True
        if (
            player is not None
            and isinstance(player_speed, (int, float))
            and player_speed > 0
        ):
            # Enforce hardcoded arcade calibrated pacing (28 frames/cell)
            player_speed = 2.1429
            speed_mult = (
                2.2
                if (self.cheat_system and self.cheat_system.is_speed_boosted)
                else 1.0
            )
            step_interval = 1.0 / (player_speed * speed_mult)

            # Synchronize timer if turnaround occurred
            curr_prog = getattr(player, "movement_progress", 0.0)
            expected_timer = curr_prog * step_interval
            if abs(self.player_timer - expected_timer) > 0.05 * step_interval:
                self.player_timer = expected_timer

            cur_dir = getattr(player, "direction", Direction.NONE)

            if cur_dir is Direction.NONE:
                self.player_timer = 0.0
                if hasattr(player, "movement_progress"):
                    player.movement_progress = 0.0
                if hasattr(player, "target_position"):
                    player.target_position = None
                should_step_player = False
            else:
                if getattr(player, "target_position", None) is None:
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
                        should_step_player = False
                    else:
                        cand = MovementSystem.calculate_next_position(
                            player, level.maze
                        )
                        cs = self.player_controller.collision_system
                        can_occupy = (
                            cand != player.position
                            and cs.can_move_to(player, cand, level.maze)
                        )
                        if can_occupy:
                            player.target_position = cand
                        else:
                            player.target_position = None
                            player.direction = Direction.NONE
                            self.player_timer = 0.0
                            if hasattr(player, "movement_progress"):
                                player.movement_progress = 0.0
                            should_step_player = False

                if getattr(player, "target_position", None) is not None:
                    self.player_timer += elapsed_seconds
                    if self.player_timer >= step_interval:
                        self.player_timer %= step_interval
                        should_step_player = True
                    else:
                        if hasattr(player, "movement_progress"):
                            player.movement_progress = min(
                                1.0, self.player_timer / step_interval
                            )
                        should_step_player = False

        if should_step_player:
            self.player_controller.update(
                level.maze,
            )
            if (
                player is not None
                and isinstance(player_speed, (int, float))
                and player_speed > 0
            ):
                cur_dir = getattr(player, "direction", Direction.NONE)
                if cur_dir is not Direction.NONE:
                    cand = MovementSystem.calculate_next_position(
                        player, level.maze
                    )
                    cs = self.player_controller.collision_system
                    can_occupy = (
                        cand != player.position
                        and cs.can_move_to(player, cand, level.maze)
                    )
                    if can_occupy:
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

        # Pellet consumption using rounded logical tile coordinates
        if player is not None and hasattr(level, "consume_pacgum_at"):
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

        # Wave tracking: Chase (20s) / Scatter (6s)
        is_powered_wave = (
            player.is_powered_up
            if player is not None
            else False
        ) or self.power_mode_system.is_active
        if not is_powered_wave:
            self.wave_timer += elapsed_seconds
            if self.is_scatter_wave:
                if self.wave_timer >= 6.0:
                    self.is_scatter_wave = False
                    self.wave_timer = 0.0
            else:
                if self.wave_timer >= 20.0:
                    self.is_scatter_wave = True
                    self.wave_timer = 0.0

        # Ghost updates with smooth delta-time speed pacing
        ghosts_frozen = (
            self.cheat_system.is_ghosts_frozen
            if self.cheat_system is not None
            else False
        )
        if not ghosts_frozen:
            if len(self.ghost_timers) != len(self.ghost_controllers):
                self.ghost_timers = [0.0] * len(self.ghost_controllers)

            player_pos = player.position if player is not None else None
            for idx, ghost_controller in enumerate(self.ghost_controllers):
                ghost = getattr(ghost_controller, "ghost", None)
                cd = (
                    getattr(ghost, "respawn_cooldown", 0.0)
                    if ghost is not None
                    else 0.0
                )
                is_cooling = isinstance(cd, (int, float)) and cd > 0.0
                if ghost is not None and is_cooling:
                    ghost.respawn_cooldown = max(
                        0.0, ghost.respawn_cooldown - elapsed_seconds
                    )
                    ghost.direction = Direction.NONE
                    ghost.target_position = None
                    ghost.movement_progress = 0.0
                    self.ghost_timers[idx] = 0.0
                    if ghost.respawn_cooldown == 0.0:
                        ghost.state = GhostState.CHASE
                    continue

                ghost_speed = getattr(ghost, "speed", 0.0)
                should_step_ghost = True
                target = player_pos

                if (
                    ghost is not None
                    and isinstance(ghost_speed, (int, float))
                    and ghost_speed > 0
                ):
                    # Enforce hardcoded arcade pacing (85% of player)
                    ghost_speed = 1.8214
                    state = getattr(ghost, "state", GhostState.CHASE)
                    if state is GhostState.FLEE:
                        speed_factor = 0.50
                    elif state is GhostState.RETURN_HOME:
                        speed_factor = 1.8667
                    else:
                        speed_factor = 1.0

                    step_interval = 1.0 / (ghost_speed * speed_factor)

                    if (
                        self.is_scatter_wave
                        or state is GhostState.RETURN_HOME
                    ):
                        target = ghost.home_position
                    elif state is GhostState.FLEE:
                        target = player_pos
                    elif player is not None and player_pos is not None:
                        target = GhostTargeting.get_chase_target(
                            ghost,
                            player,
                            getattr(level, "ghosts", None),
                            level.maze,
                        )
                    else:
                        target = player_pos

                    if (
                        getattr(ghost, "target_position", None) is None
                        or ghost.direction is Direction.NONE
                    ):
                        if hasattr(ghost_controller, "prepare_next_step"):
                            ghost_controller.prepare_next_step(
                                level.maze, target
                            )

                    self.ghost_timers[idx] += elapsed_seconds
                    if self.ghost_timers[idx] >= step_interval:
                        self.ghost_timers[idx] %= step_interval
                        should_step_ghost = True
                    else:
                        if hasattr(ghost, "movement_progress"):
                            ghost.movement_progress = min(
                                1.0, self.ghost_timers[idx] / step_interval
                            )
                        should_step_ghost = False

                if should_step_ghost:
                    if player_pos is not None or self.is_scatter_wave:
                        ghost_controller.update(
                            level.maze,
                            target,
                        )
                    else:
                        ghost_controller.update(
                            level.maze,
                        )
                    if (
                        ghost is not None
                        and isinstance(ghost_speed, (int, float))
                        and ghost_speed > 0
                        and hasattr(ghost, "movement_progress")
                    ):
                        ghost.movement_progress = min(
                            1.0, self.ghost_timers[idx] / step_interval
                        )

        # Entity collisions and ghost state checks
        ghosts = getattr(level, "ghosts", [])
        if player is not None and ghosts:
            is_powered = (
                player.is_powered_up
                or self.power_mode_system.is_active
                or (
                    self.cheat_system.is_power_mode_enabled
                    if self.cheat_system is not None
                    else False
                )
            )
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

                if CollisionSystem.check_entity_collision(player, ghost):
                    can_eat = (
                        ghost.state is GhostState.FLEE
                        or (
                            is_powered
                            and ghost.state is not GhostState.RETURN_HOME
                        )
                    )
                    if can_eat:
                        player.add_score(
                            self.scoring_system.calculate_ghost_score()
                        )
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

                if (
                    ghost.state is GhostState.RETURN_HOME
                    and ghost.position == ghost.home_position
                ):
                    if getattr(ghost, "respawn_cooldown", 0.0) <= 0.0:
                        ghost.respawn_cooldown = 5.0
                        ghost.direction = Direction.NONE
                        ghost.target_position = None
                        ghost.movement_progress = 0.0

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
