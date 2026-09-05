"""Build and package the standalone Linux Pac-Man distribution."""

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def _get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parent


def _get_release_directory(project_root: Path) -> Path:
    """Return the PyInstaller distribution directory."""
    return project_root / "dist" / "pacman"


def _clean_build_directories(project_root: Path) -> None:
    """Remove previous PyInstaller build artifacts."""
    for directory_name in ("build", "dist"):
        directory = project_root / directory_name

        if directory.exists():
            shutil.rmtree(directory)


def _build_executable(project_root: Path) -> None:
    """Build the standalone executable with PyInstaller."""
    print("==> Building standalone executable via PyInstaller...")

    if shutil.which("uv"):
        command = [
            "uv",
            "run",
            "pyinstaller",
            "pacman.spec",
            "--clean",
            "--noconfirm",
        ]
    else:
        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "pacman.spec",
            "--clean",
            "--noconfirm",
        ]

    result = subprocess.run(
        command,
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "PyInstaller failed to build the Pac-Man executable."
        )


def _verify_executable(release_directory: Path) -> Path:
    """Verify that the standalone executable binary exists."""
    for candidate_name in ("pacman", "pacman.exe"):
        candidate_path = release_directory / candidate_name
        if candidate_path.is_file():
            return candidate_path

    raise FileNotFoundError(
        f"Standalone executable was not found in: {release_directory}"
    )


def _copy_release_assets(
    project_root: Path,
    release_directory: Path,
) -> None:
    """Copy presentation assets and configs into the release root."""
    print("==> Copying assets and configurations into release root...")

    # Copy assets/ directory into dist/pacman/assets/
    assets_source = project_root / "assets"
    assets_destination = release_directory / "assets"
    if assets_source.is_dir():
        if assets_destination.exists():
            shutil.rmtree(assets_destination)
        shutil.copytree(assets_source, assets_destination)

    # Copy config.json into dist/pacman/config.json
    config_source = project_root / "config.json"
    if config_source.is_file():
        shutil.copy2(config_source, release_directory / "config.json")

    # Copy INSTRUCTIONS.txt into dist/pacman/INSTRUCTIONS.txt
    instructions_source = project_root / "INSTRUCTIONS.txt"
    if instructions_source.is_file():
        shutil.copy2(
            instructions_source,
            release_directory / "INSTRUCTIONS.txt",
        )


def _create_release_archive(
    project_root: Path,
    release_directory: Path,
) -> Path:
    """Create a ZIP archive containing the complete distribution."""
    archive_path = project_root / "dist" / "pacman_linux.zip"

    if archive_path.exists():
        archive_path.unlink()

    print("==> Creating release archive...")

    with zipfile.ZipFile(
        archive_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as archive:
        for file_path in release_directory.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(release_directory.parent)
                info = zipfile.ZipInfo.from_file(
                    file_path,
                    arcname=str(relative_path),
                )
                if file_path.name in ("pacman", "pacman.exe"):
                    info.external_attr = 0o100755 << 16
                else:
                    info.external_attr = 0o100644 << 16
                archive.writestr(info, file_path.read_bytes())

    return archive_path


def create_release_package() -> Path:
    """Build the standalone game and assemble the final release package."""
    project_root = _get_project_root()
    release_directory = _get_release_directory(project_root)

    print("==> Cleaning previous build files...")
    _clean_build_directories(project_root)

    _build_executable(project_root)

    executable_path = _verify_executable(release_directory)

    _copy_release_assets(project_root, release_directory)

    archive_path = _create_release_archive(project_root, release_directory)

    print("==> Packaging complete!")
    print(f"    Release Folder : {release_directory}")
    print(f"    Executable     : {executable_path}")
    print(f"    ZIP Archive    : {archive_path}")

    return archive_path


if __name__ == "__main__":
    try:
        create_release_package()
    except Exception as exc:
        print(
            f"Packaging failed: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
