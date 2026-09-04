"""Tests for the Pac-Man gameplay controller."""

from unittest.mock import Mock

import pytest

from src.controllers.gameplay_controller import GameplayController
from src.controllers.ghost_controller import GhostController
from src.controllers.player_controller import PlayerController
from src.systems.lives import LivesSystem
from src.systems.power_mode import PowerModeSystem
from src.systems.scoring import ScoringSystem
from src.systems.timer_system import TimerSystem
from src.world.level import Level


def create_gameplay_controller() -> GameplayController:
    """Create a gameplay controller with mocked gameplay dependencies."""
    return GameplayController(
        player_controller=Mock(spec=PlayerController),
        ghost_controllers=[
            Mock(spec=GhostController),
            Mock(spec=GhostController),
        ],
        lives_system=LivesSystem(starting_lives=3),
        scoring_system=ScoringSystem(
            points_per_pacgum=10,
            points_per_super_pacgum=50,
            points_per_ghost=200,
        ),
        power_mode_system=PowerModeSystem(duration=10.0),
        timer_system=TimerSystem(maximum_level_time=120.0),
    )


def create_level() -> Level:
    """Create a mocked level for gameplay-controller tests."""
    level = Mock(spec=Level)
    level.maze = Mock()
    return level


def test_update_rejects_negative_elapsed_time() -> None:
    """Negative elapsed time should be rejected."""
    controller = create_gameplay_controller()
    level = create_level()

    with pytest.raises(ValueError, match="Elapsed time cannot be negative"):
        controller.update(
            level=level,
            elapsed_seconds=-1.0,
        )


def test_update_updates_level_timer() -> None:
    """Updating gameplay should advance the level timer."""
    controller = create_gameplay_controller()
    level = create_level()

    controller.update(
        level=level,
        elapsed_seconds=1.5,
    )

    assert level.update_time.call_count == 1
    level.update_time.assert_called_once_with(1.5)


def test_update_updates_power_mode() -> None:
    """Updating gameplay should advance power mode timing."""
    controller = create_gameplay_controller()
    level = create_level()

    controller.power_mode_system.activate()

    controller.update(
        level=level,
        elapsed_seconds=2.0,
    )

    assert controller.power_mode_system.remaining_time == 8.0


def test_update_updates_player_controller() -> None:
    """Updating gameplay should update the player."""
    controller = create_gameplay_controller()
    level = create_level()

    controller.update(
        level=level,
        elapsed_seconds=1.0,
    )

    controller.player_controller.update.assert_called_once_with(
        level.maze,
    )


def test_update_updates_all_ghost_controllers() -> None:
    """Updating gameplay should update every ghost."""
    controller = create_gameplay_controller()
    level = create_level()

    controller.update(
        level=level,
        elapsed_seconds=1.0,
    )

    for ghost_controller in controller.ghost_controllers:
        ghost_controller.update.assert_called_once_with(
            level.maze,
        )


def test_reset_level_resets_timer() -> None:
    """Resetting a level should reset its timer."""
    controller = create_gameplay_controller()
    level = create_level()

    level.reset_timer = Mock()

    controller.reset_level(level)

    level.reset_timer.assert_called_once_with()


def test_reset_level_deactivates_power_mode() -> None:
    """Resetting a level should deactivate power mode."""
    controller = create_gameplay_controller()

    controller.power_mode_system.activate()

    controller.reset_level(
        create_level(),
    )

    assert controller.power_mode_system.is_active is False


def test_ghost_respawn_cooldown_delays_chase_by_five_seconds() -> None:
    """Ghost with respawn_cooldown > 0 should not chase until 5s elapse."""
    from src.entities.ghost import Ghost, GhostState, GhostType
    controller = create_gameplay_controller()
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(0, 0),
        home_position=(0, 0),
        state=GhostState.RETURN_HOME,
        respawn_cooldown=5.0,
    )
    ghost_ctrl = Mock()
    ghost_ctrl.ghost = ghost
    controller.ghost_controllers = [ghost_ctrl]

    level = create_level()

    # Advance 3.0s -> 2.0s cooldown remains, state is still RETURN_HOME
    controller.update(level, 3.0)
    assert ghost.respawn_cooldown == pytest.approx(2.0)
    assert ghost.state is GhostState.RETURN_HOME

    # Advance remaining 2.0s -> cooldown expires, state transitions to CHASE
    controller.update(level, 2.0)
    assert ghost.respawn_cooldown == 0.0
    assert ghost.state is GhostState.CHASE


def test_reset_level_synchronizes_lives_system() -> None:
    """Resetting the level should update lives_system with player lives."""
    controller = create_gameplay_controller()
    level = create_level()
    mock_player = Mock()
    mock_player.lives = 5
    level.player = mock_player

    controller.reset_level(level)

    assert controller.lives_system.remaining_lives == 5


def test_update_passes_personality_chase_target() -> None:
    """Updating ghosts in chase mode should pass personality targets."""
    from src.entities.direction import Direction
    from src.entities.ghost import Ghost, GhostState, GhostType
    from src.entities.player import Player

    controller = create_gameplay_controller()
    pinky = Ghost(
        ghost_type=GhostType.PINK,
        position=(18, 1),
        home_position=(18, 1),
        speed=1.8214,
        state=GhostState.CHASE,
    )
    ghost_ctrl = Mock()
    ghost_ctrl.ghost = pinky
    controller.ghost_controllers = [ghost_ctrl]

    player = Player(position=(10, 10), direction=Direction.UP)
    level = create_level()
    level.player = player
    level.ghosts = [pinky]

    controller.update(level, 1.0)

    # 4 tiles ahead of (10, 10) facing UP is (10, 6)
    assert ghost_ctrl.update.call_count >= 1
    call_args = ghost_ctrl.update.call_args[0]
    assert call_args[0] == level.maze
    assert call_args[1] == (10, 6)
