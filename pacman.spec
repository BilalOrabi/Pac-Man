# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification file for 42 School Pac-Man Linux distribution.

This file builds the completed Pac-Man application into a standalone Linux
distribution containing the executable, Python runtime, external Python
dependencies, configuration, and presentation assets.

Build Command:
    pyinstaller pacman.spec --clean --noconfirm

Output:
    dist/pacman/
"""

# ==============================================================================
# STAGE 1: NON-CODE ASSETS & DATA FILES (Delegated to package.py)
# ==============================================================================
# Non-code presentation assets (assets/), configuration (config.json), and
# documentation (INSTRUCTIONS.txt) are copied into dist/pacman/ by package.py.

# ==============================================================================
# STAGE 2: SOURCE CODE & DEPENDENCY ANALYSIS
# ==============================================================================

analysis = Analysis(
    scripts=["pac-man.py"],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=[
        "pygame",
        "mazegenerator",
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
# STAGE 3: COMPILED PYTHON ARCHIVE
# ==============================================================================

pyz_archive = PYZ(
    analysis.pure,
    analysis.zipped_data,
    cipher=None,
)


# ==============================================================================
# STAGE 4: STANDALONE LINUX EXECUTABLE
# ==============================================================================

executable = EXE(
    pyz_archive,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory="_internal",
)


# ==============================================================================
# STAGE 5: FINAL DISTRIBUTION FOLDER
# ==============================================================================

distribution_bundle = COLLECT(
    executable,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="pacman",
)
