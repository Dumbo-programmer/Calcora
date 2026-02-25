# Calcora Desktop v0.3.0 Release Notes

**Release Date:** February 26, 2026  
**Build Size:** 37.25 MB (22% smaller than v0.2)  
**Status:** Production Ready  

---

## 🎯 Overview

Calcora Desktop v0.3.0 represents a major leap in **engineering maturity and user experience polish**. This release transforms Calcora from an academic tool into a **production-grade desktop application** with professional error handling, graceful shutdown, and native branding.

**Key Achievement:** First-impression excellence — no longer feels experimental.

---

## ✨ Major Features

### 1. Custom Application Icon
- Professional mathematical design (∫ symbol with blue gradient)
- Multi-resolution support (256×256 → 16×16 px)
- Visible in Windows taskbar, Start menu, and file explorer
- Windows exe metadata (visible in Properties dialog)

**Impact:** Native branding establishes legitimacy.

### 2. Graceful Shutdown System
- **Quit button** in web UI footer (desktop mode only)
- Confirmation dialog before shutdown
- Farewell screen on successful exit
- `/shutdown` API endpoint (localhost-only security)
- Improved Ctrl+C handler with GitHub link

**Impact:** Prevents zombie processes, professional UX.

### 3. Professional Console Output
- Colored status messages (cross-platform via colorama)
- Clear visual hierarchy with separators
- Explicit privacy guarantees ("100% Offline")
- Status indicators (✓ for success, ⚠ for warnings)
- Better instructions (Quit button + Ctrl+C options)

**Impact:** Builds trust, reduces perceived complexity.

### 4. Desktop Mode Badge
- Green indicator in footer when running locally
- Shows transparency (not hiding architecture)
- Only visible in desktop mode (localhost detection)

**Impact:** Clear runtime context for users.

### 5. Enhanced Reliability
- **Health check** before browser launch (5 retries, 500ms delay)
- **Multi-browser fallback** (Default → Chrome → Firefox → Edge → Safari)
- Graceful degradation (colorama optional)
- Better error messages with log file locations

**Impact:** Robust startup on varied systems.

---

## 🔧 Architecture Improvements

### OS-Managed Port Assignment
**Before:**
```python
for port in range(8000, 8011):
    try:
        socket.bind(('127.0.0.1', port))
        break
    except OSError:
        continue
```

**After:**
```python
def get_available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))  # OS assigns available port
        return s.getsockname()[1]
```

**Impact:**
- ✅ Eliminates port collision edge cases
- ✅ Removes security predictability
- ✅ Professional-grade behavior

### Top-Level Exception Boundary
```python
def run_with_error_boundary():
    try:
        sys.exit(main())
    except Exception as e:
        log_error(e, "CRITICAL: Unhandled top-level exception")
        show_error_dialog("Calcora Critical Error", ...)
        sys.exit(1)
```

**Impact:** No raw Python tracebacks leak to users — all errors logged and handled gracefully.

---

## 📦 Build Quality

### Size Optimization
- **v0.2:** 47.79 MB
- **v0.3:** 37.25 MB
- **Reduction:** 22% (−10.54 MB)

### Metadata
- Windows version info embedded
- Company: "Calcora Project"
- File Description: "Calcora - Computational Mathematics Engine"
- Copyright: "MIT License - Open Source"

### Build Reproducibility
- `requirements-lock.txt` (300+ pinned dependencies)
- Documented in `DESKTOP_GUIDE.md`
- Quarterly rebuild policy established

---

## 🛡️ Security Enhancements

### Network Security
- ✅ Binds ONLY to `127.0.0.1` (not `0.0.0.0`)
- ✅ OS-assigned ephemeral ports (not predictable)
- ✅ `/shutdown` endpoint has localhost-only check
- ✅ No external network requests

### Privacy Guarantees
- ✅ 100% offline computation
- ✅ No telemetry or analytics
- ✅ No auto-updates (manual only)
- ✅ No data collection

---

## 🎨 UI/UX Polish

### Console Experience
```
══════════════════════════════════════════════════════════════════════
  🧮 Calcora Desktop v0.3.0
  Computational Mathematics Engine — Privacy-First, Offline
══════════════════════════════════════════════════════════════════════

✓ Network port assigned: 54782 (OS-managed)
✓ Mathematical engine loaded
✓ Browser will open automatically in 1-2 seconds...

──────────────────────────────────────────────────────────────────────
  Server Status:
  • Running at: http://127.0.0.1:54782
  • Mode: Private (localhost only, not exposed to internet)
  • Computation: 100% Offline (no data sent externally)
──────────────────────────────────────────────────────────────────────
```

### Web UI Enhancements
- Desktop mode indicator badge
- Quit Calcora button (desktop-only)
- GitHub link in footer
- Version updated to v0.3.0

---

## 📊 Performance

### Startup Time
- **Cold start:** ~2-3 seconds (double-click → browser loaded)
- **Process init:** <1 second
- **Browser launch:** ~1-2 seconds (OS-dependent)

**Verdict:** Within professional threshold (<3s).

### Runtime Performance
- No changes to mathematical engine
- Same differentiation/integration speed
- Same accuracy (100% test pass rate)

---

## 🧪 Testing

### Verified Functionality
- ✅ Build successful (PyInstaller 6.17.0)
- ✅ Icon appears in executable
- ✅ Colored console output works
- ✅ Browser auto-launches
- ✅ Shutdown button visible in footer
- ✅ Desktop mode badge shows
- ✅ All API operations working
- ✅ GitHub link functional
- ✅ Graceful shutdown via button
- ✅ Graceful shutdown via Ctrl+C

