"""
Quick API test for integration endpoint
"""

import requests
import json

API_URL = "http://localhost:5000/api/compute"

def test_integration_api():
    """Test the integration API endpoint"""
    
    print("Testing Integration API Endpoint")
    print("="*60)
    
    # Test 1: Simple indefinite integral
    print("\n1. Testing indefinite integral: x**2")
    response = requests.post(API_URL, json={
        "operation": "integrate",
        "expression": "x**2",
        "variable": "x",
        "verbosity": "detailed"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Result: {data['output']}")
        print(f"   ✓ Technique: {data['technique']}")
        print(f"   ✓ Steps: {len(data['steps'])}")
        if data.get('graph') and 'integrand' in data['graph']:
            print(f"   ✓ Graph data available")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test 2: Definite integral
    print("\n2. Testing definite integral: x**2 from 0 to 1")
    response = requests.post(API_URL, json={
        "operation": "integrate",
        "expression": "x**2",
        "variable": "x",
        "lower_limit": "0",
        "upper_limit": "1",
        "verbosity": "detailed"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Result: {data['output']}")
        print(f"   ✓ Definite: {data['definite']}")
        if data.get('graph') and data['graph'].get('area'):
            print(f"   ✓ Area value: {data['graph']['area']['value']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test 3: Trigonometric function
    print("\n3. Testing trig function: sin(x)")
    response = requests.post(API_URL, json={
        "operation": "integrate",
        "expression": "sin(x)",
        "variable": "x",
        "verbosity": "detailed"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Result: {data['output']}")
        print(f"   ✓ Technique: {data['technique']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test 4: Complex expression
    print("\n4. Testing complex: x * exp(x)")
    response = requests.post(API_URL, json={
        "operation": "integrate",
        "expression": "x * exp(x)",
        "variable": "x",
        "verbosity": "detailed"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Result: {data['output']}")
        print(f"   ✓ Technique: {data['technique']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test 5: Rational function
    print("\n5. Testing rational: 1/(x**2 + 1)")
    response = requests.post(API_URL, json={
        "operation": "integrate",
        "expression": "1/(x**2 + 1)",
        "variable": "x",
        "verbosity": "detailed"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Result: {data['output']}")
        print(f"   ✓ Technique: {data['technique']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    print("\n" + "="*60)
    print("API Testing Complete!")


if __name__ == '__main__':
    try:
        test_integration_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running with: python api_server.py")
