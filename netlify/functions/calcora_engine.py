import json
import sys
import os
from typing import Any, Dict

# Add parent directory to path to import calcora
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from calcora.bootstrap import default_engine
    from calcora.renderers.json_renderer import JsonRenderer
except ImportError as e:
    # Fallback for debugging
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Import error: {str(e)}. Python path: {sys.path}"}),
        }
    sys.exit(0)


def _error(status: int, message: str) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message}),
    }


def handler(event, context):  # type: ignore[override]
    """Netlify Function entrypoint exposing Calcora API.

    Expected JSON body examples:
    
    Differentiation:
    {
      "operation": "differentiate",
      "expression": "sin(x**2)",
      "variable": "x",
      "order": 1,
      "verbosity": "detailed"
    }
    
    Matrix operations:
    {
      "operation": "matrix_determinant",
      "expression": "[[1,2],[3,4]]",
      "verbosity": "detailed"
    }
    
    {
      "operation": "matrix_multiply",
      "expression": "[[1,2],[3,4]]",
      "matrix_b": "[[5,6],[7,8]]",
      "verbosity": "detailed"
    }
    """

    if event.get("httpMethod") == "OPTIONS":
        # CORS preflight support
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    if event.get("httpMethod") != "POST":
        return _error(405, "Only POST is supported")

    raw_body = event.get("body") or "{}"
    try:
        body = json.loads(raw_body)
    except json.JSONDecodeError:
        return _error(400, "Invalid JSON body")

    operation = body.get("operation", "differentiate")
    expression = body.get("expression")
    if not expression:
        return _error(400, "Missing required field 'expression'")

    verbosity = body.get("verbosity", "detailed")
    if verbosity not in ("concise", "detailed", "teacher"):
        return _error(400, "Invalid verbosity. Use: concise, detailed, teacher")

    engine = default_engine(load_entry_points=True)

    try:
        # Differentiation operation
        if operation == "differentiate":
            variable = body.get("variable", "x")
            order = int(body.get("order", 1))
            result = engine.run(
                operation="differentiate",
                expression=expression,
                variable=variable,
                order=order,
            )
        
        # Matrix operations
        elif operation in ("matrix_multiply", "matrix_determinant", "matrix_inverse", 
                          "matrix_rref", "matrix_eigenvalues", "matrix_lu"):
            kwargs = {"operation": operation, "expression": expression}
            
            # Matrix multiply needs second matrix
            if operation == "matrix_multiply":
                matrix_b = body.get("matrix_b")
                if not matrix_b:
                    return _error(400, "matrix_multiply requires 'matrix_b' field")
                kwargs["matrix_b"] = matrix_b
            
            result = engine.run(**kwargs)
        
        else:
            return _error(400, f"Unsupported operation '{operation}'. Supported: differentiate, matrix_multiply, matrix_determinant, matrix_inverse, matrix_rref, matrix_eigenvalues, matrix_lu")

    except ValueError as exc:
        return _error(400, str(exc))
    except Exception as exc:  # pragma: no cover - defensive
        return _error(500, f"Unexpected error: {exc}")

    renderer = engine.registry.get_renderer(format="json") or JsonRenderer()
    rendered = renderer.render(result=result, format="json", verbosity=verbosity)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": rendered,
    }
