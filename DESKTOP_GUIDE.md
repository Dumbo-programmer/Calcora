# Calcora Desktop App - Architecture & Development Guide

**Version:** 0.3.0 (in development)  
**Status:** Planning → Implementation → Testing → Release  
**Target Release:** Q2 2026

---

## 🎯 Vision

Transform Calcora from a web-only tool into a **professional desktop application** that users can:
- Download once
- Double-click to run
- Use completely offline
- Update with a single click

**Key principle:** Maximum simplicity for end users.

---

## 🏗️ Architecture

### Current (v0.2.1)
```
User Browser
    ↓
https://calcoralive.netlify.app (Netlify static hosting)
    ↓
https://calcora.onrender.com/api/compute (Render backend API)
```

**Limitations:**
- Requires internet connection
- Dependent on external hosting
- Slower (network latency)
- Complex deployment

### Desktop App (v0.3.0+)
```
Calcora.exe / Calcora.app / calcora (Linux binary)
    │
    ├── Embedded Python 3.11 runtime (PyInstaller)
    ├── Flask API server (localhost:8000)
    ├── Static web UI (bundled site/ directory)
    ├── Auto-browser launcher (webbrowser module)
    ├── NumPy + SymPy (embedded)
    └── Update checker (GitHub Releases API)
```

**Advantages:**
- ✅ No internet required
- ✅ Instant response (no network latency)
- ✅ Single-file executable
- ✅ Full offline capability
- ✅ Professional user experience

---

## 📦 Components

### 1. Desktop Launcher (`calcora_desktop.py`)

**Responsibilities:**
- Check port availability (8000-8010)
- Start Flask server on `127.0.0.1` (NEVER `0.0.0.0`)
- Auto-open browser to `http://127.0.0.1:PORT`
- Handle graceful shutdown (Ctrl+C)

**Security Features:**
- Localhost-only binding (not exposed to internet)
- Port scanning before start
- Clean error messages for users

**Code:**
```python
def main():
    port = find_available_port()
    threading.Thread(target=open_browser, args=(port,)).start()
    app.run(host='127.0.0.1', port=port, debug=False)
```

### 2. PyInstaller Spec (`calcora-desktop.spec`)

**Bundle includes:**
- Python 3.11 runtime
- Flask + dependencies
- SymPy (symbolic math)
- **NumPy** (CRITICAL - required for integration!)
- site/ directory (HTML/CSS/JS)
- api_server.py

**Bundle excludes:**
- matplotlib (optional, heavy)
- scipy (not used)
- pandas (not used)
- Jupyter (dev only)

**Build command:**
```powershell
pyinstaller calcora-desktop.spec --clean --noconfirm
```

### 3. Build Scripts

**Windows:** `build-desktop.ps1`
- Checks venv activation
- Installs PyInstaller
- Runs build
- Tests executable

**Cross-platform:** GitHub Actions (`.github/workflows/build-desktop.yml`)
- Matrix build: Windows, macOS, Linux
- Automatic releases on version tags
- Artifact uploads

### 4. Static Web UI

**Bundled from `site/` directory:**
- index.html (landing page)
- demo.html (interactive calculator)
- style.css, modern-theme.css
- ui-enhancements.js

**How bundling works:**
```python
datas=[('site', 'site'), ...]  # PyInstaller spec
```

At runtime, Flask serves from bundled directory:
```python
app = Flask(__name__, static_folder='site')
```

---

## 🔨 Development Workflow

### Phase 1: Local Testing (Current)

1. **Activate venv:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Run desktop launcher directly:**
   ```powershell
   python calcora_desktop.py
   ```
   - Tests auto-browser opening
   - Tests port detection
   - Tests Flask server

3. **Test integration features:**
   - Differentiation
   - Integration (requires numpy!)
   - Matrix operations

### Phase 2: Build & Test

1. **Build executable:**
   ```powershell
   .\build-desktop.ps1
   ```
   Output: `dist\Calcora.exe` (Windows)

2. **Test executable:**
   ```powershell
   .\dist\Calcora.exe
   ```
   - Should auto-open browser
   - Should bind to localhost only
   - Should handle Ctrl+C gracefully

3. **Check size:**
   - Target: < 50 MB (ideal)
   - Typical: 30-40 MB (with numpy)
   - Over 100 MB → investigate bloat

