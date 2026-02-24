# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Calcora Desktop (v0.3+)

Creates a single-file executable that:
- Embeds Python runtime
- Includes Flask API server
- Bundles static web UI files (site/ directory)
- Auto-launches browser to localhost
- Works completely offline

Build commands:
  Windows: pyinstaller calcora-desktop.spec
  macOS:   pyinstaller calcora-desktop.spec --target-arch=universal2
  Linux:   pyinstaller calcora-desktop.spec
"""

block_cipher = None

# Collect all files from site/ directory
site_files = []
import os
for root, dirs, files in os.walk('site'):
    for file in files:
        file_path = os.path.join(root, file)
        # Get relative path for bundling
        rel_path = os.path.dirname(file_path)
        site_files.append((file_path, rel_path))

a = Analysis(
    ['calcora_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Bundle the actual application UI (not the marketing site!)
        ('src/calcora/web', 'web'),
        # Bundle API server
        ('api_server.py', '.'),
    ],
    hiddenimports=[
        # Core calcora
        'calcora',
        'calcora.bootstrap',
        'calcora.engine',
        'calcora.engine.calculus_rules',
        'calcora.engine.linalg_rules',
        'calcora.engine.step_engine',
        'calcora.renderers',
        'calcora.renderers.json_renderer',
        'calcora.integration_engine',
        'calcora.input_validator',
        'calcora.timeout_wrapper',
        # Web server
        'flask',
        'flask.json',
        'flask_cors',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.middleware.proxy_fix',
        # Dependencies - CRITICAL: Include numpy!
        'sympy',
        'sympy.parsing',
        'sympy.parsing.sympy_parser',
        'numpy',  # REQUIRED for integration engine
        'numpy.core',
        'numpy.lib',
        'pydantic',
        'pydantic.dataclasses',
        # CLI (optional, for future CLI commands)
        'typer',
        'rich',
        'click',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy optional dependencies
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'sphinx',
        # Exclude test files
        'tests',
        'test',
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
    name='Calcora',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for GUI-only mode (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Add icon here (create calcora.ico for Windows, calcora.icns for macOS)
    icon=None,  # TODO: icon='media/calcora-icon.ico'
)

# macOS app bundle (optional, for .app creation)
# Uncomment for macOS builds
# app = BUNDLE(
#     exe,
#     name='Calcora.app',
#     icon='media/calcora-icon.icns',
#     bundle_identifier='com.calcora.desktop',
#     info_plist={
#         'NSPrincipalClass': 'NSApplication',
#         'NSHighResolutionCapable': 'True',
#         'CFBundleShortVersionString': '0.3.0',
#         'CFBundleVersion': '0.3.0',
#     },
# )
