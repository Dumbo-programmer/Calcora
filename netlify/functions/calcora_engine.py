import json
from typing import Any, Dict

from calcora.bootstrap import default_engine
from calcora.renderers.json_renderer import JsonRenderer


def _error(status: int, message: str) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message}),
    }


def handler(event, context):  # type: ignore[override]
    """Netlify Function entrypoint exposing a small Calcora API.

    Expected JSON body, for example:
    {
      "operation": "differentiate",
      "expression": "sin(x**2)",
      "variable": "x",
      "order": 1,
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

    variable = body.get("variable", "x")
    order = int(body.get("order", 1))
    verbosity = body.get("verbosity", "detailed")

    if verbosity not in ("concise", "detailed", "teacher"):
        return _error(400, "Invalid verbosity. Use: concise, detailed, teacher")

    engine = default_engine(load_entry_points=True)

    try:
        if operation == "differentiate":
            result = engine.run(
                operation="differentiate",
                expression=expression,
                variable=variable,
                order=order,
            )
        else:
            return _error(400, f"Unsupported operation '{operation}' in Netlify Function")

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
