"""Tests for the level timer system."""

import pytest

from src.config.game_config import LevelConfig
from src.entities.ghost import Ghost, GhostType
from src.entities.player import Player
from src.maze.maze import Maze, MazeCell, Wall
from src.systems.timer_system import TimerSystem
from src.world.level import Level


def create_test_level() -> Level:
    """Create a minimal level for timer tests."""
    cell = MazeCell(
        position=(0, 0),
        walls=Wall.ALL,
        is_solid_block=False,
    )

    maze = Maze(
        width=1,
        height=1,
        cells=((cell,),),
        entry=(0, 0),
        exit=(0, 0),
        shortest_path="",
    )

    return Level(
        number=1,
        configuration=LevelConfig(
            width=19,
            height=21,
        ),
        maze=maze,
        remaining_pacgums=10,
        player=Player(
            position=maze.entry,
            speed=5.0,
            lives=3,
        ),
        ghosts=[
            Ghost(
                position=maze.entry,
                ghost_type=GhostType.RED,
                home_position=maze.entry,
                speed=4.0,
            )
        ],
    )


def test_timer_updates_level_elapsed_time() -> None:
    """Timer should increase the level's elapsed time."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 5.5)

    assert level.elapsed_level_time == 5.5


def test_timer_accumulates_multiple_updates() -> None:
    """Timer should accumulate elapsed time across updates."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 10)
    timer_system.update(level, 15.5)

    assert level.elapsed_level_time == 25.5


def test_timer_reports_not_expired_before_time_limit() -> None:
    """Timer should report false before the time limit is reached."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 89.9)

    assert not timer_system.is_expired(level)


def test_timer_reports_expired_at_time_limit() -> None:
    """Timer should report true when the time limit is reached."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 90)

    assert timer_system.is_expired(level)


def test_timer_reports_expired_after_time_limit() -> None:
    """Timer should report true after exceeding the time limit."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 100)

    assert timer_system.is_expired(level)


def test_timer_reset_clears_elapsed_time() -> None:
    """Reset should return the level timer to zero."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    timer_system.update(level, 30)
    timer_system.reset(level)

    assert level.elapsed_level_time == 0.0
    assert not timer_system.is_expired(level)


def test_timer_rejects_negative_elapsed_time() -> None:
    """Timer should reject negative elapsed time."""
    level = create_test_level()
    timer_system = TimerSystem(maximum_level_time=90)

    with pytest.raises(
        ValueError,
        match="Elapsed time cannot be negative",
    ):
        timer_system.update(level, -1)


def test_timer_rejects_invalid_maximum_time() -> None:
    """Timer should reject a non-positive maximum level time."""
    with pytest.raises(
        ValueError,
        match="Maximum level time must be greater than zero",
    ):
        TimerSystem(maximum_level_time=0)
