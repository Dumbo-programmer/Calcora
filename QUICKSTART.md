# Calcora - Quick Start Guide

## Running the Web Interface

### Option 1: Double-Click (Easiest)
Just double-click `calcora-server.exe` - it will:
1. Start the server
2. Automatically open your default browser
3. Load the Calcora web interface

### Option 2: Use the Launcher
Double-click `Start-WebUI.bat` for the same result

### Option 3: Command Line
```powershell
.\calcora-server.exe
```

The browser should open automatically to: http://127.0.0.1:8000/static/index.html

If it doesn't open automatically, manually open your browser and paste that URL.

## Using the Command Line

```powershell
# Differentiate
.\calcora.exe differentiate "x**2 + sin(x)"

# Matrix operations
.\calcora.exe matrix-multiply "[[1,2],[3,4]]" "[[5,6],[7,8]]"
.\calcora.exe matrix-determinant "[[1,2],[3,4]]"
.\calcora.exe matrix-inverse "[[1,2],[3,4]]"
.\calcora.exe matrix-eigenvalues "[[1,2],[2,1]]"
.\calcora.exe matrix-lu "[[2,1,1],[4,-6,0],[-2,7,2]]"

# Get help
.\calcora.exe --help
.\calcora.exe differentiate --help
```

## Stopping the Server

Press `CTRL+C` in the terminal window where the server is running.

## Troubleshooting

**Server starts but browser doesn't open?**
- Manually open your browser to: http://127.0.0.1:8000/static/index.html
- Or use: `.\calcora-server.exe --no-browser` then open manually

**Port already in use?**
```powershell
.\calcora-server.exe --port 8080
```
Then open: http://127.0.0.1:8080/static/index.html

**Nothing happens when I run it?**
- Check Windows Defender / antivirus - it might be blocking the exe
- Run from Command Prompt or PowerShell to see error messages

## System Requirements

- Windows 10/11 (64-bit)
- ~100 MB disk space
- No Python installation needed!

## Privacy Note

Calcora runs completely offline on your computer. No data is sent to external servers.