### Phase 3: Package for Distribution

1. **Create release package:**
   ```powershell
   .\package-desktop.ps1
   ```
   Output: `dist\calcora-desktop-0.3.0-windows-x64.zip`

2. **Package contents:**
   - Calcora.exe
   - README.md
   - LICENSE
   - QUICK_START.txt

### Phase 4: CI/CD (GitHub Actions)

1. **Tag release:**
   ```bash
   git tag v0.3.0
   git push origin v0.3.0
   ```

2. **Automatic build matrix:**
   - Windows (x64)
   - macOS (Universal Binary)
   - Linux (x64)

3. **Automatic release:**
   - Creates GitHub Release
   - Uploads binaries
   - Generates release notes

---

## 🔐 Security Checklist

**Before Desktop Release:**

- [ ] Bind ONLY to `127.0.0.1` (never `0.0.0.0`)
- [ ] Disable Flask debug mode
- [ ] No stack traces in production
- [ ] Input validation via `input_validator.py`
- [ ] Timeout protection via `timeout_wrapper.py`
- [ ] Version string in UI footer
- [ ] Code signing (Windows: Authenticode, macOS: Apple Developer ID)
- [ ] Antivirus false positive mitigation
- [ ] No embedded secrets/API keys

**Why localhost-only matters:**
```python
# BAD - Exposes to network (security risk!)
app.run(host='0.0.0.0', port=8000)

# GOOD - Local only (safe)
app.run(host='127.0.0.1', port=8000)
```

---

## 📊 Build Matrix

| Platform | Binary Name | Size Target | Build Time |
|----------|-------------|-------------|------------|
| Windows x64 | Calcora.exe | 30-40 MB | 3-5 min |
| macOS Universal | Calcora.app | 35-45 MB | 5-7 min |
| Linux x64 | calcora | 30-40 MB | 3-5 min |

**GitHub Actions runners:**
- windows-latest (Windows Server 2022)
- macos-latest (macOS 13)
- ubuntu-latest (Ubuntu 22.04)

---

##  Updates Strategy

### Phase 1 (v0.3.0): Manual Updates

**On startup:**
1. Check GitHub Releases API:
   ```python
   response = requests.get('https://api.github.com/repos/Dumbo-programmer/Calcora/releases/latest')
   latest_version = response.json()['tag_name']
   ```

2. Compare versions:
   ```python
   if latest_version > current_version:
       show_update_banner()
   ```

3. **User action:**
   - Click "Download" → Opens GitHub Releases page
   - User manually downloads and replaces

**Advantages:**
- Simple & safe
- No auto-execution risk
- User stays in control

**Implementation priority:** v0.3.1 (not v0.3.0)

### Phase 2 (v0.4.0+): Optional Auto-Updater

**Only if adoption grows significantly.**

Possible tools:
- PyUpdater
- electron-updater (if migrating to Electron)
- Custom solution with signature verification

**Security requirements:**
- HTTPS-only downloads
- SHA256 signature verification
- User confirmation required
- Rollback capability

---

## 🚀 Release Process

### Pre-Release Checklist

1. **Version bump:**
   ```toml
   # pyproject.toml
   version = "0.3.0"
   ```

2. **Update CHANGELOG.md:**
   ```markdown
   ## [0.3.0] - 2026-XX-XX
   ### Added
   - Desktop application (Windows, macOS, Linux)
   - Auto-browser launcher
   - Offline-first architecture
   ```

3. **Test on all platforms:**
   - Windows 10, Windows 11
   - macOS 13+
   - Ubuntu 22.04, Debian 12

4. **Security audit:**
   - No exposed ports
   - Input validation working
   - Timeout protection active

### Release Steps

1. **Create tag:**
   ```bash
   git tag -a v0.3.0 -m "Desktop app release"
   git push origin v0.3.0
   ```

2. **GitHub Actions auto-builds:**
   - Builds all platforms
   - Creates draft release
   - Uploads artifacts

3. **Manual verification:**
   - Download each platform binary
   - Test on real hardware
   - Verify signatures

4. **Publish release:**
   - Edit release notes
   - Mark as latest
   - Announce on GitHub/social

---

## 📚 User Documentation Updates

