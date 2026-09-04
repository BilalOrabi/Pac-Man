"""Renderer responsible for displaying Pac-Man ghosts."""

import os
from dataclasses import dataclass, field
from typing import Any

import pygame

from src.entities.ghost import Ghost, GhostState
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class GhostRenderer(Renderer):
    """Render a Pac-Man ghost using configured presentation assets."""

    asset_manager: AssetManager
    ghost: Ghost | None = None
    is_initialized: bool = False
    ghost_sprite_asset: str | None = None
    surface: Any = None
    cell_size: int = 24
    offset_x: int = 30
    offset_y: int = 50
    _sprite_cache: dict[tuple[str, int], Any] = field(
        default_factory=dict, init=False, repr=False
    )

    def set_ghost(self, ghost: Ghost) -> None:
        """Set the ghost that should be rendered."""
        self.ghost = ghost

        if self.is_initialized:
            self.ghost_sprite_asset = (
                self.asset_manager.get_ghost_sprite(
                    ghost.ghost_type.value
                )
            )

    def initialize(self) -> None:
        """Initialize the ghost renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.is_initialized = True

        if self.ghost is not None:
            self.ghost_sprite_asset = (
                self.asset_manager.get_ghost_sprite(
                    self.ghost.ghost_type.value
                )
            )

    def render(self) -> None:
        """Render the currently assigned ghost."""
        if not self.is_initialized:
            raise RuntimeError(
                "GhostRenderer must be initialized before rendering."
            )

        if self.ghost is None:
            raise RuntimeError(
                "Ghost must be assigned before rendering."
            )

        if self.ghost_sprite_asset is None:
            raise RuntimeError(
                "Ghost sprite asset must be configured before rendering."
            )

        if self.surface is not None and self.ghost is not None:
            self._render_to_surface()

    def _get_ghost_image(self) -> Any:
        """Load and return the appropriate ghost sprite."""
        try:
            if not self.ghost:
                return None

            state = getattr(self.ghost, "state", GhostState.CHASE)
            if state is GhostState.FLEE:
                path = os.path.join("assets", "images", "ghost_frightened.png")
                if not os.path.exists(path):
                    path = os.path.join(
                        "assets", "images", "ghosts", "blue_ghost.png"
                    )
            elif state is GhostState.RETURN_HOME:
                return None  # Will draw eyes procedurally
            else:
                ghost_val = self.ghost.ghost_type.value
                path = (
                    self.ghost_sprite_asset
                    if self.ghost_sprite_asset
                    else f"assets/images/ghost_{ghost_val}.png"
                )

            sprite_size = max(16, round(self.cell_size * 28.0 / 36.0))
            cache_key = (path, sprite_size)
            if cache_key in self._sprite_cache:
                return self._sprite_cache[cache_key]

            img = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.scale(
                img, (sprite_size, sprite_size)
            )
            self._sprite_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _render_to_surface(self) -> None:
        """Draw Ghost to the destination Pygame surface."""
        if self.surface is None or self.ghost is None:
            return

        if hasattr(self.ghost, "get_visual_position"):
            vx, vy = self.ghost.get_visual_position()
        else:
            vx = float(self.ghost.position[0])
            vy = float(self.ghost.position[1])

        sprite_size = max(16, round(self.cell_size * 28.0 / 36.0))
        margin = (self.cell_size - sprite_size) // 2
        px = self.offset_x + round(vx * self.cell_size) + margin
        py = self.offset_y + round(vy * self.cell_size) + margin

        state = getattr(self.ghost, "state", GhostState.CHASE)
        if state is not GhostState.RETURN_HOME:
            sprite = self._get_ghost_image()
            if sprite is not None:
                self.surface.blit(sprite, (px, py))
                return

        # Procedural fallback (or eyes for RETURN_HOME)
        center_x = px + self.cell_size // 2
        center_y = py + self.cell_size // 2
        radius = max(3, self.cell_size // 2 - 2)

        if state is GhostState.RETURN_HOME:
            # Draw only eyes
            eye_offset = max(2, self.cell_size // 8)
            pygame.draw.circle(
                self.surface, (255, 255, 255),
                (center_x - eye_offset, center_y - eye_offset),
                max(2, radius // 2)
            )
            pygame.draw.circle(
                self.surface, (255, 255, 255),
                (center_x + eye_offset, center_y - eye_offset),
                max(2, radius // 2)
            )
            pygame.draw.circle(
                self.surface, (0, 0, 180),
                (center_x - eye_offset + 1, center_y - eye_offset),
                max(1, radius // 4)
            )
            pygame.draw.circle(
                self.surface, (0, 0, 180),
                (center_x + eye_offset + 1, center_y - eye_offset),
                max(1, radius // 4)
            )
            return

        color_map = {
            "red": (255, 0, 0),
            "pink": (255, 184, 255),
            "blue": (0, 255, 255),
            "orange": (255, 184, 82),
        }
        type_name = getattr(
            self.ghost.ghost_type, "value", str(self.ghost.ghost_type)
        ).lower()
        color = color_map.get(type_name, (255, 0, 0))

        if state is GhostState.FLEE:
            color = (33, 33, 255)

        pygame.draw.circle(
            self.surface, color, (center_x, center_y - 2), radius
        )
        pygame.draw.rect(
            self.surface,
            color,
            (center_x - radius, center_y - 2, radius * 2, radius),
        )

        eye_dx = max(2, self.cell_size // 8)
        pygame.draw.circle(
            self.surface, (255, 255, 255),
            (center_x - eye_dx, center_y - 3), 3
        )
        pygame.draw.circle(
            self.surface, (255, 255, 255),
            (center_x + eye_dx, center_y - 3), 3
        )
        pygame.draw.circle(
            self.surface, (0, 0, 180),
            (center_x - eye_dx + 1, center_y - 3), 1
        )
        pygame.draw.circle(
            self.surface, (0, 0, 180),
            (center_x + eye_dx + 1, center_y - 3), 1
        )

    def shutdown(self) -> None:
        """Shut down the ghost renderer."""
        self.ghost_sprite_asset = None
        self.is_initialized = False
        self._sprite_cache.clear()
