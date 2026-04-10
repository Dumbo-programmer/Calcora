from __future__ import annotations

import importlib.resources
import os
import sys
from pathlib import Path
import json

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import Response
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
except Exception as e:  # noqa: BLE001
    raise RuntimeError(
        "FastAPI is not installed. Install with: pip install 'calcora[api]'"
    ) from e

from ..bootstrap import default_engine
from ..renderers.json_renderer import JsonRenderer

try:
    import sympy as sp
except Exception as e:  # noqa: BLE001
    raise RuntimeError(
        "SymPy is required for multivariable endpoints. Install with: pip install sympy"
    ) from e


class MatrixRequest(BaseModel):
    matrix: str
    format: str = "json"
    verbosity: str = "detailed"


class MatrixMultiplyRequest(BaseModel):
    matrix_a: str
    matrix_b: str
    format: str = "json"
    verbosity: str = "detailed"


class MultivariableRequest(BaseModel):
    expression: str
    variables: list[str]
    point: dict[str, float] | None = None
    direction: list[float] | None = None
    format: str = "json"
    verbosity: str = "detailed"


class SymbolicRequest(BaseModel):
    operation: str
    expression: str
    variable: str = "x"
    point: float | None = None
    order: int = 5
    format: str = "json"
    verbosity: str = "detailed"


app = FastAPI(title="Calcora API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://calcoralive.netlify.app",
        "http://localhost:5173",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "*"  # Allow all origins for demo purposes
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _web_path(name: str):
    """Get path to web resources, works both in development and PyInstaller bundle."""
    # Check if running in PyInstaller bundle
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS) / "calcora" / "web"
        if name == ".":
            return base_path
        return base_path / name
    else:
        # Running in normal Python environment
        return importlib.resources.files("calcora.web").joinpath(name)


app.mount(
    "/static",
    StaticFiles(directory=str(_web_path("."))),
    name="static",
)


@app.get("/")
def ui():
    web_file = _web_path("index.html")
    if isinstance(web_file, Path):
        content = web_file.read_text(encoding="utf-8")
    else:
        content = web_file.read_text(encoding="utf-8")
    return Response(content=content, media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}


def _validate_verbosity(verbosity: str) -> str | None:
    if verbosity not in ("concise", "detailed", "teacher"):
        return f"Invalid verbosity '{verbosity}'. Valid options: concise, detailed, teacher"
    return None


def _parse_multivariable_expression(expression: str, variables: list[str]):
    if not expression or not expression.strip():
        raise ValueError("Missing required field 'expression'")
    if not variables:
        raise ValueError("Missing required field 'variables' (example: ['x','y'])")

    symbols = [sp.Symbol(v.strip()) for v in variables if v and v.strip()]
    if not symbols:
        raise ValueError("Variables list cannot be empty")

    local_symbols = {str(sym): sym for sym in symbols}
    expr = sp.sympify(expression, locals=local_symbols)
    return expr, symbols


def _evaluation_subs(point: dict[str, float] | None, symbols: list[sp.Symbol]):
    if not point:
        return None
    subs = {}
    for sym in symbols:
        name = str(sym)
        if name not in point:
            raise ValueError(f"Point missing coordinate '{name}'")
        subs[sym] = point[name]
    return subs


def _parse_equation_or_expression(expression: str, symbol: sp.Symbol):
    if "=" in expression:
        left, right = expression.split("=", 1)
        left_expr = sp.sympify(left.strip())
        right_expr = sp.sympify(right.strip())
        return sp.Eq(left_expr, right_expr)
    return sp.sympify(expression)


