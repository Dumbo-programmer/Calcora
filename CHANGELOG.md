# Changelog

All notable changes to Calcora will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
