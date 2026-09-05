"""Renderer responsible for displaying the Pac-Man player."""

import os
from dataclasses import dataclass, field
from typing import Any

import pygame

from src.entities.direction import Direction
from src.entities.player import Player
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class PlayerRenderer(Renderer):
    """Render the Pac-Man player using configured presentation assets."""

    asset_manager: AssetManager
    player: Player | None = None
    is_initialized: bool = False
    player_sprite_asset: str | None = None
    surface: Any = None
    cell_size: int = 24
    offset_x: int = 30
    offset_y: int = 50
    _frame_cache: dict[tuple[str, int, int], Any] = field(
        default_factory=dict, init=False, repr=False
    )

    def set_player(self, player: Player) -> None:
        """Set the player that should be rendered."""
        self.player = player

    def initialize(self) -> None:
        """Initialize the player renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.player_sprite_asset = (
            self.asset_manager.get_player_sprite()
        )
        self.is_initialized = True

    def render(self) -> None:
        """Render the currently assigned player."""
        if not self.is_initialized:
            raise RuntimeError(
                "PlayerRenderer must be initialized before rendering."
            )

        if self.player is None:
            raise RuntimeError(
                "Player must be assigned before rendering."
            )

        if self.player_sprite_asset is None:
            raise RuntimeError(
                "Player sprite asset must be configured before rendering."
            )

        if self.surface is not None and self.player is not None:
            self._render_to_surface()

    def _resolve_frame_path(
        self, dir_folder: str, frame_idx: int
    ) -> str | None:
        """Resolve filesystem path for the animated player frame."""
        path = os.path.join("assets", "images", dir_folder, f"{frame_idx}.png")
        if os.path.exists(path):
            return path
        if (
            self.player_sprite_asset
            and os.path.exists(self.player_sprite_asset)
        ):
            return self.player_sprite_asset
        return None

    def _get_player_frame(self) -> Any:
        """Load and return the appropriate directional animated frame."""
        try:
            direction = (
                self.player.direction if self.player else Direction.RIGHT
            )
            dir_folder = {
                Direction.UP: "pacman-up",
                Direction.DOWN: "pacman-down",
                Direction.LEFT: "pacman-left",
                Direction.RIGHT: "pacman-right",
                Direction.NONE: "pacman-right",
            }.get(direction, "pacman-right")

            ticks = pygame.time.get_ticks() if pygame.get_init() else 0
            frame_indices = [1, 2, 3, 2]
            frame_idx = frame_indices[(ticks // 120) % 4]

            sprite_size = max(16, round(self.cell_size * 28.0 / 36.0))
            cache_key = (dir_folder, frame_idx, sprite_size)
            if cache_key in self._frame_cache:
                return self._frame_cache[cache_key]

            path = self._resolve_frame_path(dir_folder, frame_idx)
            if path is None:
                return None

            img = pygame.image.load(path).convert_alpha()
            try:
                scaled = pygame.transform.smoothscale(
                    img, (sprite_size, sprite_size)
                )
            except Exception:
                scaled = pygame.transform.scale(
                    img, (sprite_size, sprite_size)
                )
            self._frame_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _render_fallback_circle(self, px: int, py: int) -> None:
        """Draw classic yellow circle when sprite image is unavailable."""
        center_x = px + self.cell_size // 2
        center_y = py + self.cell_size // 2
        radius = max(3, self.cell_size // 2 - 2)
        color = (
            (255, 255, 128)
            if self.player and self.player.is_powered_up
            else (255, 255, 0)
        )
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)

    def _render_to_surface(self) -> None:
        """Draw Pac-Man to the destination Pygame surface."""
        if self.surface is None or self.player is None:
            return

        if hasattr(self.player, "get_visual_position"):
            vx, vy = self.player.get_visual_position()
        else:
            vx = float(self.player.position[0])
            vy = float(self.player.position[1])

        sprite_size = max(16, round(self.cell_size * 28.0 / 36.0))
        margin = (self.cell_size - sprite_size) // 2
        px = self.offset_x + round(vx * self.cell_size) + margin
        py = self.offset_y + round(vy * self.cell_size) + margin

        sprite = self._get_player_frame()
        if sprite is not None:
            self.surface.blit(sprite, (px, py))
            return

        self._render_fallback_circle(px, py)

    def shutdown(self) -> None:
        """Shut down the player renderer."""
        self.player_sprite_asset = None
        self.is_initialized = False
        self._frame_cache.clear()
