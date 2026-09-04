"""Packaging script for 42 School Pac-Man platform distribution."""

import shutil
import sys
import zipfile
from pathlib import Path


def create_release_bundle() -> Path:
    """Bundle the Pac-Man project into a distributable release directory."""
    project_root = Path(__file__).resolve().parent
    dist_dir = project_root / "dist"
    release_dir = dist_dir / "pacman_release"

    print("==> Packaging 42 School Pac-Man for distribution...")

    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy source code and entry points
    src_dest = release_dir / "src"
    shutil.copytree(project_root / "src", src_dest)

    # Clean __pycache__ from bundle
    for pycache in release_dir.rglob("__pycache__"):
        shutil.rmtree(pycache)

    shutil.copy2(project_root / "pac-man.py", release_dir / "pac-man.py")
    shutil.copy2(project_root / "config.json", release_dir / "config.json")

    instructions_src = project_root / "INSTRUCTIONS.txt"
    if instructions_src.exists():
        shutil.copy2(instructions_src, release_dir / "INSTRUCTIONS.txt")

    # 2. Copy libs and wheels
    libs_dir = project_root / "libs"
    if libs_dir.exists():
        shutil.copytree(libs_dir, release_dir / "libs")

    # 3. Copy assets if present
    assets_dir = project_root / "assets"
    if assets_dir.exists():
        shutil.copytree(assets_dir, release_dir / "assets")
    else:
        (release_dir / "assets").mkdir(exist_ok=True)

    # 4. Generate OS Launchers
    run_bat = release_dir / "run.bat"
    run_bat.write_text(
        "@echo off\n"
        "echo Launching 42 School Pac-Man...\n"
        "python pac-man.py config.json\n"
        "if %errorlevel% neq 0 pause\n",
        encoding="utf-8",
    )

    run_sh = release_dir / "run.sh"
    run_sh.write_text(
        "#!/usr/bin/env bash\n"
        "echo 'Launching 42 School Pac-Man...'\n"
        "python3 pac-man.py config.json\n",
        encoding="utf-8",
    )

    # 5. Create release ZIP archive for itch.io / Steam upload
    zip_path = dist_dir / "pacman_release.zip"
    if zip_path.exists():
        zip_path.unlink()

    print("==> Creating release archive pacman_release.zip...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in release_dir.rglob("*"):
            archive.write(file_path, file_path.relative_to(dist_dir))

    print("==> Standalone release bundle built successfully in:")
    print(f"    {release_dir}")
    print(f"==> Standalone release archive created: {zip_path}")
    return release_dir


if __name__ == "__main__":
    try:
        create_release_bundle()
    except Exception as exc:
        print(f"Packaging failed: {exc}", file=sys.stderr)
        sys.exit(1)
