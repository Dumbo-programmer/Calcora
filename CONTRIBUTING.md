# Contributing to Calcora

**Welcome!** Calcora aims to be research-grade, explainable, and contributor-friendly.

This guide helps you understand the codebase and make meaningful contributions.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Architecture](#understanding-the-architecture)
3. [Development Workflow](#development-workflow)
4. [Code Standards](#code-standards)
5. [Testing Strategy](#testing-strategy)
6. [Common Tasks](#common-tasks)
7. [How Decisions Are Made](#how-decisions-are-made)
8. [Getting Help](#getting-help)

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/calcora.git
cd calcora
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install with development dependencies
python -m pip install -e ".[engine-sympy,cli,api,dev]"
```

### 2. Verify Installation

```bash
# Run tests (should see 43/43 passing)
pytest

# Check coverage (should see ~47%)
pytest --cov=src/calcora --cov-report=term-missing

# Run linters
ruff check src/
mypy src/
```

### 3. Explore the Codebase

```bash
# See project structure
tree src/calcora -L 2

# Read architecture docs
cat docs/ARCHITECTURE.md
cat docs/ADR/README.md
```

**You're ready!** Pick an issue labeled `good-first-issue` and start contributing.

---

## Understanding the Architecture

**Goal:** Understand the codebase in 30 minutes.

### The Big Picture

Calcora is a **step-by-step explanation engine** for Calculus I/II, not a traditional Computer Algebra System (CAS).

```
User Input → Parser → Technique Detection → Symbolic Computation → Step Generation → Renderer → Output
   "∫x·e^x dx"  │         │                     │                      │               │         "Steps + Answer"
                │         │                     │                      │               │
                │         └─ integration_engine.py                     │               └─ text/JSON/LaTeX
                │                               │                      │
                └─ SymPy                        └─ SymPy              └─ step_engine.py (DAG)
```

### Key Components

#### 1. **Integration Engine** (`src/calcora/integration_engine.py`)
- **Purpose:** Detect integration technique and generate step-by-step explanation
- **Main Classes:**
  - `IntegrationStep`: Single step in explanation
  - `IntegrationEngine`: Orchestrates integration process
- **Key Method:** `integrate(expression, variable, lower_limit, upper_limit, verbosity, generate_graph)`
- **Returns:** `dict` with `success`, `output`, `steps`, `technique`, `graph`
- **Why separate from step_engine?** See [ADR-001](docs/ADR/ADR-001-separate-integration-engine.md)

#### 2. **Step Engine** (`src/calcora/step_engine.py`)
- **Purpose:** Generic DAG (Directed Acyclic Graph) construction for step-by-step reasoning
- **Data Model:** `StepNode` with `id`, `operation`, `rule`, `input`, `output`, `explanation`, `dependencies`, `metadata`
- **Used By:** Differentiation (currently), Integration (future convergence)
- **Design Principles:** Determinism, auditability, separation of concerns, safety
- **Why DAG?** Allows branching explanations (e.g., "Alternative method: by parts")

#### 3. **SymPy Backend** (external dependency)
- **Purpose:** Symbolic computation correctness
- **What we use:** `sp.sympify()`, `sp.integrate()`, `sp.diff()`, `sp.simplify()`
- **Why SymPy?** Peer-reviewed, Python-native, actively maintained — See [ADR-002](docs/ADR/ADR-002-sympy-as-backend.md)
- **Our Value-Add:** Technique detection + step-by-step explanation (SymPy gives answers, we explain *why*)

#### 4. **API Layer** (`src/calcora/api/`)
- **Framework:** FastAPI
- **Endpoints:**
  - `POST /integrate` — Integration with steps
  - `POST /differentiate` — Differentiation with steps
  - `GET /health` — Health check
- **Why FastAPI?** Auto-generated OpenAPI docs, Pydantic validation, async support

#### 5. **Frontend** (`frontend/`)
- **Framework:** Vanilla JavaScript + Chart.js
- **Files:**
  - `demo.html` — Main UI
  - `app.js` — Integration with backend API
  - `styles.css` — Bootstrap-based styling
- **Why vanilla JS?** Keep it simple, no build step, easy for educators to customize

### File Organization

```
calcora/
├── src/calcora/                  # Backend Python package
│   ├── integration_engine.py    # Integration logic (700 lines)
│   ├── step_engine.py            # Step DAG model (400 lines)
│   ├── api/                      # FastAPI endpoints
│   ├── cli/                      # Command-line interface
│   └── renderers/                # Output formatting
├── frontend/                     # Frontend (HTML/CSS/JS)
│   ├── demo.html
│   └── app.js
├── tests/                        # Test suite
│   ├── integration/              # Integration engine tests (43 tests)
│   └── unit/                     # Unit tests
├── benchmarks/                   # Validation scripts
│   └── validate_integration.py  # SymPy cross-validation
├── docs/
│   └── ADR/                      # Architecture Decision Records
├── docs/
│   ├── ARCHITECTURE.md          # Design principles
│   ├── CODING_STANDARDS.md      # Style guide
│   ├── VERSIONING.md            # SemVer policy
│   ├── ROADMAP.md               # Public roadmap
│   └── ADR/                     # Architecture decisions
├── CONTRIBUTING.md              # This file
└── README.md                    # Project overview
```

### Data Flow Example: `∫x·e^x dx`

1. **User Input:** `"x * exp(x)"`, variable `"x"`
2. **Parser:** SymPy converts to symbolic expression
3. **Technique Detection:** `integration_engine._detect_technique()` sees product → checks LIATE priority → returns `"integration_by_parts"`
4. **Symbolic Computation:** `sp.integrate(x * exp(x), x)` → `x*exp(x) - exp(x)`
5. **Step Generation:** Create list of `IntegrationStep` objects:
   - Step 1: "Select u and dv using LIATE priority"
   - Step 2: "Let u = x, dv = exp(x) dx"
   - Step 3: "Compute du = dx, v = exp(x)"
   - Step 4: "Apply integration by parts formula"
   - Step 5: "Simplify: x*exp(x) - ∫exp(x) dx"
   - Step 6: "Evaluate remaining integral: exp(x)"
   - Step 7: "Combine: x*exp(x) - exp(x) + C"
6. **Renderer:** Convert steps to JSON/text/LaTeX
7. **Output:** Return `dict` with `success=True`, `output="x*exp(x) - exp(x) + C"`, `steps=[...]`, `technique="integration_by_parts"`

**Time to understand:** ~20 minutes of reading code after this overview.

---

## Development Workflow

### Branching Strategy

```
main ──────────────────────────────── (Production: v0.2.0, v0.3.0, ...)
  └── dev ──────────────────────────── (Integration branch: all features merge here first)
       ├── feature/add-trig-substitution
       ├── bugfix/definite-integral-limits
       └── docs/update-roadmap
```

**Rules:**
1. **Never commit directly to `main`** (protected branch)
2. **All changes go to `dev` first** via Pull Request
3. **Use descriptive branch names:** `feature/`, `bugfix/`, `docs/`, `test/`, `refactor/`

### Creating a Feature

```bash
# 1. Start from latest dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/add-trig-substitution

# 3. Make changes, commit frequently
git add src/calcora/integration_engine.py tests/integration/test_trig_sub.py
git commit -m "feat: add trigonometric substitution for sqrt(a^2 - x^2)"

# 4. Push to GitHub
git push origin feature/add-trig-substitution

# 5. Open Pull Request: feature/add-trig-substitution → dev
# (Use GitHub web UI)
```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature (e.g., `feat(integration): add trig substitution`)
- `fix`: Bug fix (e.g., `fix(integration): handle definite integrals with string limits`)
- `docs`: Documentation only (e.g., `docs(roadmap): update v0.3 timeline`)
- `test`: Add tests (e.g., `test(integration): add edge cases for improper integrals`)
- `refactor`: Code restructuring (e.g., `refactor(engine): extract technique detection to separate file`)
- `chore`: Maintenance (e.g., `chore: update dependencies`)

**Examples:**
```bash
git commit -m "feat(integration): add trigonometric substitution technique"
git commit -m "fix(api): return 400 for invalid expressions instead of 500"
git commit -m "docs(adr): add ADR-004 for caching strategy"
git commit -m "test(integration): improve coverage for rational functions"
```

### Code Review Process

**All PRs require:**
1. ✅ **Passing CI** (43/43 tests, linting clean)
2. ✅ **Coverage maintained** (don't drop below 47%)
3. ✅ **Coding standards met** (see [CODING_STANDARDS.md](docs/CODING_STANDARDS.md))
4. ✅ **Reviewer approval** (at least 1 maintainer)

**Review Checklist** (from [CODING_STANDARDS.md](docs/CODING_STANDARDS.md)):
- [ ] All tests passing
- [ ] Coverage not decreased
- [ ] Docstrings for new functions
- [ ] Type hints present
- [ ] No magic numbers (use named constants)
- [ ] Max 50 lines per function
- [ ] Max 4 nesting levels
- [ ] Commit messages follow Conventional Commits
- [ ] CHANGELOG.md updated (if user-facing change)

---

## Code Standards

**Full details:** [CODING_STANDARDS.md](docs/CODING_STANDARDS.md)

**Quick summary:**

### Naming Conventions
- **Classes:** `PascalCase` (e.g., `IntegrationEngine`)
- **Functions/variables:** `snake_case` (e.g., `detect_technique`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_ITERATIONS`)
- **Private:** `_leading_underscore` (e.g., `_internal_helper`)

### Documentation
```python
def integrate(expression: str, variable: str, verbosity: str = "concise") -> dict:
    """
    Perform symbolic integration with step-by-step explanation.
    
    Args:
        expression: Mathematical expression (e.g., "x**2 + sin(x)")
        variable: Variable to integrate with respect to (e.g., "x")
        verbosity: Explanation detail level ("concise" | "detailed" | "teacher")
    
    Returns:
        dict: {
            "success": bool,
            "output": str,
            "steps": List[dict],
            "technique": str,
            "error": Optional[str]
        }
    
    Raises:
        ValueError: If expression is invalid or variable not found
    
    Example:
        >>> engine = IntegrationEngine()
        >>> result = engine.integrate("x**2", "x")
        >>> result["success"]
        True
        >>> result["output"]
        "x**3/3 + C"
    """
```

### Complexity Limits
- **Max 50 lines per function** (excluding docstring)
- **Max 500 lines per file**
- **Max 4 nesting levels**

If you exceed these, refactor:
```python
# ❌ Bad: 6 nesting levels
if technique == "by_parts":
    if LIATE_priority:
        for term in expression:
            if term.is_product:
                for factor in term.factors:
                    if factor.is_exponential:
                        # Too deep!

# ✅ Good: Extract to helper
if technique == "by_parts":
    u, dv = self._select_u_dv_by_liate(expression)
```

---

## Testing Strategy

### Test Structure

```
tests/
├── integration/                # Integration tests (full workflows)
│   └── test_integration_engine.py  # 43 tests covering 10 techniques
├── unit/                       # Unit tests (individual functions)
│   ├── test_step_engine.py
│   └── test_technique_detection.py
└── benchmarks/                 # Validation against SymPy
    └── validate_integration.py
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/integration/test_integration_engine.py

# Specific test
pytest tests/integration/test_integration_engine.py::TestBasicPolynomials::test_quadratic

# With coverage
pytest --cov=src/calcora --cov-report=html
# Open htmlcov/index.html in browser

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Writing Tests

```python
import pytest
from calcora.integration_engine import IntegrationEngine

class TestTrigSubstitution:
    """Tests for ∫ 1/sqrt(a^2 - x^2) dx using trig substitution."""
    
    @pytest.fixture
    def engine(self):
        """Provide IntegrationEngine instance for all tests."""
        return IntegrationEngine()
    
    def test_basic_arcsine_form(self, engine):
        """Test ∫ 1/sqrt(1 - x^2) dx = arcsin(x) + C."""
        result = engine.integrate("1/sqrt(1 - x**2)", "x")
        
        assert result["success"], f"Integration failed: {result.get('error')}"
        assert result["technique"] == "trig_substitution"
        assert "arcsin" in result["output"]
        assert len(result["steps"]) >= 3, "Should show substitution steps"
    
    def test_scaled_form(self, engine):
        """Test ∫ 1/sqrt(4 - x^2) dx = arcsin(x/2) + C."""
        result = engine.integrate("1/sqrt(4 - x**2)", "x")
        
        assert result["success"]
        assert "arcsin(x/2)" in result["output"] or "asin(x/2)" in result["output"]
    
    @pytest.mark.parametrize("a,expected", [
        (1, "arcsin(x)"),
        (2, "arcsin(x/2)"),
        (3, "arcsin(x/3)"),
    ])
    def test_parameterized_forms(self, engine, a, expected):
        """Test ∫ 1/sqrt(a^2 - x^2) dx for various a values."""
        expr = f"1/sqrt({a**2} - x**2)"
        result = engine.integrate(expr, "x")
        
        assert result["success"]
        assert expected in result["output"]
```

### Test Markers

```python
@pytest.mark.slow  # For tests taking >1s
@pytest.mark.integration  # For end-to-end tests
@pytest.mark.unit  # For isolated function tests

# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

---

## Common Tasks

### Task 1: Add a New Integration Technique

**Example:** Adding trigonometric substitution

1. **Update `_detect_technique()` in `integration_engine.py`:**
   ```python
   def _detect_technique(self, expr, var):
       # ... existing checks ...
       
       # Check for sqrt(a^2 - x^2) patterns
       if self._is_sqrt_difference_of_squares(expr, var):
           return "trig_substitution"
   ```

2. **Implement detection helper:**
   ```python
   def _is_sqrt_difference_of_squares(self, expr, var):
       """Check if expr matches sqrt(a^2 - x^2)."""
       if not expr.has(sp.sqrt):
           return False
       # ... pattern matching logic ...
   ```

3. **Add step generation:**
   ```python
   def integrate(self, expression, variable, ...):
       # ... existing code ...
       
       if technique == "trig_substitution":
           steps.append({
               "rule": "Identify form",
               "explanation": f"Expression matches sqrt(a^2 - x^2) form"
           })
           steps.append({
               "rule": "Choose substitution",
               "explanation": f"Let x = a*sin(θ), dx = a*cos(θ) dθ"
           })
           # ... more steps ...
   ```

4. **Write tests:**
   ```python
   # tests/integration/test_trig_substitution.py
   class TestTrigSubstitution:
       def test_basic_form(self, engine):
           result = engine.integrate("1/sqrt(1 - x**2)", "x")
           assert result["success"]
           assert result["technique"] == "trig_substitution"
   ```

5. **Update benchmark validation:**
   ```python
   # benchmarks/validate_integration.py
   # Add to test cases:
   validator.validate("1/sqrt(1 - x**2)", "x", "Trig Sub Basic", "trig_substitution")
   ```

6. **Document in README:**
   - Add to "Supported Techniques" list
   - Add example to showcase section

### Task 2: Fix a Bug

**Example:** Definite integrals fail with string limits

1. **Reproduce the bug:**
   ```python
   # tests/integration/test_integration_engine.py
   def test_definite_integral_string_limits_bug(self, engine):
       # This currently fails
       result = engine.integrate("x**2", "x", lower_limit="0", upper_limit="1")
       assert result["success"]  # Should pass but doesn't
   ```

2. **Identify root cause:**
   - Check error message: `TypeError: ufunc 'isfinite' not supported for input types`
   - Trace to `np.isfinite(lower_limit)` call
   - Problem: String `"0"` passed instead of numeric `0`

3. **Fix in `integration_engine.py`:**
   ```python
   def integrate(self, expression, variable, lower_limit=None, upper_limit=None, ...):
       # Convert string limits to numeric
       if lower_limit is not None:
           lower_limit = float(lower_limit)
       if upper_limit is not None:
           upper_limit = float(upper_limit)
       
       # ... rest of function ...
   ```

4. **Verify fix:**
   ```bash
   pytest tests/integration/test_integration_engine.py::test_definite_integral_string_limits_bug
   # Should pass now
   ```

5. **Commit:**
   ```bash
   git commit -m "fix(integration): convert string limits to numeric before validation"
   ```

### Task 3: Improve Documentation

**Example:** Add 30-minute architecture overview

1. **Create new section in docs/ARCHITECTURE.md:**
   ```markdown
   ## Quick Start Guide (30-Minute Architecture Overview)
   
   ### 1. Read the Big Picture (5 min)
   [Explain data flow]
   
   ### 2. Understand Key Classes (10 min)
   [IntegrationEngine, StepEngine, StepNode]
   
   ### 3. Trace a Sample Computation (10 min)
   [Walk through ∫x·e^x dx step-by-step]
   
   ### 4. Explore Extension Points (5 min)
   [Where to add new techniques]
   ```

2. **Add diagrams (optional):**
   ```bash
   # Create docs/diagrams/data-flow.png using Mermaid
   # Reference in docs/ARCHITECTURE.md
   ```

3. **Get feedback:**
   - Ask a new contributor to follow the guide
   - Time them (should take ≤30 minutes)
   - Iterate based on confusion points

4. **Commit:**
   ```bash
   git commit -m "docs(architecture): add 30-minute quick start guide"
   ```

---

## How Decisions Are Made

### Architecture Decision Records (ADRs)

**All significant architectural decisions are documented in `docs/ADR/`.**

**Existing ADRs:**
- [ADR-001](docs/ADR/ADR-001-separate-integration-engine.md): Why integration engine is separate from step engine
- [ADR-002](docs/ADR/ADR-002-sympy-as-backend.md): Why we use SymPy instead of custom CAS
- [ADR-003](docs/ADR/ADR-003-dict-return-not-class.md): Why we return dicts instead of result classes

**When to create an ADR:**
- Adding a new module (e.g., `series_engine.py`)
- Choosing a dependency (e.g., switching from FastAPI to Flask)
- Changing public API (e.g., breaking change in return format)
- Establishing a pattern (e.g., error handling strategy)

**How to create an ADR:**
1. Copy template from existing ADRs (use ADR-001 as model)
2. Increment number: Next is ADR-004
3. Fill in:
   - **Context:** What problem are we solving?
   - **Decision:** What did we decide?
   - **Alternatives Considered:** What else did we evaluate? Why rejected?
   - **Consequences:** Positive, negative, neutral impacts
4. Get review from maintainer
5. Merge to `dev`, then `main`
6. Update `docs/ADR/README.md` index

### Decision-Making Process

**For small changes (bug fixes, docs, tests):**
- Make PR → Review → Merge (no ADR needed)

**For medium changes (new feature, refactoring):**
- Open GitHub Issue → Discuss approach → Implement → PR → Review → Merge
- ADR optional (use judgment)

**For large changes (new module, breaking API change):**
- Open GitHub Discussion → Propose ADR → Get consensus → Create ADR → Implement → PR → Review → Merge
- ADR required

**Who decides:** Maintainers have final say, but community input is valued. For v0.2-v0.9, single maintainer approval is sufficient. For v1.0+, require 2+ maintainer approvals for breaking changes.

---

## Getting Help

### Resources

- **Architecture overview:** [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Coding standards:** [CODING_STANDARDS.md](docs/CODING_STANDARDS.md)
- **Versioning policy:** [VERSIONING.md](docs/VERSIONING.md)
- **Roadmap:** [ROADMAP.md](docs/ROADMAP.md)
- **ADRs:** [docs/ADR/](docs/ADR/)

### Communication Channels

- **GitHub Discussions:** For questions, ideas, feedback
- **GitHub Issues:** For bug reports, feature requests (use templates)
- **Pull Requests:** For code contributions (use review checklist)
- **Email:** team@calcora.dev for private matters

### Common Questions

**Q: I found a bug. What do I do?**  
A: Open a GitHub Issue with:
1. Minimal reproduction (e.g., `engine.integrate("x**2", "x")` fails)
2. Expected vs actual behavior
3. Error message / stack trace
4. Environment (Python version, OS)

**Q: I want to add a feature. Where do I start?**  
A: 
1. Check [ROADMAP.md](docs/ROADMAP.md) to see if it's planned
2. Open GitHub Discussion to propose it
3. Get maintainer feedback before implementing
4. Follow "Add New Integration Technique" guide above

**Q: Tests are failing locally but I didn't touch test files. Why?**  
A:
1. Run `git pull origin dev` (ensure you're on latest)
2. Run `pip install -e ".[dev]"` (ensure dependencies updated)
3. Run `pytest --lf` (re-run only last failures for faster iteration)
4. Check CI logs on GitHub for hints

**Q: How do I know if my code is good enough to PR?**  
A:
1. All tests passing: `pytest`
2. Coverage not decreased: `pytest --cov=src/calcora`
3. Linting clean: `ruff check src/`
4. Type hints valid: `mypy src/`
5. Coding standards met: Review [CODING_STANDARDS.md](docs/CODING_STANDARDS.md) checklist

If yes to all 5 → Open PR!

**Q: My PR was rejected. What now?**  
A: Don't worry! Common reasons:
1. **Out of scope:** Feature doesn't align with Calculus I/II focus (see [ROADMAP.md](docs/ROADMAP.md))
2. **Needs tests:** Add tests covering new code paths
3. **Coding standards:** Follow naming conventions, add docstrings
4. **Too large:** Break into smaller PRs (easier to review)

Maintainers will explain why and suggest improvements. Iterate and resubmit!

---

## Philosophy & Values

**Determinism over heuristics**  
- Prefer provably correct algorithms to "usually works" heuristics
- Document edge cases where correctness isn't guaranteed

**Auditability over magic**  
- Every step must explain *why* (not just *what*)
- Avoid "black box" transformations

**Education over speed**  
- Clearer explanations > faster computation
- Target audience: students, not research supercomputers

**Simplicity over features**  
- Master Calculus I/II before expanding to new domains
- "Lock scope, deepen vertically" (see [ROADMAP.md](docs/ROADMAP.md))

**Transparency over promises**  
- Honest about limitations (see README "Current Limitations")
- Conservative roadmap (see [ROADMAP.md](docs/ROADMAP.md))

---

## Thank You!

Contributing to Calcora helps students learn math better. Your work matters.

**Happy coding!** 🎓✨
