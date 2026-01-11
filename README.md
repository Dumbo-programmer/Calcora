# Calcora

Calcora is an open-source, self-hosted computational mathematics engine designed to provide symbolic and numerical solutions with transparent, step-by-step reasoning. Unlike cloud-based tools, Calcora runs entirely on your own machine, making it ideal for classrooms, low-connectivity environments, and privacy-conscious users.

**Status**: v0.1 is an architecture-first alpha. The public API is intentionally small while the explainability engine stabilizes.

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

### Python package (dev)

```bash
python -m pip install -e ".[engine-sympy,cli,api,dev]"
```

### Run the CLI

```bash
python -m calcora --help
```

On Windows, you can also call the venv script directly:

```bash
.venv\Scripts\calcora.exe --help
```

### Run the API (optional)

```bash
uvicorn calcora.api.main:app --reload
```

Then open the local GUI at `http://127.0.0.1:8000/`.

## Architecture (short)

Calcora represents computation as a directed acyclic graph (DAG) of **StepNodes**. Each step records:

- operation name
- applied rule
- input expression
- output expression
- human-readable explanation
- dependencies on prior steps

See [ARCHITECTURE.md](ARCHITECTURE.md) for the formal model.

### Supported differentiation rules (v0.1)

**Basic rules**:
- Constants and identity: d/dx(c) = 0, d/dx(x) = 1
- Sum rule: d/dx(f+g) = f' + g'
- Constant multiple: d/dx(c·f) = c·f'
- Product rule: d/dx(f·g) = f·g' + g·f'
- Power rule: d/dx(x^n) = n·x^(n-1) (with chain rule)

**Trigonometric functions**:
- sin, cos, tan, sec, csc, cot (with chain rule)

**Exponential and logarithmic**:
- exp(u), log(u) (natural log, with chain rule)

**Inverse trigonometric**:
- asin(u), acos(u), atan(u) (with chain rule)

**Fallback**: SymPy integration for any unsupported expressions

All rules include step-by-step explanations with multiple verbosity levels.

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
