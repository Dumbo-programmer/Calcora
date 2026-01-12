# Clone & Run Verification Guide

This document verifies that anyone can clone Calcora and get it running.

## ✅ Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Git installed (`git --version`)
- [ ] Internet connection (for pip downloads)

## 🚀 Clone & Run (5 Minutes)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR-USERNAME/calcora.git
cd calcora
```

**Verify**: You should see files like `README.md`, `pyproject.toml`, `src/`

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

**Verify**: A `.venv/` directory should now exist

### Step 3: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Verify**: Your prompt should now show `(.venv)` at the beginning

### Step 4: Install Calcora

```bash
pip install --upgrade pip
pip install -e ".[engine-sympy,cli,api]"
```

**Verify**: This should complete without errors. Takes 1-2 minutes.

### Step 5: Test Installation

```bash
python test_installation.py
```

**Expected output:**
```
Testing Calcora installation...

✓ Test 1: Importing modules...
  ✓ Core modules imported successfully

✓ Test 2: Creating engine...
  ✓ Engine created successfully

✓ Test 3: Testing differentiation...
  ✓ d/dx(x²) = 2*x

✓ Test 4: Testing matrix operations...
  ✓ det([[1,2],[3,4]]) = -2

✓ Test 5: Testing symbolic matrices...
  ✓ det([[a,b],[c,d]]) = a*d - b*c

==================================================
✓ All tests passed! Calcora is ready to use.
==================================================
```

If all tests pass, **installation successful! ✅**

### Step 6: Try the CLI

```bash
# Differentiation
calcora differentiate "x**2 + sin(x)"

# Matrix determinant
calcora matrix-determinant "[[1,2],[3,4]]"

# Get help
calcora --help
```

### Step 7: Start Web Interface

```bash
uvicorn calcora.api.main:app --reload
```

Then open in your browser: http://127.0.0.1:8000/static/index.html

You should see the Calcora web interface!

Press `CTRL+C` to stop the server.

---

## ✅ Success Checklist

- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed without errors
- [ ] `test_installation.py` passes all tests
- [ ] CLI commands work (`calcora --help`)
- [ ] Web interface loads in browser

If all checkboxes are checked, you have successfully:
- ✅ Cloned Calcora
- ✅ Installed all dependencies
- ✅ Verified the installation
- ✅ Run CLI and web interface

**You can now use Calcora or start developing!**

---

## 🔧 Troubleshooting

### "python: command not found"

**Fix**: Install Python 3.11+ from python.org

### "pip: command not found"

**Fix**: 
```bash
python -m ensurepip --upgrade
```

### "ModuleNotFoundError: No module named 'calcora'"

**Cause**: Virtual environment not activated or installation failed

**Fix**:
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows

# Reinstall
pip install -e ".[engine-sympy,cli,api]"
```

### "Permission denied" (Linux/macOS)

**Fix**: Don't use `sudo`. Use virtual environment instead.

### uvicorn not found

**Fix**: 
```bash
pip install uvicorn
# Or reinstall with API dependencies
pip install -e ".[engine-sympy,cli,api]"
```

### Port 8000 already in use

**Fix**: Use different port
```bash
uvicorn calcora.api.main:app --port 8080
# Then open: http://127.0.0.1:8080/static/index.html
```

### Tests fail

**Check**:
1. Virtual environment is activated
2. All dependencies installed: `pip list | grep -E "sympy|pydantic|typer"`
3. You're in the `calcora` directory
4. Python version is 3.11+: `python --version`

If still failing, open an issue on GitHub with the error message.

---

## 📚 Next Steps

Now that you have Calcora running:

- **Explore the CLI**: Try different mathematical expressions
- **Use the web UI**: Test differentiation and matrix operations
- **Read the docs**: Check out [ARCHITECTURE.md](ARCHITECTURE.md) and [ROADMAP.md](ROADMAP.md)
- **Build executables**: See [BUILD.md](BUILD.md) (Windows only)
- **Self-host on a server**: See [SELF_HOSTING.md](SELF_HOSTING.md)
- **Deploy to cloud**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💬 Support

- **Documentation**: Start with [README.md](README.md)
- **Issues**: Report bugs on GitHub Issues
- **Questions**: Open a Discussion on GitHub

---

**That's it!** You've successfully cloned and run Calcora. 🎉

Time taken: ~5 minutes  
Difficulty: Easy (if prerequisites met)  
Cost: $0
