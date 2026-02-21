# Coding Standards — Calcora

**Purpose:** Ensure code remains understandable 2 years from now when you've forgotten why you made decisions.

---

## Core Principles

1. **Explicit over clever** — Future maintainers shouldn't need to decrypt your logic
2. **Comments explain WHY, not WHAT** — Code shows what happens, comments explain reasoning
3. **Test edge cases** — The weird inputs are where bugs hide
4. **One file, one responsibility** — If a file does >3 things, split it

---

## Python Style Guide

### File Organization

```python
"""
Module docstring: What does this module do? Why does it exist?

Example:
    Basic usage example here
"""

# Standard library imports
import sys
from typing import Dict, List

# Third-party imports
import sympy as sp
import numpy as np

# Local imports
from calcora.engine.models import StepNode
from calcora.plugins.interfaces import RulePlugin

# Constants at top
DEFAULT_TIMEOUT = 10
MAX_ITERATIONS = 100

# Classes and functions below
class MyClass:
    """Class docstring explaining purpose."""
    pass
```

### Naming Conventions

```python
# Classes: PascalCase
class IntegrationEngine:
    pass

# Functions/methods: snake_case
def integrate_by_parts(u, dv):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_POLYNOMIAL_DEGREE = 50

# Private methods: _leading_underscore
def _internal_helper(self):
    pass

# Boolean variables: is_/has_/can_ prefix
is_polynomial = True
has_trig_functions = False
can_substitute = True
```

### Documentation Standards

#### Module Docstrings (Required)

```python
"""
Integration engine for symbolic calculus.

This module implements 10 core integration techniques following
standard Calculus II curriculum (Stewart Ch. 7-8).

Architecture Decision:
    - Separate from step_engine.py to isolate integration complexity
    - Uses SymPy as symbolic backend (see ADR-002)
    - Returns dict instead of StepGraph for API compatibility

Usage:
    engine = IntegrationEngine()
    result = engine.integrate("x**2", "x", verbosity="detailed")
"""
```

#### Class Docstrings (Required)

```python
class IntegrationEngine:
    """
    Symbolic integration engine using rule-based technique selection.
    
    Attributes:
        timeout (int): Maximum seconds before aborting computation
        
    Methods:
        integrate: Main entry point for integration
        _detect_technique: Determines which technique to apply
    """
```

#### Function Docstrings (Required for Public APIs)

```python
def integrate(self, expression: str, variable: str, verbosity: str = "concise") -> dict:
    """
    Integrate a symbolic expression with step-by-step explanations.
    
    Args:
        expression: Mathematical expression as string (e.g., "x**2 + sin(x)")
        variable: Variable to integrate with respect to (usually "x")
        verbosity: Level of explanation detail ("concise", "detailed", "teacher")
        
    Returns:
        dict: {
            'success': bool,
            'output': str (antiderivative),
            'technique': str (method used),
            'steps': List[dict] (step-by-step explanation),
            'error': str (if success=False)
        }
        
    Raises:
        ValueError: If expression contains unsupported syntax
        TimeoutError: If computation exceeds self.timeout
        
    Example:
        >>> engine = IntegrationEngine()
        >>> result = engine.integrate("x**2", "x")
        >>> result['output']
        'x**3/3'
    """
```

#### Inline Comments (Use Sparingly)

```python
# GOOD: Explains WHY, documents non-obvious reasoning
def _detect_partial_fractions(self, expr):
    # Partial fractions only works for proper rational functions
    # (numerator degree < denominator degree). Check this first
    # to avoid expensive factorization on invalid cases.
    if expr.is_rational_function():
        num_deg = sp.degree(expr.as_numer_denom()[0])
        den_deg = sp.degree(expr.as_numer_denom()[1])
        return num_deg < den_deg
    return False

# BAD: States the obvious
def _detect_partial_fractions(self, expr):
    # Check if expression is rational
    if expr.is_rational_function():
        # Get numerator and denominator degrees
        num_deg = sp.degree(expr.as_numer_denom()[0])
        den_deg = sp.degree(expr.as_numer_denom()[1])
        # Return true if numerator degree less than denominator
        return num_deg < den_deg
    # Return false
    return False
```

### Code Complexity Limits

- **Functions:** Max 50 lines (excluding docstring)
  - If longer, extract helper methods
  - Exception: Large `if-elif` chains for technique detection
  
- **Files:** Max 500 lines
  - If longer, split into submodules
  - Exception: `integration_engine.py` at 700 lines is borderline — consider refactoring
  
- **Nesting depth:** Max 4 levels
  - Deeply nested code is hard to test and understand
  - Extract early returns or helper functions

### Error Handling

```python
# GOOD: Specific exceptions with context
def integrate(self, expression: str, variable: str):
    try:
        expr = sp.sympify(expression)
    except sp.SympifyError as e:
        return {
            'success': False,
            'error': f"Invalid syntax in '{expression}': {str(e)}"
        }
    
    if not expr.free_symbols:
        return {
            'success': False,
            'error': f"Expression '{expression}' has no variables to integrate"
        }

# BAD: Bare except swallows debugging info
def integrate(self, expression: str, variable: str):
    try:
        expr = sp.sympify(expression)
        # ... computation
    except:
        return {'success': False, 'error': 'Something went wrong'}
```

### Type Hints (Required)

