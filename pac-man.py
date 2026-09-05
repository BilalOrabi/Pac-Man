"""Main entry point for the Pac-Man game."""

import os
import sys

import pygame

from src.ai.ghost_ai import GhostAI
from src.application.game_coordinator import GameCoordinator
from src.application.main_loop import MainGameLoop
from src.cheat.cheat_system import CheatSystem
from src.config.config_loader import ConfigError, ConfigLoader
from src.config.game_config import GameConfig
from src.controllers.gameplay_controller import GameplayController
from src.controllers.ghost_controller import GhostController
from src.controllers.player_controller import PlayerController
from src.highscore.highscore_manager import HighscoreEntry, HighscoreManager
from src.input.input_event import InputAction
from src.input.input_system import InputSystem
from src.maze.adapter import MazeAdapter
from src.persistence.persistence_manager import PersistenceManager
from src.rendering.game_renderer import GameRenderer
from src.rendering.ghost_renderer import GhostRenderer
from src.rendering.maze_renderer import MazeRenderer
from src.rendering.player_renderer import PlayerRenderer
from src.rendering.ui_renderer import UIRenderer
from src.states.game_state import GameStateType
from src.states.state_machine import GameStateMachine
from src.systems.collision import CollisionSystem
from src.systems.lives import LivesSystem
from src.systems.power_mode import PowerModeSystem
from src.systems.scoring import ScoringSystem
from src.systems.timer_system import TimerSystem
from src.theme.asset_manager import AssetManager
from src.theme.assets import AssetPaths
from src.utils.error_logger import ErrorLogger
from src.world.game_world import GameWorld
from src.world.level import Level
from src.world.level_factory import LevelFactory

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


def load_persistent_highscores(
    persistence_manager: PersistenceManager,
) -> HighscoreManager:
    """Load high-score leaderboard from disk safely."""
    try:
        data = persistence_manager.load_data()
        entries: list[HighscoreEntry] = []
        for item in data.get("highscores", []):
            if (
                isinstance(item, dict)
                and "player_name" in item
                and "score" in item
            ):
                entries.append(
                    HighscoreEntry(
                        player_name=str(item["player_name"]),
                        score=int(item["score"]),
                    )
                )
        return HighscoreManager(entries=entries)
    except Exception:
        return HighscoreManager()


def save_persistent_highscores(
    persistence_manager: PersistenceManager,
    highscore_manager: HighscoreManager,
) -> None:
    """Save high-score leaderboard to disk."""
    try:
        data = {
            "highscores": [
                {"player_name": e.player_name, "score": e.score}
                for e in highscore_manager.entries
            ]
        }
        persistence_manager.save_data(data)
    except Exception as exc:
        print(f"Warning: Could not save highscores: {exc}", file=sys.stderr)


def _build_renderers(
    asset_manager: AssetManager,
    initial_level: Level,
    highscore_mgr: HighscoreManager,
) -> tuple[GameRenderer, UIRenderer]:
    """Construct and configure all graphics renderers."""
    maze_renderer = MazeRenderer(asset_manager=asset_manager)
    player_renderer = PlayerRenderer(asset_manager=asset_manager)
    ghost_renderers = [
        GhostRenderer(asset_manager=asset_manager)
        for _ in range(len(initial_level.ghosts))
    ]
    ui_renderer = UIRenderer(asset_manager=asset_manager)
    ui_renderer.game_state_name = "MENU"
    ui_renderer.highscores = [
        {"name": e.player_name, "score": e.score}
        for e in highscore_mgr.entries
    ]

    game_renderer = GameRenderer(
        maze_renderer=maze_renderer,
        player_renderer=player_renderer,
        ghost_renderers=ghost_renderers,
        ui_renderer=ui_renderer,
    )
    game_renderer.initialize()
    game_renderer.set_level(initial_level)
    return game_renderer, ui_renderer


