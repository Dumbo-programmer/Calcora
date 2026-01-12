"""
Comprehensive edge case testing for the integration engine.
Tests error handling, edge cases, and potential breaking scenarios.
"""
import sys
sys.path.insert(0, 'src')

from calcora.integration_engine import IntegrationEngine
import traceback

def test_case(name, expression, variable='x', lower=None, upper=None, should_fail=False):
    """Run a single test case"""
    print(f"\n{'='*70}")
    print(f"Test: {name}")
    print(f"Expression: {expression}")
    if lower is not None and upper is not None:
        print(f"Bounds: [{lower}, {upper}]")
    print(f"{'='*70}")
    
    try:
        engine = IntegrationEngine()
        result = engine.integrate(expression, variable, lower, upper, verbosity='detailed')
        
        if should_fail:
            print(f"❌ FAIL: Expected error but got result: {result.get('output')}")
            return False
        else:
            print(f"✅ PASS: {result.get('output')}")
            print(f"Technique: {result.get('technique')}")
            print(f"Steps: {len(result.get('steps', []))} steps")
            return True
    except Exception as e:
        if should_fail:
            print(f"✅ PASS: Expected error caught: {type(e).__name__}: {str(e)[:100]}")
            return True
        else:
            print(f"❌ FAIL: Unexpected error: {type(e).__name__}: {str(e)}")
            traceback.print_exc()
            return False

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print("INTEGRATION ENGINE - COMPREHENSIVE TESTING")
    print("="*70)
    
    passed = 0
    failed = 0
    
    # ============ BASIC TESTS ============
    print("\n\n### BASIC POLYNOMIAL TESTS ###")
    
    tests = [
        ("Simple power", "x", "x"),
        ("Quadratic", "x**2", "x"),
        ("Cubic", "x**3", "x"),
        ("Higher power", "x**5", "x"),
        ("Constant", "5", "x"),
        ("Linear with coefficient", "3*x", "x"),
        ("Sum of powers", "x**2 + 2*x + 1", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ TRIGONOMETRIC TESTS ============
    print("\n\n### TRIGONOMETRIC TESTS ###")
    
    tests = [
        ("sin(x)", "sin(x)", "x"),
        ("cos(x)", "cos(x)", "x"),
        ("tan(x)", "tan(x)", "x"),
        ("sin(2*x)", "sin(2*x)", "x"),
        ("cos**2", "cos(x)**2", "x"),
        ("sin**2", "sin(x)**2", "x"),
        ("sin*cos", "sin(x)*cos(x)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ EXPONENTIAL & LOGARITHMIC ============
    print("\n\n### EXPONENTIAL & LOGARITHMIC TESTS ###")
    
    tests = [
        ("e^x", "exp(x)", "x"),
        ("e^(2x)", "exp(2*x)", "x"),
        ("ln(x)", "log(x)", "x"),
        ("1/x", "1/x", "x"),
        ("x*e^x", "x*exp(x)", "x"),
        ("x**2*e^x", "x**2*exp(x)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ DEFINITE INTEGRALS ============
    print("\n\n### DEFINITE INTEGRAL TESTS ###")
    
    tests = [
        ("x^2 from 0 to 1", "x**2", "x", 0, 1),
        ("x^2 from -1 to 1", "x**2", "x", -1, 1),
        ("sin(x) from 0 to pi", "sin(x)", "x", 0, 3.14159),
        ("e^x from 0 to 1", "exp(x)", "x", 0, 1),
        ("1/x from 1 to e", "1/x", "x", 1, 2.71828),
    ]
    
    for name, expr, var, lower, upper in tests:
        if test_case(name, expr, var, lower, upper):
            passed += 1
        else:
            failed += 1
    
    # ============ EDGE CASES & ERROR HANDLING ============
    print("\n\n### EDGE CASES & ERROR HANDLING ###")
    
    # These should work
    tests = [
        ("Negative power", "x**(-1)", "x", None, None, False),
        ("Fractional power", "x**(1/2)", "x", None, None, False),
        ("Complex expression", "x**2 + sin(x) + exp(x)", "x", None, None, False),
        ("Different variable", "t**2", "t", None, None, False),
    ]
    
    for name, expr, var, lower, upper, should_fail in tests:
        if test_case(name, expr, var, lower, upper, should_fail):
            passed += 1
        else:
            failed += 1
    
    # ============ RATIONAL FUNCTIONS ============
    print("\n\n### RATIONAL FUNCTION TESTS ###")
    
    tests = [
        ("Simple rational", "1/(x+1)", "x"),
        ("Rational with power", "x/(x**2+1)", "x"),
        ("Complex rational", "(x**2+1)/(x+1)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ SQUARE ROOTS & RADICALS ============
    print("\n\n### SQUARE ROOTS & RADICALS ###")
    
    tests = [
        ("sqrt(x)", "sqrt(x)", "x"),
        ("sqrt(x**2+1)", "sqrt(x**2+1)", "x"),
        ("1/sqrt(x)", "1/sqrt(x)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ INVERSE TRIG ============
    print("\n\n### INVERSE TRIGONOMETRIC ###")
    
    tests = [
        ("arcsin(x)", "asin(x)", "x"),
        ("arccos(x)", "acos(x)", "x"),
        ("arctan(x)", "atan(x)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ HYPERBOLIC ============
    print("\n\n### HYPERBOLIC FUNCTIONS ###")
    
    tests = [
        ("sinh(x)", "sinh(x)", "x"),
        ("cosh(x)", "cosh(x)", "x"),
        ("tanh(x)", "tanh(x)", "x"),
    ]
    
    for name, expr, var in tests:
        if test_case(name, expr, var):
            passed += 1
        else:
            failed += 1
    
    # ============ RESULTS ============
    print("\n\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📊 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%")
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
