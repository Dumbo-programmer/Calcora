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
        import re
        
        sp = _try_import_sympy()
        x = sp.Symbol("x")
        
        # Preprocess input: convert ln() to log() for SymPy
        # Also handle log_b(x) notation -> log(x, b)
        # Note: SymPy uses log(x, base) syntax where x is the argument and base is the logarithm base
        # So log(x, 10) = log base 10 of x, and log(10, x) = log base x of 10 (different functions!)
        expression = expression.replace('ln(', 'log(')
        
        # Handle log_3(x) or log_{3}(x) -> log(x, 3)
        expression = re.sub(r'log_\{?(\w+)\}?\(', r'log(\1,', expression)
        
        parsed = sp.sympify(expression)
        # If we're already in an unevaluated derivative form, evaluate it.
        if isinstance(parsed, sp.Derivative):
            out = parsed.doit()
        else:
            out = sp.diff(parsed, x)
        
        # Format output: convert log() to ln() for natural logarithm
        result_str = str(out)
        result_str = self._format_expression(result_str)
        
        return (
            result_str,
            "Differentiate using SymPy as a fallback rule.",
            [],
            {"domain": "calculus", "backend": "sympy"},
        )
    
    def _format_expression(self, expr_str: str) -> str:
        """Format expression to use proper mathematical notation.
        
        SymPy uses log() for natural logarithm, but mathematically:
        - ln(x) = natural logarithm (base e)
        - log(x) = typically log base 10
        - log(x, base) = logarithm with specified base
        
        This function converts:
        - log(x) -> ln(x) (natural log)
        - log(x, 10) -> log(x) (common log)
        - log(x, b) -> log_b(x) (log base b)
        """
        import re
        
        # Pattern to match log(arg, base) - log with explicit base
        base_log_pattern = r'log\(([^,]+),\s*([^)]+)\)'
        
        def replace_base_log(match):
            arg = match.group(1)
            base = match.group(2).strip()
            if base == '10':
                # log base 10 - use standard log notation
                return f'log({arg})'
            elif base == 'E' or base == 'e':
                # Explicit base e - use ln
                return f'ln({arg})'
            else:
                # Other bases - use subscript notation
                return f'log_{{{base}}}({arg})'
        
        # First replace logs with explicit bases
        result = re.sub(base_log_pattern, replace_base_log, expr_str)
        
        # Then replace remaining log() (which are natural logs) with ln()
        result = re.sub(r'(?<!log_)\blog\(', 'ln(', result)
        
        return result
