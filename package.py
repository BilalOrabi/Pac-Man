"""Packaging script for 42 School Pac-Man platform distribution.

This script automates building standalone distribution packages suitable
for distribution on game platforms (such as itch.io and Steam).
"""

import shutil
import sys
import zipfile
from pathlib import Path


def _prepare_release_directory(release_dir: Path) -> None:
    """Wipe any existing build and initialize a fresh release directory."""
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)


def _copy_source_files(project_root: Path, release_dir: Path) -> None:
    """Copy pure domain and presentation Python packages and entry points."""
    src_dest = release_dir / "src"
    shutil.copytree(project_root / "src", src_dest)

    # Clean intermediate Python bytecode (__pycache__) from release bundle
    for pycache_dir in release_dir.rglob("__pycache__"):
        shutil.rmtree(pycache_dir)

    # Copy entry point and core configuration
    shutil.copy2(project_root / "pac-man.py", release_dir / "pac-man.py")
    shutil.copy2(project_root / "config.json", release_dir / "config.json")

    # Copy player manual if present
    instructions_file = project_root / "INSTRUCTIONS.txt"
    if instructions_file.exists():
        shutil.copy2(instructions_file, release_dir / "INSTRUCTIONS.txt")


def _copy_dependencies_and_assets(
    project_root: Path, release_dir: Path
) -> None:
    """Copy external wheels (mazegenerator) and presentation assets."""
    libs_dir = project_root / "libs"
    if libs_dir.exists():
        shutil.copytree(libs_dir, release_dir / "libs")

    assets_dir = project_root / "assets"
    if assets_dir.exists():
        shutil.copytree(assets_dir, release_dir / "assets")
    else:
        (release_dir / "assets").mkdir(exist_ok=True)


def _generate_platform_launchers(release_dir: Path) -> None:
    """Generate double-click OS execution scripts for Windows and Unix."""
    # Windows Command Batch Launcher
    run_bat = release_dir / "run.bat"
    run_bat.write_text(
        "@echo off\n"
        "echo Launching 42 School Pac-Man...\n"
        "python pac-man.py config.json\n"
        "if %errorlevel% neq 0 pause\n",
        encoding="utf-8",
    )

    # Linux and macOS Bash Shell Launcher
    run_sh = release_dir / "run.sh"
    run_sh.write_text(
        "#!/usr/bin/env bash\n"
        "echo 'Launching 42 School Pac-Man...'\n"
        "python3 pac-man.py config.json\n",
        encoding="utf-8",
    )


def _create_release_archive(dist_dir: Path, release_dir: Path) -> Path:
    """Compress the release directory into a distributable ZIP archive."""
    zip_path = dist_dir / "pacman_release.zip"
    if zip_path.exists():
        zip_path.unlink()

    print("==> Compressing release directory into pacman_release.zip...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in release_dir.rglob("*"):
            archive.write(file_path, file_path.relative_to(dist_dir))

    return zip_path


def create_release_bundle() -> Path:
    """Bundle the Pac-Man project into a distributable release directory.

    Execution Pipeline:
      Step 1: Clean and create target release folder (dist/pacman_release/).
      Step 2: Copy game source code, config, and documentation.
      Step 3: Copy external wheel libraries and presentation assets.
      Step 4: Generate OS launchers (run.bat for Windows, run.sh for Unix).
      Step 5: Compress bundle into pacman_release.zip for itch.io / Steam.

    Returns:
        Path to the generated release directory.
    """
    project_root = Path(__file__).resolve().parent
    dist_dir = project_root / "dist"
    release_dir = dist_dir / "pacman_release"

    print("==> Step 1: Initializing fresh release directory...")
    _prepare_release_directory(release_dir)

    print("==> Step 2: Copying source packages, entry point and configs...")
    _copy_source_files(project_root, release_dir)

    print("==> Step 3: Bundling wheel dependencies and presentation assets...")
    _copy_dependencies_and_assets(project_root, release_dir)

    print("==> Step 4: Generating Windows (.bat) and Unix (.sh) launchers...")
    _generate_platform_launchers(release_dir)

    print("==> Step 5: Building compressed distribution archive...")
    zip_path = _create_release_archive(dist_dir, release_dir)

    print("==> Packaging Complete!")
    print(f"    Release Folder  : {release_dir}")
    print(f"    Release Archive : {zip_path}")
    return release_dir


if __name__ == "__main__":
    try:
        create_release_bundle()
    except Exception as exc:
        print(f"Packaging failed: {exc}", file=sys.stderr)
        sys.exit(1)
