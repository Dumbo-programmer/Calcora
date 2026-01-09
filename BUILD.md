# Building and Distributing Calcora

This guide explains how to create distributable executables for Calcora.

## Prerequisites

- Python 3.11+ with virtual environment activated
- All dependencies installed (`pip install -e .[engine-sympy,cli,api]`)
- PyInstaller installed (`pip install pyinstaller`)

## Building Executables

### Build Everything

```powershell
.\build.ps1
```

This builds both the CLI and server executables in the `dist/` folder:
- `dist/calcora.exe` - Command-line interface
- `dist/calcora-server.exe` - Web server with UI

### Build Individual Components

```powershell
# Build only CLI
.\build.ps1 cli

# Build only server
.\build.ps1 server
```

## Creating Distribution Package

After building, create a distributable ZIP package:

```powershell
.\package.ps1
```

This creates `dist/calcora-{version}-windows-x64.zip` containing:
- Both executables (CLI and server)
- README.txt with user instructions
- Start-WebUI.bat quick launcher
- LICENSE.txt

The package is completely self-contained - no Python installation required.

## Distribution Package Size

Typical package size: ~48 MB compressed (~120 MB uncompressed)

This includes:
- Python runtime
- SymPy symbolic math library
- FastAPI web framework
- All Calcora code and rules

## Testing the Build

Test the CLI:
```powershell
.\dist\calcora.exe differentiate "x**2"
.\dist\calcora.exe matrix-determinant "[[1,2],[3,4]]"
```

Test the server:
```powershell
.\dist\calcora-server.exe
# Open browser to http://127.0.0.1:8000/static/index.html
```

## Distribution Channels

### GitHub Releases

1. Create a new release on GitHub
2. Upload the ZIP file
3. Tag with version number (e.g., `v0.1.0`)

Example release notes:
```
## Calcora v0.1.0 - Windows x64

Self-contained executable package for Windows.

### Download
- calcora-0.1.0-windows-x64.zip (48 MB)

### What's Inside
- CLI tool for command-line usage
- Web server with interactive UI
- Complete offline functionality

### Requirements
- Windows 10+ (64-bit)
- No Python installation needed
```

### Direct Download

Host the ZIP file on:
- GitHub Releases (recommended)
- Project website
- Cloud storage (Google Drive, Dropbox, etc.)

## Platform Support

Currently supported:
- ✅ Windows 10/11 (64-bit)

Future platforms:
- 🔄 macOS (Intel and Apple Silicon)
- 🔄 Linux (x64)

To build for other platforms, run the build scripts on those platforms with the same Python version.

## Build Configuration

### PyInstaller Spec Files

- `calcora-cli.spec` - CLI configuration
- `calcora-server.spec` - Server configuration

Key settings:
- `--onefile`: Single executable (no folder)
- `--clean`: Clean build cache
- `--noconfirm`: No prompts during build
- `upx=True`: Compress with UPX (reduces size)
- `console=True`: Console application (shows terminal)

### Customization

To customize builds, edit the `.spec` files:

```python
# Add data files
datas=[
    ('custom_data/*', 'data'),
],

# Add hidden imports
hiddenimports=[
    'custom_module',
],

# Add icon
icon='icon.ico',
```

## Troubleshooting

### "Module not found" errors

Add missing modules to `hiddenimports` in the `.spec` file:
```python
hiddenimports=[
    'missing_module',
],
```

### Large file size

Exclude unnecessary packages:
```python
excludes=[
    'matplotlib',
    'scipy',
    'numpy',
],
```

### Slow startup

This is normal for first launch. PyInstaller extracts files to temp folder.

### Antivirus false positives

PyInstaller executables may trigger antivirus warnings. Submit to vendors for whitelisting or sign the executable with a code signing certificate.

## Code Signing (Optional)

For production distribution, sign the executables:

```powershell
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\calcora.exe
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\calcora-server.exe
```

This prevents Windows SmartScreen warnings and builds user trust.

## Continuous Integration

### GitHub Actions Example

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[engine-sympy,cli,api]
          pip install pyinstaller
      - name: Build executables
        run: .\build.ps1
      - name: Create package
        run: .\package.ps1
      - name: Upload release
        uses: actions/upload-artifact@v3
        with:
          name: calcora-windows-x64
          path: dist/*.zip
```

## Version Management

Update version in `pyproject.toml`:
```toml
[project]
version = "0.2.0"
```

The package script automatically reads this version for naming.

## License

Ensure the package includes LICENSE.txt. The package script automatically copies it from the project root.

## Support

For build issues, check:
- PyInstaller version compatibility
- Python version (3.13.7 recommended)
- Virtual environment activation
- Antivirus interference

Report issues at: https://github.com/Dumbo-programmer/calcora/issues