# Unified compute endpoint for frontend
@app.post("/api/compute")
def compute(request: dict):
    """Unified compute endpoint that handles all operations.
    
    Accepts JSON body with:
    - operation: 'differentiate', 'integrate', 'matrix_multiply', etc.
    - expression: the expression or matrix
    - variable: (for differentiate/integrate) variable to differentiate/integrate
    - verbosity: 'concise', 'detailed', or 'teacher'
    - lower_limit, upper_limit: (for integrate) definite integral bounds
    - matrix_b: (for multiply) second matrix
    """
    operation = request.get("operation")
    expression = request.get("expression", "")
    variable = request.get("variable", "x")
    verbosity = request.get("verbosity", "detailed")
    matrix_b = request.get("matrix_b")
    lower_limit = request.get("lower_limit")
    upper_limit = request.get("upper_limit")
    
    if not operation:
        return {"error": "Missing 'operation' parameter"}
    
    try:
        if operation == "differentiate":
            engine = default_engine(load_entry_points=True)
            result = engine.run(operation="differentiate", expression=expression, variable=variable)
        elif operation == "integrate":
            from ..integration_engine import IntegrationEngine
            int_engine = IntegrationEngine()
            result_dict = int_engine.integrate(
                expression=expression,
                variable=variable,
                lower_limit=float(lower_limit) if lower_limit else None,
                upper_limit=float(upper_limit) if upper_limit else None,
                verbosity=verbosity
            )
            return result_dict
        elif operation.startswith("matrix_"):
            engine = default_engine(load_entry_points=True)
            if operation == "matrix_multiply" and matrix_b:
                result = engine.run(operation=operation, expression=expression, matrix_b=matrix_b)
            else:
                result = engine.run(operation=operation, expression=expression)
        else:
            return {"error": f"Unknown operation: {operation}"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = JsonRenderer()
    rendered = renderer.render(result=result, format="json", verbosity=verbosity)
    return Response(content=rendered, media_type="application/json")


@app.post("/multivariable/partial")
def multivariable_partial(req: MultivariableRequest):
    err = _validate_verbosity(req.verbosity)
    if err:
        return {"error": err}
    try:
        expr, symbols = _parse_multivariable_expression(req.expression, req.variables)
        target = symbols[0]
        derivative = sp.diff(expr, target)
        subs = _evaluation_subs(req.point, symbols)
        payload = {
            "operation": "partial_derivative",
            "input": req.expression,
            "variable": str(target),
            "variables": [str(s) for s in symbols],
            "output": str(derivative),
            "steps": [
                {
                    "rule": "Partial differentiation",
                    "before": str(expr),
                    "after": str(derivative),
                    "explanation": f"Differentiate with respect to {target} while treating other variables as constants."
                }
            ]
        }
        if subs:
            payload["evaluated_at_point"] = str(sp.N(derivative.subs(subs)))
            payload["point"] = req.point
        return Response(content=json.dumps(payload), media_type="application/json")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@app.post("/multivariable/gradient")
def multivariable_gradient(req: MultivariableRequest):
    err = _validate_verbosity(req.verbosity)
    if err:
        return {"error": err}
    try:
        expr, symbols = _parse_multivariable_expression(req.expression, req.variables)
        grad = [sp.diff(expr, s) for s in symbols]
        subs = _evaluation_subs(req.point, symbols)

        payload = {
            "operation": "gradient",
            "input": req.expression,
            "variables": [str(s) for s in symbols],
            "output": json.dumps([str(g) for g in grad]),
            "gradient": [str(g) for g in grad],
            "steps": [
                {
                    "rule": "Gradient operator",
                    "before": str(expr),
                    "after": "[" + ", ".join(str(g) for g in grad) + "]",
                    "explanation": "Compute all first-order partial derivatives to form the gradient vector."
                }
            ]
        }
        if subs:
            numeric = [str(sp.N(g.subs(subs))) for g in grad]
            payload["gradient_at_point"] = numeric
            payload["point"] = req.point
        return Response(content=json.dumps(payload), media_type="application/json")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@app.post("/multivariable/directional")
def multivariable_directional(req: MultivariableRequest):
    err = _validate_verbosity(req.verbosity)
    if err:
        return {"error": err}
    try:
        expr, symbols = _parse_multivariable_expression(req.expression, req.variables)
        if not req.point:
            return {"error": "Directional derivative requires 'point' with values for all variables"}
        if not req.direction:
            return {"error": "Directional derivative requires 'direction' vector"}
        if len(req.direction) != len(symbols):
            return {"error": "Direction vector length must match number of variables"}

        subs = _evaluation_subs(req.point, symbols)
        grad = [sp.diff(expr, s) for s in symbols]
        grad_at_point = [sp.N(g.subs(subs)) for g in grad]

        direction_vec = sp.Matrix(req.direction)
        norm = sp.sqrt(sum(c**2 for c in direction_vec))
        if norm == 0:
            return {"error": "Direction vector cannot be zero"}
        unit_direction = direction_vec / norm
        directional_value = sp.N(sp.Matrix(grad_at_point).dot(unit_direction))

        payload = {
            "operation": "directional_derivative",
            "input": req.expression,
            "variables": [str(s) for s in symbols],
            "point": req.point,
            "direction": req.direction,
            "output": str(directional_value),
            "gradient_at_point": [str(v) for v in grad_at_point],
            "unit_direction": [str(sp.N(v)) for v in unit_direction],
            "steps": [
                {
                    "rule": "Directional derivative",
                    "before": "grad(f) dot u",
                    "after": str(directional_value),
                    "explanation": "Evaluate gradient at the point and dot it with the normalized direction vector."
                }
            ]
        }
        return Response(content=json.dumps(payload), media_type="application/json")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@app.post("/multivariable/jacobian")
def multivariable_jacobian(req: dict):
    verbosity = req.get("verbosity", "detailed")
    err = _validate_verbosity(verbosity)
    if err:
        return {"error": err}
    expressions = req.get("expressions")
    variables = req.get("variables")
    point = req.get("point")
    if not expressions or not isinstance(expressions, list):
        return {"error": "Missing required field 'expressions' as a list"}
    if not variables or not isinstance(variables, list):
        return {"error": "Missing required field 'variables' as a list"}

    try:
        symbols = [sp.Symbol(v.strip()) for v in variables if v and v.strip()]
        local_symbols = {str(sym): sym for sym in symbols}
        funcs = [sp.sympify(e, locals=local_symbols) for e in expressions]
        jac = sp.Matrix(funcs).jacobian(symbols)

        payload = {
            "operation": "jacobian",
            "inputs": expressions,
            "variables": [str(s) for s in symbols],
            "output": json.dumps([[str(cell) for cell in row] for row in jac.tolist()]),
            "jacobian": [[str(cell) for cell in row] for row in jac.tolist()],
            "steps": [
                {
                    "rule": "Jacobian matrix",
                    "before": "Vector function",
                    "after": "Matrix of first-order partial derivatives",
                    "explanation": "Differentiate each component function with respect to each variable."
                }
            ]
        }

        if point:
            subs = {}
            for sym in symbols:
                name = str(sym)
                if name not in point:
                    return {"error": f"Point missing coordinate '{name}'"}
                subs[sym] = point[name]
            jac_num = jac.subs(subs)
            payload["point"] = point
            payload["jacobian_at_point"] = [[str(sp.N(cell)) for cell in row] for row in jac_num.tolist()]

        return Response(content=json.dumps(payload), media_type="application/json")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@app.post("/symbolic/compute")
def symbolic_compute(req: SymbolicRequest):
    err = _validate_verbosity(req.verbosity)
    if err:
        return {"error": err}

    operation = (req.operation or "").strip().lower()
    expression = (req.expression or "").strip()
    if not operation:
        return {"error": "Missing required field 'operation'"}
    if not expression:
        return {"error": "Missing required field 'expression'"}

    x = sp.Symbol((req.variable or "x").strip())

    try:
        parsed = _parse_equation_or_expression(expression, x)

        if operation == "algebra_simplify":
            output = sp.simplify(parsed)
            explanation = "Applied symbolic simplification rules."
        elif operation == "algebra_expand":
            output = sp.expand(parsed)
            explanation = "Expanded products and powers into polynomial form where possible."
        elif operation == "algebra_factor":
            output = sp.factor(parsed)
            explanation = "Factored the expression into irreducible symbolic factors."
        elif operation == "algebra_solve":
            if isinstance(parsed, sp.Equality):
                sols = sp.solve(parsed, x)
            else:
                sols = sp.solve(parsed, x)
            output = sols
            explanation = f"Solved for variable {x}."
        elif operation == "calculus_limit":
            if req.point is None:
                return {"error": "calculus_limit requires 'point'"}
            output = sp.limit(parsed, x, req.point)
            explanation = f"Computed limit as {x} approaches {req.point}."
        elif operation == "calculus_taylor":
            point = 0 if req.point is None else req.point
            order = max(1, min(req.order, 20))
            output = sp.series(parsed, x, point, order + 1).removeO()
            explanation = f"Computed Taylor polynomial around {x}={point} up to degree {order}."
        elif operation == "calculus_tangent_line":
            if req.point is None:
                return {"error": "calculus_tangent_line requires 'point'"}
            f_point = sp.simplify(parsed.subs(x, req.point))
            slope = sp.simplify(sp.diff(parsed, x).subs(x, req.point))
            output = sp.expand(slope * (x - req.point) + f_point)
            explanation = f"Computed tangent line at {x}={req.point} using y = f(a) + f'(a)(x-a)."
        else:
            return {"error": f"Unknown symbolic operation: {operation}"}

        payload = {
            "operation": operation,
            "input": expression,
            "variable": str(x),
            "output": str(output),
            "steps": [
                {
                    "rule": operation,
                    "before": expression,
                    "after": str(output),
                    "explanation": explanation,
                }
            ],
        }

        return Response(content=json.dumps(payload), media_type="application/json")
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


@app.get("/integrate")
def integrate(expr: str, variable: str = "x", lower_limit: float | None = None, upper_limit: float | None = None, format: str = "json", verbosity: str = "detailed"):
    """Integrate an expression with respect to a variable.
    
    Args:
        expr: Mathematical expression (e.g., 'x**2')
        variable: Variable to integrate with respect to (default: 'x')
        lower_limit: Lower bound for definite integral (optional)
        upper_limit: Upper bound for definite integral (optional)
        format: Output format ('json' or 'text')
        verbosity: Detail level ('concise', 'detailed', or 'teacher')
    
    Returns:
        Integration result with step-by-step explanation and optional graph data
    """
    if not expr or not expr.strip():
        return {"error": "Missing required parameter 'expr'. Example: ?expr=x**2"}
    
    if not variable or not variable.strip():
        return {"error": "Variable parameter cannot be empty"}
    
    if verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{verbosity}'. Valid options: concise, detailed, teacher"}
    
    from ..integration_engine import IntegrationEngine
    
    try:
        int_engine = IntegrationEngine()
        result_dict = int_engine.integrate(
            expression=expr,
            variable=variable,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            verbosity=verbosity,
            generate_graph=True
        )
        
        # Return JSON response
        import json
        return Response(content=json.dumps(result_dict), media_type="application/json")
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@app.get("/differentiate")
def differentiate(expr: str, variable: str = "x", order: int = 1, format: str = "json", verbosity: str = "detailed"):
    """Differentiate an expression with respect to a variable.
    
    Args:
        expr: Mathematical expression (e.g., 'sin(x**2)')
        variable: Variable to differentiate with respect to (default: 'x')
        order: Order of derivative (1 for first derivative, 2 for second, etc.; default: 1)
        format: Output format ('json' or 'text')
        verbosity: Detail level ('concise', 'detailed', or 'teacher')
    
    Returns:
        Differentiation result with step-by-step explanation
    """
    if not expr or not expr.strip():
        return {"error": "Missing required parameter 'expr'. Example: ?expr=sin(x**2)"}
    
    if not variable or not variable.strip():
        return {"error": "Variable parameter cannot be empty"}
    
    if order < 1:
        return {"error": f"Order must be at least 1, got {order}"}
    
    if order > 10:
        return {"error": f"Order must be at most 10, got {order}"}
    
    if verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="differentiate", expression=expr, variable=variable, order=order)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=format)
    if renderer is None:
        renderer = JsonRenderer()
        format = "json"

    rendered = renderer.render(result=result, format=format, verbosity=verbosity)
    
    # Determine media type based on format
    if format == "json":
        media_type = "application/json"
    elif format in ("latex", "tex"):
        media_type = "text/plain; charset=utf-8"
    else:
        media_type = "text/plain"
    
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/multiply")
def matrix_multiply(req: MatrixMultiplyRequest):
    """Multiply two matrices with step-by-step explanation.
    
    Args:
        req: Request body with matrix_a, matrix_b, format, verbosity
    
    Returns:
        Matrix multiplication result with step-by-step explanation
    """
    if not req.matrix_a or not req.matrix_a.strip():
        return {"error": "Missing required parameter 'matrix_a'. Example: [[1,2],[3,4]]"}
    
    if not req.matrix_b or not req.matrix_b.strip():
        return {"error": "Missing required parameter 'matrix_b'. Example: [[5,6],[7,8]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_multiply", expression=req.matrix_a, matrix_b=req.matrix_b)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/determinant")
def matrix_determinant(req: MatrixRequest):
    """Calculate the determinant of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Determinant value with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_determinant", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/inverse")
def matrix_inverse(req: MatrixRequest):
    """Calculate the inverse of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Inverse matrix with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_inverse", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/rref")
def matrix_rref(req: MatrixRequest):
    """Transform a matrix to Reduced Row Echelon Form (RREF) with step-by-step row operations.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        RREF matrix with step-by-step row operations
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2,3],[4,5,6]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_rref", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/eigenvalues")
def matrix_eigenvalues(req: MatrixRequest):
    """Calculate eigenvalues and eigenvectors of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Eigenvalues and eigenvectors with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_eigenvalues", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/lu")
def matrix_lu(req: MatrixRequest):
    """Perform LU decomposition with partial pivoting: PA = LU.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        P, L, U matrices with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_lu", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)
