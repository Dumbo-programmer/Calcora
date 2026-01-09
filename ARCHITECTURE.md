# Calcora Architecture

This document defines Calcora’s core invariants: the step-by-step reasoning engine, the directed reasoning DAG model, and the plugin boundaries.

## Design principles

- **Determinism**: identical inputs + same plugin set → identical step DAG.
- **Auditability**: each step declares what rule was applied and why.
- **Separation**: the engine owns the step DAG; plugins propose transformations.
- **Safety**: plugins are validated; invalid steps are rejected.

## Step engine: the reasoning DAG

A computation produces a `StepGraph` (DAG) of `StepNode`s.

### StepNode schema

Each `StepNode` records:

- `id`: stable identifier within the graph
- `operation`: e.g. `differentiate`, `integrate`, `solve`
- `rule`: canonical rule name (plugin-provided)
- `input`: input expression (string or structured form)
- `output`: output expression
- `explanation`: human-readable explanation for renderers
- `dependencies`: upstream step ids
- `metadata`: optional structured data (domains, confidence, tags)

### DAG invariants

- `dependencies` must reference earlier nodes.
- Cycles are forbidden.
- Steps must be validated before insertion.

## Verbosity levels

Calcora stores one canonical DAG; renderers control how much explanation is shown:

- **concise**: key transformations only
- **detailed**: rule names + short intuition
- **teacher**: definitions and side notes (where available)

## Plugin boundaries

Calcora supports:

- **Rule plugins**: propose symbolic transformations for a specific operation.
- **Solver plugins**: implement algorithmic solvers (numerical methods, graph algorithms, linear algebra routines).
- **Renderer plugins**: transform a `StepGraph` into text/LaTeX/JSON/HTML.

Plugins must declare supported `domains` and `operations` and are validated at load time.

## Current implementation status (v0.1)

### Completed features

- ✅ Core step engine with deterministic rule selection
- ✅ StepGraph validation (DAG checks, dependency validation)
- ✅ Plugin registry with priority-based rule selection
- ✅ Built-in differentiation rules:
  - Constant, identity, sum, product, power rules
  - Constant multiple factoring
  - Chain rules for: sin, cos, tan, sec, csc, cot, exp, log
  - Inverse trig: asin, acos, atan
  - SymPy fallback for complex expressions
- ✅ Text and JSON renderers with verbosity levels
- ✅ FastAPI HTTP API with local web GUI
- ✅ Typer CLI interface
- ✅ Plugin entry point discovery

### Architecture improvements

**Terminal condition**: The engine halts when an expression is fully differentiated (no more `Derivative` nodes), preventing infinite fallback loops.

**Rule priority system**:
- Priority 100: Terminal rules (constants, identity)
- Priority 95: Constant multiple extraction
- Priority 90: Linearity (sum rule)
- Priority 85: Chain rules and power rule
- Priority 80: Product rule
- Priority -50: SymPy fallback for unevaluated derivatives
- Priority -200: Final simplification

This ordering ensures pedagogically meaningful step sequences.

## Future architecture (v0.2+)

- AST-level expression validation
- Domain-specific rule whitelists
- Solver plugins with step emission
- Enhanced metadata (confidence scores, multiple proof strategies)
- Quotient rule, hyperbolic functions, piecewise/absolute value handling
