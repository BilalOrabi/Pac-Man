"""Application coordinator for the Pac-Man game."""

from dataclasses import dataclass

from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.world.game_world import GameWorld


@dataclass
class GameCoordinator:
    """Coordinate the game world, input system, and state machine."""

    game_world: GameWorld
    input_system: InputSystem
    state_machine: GameStateMachine

    def start_game(self) -> None:
        """Start a new Pac-Man game."""
        self.game_world.start()
        self.state_machine.transition_to(GameStateType.PLAYING)

    def update(self, elapsed_seconds: float) -> None:
        """Update the active game state and world."""
        if elapsed_seconds < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        current_state = self.state_machine.current_state

        if current_state is not GameStateType.PLAYING:
            return

        if self.game_world.current_level is not None:
            self.game_world.current_level.update_time(
                elapsed_seconds
            )

    def handle_action(self, action: InputAction) -> None:
        """Handle a game input action."""
        if not isinstance(action, InputAction):
            raise TypeError(
                "action must be an InputAction."
            )

        current_state = self.state_machine.current_state

        if (
            current_state is GameStateType.MENU
            and action is InputAction.START_GAME
        ):
            self.start_game()
            return

        if (
            current_state is GameStateType.PLAYING
            and action is InputAction.PAUSE_GAME
        ):
            self.state_machine.transition_to(
                GameStateType.PAUSED
            )
            return

        if (
            current_state is GameStateType.PAUSED
            and action is InputAction.PAUSE_GAME
        ):
            self.state_machine.transition_to(
                GameStateType.PLAYING
            )
