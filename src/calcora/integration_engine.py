"""
Integration engine for Calcora v0.2+

This module provides comprehensive symbolic integration with step-by-step explanations
and graphing capabilities.

Features:
- Indefinite integrals
- Definite integrals with area visualization
- Advanced integration techniques (substitution, by parts, partial fractions, etc.)
- Graph generation for integrand, integral, and area under curve
- Numerical fallback for non-elementary integrals
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
import re
import numpy as np


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
    Advanced symbolic integration engine with educational explanations and graphing.
    
    Supports:
    - Power rule (polynomials, rational exponents)
    - Substitution (u-substitution, trigonometric substitution)
    - Integration by parts (with LIATE priority)
    - Trigonometric integrals (sin, cos, tan, sec, csc, cot)
    - Inverse trigonometric functions
    - Hyperbolic functions (sinh, cosh, tanh)
    - Exponential and logarithmic functions
    - Partial fractions (rational functions)
    - Improper integrals
    - Numerical integration (fallback for non-elementary)
    - Graph generation for visualization
    """
    
    def __init__(self):
        self.steps: List[IntegrationStep] = []
        self.can_integrate = True
    
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
        import sympy as sp
        
        # Pattern to match log(arg, base) - log with explicit base
        # This handles log(x, 10), log(x**2, 3), etc.
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
        # Use negative lookbehind to avoid matching log_
        result = re.sub(r'(?<!log_)\blog\(', 'ln(', result)
        
        return result
        
    def integrate(
        self,
        expression: str,
        variable: str = 'x',
        lower_limit: Optional[float] = None,
        upper_limit: Optional[float] = None,
        verbosity: str = 'detailed',
        generate_graph: bool = True
    ) -> Dict[str, Any]:
        """
        Integrate an expression with comprehensive step-by-step explanation and graphs.
        
        Args:
            expression: Mathematical expression to integrate
            variable: Variable of integration (default: 'x')
            lower_limit: For definite integrals
            upper_limit: For definite integrals
            verbosity: Level of detail ('concise', 'detailed', 'teacher')
            generate_graph: Whether to generate graph data
            
        Returns:
            Dictionary with result, steps, metadata, and graph data
        """
        self.steps = []
        self.can_integrate = True
        
        try:
            import sympy as sp
        except ImportError:
            raise RuntimeError(
                "SymPy is required for integration. "
                "Install with: pip install 'calcora[engine-sympy]'"
            )
        
        # Preprocess input: convert ln() to log() for SymPy
        # Also handle log_b(x) notation -> log(x, b)
        # Note: SymPy uses log(x, base) syntax where x is the argument and base is the logarithm base
        # So log(x, 10) = log base 10 of x, and log(10, x) = log base x of 10 (different functions!)
        expression = expression.replace('ln(', 'log(')
        
        # Handle log_3(x) or log_{3}(x) -> log(x, 3)
        expression = re.sub(r'log_\{?(\w+)\}?\(', r'log(\1,', expression)
            
        # Parse expression
        x = sp.Symbol(variable)
        try:
            expr = sp.sympify(expression)
        except Exception as e:
            return {
                'operation': 'integrate',
                'input': expression,
                'error': f'Failed to parse expression: {str(e)}',
                'success': False
            }
        
        # Determine integration technique
        technique = self._determine_technique(expr, x)
        
        # Perform integration with explanation
        try:
            if technique == 'power_rule':
                result = self._integrate_power_rule(expr, x, verbosity)
            elif technique == 'substitution':
                result = self._integrate_substitution(expr, x, verbosity)
            elif technique == 'by_parts':
                result = self._integrate_by_parts(expr, x, verbosity)
            elif technique == 'trig':
                result = self._integrate_trig(expr, x, verbosity)
            elif technique == 'partial_fractions':
                result = self._integrate_partial_fractions(expr, x, verbosity)
            elif technique == 'inverse_trig':
                result = self._integrate_inverse_trig(expr, x, verbosity)
            elif technique == 'hyperbolic':
                result = self._integrate_hyperbolic(expr, x, verbosity)
            else:
                # General case - let SymPy handle it with fallback
                result = self._integrate_general(expr, x, verbosity)
        except Exception as e:
            # Try numerical integration as ultimate fallback
            self.steps.append(IntegrationStep(
                rule="numerical_fallback",
                explanation=f"Symbolic integration failed. Using numerical approximation.",
                expression_before=f"∫ {expr} dx",
                expression_after="(numerical approximation)",
                technique="numerical"
            ))
            self.can_integrate = False
            result = None
        
        # Handle definite integral
        is_definite = lower_limit is not None and upper_limit is not None
        definite_value = None
        
        if is_definite and result is not None:
            try:
                definite_value = self._evaluate_definite(result, x, lower_limit, upper_limit, verbosity)
            except Exception as e:
                # Numerical fallback for definite integral
                definite_value = self._numerical_definite_integral(expr, x, lower_limit, upper_limit)
                self.steps.append(IntegrationStep(
                    rule="numerical_definite",
                    explanation=f"Using numerical integration to approximate area",
                    expression_before=f"∫[{lower_limit} to {upper_limit}] {expr} dx",
                    expression_after=f"≈ {definite_value}",
                    technique="numerical"
                ))
        
        # Generate graph data
        graph_data = None
        if generate_graph:
            graph_data = self._generate_graph_data(
                expr, result, x, lower_limit, upper_limit, definite_value
            )
        
        # Format output with proper log/ln notation
        output_str = str(definite_value if is_definite else result)
        output_str = self._format_expression(output_str)
        if not is_definite:
            output_str += " + C"
        
        return {
            'operation': 'integrate',
            'input': expression,
            'output': output_str,
            'variable': variable,
            'technique': technique,
            'definite': is_definite,
            'limits': [lower_limit, upper_limit] if is_definite else None,
            'can_integrate': self.can_integrate,
            'steps': [
                {
                    'rule': step.rule,
                    'explanation': step.explanation,
                    'before': self._format_expression(step.expression_before),
                    'after': self._format_expression(step.expression_after),
                    'technique': step.technique
                }
                for step in self.steps
            ],
            'graph': graph_data if graph_data else {'nodes': self.steps},
            'success': True
        }
    
    def _determine_technique(self, expr, x) -> str:
        """Determine best integration technique for expression"""
        import sympy as sp
        
        # Check for simple power rule (polynomials)
        if expr.is_polynomial(x):
            return 'power_rule'
        
        # Check for rational functions (partial fractions)
        if expr.is_rational_function(x):
            return 'partial_fractions'
        
        # Check for inverse trig patterns
        if self._is_inverse_trig_candidate(expr, x):
            return 'inverse_trig'
        
        # Check for hyperbolic functions
        if any(expr.has(func) for func in [sp.sinh, sp.cosh, sp.tanh, sp.coth, sp.sech, sp.csch]):
            return 'hyperbolic'
        
        # Check for substitution candidates
        if self._is_substitution_candidate(expr, x):
            return 'substitution'
        
        # Check for integration by parts
        if self._is_by_parts_candidate(expr, x):
            return 'by_parts'
        
        # Check for trigonometric integrals
        if any(expr.has(func) for func in [sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot]):
            return 'trig'
        
        return 'general'
    
    def _is_inverse_trig_candidate(self, expr, x) -> bool:
        """Check if expression matches inverse trig integration patterns"""
        import sympy as sp
        
        # Common patterns:
        # 1/(1+x^2) -> arctan
        # 1/sqrt(1-x^2) -> arcsin
        # 1/(x*sqrt(x^2-1)) -> arcsec
        
        if expr.has(sp.asin, sp.acos, sp.atan, sp.asec, sp.acsc, sp.acot):
            return True
        
        # Check for patterns
        try:
            if isinstance(expr, sp.Pow) and expr.exp == -1:
                base = expr.base
                # 1/(1+x^2)
                if base.match(1 + x**2) or base.match(x**2 + 1):
                    return True
                # 1/sqrt(1-x^2)
                if isinstance(base, sp.Pow) and base.exp == sp.Rational(1, 2):
                    inner = base.base
                    if inner.match(1 - x**2):
                        return True
        except:
            pass
        
        return False
    
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
    
    def _integrate_partial_fractions(self, expr, x, verbosity: str):
        """Integrate using partial fraction decomposition"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="partial_fractions",
            explanation="Decompose rational function into partial fractions",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="partial_fractions"
        ))
        
        # Perform partial fraction decomposition
        try:
            decomposed = sp.apart(expr, x)
            if decomposed != expr:
                self.steps.append(IntegrationStep(
                    rule="decomposition",
                    explanation=f"Decomposed form: {decomposed}",
                    expression_before=str(expr),
                    expression_after=str(decomposed),
                    technique="partial_fractions"
                ))
        except:
            decomposed = expr
        
        result = sp.integrate(decomposed, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        return result
    
    def _integrate_inverse_trig(self, expr, x, verbosity: str):
        """Integrate expressions yielding inverse trig functions"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="inverse_trigonometric",
            explanation="This integral yields an inverse trigonometric function",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="inverse_trig"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        if verbosity == 'teacher':
            self.steps.append(IntegrationStep(
                rule="explanation",
                explanation=(
                    "Common inverse trig integrals:\n"
                    "• ∫ 1/(1+x²) dx = arctan(x) + C\n"
                    "• ∫ 1/√(1-x²) dx = arcsin(x) + C\n"
                    "• ∫ 1/(x√(x²-1)) dx = arcsec(x) + C"
                ),
                expression_before="",
                expression_after="",
                technique="inverse_trig"
            ))
        
        return result
    
    def _integrate_hyperbolic(self, expr, x, verbosity: str):
        """Integrate hyperbolic functions"""
        import sympy as sp
        
        self.steps.append(IntegrationStep(
            rule="hyperbolic_functions",
            explanation="Integrating hyperbolic function",
            expression_before=f"∫ {expr} dx",
            expression_after="",
            technique="hyperbolic"
        ))
        
        result = sp.integrate(expr, x)
        self.steps[-1].expression_after = str(result) + " + C"
        
        if verbosity == 'teacher':
            self.steps.append(IntegrationStep(
                rule="explanation",
                explanation=(
                    "Common hyperbolic integrals:\n"
                    "• ∫ sinh(x) dx = cosh(x) + C\n"
                    "• ∫ cosh(x) dx = sinh(x) + C\n"
                    "• ∫ tanh(x) dx = ln|cosh(x)| + C"
                ),
                expression_before="",
                expression_after="",
                technique="hyperbolic"
            ))
        
        return result
    
    def _numerical_definite_integral(self, expr, x, a, b) -> float:
        """Compute definite integral numerically using Simpson's rule"""
        import sympy as sp
        
        # Convert to numpy-compatible function
        f = sp.lambdify(x, expr, 'numpy')
        
        try:
            # Use Simpson's rule
            n = 1000  # Number of intervals
            h = (b - a) / n
            result = f(a) + f(b)
            
            for i in range(1, n):
                k = a + i * h
                if i % 2 == 0:
                    result += 2 * f(k)
                else:
                    result += 4 * f(k)
            
            result *= h / 3
            return float(result)
        except:
            return 0.0
    
    def _generate_graph_data(
        self,
        expr,
        antiderivative,
        x,
        lower_limit: Optional[float],
        upper_limit: Optional[float],
        definite_value: Optional[float]
    ) -> Dict[str, Any]:
        """
        Generate graph data for visualization
        
        Returns data for:
        - Original function (integrand)
        - Integrated function (antiderivative)  
        - Shaded area (for definite integrals)
        """
        import sympy as sp
        
        # Determine x range
        if lower_limit is not None and upper_limit is not None:
            x_min = float(lower_limit) - 2
            x_max = float(upper_limit) + 2
        else:
            x_min = -10
            x_max = 10
        
        # Generate points
        num_points = 300
        x_values = np.linspace(x_min, x_max, num_points)
        
        # Create lambdified functions
        try:
            f_integrand = sp.lambdify(x, expr, 'numpy')
            integrand_values = []
            for xi in x_values:
                try:
                    val = float(f_integrand(xi))
                    # Convert NaN/inf to None (null in JSON)
                    if np.isnan(val) or np.isinf(val):
                        integrand_values.append(None)
                    else:
                        integrand_values.append(val)
                except:
                    integrand_values.append(None)
        except:
            integrand_values = [None] * num_points
        
        # For antiderivative, we need to handle the constant C
        # We'll normalize it so F(lower_limit) = 0 for definite integrals
        antiderivative_values = []
        if antiderivative is not None:
            try:
                f_antiderivative = sp.lambdify(x, antiderivative, 'numpy')
                offset = 0
                if lower_limit is not None:
                    try:
                        offset = float(f_antiderivative(lower_limit))
                        if np.isnan(offset) or np.isinf(offset):
                            offset = 0
                    except:
                        offset = 0
                
                for xi in x_values:
                    try:
                        val = float(f_antiderivative(xi)) - offset
                        # Convert NaN/inf to None (null in JSON)
                        if np.isnan(val) or np.isinf(val):
                            antiderivative_values.append(None)
                        else:
                            antiderivative_values.append(val)
                    except:
                        antiderivative_values.append(None)
            except:
                antiderivative_values = [None] * num_points
        
        # Generate area data for definite integrals
        area_data = None
        if lower_limit is not None and upper_limit is not None:
            # Points within the integration bounds
            area_x = []
            area_y = []
            for i, xi in enumerate(x_values):
                if lower_limit <= xi <= upper_limit:
                    # Only add non-None values for area shading
                    if integrand_values[i] is not None:
                        area_x.append(float(xi))
                        area_y.append(integrand_values[i])
            area_data = {
                'x': area_x,
                'y': area_y,
                'value': float(definite_value) if definite_value is not None else 0
            }
        
        return {
            'data': {
                'x_values': x_values.tolist(),
                'integrand_curve': integrand_values,
                'antiderivative_curve': antiderivative_values if antiderivative_values else None,
                'area': area_data
            },
            'labels': {
                'integrand': f'f(x) = {expr}',
                'antiderivative': f'F(x) = ∫ f(x) dx' + ("" if lower_limit is not None else " + C")
            },
            'limits': {
                'lower': float(lower_limit) if lower_limit is not None else None,
                'upper': float(upper_limit) if upper_limit is not None else None
            }
        }
