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

    def toggle_invincibility(self) -> bool:
        """Toggle player invincibility and return the new state."""
        self.is_invincible = not self.is_invincible
        return self.is_invincible

    def toggle_infinite_lives(self) -> bool:
        """Toggle infinite lives and return the new state."""
        self.is_infinite_lives = not self.is_infinite_lives
        return self.is_infinite_lives

    def toggle_power_mode(self) -> bool:
        """Toggle permanent power mode and return the new state."""
        self.is_power_mode_enabled = not self.is_power_mode_enabled
        return self.is_power_mode_enabled

    def toggle_ghost_freeze(self) -> bool:
        """Toggle freezing ghosts and return the new state."""
        self.is_ghosts_frozen = not self.is_ghosts_frozen
        return self.is_ghosts_frozen

    def toggle_speed_boost(self) -> bool:
        """Toggle player speed boost and return the new state."""
        self.is_speed_boosted = not self.is_speed_boosted
        return self.is_speed_boosted

    def trigger_level_skip(self) -> None:
        """Request immediate level skip."""
        self.level_skip_requested = True

    def reset(self) -> None:
        """Disable all cheats."""
        self.is_invincible = False
        self.is_infinite_lives = False
        self.is_power_mode_enabled = False
        self.is_ghosts_frozen = False
        self.is_speed_boosted = False
        self.level_skip_requested = False
