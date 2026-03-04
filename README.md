# Calcora — Transparent Computational Mathematics for Learning

**Calcora** is an open-source educational platform that provides step-by-step explanations for symbolic differentiation, integration, and linear algebra. Built on SymPy and designed for **transparency over power**, Calcora helps students understand *why* solutions work, not just *what* the answer is.

**Status**: v0.3.0 (Production-Ready Release)  
**Maturity**: Production-ready educational tool — suitable for Calculus I/II coursework and linear algebra

📚 **[Full Documentation](https://calcoralive.netlify.app/docs-user-guide)** | 🔧 **[API Reference](https://calcoralive.netlify.app/docs-api)** | 🚀 **[Live Demo](https://calcoralive.netlify.app/demo)** | 📋 **[Changelog](CHANGELOG.md)**

![Tests](https://img.shields.io/badge/tests-73%2F73%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-52%25-yellow)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
[![PyPI version](https://img.shields.io/pypi/v/calcora.svg)](https://pypi.org/project/calcora/)
![License](https://img.shields.io/badge/license-MIT-blue)

## Core Philosophy

1. **Pedagogical First**: Every operation shows step-by-step reasoning
2. **Transparent Algorithms**: Open-source implementation following standard textbooks (Stewart, Thomas, Anton)
3. **Self-Hosted Option**: Privacy-conscious educators can run locally (no data collection)
4. **Honest Limitations**: We document what we *can't* do (see Current Limitations below)

## 🖥️ Desktop App (Available Now - v0.3.0)

**Download → Double-click → Compute — No installation required!**

**[📥 Download Calcora.exe (37 MB)](https://github.com/Dumbo-programmer/Calcora/releases/latest/download/Calcora.exe)**

## 📦 PyPI Package (Available Now)

```bash
pip install calcora
```

**[View on PyPI →](https://pypi.org/project/calcora/)**

### Features:
- ✅ Single-file executable (Windows 10/11)
- ✅ Completely offline — no internet connection needed
- ✅ Auto-opens browser to localhost interface
- ✅ All your data stays on your computer (100% private)
- ✅ Custom application icon with professional branding
- ✅ Graceful shutdown system (no zombie processes)

### ⚠️ First-Run Security Warning

**Windows will show "Windows protected your PC" warning** — this is expected for unsigned open-source apps.

**Why?** Code signing certificates cost ~$200/year. v0.3.0 is unsigned; v0.3.1 will be signed.

**Is it safe?**
- ✅ Open source (audit the code on GitHub)
- ✅ Built with PyInstaller (standard Python packager)
- ✅ 100% offline, no telemetry
- ✅ SHA256: `53CE893F6A634043573111D43A8B07E62BCE4A9EC38E39B3D3F1AFF5C386A5EC`

**To run:** Click "More info" → "Run anyway" (warning only shows once)

**More details:** See [DESKTOP_GUIDE.md](DESKTOP_GUIDE.md) and [CODE_SIGNING_GUIDE.md](docs/CODE_SIGNING_GUIDE.md)

**Why desktop?** Web version requires internet and external hosting. Desktop version runs entirely on your machine - perfect for classrooms, exams, or offline use.

## What Works Well (v0.2)

### ✅ Current Capabilities
- **Symbolic Differentiation**: Product rule, chain rule, quotient rule, trigonometric functions
- **Integration**: 10 core techniques covering ~80% of Calculus II curriculum
  - Power rule, u-substitution, integration by parts (LIATE)
  - Partial fractions, trig identities, inverse trig patterns
  - Hyperbolic functions, exponentials, logarithms
  - Definite integrals with area visualization
- **Linear Algebra**: Matrix operations (determinant, inverse, eigenvalues, LU, RREF)
- **Interactive Graphs**: Chart.js visualizations for functions and definite integral areas
- **Three Verbosity Modes**: Concise / Detailed / Teacher Mode
- **LaTeX Export**: Export step-by-step solutions as LaTeX markup (NEW in v0.3.0)

### ⚠️ Current Limitations
- ❌ **Advanced Integration**: Trig substitution, Weierstrass, reduction formulas (v0.4 planned)
- ❌ **Series & Limits**: Not yet implemented (v0.4-0.5 roadmap)
- ❌ **Equation Solving**: Symbolic equation solving postponed to v0.4
- ⚠️ **Performance**: Not optimized for >50 term expressions or symbolic matrices >5×5
- ⚠️ **Accessibility**: WCAG 2.1 progress at ~85% (keyboard nav done, screen reader improvements ongoing)

## 🎥 Demo Video

https://github.com/user-attachments/assets/bdb41766-a890-436f-9cc3-a4ffd5e603d4

## 🚀 Try the Live Demo
[![Netlify Status](https://api.netlify.com/api/v1/badges/e9aad821-2663-4238-80af-00966848f29e/deploy-status)](https://app.netlify.com/projects/calcoralive/deploys)



**[Interactive Demo →](https://calcoralive.netlify.app/demo)**

Test Calcora directly in your browser - no installation required. Try:
- **Differentiation** with step-by-step explanations
- **Integration** with 8+ techniques and graph visualization
- **Matrix operations** (determinant, inverse, RREF, eigenvalues, LU decomposition)
- **Interactive graphs** for visualizing functions and definite integrals

**[📖 Complete Documentation →](https://calcoralive.netlify.app/docs-user-guide)**

## Target Audience

### ✅ Well-Suited For:
- Calculus I/II students verifying homework solutions
- Educators demonstrating integration techniques in lectures  
- Self-learners who want to see algorithmic steps, not just answers
- Privacy-conscious users wanting local computation

### ⚠️ Use With Caution:
- Advanced mathematics beyond Calculus II (results may be incomplete)
- Grading or assessment (manual verification recommended)
- Research computations (use SymPy/SageMath/Mathematica directly)

### ❌ Not Recommended For:
- Production scientific computing (performance/precision not optimized)
- Computer algebra research (SymPy itself is better suited)
- Mission-critical or peer-reviewed publications (insufficient validation)

## What's New in v0.2+

### 🚀 **Integration Engine** (NEW in v0.2)

Calculora's integration engine covers **standard Calculus II curriculum** (10 core techniques):

#### **What's Implemented** ✅
- ✅ **Polynomials** - Power rule for any degree
- ✅ **Trigonometric** - sin, cos, tan, sec² and standard identities
- ✅ **Inverse Trig** - arcsin, arctan patterns with automatic recognition
- ✅ **Hyperbolic** - sinh, cosh and their integrals
- ✅ **Exponential & Logarithmic** - e^x, ln(x), and basic products
- ✅ **Rational Functions** - Basic partial fraction decomposition
- ✅ **Square Roots** - √x and standard radical patterns
- ✅ **Products** - Integration by parts automatically applied
- ✅ **Compositions** - U-substitution for nested functions
- ✅ **Definite Integrals** - With numerical area calculation and visualization

#### **Advanced Graphing** 📊
Every integration now includes beautiful, interactive graphs:

**Indefinite Integrals:**
- 📈 Original function (integrand) f(x) plotted
- 📊 Integrated function (antiderivative) F(x) overlaid
- 🎨 Dual plotting for visual comparison

**Definite Integrals:**
- 📐 **Shaded area under the curve** showing the integral value
- 🎯 **Vertical lines** marking integration bounds
- 🔢 **Exact area value** displayed prominently
- 📈 Both integrand and antiderivative plotted together
- 🎨 Color-coded regions for positive/negative areas

#### **Intelligent Technique Detection** 🧠
The engine automatically selects the optimal integration method:
- **Power Rule** - For polynomials (instant)
- **Substitution** - For composite functions  
- **Integration by Parts** - For products (LIATE priority)
- **Partial Fractions** - For rational functions
- **Trigonometric Identities** - For trig combinations
- **Numerical Fallback** - For non-elementary integrals

#### **Validation** ✅
- ✅ **29/29 integration tests passing** (100% pass rate on implemented techniques)
- ✅ **Benchmark validation**: 25+ problems verified against SymPy (see [benchmarks/](benchmarks/))
- ⚠️ **Scope**: Covers ~80% of standard Calculus II textbook problems
- ❌ **Not Implemented**: Trig substitution, tabular integration, advanced reduction

See [INTEGRATION_FEATURES.md](INTEGRATION_FEATURES.md) and [benchmarks/README.md](benchmarks/README.md) for validation details.

### 🎯 Usage Examples

#### Indefinite Integral:
```python
from calcora.integration_engine import IntegrationEngine

engine = IntegrationEngine()
result = engine.integrate("x**2", variable="x", generate_graph=True)
# Output: x**3/3 + C
# Graph: Shows parabola f(x) = x² and cubic F(x) = x³/3
```

#### Definite Integral with Area:
```python
result = engine.integrate("x**2", variable="x", lower_limit=0, upper_limit=1)
# Output: 1/3 ≈ 0.333333
# Graph: Shows shaded area under parabola from 0 to 1
```

#### Complex Expression:
```python
result = engine.integrate("x * exp(x)")
# Output: (x - 1)·e^x + C
# Technique: Integration by parts
# Graph: Both functions plotted with clear relationship
```

#### LaTeX Export (NEW in v0.3.0):
```python
# Export solutions as LaTeX for homework assignments
from calcora.bootstrap import default_engine

engine = default_engine()
result = engine.run(operation="differentiate", expression="x**2", variable="x")

# Get LaTeX renderer
latex_renderer = engine.registry.get_renderer(format="latex")
latex_output = latex_renderer.render(result=result, format="latex", verbosity="detailed")

# Output: 
# % Calcora Differentiate Result
# \section*{Result}
# \[2 x\]
# ... (full step-by-step in LaTeX)
```

Or via API:
```bash
curl 'http://localhost:5000/differentiate?expr=x**2&format=latex'
```

### Coming Soon
- **Series Expansion**: Taylor and Maclaurin series
- **Limits**: Symbolic limit computation
- **Equation Solving**: Solve algebraic and transcendental equations
- **PyWebView GUI**: Native window wrapper (v0.4)

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

**Prerequisites**: Python 3.10+ and Git

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
- Determinants (2×2, 3×3, general n×n)
- Matrix inverse (with step-by-step Gauss-Jordan)
- Row Reduced Echelon Form (RREF)
- Eigenvalues and eigenvectors (with characteristic polynomial)
- **LU decomposition** with partial pivoting (PA = LU)
- Matrix rank
- **Symbolic matrices**: Variables as entries (e.g., [["a","b"],["c","d"]])

All operations include step-by-step explanations with multiple verbosity levels.

**[📖 Full API Documentation →](https://calcoralive.netlify.app/docs-api)**

## Plugins

Calcora supports three plugin types:

- **Rule plugins**: symbolic transformations that emit StepNodes
- **Solver plugins**: algorithmic / numeric solvers (root finding, etc.)
- **Renderer plugins**: text, LaTeX, JSON, and future visualization

See [docs/PLUGINS.md](docs/PLUGINS.md).

## Documentation

### For Users
- 📚 **[User Guide](https://calcoralive.netlify.app/docs-user-guide)** - Complete guide with examples
- 🔧 **[API Documentation](https://calcoralive.netlify.app/docs-api)** - REST API reference and Python SDK
- 🏠 **[Self-Hosting](https://calcoralive.netlify.app/docs-self-hosting)** - Deploy your own instance
- 🔨 **[Building from Source](https://calcoralive.netlify.app/docs-building)** - Desktop app and custom builds
- 📖 **[Getting Started](CLONE_AND_RUN.md)** - Quick setup guide

### For Developers
- 🏗️ **[Architecture](ARCHITECTURE.md)** - Technical design and DAG model
- 🔌 **[Plugins](docs/PLUGINS.md)** - Creating custom rules and solvers
- 🤝 **[Contributing](CONTRIBUTING.md)** - Development guidelines

### Release Documentation
- 📝 **[Release Notes v0.2.0](RELEASE_NOTES_v0.2.0.md)** - Security & Robustness release details
- 📋 **[Changelog](CHANGELOG.md)** - Complete version history
- 🎯 **[Release Summary v0.2.0](RELEASE_SUMMARY_v0.2.0.md)** - Release completion and metrics
- 🔍 **[Architecture Verification](ARCHITECTURE_VERIFICATION_v0.2.md)** - Pre-release validation audit
- 🗺️ **[Roadmap](ROADMAP.md)** - Feature timeline v0.1 → v0.5

### Policies
- 🛡️ **[Security Policy](SECURITY.md)** - Reporting vulnerabilities
- 📜 **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## References & Validation

### Academic Foundation

Calcora's algorithms are based on standard calculus textbooks and peer-reviewed libraries:

**Mathematical References:**
- Stewart, J. (2015). *Calculus: Early Transcendentals* (8th ed.). Cengage Learning.
- Thomas, G. B., Weir, M. D., & Hass, J. (2018). *Thomas' Calculus* (14th ed.). Pearson.
- Anton, H., Bivens, I., & Davis, S. (2021). *Calculus: Early Transcendentals* (12th ed.). Wiley.

**Software & Libraries:**
- **SymPy** - Meurer, A., et al. (2017). "SymPy: symbolic computing in Python." *PeerJ Computer Science*, 3, e103. https://doi.org/10.7717/peerj-cs.103
- **NumPy** - Harris, C.R., et al. (2020). "Array programming with NumPy." *Nature*, 585, 357-362. https://doi.org/10.1038/s41586-020-2649-2
- **FastAPI** - Modern Python web framework for building APIs with automatic documentation

### Integration Techniques Implemented

Based on standard calculus curriculum (Calculus II level):

1. **Power Rule**: ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C
2. **U-Substitution**: ∫ f(g(x))·g'(x) dx = F(g(x)) + C
3. **Integration by Parts**: ∫ u dv = uv - ∫ v du (LIATE priority)
4. **Partial Fractions**: Decomposition for rational functions
5. **Trigonometric Integrals**: Standard identities and substitutions
6. **Inverse Trig**: arctan, arcsin, arcsec patterns
7. **Hyperbolic Functions**: sinh, cosh, tanh and inverses
8. **Exponential/Logarithmic**: Natural base and general base handling
9. **Numerical Integration**: Simpson's rule fallback for non-elementary

### Test Coverage & Accuracy

**Current Status (v0.3.0):**
- ✅ **73/73 automated tests passing** (100% pass rate across all features)
- ✅ **52% overall code coverage** (differentiation: 89%, integration: 73%, matrices: 69%)
- ✅ **CI/CD**: GitHub Actions runs tests on 9 platform combinations (3 OS × 3 Python versions)
- ✅ **Edge case handling**: Complex numbers, infinite limits, domain errors

**Validation Methods:**
- Cross-verification with SymPy symbolic results
- Numerical comparison for definite integrals
- Manual verification against textbook solutions
- Edge case testing (discontinuities, undefined points, complex compositions)

**Known Limitations:**
- **Alpha software**: Active development, breaking changes possible
- **Missing techniques**: Trigonometric substitution, advanced partial fractions
- **Performance**: Not optimized for extremely complex expressions (>100 terms)
- **Accessibility**: WCAG compliance in progress (keyboard nav implemented, screen reader testing pending)
- **Browser support**: Modern browsers only (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

### Comparison with Alternatives

| Feature | **Calcora** | WolframAlpha | SymPy (direct) | Photomath |
|---------|-------------|--------------|----------------|-----------|
| **Cost** | Free (MIT) | Free (limited) / $5-7/mo | Free (open source) | Free (limited) / $10/mo |
| **Step-by-step** | ✅ Full detail | ⚠️ Pro only | ❌ No explanations | ✅ Yes |
| **Transparency** | ✅ Open source | ❌ Proprietary | ✅ Open source | ❌ Proprietary |
| **Integration** | ✅ 10+ techniques | ✅ Comprehensive | ✅ Symbolic only | ⚠️ Basic |
| **Differentiation** | ✅ All standard rules | ✅ Comprehensive | ✅ Symbolic only | ✅ Standard |
| **Graphs** | ✅ Interactive (Chart.js) | ✅ Static images | ❌ Matplotlib required | ⚠️ Limited |
| **Self-hosted** | ✅ Yes | ❌ Cloud only | ✅ Local Python | ❌ Cloud only |
| **Privacy** | ✅ Complete control | ❌ Data collected | ✅ Local compute | ❌ Data collected |
| **Verbosity levels** | ✅ 3 modes | ⚠️ Fixed | N/A | ⚠️ Fixed |
| **Citable** | ✅ Open algorithms | ❌ Black box | ✅ Published papers | ❌ Proprietary |
| **LaTeX export** | 🔄 Coming v0.3 | ✅ Available | ✅ Built-in | ❌ No |
| **API access** | ✅ Free, unlimited | ⚠️ Paid tiers | ✅ Python library | ❌ No public API |
| **Educational focus** | ✅ Primary goal | ⚠️ Secondary | ❌ Research tool | ✅ Primary goal |
| **Offline mode** | ✅ Full functionality | ❌ Internet required | ✅ Local install | ❌ Internet required |
| **Target audience** | Students, educators | General public | Researchers, devs | High school students |

**Key Differentiators:**
- **Transparency**: Only open-source tool with full step-by-step explanations
- **Privacy**: Self-hosted option means zero data collection
- **Cost**: Free forever, no paywalls or premium tiers
- **Educational**: Designed for learning, not just getting answers
- **Citable**: Algorithms are documented and reproducible

### Usage Recommendations

**Best for:**
- ✅ Calculus I/II students learning techniques
- ✅ Educators demonstrating step-by-step solutions
- ✅ Researchers needing reproducible symbolic computation
- ✅ Privacy-conscious users (FERPA/GDPR compliance)
- ✅ Offline computation (air-gapped environments)

**Not ideal for:**
- ❌ Extremely advanced mathematics (topology, abstract algebra)
- ❌ Production-critical scientific computing (use SymPy/SageMath directly)
- ❌ Non-technical users (WolframAlpha has better NLP)
- ❌ Mobile-first experience (responsive but not optimized)

**When to use alternatives:**
- **WolframAlpha**: Natural language queries, broader math coverage
- **SymPy**: Research-grade symbolic computation, performance critical
- **Photomath**: Handwriting recognition, mobile scanning
- **Mathematica**: Professional research, publication-quality outputs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

We follow a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming community.

## License

Calcora is released under the [MIT License](LICENSE).
