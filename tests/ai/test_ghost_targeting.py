"""Tests for individual ghost chase targeting personalities."""

from src.ai.ghost_targeting import GhostTargeting
from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.entities.player import Player
from src.maze.maze import Maze, MazeCell, Wall


def create_test_maze(width: int = 20, height: int = 20) -> Maze:
    """Create a rectangular maze for boundary clamping tests."""
    cells = tuple(
        tuple(
            MazeCell(
                position=(x, y),
                walls=Wall.NONE,
                is_solid_block=False,
            )
            for x in range(width)
        )
        for y in range(height)
    )
    return Maze(
        width=width,
        height=height,
        cells=cells,
        entry=(0, 0),
        exit=(width - 1, height - 1),
        shortest_path="",
    )


def test_blinky_targets_player_directly() -> None:
    """Blinky should target Pac-Man's exact grid cell."""
    blinky = Ghost(
        position=(1, 1),
        ghost_type=GhostType.RED,
        home_position=(1, 1),
    )
    player = Player(position=(10, 12), direction=Direction.RIGHT)

    target = GhostTargeting.get_chase_target(blinky, player)
    assert target == (10, 12)


def test_pinky_targets_four_tiles_ahead() -> None:
    """Pinky should target 4 tiles ahead of Pac-Man's direction."""
    pinky = Ghost(
        position=(18, 1),
        ghost_type=GhostType.PINK,
        home_position=(18, 1),
    )
    maze = create_test_maze(25, 25)

    player_up = Player(position=(10, 10), direction=Direction.UP)
    assert GhostTargeting.get_chase_target(
        pinky, player_up, maze=maze
    ) == (10, 6)

    player_down = Player(position=(10, 10), direction=Direction.DOWN)
    assert GhostTargeting.get_chase_target(
        pinky, player_down, maze=maze
    ) == (10, 14)

    player_left = Player(position=(10, 10), direction=Direction.LEFT)
    assert GhostTargeting.get_chase_target(
        pinky, player_left, maze=maze
    ) == (6, 10)

    player_right = Player(position=(10, 10), direction=Direction.RIGHT)
    assert GhostTargeting.get_chase_target(
        pinky, player_right, maze=maze
    ) == (14, 10)

    player_none = Player(position=(10, 10), direction=Direction.NONE)
    assert GhostTargeting.get_chase_target(
        pinky, player_none, maze=maze
    ) == (10, 10)


def test_pinky_clamps_to_maze_boundaries() -> None:
    """Pinky targeting should clamp inside maze dimensions."""
    pinky = Ghost(
        position=(0, 0),
        ghost_type=GhostType.PINK,
        home_position=(0, 0),
    )
    maze = create_test_maze(15, 15)

    player_near_top = Player(position=(5, 1), direction=Direction.UP)
    assert GhostTargeting.get_chase_target(
        pinky, player_near_top, maze=maze
    ) == (5, 0)

    player_near_right = Player(position=(13, 5), direction=Direction.RIGHT)
    assert GhostTargeting.get_chase_target(
        pinky, player_near_right, maze=maze
    ) == (14, 5)


def test_inky_flanks_using_pivot_and_blinky() -> None:
    """Inky should double the vector from Blinky to the 2-tile pivot."""
    inky = Ghost(
        position=(1, 18),
        ghost_type=GhostType.BLUE,
        home_position=(1, 18),
    )
    blinky = Ghost(
        position=(8, 6),
        ghost_type=GhostType.RED,
        home_position=(18, 1),
    )
    player = Player(position=(10, 10), direction=Direction.RIGHT)
    maze = create_test_maze(30, 30)

    target = GhostTargeting.get_chase_target(
        inky, player, ghosts=[blinky, inky], maze=maze
    )
    assert target == (16, 14)


def test_inky_fallback_when_blinky_absent() -> None:
    """Inky should fall back to the pivot tile if Blinky is absent."""
    inky = Ghost(
        position=(1, 18),
        ghost_type=GhostType.BLUE,
        home_position=(1, 18),
    )
    player = Player(position=(10, 10), direction=Direction.DOWN)
    maze = create_test_maze(30, 30)

    target = GhostTargeting.get_chase_target(
        inky, player, ghosts=[], maze=maze
    )
    assert target == (10, 12)


def test_clyde_chases_when_farther_than_eight_tiles() -> None:
    """Clyde should chase Pac-Man when farther than 8 tiles away."""
    clyde = Ghost(
        position=(0, 0),
        ghost_type=GhostType.ORANGE,
        home_position=(0, 0),
    )
    player = Player(position=(10, 10), direction=Direction.NONE)

    target = GhostTargeting.get_chase_target(clyde, player)
    assert target == (10, 10)


def test_clyde_retreats_when_within_eight_tiles() -> None:
    """Clyde should retreat to home corner when within 8 tiles."""
    clyde = Ghost(
        position=(10, 8),
        ghost_type=GhostType.ORANGE,
        home_position=(2, 2),
    )
    player = Player(position=(10, 10), direction=Direction.NONE)

    target = GhostTargeting.get_chase_target(clyde, player)
    assert target == (2, 2)


def test_clyde_retreats_at_exact_boundary_of_eight_tiles() -> None:
    """Clyde should retreat to home corner at exactly 8 tiles distance."""
    clyde = Ghost(
        position=(10, 2),
        ghost_type=GhostType.ORANGE,
        home_position=(1, 1),
    )
    player = Player(position=(10, 10), direction=Direction.NONE)

    target = GhostTargeting.get_chase_target(clyde, player)
    assert target == (1, 1)
