# Contributing to Calcora

Calcora aims to be research-grade, explainable, and contributor-friendly.

## Development setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[engine-sympy,cli,api,dev]"
pytest
```

## Core contribution rules

- Prefer **determinism** over heuristics.
- Each rule plugin must be **auditable**: name + explanation + declared domains.
- Avoid “magical” simplifications unless they are formally justified.
- Add tests for every new rule/solver.

## Where to add code

- Engine core: `src/calcora/engine/`
- Plugin SDK + registry: `src/calcora/plugins/`
- Built-in renderers: `src/calcora/renderers/`
- API: `src/calcora/api/`
- CLI: `src/calcora/cli/`

## Style

- Run `ruff` and `pytest` before opening PRs.
- Keep changes small and focused.
