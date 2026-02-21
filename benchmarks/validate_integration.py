"""
Benchmark Validation Dataset for Calcora Integration Engine

This script validates Calcora's integration results against SymPy (ground truth)
for standard Calculus II curriculum problems.

Purpose:
- Provide objective proof of correctness for academic review
- Document coverage across standard integration techniques
- Enable regression testing for accuracy

Usage:
    python benchmarks/validate_integration.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calcora.integration_engine import IntegrationEngine
import sympy as sp
from sympy.abc import x
import time


class BenchmarkValidator:
    """Validates integration results against SymPy"""
    
    def __init__(self):
        self.engine = IntegrationEngine()
        self.results = []
    
    def validate(self, expression, variable='x', test_name="", category=""):
        """Validate a single integration"""
        print(f"\n{'─'*80}")
        print(f"Test: {test_name} [{category}]")
        print(f"Expression: ∫ {expression} d{variable}")
        
        # Calcora result
        start = time.time()
        calcora_result = self.engine.integrate(expression, variable, verbosity='concise')
        calcora_time = (time.time() - start) * 1000  # ms
        
        # SymPy result (ground truth)
        try:
            sympy_expr = sp.sympify(expression)
            sympy_result = sp.integrate(sympy_expr, x)
            sympy_str = str(sympy_result)
        except Exception as e:
            sympy_str = f"ERROR: {str(e)}"
        
        # Compare (symbolic equality check)
        match = False
        if calcora_result['success']:
            calcora_str = str(calcora_result['output'])
            try:
                # Parse both results and check if difference is constant
                calcora_sympy = sp.sympify(calcora_str)
                diff = sp.simplify(calcora_sympy - sympy_result)
                # If difference is a number (constant of integration), it's correct
                match = diff.is_number or diff == 0
            except:
                # Fallback: string comparison (less reliable)
                match = sympy_str in calcora_str or calcora_str in sympy_str
        
        result_dict = {
            'test_name': test_name,
            'category': category,
            'expression': expression,
            'calcora_result': calcora_result.get('output', 'FAILED'),
            'sympy_result': sympy_str,
            'match': match,
            'time_ms': round(calcora_time, 2),
            'technique': calcora_result.get('technique', 'N/A'),
            'success': calcora_result['success']
        }
        
        self.results.append(result_dict)
        
        # Print result
        status = "✅ MATCH" if match else "❌ MISMATCH"
        print(f"Calcora: {calcora_result.get('output', 'FAILED')}")
        print(f"SymPy:   {sympy_str}")
        print(f"Status:  {status} | Time: {calcora_time:.2f}ms | Technique: {result_dict['technique']}")
        
        return match
    
    def print_summary(self):
        """Print benchmark summary table"""
        print("\n" + "="*80)
        print("BENCHMARK VALIDATION SUMMARY")
        print("="*80)
        
        # Category breakdown
        categories = {}
        for r in self.results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0, 'avg_time': []}
            categories[cat]['total'] += 1
            if r['match']:
                categories[cat]['passed'] += 1
            if r['success']:
                categories[cat]['avg_time'].append(r['time_ms'])
        
        print("\nBy Category:")
        for cat, stats in categories.items():
            avg_time = sum(stats['avg_time']) / len(stats['avg_time']) if stats['avg_time'] else 0
            print(f"  {cat:25s}: {stats['passed']:2d}/{stats['total']:2d} passed ({stats['passed']/stats['total']*100:.0f}%) | Avg: {avg_time:.1f}ms")
        
        # Overall stats
        total = len(self.results)
        passed = sum(1 for r in self.results if r['match'])
        avg_time = sum(r['time_ms'] for r in self.results if r['success']) / total
        
        print(f"\n{'─'*80}")
        print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print(f"Average computation time: {avg_time:.2f}ms")
        print(f"Techniques used: {len(set(r['technique'] for r in self.results))}")
        
        # Failed tests
        failed = [r for r in self.results if not r['match']]
        if failed:
            print(f"\n⚠️  Failed Tests ({len(failed)}):")
            for r in failed:
                print(f"  - {r['test_name']}: {r['expression']}")
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        return passed, total


def main():
    """Run benchmark validation suite"""
    validator = BenchmarkValidator()
    
    print("="*80)
    print("CALCORA INTEGRATION BENCHMARK VALIDATION")
    print("Comparing against SymPy (ground truth)")
    print("="*80)
    
    # Polynomials
    validator.validate("x**2", x, "Power rule (x²)", "Polynomials")
    validator.validate("x**5", x, "High degree power (x⁵)", "Polynomials")
    validator.validate("3*x**4 - 2*x**2 + 5", x, "Polynomial combination", "Polynomials")
    
    # Trigonometric
    validator.validate("sin(x)", x, "Basic sine", "Trigonometric")
    validator.validate("cos(x)", x, "Basic cosine", "Trigonometric")
    validator.validate("tan(x)", x, "Tangent", "Trigonometric")
    validator.validate("sec(x)**2", x, "Secant squared", "Trigonometric")
    validator.validate("cos(x)**2", x, "Cosine squared", "Trigonometric")
    
    # Exponential/Logarithmic
    validator.validate("exp(x)", x, "Natural exponential", "Exponential")
    validator.validate("1/x", x, "Natural logarithm (1/x)", "Exponential")
    validator.validate("log(x)", x, "Logarithm", "Exponential")
    
    # Rational Functions
    validator.validate("1/(x**2 + 1)", x, "Arctan pattern", "Rational")
    validator.validate("1/(x**2 + 4)", x, "Scaled arctan", "Rational")
    validator.validate("x/(x**2 + 1)", x, "Rational u-sub", "Rational")
    
    # Square Roots
    validator.validate("sqrt(x)", x, "Square root", "Radicals")
    validator.validate("1/sqrt(x)", x, "Inverse square root", "Radicals")
    validator.validate("x*sqrt(x)", x, "Product with sqrt", "Radicals")
    
    # Inverse Trigonometric
    validator.validate("1/sqrt(1 - x**2)", x, "Arcsin pattern", "Inverse Trig")
    validator.validate("1/(1 + x**2)", x, "Arctan pattern", "Inverse Trig")
    
    # Hyperbolic
    validator.validate("sinh(x)", x, "Hyperbolic sine", "Hyperbolic")
    validator.validate("cosh(x)", x, "Hyperbolic cosine", "Hyperbolic")
    
    # Integration by Parts
    validator.validate("x * exp(x)", x, "By parts: x*e^x", "By Parts")
    validator.validate("x * sin(x)", x, "By parts: x*sin(x)", "By Parts")
    validator.validate("x * log(x)", x, "By parts: x*ln(x)", "By Parts")
    
    # Substitution
    validator.validate("2*x * cos(x**2)", x, "U-substitution: chain rule", "Substitution")
    validator.validate("x / sqrt(x**2 + 1)", x, "U-sub with sqrt", "Substitution")
    
    # Print summary
    passed, total = validator.print_summary()
    
    # Export to markdown table
    print("\n" + "="*80)
    print("MARKDOWN TABLE (for README.md)")
    print("="*80)
    print("\n| Expression | Calcora Result | SymPy Result | Match | Time (ms) | Technique |")
    print("|------------|----------------|--------------|-------|-----------|-----------|")
    for r in validator.results[:15]:  # First 15 for brevity
        match_icon = "✅" if r['match'] else "❌"
        expr_short = r['expression'][:20] + "..." if len(r['expression']) > 20 else r['expression']
        calcora_short = str(r['calcora_result'])[:25] + "..." if len(str(r['calcora_result'])) > 25 else str(r['calcora_result'])
        sympy_short = str(r['sympy_result'])[:25] + "..." if len(str(r['sympy_result'])) > 25 else str(r['sympy_result'])
        print(f"| `{expr_short}` | `{calcora_short}` | `{sympy_short}` | {match_icon} | {r['time_ms']:.1f} | {r['technique']} |")
    
    if total > 15:
        print(f"| ... | ... | ... | ... | ... | ... |")
        print(f"| **Total** | **{passed}/{total} passed** | **{passed/total*100:.0f}% accuracy** | | **Avg: {sum(r['time_ms'] for r in validator.results)/total:.1f}ms** | |")
    
    # Exit code
    return 0 if passed == total else 1


if __name__ == '__main__':
    exit(main())
