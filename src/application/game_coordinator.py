"""Application coordinator for the Pac-Man game."""

from dataclasses import dataclass
from typing import Any

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

    def _handle_level_completion(self, level: Any) -> None:
        """Advance to next level or trigger victory if all levels cleared."""
        if not getattr(level, "completed", False):
            return

        if self.game_world.has_completed_all_levels():
            self.state_machine.transition_to(GameStateType.VICTORY)
            return

        next_level = self.game_world.advance_to_next_level()
        if next_level is None:
            self.state_machine.transition_to(GameStateType.VICTORY)
            return

        if hasattr(self.game_renderer, "set_level"):
            self.game_renderer.set_level(next_level)
        if self.gameplay_controller is not None:
            self.gameplay_controller.reset_level(next_level)

    def _check_game_over_conditions(self, level: Any) -> None:
        """Check if remaining lives or time limit triggered game over."""
        player = getattr(level, "player", None)
        if player is not None:
            lives = getattr(player, "lives", None)
            if isinstance(lives, (int, float)) and lives <= 0:
                self.state_machine.transition_to(GameStateType.GAME_OVER)
                return

        max_time = getattr(
            self.game_world.game_configuration, "level_max_time", 90
        )
        if (
            hasattr(level, "is_time_expired")
            and level.is_time_expired(max_time)
        ):
            self.state_machine.transition_to(GameStateType.GAME_OVER)

    def update(self, elapsed_seconds: float) -> None:
        """Update the active game state and world."""
        if elapsed_seconds < 0:
            raise ValueError("Elapsed time cannot be negative.")

        if self.state_machine.current_state is not GameStateType.PLAYING:
            return

        level = self.game_world.current_level
        if level is None:
            return

        if self.gameplay_controller is not None:
            self.gameplay_controller.update(level, elapsed_seconds)
        else:
            level.update_time(elapsed_seconds)

        self._handle_level_completion(level)
        self._check_game_over_conditions(level)

    def render(self) -> None:
        """Render the current application frame."""
        if not self.game_renderer.is_initialized:
            self.game_renderer.initialize()

        self.game_renderer.render()

    def shutdown(self) -> None:
        """Shut down the application presentation layer."""
        if self.game_renderer.is_initialized:
            self.game_renderer.shutdown()

    def _handle_menu_action(self, action: InputAction) -> bool:
        """Handle actions available during MENU state."""
        if action is InputAction.START_GAME:
            self.start_game()
            return True
        return False

    def _handle_playing_action(self, action: InputAction) -> bool:
        """Handle actions available during PLAYING state."""
        if action is InputAction.PAUSE_GAME:
            self.state_machine.transition_to(GameStateType.PAUSED)
            return True
        if self.gameplay_controller is not None:
            pc = self.gameplay_controller.player_controller
            pc.handle_action(action)
            return True
        return False

    def _handle_paused_action(self, action: InputAction) -> bool:
        """Handle actions available during PAUSED state."""
        if action is InputAction.PAUSE_GAME:
            self.state_machine.transition_to(GameStateType.PLAYING)
            return True
        return False

    def _handle_navigation_action(
        self,
        current_state: GameStateType,
        action: InputAction,
    ) -> bool:
        """Handle common state transitions like return-to-menu and restart."""
        nav_states = (
            GameStateType.PAUSED,
            GameStateType.GAME_OVER,
            GameStateType.VICTORY,
            GameStateType.ENTER_NAME,
        )
        if (
            current_state in nav_states
            and action is InputAction.RETURN_TO_MENU
        ):
            self.state_machine.transition_to(GameStateType.MENU)
            return True

        term_states = (GameStateType.GAME_OVER, GameStateType.VICTORY)
        if current_state in term_states and action is InputAction.START_GAME:
            self.state_machine.transition_to(GameStateType.ENTER_NAME)
            return True

        return False

    def handle_action(self, action: InputAction) -> None:
        """Handle a game input action."""
        if not isinstance(action, InputAction):
            raise TypeError("action must be an InputAction.")

        state = self.state_machine.current_state

        if state is GameStateType.MENU and self._handle_menu_action(action):
            return
        if (
            state is GameStateType.PLAYING
            and self._handle_playing_action(action)
        ):
            return
        if (
            state is GameStateType.PAUSED
            and self._handle_paused_action(action)
        ):
            return
        self._handle_navigation_action(state, action)
