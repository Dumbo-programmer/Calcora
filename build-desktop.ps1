# Build script for Calcora Desktop v0.3+
# Creates a single-file desktop executable with embedded web UI

param(
    [switch]$Clean,
    [switch]$Test
)

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Host ""
Write-Info "=" * 60
Write-Info "  Calcora Desktop Builder v0.3"
Write-Info "=" * 60
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Error "Virtual environment is not activated!"
    Write-Info "Please activate it first with .\.venv\Scripts\Activate.ps1"
    exit 1
}

# Install PyInstaller if not present
Write-Info "Checking for PyInstaller..."
$pyinstaller = python -m pip list | Select-String "pyinstaller"
if (-not $pyinstaller) {
    Write-Info "Installing PyInstaller..."
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install PyInstaller"
        exit 1
    }
}

# Clean previous builds if requested
if ($Clean) {
    Write-Info "Cleaning previous builds..."
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "Calcora.spec") { Remove-Item -Force "Calcora.spec" }
    Write-Success "Clean complete"
}

# Create dist directory
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Path "dist" | Out-Null
}

Write-Host ""
Write-Info "Building Calcora Desktop executable..."
Write-Info "This may take 2-5 minutes..."
Write-Host ""

# Run PyInstaller
pyinstaller calcora-desktop.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed!"
    exit 1
}

# Check if executable was created
if (Test-Path "dist\Calcora.exe") {
    $size = (Get-Item "dist\Calcora.exe").Length / 1MB
    Write-Host ""
    Write-Success "Build successful!"
    Write-Info "Executable: dist\Calcora.exe"
    Write-Info "Size: $([math]::Round($size, 2)) MB"
    
    if ($Test) {
        Write-Host ""
        Write-Info "Testing executable..."
        Write-Info "(Server will start - press Ctrl+C to stop)"
        Write-Host ""
        
        Start-Sleep -Seconds 2
        & "dist\Calcora.exe"
    }
    else {
        Write-Host ""
        Write-Info "To test the executable, run:"
        Write-Info "  .\dist\Calcora.exe"
        Write-Host ""
        Write-Info "To create a distribution package:"
        Write-Info "  .\package-desktop.ps1"
    }
}
else {
    Write-Error "Build failed - executable not found!"
    Write-Info "Check the build output above for errors"
    exit 1
}

Write-Host ""
