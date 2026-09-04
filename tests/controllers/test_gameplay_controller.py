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
