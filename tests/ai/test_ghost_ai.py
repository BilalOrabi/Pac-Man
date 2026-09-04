"""Tests for the Pac-Man ghost AI controller."""

from src.ai.ghost_ai import GhostAI
from src.ai.ghost_mode import GhostMode
from src.entities.direction import Direction
from src.maze.maze import Maze, MazeCell, Wall


def create_open_maze(
    width: int = 5,
    height: int = 5,
) -> Maze:
    """Create a small maze with walkable cells."""
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


def test_ghost_ai_starts_in_chase_mode() -> None:
    """Ghost AI should start in CHASE mode."""
    ghost_ai = GhostAI()

    assert ghost_ai.get_current_mode() is GhostMode.CHASE
    assert ghost_ai.get_current_direction() is Direction.NONE


def test_ghost_ai_can_change_mode() -> None:
    """Ghost AI should allow its behavioral mode to be changed."""
    ghost_ai = GhostAI()

    ghost_ai.set_mode(GhostMode.FLEE)

    assert ghost_ai.get_current_mode() is GhostMode.FLEE


def test_ghost_ai_can_change_direction() -> None:
    """Ghost AI should store the current movement direction."""
    ghost_ai = GhostAI()

    ghost_ai.set_direction(Direction.LEFT)

    assert ghost_ai.get_current_direction() is Direction.LEFT


def test_ghost_ai_uses_chase_behavior() -> None:
    """Ghost AI should use ChaseBehavior in CHASE mode."""
    maze = create_open_maze()
    ghost_ai = GhostAI(current_mode=GhostMode.CHASE)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=(1, 2),
        target_position=(4, 2),
        home_position=(0, 0),
    )

    assert direction is Direction.RIGHT


def test_ghost_ai_uses_flee_behavior() -> None:
    """Ghost AI should use FleeBehavior in FLEE mode."""
    maze = create_open_maze()
    ghost_ai = GhostAI(current_mode=GhostMode.FLEE)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(1, 2),
        home_position=(0, 0),
    )

    assert direction is Direction.RIGHT


def test_ghost_ai_uses_return_home_behavior() -> None:
    """Ghost AI should use ReturnHomeBehavior in RETURN_HOME mode."""
    maze = create_open_maze()
    ghost_ai = GhostAI(current_mode=GhostMode.RETURN_HOME)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=(1, 2),
        target_position=(4, 4),
        home_position=(4, 2),
    )

    assert direction is Direction.RIGHT


def test_ghost_ai_changes_behavior_after_mode_change() -> None:
    """Changing mode should change the behavior used by the controller."""
    maze = create_open_maze()
    ghost_ai = GhostAI()

    chase_direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(4, 2),
        home_position=(0, 2),
    )

    ghost_ai.set_mode(GhostMode.FLEE)

    flee_direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=(2, 2),
        target_position=(4, 2),
        home_position=(0, 2),
    )

    assert chase_direction is Direction.RIGHT
    assert flee_direction is Direction.LEFT


def test_ghost_ai_reset_restores_initial_state() -> None:
    """Reset should restore CHASE mode and NONE direction."""
    ghost_ai = GhostAI(
        current_mode=GhostMode.FLEE,
        current_direction=Direction.UP,
    )

    ghost_ai.reset()

    assert ghost_ai.get_current_mode() is GhostMode.CHASE
    assert ghost_ai.get_current_direction() is Direction.NONE
