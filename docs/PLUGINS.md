# Calcora Plugins

Calcora is a platform. The core engine owns:

- the **StepGraph** (reasoning DAG)
- deterministic **rule selection**
- validation and safety checks

Plugins extend Calcora without modifying the core.

## Plugin types

### 1) Rule plugins

Rule plugins propose symbolic transformations for a specific operation (e.g. `differentiate`).

**Required metadata**
- `name`
- `operation`
- `priority` (higher wins)
- supported `domains`

**Required behavior**
- deterministic
- returns `(output_expr, explanation, dependencies, metadata)`

### 2) Solver plugins

Solver plugins implement algorithmic solvers (numerical methods, graph algorithms, linear algebra routines). They can emit a result plus metadata; in later versions they may also emit steps.

### 3) Renderer plugins

Renderer plugins convert an `EngineResult` (including its `StepGraph`) into a presentation format: text, LaTeX, JSON, HTML, or future visualizations.

## Writing a rule plugin (SDK)

Calcora includes a small decorator for rule plugins:

```python
from calcora.plugins.decorators import rule

@rule(
    name="my_rule",
    operation="differentiate",
    priority=10,
    domains=("calculus",),
    plugin_name="calcora-my-plugin",
    plugin_version="0.1.0",
)
def my_rule(expr: str, graph):
    # Return: output, explanation, dependencies, metadata
    return "2*x", "Differentiate x^2", [], {"tags": ["power_rule"]}
```

## Registering plugins (entry points)

Calcora discovers third-party plugins via Python entry points.

In your plugin’s `pyproject.toml`:

```toml
[project.entry-points."calcora.rule_plugins"]
my_rule = "my_package.my_module:my_rule"
```

Similarly:

- `calcora.solver_plugins`
- `calcora.renderer_plugins`

## Safety model

The engine validates:

- step ids are unique
- dependencies reference existing nodes
- the graph remains acyclic

In v0.2+, Calcora will also validate expression structure more deeply (AST-level constraints) and support domain-specific rule whitelists.
