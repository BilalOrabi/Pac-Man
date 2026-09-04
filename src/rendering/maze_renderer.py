"""Renderer responsible for displaying the Pac-Man maze."""

import os
from dataclasses import dataclass, field
from typing import Any

import pygame

from src.maze.maze import Maze, Wall
from src.rendering.renderer import Renderer
from src.theme.asset_manager import AssetManager


@dataclass
class MazeRenderer(Renderer):
    """Render the maze using configured presentation assets."""

    asset_manager: AssetManager
    maze: Maze | None = None
    is_initialized: bool = False
    background_asset: str | None = None
    surface: Any = None
    level: Any = None
    cell_size: int = 24
    offset_x: int = 30
    offset_y: int = 50
    _image_cache: dict[tuple[str, int], Any] = field(
        default_factory=dict, init=False, repr=False
    )

    def set_maze(self, maze: Maze) -> None:
        """Set the maze that should be rendered."""
        self.maze = maze

    def initialize(self) -> None:
        """Initialize the maze renderer and its presentation assets."""
        if not self.asset_manager.is_initialized:
            self.asset_manager.initialize()

        self.background_asset = self.asset_manager.get_background()
        self.is_initialized = True

    def render(self) -> None:
        """Render the currently assigned maze."""
        if not self.is_initialized:
            raise RuntimeError(
                "MazeRenderer must be initialized before rendering."
            )

        if self.maze is None:
            raise RuntimeError(
                "Maze must be assigned before rendering."
            )

        if self.background_asset is None:
            raise RuntimeError(
                "Background asset must be configured before rendering."
            )

        if self.surface is not None:
            self._render_to_surface()

    def _get_scaled_image(self, rel_path: str, size: int) -> Any:
        """Load and cache an image scaled to the requested dimension."""
        try:
            cache_key = (rel_path, size)
            if cache_key in self._image_cache:
                return self._image_cache[cache_key]

            if not os.path.exists(rel_path):
                return None

            img = pygame.image.load(rel_path).convert_alpha()
            scaled = pygame.transform.scale(img, (size, size))
            self._image_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _render_to_surface(self) -> None:
        """Draw maze corridors, walls, and pellets to the Pygame surface."""
        if self.maze is None or self.surface is None:
            return

        self.surface.fill((10, 10, 20))
        wall_color = (33, 33, 222)
        wall_block_img = self._get_scaled_image(
            os.path.join("assets", "images", "wall_block.png"),
            self.cell_size,
        )

        line_width = max(2, self.cell_size // 12)

        for y, row in enumerate(self.maze.cells):
            for x, cell in enumerate(row):
                px = self.offset_x + x * self.cell_size
                py = self.offset_y + y * self.cell_size

                if cell.is_solid_block:
                    if wall_block_img is not None:
                        self.surface.blit(wall_block_img, (px, py))
                    else:
                        pygame.draw.rect(
                            self.surface,
                            wall_color,
                            (px, py, self.cell_size, self.cell_size),
                        )
                    continue

                if cell.has_wall(Wall.NORTH):
                    pygame.draw.line(
                        self.surface,
                        wall_color,
                        (px, py),
                        (px + self.cell_size, py),
                        line_width,
                    )
                if cell.has_wall(Wall.SOUTH):
                    pygame.draw.line(
                        self.surface,
                        wall_color,
                        (px, py + self.cell_size),
                        (px + self.cell_size, py + self.cell_size),
                        line_width,
                    )
                if cell.has_wall(Wall.WEST):
                    pygame.draw.line(
                        self.surface,
                        wall_color,
                        (px, py),
                        (px, py + self.cell_size),
                        line_width,
                    )
                if cell.has_wall(Wall.EAST):
                    pygame.draw.line(
                        self.surface,
                        wall_color,
                        (px + self.cell_size, py),
                        (px + self.cell_size, py + self.cell_size),
                        line_width,
                    )

        # Draw pacgums and super-pacgums
        if self.level is not None:
            half = self.cell_size // 2
            dot_size = max(8, self.cell_size // 3)
            dot_img = self._get_scaled_image(
                os.path.join("assets", "images", "dot.png"),
                dot_size,
            )

            super_dot_size = max(16, self.cell_size * 2 // 3)
            super_dot_img = self._get_scaled_image(
                os.path.join("assets", "images", "super_dot.png"),
                super_dot_size,
            )

            pacgums: set[tuple[int, int]] = getattr(
                self.level, "pacgums", set()
            )
            for gx, gy in pacgums:
                dot_x = self.offset_x + gx * self.cell_size + half
                dot_y = self.offset_y + gy * self.cell_size + half
                if dot_img is not None:
                    self.surface.blit(
                        dot_img,
                        (dot_x - dot_size // 2, dot_y - dot_size // 2),
                    )
                else:
                    pygame.draw.circle(
                        self.surface,
                        (255, 184, 151),
                        (dot_x, dot_y),
                        max(2, self.cell_size // 8),
                    )

            super_pacgums: set[tuple[int, int]] = getattr(
                self.level, "super_pacgums", set()
            )
            for sx, sy in super_pacgums:
                dot_x = self.offset_x + sx * self.cell_size + half
                dot_y = self.offset_y + sy * self.cell_size + half
                if super_dot_img is not None:
                    self.surface.blit(
                        super_dot_img,
                        (
                            dot_x - super_dot_size // 2,
                            dot_y - super_dot_size // 2,
                        ),
                    )
                else:
                    pygame.draw.circle(
                        self.surface,
                        (255, 200, 180),
                        (dot_x, dot_y),
                        max(4, self.cell_size // 4),
                    )

    def shutdown(self) -> None:
        """Shut down the maze renderer."""
        self.background_asset = None
        self.is_initialized = False
        self._image_cache.clear()
