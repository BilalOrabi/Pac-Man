"""Tests for the Pac-Man ghost controller."""

from unittest.mock import Mock

from src.controllers.ghost_controller import GhostController
from src.entities.direction import Direction
from src.entities.ghost import Ghost, GhostType
from src.maze.maze import Maze
from src.systems.collision import CollisionSystem


def test_update_moves_ghost_through_collision_system() -> None:
    """Updating the controller should validate the ghost's next position."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.RIGHT
    ghost.position = (1, 1)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (2, 1),
        maze,
    )


def test_update_with_no_direction_keeps_ghost_in_place() -> None:
    """A ghost with no direction should remain in its current position."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.NONE
    ghost.position = (2, 3)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (2, 3),
        maze,
    )


def test_update_does_not_move_ghost_outside_maze() -> None:
    """The movement system should keep an out-of-bounds ghost in place."""
    ghost = Mock(spec=Ghost)
    ghost.direction = Direction.LEFT
    ghost.position = (0, 1)

    collision_system = Mock(spec=CollisionSystem)

    maze = Mock(spec=Maze)
    maze.is_inside.return_value = False

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
    )

    controller.update(maze)

    collision_system.move_if_valid.assert_called_once_with(
        ghost,
        (0, 1),
        maze,
    )


def test_prepare_next_step_sets_target_position() -> None:
    """prepare_next_step should evaluate AI and assign target_position."""
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(1, 1),
        home_position=(0, 0),
    )
    collision_system = CollisionSystem()
    ai = Mock()
    ai.get_next_direction.return_value = Direction.RIGHT
    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True
    maze.can_move.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
        ai=ai,
    )

    controller.prepare_next_step(maze, (5, 5))

    assert ghost.direction is Direction.RIGHT
    assert ghost.target_position == (2, 1)
    assert ghost.movement_progress == 0.0


def test_ghost_arriving_at_home_position_respawns_to_chase() -> None:
    """Ghost returning home should immediately transition to CHASE at home."""
    from src.entities.ghost import GhostState
    ghost = Ghost(
        ghost_type=GhostType.RED,
        position=(1, 0),
        home_position=(0, 0),
        state=GhostState.RETURN_HOME,
        target_position=(0, 0),
    )
    collision_system = CollisionSystem()
    ai = Mock()
    ai.get_next_direction.return_value = Direction.RIGHT
    maze = Mock(spec=Maze)
    maze.is_inside.return_value = True
    maze.can_move.return_value = True

    controller = GhostController(
        ghost=ghost,
        collision_system=collision_system,
        ai=ai,
    )

    controller.update(maze, target_position=(5, 5))

    assert ghost.position == (0, 0)
    assert ghost.state is GhostState.RETURN_HOME
    assert ghost.respawn_cooldown == 5.0