### Known Limitations
- Console window always visible (trade-off for transparency)
- First-run may trigger Windows Defender scan (~5-10s delay)
- PyInstaller antivirus false positives possible (submit for whitelisting if needed)

---

## 📁 File Structure Changes

### New Files
```
media/
├── calcora-icon.ico          # Multi-res Windows icon
└── calcora-icon.png          # PNG version (documentation)

scripts/
├── generate_icon.py          # Icon generator script
└── measure_startup.ps1       # Startup time measurement

version_info.txt              # Windows exe metadata
docs/releases/v0.3/
└── PRE_SHIP_AUDIT.md         # Comprehensive pre-release audit
```

### Modified Files
- `calcora_desktop.py` — Console polish, health check, browser fallback
- `api_server.py` — /shutdown endpoint
- `calcora-desktop.spec` — Icon + version metadata
- `src/calcora/web/index.html` — Quit button, desktop badge
- `DESKTOP_GUIDE.md` — Enhanced documentation

---

## 🚀 Installation

### Windows
1. Download `Calcora.exe` (37.25 MB)
2. Double-click to run (no installation needed)
3. Calculator opens in your browser automatically

### First Run
- May trigger Windows Defender scan (one-time delay)
- Creates `~/.calcora/error.log` for troubleshooting
- No admin privileges required

### Uninstall
- Delete `Calcora.exe`
- Optionally delete `~/.calcora/` directory

---

## 🔬 Technical Details

### System Requirements
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 512 MB minimum (1 GB recommended)
- **Disk:** 50 MB free space
- **Browser:** Chrome, Edge, Firefox, or Safari

### Included Components
- Python 3.13.7 runtime (embedded)
- SymPy 1.13.3 (symbolic mathematics)
- NumPy 2.2.4 (numerical computation)
- Flask 3.1.0 (API server)
- Colorama 0.4.6 (colored console output)

### Security Model
- Localhost-only server (127.0.0.1)
- No internet access required
- All computation runs locally
- No external dependencies at runtime

---

## 📚 Documentation

### Updated Guides
- `DESKTOP_GUIDE.md` — Comprehensive desktop app documentation
- `PRE_SHIP_AUDIT.md` — Engineering review and security assessment
- `README.md` — Updated installation instructions

### For Developers
- `requirements-lock.txt` — Reproducible build environment
- `build-desktop.ps1` — Automated build script
- `scripts/generate_icon.py` — Icon generation for custom branding

---

## 🎓 Use Cases

### Ideal For
- ✅ **Students:** Homework with step-by-step solutions
- ✅ **Teachers:** Classroom demonstrations (offline, no setup)
- ✅ **Researchers:** Reproducible symbolic computation
- ✅ **Privacy-conscious users:** No cloud dependencies

### Examples
```python
# Differentiation
d/dx[sin(x²)] → 2x·cos(x²)

# Integration
∫ x² dx → x³/3 + C

# Matrix Operations
det([[1,2],[3,4]]) → -2
```

---

## 🐛 Bug Fixes

### Fixed Issues
- ✅ Port collision issues (OS-managed ports)
- ✅ Zombie processes after browser close (Quit button)
- ✅ Raw traceback leaks (exception boundary)
- ✅ Unclear shutdown process (multiple exit methods)
- ✅ Missing application icon
- ✅ Console output readability

---

## ⚠️ Breaking Changes

**None.** This is a backward-compatible release.

All v0.2 features remain functional with improved polish and reliability.

---

## 🔮 Future Roadmap

### v0.3.1 (Patch)
- Optional console-less mode (`console=False` build)
- Windows Defender submission (reduce false positives)
- Code signing certificate (trust validation)

### v0.4.0 (Feature)
- macOS support (.app bundle)
- Linux support (.AppImage)
- Settings panel (optional)
- Export results to PDF

### v0.5.0 (Long-term)
- Multi-language support
- Plugin system for custom rules
- Visualization improvements

---

## 📢 Community

### Links
- **GitHub:** https://github.com/Dumbo-programmer/Calcora
- **Website:** https://Dumbo-programmer.github.io/calcora/
- **Issues:** https://github.com/Dumbo-programmer/calcora/issues

### Contributing
Contributions welcome! See `CONTRIBUTING.md` for guidelines.

### License
MIT License — Free and open source forever.

---

## 🙏 Acknowledgments

- SymPy community for symbolic computation engine
- PyInstaller team for executable packaging
- Flask team for lightweight web framework
- All early testers and contributors

---

## 📝 Changelog Summary

```
v0.3.0 (2026-02-26)
- feat: Custom application icon with mathematical branding
- feat: Graceful shutdown system with UI button
- feat: Professional colored console output
- feat: Desktop mode badge in footer
- feat: Enhanced browser launch reliability
- improve: OS-managed port assignment (security)
- improve: Top-level exception boundary (no raw tracebacks)
- improve: Binary size reduction (22% smaller)
- improve: Windows exe metadata embedding
- fix: Port collision issues
- fix: Zombie process after browser close
- docs: Comprehensive pre-ship audit
- docs: Enhanced DESKTOP_GUIDE.md
```

---

**Upgrade Recommended:** All users should upgrade to v0.3.0 for improved stability and UX.

**Download:** [Calcora.exe (37.25 MB)](https://github.com/Dumbo-programmer/Calcora/releases/tag/v0.3.0)

---

*Calcora — Privacy-first, offline, explainable mathematics.*
