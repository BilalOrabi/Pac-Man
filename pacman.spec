# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification file for 42 School Pac-Man.

This file defines the PyInstaller build pipeline used to compile the Python
codebase into a standalone desktop executable (pacman.exe on Windows, pacman
on Linux/macOS) with all assets and C-dependencies bundled together.

Build Command:
    pyinstaller pacman.spec --noconfirm

Output:
    dist/pacman/  (contains the standalone executable and all bundled assets)
"""

import os

# ==============================================================================
# STAGE 1: NON-CODE ASSETS & DATA FILES
# ==============================================================================
# Define additional data files and folders to bundle alongside the executable.
# Each tuple is formatted as: (source_path_on_disk, destination_folder_in_bundle)

bundle_data_files = []

# Bundle presentation assets (sprites, background artwork, font files)
if os.path.exists("assets"):
    bundle_data_files.append(("assets", "assets"))

# Bundle default game configuration
if os.path.exists("config.json"):
    bundle_data_files.append(("config.json", "."))

# Bundle player manual and instructions
if os.path.exists("INSTRUCTIONS.txt"):
    bundle_data_files.append(("INSTRUCTIONS.txt", "."))


# ==============================================================================
# STAGE 2: SOURCE CODE & DEPENDENCY ANALYSIS
# ==============================================================================
# Analyzes entry-point scripts, discovers module dependencies, and registers
# modules that are loaded dynamically (hidden imports).

analysis = Analysis(
    # Primary entry point script
    scripts=["pac-man.py"],

    # Root directory search path for imports
    pathex=["."],

    # Native compiled binaries (C-extensions)
    binaries=[],

    # Static data files and assets mapped in Stage 1
    datas=bundle_data_files,

    # Explicitly register modules imported dynamically at runtime
    hiddenimports=[
        # External dependencies
        "pygame",
        "mazegenerator",

        # Internal project packages & modules
        "src",
        "src.ai",
        "src.application",
        "src.cheat",
        "src.config",
        "src.controllers",
        "src.entities",
        "src.highscore",
        "src.input",
        "src.maze",
        "src.persistence",
        "src.rendering",
        "src.states",
        "src.systems",
        "src.theme",
        "src.utils",
        "src.world",
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)


# ==============================================================================
# STAGE 3: COMPILED PYTHON ARCHIVE (PYZ)
# ==============================================================================
# Compiles pure Python source files into bytecode (.pyc) and packs them into
# a single compressed archive.

pyz_archive = PYZ(
    analysis.pure,
    analysis.zipped_data,
    cipher=None,
)


# ==============================================================================
# STAGE 4: STANDALONE BOOTLOADER EXECUTABLE (EXE)
# ==============================================================================
# Combines the compiled C-bootloader with the startup script and PYZ archive.

executable = EXE(
    pyz_archive,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,                       # Keep console active for terminal launch
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory=".",
)


# ==============================================================================
# STAGE 5: FINAL DISTRIBUTION FOLDER (COLLECT)
# ==============================================================================
# Gathers the executable, shared libraries (DLLs / .so), and bundled assets
# into a clean, ready-to-distribute folder at dist/pacman/.

distribution_bundle = COLLECT(
    executable,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pacman",
)

