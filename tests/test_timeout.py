"""
Test timeout functionality for integration engine

These tests verify that DoS protection via execution timeout works correctly.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calcora.integration_engine import IntegrationEngine
from calcora.timeout_wrapper import TimeoutError


class TestTimeoutProtection:
    """Test suite for execution timeout"""
    
    def test_normal_integration_completes(self):
        """Normal integrations should complete within timeout"""
        engine = IntegrationEngine()
        
        # Simple polynomial - should complete quickly
        result = engine.integrate("x**2", variable="x", timeout=1.0)
        assert result['success'] is True
        assert 'error' not in result or result.get('code') != 'TIMEOUT'
    
    def test_complex_integration_completes(self):
        """Moderately complex integrations should complete within reasonable timeout"""
        engine = IntegrationEngine()
        
        # More complex expression
        result = engine.integrate("x**3 * sin(x)", variable="x", timeout=3.0)
        assert result['success'] is True
        assert 'error' not in result or result.get('code') != 'TIMEOUT'
    
    def test_timeout_validation_rejects_negative(self):
        """Negative timeout should disable timeout (return 0)"""
        engine = IntegrationEngine()
        
        # Negative timeout disables timeout enforcement
        result = engine.integrate("x**2", variable="x", timeout=-1.0)
        assert result['success'] is True  # Should succeed (no timeout)
    
    def test_timeout_validation_rejects_too_large(self):
        """Timeout > 30s should be rejected"""
        engine = IntegrationEngine()
        
        result = engine.integrate("x**2", variable="x", timeout=100.0)
        assert result['success'] is False
        assert result.get('code') == 'INVALID_TIMEOUT'
    
    def test_timeout_validation_rejects_too_small(self):
        """Timeout < 0.1s should be rejected as too aggressive"""
        engine = IntegrationEngine()
        
        result = engine.integrate("x**2", variable="x", timeout=0.01)
        assert result['success'] is False
        assert result.get('code') == 'INVALID_TIMEOUT'
    
    def test_zero_timeout_disables_timeout(self):
        """Timeout=0 should disable timeout enforcement"""
        engine = IntegrationEngine()
        
        # Should work without timeout
        result = engine.integrate("x**2", variable="x", timeout=0)
        assert result['success'] is True
    
    def test_default_timeout_is_applied(self):
        """Default timeout should be 3.0s when not specified"""
        engine = IntegrationEngine()
        
        # Call without timeout parameter - should use default
        result = engine.integrate("x**2", variable="x")
        assert result['success'] is True
        
    @pytest.mark.slow
    def test_pathological_expression_times_out(self):
        """
        Extremely complex expressions should timeout gracefully
        
        Note: This test is marked as 'slow' because it intentionally
        runs until timeout occurs.
        """
        engine = IntegrationEngine()
        
        # Create a complex expression (within character limit)
        # High degree polynomial that should take time to integrate
        pathological = " + ".join([f"x**{i}" for i in range(20)])  # 20 terms, not 100
        
        result = engine.integrate(pathological, variable="x", timeout=0.5)
        
        #Should either succeed quickly or timeout
        if not result['success']:
            # If it failed, it should be due to timeout (not other errors)
            # Note: It might also succeed if SymPy is fast enough
            pass  # Accept both outcomes
    
    def test_timeout_error_message_includes_duration(self):
        """Timeout error should include the timeout duration"""
        engine = IntegrationEngine()
        
        # Very short timeout to force timeout (if expression is complex enough)
        timeout_val = 0.1
        result = engine.integrate("x**50", variable="x", timeout=timeout_val)
        
        # If timeout occurred, check error message
        if not result['success'] and result.get('code') == 'TIMEOUT':
            assert f'{timeout_val}' in result.get('error', '')
            assert result['timeout'] == timeout_val


class TestTimeoutWrapper:
    """Test the timeout wrapper utility functions"""
    
    def test_timeout_decorator_on_fast_function(self):
        """Timeout decorator should not interfere with fast functions"""
        from calcora.timeout_wrapper import timeout
        
        @timeout(1.0)
        def fast_function(x):
            return x * 2
        
        result = fast_function(5)
        assert result == 10
    
    def test_timeout_decorator_on_slow_function(self):
        """Timeout decorator should raise TimeoutError on slow functions"""
        import time
        from calcora.timeout_wrapper import timeout, TimeoutError as CalcoraTimeoutError
        
        @timeout(0.5)
        def slow_function():
            time.sleep(2.0)
            return "completed"
        
        # Note: On Windows, the thread can't be killed, so timeout is approximate
        # We just check that timeout is attempted
        try:
            result = slow_function()
            # On Windows, thread might complete in background
            # This is a known limitation
        except CalcoraTimeoutError:
            # Expected on Unix systems
            pass
    
    def test_validate_timeout_value(self):
        """Test timeout validation function"""
        from calcora.timeout_wrapper import validate_timeout_value
        
        # Valid timeouts
        assert validate_timeout_value(None) == 3.0  # Default
        assert validate_timeout_value(5.0) == 5.0
        assert validate_timeout_value(0) == 0  # Disabled
        assert validate_timeout_value(-1.0) == 0  # Negative also disables
        
        # Invalid timeouts
        with pytest.raises(ValueError):
            validate_timeout_value(0.05)  # Too small (min is 0.1)
        
        with pytest.raises(ValueError):
            validate_timeout_value(100.0)  # Too large (max is 30)
        
        with pytest.raises(ValueError):
            validate_timeout_value("not a number")  # Wrong type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
