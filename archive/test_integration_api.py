"""
Quick test script for the integration API endpoint.
Run this to verify the integration feature works correctly.
"""
import requests
import json

API_URL = "http://localhost:8000/api/compute"

def test_integration(expression, variable="x", lower_limit=None, upper_limit=None, verbosity="detailed"):
    """Test integration API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: ∫ {expression} d{variable}")
    if lower_limit is not None and upper_limit is not None:
        print(f"Bounds: [{lower_limit}, {upper_limit}]")
    print(f"{'='*60}")
    
    payload = {
        "operation": "integrate",
        "expression": expression,
        "variable": variable,
        "verbosity": verbosity
    }
    
    if lower_limit is not None:
        payload["lower_limit"] = str(lower_limit)
    if upper_limit is not None:
        payload["upper_limit"] = str(upper_limit)
    
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Result: {data.get('output', 'N/A')}")
            print(f"Technique: {data.get('technique', 'N/A')}")
            print(f"\nStep-by-step explanation:")
            steps = data.get('steps', [])
            for i, step in enumerate(steps, 1):
                print(f"  {i}. [{step.get('rule', 'N/A')}] {step.get('explanation', 'N/A')}")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    print("\n🧪 Testing Calcora Integration API\n")
    
    # Test 1: Simple power rule
    test_integration("x**2", "x")
    
    # Test 2: Trigonometric
    test_integration("sin(x)", "x")
    
    # Test 3: Exponential
    test_integration("exp(x)", "x")
    
    # Test 4: Definite integral
    test_integration("x**2", "x", lower_limit=0, upper_limit=1)
    
    # Test 5: Integration by parts candidate
    test_integration("x * exp(x)", "x")
    
    # Test 6: Trig identity
    test_integration("cos(x)**2", "x")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")
