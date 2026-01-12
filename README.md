# Calcora

Calcora is an open-source, self-hosted computational mathematics engine designed to provide symbolic and numerical solutions with transparent, step-by-step reasoning. Unlike cloud-based tools, Calcora runs entirely on your own machine, making it ideal for classrooms, low-connectivity environments, and privacy-conscious users.

**Status**: v0.1 is an architecture-first alpha. The public API is intentionally small while the explainability engine stabilizes.

## 🎥 Demo Video

https://github.com/user-attachments/assets/bdb41766-a890-436f-9cc3-a4ffd5e603d4

## 🚀 Try the Live Demo
[![Netlify Status](https://api.netlify.com/api/v1/badges/e9aad821-2663-4238-80af-00966848f29e/deploy-status)](https://app.netlify.com/projects/calcoralive/deploys)



**[Interactive Demo →](https://calcoralive.netlify.app/demo.html)**

Test Calcora directly in your browser - no installation required. Try differentiation, matrix operations, and symbolic computation with step-by-step explanations.

## Why Calcora

- **Offline & private**: computation stays on your machine.
- **Explainable**: every result is backed by a deterministic, auditable reasoning DAG.
- **Extensible**: rule plugins, solver plugins, and renderer plugins.

## What Calcora is

- A **core engine** (deterministic rule application + step DAG)
- A **CLI** (`calcora ...`)
- A **developer API** (Python) and optional **HTTP API** (FastAPI)
- A **static website** (GitHub Pages) for docs and demos

## Install

### Quick Start (Clone & Run)

**New to the project? Follow the step-by-step guide: [CLONE_AND_RUN.md](CLONE_AND_RUN.md)**

**Prerequisites**: Python 3.11+ and Git

```bash
# 1. Clone the repository
git clone https://github.com/Dumbo-programmer/calcora.git
cd calcora

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install Calcora with dependencies
pip install -e ".[engine-sympy,cli,api]"

# 5. Test installation (optional but recommended)
python test_installation.py

# 6. Run the CLI
calcora differentiate "sin(x**2)"

# 7. Or start the web interface
uvicorn calcora.api.main:app --reload
# Then open: http://127.0.0.1:8000/static/index.html
```

That's it! You now have a fully functional local instance.

### Building Standalone Executables (Windows)

Want to share Calcora without requiring Python? Build standalone executables:

```powershell
# Install PyInstaller
pip install pyinstaller

# Build both CLI and server executables
.\build.ps1 all

# Executables are in dist/
.\dist\calcora.exe differentiate "x**2"
.\dist\calcora-server.exe  # Opens browser automatically

# Create distribution package
.\package.ps1
# Creates: dist/calcora-{version}-windows-x64.zip
```

See [BUILD.md](BUILD.md) for detailed build instructions.

### Self-Hosting the Web UI

Run your own Calcora web server:

```bash
# Development mode (auto-reload)
uvicorn calcora.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access from any device on your network at `http://YOUR-IP:8000/static/index.html`

**For complete self-hosting guide** (VPS, systemd, Nginx, SSL, etc.), see **[SELF_HOSTING.md](SELF_HOSTING.md)**.

For deployment to cloud platforms, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Docker (Coming Soon)

```bash
docker compose up
```

Docker deployment is on the roadmap for v0.2.

## Architecture (short)

Calcora represents computation as a directed acyclic graph (DAG) of **StepNodes**. Each step records:

- operation name
- applied rule
- input expression
- output expression
- human-readable explanation
- dependencies on prior steps

See [ARCHITECTURE.md](ARCHITECTURE.md) for the formal model.

### Supported operations (v0.1)

**Differentiation**:
- Constants and identity: d/dx(c) = 0, d/dx(x) = 1
- Sum rule: d/dx(f+g) = f' + g'
- Constant multiple: d/dx(c·f) = c·f'
- Product rule: d/dx(f·g) = f·g' + g·f'
- Power rule: d/dx(x^n) = n·x^(n-1) (with chain rule)
- Trigonometric: sin, cos, tan, sec, csc, cot (with chain rule)
- Exponential and logarithmic: exp(u), log(u) (with chain rule)
- Inverse trigonometric: asin(u), acos(u), atan(u) (with chain rule)
- SymPy fallback for complex expressions

**Linear Algebra**:
- Matrix multiplication
- Determinants (2×2, 3×3, general)
- Matrix inverse
- Row Reduced Echelon Form (RREF)
- Eigenvalues and eigenvectors
- LU decomposition
- **Symbolic matrices**: Variables as entries (e.g., [["a","b"],["c","d"]])

All operations include step-by-step explanations with multiple verbosity levels.

## Plugins

Calcora supports three plugin types:

- **Rule plugins**: symbolic transformations that emit StepNodes
- **Solver plugins**: algorithmic / numeric solvers (root finding, etc.)
- **Renderer plugins**: text, LaTeX, JSON, and future visualization

See [docs/PLUGINS.md](docs/PLUGINS.md).

## Roadmap

See [ROADMAP.md](ROADMAP.md) for v0.1 → v0.5.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

We follow a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming community.

## Security

For security concerns, please see our [Security Policy](SECURITY.md).

## License

Calcora is released under the [MIT License](LICENSE).

## License

MIT
