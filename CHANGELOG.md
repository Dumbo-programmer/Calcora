# Changelog

All notable changes to Calcora will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-24

### Added (Integration Engine)
- **Complete Integration Engine** with 10 core techniques covering ~80% of Calculus II curriculum
  - Power rule for polynomials (any degree)
  - U-substitution for composite functions
  - Integration by parts (LIATE priority)
  - Partial fractions for rational functions
  - Trigonometric identities and integration
  - Inverse trigonometric patterns
  - Hyperbolic function integration
  - Exponential and logarithmic forms
  - Square root and radical patterns
  - General fallback with numerical approximation
- **Definite Integral Support** with numerical area calculation
- **Interactive Graphing** for all integration results
  - Dual plotting (integrand + antiderivative)
  - Shaded area visualization for definite integrals
  - Vertical bound markers with exact values
  - Color-coded regions for positive/negative areas
- **Intelligent Technique Detection** - automatically selects optimal integration method
- **Three Verbosity Modes**: Concise / Detailed / Teacher Mode
- **Benchmark Validation Suite**: 26 problems verified against SymPy (100% accuracy)

### Added (Security & Robustness)
- **Input Validation Layer** (`input_validator.py`) preventing code execution attacks
  - Safe SymPy parsing with whitelisted functions only
  - Expression blacklist blocking `__import__`, `eval`, `exec`, SQL injection, XSS
  - Character whitelist validation (max 500 chars)
  - Variable name validation (no keywords, double underscore, reserved names)
  - Literal division-by-zero detection
- **Execution Timeout Protection** (`timeout_wrapper.py`) preventing DoS attacks
  - Platform-independent timeout mechanism (signal.alarm on Unix, threading on Windows)
  - Default 3.0s timeout (configurable 0.1s - 30s)
  - Graceful timeout errors with structured error codes
  - Daemon thread cleanup (no resource leakage)
- **Malformed Input Test Suite**: 18 defensive tests for security validation
- **Timeout Test Suite**: 12 tests verifying DoS protection

### Changed (UI/UX)
- **Responsive Layout Improvements**
  - Fixed cramped two-column layout on medium screens (1200-1400px)
  - Added `minmax(400px, 1fr)` grid columns preventing <400px columns
  - 4 breakpoints: 1600px → 1400px → 1100px → 768px → 600px
  - Single column layout on mobile (<1100px)
- **Loading Screen** - Full overlay with API connection status
- **Button Layout Fixes**
  - Consolidated result card header (removed duplicate controls)
  - Copy button auto-expands to show "Copied!" text
  - Format badge inline with title, hides on mobile
- **Overflow Handling** - Long formulas scroll instead of wrap

### Fixed
- **Benchmark Script**: Unicode → ASCII encoding for Windows console
- **Benchmark Comparison**: Strip "+ C" from Calcora output before SymPy comparison
- **Variable Passing**: Changed from Symbol object to string in benchmark validation
- **Test Parameter Names**: `limits` → `lower_limit`/`upper_limit` for consistency

### Testing
- **73 total tests**: 69 passing (94.5% pass rate)
- **Integration Engine Coverage**: 71% (exceeds 65% target)
- **Overall Coverage**: 51% (3.4x improvement from 15%)
- **Input Validator Coverage**: 77%
- **Timeout Wrapper Coverage**: 75%
- **Benchmark Results**: 26/26 passing (100% accuracy), avg 15ms per problem

### Security Impact
- ✅ **Code Execution Blocked**: Arbitrary `__import__`, `eval`, `exec` prevented
- ✅ **DoS Protection**: Single expression cannot freeze server >3s
- ✅ **Classroom-Safe**: Students cannot hang system with malicious/accidental input
- ✅ **Trust Boundary**: All user input passes through validation layer

### Performance
- Average integration time: ~15ms (includes timeout overhead)
- Benchmark suite: all problems complete <200ms
- No false positives on timeout enforcement

### Known Limitations
- Complex number conversion in graph generation (4 edge case test failures)
- Windows threading timeout is approximate (Python limitation - cannot kill threads)
- Trig substitution not implemented (v0.3 planned)
- Advanced reduction formulas not implemented (v0.3 planned)

### Documentation
- Added [benchmarks/results_2026-02-24_post_timeout.txt](benchmarks/results_2026-02-24_post_timeout.txt)
- Updated README with badges: tests, coverage, accuracy, engine coverage, security
- Added STATUS.md documenting release readiness assessment

### For Educators
This release makes Calcora suitable for classroom use:
- **Security**: Input validation prevents code execution exploits
- **Reliability**: Timeout protection ensures system remains responsive
- **Accuracy**: 100% match with SymPy on benchmark suite
- **Coverage**: 71% integration engine code paths tested
- **Transparency**: Honest limitations documented

**Academic Credibility**: Suitable for Calculus I/II coursework and outreach. Not recommended for research computing or peer-reviewed publications.

[0.2.0]: https://github.com/Dumbo-programmer/calcora/releases/tag/v0.2.0

## [0.1.0] - 2026-01-12

### Added
- Core step-by-step reasoning engine with DAG-based computation model
- Differentiation with explicit rule decomposition (chain, product, power, sum rules)
- Support for trigonometric functions (sin, cos, tan, sec, csc, cot)
- Support for exponential and logarithmic functions
- Support for inverse trigonometric functions (asin, acos, atan)
- Linear algebra operations:
  - Matrix multiplication
  - Matrix determinants (2x2, 3x3, general)
  - Matrix inverse
  - Matrix RREF (Row Reduced Echelon Form)
  - Matrix eigenvalues and eigenvectors
  - LU decomposition
- Symbolic matrix support (variables as matrix entries)
- Plugin system with rule, solver, and renderer plugins
- Command-line interface (CLI) with Typer
- FastAPI-based HTTP API
- Static web UI for interactive computation
- Text and JSON renderers with multiple verbosity levels
- PyInstaller-based standalone executables for Windows
- Plugin entry point discovery system
- Comprehensive documentation (Architecture, Roadmap, Contributing, Quick Start)

### Technical Details
- Python 3.11+ support
- SymPy integration for symbolic mathematics
- Pydantic models for type safety and validation
- Step graph validation with DAG integrity checks
- Priority-based rule selection system
- Terminal condition detection to prevent infinite loops

### Distribution
- Standalone Windows executables (CLI and server)
- Distribution package with quick launcher scripts
- No external dependencies required for end users

[0.1.0]: https://github.com/Dumbo-programmer/calcora/releases/tag/v0.1.0
