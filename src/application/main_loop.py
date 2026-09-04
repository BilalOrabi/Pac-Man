"""Main application loop for the Pac-Man game."""

from dataclasses import dataclass

from src.application.game_coordinator import GameCoordinator
from src.input.input_event import InputAction


@dataclass
class MainGameLoop:
    """Run the main update cycle of the Pac-Man application."""

    game_coordinator: GameCoordinator
    is_running: bool = False

    def start(self) -> None:
        """Start the main game loop."""
        self.is_running = True

    def stop(self) -> None:
        """Stop the main game loop."""
        self.is_running = False

    def process_action(self, action: InputAction) -> None:
        """Send an input action to the game coordinator."""
        if not isinstance(action, InputAction):
            raise TypeError(
                "action must be an InputAction."
            )

        if not self.is_running:
            return

        if action is InputAction.QUIT_GAME:
            self.stop()
            return

        self.game_coordinator.handle_action(action)

    def update(self, elapsed_seconds: float) -> None:
        """Update the game while the loop is running."""
        if elapsed_seconds < 0:
            raise ValueError(
                "Elapsed time cannot be negative."
            )

        if not self.is_running:
            return

        self.game_coordinator.update(elapsed_seconds)

    def run_once(
        self,
        elapsed_seconds: float,
        action: InputAction | None = None,
    ) -> None:
        """Process one iteration of the main game loop."""
        if not self.is_running:
            return

        if action is not None:
            self.process_action(action)

        if self.is_running:
            self.update(elapsed_seconds)
