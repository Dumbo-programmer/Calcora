"""
Test suite for enhanced integration engine with graphing capabilities
Tests comprehensive integration coverage for v0.2+
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from calcora.integration_engine import IntegrationEngine


def test_integration(expression, variable='x', lower=None, upper=None, test_name=""):
    """Helper function to test integration"""
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Expression: ∫ {expression} d{variable}")
    if lower is not None and upper is not None:
        print(f"Limits: [{lower}, {upper}]")
    
    engine = IntegrationEngine()
    try:
        result = engine.integrate(
            expression=expression,
            variable=variable,
            lower_limit=lower,
            upper_limit=upper,
            verbosity='detailed',
            generate_graph=True
        )
        
        if result.get('success'):
            print(f"✓ Result: {result['output']}")
            print(f"  Technique: {result['technique']}")
            print(f"  Steps: {len(result['steps'])}")
            
            # Check graph data
            if result.get('graph'):
                graph = result['graph']
                if 'integrand' in graph:
                    print(f"  Graph: ✓ Integrand data available ({len(graph['integrand']['x'])} points)")
                if 'antiderivative' in graph and graph['antiderivative']:
                    print(f"  Graph: ✓ Antiderivative data available")
                if 'area' in graph and graph['area']:
                    print(f"  Graph: ✓ Area data (value={graph['area']['value']:.6f})")
            
            return True
        else:
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*80)
    print("ENHANCED INTEGRATION ENGINE TEST SUITE")
    print("Testing comprehensive integration with graphing")
    print("="*80)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Basic Polynomials
    tests_total += 1
    if test_integration("x**2", test_name="Basic polynomial x²"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x**3 + 2*x**2 + 3*x + 4", test_name="Higher degree polynomial"):
        tests_passed += 1
    
    # Test 2: Trigonometric Functions
    tests_total += 1
    if test_integration("sin(x)", test_name="Simple sine"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("cos(x)**2", test_name="Cosine squared"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("tan(x)", test_name="Tangent"):
        tests_passed += 1
    
    # Test 3: Exponential and Logarithmic
    tests_total += 1
    if test_integration("exp(x)", test_name="Exponential e^x"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("1/x", test_name="Natural log (1/x)"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x * exp(x)", test_name="Product requiring by parts"):
        tests_passed += 1
    
    # Test 4: Rational Functions (Partial Fractions)
    tests_total += 1
    if test_integration("1/(x**2 + 1)", test_name="Rational -> arctan"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("1/(x**2 + 2*x + 1)", test_name="Rational with repeated root"):
        tests_passed += 1
    
    # Test 5: Inverse Trigonometric
    tests_total += 1
    if test_integration("1/sqrt(1 - x**2)", test_name="Inverse trig -> arcsin"):
        tests_passed += 1
    
    # Test 6: Square Roots
    tests_total += 1
    if test_integration("sqrt(x)", test_name="Square root"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("1/sqrt(x)", test_name="Inverse square root"):
        tests_passed += 1
    
    # Test 7: Hyperbolic Functions
    tests_total += 1
    if test_integration("sinh(x)", test_name="Hyperbolic sine"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("cosh(x)", test_name="Hyperbolic cosine"):
        tests_passed += 1
    
    # Test 8: Definite Integrals
    tests_total += 1
    if test_integration("x**2", lower=0, upper=1, test_name="Definite integral of x² from 0 to 1"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("sin(x)", lower=0, upper=3.14159, test_name="Definite integral of sin(x) from 0 to π"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("exp(x)", lower=0, upper=1, test_name="Definite integral of e^x from 0 to 1"):
        tests_passed += 1
    
    # Test 9: Complex Expressions
    tests_total += 1
    if test_integration("x * sin(x)", test_name="Complex by parts"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("exp(x) * cos(x)", test_name="Exponential-trig product"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x**2 * exp(-x)", test_name="Polynomial-exponential"):
        tests_passed += 1
    
    # Test 10: Substitution Candidates
    tests_total += 1
    if test_integration("2*x * cos(x**2)", test_name="U-substitution candidate"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x / sqrt(x**2 + 1)", test_name="Substitution with sqrt"):
        tests_passed += 1
    
    # Test 11: Advanced Functions
    tests_total += 1
    if test_integration("log(x)", test_name="Natural logarithm"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x * log(x)", test_name="Product with log"):
        tests_passed += 1
    
    # Test 12: Mixed Functions
    tests_total += 1
    if test_integration("sin(x) * cos(x)", test_name="Trig product"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("x / (1 + x**2)", test_name="Rational with arctan result"):
        tests_passed += 1
    
    # Test 13: Definite Integrals with Area
    tests_total += 1
    if test_integration("x**2", lower=-1, upper=1, test_name="Symmetric definite integral"):
        tests_passed += 1
    
    tests_total += 1
    if test_integration("sin(x)", lower=-3.14159, upper=3.14159, test_name="Symmetric trig integral"):
        tests_passed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total*100):.1f}%")
    
    if tests_passed == tests_total:
        print("\n🎉 ALL TESTS PASSED! Integration engine is production ready!")
        return 0
    else:
        print(f"\n⚠ {tests_total - tests_passed} test(s) failed. Review failures above.")
        return 1


if __name__ == '__main__':
    exit(main())
