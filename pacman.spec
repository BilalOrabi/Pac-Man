# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for packaging 42 School Pac-Man."""

import os
import sys

block_cipher = None

datas = []
if os.path.exists("assets"):
    datas.append(("assets", "assets"))
if os.path.exists("config.json"):
    datas.append(("config.json", "."))
if os.path.exists("INSTRUCTIONS.txt"):
    datas.append(("INSTRUCTIONS.txt", "."))

a = Analysis(
    ["pac-man.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "pygame",
        "mazegenerator",
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
        "src.world",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pacman",
)
