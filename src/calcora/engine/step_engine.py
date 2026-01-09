from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import EngineResult, StepGraph, StepNode
from .validation import StepValidationError, validate_step_graph, validate_step_node
from ..plugins.registry import PluginRegistry


@dataclass(frozen=True)
class EngineConfig:
    max_steps: int = 64


class StepEngine:
    """Runs deterministic rule applications to produce a reasoning DAG.

    The engine itself never invents steps. It only:
    - selects among registered rule plugins (by declared operation + priority)
    - applies the chosen rule
    - validates the emitted step
    """

    def __init__(self, registry: PluginRegistry, config: EngineConfig | None = None) -> None:
        self._registry = registry
        self._config = config or EngineConfig()

    @property
    def registry(self) -> PluginRegistry:
        return self._registry

    def run(self, *, operation: str, expression: str, variable: str = "x", order: int = 1, **kwargs) -> EngineResult:
        graph = StepGraph()
        current = expression
        
        # Handle matrix operations specially (they don't use the iterative rule system)
        if operation in ("matrix_multiply", "matrix_determinant", "matrix_inverse", "matrix_rref", "matrix_eigenvalues", "matrix_lu"):
            # Combine expression and matrix_b into single expression format for multiply
            if operation == "matrix_multiply" and "matrix_b" in kwargs:
                current = f"{expression}|||{kwargs['matrix_b']}"
            
            rule = self._registry.select_rule(operation=operation, expression=current)
            if rule is None:
                raise ValueError(f"No rule found for operation '{operation}'")
            
            output, explanation, deps, metadata = rule.apply(expression=current, graph=graph)
            
            # Return result with all accumulated steps from graph
            return EngineResult(
                operation=operation,
                input=expression,
                output=output,
                graph=graph,
            )
        
        if operation == "differentiate":
            try:
                import sympy as sp  # type: ignore
            except Exception as e:  # noqa: BLE001
                raise RuntimeError(
                    "SymPy is required for differentiate. Install with: pip install 'calcora[engine-sympy]'"
                ) from e

            if order < 1:
                raise ValueError(f"Order must be at least 1, got {order}")
            if order > 10:
                raise ValueError(f"Order must be at most 10, got {order}")

            var = sp.Symbol(variable)
            try:
                parsed = sp.sympify(expression)
            except (sp.SympifyError, SyntaxError) as e:
                raise ValueError(
                    f"Invalid mathematical expression '{expression}'. "
                    f"Please check syntax (parentheses, operators, function names). "
                    f"Error: {str(e).split(':', 1)[-1].strip()}"
                ) from e
            
            # Warn about expressions that don't contain the variable
            if not parsed.free_symbols or var not in parsed.free_symbols:
                import warnings
                warnings.warn(
                    f"Expression '{expression}' does not contain variable '{variable}'. "
                    "The derivative will be 0 or a constant.",
                    UserWarning,
                    stacklevel=2
                )
            
            # Create derivative with specified order
            current = str(sp.Derivative(parsed, (var, order), evaluate=False))

        prev_step_id: str | None = None

        for idx in range(self._config.max_steps):
            step_id = f"step_{idx + 1:03d}"
            rule = self._registry.select_rule(operation=operation, expression=current)
            if rule is None:
                break

            output, explanation, deps, metadata = rule.apply(expression=current, graph=graph)

            # Avoid recording no-op steps; treat them as terminal.
            if output == current or (isinstance(metadata, dict) and metadata.get("noop") is True):
                break

            # Halt if the output is fully resolved (no more Derivative nodes)
            try:
                import sympy as sp
                parsed_out = sp.sympify(output)
                if not parsed_out.has(sp.Derivative):
                    # Record the final step, then halt
                    node = StepNode(
                        id=step_id,
                        operation=operation,
                        rule=rule.name,
                        input=current,
                        output=output,
                        explanation=explanation,
                        dependencies=list(deps) if deps else ([prev_step_id] if prev_step_id else []),
                        metadata=dict(metadata),
                    )
                    validate_step_node(node)
                    graph.nodes.append(node)
                    try:
                        validate_step_graph(graph)
                    except StepValidationError as e:
                        raise StepValidationError(f"Invalid step emitted by rule {rule.name}: {e}") from e
                    current = output
                    prev_step_id = step_id
                    break
            except Exception:
                pass

            node = StepNode(
                id=step_id,
                operation=operation,
                rule=rule.name,
                input=current,
                output=output,
                explanation=explanation,
                dependencies=list(deps) if deps else ([prev_step_id] if prev_step_id else []),
                metadata=dict(metadata),
            )

            validate_step_node(node)
            graph.nodes.append(node)

            # Ensure the DAG remains valid after each insertion.
            try:
                validate_step_graph(graph)
            except StepValidationError as e:
                raise StepValidationError(f"Invalid step emitted by rule {rule.name}: {e}") from e

            current = output
            prev_step_id = step_id

        # Apply simplification to final result if differentiating
        if operation == "differentiate":
            try:
                import sympy as sp
                current_expr = sp.sympify(current)
                # Only simplify if there are no remaining unevaluated derivatives
                if not current_expr.has(sp.Derivative):
                    simplified = sp.simplify(current_expr)
                    simplified_str = str(simplified)
                    if simplified_str != current:
                        # Add simplification step
                        step_id = f"step_{len(graph.nodes) + 1:03d}"
                        node = StepNode(
                            id=step_id,
                            operation=operation,
                            rule="simplify_result",
                            input=current,
                            output=simplified_str,
                            explanation="Simplify the final result using algebraic and trigonometric identities",
                            dependencies=[prev_step_id] if prev_step_id else [],
                            metadata={"explanations": {
                                "detailed": "Apply algebraic simplification, combine like terms, and use trigonometric identities to present the result in its simplest form.",
                                "teacher": "After completing all differentiation steps, we simplify the result. This involves combining like terms, reducing fractions, and applying algebraic and trigonometric identities to express the derivative in its most compact and elegant form."
                            }},
                        )
                        validate_step_node(node)
                        graph.nodes.append(node)
                        current = simplified_str
            except Exception:
                pass  # If simplification fails, use unsimplified result

        result = EngineResult(operation=operation, input=expression, output=current, graph=graph)
        return result

    def available_rules(self, operation: str) -> Iterable[str]:
        return [r.name for r in self._registry.list_rules(operation=operation)]