```python
from typing import Dict, List, Optional, Tuple, Union

# All public functions must have type hints
def integrate(
    self,
    expression: str,
    variable: str,
    lower_limit: Optional[float] = None,
    upper_limit: Optional[float] = None,
    verbosity: str = "concise"
) -> Dict[str, Union[str, bool, List[dict]]]:
    pass

# Return types for complex structures
def _generate_steps(self, expr) -> List[Dict[str, str]]:
    """Returns list of step dictionaries with 'rule' and 'explanation' keys."""
    pass
```

---

## Testing Standards

### Test Structure

```python
def test_integration_polynomial():
    """Test basic polynomial integration using power rule."""
    engine = IntegrationEngine()
    result = engine.integrate("x**2", "x")
    
    # Assertions should be specific and explain intent
    assert result['success'], f"Integration failed: {result.get('error')}"
    assert 'x**3/3' in str(result['output']) or 'x³/3' in str(result['output']), \
        f"Expected x³/3, got {result['output']}"
    assert result['technique'] == 'Power Rule', \
        f"Expected Power Rule, engine used {result['technique']}"
```

### Coverage Requirements

- **New features:** Minimum 70% line coverage
- **Bug fixes:** Add regression test that would have caught the bug
- **Integration engine:** Target 80% coverage (currently 70%)
- **Critical paths:** 100% coverage (API endpoints, error handling)

### Test Naming

```python
# Pattern: test_<function>_<scenario>_<expected_result>

def test_integrate_polynomial_returns_antiderivative():
    pass

def test_integrate_invalid_syntax_returns_error():
    pass

def test_integrate_with_limits_calculates_area():
    pass
```

---

## Git Commit Standards

### Conventional Commits

```bash
# Format: <type>(<scope>): <description>

# Types:
feat:     New feature
fix:      Bug fix
docs:     Documentation only
style:    Formatting, no code change
refactor: Code restructuring, no behavior change
test:     Adding/updating tests
chore:    Build process, dependencies

# Examples:
feat(integration): add hyperbolic trig support
fix(api): handle empty expression input
docs(architecture): update integration engine design
test(integration): add edge cases for sqrt(x)
refactor(engine): extract _detect_technique to submodule
```

### Commit Size

- **One logical change per commit**
- Max ~300 lines changed (excluding generated files)
- If larger, break into multiple commits

### Commit Messages

```
feat(integration): implement integration by parts

- Adds LIATE priority system for u/dv selection
- Includes fallback for cases where LIATE fails
- Test coverage: 15 new cases including x*sin(x), x*ln(x)

Closes #42
```

---

## Code Review Checklist

Before submitting PR:

- [ ] All tests pass (`pytest tests/`)
- [ ] Coverage ≥70% for new code
- [ ] Docstrings for all public functions
- [ ] Type hints added
- [ ] No commented-out code (delete or explain with FIXME)
- [ ] No `print()` debugging statements (use `logging`)
- [ ] Conventional commit messages
- [ ] CHANGELOG.md updated (for features/breaking changes)

---

## Anti-Patterns to Avoid

### ❌ Magic Numbers

```python
# BAD
if polynomial_degree > 50:
    return fallback()

# GOOD
MAX_POLYNOMIAL_DEGREE = 50  # Beyond this, symbolic computation becomes impractical
if polynomial_degree > MAX_POLYNOMIAL_DEGREE:
    return fallback()
```

### ❌ Deeply Nested Conditions

```python
# BAD
def detect_technique(expr):
    if expr.is_Add:
        if all(term.is_polynomial() for term in expr.args):
            if degree < 10:
                if has_integer_coeffs():
                    return "power_rule"

# GOOD
def detect_technique(expr):
    if not expr.is_Add:
        return None
    if not all(term.is_polynomial() for term in expr.args):
        return None
    if degree >= 10:
        return "numerical_fallback"
    if not has_integer_coeffs():
        return "simplify_first"
    return "power_rule"
```

### ❌ God Classes

```python
# BAD: IntegrationEngine with 2000 lines doing differentiation, matrices, plotting

# GOOD: Separate engines
# - IntegrationEngine (integration only)
# - DifferentiationEngine (differentiation only)  
# - MatrixEngine (linear algebra only)
```

### ❌ Silent Failures

```python
# BAD
try:
    result = integrate(expr)
except:
    pass  # Oops, we just lost the error

# GOOD
try:
    result = integrate(expr)
except IntegrationError as e:
    logger.error(f"Integration failed for {expr}: {e}")
    return {'success': False, 'error': str(e)}
```

---

## When to Refactor

**Refactor immediately if:**
- Function >100 lines
- Cyclomatic complexity >10 (many nested ifs)
- Copy-pasted code appears 3+ times
- You can't explain what it does in one sentence

**Refactor eventually if:**
- Test coverage <70%
- No docstrings
- File >500 lines
- Unclear variable names (`x`, `temp`, `data`)

**Document refactoring decisions in ADRs** (see `docs/ADR/`)

---

## IDE Configuration

### VS Code Settings (`.vscode/settings.json`)

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true
}
```

### Pre-commit Hooks (Recommended)

```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

---

## Questions?

If these standards conflict with external library conventions (SymPy, NumPy), follow the external library's style for code interfacing with it.

For architecture decisions not covered here, create an ADR in `docs/ADR/`.
