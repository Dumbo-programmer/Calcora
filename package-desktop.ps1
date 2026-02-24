# Package script for Calcora Desktop v0.3
# Creates distributable ZIP packages for release

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Host ""
Write-Info "=" * 60
Write-Info "  Calcora Desktop Packager v0.3"
Write-Info "=" * 60
Write-Host ""

# Check if executable exists
if (-not (Test-Path "dist\Calcora.exe")) {
    Write-Error "Executable not found! Run .\build-desktop.ps1 first"
    exit 1
}

# Get version from pyproject.toml
$version = "0.3.0"
if (Test-Path "pyproject.toml") {
    $content = Get-Content "pyproject.toml" -Raw
    if ($content -match 'version\s*=\s*"([^"]+)"') {
        $version = $matches[1]
    }
}

# Create package directory
$packageName = "calcora-desktop-$version-windows-x64"
$packageDir = "dist\$packageName"

Write-Info "Creating package: $packageName"

# Clean up old package
if (Test-Path $packageDir) {
    Remove-Item -Recurse -Force $packageDir
}

New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy executable
Write-Info "Copying executable..."
Copy-Item "dist\Calcora.exe" $packageDir

# Copy documentation
Write-Info "Copying documentation..."
Copy-Item "README.md" $packageDir
Copy-Item "LICENSE" $packageDir

# Create Quick Start guide
Write-Info "Creating Quick Start guide..."
@"
# Calcora Desktop - Quick Start

Version: $version
Platform: Windows 64-bit

## Installation

No installation required! Calcora Desktop is a standalone executable.

## Quick Start

### Option 1: Double-Click (Easiest)

1. Simply **double-click Calcora.exe**
2. Your browser will open automatically
3. Start computing!

### Option 2: Command Line

1. Open PowerShell or Command Prompt in this folder
2. Run: ``.\Calcora.exe``
3. Browser opens automatically to http://localhost:8000

## Features

✅ **Differentiation**
   - Basic and higher-order derivatives
   - Step-by-step explanations
   - Interactive graphing

✅ **Integration** (NEW in v0.2+)
   - Indefinite and definite integrals
   - Multiple integration techniques
   - Area visualization

✅ **Matrix Operations**
   - Determinant, Inverse, RREF
   - Eigenvalues, LU Decomposition
   - Symbolic and numeric support

✅ **Completely Offline**
   - All computation runs locally
   - No internet connection needed
   - Your data never leaves your computer

## Security & Privacy

- ✅ Runs only on localhost (127.0.0.1)
- ✅ Not exposed to the internet
- ✅ No data collection
- ✅ No telemetry
- ✅ Open source (MIT License)

## Troubleshooting

**"Port already in use" error:**
- Calcora automatically finds an available port
- Close other applications using port 8000-8010
- Or restart your computer

**Browser doesn't open automatically:**
- Manually open: http://localhost:8000
- Check firewall settings

**Antivirus warning:**
- This is common for PyInstaller executables
- Calcora is safe (verify source code on GitHub)
- Add to antivirus exclusions if needed

## System Requirements

- Windows 10/11 (64-bit)
- 4 GB RAM minimum
- 100 MB disk space
- Modern web browser (Chrome, Firefox, Edge)

## Support

- 📖 Documentation: https://github.com/Dumbo-programmer/Calcora
- 🐛 Report bugs: https://github.com/Dumbo-programmer/Calcora/issues
- 💡 Feature requests: https://github.com/Dumbo-programmer/Calcora/discussions

## License

MIT License - See LICENSE file for details

---

Made with ❤️ by the Calcora team
"@ | Out-File -FilePath "$packageDir\QUICK_START.txt" -Encoding UTF8

# Create ZIP archive
Write-Info "Creating ZIP archive..."
$zipPath = "dist\$packageName.zip"
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

Compress-Archive -Path "$packageDir\*" -DestinationPath $zipPath

if (Test-Path $zipPath) {
    $zipSize = (Get-Item $zipPath).Length / 1MB
    Write-Host ""
    Write-Success "Package created successfully!"
    Write-Info "Package: $zipPath"
    Write-Info "Size: $([math]::Round($zipSize, 2)) MB"
    Write-Host ""
    Write-Info "Ready for distribution!"
    Write-Info "Upload to GitHub Releases or share directly"
}
else {
    Write-Error "Failed to create ZIP archive"
    exit 1
}

Write-Host ""
