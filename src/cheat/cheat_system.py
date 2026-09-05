"""Cheat system for the Pac-Man game."""

from dataclasses import dataclass


@dataclass
class CheatSystem:
    """Manage optional cheat features."""

    is_invincible: bool = False
    is_infinite_lives: bool = False
    is_power_mode_enabled: bool = False
    is_ghosts_frozen: bool = False
    is_speed_boosted: bool = False
    level_skip_requested: bool = False

    def _toggle_flag(self, attr_name: str) -> bool:
        """Invert a boolean cheat flag attribute and return its new value."""
        new_val = not getattr(self, attr_name)
        setattr(self, attr_name, new_val)
        return new_val

    def toggle_invincibility(self) -> bool:
        """Toggle player invincibility and return the new state."""
        return self._toggle_flag("is_invincible")

    def toggle_infinite_lives(self) -> bool:
        """Toggle infinite lives and return the new state."""
        return self._toggle_flag("is_infinite_lives")

    def toggle_power_mode(self) -> bool:
        """Toggle permanent power mode and return the new state."""
        return self._toggle_flag("is_power_mode_enabled")

    def toggle_ghost_freeze(self) -> bool:
        """Toggle freezing ghosts and return the new state."""
        return self._toggle_flag("is_ghosts_frozen")

    def toggle_speed_boost(self) -> bool:
        """Toggle player speed boost and return the new state."""
        return self._toggle_flag("is_speed_boosted")

    def trigger_level_skip(self) -> None:
        """Request immediate level skip."""
        self.level_skip_requested = True

    def _clear_all_flags(self) -> None:
        """Reset all internal boolean cheat flags to inactive False."""
        self.is_invincible = False
        self.is_infinite_lives = False
        self.is_power_mode_enabled = False
        self.is_ghosts_frozen = False
        self.is_speed_boosted = False
        self.level_skip_requested = False

    def reset(self) -> None:
        """Disable all cheats."""
        self._clear_all_flags()
