"""Integration tests for the Pac-Man ghost AI flow."""

from src.ai.ghost_ai import GhostAI
from src.ai.ghost_mode import GhostMode
from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.maze.maze import Maze, MazeCell, Wall


def create_open_maze(
    width: int = 5,
    height: int = 5,
) -> Maze:
    """Create a small maze with fully walkable cells."""
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


def create_ghost_ai() -> tuple[Ghost, GhostAI]:
    """Create a ghost and its AI controller."""
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(2, 2),
        home_position=(0, 0),
    )

    ghost_ai = GhostAI()

    return ghost, ghost_ai


def test_ghost_ai_chase_mode_produces_direction() -> None:
    """A ghost in chase mode should select a direction toward its target."""
    maze = create_open_maze()
    ghost, ghost_ai = create_ghost_ai()

    ghost_ai.set_mode(GhostMode.CHASE)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=ghost.position,
        target_position=(4, 2),
        home_position=ghost.home_position,
    )

    assert direction is Direction.RIGHT


def test_ghost_ai_flee_mode_produces_direction() -> None:
    """A ghost in flee mode should move away from its target."""
    maze = create_open_maze()
    ghost, ghost_ai = create_ghost_ai()

    ghost_ai.set_mode(GhostMode.FLEE)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=ghost.position,
        target_position=(0, 2),
        home_position=ghost.home_position,
    )

    assert direction is Direction.RIGHT


def test_ghost_ai_return_home_mode_produces_direction() -> None:
    """A ghost returning home should move toward its home position."""
    maze = create_open_maze()
    ghost, ghost_ai = create_ghost_ai()

    ghost_ai.set_mode(GhostMode.RETURN_HOME)

    direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=ghost.position,
        target_position=(4, 4),
        home_position=(0, 2),
    )

    assert direction is Direction.LEFT


def test_ghost_ai_mode_change_changes_behavior() -> None:
    """Changing the AI mode should change the decision source."""
    maze = create_open_maze()
    ghost, ghost_ai = create_ghost_ai()

    ghost_ai.set_mode(GhostMode.CHASE)

    chase_direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=ghost.position,
        target_position=(4, 2),
        home_position=ghost.home_position,
    )

    ghost_ai.set_mode(GhostMode.FLEE)

    flee_direction = ghost_ai.get_next_direction(
        maze=maze,
        ghost_position=ghost.position,
        target_position=(0, 2),
        home_position=ghost.home_position,
    )

    assert chase_direction is Direction.RIGHT
    assert flee_direction is Direction.RIGHT


def test_ghost_ai_reset_restores_initial_state() -> None:
    """Reset should restore chase mode and no current direction."""
    _, ghost_ai = create_ghost_ai()

    ghost_ai.set_mode(GhostMode.FLEE)
    ghost_ai.set_direction(Direction.LEFT)

    ghost_ai.reset()

    assert ghost_ai.get_current_mode() is GhostMode.CHASE
    assert ghost_ai.get_current_direction() is Direction.NONE
