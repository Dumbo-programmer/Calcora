"""
Test suite for malformed and edge-case input handling.

Purpose: Ensure Calcora handles invalid/malicious input gracefully without:
- Crashing
- Silent failures
- Infinite loops
- Security vulnerabilities

Critical for classroom use where students may enter anything.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calcora.integration_engine import IntegrationEngine


class TestMalformedInputIntegration:
    """Test malformed input for integration"""
    
    def setup_method(self):
        self.engine = IntegrationEngine()
    
    def test_empty_string(self):
        """Empty expression should fail gracefully"""
        result = self.engine.integrate("", variable="x")
        assert result['success'] is False
        assert 'error' in result or 'message' in result
    
    def test_whitespace_only(self):
        """Whitespace-only expression should fail gracefully"""
        result = self.engine.integrate("   ", variable="x")
        assert result['success'] is False
    
    def test_invalid_syntax(self):
        """Invalid mathematical syntax should fail gracefully"""
        test_cases = [
            "x +",  # Incomplete expression
            "* x",  # Starts with operator
            "x **",  # Incomplete operator
            "((x",  # Unmatched parentheses
            "x))",  # Unmatched parentheses
            "x ++ x",  # Invalid C-style operator
        ]
        for expr in test_cases:
            result = self.engine.integrate(expr, variable="x")
            assert result['success'] is False, f"Should fail on: {expr}"
    
    def test_undefined_symbols(self):
        """Unknown symbols should be handled"""
        result = self.engine.integrate("xyz123", variable="x")
        # May succeed (treating as constant) or fail - either is acceptable
        # Key: should not crash
        assert 'error' in result or 'success' in result
    
    def test_division_by_zero(self):
        """Division by zero expressions should be detected"""
        result = self.engine.integrate("1/0", variable="x")
        assert result['success'] is False
    
    def test_extremely_long_expression(self):
        """Very long expressions should not cause timeout"""
        # 100-term polynomial
        long_expr = " + ".join([f"x**{i}" for i in range(100)])
        result = self.engine.integrate(long_expr, variable="x", timeout=5.0)
        # May succeed or fail - key is it returns within timeout
        assert 'success' in result
    
    def test_deeply_nested_parentheses(self):
        """Deeply nested expressions should not cause stack overflow"""
        nested = "x"
        for _ in range(50):
            nested = f"({nested})"
        result = self.engine.integrate(nested, variable="x")
        assert 'success' in result  # Should complete without crashing
    
    def test_special_characters(self):
        """Special characters should be rejected"""
        special_inputs = [
            "x@2",
            "x#x",
            "x$2",
            "x%2",
            "x&x",
            "'; DROP TABLE;",  # SQL injection attempt
            "<script>alert(1)</script>",  # XSS attempt
        ]
        for expr in special_inputs:
            result = self.engine.integrate(expr, variable="x")
            assert result['success'] is False
    
    def test_unicode_characters(self):
        """Unicode/emoji should be rejected gracefully"""
        result = self.engine.integrate("x² + 2x", variable="x")  # Superscript 2
        # May or may not work - key is no crash
        assert 'success' in result
    
    def test_empty_variable(self):
        """Empty variable name should fail"""
        result = self.engine.integrate("x**2", variable="")
        assert result['success'] is False
    
    def test_multi_char_variable(self):
        """Variables with multiple characters should work or fail gracefully"""
        result = self.engine.integrate("theta**2", variable="theta")
        # May work or fail - key is no crash
        assert 'success' in result


class TestInputSanitization:
    """Test that input sanitization prevents exploits"""
    
    def test_no_code_execution(self):
        """Ensure eval/exec is not used unsafely"""
        integration = IntegrationEngine()
        
        # These should NOT execute arbitrary Python code
        dangerous_inputs = [
            "__import__('os').system('ls')",
            "eval('2+2')",
            "exec('print(1)')",
            "compile('1+1', '', 'eval')",
        ]
        
        for dangerous in dangerous_inputs:
            result = integration.integrate(dangerous, variable="x")
            # Should fail to parse, NOT execute
            assert result['success'] is False
    
    def test_no_file_access(self):
        """Ensure file paths in expressions don't cause file access"""
        integration = IntegrationEngine()
        
        file_paths = [
            "/etc/passwd",
            "C:\\Windows\\System32",
            "../../../etc/shadow",
        ]
        
        for path in file_paths:
            result = integration.integrate(path, variable="x")
            # Should fail to parse as math, not attempt file access
            assert result['success'] is False


class TestEdgeCases:
    """Mathematical edge cases"""
    
    def test_discontinuous_integration(self):
        """Integration across discontinuity should be detected"""
        integration = IntegrationEngine()
        
        # 1/x is discontinuous at x=0
        # Definite integral from -1 to 1 should fail or warn
        result = integration.integrate("1/x", variable="x", lower_limit=-1, upper_limit=1)
        # Should either fail or include warning
        if result['success']:
            assert 'warning' in result or 'discontinuous' in str(result).lower()
    
    def test_improper_integral_infinite_limit(self):
        """Improper integrals with infinite limits"""
        integration = IntegrationEngine()
        
        # ∫[1,∞] 1/x² dx should converge to 1
        result = integration.integrate("1/x**2", variable="x", lower_limit=1, upper_limit=float('inf'))
        # Should handle gracefully (may not support infinite limits yet)
        assert 'success' in result
    
    def test_domain_error_in_integral(self):
        """Integration of function outside its domain"""
        integration = IntegrationEngine()
        
        # √x is undefined for x < 0
        result = integration.integrate("sqrt(x)", variable="x", lower_limit=-1, upper_limit=1)
        # Should detect domain issue
        if result['success']:
            assert 'warning' in result or 'domain' in str(result).lower()
    
    def test_very_large_numbers(self):
        """Very large coefficients"""
        integration = IntegrationEngine()
        result = integration.integrate("1e100 * x", variable="x")
        assert 'success' in result  # Should handle without overflow
    
    def test_very_small_numbers(self):
        """Very small coefficients"""
        integration = IntegrationEngine()
        result = integration.integrate("1e-100 * x", variable="x")
        assert 'success' in result  # Should handle without underflow


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
