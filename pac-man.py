"""Main entry point for the Pac-Man game."""

import sys

from src.config import ConfigError, ConfigLoader


def main() -> None:
    """Start the Pac-Man application."""
    args: list[str] = sys.argv[1:]

    if len(args) != 1:
        print("Error: Invalid arguments.", file=sys.stderr)
        print(
            "Usage: python3 pac-man.py <config.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_path = args[0]

    try:
        config = ConfigLoader.load(config_path)
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    print("Pac-Man configuration loaded successfully.")
    print(f"  Lives: {config.lives}")
    print(f"  Pacgums: {config.pacgum}")
    print(f"  Levels: {len(config.levels)}")
    print(f"  Level time: {config.level_max_time}s")


if __name__ == "__main__":
    main()
