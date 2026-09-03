"""Tests for the Level domain model."""

import pytest

from src.config.game_config import LevelConfig
from src.maze.maze import Maze, MazeCell, Wall
from src.world.level import Level


def create_test_maze() -> Maze:
    """Create a small maze for level tests."""
    cells = (
        (
            MazeCell(
                position=(0, 0),
                walls=Wall.NORTH | Wall.WEST,
                is_solid_block=False,
            ),
            MazeCell(
                position=(1, 0),
                walls=Wall.NORTH | Wall.EAST,
                is_solid_block=False,
            ),
        ),
        (
            MazeCell(
                position=(0, 1),
                walls=Wall.SOUTH | Wall.WEST,
                is_solid_block=False,
            ),
            MazeCell(
                position=(1, 1),
                walls=Wall.ALL,
                is_solid_block=True,
            ),
        ),
    )

    return Maze(
        width=2,
        height=2,
        cells=cells,
        entry=(0, 0),
        exit=(1, 0),
        shortest_path="E",
    )


def create_test_level() -> Level:
    """Create a level with predictable test data."""
    return Level(
        number=1,
        configuration=LevelConfig(width=2, height=2),
        maze=create_test_maze(),
        remaining_pacgums=3,
    )


def test_level_stores_initial_state() -> None:
    """Level should store its initial runtime state."""
    level = create_test_level()

    assert level.number == 1
    assert level.configuration.width == 2
    assert level.configuration.height == 2
    assert level.remaining_pacgums == 3
    assert level.elapsed_level_time == 0.0
    assert not level.completed


def test_update_time_advances_level_timer() -> None:
    """Level should increase its elapsed time."""
    level = create_test_level()

    level.update_time(2.5)

    assert level.elapsed_level_time == 2.5


def test_update_time_accumulates_elapsed_time() -> None:
    """Multiple time updates should accumulate."""
    level = create_test_level()

    level.update_time(1.5)
    level.update_time(2.0)

    assert level.elapsed_level_time == 3.5


def test_update_time_rejects_negative_time() -> None:
    """Level should reject negative elapsed time."""
    level = create_test_level()

    with pytest.raises(ValueError):
        level.update_time(-1.0)


def test_completed_level_does_not_continue_timer() -> None:
    """Completed levels should not continue accumulating time."""
    level = create_test_level()

    level.completed = True
    level.update_time(5.0)

    assert level.elapsed_level_time == 0.0


def test_consume_pacgum_decreases_remaining_count() -> None:
    """Consuming a pacgum should decrease the remaining count."""
    level = create_test_level()

    level.consume_pacgum()

    assert level.remaining_pacgums == 2
    assert not level.completed


def test_consuming_last_pacgum_completes_level() -> None:
    """Consuming the final pacgum should complete the level."""
    level = create_test_level()

    level.remaining_pacgums = 1

    level.consume_pacgum()

    assert level.remaining_pacgums == 0
    assert level.completed


def test_consume_pacgum_does_nothing_when_none_remain() -> None:
    """Consuming a pacgum should do nothing when none remain."""
    level = create_test_level()

    level.remaining_pacgums = 0
    level.consume_pacgum()

    assert level.remaining_pacgums == 0
    assert not level.completed


def test_is_time_expired_returns_false_before_limit() -> None:
    """Level should not expire before reaching its time limit."""
    level = create_test_level()

    level.update_time(10.0)

    assert not level.is_time_expired(90.0)


def test_is_time_expired_returns_true_at_limit() -> None:
    """Level should expire when its time limit is reached."""
    level = create_test_level()

    level.update_time(90.0)

    assert level.is_time_expired(90.0)


def test_is_time_expired_rejects_invalid_limit() -> None:
    """Level should reject a non-positive time limit."""
    level = create_test_level()

    with pytest.raises(ValueError):
        level.is_time_expired(0.0)


def test_reset_timer_sets_elapsed_time_to_zero() -> None:
    """Resetting the timer should clear elapsed level time."""
    level = create_test_level()

    level.update_time(15.0)
    level.reset_timer()

    assert level.elapsed_level_time == 0.0