def build_game_systems(
    config: GameConfig,
) -> tuple[
    GameWorld,
    GameCoordinator,
    MainGameLoop,
    UIRenderer,
    CheatSystem,
    HighscoreManager,
    PersistenceManager,
]:
    """Build and wire all game dependencies."""
    persistence = PersistenceManager("highscores.json")
    highscore_mgr = load_persistent_highscores(persistence)

    bg_asset = (
        "assets/images/background.jpg"
        if os.path.exists("assets/images/background.jpg")
        else "assets/images/background.png"
    )
    asset_paths = AssetPaths(background=bg_asset)
    asset_manager = AssetManager(assets=asset_paths)
    asset_manager.initialize()

    maze_adapter = MazeAdapter()
    level_factory = LevelFactory(
        maze_adapter=maze_adapter,
        game_configuration=config,
    )
    game_world = GameWorld(
        game_configuration=config,
        level_factory=level_factory,
    )
    initial_level = game_world.start()

    collision_system = CollisionSystem()
    player_controller = PlayerController(
        player=initial_level.player,
        collision_system=collision_system,
    )

    ghost_ai = GhostAI()
    ghost_controllers = [
        GhostController(
            ghost=g,
            collision_system=collision_system,
            ai=ghost_ai,
        )
        for g in initial_level.ghosts
    ]

    lives_system = LivesSystem(starting_lives=config.lives)
    scoring_system = ScoringSystem(
        points_per_pacgum=config.points_per_pacgum,
        points_per_super_pacgum=config.points_per_pacgum * 5,
        points_per_ghost=200,
    )
    power_mode_system = PowerModeSystem(
        duration=config.power_mode_duration,
    )
    timer_system = TimerSystem(maximum_level_time=config.level_max_time)
    cheat_system = CheatSystem()

    gameplay_controller = GameplayController(
        player_controller=player_controller,
        ghost_controllers=ghost_controllers,
        lives_system=lives_system,
        scoring_system=scoring_system,
        power_mode_system=power_mode_system,
        timer_system=timer_system,
        cheat_system=cheat_system,
    )

    game_renderer, ui_renderer = _build_renderers(
        asset_manager, initial_level, highscore_mgr
    )

    state_machine = GameStateMachine()
    input_system = InputSystem()

    game_coordinator = GameCoordinator(
        game_world=game_world,
        input_system=input_system,
        state_machine=state_machine,
        game_renderer=game_renderer,
        gameplay_controller=gameplay_controller,
        cheat_system=cheat_system,
    )

    main_loop = MainGameLoop(game_coordinator=game_coordinator)
    main_loop.start()

    return (
        game_world,
        game_coordinator,
        main_loop,
        ui_renderer,
        cheat_system,
        highscore_mgr,
        persistence,
    )


def _handle_enter_name_key(
    event: pygame.event.Event,
    coordinator: GameCoordinator,
    ui_renderer: UIRenderer,
    highscore_mgr: HighscoreManager,
    persistence: PersistenceManager,
) -> None:
    """Handle keyboard interaction in ENTER_NAME state."""
    if event.key == pygame.K_RETURN:
        name = ui_renderer.name_input.strip() or "PACMAN"
        if HighscoreManager.validate_player_name(name):
            highscore_mgr.add_score(name, ui_renderer.score)
            save_persistent_highscores(persistence, highscore_mgr)
            ui_renderer.highscores = [
                {"name": e.player_name, "score": e.score}
                for e in highscore_mgr.entries
            ]
        ui_renderer.name_input = ""
        coordinator.state_machine.transition_to(GameStateType.MENU)
    elif event.key == pygame.K_ESCAPE:
        ui_renderer.name_input = ""
        coordinator.state_machine.transition_to(GameStateType.MENU)
    elif event.key == pygame.K_BACKSPACE:
        ui_renderer.name_input = ui_renderer.name_input[:-1]
    else:
        char = event.unicode
        if len(ui_renderer.name_input) < 10 and (
            char.isalnum() or char == " "
        ):
            ui_renderer.name_input += char


def _handle_menu_key(
    event: pygame.event.Event,
    coordinator: GameCoordinator,
    main_loop: MainGameLoop,
    ui_renderer: UIRenderer,
) -> None:
    """Handle keyboard interaction in MENU state."""
    if ui_renderer.menu_view != "main":
        if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            ui_renderer.menu_view = "main"
        return

    if event.key == pygame.K_UP:
        ui_renderer.menu_selection = (ui_renderer.menu_selection - 1) % 4
    elif event.key == pygame.K_DOWN:
        ui_renderer.menu_selection = (ui_renderer.menu_selection + 1) % 4
    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
        if ui_renderer.menu_selection == 0:
            coordinator.start_game()
        elif ui_renderer.menu_selection == 1:
            ui_renderer.menu_view = "highscores"
        elif ui_renderer.menu_selection == 2:
            ui_renderer.menu_view = "instructions"
        elif ui_renderer.menu_selection == 3:
            main_loop.stop()
    elif event.key == pygame.K_1:
        coordinator.start_game()
    elif event.key == pygame.K_2:
        ui_renderer.menu_view = "highscores"
    elif event.key == pygame.K_3:
        ui_renderer.menu_view = "instructions"
    elif event.key in (pygame.K_4, pygame.K_ESCAPE):
        main_loop.stop()


def _handle_playing_key(
    event: pygame.event.Event,
    coordinator: GameCoordinator,
    main_loop: MainGameLoop,
    cheat_system: CheatSystem,
) -> None:
    """Handle keyboard interaction in PLAYING state."""
    if event.key == pygame.K_1:
        cheat_system.toggle_invincibility()
        return
    if event.key == pygame.K_2:
        cheat_system.toggle_ghost_freeze()
        return
    if event.key == pygame.K_3:
        cheat_system.toggle_speed_boost()
        return
    if event.key == pygame.K_4:
        level = coordinator.game_world.current_level
        if level and level.player:
            level.player.lives += 1
        return
    if event.key == pygame.K_5:
        cheat_system.trigger_level_skip()
        return

    movement_map = {
        pygame.K_UP: InputAction.MOVE_UP,
        pygame.K_w: InputAction.MOVE_UP,
        pygame.K_DOWN: InputAction.MOVE_DOWN,
        pygame.K_s: InputAction.MOVE_DOWN,
        pygame.K_LEFT: InputAction.MOVE_LEFT,
        pygame.K_a: InputAction.MOVE_LEFT,
        pygame.K_RIGHT: InputAction.MOVE_RIGHT,
        pygame.K_d: InputAction.MOVE_RIGHT,
        pygame.K_p: InputAction.PAUSE_GAME,
        pygame.K_ESCAPE: InputAction.PAUSE_GAME,
    }
    action = movement_map.get(event.key)
    if action is not None:
        main_loop.process_action(action)


