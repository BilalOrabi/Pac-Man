"""Application coordinator for the Pac-Man game."""

from dataclasses import dataclass

from src.cheat.cheat_system import CheatSystem
from src.controllers.gameplay_controller import GameplayController
from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.rendering.game_renderer import GameRenderer
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.world.game_world import GameWorld


@dataclass
class GameCoordinator:
    """Coordinate the game world, input, state machine, and rendering."""

    game_world: GameWorld
    input_system: InputSystem
    state_machine: GameStateMachine
    game_renderer: GameRenderer
    gameplay_controller: GameplayController | None = None
    cheat_system: CheatSystem | None = None

    def start_game(self) -> None:
        """Start a new Pac-Man game."""
        level = self.game_world.start()

        if not self.game_renderer.is_initialized:
            self.game_renderer.initialize()

        if hasattr(self.game_renderer, "set_level") and level is not None:
            self.game_renderer.set_level(level)

        if self.gameplay_controller is not None and level is not None:
            self.gameplay_controller.reset_level(level)

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

        level = self.game_world.current_level
        if level is None:
            return

        if self.gameplay_controller is not None:
            self.gameplay_controller.update(level, elapsed_seconds)
        else:
            level.update_time(elapsed_seconds)

        # Check level completion
        if getattr(level, "completed", False):
            if self.game_world.has_completed_all_levels():
                self.state_machine.transition_to(GameStateType.VICTORY)
            else:
                next_level = self.game_world.advance_to_next_level()
                if next_level is None:
                    self.state_machine.transition_to(GameStateType.VICTORY)
                else:
                    if hasattr(self.game_renderer, "set_level"):
                        self.game_renderer.set_level(next_level)
                    if self.gameplay_controller is not None:
                        self.gameplay_controller.reset_level(next_level)

        # Check lives for game over
        player = getattr(level, "player", None)
        if player is not None:
            lives = getattr(player, "lives", None)
            if isinstance(lives, (int, float)) and lives <= 0:
                self.state_machine.transition_to(GameStateType.GAME_OVER)

        # Check time expiration
        max_time = getattr(
            self.game_world.game_configuration, "level_max_time", 90
        )
        if (
            hasattr(level, "is_time_expired")
            and level.is_time_expired(max_time)
        ):
            self.state_machine.transition_to(GameStateType.GAME_OVER)

    def render(self) -> None:
        """Render the current application frame."""
        if not self.game_renderer.is_initialized:
            self.game_renderer.initialize()

        self.game_renderer.render()

    def shutdown(self) -> None:
        """Shut down the application presentation layer."""
        if self.game_renderer.is_initialized:
            self.game_renderer.shutdown()

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

        if current_state is GameStateType.PLAYING:
            if action is InputAction.PAUSE_GAME:
                self.state_machine.transition_to(
                    GameStateType.PAUSED
                )
                return
            if self.gameplay_controller is not None:
                pc = self.gameplay_controller.player_controller
                pc.handle_action(action)
            return

        if (
            current_state is GameStateType.PAUSED
            and action is InputAction.PAUSE_GAME
        ):
            self.state_machine.transition_to(
                GameStateType.PLAYING
            )
            return

        if (
            current_state in (
                GameStateType.PAUSED,
                GameStateType.GAME_OVER,
                GameStateType.VICTORY,
                GameStateType.ENTER_NAME,
            )
            and action is InputAction.RETURN_TO_MENU
        ):
            self.state_machine.transition_to(
                GameStateType.MENU
            )
            return

        if (
            current_state in (GameStateType.GAME_OVER, GameStateType.VICTORY)
            and action is InputAction.START_GAME
        ):
            self.state_machine.transition_to(
                GameStateType.ENTER_NAME
            )
            return
