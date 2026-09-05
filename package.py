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
    """Build the standalone Linux executable with PyInstaller."""
    print("==> Building standalone Linux executable...")

    result = subprocess.run(
        [
            "uv",
            "run",
            "pyinstaller",
            "pacman.spec",
            "--clean",
            "--noconfirm",
        ],
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "PyInstaller failed to build the Pac-Man executable."
        )


def _verify_executable(release_directory: Path) -> Path:
    """Verify that the standalone executable was created."""
    executable_path = release_directory / "pacman"

    if not executable_path.is_file():
        raise FileNotFoundError(
            f"Standalone executable was not created: {executable_path}"
        )

    return executable_path


def _create_release_archive(
    project_root: Path,
    release_directory: Path,
) -> Path:
    """Create a ZIP archive containing the complete Linux distribution."""
    archive_path = project_root / "dist" / "pacman_linux.zip"

    if archive_path.exists():
        archive_path.unlink()

    print("==> Creating Linux release archive...")

    with zipfile.ZipFile(
        archive_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as archive:
        for file_path in release_directory.rglob("*"):
            if file_path.is_file():
                archive.write(
                    file_path,
                    file_path.relative_to(
                        release_directory.parent
                    ),
                )

    return archive_path


def create_release_package() -> Path:
    """Build the standalone Linux game and create its ZIP archive."""
    project_root = _get_project_root()
    release_directory = _get_release_directory(project_root)

    print("==> Cleaning previous build files...")
    _clean_build_directories(project_root)

    _build_executable(project_root)

    executable_path = _verify_executable(
        release_directory
    )

    archive_path = _create_release_archive(
        project_root,
        release_directory,
    )

    print("==> Packaging complete!")
    print(f"    Executable : {executable_path}")
    print(f"    ZIP        : {archive_path}")

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