def handle_key_events(
    event: pygame.event.Event,
    coordinator: GameCoordinator,
    main_loop: MainGameLoop,
    ui_renderer: UIRenderer,
    cheat_system: CheatSystem,
    highscore_mgr: HighscoreManager,
    persistence: PersistenceManager,
) -> None:
    """Handle keyboard interaction based on current game state."""
    state = coordinator.state_machine.current_state

    if state is GameStateType.ENTER_NAME:
        _handle_enter_name_key(
            event, coordinator, ui_renderer, highscore_mgr, persistence
        )
    elif state is GameStateType.MENU:
        _handle_menu_key(event, coordinator, main_loop, ui_renderer)
    elif state is GameStateType.PLAYING:
        _handle_playing_key(event, coordinator, main_loop, cheat_system)
    elif state is GameStateType.PAUSED:
        if event.key in (pygame.K_p, pygame.K_ESCAPE):
            main_loop.process_action(InputAction.PAUSE_GAME)
        elif event.key == pygame.K_m:
            main_loop.process_action(InputAction.RETURN_TO_MENU)
    elif state in (GameStateType.GAME_OVER, GameStateType.VICTORY):
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            main_loop.process_action(InputAction.START_GAME)
        elif event.key == pygame.K_ESCAPE:
            main_loop.process_action(InputAction.RETURN_TO_MENU)


def _collect_active_cheats(cheat_system: CheatSystem) -> list[str]:
    """Collect active cheat mode display tags."""
    active: list[str] = []
    if cheat_system.is_invincible:
        active.append("INVINCIBLE")
    if cheat_system.is_ghosts_frozen:
        active.append("FROZEN")
    if cheat_system.is_speed_boosted:
        active.append("SPEED")
    if cheat_system.is_power_mode_enabled:
        active.append("POWER")
    return active


def sync_ui(
    ui_renderer: UIRenderer,
    coordinator: GameCoordinator,
    cheat_system: CheatSystem,
    config: GameConfig,
) -> None:
    """Synchronize UI renderer state with current game telemetry."""
    ui_renderer.game_state_name = (
        coordinator.state_machine.current_state.name
    )
    level = coordinator.game_world.current_level
    if level and level.player:
        ui_renderer.score = level.player.score
        ui_renderer.lives = level.player.lives
        ui_renderer.level_number = level.number
        rem = max(0.0, config.level_max_time - level.elapsed_level_time)
        ui_renderer.time_remaining = rem

    ui_renderer.active_cheats = _collect_active_cheats(cheat_system)

    cur_state = coordinator.state_machine.current_state
    if cur_state is GameStateType.VICTORY:
        ui_renderer.last_outcome = "victory"
    elif cur_state is GameStateType.GAME_OVER:
        ui_renderer.last_outcome = "game_over"


def run_game(config: GameConfig) -> None:
    """Initialize Pygame presentation and run the 60 FPS loop."""
    (
        game_world,
        coordinator,
        main_loop,
        ui_renderer,
        cheat_system,
        highscore_mgr,
        persistence,
    ) = build_game_systems(config)

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("42 Pac-Man")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    coordinator.game_renderer.set_surface(screen)
    clock = pygame.time.Clock()

    while main_loop.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop.stop()
            elif event.type == pygame.KEYDOWN:
                handle_key_events(
                    event,
                    coordinator,
                    main_loop,
                    ui_renderer,
                    cheat_system,
                    highscore_mgr,
                    persistence,
                )

        dt = min(clock.tick(60) / 1000.0, 0.05)
        sync_ui(ui_renderer, coordinator, cheat_system, config)

        main_loop.update(dt)

        screen.fill((0, 0, 0))
        main_loop.render()
        pygame.display.flip()

    save_persistent_highscores(persistence, highscore_mgr)
    coordinator.shutdown()
    pygame.quit()


def main() -> None:
    """Start the Pac-Man application."""
    ErrorLogger.install("errors.log")
    args: list[str] = sys.argv[1:]

    if len(args) != 1:
        print("Error: Invalid arguments.", file=sys.stderr)
        print("Usage: python3 pac-man.py <config.json>", file=sys.stderr)
        sys.exit(1)

    config_path = args[0]

    try:
        config = ConfigLoader.load(config_path, fallback_to_defaults=True)
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error loading configuration: {exc}", file=sys.stderr)
        sys.exit(1)

    run_game(config)


if __name__ == "__main__":
    main()
