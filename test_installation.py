#!/usr/bin/env python
"""
Test script to verify Calcora installation.
Run this after: pip install -e ".[engine-sympy,cli,api]"
"""

def test_installation():
    """Test that Calcora is installed and working."""
    print("Testing Calcora installation...\n")
    
    # Test 1: Import core modules
    print("✓ Test 1: Importing modules...")
    try:
        from calcora.bootstrap import default_engine
        from calcora.engine.models import EngineResult
        print("  ✓ Core modules imported successfully")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False
    
    # Test 2: Create engine
    print("\n✓ Test 2: Creating engine...")
    try:
        engine = default_engine(load_entry_points=True)
        print("  ✓ Engine created successfully")
    except Exception as e:
        print(f"  ✗ Engine creation failed: {e}")
        return False
    
    # Test 3: Differentiation
    print("\n✓ Test 3: Testing differentiation...")
    try:
        result = engine.run(operation="differentiate", expression="x**2")
        assert result.output == "2*x", f"Expected '2*x', got '{result.output}'"
        print(f"  ✓ d/dx(x²) = {result.output}")
    except Exception as e:
        print(f"  ✗ Differentiation failed: {e}")
        return False
    
    # Test 4: Matrix determinant
    print("\n✓ Test 4: Testing matrix operations...")
    try:
        result = engine.run(operation="matrix_determinant", expression="[[1,2],[3,4]]")
        print(f"  ✓ det([[1,2],[3,4]]) = {result.output}")
    except Exception as e:
        print(f"  ✗ Matrix operation failed: {e}")
        return False
    
    # Test 5: Symbolic matrix
    print("\n✓ Test 5: Testing symbolic matrices...")
    try:
        result = engine.run(operation="matrix_determinant", expression='[["a","b"],["c","d"]]')
        assert "a*d" in result.output and "b*c" in result.output
        print(f"  ✓ det([[a,b],[c,d]]) = {result.output}")
    except Exception as e:
        print(f"  ✗ Symbolic matrix failed: {e}")
        return False
    
    print("\n" + "="*50)
    print("✓ All tests passed! Calcora is ready to use.")
    print("="*50)
    print("\nQuick commands to try:")
    print("  calcora differentiate 'sin(x**2)'")
    print("  calcora matrix-determinant '[[1,2],[3,4]]'")
    print("  uvicorn calcora.api.main:app --reload")
    print("\nFor full documentation, see README.md")
    return True


if __name__ == "__main__":
    import sys
    success = test_installation()
    sys.exit(0 if success else 1)
