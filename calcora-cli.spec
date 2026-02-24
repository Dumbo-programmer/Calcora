# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Calcora CLI executable."""

block_cipher = None

a = Analysis(
    ['src/calcora/cli/cli_entry.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'calcora.engine.calculus_rules',
        'calcora.engine.linalg_rules',
        'calcora.engine.step_engine',
        'calcora.bootstrap',
        'sympy',
        'typer',
        'rich',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        # NOTE: numpy is required for integration engine - do NOT exclude!
        'pandas',
        'IPython',
        'jupyter',
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
    name='calcora',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
