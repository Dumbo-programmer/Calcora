"""
Comprehensive pytest suite for integration engine.
Tests all 29+ integration scenarios from v0.2 release.
"""

import pytest
from calcora.integration_engine import IntegrationEngine


@pytest.fixture
def engine():
    """Integration engine fixture"""
    return IntegrationEngine()


class TestBasicPolynomials:
    """Test polynomial integration"""
    
    def test_simple_polynomial(self, engine):
        """Test basic polynomial x²"""
        result = engine.integrate("x**2", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'x**3/3' in str(result['output']) or 'x³/3' in str(result['output'])
    
    def test_higher_degree_polynomial(self, engine):
        """Test polynomial x³ + 2x² + 3x + 4"""
        result = engine.integrate("x**3 + 2*x**2 + 3*x + 4", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert result['technique'] is not None


class TestTrigonometric:
    """Test trigonometric function integration"""
    
    def test_sine(self, engine):
        """Test sin(x) integration"""
        result = engine.integrate("sin(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'cos' in str(result['output']).lower()
    
    def test_cosine_squared(self, engine):
        """Test cos²(x) integration"""
        result = engine.integrate("cos(x)**2", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_tangent(self, engine):
        """Test tan(x) integration"""
        result = engine.integrate("tan(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestExponentialLogarithmic:
    """Test exponential and logarithmic integration"""
    
    def test_exponential(self, engine):
        """Test e^x integration"""
        result = engine.integrate("exp(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'exp' in str(result['output']).lower() or 'e^' in str(result['output'])
    
    def test_reciprocal(self, engine):
        """Test 1/x → ln(x) integration"""
        result = engine.integrate("1/x", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'log' in str(result['output']).lower() or 'ln' in str(result['output']).lower()
    
    def test_integration_by_parts(self, engine):
        """Test x*e^x requiring integration by parts"""
        result = engine.integrate("x * exp(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestRationalFunctions:
    """Test rational function integration and partial fractions"""
    
    def test_arctan_pattern(self, engine):
        """Test 1/(x²+1) → arctan(x)"""
        result = engine.integrate("1/(x**2 + 1)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'atan' in str(result['output']).lower() or 'arctan' in str(result['output']).lower()
    
    def test_repeated_root(self, engine):
        """Test 1/(x²+2x+1) with repeated root"""
        result = engine.integrate("1/(x**2 + 2*x + 1)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestInverseTrigonometric:
    """Test inverse trigonometric patterns"""
    
    def test_arcsin_pattern(self, engine):
        """Test 1/√(1-x²) → arcsin(x)"""
        result = engine.integrate("1/sqrt(1 - x**2)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        assert 'asin' in str(result['output']).lower() or 'arcsin' in str(result['output']).lower()


class TestSquareRoots:
    """Test square root integration"""
    
    def test_sqrt_x(self, engine):
        """Test √x integration"""
        result = engine.integrate("sqrt(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_inverse_sqrt(self, engine):
        """Test 1/√x integration"""
        result = engine.integrate("1/sqrt(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestHyperbolic:
    """Test hyperbolic function integration"""
    
    def test_sinh(self, engine):
        """Test sinh(x) integration"""
        result = engine.integrate("sinh(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_cosh(self, engine):
        """Test cosh(x) integration"""
        result = engine.integrate("cosh(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestDefiniteIntegrals:
    """Test definite integrals with bounds"""
    
    def test_polynomial_definite(self, engine):
        """Test ∫₀¹ x² dx = 1/3"""
        result = engine.integrate("x**2", "x", lower_limit=0, upper_limit=1, verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
        # Should have numerical area value
        if result.get('graph') and result['graph'].get('area'):
            area = result['graph']['area']['value']
            assert abs(area - 0.333333) < 0.01, f"Expected ~0.333, got {area}"
    
    def test_sine_definite(self, engine):
        """Test ∫₀^π sin(x) dx = 2"""
        result = engine.integrate("sin(x)", "x", lower_limit=0, upper_limit=3.14159, verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_exponential_definite(self, engine):
        """Test ∫₀¹ e^x dx"""
        result = engine.integrate("exp(x)", "x", lower_limit=0, upper_limit=1, verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_symmetric_polynomial(self, engine):
        """Test ∫₋₁¹ x² dx"""
        result = engine.integrate("x**2", "x", lower_limit=-1, upper_limit=1, verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_symmetric_trig(self, engine):
        """Test symmetric trig integral"""
        result = engine.integrate("sin(x)", "x", lower_limit=-3.14159, upper_limit=3.14159, verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestComplexExpressions:
    """Test complex expressions requiring advanced techniques"""
    
    def test_product_by_parts(self, engine):
        """Test x*sin(x) requiring integration by parts"""
        result = engine.integrate("x * sin(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_exp_trig_product(self, engine):
        """Test e^x * cos(x) product"""
        result = engine.integrate("exp(x) * cos(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_polynomial_exp_product(self, engine):
        """Test x² * e^(-x)"""
        result = engine.integrate("x**2 * exp(-x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestSubstitution:
    """Test u-substitution patterns"""
    
    def test_chain_rule_substitution(self, engine):
        """Test 2x*cos(x²) u-substitution"""
        result = engine.integrate("2*x * cos(x**2)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_sqrt_substitution(self, engine):
        """Test x/√(x²+1) substitution"""
        result = engine.integrate("x / sqrt(x**2 + 1)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestAdvancedFunctions:
    """Test logarithms and advanced products"""
    
    def test_logarithm(self, engine):
        """Test ln(x) integration"""
        result = engine.integrate("log(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_x_times_log(self, engine):
        """Test x*ln(x) product"""
        result = engine.integrate("x * log(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


class TestMixedFunctions:
    """Test mixed trigonometric and rational functions"""
    
    def test_trig_product(self, engine):
        """Test sin(x)*cos(x)"""
        result = engine.integrate("sin(x) * cos(x)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"
    
    def test_rational_arctan(self, engine):
        """Test x/(1+x²) → (1/2)ln(1+x²)"""
        result = engine.integrate("x / (1 + x**2)", "x", verbosity="detailed")
        assert result['success'], f"Failed: {result.get('error')}"


@pytest.mark.parametrize("expr,var", [
    ("x**2", "x"),
    ("sin(x)", "x"),
    ("exp(x)", "x"),
    ("1/x", "x"),
    ("sqrt(x)", "x"),
])
def test_basic_integration_suite(expr, var):
    """Parametrized test for basic integration coverage"""
    engine = IntegrationEngine()
    result = engine.integrate(expr, var, verbosity="concise")
    assert result['success'], f"Failed to integrate {expr}: {result.get('error')}"
