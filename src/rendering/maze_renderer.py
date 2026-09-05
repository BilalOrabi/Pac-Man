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
    _bg_cache: dict[tuple[str, int, int], Any] = field(
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
            try:
                scaled = pygame.transform.smoothscale(img, (size, size))
            except Exception:
                scaled = pygame.transform.scale(img, (size, size))
            self._image_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _resolve_background_path(self) -> str:
        """Find the most appropriate background image path."""
        candidate = "assets/images/game_background.jpg"
        if os.path.exists(candidate):
            return candidate
        bg_path = self.background_asset or ""
        if (
            bg_path
            and not os.path.exists(bg_path)
            and bg_path.endswith(".png")
        ):
            alt = bg_path[:-4] + ".jpg"
            if os.path.exists(alt):
                return alt
        return bg_path

    def _get_background_surface(self, width: int, height: int) -> Any:
        """Load and cache the game background scaled to screen dimensions."""
        try:
            bg_path = self._resolve_background_path()
            if not bg_path or not os.path.exists(bg_path):
                return None

            cache_key = (bg_path, width, height)
            if cache_key in self._bg_cache:
                return self._bg_cache[cache_key]

            raw_img = pygame.image.load(bg_path)
            if pygame.display.get_surface() is not None:
                img = raw_img.convert()
            else:
                img = raw_img
            scaled = pygame.transform.scale(img, (width, height))
            self._bg_cache[cache_key] = scaled
            return scaled
        except Exception:
            return None

    def _render_background(self, surf_w: int, surf_h: int) -> None:
        """Render background image or fallback clear color."""
        bg_surf = self._get_background_surface(surf_w, surf_h)
        if bg_surf is not None:
            self.surface.blit(bg_surf, (0, 0))
        else:
            self.surface.fill((10, 10, 20))

    def _render_maze_backdrop(self) -> None:
        """Render a darkened translucent rectangle under the maze corridors."""
        if self.maze is None:
            return
        maze_pixel_w = self.maze.width * self.cell_size
        maze_pixel_h = self.maze.height * self.cell_size
        backdrop = pygame.Surface(
            (maze_pixel_w + 16, maze_pixel_h + 16), pygame.SRCALPHA
        )
        backdrop.fill((8, 10, 24, 210))
        self.surface.blit(backdrop, (self.offset_x - 8, self.offset_y - 8))

    def _render_cell_walls(
        self,
        cell: Any,
        px: int,
        py: int,
        wall_block_img: Any,
        wall_color: tuple[int, int, int],
        line_width: int,
    ) -> None:
        """Draw walls or solid block for a single maze cell."""
        if cell.is_solid_block:
            if wall_block_img is not None:
                self.surface.blit(wall_block_img, (px, py))
            else:
                pygame.draw.rect(
                    self.surface,
                    wall_color,
                    (px, py, self.cell_size, self.cell_size),
                )
            return

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

    def _render_maze_cells(
        self,
        wall_block_img: Any,
        wall_color: tuple[int, int, int],
        line_width: int,
    ) -> None:
        """Iterate over maze grid and draw every cell's walls."""
        if self.maze is None:
            return
        for y, row in enumerate(self.maze.cells):
            for x, cell in enumerate(row):
                px = self.offset_x + x * self.cell_size
                py = self.offset_y + y * self.cell_size
                self._render_cell_walls(
                    cell, px, py, wall_block_img, wall_color, line_width
                )

    def _render_pellets(self) -> None:
        """Draw pacgums and super-pacgums in open corridors."""
        if self.level is None:
            return
        half = self.cell_size // 2
        dot_size = max(10, round(self.cell_size * 0.42))
        dot_img = self._get_scaled_image(
            os.path.join("assets", "images", "dot.png"),
            dot_size,
        )
        super_dot_size = max(16, round(self.cell_size * 0.78))
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

    def _render_to_surface(self) -> None:
        """Draw maze corridors, walls, and pellets to the Pygame surface."""
        if self.maze is None or self.surface is None:
            return

        surf_w = (
            self.surface.get_width()
            if hasattr(self.surface, "get_width")
            else 1600
        )
        surf_h = (
            self.surface.get_height()
            if hasattr(self.surface, "get_height")
            else 900
        )

        self._render_background(surf_w, surf_h)
        self._render_maze_backdrop()

        wall_color = (33, 33, 222)
        wall_block_img = self._get_scaled_image(
            os.path.join("assets", "images", "wall_block.png"),
            self.cell_size,
        )
        line_width = max(2, self.cell_size // 12)

        self._render_maze_cells(wall_block_img, wall_color, line_width)
        self._render_pellets()

    def shutdown(self) -> None:
        """Shut down the maze renderer."""
        self.background_asset = None
        self.is_initialized = False
        self._image_cache.clear()
        self._bg_cache.clear()
