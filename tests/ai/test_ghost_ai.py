"""Tests for Pac-Man ghost AI."""

from unittest.mock import patch

from src.ai.chase import ChaseBehavior
from src.ai.flee import FleeBehavior
from src.ai.ghost_ai import GhostAI
from src.ai.ghost_mode import GhostMode
from src.ai.return_home import ReturnHomeBehavior
from src.entities.direction import Direction
from src.maze.maze import Maze


def create_mock_maze() -> Maze:
    """Create a maze object for mocked behavior tests."""
    return Maze(
        width=5,
        height=5,
        cells=tuple(),
        entry=(0, 0),
        exit=(4, 4),
        shortest_path="",
    )


def test_ghost_ai_starts_in_chase_mode() -> None:
    """Ghost AI should start in CHASE mode."""
    ghost_ai = GhostAI()

    assert ghost_ai.get_current_mode() is GhostMode.CHASE


def test_chase_mode_uses_chase_behavior() -> None:
    """CHASE mode should delegate direction calculation to ChaseBehavior."""
    ghost_ai = GhostAI()
    maze = create_mock_maze()

    with patch.object(
        ChaseBehavior,
        "get_direction_toward_target",
        return_value=Direction.RIGHT,
    ) as mocked_chase:
        direction = ghost_ai.get_next_direction(
            maze=maze,
            ghost_position=(1, 1),
            target_position=(4, 1),
            home_position=(2, 2),
        )

    assert direction is Direction.RIGHT
    mocked_chase.assert_called_once_with(
        maze=maze,
        ghost_position=(1, 1),
        target_position=(4, 1),
    )


def test_flee_mode_uses_flee_behavior() -> None:
    """FLEE mode should delegate direction calculation to FleeBehavior."""
    ghost_ai = GhostAI()
    ghost_ai.set_mode(GhostMode.FLEE)

    maze = create_mock_maze()

    with patch.object(
        FleeBehavior,
        "get_direction_away_from_target",
        return_value=Direction.LEFT,
    ) as mocked_flee:
        direction = ghost_ai.get_next_direction(
            maze=maze,
            ghost_position=(3, 1),
            target_position=(4, 1),
            home_position=(2, 2),
        )

    assert direction is Direction.LEFT
    mocked_flee.assert_called_once_with(
        maze=maze,
        ghost_position=(3, 1),
        target_position=(4, 1),
    )


def test_return_home_mode_uses_return_home_behavior() -> None:
    """RETURN_HOME should delegate to ReturnHomeBehavior."""
    ghost_ai = GhostAI()
    ghost_ai.set_mode(GhostMode.RETURN_HOME)

    maze = create_mock_maze()

    with patch.object(
        ReturnHomeBehavior,
        "get_direction_toward_home",
        return_value=Direction.UP,
    ) as mocked_return_home:
        direction = ghost_ai.get_next_direction(
            maze=maze,
            ghost_position=(2, 3),
            target_position=(4, 4),
            home_position=(2, 0),
        )

    assert direction is Direction.UP
    mocked_return_home.assert_called_once_with(
        maze=maze,
        ghost_position=(2, 3),
        home_position=(2, 0),
    )


def test_set_mode_changes_current_mode() -> None:
    """Setting a mode should update the ghost's current mode."""
    ghost_ai = GhostAI()

    ghost_ai.set_mode(GhostMode.FLEE)

    assert ghost_ai.get_current_mode() is GhostMode.FLEE


def test_set_direction_changes_current_direction() -> None:
    """Setting a direction should update the ghost's current direction."""
    ghost_ai = GhostAI()

    ghost_ai.set_direction(Direction.LEFT)

    assert ghost_ai.get_current_direction() is Direction.LEFT


def test_reset_restores_initial_state() -> None:
    """Reset should restore CHASE mode and no direction."""
    ghost_ai = GhostAI()

    ghost_ai.set_mode(GhostMode.RETURN_HOME)
    ghost_ai.set_direction(Direction.DOWN)

    ghost_ai.reset()

    assert ghost_ai.get_current_mode() is GhostMode.CHASE
    assert ghost_ai.get_current_direction() is Direction.NONE
