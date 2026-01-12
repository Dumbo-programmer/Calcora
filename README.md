# Calcora

(A fun personal tool which I decided to commit to and turn into something good and useable for everyone because why not.)
Calcora is an open-source, self-hosted computational mathematics engine designed to provide symbolic and numerical solutions with transparent, step-by-step reasoning. Unlike cloud-based tools, Calcora runs entirely on your own machine, making it ideal for classrooms, research, and privacy-conscious users.

**Status**: v0.2-alpha - Now with **Integration** support! Academic adoption features in active development.

📚 **[Complete Documentation](CLONE_AND_RUN.md)** | 🎓 **[Academic Strategy](ACADEMIC_STRATEGY.md)** | 🚀 **[Release Notes](RELEASE_NOTES_v0.2.md)**

## 🎯 Vision: Academic Adoption

Calcora aims to become the preferred computational tool for universities, STEM students, and researchers. We're building a transparent, educational alternative to WolframAlpha that emphasizes:
- **Step-by-step explanations** that help students learn
- **Open-source transparency** for research reproducibility
- **Zero cost** for educational institutions
- **Offline-first** for privacy and accessibility

**Phase 1 Features** (v0.2): Integration, Series Expansion, Limits, LaTeX Export, Equation Solving

See our [Academic Strategy Document](ACADEMIC_STRATEGY.md) for the complete roadmap.

## 🎥 Demo Video

https://github.com/user-attachments/assets/bdb41766-a890-436f-9cc3-a4ffd5e603d4

## 🚀 Try the Live Demo
[![Netlify Status](https://api.netlify.com/api/v1/badges/e9aad821-2663-4238-80af-00966848f29e/deploy-status)](https://app.netlify.com/projects/calcoralive/deploys)



**[Interactive Demo →](https://calcoralive.netlify.app/demo.html)**

Test Calcora directly in your browser - no installation required. Try:
- **Differentiation** with step-by-step explanations
- **Integration** (NEW!) with multiple techniques
- **Matrix operations** (determinant, inverse, RREF, eigenvalues, LU decomposition)
- **Interactive graphs** for visualizing functions

## Why Calcora

- **Offline & private**: computation stays on your machine.
- **Explainable**: every result is backed by a deterministic, auditable reasoning DAG.
- **Educational**: detailed step-by-step explanations help students understand the process.
- **Extensible**: rule plugins, solver plugins, and renderer plugins.
- **Modern UI**: Glassmorphism design with dark mode support.

## What's New in v0.2

### 🆕 Integration Engine
- **Indefinite integrals**: Automatic technique detection (power rule, substitution, by parts, trigonometric)
- **Definite integrals**: Fundamental theorem of calculus with bounds
- **Step-by-step**: Detailed explanations showing which technique is used and why
- **Interactive graphs**: Visualize area under curve for definite integrals
- **Verbosity levels**: Choose between concise, detailed, or teacher mode explanations

Example:
```python
from calcora.integration_engine import IntegrationEngine

engine = IntegrationEngine()
result = engine.integrate("x**2", variable="x")
# Returns: x**3/3 + C with step-by-step explanation

result = engine.integrate("x**2", variable="x", lower_limit=0, upper_limit=1)
# Returns: 1/3 (definite integral)
```

### Coming Soon
- **Series Expansion**: Taylor and Maclaurin series
- **Limits**: Symbolic limit computation
- **LaTeX Export**: Export results as publication-ready LaTeX
- **Equation Solving**: Solve algebraic and transcendental equations

## What Calcora is

- A **core engine** (deterministic rule application + step DAG)
- An **integration engine** (multiple integration techniques with explanations)
- A **CLI** (`calcora ...`)
- A **developer API** (Python) and **HTTP API** (FastAPI)
- A **modern web interface** with interactive graphs and step-by-step explanations
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

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed build and distribution instructions.

### Self-Hosting the Web UI

Run your own Calcora web server:

```bash
# Development mode (auto-reload)
uvicorn calcora.api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access from any device on your network at `http://YOUR-IP:8000/static/index.html`

For complete deployment guide (cloud platforms, Docker, systemd, etc.), see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

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

## Documentation

### For Users
- 📚 **[Getting Started](CLONE_AND_RUN.md)** - Complete setup guide from clone to running
- 🚀 **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy to Netlify, Render, or self-host
- 📖 **[SEO Guide](SEO_GUIDE.md)** - Optimize discoverability and marketing

### For Developers
- 🏗️ **[Architecture](ARCHITECTURE.md)** - Technical design and DAG model
- 🔌 **[Plugins](docs/PLUGINS.md)** - Creating custom rules and solvers
- 🤝 **[Contributing](CONTRIBUTING.md)** - Development guidelines

### Project Management
- 🎯 **[Academic Strategy](ACADEMIC_STRATEGY.md)** - v0.2 roadmap for university adoption
- 🗺️ **[Roadmap](ROADMAP.md)** - Feature timeline v0.1 → v0.5
- 📝 **[Release Notes v0.2](RELEASE_NOTES_v0.2.md)** - What's new in integration engine
- 📋 **[Changelog](CHANGELOG.md)** - Version history

### Policies
- 🛡️ **[Security Policy](SECURITY.md)** - Reporting vulnerabilities
- 📜 **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

We follow a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming community.

## License

Calcora is released under the [MIT License](LICENSE).
