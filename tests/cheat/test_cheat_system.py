"""Tests for the Pac-Man cheat system."""

from src.cheat.cheat_system import CheatSystem


def test_cheat_system_starts_with_all_cheats_disabled() -> None:
    """All cheats should initially be disabled."""
    cheat_system = CheatSystem()

    assert cheat_system.is_invincible is False
    assert cheat_system.is_infinite_lives is False
    assert cheat_system.is_power_mode_enabled is False


def test_toggle_invincibility_enables_cheat() -> None:
    """Toggling invincibility should enable it."""
    cheat_system = CheatSystem()

    result = cheat_system.toggle_invincibility()

    assert result is True
    assert cheat_system.is_invincible is True


def test_toggle_invincibility_disables_cheat() -> None:
    """Toggling invincibility twice should disable it."""
    cheat_system = CheatSystem()

    cheat_system.toggle_invincibility()
    result = cheat_system.toggle_invincibility()

    assert result is False
    assert cheat_system.is_invincible is False


def test_toggle_infinite_lives_enables_cheat() -> None:
    """Toggling infinite lives should enable it."""
    cheat_system = CheatSystem()

    result = cheat_system.toggle_infinite_lives()

    assert result is True
    assert cheat_system.is_infinite_lives is True


def test_toggle_infinite_lives_disables_cheat() -> None:
    """Toggling infinite lives twice should disable it."""
    cheat_system = CheatSystem()

    cheat_system.toggle_infinite_lives()
    result = cheat_system.toggle_infinite_lives()

    assert result is False
    assert cheat_system.is_infinite_lives is False


def test_toggle_power_mode_enables_cheat() -> None:
    """Toggling permanent power mode should enable it."""
    cheat_system = CheatSystem()

    result = cheat_system.toggle_power_mode()

    assert result is True
    assert cheat_system.is_power_mode_enabled is True


def test_toggle_power_mode_disables_cheat() -> None:
    """Toggling permanent power mode twice should disable it."""
    cheat_system = CheatSystem()

    cheat_system.toggle_power_mode()
    result = cheat_system.toggle_power_mode()

    assert result is False
    assert cheat_system.is_power_mode_enabled is False


def test_cheats_are_independent() -> None:
    """Changing one cheat should not affect the others."""
    cheat_system = CheatSystem()

    cheat_system.toggle_invincibility()

    assert cheat_system.is_invincible is True
    assert cheat_system.is_infinite_lives is False
    assert cheat_system.is_power_mode_enabled is False


def test_reset_disables_all_cheats() -> None:
    """Reset should disable every cheat."""
    cheat_system = CheatSystem()

    cheat_system.toggle_invincibility()
    cheat_system.toggle_infinite_lives()
    cheat_system.toggle_power_mode()

    cheat_system.reset()

    assert cheat_system.is_invincible is False
    assert cheat_system.is_infinite_lives is False
    assert cheat_system.is_power_mode_enabled is False
