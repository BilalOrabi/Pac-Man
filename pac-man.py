import sys


def main() -> None:
    """Main application entry point."""
    args: list[str] = sys.argv[1:]
    if len(args) != 1:
        print("Error: Invalid arguments.", file=sys.stderr)
        print("Usage: python3 pac-man.py <config.json>", file=sys.stderr)
        sys.exit(1)

    config_path: str = args[0]
    print(f"Starting Pac-Man engine with configuration: {config_path}")


if __name__ == "__main__":
    main()
