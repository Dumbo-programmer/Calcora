"""LaTeX renderer for mathematical expressions and step-by-step solutions."""

from __future__ import annotations

from dataclasses import dataclass
import sympy as sp

from ..engine.models import EngineResult, StepNode
from ..plugins.interfaces import PluginManifest, RendererCapabilities


@dataclass(frozen=True)
class LatexRenderer:
    """Renders mathematical results as LaTeX markup."""

    manifest: PluginManifest = PluginManifest(
        name="calcora-latex-renderer",
        version="0.3.0",
        description="Renders mathematical expressions in LaTeX format",
    )
    capabilities: RendererCapabilities = RendererCapabilities(
        name="latex", formats=("latex", "tex")
    )

    @property
    def name(self) -> str:
        return self.capabilities.name

    def render(self, *, result: EngineResult, format: str, verbosity: str) -> str:
        """
        Render engine result as LaTeX.

        Args:
            result: Engine computation result
            format: Output format (latex or tex)
            verbosity: Detail level (concise, detailed, teacher)

        Returns:
            LaTeX string with mathematical markup
        """
        lines = []

        # Title based on operation
        operation = result.operation if result.operation else "computation"
        lines.append(f"% Calcora {operation.capitalize()} Result")
        lines.append("")

        # Result section
        if result.output:
            lines.append("\\section*{Result}")
            lines.append(self._expr_to_latex(result.output))
            lines.append("")

        # Step-by-step explanation (if verbosity > concise)
        if verbosity != "concise" and result.graph and result.graph.nodes:
            lines.append("\\section*{Step-by-Step Explanation}")
            for idx, step in enumerate(result.graph.nodes, 1):
                lines.extend(self._render_step(step, idx, verbosity))
            lines.append("")

        # Metadata (if teacher mode)
        if verbosity == "teacher":
            lines.append("\\section*{Metadata}")
            lines.append(f"\\textbf{{Operation:}} {result.operation}")
            if result.input:
                lines.append(f"\\textbf{{Input:}} {self._expr_to_latex(result.input)}")
            lines.append("")

        return "\n".join(lines)

    def _render_step(self, step: StepNode, step_num: int, verbosity: str) -> list[str]:
        """Render a single step as LaTeX."""
        lines = []

        # Step number and rule
        rule_name = step.rule.replace("_", " ").title() if step.rule else "Step"
        lines.append(f"\\subsection*{{Step {step_num}: {rule_name}}}")

        # Input expression
        if step.input:
            lines.append("\\textbf{Input:}")
            lines.append(f"\\[{self._expr_to_latex(step.input)}\\]")

        # Explanation (detailed/teacher mode)
        if verbosity in ("detailed", "teacher") and step.explanation:
            lines.append(f"\\textit{{{step.explanation}}}")
            lines.append("")

        # Output expression
        if step.output:
            lines.append("\\textbf{Output:}")
            lines.append(f"\\[{self._expr_to_latex(step.output)}\\]")

        lines.append("")
        return lines

    def _expr_to_latex(self, expr: str | sp.Expr) -> str:
        """Convert expression to LaTeX format."""
        if isinstance(expr, str):
            # Try to parse as SymPy expression
            try:
                expr_parsed = sp.sympify(expr, evaluate=False)
                return sp.latex(expr_parsed)
            except Exception:
                # If parsing fails, return escaped string
                return expr.replace("_", "\\_").replace("**", "^")

        # Already a SymPy expression
        try:
            return sp.latex(expr)
        except Exception:
            return str(expr).replace("_", "\\_").replace("**", "^")


def create_latex_renderer() -> LatexRenderer:
    """Factory function for creating a LaTeX renderer."""
    return LatexRenderer()