### README.md Updates

**Add section:**
```markdown
## 🖥️ Desktop App (Recommended)

**Download and run - no installation needed!**

### Windows
1. Download `calcora-windows-x64.zip` from [Releases](https://github.com/Dumbo-programmer/Calcora/releases)
2. Extract ZIP
3. Double-click `Calcora.exe`
4. Browser opens automatically!

### macOS
1. Download `calcora-macos-universal.tar.gz`
2. Extract → Drag to Applications
3. Open Calcora.app
4. Allow in System Preferences if prompted

### Linux
1. Download `calcora-linux-x64.tar.gz`
2. Extract: `tar -xzf calcora-linux-x64.tar.gz`
3. Run: `chmod +x calcora && ./calcora`

**Privacy:** All computation runs locally. No data sent to servers.
```

---

## 🐛 Known Issues & Mitigations

### Issue 1: Antivirus False Positives

**Problem:** PyInstaller executables often flagged by antivirus

**Mitigations:**
1. Code signing (Authenticode/Apple Developer ID)
2. Submit to antivirus vendors for whitelisting
3. Build on GitHub Actions (trusted environment)
4. Publish SHA256 hashes for verification

### Issue 2: macOS Gatekeeper

**Problem:** "Calcora.app is from an unidentified developer"

**User instructions:**
1. Right-click → Open (not double-click)
2. Or: System Preferences → Security → Allow

**Long-term fix:** Apple Developer ID signing ($99/year)

### Issue 3: Large Binary Size

**Current:** ~35 MB with numpy  
**Bloat sources:** numpy, SymPy, Flask

**Optimizations:**
- UPX compression (already enabled)
- Exclude unnecessary SymPy modules
- Consider Nuitka instead of PyInstaller (v0.4+)

---

## 🔮 Future Enhancements (v0.4+)

### Optional: Electron/Tauri Wrapper

**Advantages:**
- Better desktop integration
- Native menus, notifications
- Smaller update packages
- Modern UI framework

**Disadvantages:**
- Larger binary (~100-150 MB)
- More complex build process
- Two languages (Python + JS)

**Recommendation:** Only if desktop version sees significant adoption (1000+ users)

### Optional: Native UI (PyQt/Tkinter)

**Advantages:**
- True native app (no browser)
- Smaller binary
- Better performance

**Disadvantages:**
- Rewrite entire UI
- Lose web demo compatibility
- More maintenance

**Recommendation:** Not worth it - web UI is already excellent

---

## 📋 Development Checklist

**For v0.3.0 Release:**

### Core Development
- [x] Create `calcora_desktop.py` launcher
- [x] Create `calcora-desktop.spec` PyInstaller config
- [x] Fix numpy exclusion bug in old specs
- [x] Add auto-browser opening
- [x] Add port detection (8000-8010)
- [ ] Test on Windows 10/11
- [ ] Test on macOS 13+
- [ ] Test on Ubuntu 22.04

### Build & CI
- [x] Create `build-desktop.ps1` script
- [x] Create `package-desktop.ps1` script
- [x] Create GitHub Actions workflow
- [ ] Test GitHub Actions build
- [ ] Set up code signing (optional)

### Documentation
- [x] Create DESKTOP_GUIDE.md
- [ ] Update README.md with desktop instructions
- [ ] Create QUICK_START.txt for packages
- [ ] Record demo video (optional)

### Testing
- [ ] Integration tests work offline
- [ ] Browser auto-opens correctly
- [ ] Port conflict handling works
- [ ] Ctrl+C shutdown graceful
- [ ] No stack traces shown to users
- [ ] Performance acceptable (< 3s startup)

### Release
- [ ] Version bump to 0.3.0
- [ ] Update CHANGELOG.md
- [ ] Create release tag
- [ ] Publish GitHub Release
- [ ] Announce on GitHub/social

---

## 📞 Support Channels

**For desktop app issues:**

1. **GitHub Issues:** Bug reports, feature requests
2. **GitHub Discussions:** General questions, help
3. **README.md:** Installation instructions
4. **QUICK_START.txt:** In-package guide

---

**Last Updated:** February 24, 2026  
**Next Review:** Before v0.3.0 release  
**Maintainer:** @Dumbo-programmer
