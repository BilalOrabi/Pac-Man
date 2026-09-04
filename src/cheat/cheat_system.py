"""Cheat system for the Pac-Man game."""

from dataclasses import dataclass


@dataclass
class CheatSystem:
    """Manage optional cheat features."""

    is_invincible: bool = False
    is_infinite_lives: bool = False
    is_power_mode_enabled: bool = False

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

    def reset(self) -> None:
        """Disable all cheats."""
        self.is_invincible = False
        self.is_infinite_lives = False
        self.is_power_mode_enabled = False
