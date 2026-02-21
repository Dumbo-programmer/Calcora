# Semantic Versioning — Calcora

**Current Version:** v0.2.0-alpha  
**Versioning Scheme:** [SemVer 2.0.0](https://semver.org/)

---

## Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE]

Example: 1.2.3-beta.1
```

### MAJOR (Breaking Changes)

Increment when making **incompatible API changes**:

- Removing public functions/classes
- Changing function signatures (parameters, return types)
- Changing output format (e.g., JSON structure)
- Removing supported Python versions

**Example:** `0.2.0` → `1.0.0`

```python
# v0.2.0
result = engine.integrate(expression, variable)  # Returns dict

# v1.0.0 (BREAKING)
result = engine.integrate(expression, variable)  # Now returns IntegrationResult object
```

### MINOR (New Features)

Increment when adding **backward-compatible functionality**:

- New integration techniques
- New API endpoints
- New optional parameters (with defaults)
- Performance improvements
- New verbosity modes

**Example:** `0.2.0` → `0.3.0`

```python
# v0.2.0
engine.integrate(expr, var, verbosity="detailed")

# v0.3.0 (NEW FEATURE)
engine.integrate(expr, var, verbosity="detailed", timeout=10)  # New optional param
```

### PATCH (Bug Fixes)

Increment for **backward-compatible bug fixes**:

- Fixing incorrect integration results
- Fixing rendering bugs
- Fixing error messages
- Documentation corrections

**Example:** `0.2.0` → `0.2.1`

```python
# v0.2.0 (BUG: cos²(x) integrated incorrectly)
result = engine.integrate("cos(x)**2", "x")  # Returns wrong answer

# v0.2.1 (FIX)
result = engine.integrate("cos(x)**2", "x")  # Now correct
```

### Pre-release Labels

Used during development (unstable API):

- `-alpha`: Early testing, features incomplete
- `-beta`: Feature-complete, stabilizing API
- `-rc.N`: Release candidate (frozen features, bug fixes only)

**Example:** `0.3.0-alpha.1` → `0.3.0-beta.1` → `0.3.0-rc.1` → `0.3.0`

---

## Version Lifecycle

### Phase 1: Alpha (Current: v0.2.0-alpha)

**Characteristics:**
- API can change without notice
- Features incomplete or experimental
- Suitable for early adopters only
- No backward compatibility guarantees

**When to release:**
- Core feature implemented but not battle-tested
- Seeking feedback from friendly users

### Phase 2: Beta (Future: v0.3.0-beta)

**Characteristics:**
- API mostly stable (changes require strong justification)
- All planned features implemented
- Test coverage ≥70%
- Ready for pilot deployments

**When to release:**
- After collecting alpha feedback
- All Phase 1 tests passing
- Documentation complete

### Phase 3: Stable (Future: v1.0.0)

**Characteristics:**
- API frozen (breaking changes only in MAJOR version)
- Production-ready
- SemVer guarantees enforced strictly
- Long-term support (LTS) commitments

**When to release:**
- ✅ 6+ months of beta stability
- ✅ Used by 10+ real classrooms
- ✅ Test coverage ≥80%
- ✅ Performance benchmarked
- ✅ Security audit complete

---

## API Stability Guarantees

### Public API (Stable)

Functions/classes documented in README or API docs:

```python
# PUBLIC (stability guaranteed)
from calcora.integration_engine import IntegrationEngine

engine = IntegrationEngine()
result = engine.integrate(expr, var, verbosity="detailed")
```

### Internal API (Unstable)

Functions/classes prefixed with `_` or undocumented:

```python
# INTERNAL (can change without notice)
from calcora.integration_engine import IntegrationEngine

engine = IntegrationEngine()
result = engine._detect_technique(expr)  # UNSTABLE, may break
```

---

## Deprecation Policy

**Before removing a feature:**

1. **MINOR release:** Mark as deprecated with warning
   ```python
   import warnings
   
   def old_function():
       warnings.warn(
           "old_function() is deprecated, use new_function() instead. "
           "Will be removed in v2.0.0",
           DeprecationWarning,
           stacklevel=2
       )
   ```

2. **Wait 2 MINOR releases** (e.g., deprecated in v0.3.0, removed in v0.5.0 or v1.0.0)

3. **MAJOR release:** Remove the feature
   ```python
   # v1.0.0: old_function() deleted
   ```

---

## Version Decision Matrix

| Change Type | MAJOR | MINOR | PATCH |
|-------------|-------|-------|-------|
| **New integration technique** | | ✅ | |
| **Fix wrong result** | | | ✅ |
| **New verbosity mode** | | ✅ | |
| **Change return type** | ✅ | | |
| **Add optional parameter** | | ✅ | |
| **Remove parameter** | ✅ | | |
| **Performance improvement** | | ✅ | |
| **Documentation fix** | | | ✅ |
| **Dependency update (major)** | ✅ | | |
| **Dependency update (minor)** | | | ✅ |
| **Drop Python 3.9 support** | ✅ | | |
| **Add Python 3.13 support** | | ✅ | |

---

## Release Checklist

### Before Tagging

- [ ] All tests pass (`pytest tests/`)
- [ ] Coverage ≥70% (check `htmlcov/index.html`)
- [ ] CHANGELOG.md updated with user-facing changes
- [ ] Version bumped in:
  - [ ] `src/calcora/version.py`
  - [ ] `pyproject.toml`
  - [ ] README.md (status badge)
- [ ] Breaking changes documented in migration guide
- [ ] Benchmark validation passing (if integration changes)

### Tagging Release

```bash
# Format: vMAJOR.MINOR.PATCH[-PRERELEASE]
git tag -a v0.3.0-beta.1 -m "Beta release: LaTeX export + performance improvements"
git push origin v0.3.0-beta.1
```

### Post-Release

- [ ] GitHub Release created with changelog
- [ ] PyPI package published (if public)
- [ ] Documentation site updated
- [ ] Announce in discussions/Discord

---

## Backward Compatibility

### What We Guarantee (v1.0+)

✅ **Guaranteed stable:**
- Function signatures (parameters, return types)
- JSON output format
- CLI command syntax
- API endpoint paths

✅ **Allowed to change (with deprecation):**
- Internal implementation details
- Performance characteristics
- Error message wording
- Default parameter values (with notice)

❌ **Not guaranteed:**
- Exact step-by-step explanation wording
- Graph rendering aesthetics
- Verbosity level detail (can improve)
- Computation time (can optimize)

### Alpha/Beta Exceptions

During alpha/beta (v0.x.x), **breaking changes allowed** but must be:
1. Documented in CHANGELOG
2. Announced in release notes
3. Justified with reasoning (ADR if major)

---

## Version Branching Strategy

### Development Flow

```
main          [v0.2.0-alpha] ──→ [v0.3.0-beta] ──→ [v1.0.0]
                ↓                     ↓                ↓
dev            (unstable)         (feature freeze)  (hotfix only)
                ↓                     ↓
feature/*     (merge to dev)     (merge to dev)
hotfix/*                                            (merge to main + dev)
```

### Branch Naming

```bash
feature/add-hyperbolic-integration    # New features → MINOR bump
bugfix/fix-trig-substitution          # Bug fixes → PATCH bump
breaking/change-api-return-type       # Breaking → MAJOR bump
hotfix/v0.2.1-critical-security-fix   # Emergency patches
```

---

## Examples

### Scenario 1: Adding LaTeX Export

**Change:** New feature, backward-compatible

```python
# v0.2.0
engine.integrate(expr, var)  # Returns dict with 'output', 'steps'

# v0.3.0
engine.integrate(expr, var, output_format="latex")  # New optional param
```

**Version:** `0.2.0` → `0.3.0` (MINOR bump)

---

### Scenario 2: Fixing Integration Bug

**Change:** Bug fix, no API impact

```python
# v0.2.0 (BUG)
engine.integrate("1/x", "x")  # Returns wrong result

# v0.2.1 (FIX)
engine.integrate("1/x", "x")  # Now returns correct ln(x)
```

**Version:** `0.2.0` → `0.2.1` (PATCH bump)

---

### Scenario 3: Changing Return Type

**Change:** Breaking API modification

```python
# v0.9.5 (OLD)
result = engine.integrate(expr, var)  # Returns dict
print(result['output'])

# v1.0.0 (NEW)
result = engine.integrate(expr, var)  # Returns IntegrationResult object
print(result.antiderivative)  # Different access pattern
```

**Version:** `0.9.5` → `1.0.0` (MAJOR bump)

**Migration Guide Required:**
```markdown
## Migrating from v0.x to v1.0

**Breaking Change:** `integrate()` now returns `IntegrationResult` object

Before (v0.9.x):
```python
result = engine.integrate(expr, var)
print(result['output'])
```

After (v1.0.0):
```python
result = engine.integrate(expr, var)
print(result.antiderivative)  # or str(result)
```

For backward compatibility:
```python
result = engine.integrate(expr, var)
legacy_dict = result.to_dict()  # Get old format
```

---

## Current Roadmap Versions

| Version | Status | Scope | ETA |
|---------|--------|-------|-----|
| v0.2.0-alpha | ✅ Released | Integration engine (10 techniques) | Feb 2026 |
| v0.3.0-beta | 🔄 Planning | LaTeX export, performance, stability | Apr 2026 |
| v0.4.0-beta | 📋 Planned | Series expansion, limits (Calc I focus) | Jul 2026 |
| v1.0.0 | 🎯 Goal | Production-ready Calculus I/II engine | Dec 2026 |

**Note:** Dates are estimates, not promises. Quality over deadlines.

---

## Questions?

If unsure whether a change is MAJOR/MINOR/PATCH:

1. Ask: "Could this break existing code?"
   - Yes → MAJOR
   - No → Continue

2. Ask: "Does this add new functionality?"
   - Yes → MINOR
   - No → PATCH

3. Still unsure? Create discussion in GitHub Issues.
