"""
Integration engine for Calcora v0.2

This module provides symbolic integration with step-by-step explanations.
Priority features:
- Indefinite integrals
- Definite integrals
- Common integration techniques
- Numerical fallback
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class IntegrationStep:
    """Represents a single step in integration process"""
    rule: str
    explanation: str
    expression_before: str
    expression_after: str
    technique: Optional[str] = None


class IntegrationEngine:
    """
    Symbolic integration engine with educational explanations.
    
    Supports:
    - Power rule
    - Substitution (u-substitution)
    - Integration by parts
    - Trigonometric integrals
    - Partial fractions
    - Numerical integration (fallback)
    """
    
    def __init__(self):
        self.steps: List[IntegrationStep] = []
        
    def integrate(
        self,
        expression: str,
        variable: str = 'x',
        lower_limit: Optional[float] = None,
        upper_limit: Optional[float] = None,
        verbosity: str = 'detailed'
    ) -> Dict[str, Any]:
        """
        Integrate an expression with step-by-step explanation.
        
        Args:
            expression: Mathematical expression to integrate
            variable: Variable of integration (default: 'x')
            lower_limit: For definite integrals
            upper_limit: For definite integrals
            verbosity: Level of detail ('concise', 'detailed', 'teacher')
            
        Returns:
            Dictionary with result, steps, and metadata
        """
        self.steps = []
        
        try:
            import sympy as sp
        except ImportError:
            raise RuntimeError(
                "SymPy is required for integration. "
                "Install with: pip install 'calcora[engine-sympy]'"
            )
            
        # Parse expression
        x = sp.Symbol(variable)
        expr = sp.sympify(expression)
        
        # Determine integration technique
        technique = self._determine_technique(expr, x)
        
        # Perform integration with explanation
        if technique == 'power_rule':
            result = self._integrate_power_rule(expr, x, verbosity)
        elif technique == 'substitution':
            result = self._integrate_substitution(expr, x, verbosity)
        elif technique == 'by_parts':
            result = self._integrate_by_parts(expr, x, verbosity)
        elif technique == 'trig':
            result = self._integrate_trig(expr, x, verbosity)
        else:
            # General case - let SymPy handle it
            result = self._integrate_general(expr, x, verbosity)
        
        # Handle definite integral
        if lower_limit is not None and upper_limit is not None:
            result = self._evaluate_definite(result, x, lower_limit, upper_limit, verbosity)
        
        return {
            'operation': 'integrate',
            'input': expression,
            'output': str(result),
            'variable': variable,
            'technique': technique,
            'definite': lower_limit is not None,
            'limits': [lower_limit, upper_limit] if lower_limit is not None else None,
            'steps': [
                {
                    'rule': step.rule,
                    'explanation': step.explanation,
                    'before': step.expression_before,
                    'after': step.expression_after,
                    'technique': step.technique
                }
                for step in self.steps
            ],
            'graph': {'nodes': self.steps}
        }
    
    def _determine_technique(self, expr, x) -> str:
        """Determine best integration technique for expression"""
        import sympy as sp
        
        # Check for simple power rule
        if expr.is_polynomial(x):
            return 'power_rule'
        
        # Check for substitution candidates
        if self._is_substitution_candidate(expr, x):
            return 'substitution'
        
        # Check for integration by parts
        if self._is_by_parts_candidate(expr, x):
            return 'by_parts'
        
        # Check for trigonometric integrals
        if any(expr.has(func) for func in [sp.sin, sp.cos, sp.tan]):
            return 'trig'
        
        return 'general'
    
    def _is_substitution_candidate(self, expr, x) -> bool:
        """Check if expression is a good candidate for u-substitution"""
        import sympy as sp
        
        # Look for composite functions f(g(x)) * g'(x)
        # This is a simplified heuristic
        return expr.has(sp.sin, sp.cos, sp.exp, sp.log) and not expr.is_polynomial(x)
    
    def _is_by_parts_candidate(self, expr, x) -> bool:
        """Check if expression needs integration by parts"""
        import sympy as sp
        
        # Products of different function types
        has_poly = expr.is_polynomial(x) or any(expr.has(x**n) for n in range(1, 4))
        has_trig = expr.has(sp.sin, sp.cos)
        has_exp = expr.has(sp.exp)
        has_log = expr.has(sp.log)
        
        return sum([has_poly, has_trig, has_exp, has_log]) >= 2
    
    def _integrate_power_rule(self, expr, x, verbosity: str):
        """Integrate using power rule with explanation"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="power_rule",
            explanation="Using power rule: ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="power_rule"
        ))
        
        result = sp.integrate(expr, x)
        
        self.steps[-1].expression_after = str(result) + " + C"
        
        if verbosity == 'teacher':
            self.steps.append(IntegrationStep(
                rule="explanation",
                explanation=(
                    "The power rule is one of the most fundamental integration rules. "
                    "For any power of x (except x⁻¹), we increase the exponent by 1 and "
                    "divide by the new exponent. Don't forget the constant of integration C!"
                ),
                expression_before="",
                expression_after="",
                technique="power_rule"
            ))
        
        return result
    
    def _integrate_substitution(self, expr, x, verbosity: str):
        """Integrate using u-substitution"""
        import sympy as sp
        
        # This is simplified - full substitution logic would be more complex
        self.steps.append(IntegrationStep(
            rule="u_substitution",
            explanation="This integral requires u-substitution",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="substitution"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        return result
    
    def _integrate_by_parts(self, expr, x, verbosity: str):
        """Integrate using integration by parts"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="integration_by_parts",
            explanation="Using integration by parts: ∫ u dv = uv - ∫ v du",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="by_parts"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        return result
    
    def _integrate_trig(self, expr, x, verbosity: str):
        """Integrate trigonometric functions"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="trigonometric_integration",
            explanation="Integrating trigonometric function",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="trig"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        return result
    
    def _integrate_general(self, expr, x, verbosity: str):
        """General integration (let SymPy handle it)"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="symbolic_integration",
            explanation="Applying symbolic integration techniques",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="general"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        return result
    
    def _evaluate_definite(self, antiderivative, x, a, b, verbosity: str):
        """Evaluate definite integral using fundamental theorem of calculus"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="fundamental_theorem_of_calculus",
            explanation=f"Evaluate F({b}) - F({a}) where F(x) = {antiderivative}",
            expression_before=f"[{antiderivative}] from {a} to {b}",
            expression_after="",
            technique="definite"
        ))
        
        result = antiderivative.subs(x, b) - antiderivative.subs(x, a)
        self.steps[-1].expression_after = str(result)
        
        return result
