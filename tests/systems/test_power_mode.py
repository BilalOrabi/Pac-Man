"""Tests for the power mode system."""

import pytest

from src.systems.power_mode import PowerModeState, PowerModeSystem


def create_power_mode_system() -> PowerModeSystem:
    """Create a power mode system for testing."""
    return PowerModeSystem(duration=8.0)


def test_power_mode_starts_inactive() -> None:
    """Power mode should initially be inactive."""
    power_mode_system = create_power_mode_system()

    assert power_mode_system.state == PowerModeState.INACTIVE
    assert not power_mode_system.is_active
    assert power_mode_system.remaining_time == 0.0


def test_activate_starts_power_mode() -> None:
    """Activating power mode should start its timer."""
    power_mode_system = create_power_mode_system()

    power_mode_system.activate()

    assert power_mode_system.state == PowerModeState.ACTIVE
    assert power_mode_system.is_active
    assert power_mode_system.remaining_time == 8.0


def test_update_reduces_remaining_time() -> None:
    """Updating should reduce the remaining power mode time."""
    power_mode_system = create_power_mode_system()
    power_mode_system.activate()

    power_mode_system.update(3.0)

    assert power_mode_system.remaining_time == 5.0
    assert power_mode_system.is_active


def test_power_mode_deactivates_when_timer_expires() -> None:
    """Power mode should deactivate when its timer reaches zero."""
    power_mode_system = create_power_mode_system()
    power_mode_system.activate()

    power_mode_system.update(8.0)

    assert power_mode_system.remaining_time == 0.0
    assert power_mode_system.state == PowerModeState.INACTIVE
    assert not power_mode_system.is_active


def test_timer_cannot_become_negative() -> None:
    """Remaining power mode time should never become negative."""
    power_mode_system = create_power_mode_system()
    power_mode_system.activate()

    power_mode_system.update(20.0)

    assert power_mode_system.remaining_time == 0.0
    assert not power_mode_system.is_active


def test_activate_restarts_power_mode() -> None:
    """Activating an active mode should reset its duration."""
    power_mode_system = create_power_mode_system()
    power_mode_system.activate()
    power_mode_system.update(5.0)

    power_mode_system.activate()

    assert power_mode_system.remaining_time == 8.0
    assert power_mode_system.is_active


def test_deactivate_stops_power_mode_immediately() -> None:
    """Power mode should be possible to deactivate immediately."""
    power_mode_system = create_power_mode_system()
    power_mode_system.activate()

    power_mode_system.deactivate()

    assert power_mode_system.remaining_time == 0.0
    assert power_mode_system.state == PowerModeState.INACTIVE


def test_update_does_nothing_when_inactive() -> None:
    """Updating inactive power mode should not change its state."""
    power_mode_system = create_power_mode_system()

    power_mode_system.update(5.0)

    assert power_mode_system.remaining_time == 0.0
    assert not power_mode_system.is_active


def test_duration_must_be_positive() -> None:
    """Power mode should reject zero or negative durations."""
    with pytest.raises(ValueError):
        PowerModeSystem(duration=0.0)

    with pytest.raises(ValueError):
        PowerModeSystem(duration=-1.0)


def test_elapsed_time_cannot_be_negative() -> None:
    """Power mode should reject negative elapsed time."""
    power_mode_system = create_power_mode_system()

    with pytest.raises(ValueError):
        power_mode_system.update(-1.0)
