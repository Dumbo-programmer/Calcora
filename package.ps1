# Package script for creating distributable Calcora packages
# Creates a ZIP file with executables and documentation

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

# Check if executables exist
if (-not (Test-Path "dist\calcora.exe")) {
    Write-Error "CLI executable not found! Run .\build.ps1 first"
    exit 1
}

if (-not (Test-Path "dist\calcora-server.exe")) {
    Write-Error "Server executable not found! Run .\build.ps1 first"
    exit 1
}

# Get version from pyproject.toml
$version = "0.1.0"
if (Test-Path "pyproject.toml") {
    $content = Get-Content "pyproject.toml" -Raw
    if ($content -match 'version\s*=\s*"([^"]+)"') {
        $version = $matches[1]
    }
}

# Create package directory
$packageName = "calcora-$version-windows-x64"
$packageDir = "dist\$packageName"

Write-Info "Creating package: $packageName"

# Clean up old package
if (Test-Path $packageDir) {
    Remove-Item -Recurse -Force $packageDir
}

New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy executables
Write-Info "Copying executables..."
Copy-Item "dist\calcora.exe" $packageDir
Copy-Item "dist\calcora-server.exe" $packageDir

# Create README for the package
Write-Info "Creating README..."
@"
# Calcora - Computational Mathematics Engine

Version: $version
Platform: Windows x64

## What's Included

- **calcora.exe** - Command-line interface for mathematical operations
- **calcora-server.exe** - API server with web interface

## Quick Start

### Command Line Interface (CLI)

Open PowerShell or Command Prompt in this folder and run:

``````powershell
# Differentiate an expression
.\calcora.exe differentiate "x**2 + 3*x"

# Higher-order derivatives
.\calcora.exe differentiate "sin(x)" --order 2

# Matrix operations
.\calcora.exe matrix-multiply "[[1,2],[3,4]]" "[[5,6],[7,8]]"
.\calcora.exe matrix-determinant "[[1,2],[3,4]]"
.\calcora.exe matrix-inverse "[[1,2],[3,4]]"
.\calcora.exe matrix-rref "[[1,2,3],[4,5,6]]"
.\calcora.exe matrix-eigenvalues "[[1,2],[2,1]]"
.\calcora.exe matrix-lu "[[2,1,1],[4,-6,0],[-2,7,2]]"

# Get help
.\calcora.exe --help
.\calcora.exe differentiate --help
``````

### Web Interface

**Option 1: Double-Click (Easiest)**
- Simply double-click `calcora-server.exe`
- Your browser will open automatically with the web interface

**Option 2: Use the Quick Launcher**
- Double-click `Start-WebUI.bat`
- Browser opens automatically

**Option 3: Command Line**
   ``````powershell
   .\calcora-server.exe
   ``````

The browser will automatically open to: http://127.0.0.1:8000/static/index.html

If the browser doesn't open automatically, manually navigate to that URL.

To stop the server, press CTRL+C in the terminal window.

**Server Options:**
``````powershell
# Run on different port
.\calcora-server.exe --port 8080

# Don't auto-open browser
.\calcora-server.exe --no-browser

# Custom host and port
.\calcora-server.exe --host 0.0.0.0 --port 8080
``````

2. Use the web interface to:
   - Differentiate expressions with step-by-step explanations
   - Perform matrix operations
   - View detailed mathematical steps

## Features

### Differentiation
- Basic rules: power, sum, product, quotient, chain rule
- Trigonometric functions: sin, cos, tan, sec, csc, cot
- Inverse trig: asin, acos, atan, asec, acsc, acot
- Hyperbolic: sinh, cosh, tanh, sech, csch, coth
- Exponential and logarithmic functions
- Special functions: erf, gamma, Heaviside, abs, floor, ceiling
- Multi-variable support
- Higher-order derivatives (up to 10th order)

### Linear Algebra
- Matrix multiplication
- Determinant (2×2, 3×3, n×n)
- Matrix inverse
- Row-reduced echelon form (RREF)
- Eigenvalues and eigenvectors
- LU decomposition with partial pivoting

## Privacy & Offline Use

Calcora runs completely offline on your computer. No data is sent to external servers.
All computations happen locally using symbolic mathematics.

## System Requirements

- Windows 10 or later (64-bit)
- No Python installation required (self-contained)
- ~100 MB disk space

## Support

- Documentation: https://Dumbo-programmer.github.io/calcora/
- Issues: https://github.com/Dumbo-programmer/calcora/issues
- Repository: https://github.com/Dumbo-programmer/calcora

## License

MIT License - See repository for full license text.

"@ | Out-File -FilePath "$packageDir\README.txt" -Encoding utf8

# Create a simple launcher script for the web interface
Write-Info "Creating launcher script..."
@"
@echo off
echo Starting Calcora Web Interface...
echo.
echo The server will start at http://127.0.0.1:8000
echo Web UI: http://127.0.0.1:8000/static/index.html
echo.
echo Press CTRL+C to stop the server
echo.
start http://127.0.0.1:8000/static/index.html
calcora-server.exe
"@ | Out-File -FilePath "$packageDir\Start-WebUI.bat" -Encoding ascii

# Copy license if exists
if (Test-Path "LICENSE") {
    Copy-Item "LICENSE" "$packageDir\LICENSE.txt"
}

# Create ZIP file
$zipFile = "dist\$packageName.zip"
Write-Info "Creating ZIP archive..."

if (Test-Path $zipFile) {
    Remove-Item $zipFile
}

Compress-Archive -Path $packageDir -DestinationPath $zipFile

# Calculate size
$size = (Get-Item $zipFile).Length / 1MB
$sizeFormatted = "{0:N2}" -f $size

Write-Success ""
Write-Success "═══════════════════════════════════════="
Write-Success "Package created successfully!"
Write-Success "════════════════════════════════════════"
Write-Info "Package: $zipFile"
Write-Info "Size: $sizeFormatted MB"
Write-Info ""
Write-Info "Contents:"
Write-Info "  - calcora.exe (CLI)"
Write-Info "  - calcora-server.exe (Web UI)"
Write-Info "  - Start-WebUI.bat (Quick launcher)"
Write-Info "  - README.txt"
Write-Info "  - LICENSE.txt"
Write-Success ""
Write-Success "Ready for distribution!"
