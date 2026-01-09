from __future__ import annotations

from dataclasses import dataclass

from .models import Domain, StepGraph
from ..plugins.interfaces import PluginManifest, RuleCapabilities


def _try_import_sympy():
    try:
        import sympy as sp  # type: ignore

        return sp
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            "SymPy is not installed. Install with: pip install 'calcora[engine-sympy]'"
        ) from e


@dataclass(frozen=True)
class SympyDifferentiateRule:
    """Fallback differentiator rule.

    This is intentionally a *single* rule that delegates to SymPy. In v0.2+,
    Calcora should expand to multiple auditable rules (product/chain/etc.).
    """

    manifest: PluginManifest = PluginManifest(
        name="calcora-engine-sympy",
        version="0.1.0",
        description="SymPy-backed symbolic rules",
    )
    capabilities: RuleCapabilities = RuleCapabilities(
        name="sympy_diff",
        operation="differentiate",
        priority=-100,
        domains=("calculus",),
    )

    @property
    def name(self) -> str:
        return self.capabilities.name

    def matches(self, *, expression: str) -> bool:
        # As a fallback rule, it matches everything.
        return True

    def apply(self, *, expression: str, graph: StepGraph):
        sp = _try_import_sympy()
        x = sp.Symbol("x")
        parsed = sp.sympify(expression)
        # If we're already in an unevaluated derivative form, evaluate it.
        if isinstance(parsed, sp.Derivative):
            out = parsed.doit()
        else:
            out = sp.diff(parsed, x)
        return (
            str(out),
            "Differentiate using SymPy as a fallback rule.",
            [],
            {"domain": "calculus", "backend": "sympy"},
        )
