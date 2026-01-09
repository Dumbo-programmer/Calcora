# Build script for creating Calcora executables with PyInstaller
# Usage: .\build.ps1 [cli|server|all]

param(
    [Parameter(Position=0)]
    [ValidateSet("cli", "server", "all")]
    [string]$Target = "all"
)

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

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
}

# Create dist directory
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Path "dist" | Out-Null
}

# Build CLI
function Build-CLI {
    Write-Host ""
    Write-Info "Building Calcora CLI executable..."
    .\.venv\Scripts\pyinstaller.exe calcora-cli.spec --clean --noconfirm
    
    if (Test-Path "dist\calcora.exe") {
        Write-Success "CLI executable created at dist\calcora.exe"
        
        # Test the executable
        Write-Info "Testing CLI executable..."
        $testOutput = & "dist\calcora.exe" differentiate "x**2" --verbosity concise 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "CLI test passed"
        } else {
            Write-Error "CLI test failed"
        }
    } else {
        Write-Error "Failed to create CLI executable"
        exit 1
    }
}

# Build Server
function Build-Server {
    Write-Host ""
    Write-Info "Building Calcora Server executable..."
    .\.venv\Scripts\pyinstaller.exe calcora-server.spec --clean --noconfirm
    
    if (Test-Path "dist\calcora-server.exe") {
        Write-Success "Server executable created at dist\calcora-server.exe"
        Write-Info "Note - Server needs to be tested manually by running it"
    } else {
        Write-Error "Failed to create server executable"
        exit 1
    }
}

# Execute builds based on target
switch ($Target) {
    "cli" {
        Build-CLI
    }
    "server" {
        Build-Server
    }
    "all" {
        Build-CLI
        Build-Server
        
        Write-Host ""
        Write-Success "Build complete!"
        Write-Info "CLI is at dist\calcora.exe"
        Write-Info "Server is at dist\calcora-server.exe"
        Write-Host ""
        Write-Info "To create a distribution package run package.ps1"
    }
}
