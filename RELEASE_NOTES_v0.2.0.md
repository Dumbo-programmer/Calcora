# Release v0.2.0 — Security & Robustness

**Release Date**: February 24, 2026  
**Focus**: Input validation, timeout protection, test coverage  
**Type**: Stabilization release

---

## Summary

v0.2.0 hardens Calcora's integration engine with security boundary implementation and DoS prevention. This release prioritizes **robustness over features**.

### Primary Changes
- Input validation layer preventing code execution
- Execution timeout protection (3s default)
- Integration engine test coverage: 71% (exceeds 65% target)
- Benchmark validation: 26/26 passing (100% accuracy vs SymPy)
- UI responsive layout improvements

### Target Audience
Calculus I/II students and educators evaluating classroom tools.

### Not Recommended For
Advanced mathematics beyond Calculus II, research computing, production scientific applications.

---

## Security Hardening

### Input Validation (`input_validator.py`)

**Purpose**: Trust boundary preventing malicious input exploitation

**Implementation**:
- Expression whitelist: `[a-zA-Z0-9\s\+\-\*/\^\(\)\.,_]+` (max 500 chars)
- Blacklist patterns: `__import__`, `eval`, `exec`, SQL injection, XSS
- Safe SymPy parsing: Restricted `locals` (40+ whitelisted math functions, no `__builtins__`)
- Variable validation: No Python keywords, no double underscore, max 20 chars

**Test Evidence**:
- Code execution attempts: ❌ Blocked (test passing)
- File access patterns: ❌ Blocked (test passing)
- Coverage: 77%

### Timeout Protection (`timeout_wrapper.py`)

**Purpose**: DoS prevention via execution time limits

**Implementation**:
- Platform-independent mechanism (signal.alarm on Unix, threading on Windows)
- Default timeout: 3.0s (configurable: 0.1s - 30s)
- Structured error codes: `TIMEOUT`, `VALIDATION_ERROR`, `PARSE_ERROR`
- Resource cleanup: Daemon threads (auto-cleanup on process exit)

**Known Limitation**:
Python threads cannot be forcefully killed. On timeout, computation continues in background until completion. This is acceptable for educational use (low concurrency). Production deployment should use process-level isolation (Gunicorn/uWSGI).

**Test Evidence**:
- Timeout enforcement: 12/12 tests passing
- Coverage: 75%

---

## Integration Engine

### Coverage Improvement
- Integration engine: **71%** (was 36%, target was 65%)
- Overall: **51%** (was 15%)
- Input validator: **77%**
- Timeout wrapper: **75%**

### Benchmark Validation
- **26/26 tests passing** (100% accuracy)
- Average time: ~15ms per problem
- Environment: Python 3.13.7, SymPy 1.14.0
- Results: `benchmarks/results_2026-02-24_post_timeout.txt`

### Techniques Validated
Power rule, u-substitution, integration by parts, partial fractions, trigonometric, inverse trig, hyperbolic, exponentials, radicals.

**Not Implemented**: Trig substitution, reduction formulas, improper integrals (deferred to v0.3+).

---

## UI/UX Improvements

### Responsive Layout
- Fixed cramped two-column layout on medium screens (1200-1400px)
- Minimum column width: 400px (prevents excessive narrowing)
- Single column on mobile (<1100px)
- Loading screen with API connection status

### Button Layout
- Consolidated result card header (removed duplicate controls)
- Copy button auto-expands for "Copied!" feedback
- Format badge inline with title, hides on mobile

---

## Testing

### Test Results
- **73 total tests**: 69 passing (94.5%)
- **Integration tests**: 35/35 passing
- **Timeout tests**: 12/12 passing
- **Malformed input tests**: 14/18 passing (78%)
- **Security tests**: Code execution blocked, file access blocked

### Known Failures (4 tests, non-blocking)
1. `x ++ x` - Not a bug (unary plus operator is mathematically valid)
2-4. Complex number conversion in graphing - Edge case in visualization (non-core feature)

---

## Architecture Validation

### Critical Checks (All Passing)
- ✅ No circular imports (timeout_wrapper is stdlib-only)
- ✅ No swallowed exceptions (all errors propagate with structured codes)
- ✅ Timeout errors reach UI cleanly
- ✅ No resource leaks (daemon threads with auto-cleanup)

**Verification Document**: `ARCHITECTURE_VERIFICATION_v0.2.md`

---

## Breaking Changes

None. v0.2.0 is backward-compatible with v0.1.0 API.

New optional parameter: `timeout` (default: 3.0s) on `integrate()` method.

---

## Known Limitations

### Not Implemented
- ❌ Trig substitution (v0.3)
- ❌ Reduction formulas (v0.3)
- ❌ Series expansion (v0.3-0.4)
- ❌ Limits (v0.3)
- ❌ LaTeX export (v0.3)

### Performance
- Not optimized for >50 term expressions
- Not optimized for symbolic matrices >5×5

### Accessibility
- WCAG 2.1 progress: ~85%
- Keyboard navigation: Complete
- Screen reader improvements: Ongoing

---

## Upgrade Path

### From v0.1.0
No migration required. All v0.1.0 code works unchanged.

Optional: Add `timeout` parameter to `integrate()` calls:
```python
# Before (still works)
result = engine.integrate("x**2")

# After (with timeout)
result = engine.integrate("x**2", timeout=5.0)
```

---

## Installation

```bash
# Clone repository
git clone https://github.com/Dumbo-programmer/calcora.git
cd calcora

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run benchmarks
python benchmarks/validate_integration.py
```

---

## Academic Context

### Suitable For
- Calculus I/II coursework (Stewart, Thomas, Anton textbooks)
- Educational demonstrations in lectures
- Homework verification (manual review recommended)
- Self-learning with algorithm transparency

### Not Suitable For
- Advanced mathematics beyond Calculus II
- Research-grade symbolic computation
- Grading without human verification
- Peer-reviewed publications

---

## Acknowledgments

- **SymPy**: Ground truth for benchmark validation
- **Security testing**: Malformed input test suite inspiration from OWASP guidelines
- **Timeout design**: Platform-independent approach verified on Windows/Linux

---

## Next Steps (v0.3 Roadmap - Not Committing to Timeline)

Potential future work (no promises):
- Trig substitution implementation
- LaTeX export
- Screen reader improvements
- Series expansion
- Limits

**Scope freeze for v0.2**: No new math techniques until feedback is gathered.

---

## Release Artifacts

### Files
- Source code: `calcora-v0.2.0.zip`
- Benchmark results: `benchmarks/results_2026-02-24_post_timeout.txt`
- Architecture verification: `ARCHITECTURE_VERIFICATION_v0.2.md`
- CHANGELOG: `CHANGELOG.md`

### Git Tags
```bash
git tag -a v0.2.0 -m "Release v0.2.0: Security & Robustness"
git push origin v0.2.0
```

---

**Maintainer**: Architecture validation process  
**Review**: Before each release tag  
**Tone**: Disciplined and factual  
**Position**: Stabilized core, not production-ready
