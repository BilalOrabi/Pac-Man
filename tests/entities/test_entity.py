"""Tests for the base Entity class."""

from src.entities.direction import Direction
from src.entities.entity import Entity


def test_entity_has_default_direction_and_speed() -> None:
    """Entity should start without movement by default."""
    entity = Entity(position=(5, 7))

    assert entity.position == (5, 7)
    assert entity.direction is Direction.NONE
    assert entity.speed == 0.0


def test_entity_accepts_initial_direction() -> None:
    """Entity should accept an initial movement direction."""
    entity = Entity(
        position=(5, 7),
        direction=Direction.UP,
        speed=2.5,
    )

    assert entity.direction is Direction.UP
    assert entity.speed == 2.5


def test_set_direction_changes_entity_direction() -> None:
    """set_direction should update the current direction."""
    entity = Entity(position=(5, 7))

    entity.set_direction(Direction.RIGHT)

    assert entity.direction is Direction.RIGHT


def test_stop_resets_direction_to_none() -> None:
    """stop should remove the entity's current movement direction."""
    entity = Entity(
        position=(5, 7),
        direction=Direction.LEFT,
        speed=2.5,
    )

    entity.stop()

    assert entity.direction is Direction.NONE
