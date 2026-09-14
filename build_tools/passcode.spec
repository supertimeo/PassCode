# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for PassCode application

import os
from pathlib import Path

block_cipher = None

# Chemin racine du projet
project_root = Path(os.path.dirname(os.path.abspath(SPEC))).parent

# Fichiers source principaux
a = Analysis(
    [str(project_root / "src" / "app" / "app.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[
        # Assets (images, styles, médias, configuration)
        (str(project_root / "assets"), "assets"),
        (str(project_root / "configs"), "configs"),
    ],
    hiddenimports=[
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        # Exclure les modules non nécessaires
        "playwright",
        "beautifulsoup4",
        "selectolax",
        "ffmpeg",
        "tqdm",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PassCode",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
